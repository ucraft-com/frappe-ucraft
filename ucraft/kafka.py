from confluent_kafka import Producer
import datetime
import json

import frappe


def send_to_kafka(doc, method):
    try:
        kafka_config = frappe.get_doc(
            "Ucraft Kafka Configuration",
        )
    except:
        return
    should_execute, producer, topic = kafka_config.create_kafka_producer()
    if should_execute:
        data = {k: str(v) if isinstance(v, datetime.datetime) else v for k, v in doc.as_dict().items()}
        data = json.dumps(data)
        key = get_kafka_key(doc, method)
        producer.produce(topic, key=key, value=data)
        print(f"Sent {data} to Kafka topic {topic} with key {key}")
        producer.flush()


def get_kafka_key(doc, method):
    return f"{doc.doctype}-{method}-{doc.name}"
