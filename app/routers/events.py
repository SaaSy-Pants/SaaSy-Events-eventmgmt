from fastapi import APIRouter

from app.models.event import Event
from app.resources.event_resource import EventResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/eve_tab/{EID}", tags=["users"])
async def get_events(eid: str) -> Event:

    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("EventResource")
    result = res.get_by_key(eid)
    return result

