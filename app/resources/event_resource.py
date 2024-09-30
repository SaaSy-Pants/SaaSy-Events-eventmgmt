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


