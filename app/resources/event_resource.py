from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.event import Event
from app.services.service_factory import ServiceFactory


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
        event_data = event.model_dump()
        result = self.data_service.update_data_object(
            self.database, self.collection, self.key_field, event_id, event_data
        )
        return result

    def delete_event(self, event_id: str) -> bool:
        result = self.data_service.delete_data_object(
            self.database, self.collection, self.key_field, event_id
        )
        return result
