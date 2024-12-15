import pika
import json
from typing import Any

from framework.resources.base_resource import BaseResource
from app.models.event import Event
from app.services.service_factory import ServiceFactory

import datetime

EVENT_BOOKING_URL = "localhost"

class EventResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        # TODO -- Replace with dependency injection.
        #
        self.data_service = ServiceFactory.get_service("EventResourceDataService")
        self.database = "EVENTS"
        self.collection = "eve_tab"
        self.key_field="EID"
        # TODO -- foreign key

        # Initialize RabbitMQ connection and channel
        self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(EVENT_BOOKING_URL))
        self.channel = self.rabbitmq_connection.channel()

        # Declare the RabbitMQ exchange and queue (similar to Kafka topic)
        self.channel.exchange_declare(exchange='event_updates', exchange_type='fanout')

    def get_by_key(self, key: str) -> Event:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        result = Event(**result)
        return result
    
    def get_all_events(self, limit: int, offset: int):
        data_service = self.data_service
        result = data_service.get_data_objects(self.database, self.collection, limit, offset)
        return result
    
    def get_events_by_organizer(self, oid: str, limit: int, offset: int):
        """
        Fetch events by organizer ID (OID) with pagination.
        """
        query_filter = {"OID": oid}
        try:
            result = self.data_service.get_filtered_data_objects(
                self.database, self.collection, query_filter, limit=limit, offset=offset
            )
            return result
        except Exception as e:
            raise Exception(f"Failed to fetch events for organizer {oid}: {str(e)}")

    def insert_event(self, event: Event) -> bool:
        event_data = event.model_dump()

        try:
            result = self.data_service.insert_data_object(
                self.database, self.collection, event_data
            )
            return result
        except Exception as e:
            raise Exception(f"Failed to insert event: {str(e)}")

    def update_event(self, event_id: str, event: Event) -> bool:
        
        def convert_to_serializable(value):
            # Check if the value is of type datetime.date
            if isinstance(value, datetime.date):
                return value.isoformat()  # Convert to ISO 8601 string format
            # Check if the value is of type datetime.timedelta
            elif isinstance(value, datetime.timedelta):
                # You can convert timedelta to a string or seconds (or another suitable format)
                return str(value)  # Convert to a string like '1 day, 2:30:00'
            return value  # Return as is for other types

        event_data = event.model_dump()
        result = self.data_service.update_data_object(
            self.database, self.collection, self.key_field, event_id, event_data
        )

        serializable_event_data = {k: convert_to_serializable(v) for k, v in event_data.items()}

        print(result)

        if result:
            # After event is updated, publish an event to RabbitMQ
            message = {
                'event_id': event_id,
                'updated_data': serializable_event_data
            }
            try:
                self.channel.basic_publish(
                    exchange='event_updates',
                    routing_key='',
                    body=json.dumps(message)  # Serialize message to JSON
                )
                print(f"Event update message published to RabbitMQ for event ID: {event_id}")
            except Exception as rmq_error:
                # Log the error if publishing fails
                print(f"Failed to publish event update to RabbitMQ for event ID: {event_id}, Error: {rmq_error}")
                # Optionally, you can raise an exception here if you need to abort or handle it further
                # raise Exception(f"Failed to publish event update to RabbitMQ: {rmq_error}")

        return result

    
    def update_field(self, event_id: str, field_name: str, field_value: Any) -> bool:
        """
        Update a single field of an event in the database.

        :param event_id: ID of the event to update.
        :param field_name: The field to update.
        :param field_value: The new value for the field.
        :return: True if the update was successful, False otherwise.
        """
        try:
            update_data = {field_name: field_value}
            result = self.data_service.update_data_object(
                self.database, self.collection, self.key_field, event_id, update_data
            )
            return result
        except Exception as e:
            raise Exception(f"Failed to update field {field_name} for event {event_id}: {str(e)}")

    def delete_event(self, event_id: str) -> bool:
        result = self.data_service.delete_data_object(
            self.database, self.collection, self.key_field, event_id
        )
        return result
