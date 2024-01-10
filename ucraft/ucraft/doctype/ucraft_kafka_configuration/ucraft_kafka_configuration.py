# Copyright (c) 2024, Webisoft and contributors
# For license information, please see license.txt
from pprint import pprint

from confluent_kafka import Producer

# import frappe
from frappe.model.document import Document


class UcraftKafkaConfiguration(Document):

    def create_kafka_producer(self):
        # Extract the configuration details from the current instance
        # if self.disable_sync_to_kafka: TODO remove this after fixing the bug
        # if True:
        #     return False, None, None

        conf = {
            'bootstrap.servers': self.kafka_bootstrap_service,
            'security.protocol': self.kafks_security_protocol,
            'sasl.mechanism': 'PLAIN',
            'sasl.username': self.kafka_sasl_username,
            'sasl.password': self.kafka_sasl_password,
            'client.id': self.kafka_client_id,
        }

        # Create the Kafka producer
        p = Producer(conf)

        return True, p, self.kafka_topic
