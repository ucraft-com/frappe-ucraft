# Copyright (c) 2024, Webisoft and contributors
# For license information, please see license.txt
from pprint import pprint

from confluent_kafka import Producer

# import frappe
from frappe.model.document import Document


class UcraftKafkaConfiguration(Document):

    def create_kafka_producer(self):
        # Extract the configuration details from the current instance
        if self.disable_sync_to_kafka:
            return False, None, None

        kafka_bootstrap_service = self.kafka_bootstrap_service
        kafka_client_id = self.kafka_client_id
        kafka_sasl_username = self.kafka_sasl_username
        kafka_sasl_password = self.kafka_sasl_password
        kafka_security_protocol = self.kafks_security_protocol
        kafka_topic = self.kafka_topic
        pprint({
            'bootstrap.servers': kafka_bootstrap_service,
            'client.id': kafka_client_id,
            'sasl.username': kafka_sasl_username,
            'sasl.password': kafka_sasl_password,
            'security.protocol': kafka_security_protocol,
        })

        # Create the Kafka producer
        p = Producer({
            'bootstrap.servers': kafka_bootstrap_service,
            'client.id': kafka_client_id,
            'sasl.username': kafka_sasl_username,
            'sasl.password': kafka_sasl_password,
            'security.protocol': kafka_security_protocol,
        })

        return True, p, kafka_topic
