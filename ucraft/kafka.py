from pprint import pprint

from confluent_kafka import Producer
import datetime
import json
import frappe

from ucraft.constants import KAFKA_BOOTSTRAP_SERVERS, KAFKA_CLIENT_ID, KAFKA_SASL_USERNAME, KAFKA_SASL_PASSWORD, \
    KAFKA_SECURITY_PROTOCOL, KAFKA_TOPIC


def send_to_kafka_async(doc, method, *args, **kwargs):
    args_to_send = {
        "doc": doc,
        "method_name": method,
        #     insert args and kwargs here
        "args": args,
        "kwargs": kwargs,
    }
    frappe.enqueue(
        method="ucraft.kafka.send_to_kafka",
        queue="short",
        **args_to_send
    )
    send_to_kafka(**args_to_send)


@frappe.whitelist()
def send_to_kafka(
        doc,
        method_name,
        *args,
        **kwargs
):
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'security.protocol': KAFKA_SECURITY_PROTOCOL,
        'sasl.mechanism': 'PLAIN',
        'sasl.username': KAFKA_SASL_USERNAME,
        'sasl.password': KAFKA_SASL_PASSWORD,
        'client.id': KAFKA_CLIENT_ID,
    }
    # Create the Kafka producer
    producer = Producer(conf)
    should_execute = False
    try:
        kafka_config = frappe.get_doc("Kafka Configuration")
        should_execute = kafka_config.should_execute(doc.doctype, method_name)
    except Exception as e:
        frappe.log("Error getting Kafka Configuration " + str(e))

    if should_execute:
        data = serialize_dates(doc.as_dict())
        final_data = {
            "doctype": doc.doctype,
            "method": method_name,
            "data": data,

        }
        data = json.dumps(final_data)
        key = get_kafka_key(doc, method_name)
        producer.produce(KAFKA_TOPIC, key=key, value=data)
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
