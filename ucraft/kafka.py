# from confluent_kafka import Producer
import datetime
import json
from pprint import pprint


def send_to_kafka(doc, method):
    # Convert datetime objects to strings
    data = {k: str(v) if isinstance(v, datetime.datetime) else v for k, v in doc.as_dict().items()}
    data = json.dumps(data)
    key = get_kafka_key(doc, method)


def get_kafka_key(doc, method):
    return f"{doc.doctype}-{method}-{doc.name}"
