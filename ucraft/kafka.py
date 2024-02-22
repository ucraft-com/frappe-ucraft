from pprint import pprint

from confluent_kafka import Producer
import datetime
import json

import frappe

from threading import Thread


def send_to_kafka_async(doc, method, *args, **kwargs):
    args_to_send = {
        "doc": doc,
        "method_name": method,
        #     insert args and kwargs here
        "args": args,
        "kwargs": kwargs,
    }
    print("Sending to Kafka")
    return

    frappe.enqueue(
        method="ucraft.kafka.send_to_kafka",
        queue="short",
        **args_to_send
    )


@frappe.whitelist()
def send_to_kafka(
        doc,
        method_name,
        *args,
        **kwargs
):
    try:
        kafka_config = frappe.get_doc(
            "Kafka Configuration",
        )
    except:
        return
    should_execute, producer, topic = kafka_config.create_kafka_producer()
    doc_name = doc.as_dict().get("name", "")

    if method_name not in kafka_config.get_active_events_list():
        should_execute = False

    if should_execute:
        data = serialize_dates(doc.as_dict())
        final_data = {
            "doctype": doc.doctype,
            "method": method_name,
            "data": data,

        }
        data = json.dumps(final_data)

        key = get_kafka_key(doc, method_name)
        producer.produce(topic, key=key, value=data)
        producer.flush()


def get_kafka_key(doc, method):
    return f"{doc.doctype}-{method}"


def serialize_dates(obj):
    """
    Recursively convert datetime and date objects in a dictionary to their string representation.
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_dates(v) for v in obj]
    else:
        return obj
