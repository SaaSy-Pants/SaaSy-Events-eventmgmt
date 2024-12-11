from fastapi import APIRouter, HTTPException, Query

from app.models.event import Event
from app.resources.event_resource import EventResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/events/{eid}", tags=["events"])
async def get_event(eid: str) -> Event:
    res = ServiceFactory.get_service("EventResource")
    result = res.get_by_key(eid)
    return result


@router.get("/events", tags=["events"])
async def get_events(limit: int = Query(10, description="Number of items per page"), 
                     offset: int = Query(0, description="Offset for pagination")):
    eve_resource = EventResource(config=None)
    try:
        result = eve_resource.get_all_events(limit=limit, offset=offset)
        return {"status": "connected", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


@router.post("/events", tags=["event"])
async def create_event(event: Event):
    eve_resource = EventResource(config=None)
    try:
        success = eve_resource.insert_event(event)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create the event")
        return {"message": "Event created successfully", "EID": event.EID}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event creation failed: {str(e)}")


@router.put("/events", tags=["event"])
async def update_event(event: Event):
    eve_resource = EventResource(config=None)
    try:
        success = eve_resource.update_event(event.EID, event)
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event updated successfully", "EID": event.EID}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event update failed: {str(e)}")

@router.patch("/events/{eid}/guests_remaining", tags=["event"])
async def update_guests_remaining(eid: str, guests_remaining: int):
    """
    Update the guests_remaining field of an event.
    :param eid: Event ID to update.
    :param guests_remaining: New value for guests_remaining.
    """
    eve_resource = EventResource(config=None)
    try:
        # Ensure guests_remaining is a non-negative integer
        if guests_remaining < 0:
            raise HTTPException(status_code=400, detail="guests_remaining cannot be negative")

        success = eve_resource.update_field(eid, "GuestsRem", guests_remaining)
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")

        return {
            "message": "Guests remaining updated successfully",
            "EID": eid,
            "guests_remaining": guests_remaining
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Guests remaining update failed: {str(e)}")

@router.get("/events/organizer/{oid}", tags=["events"])
async def get_events_by_organizer(oid: str, 
                                  limit: int = Query(10, description="Number of items per page"), 
                                  offset: int = Query(0, description="Offset for pagination")):
    """
    Fetch all events belonging to a particular organizer (OID) with pagination.
    """
    eve_resource = EventResource(config=None)
    try:
        events = eve_resource.get_events_by_organizer(oid, limit=limit, offset=offset)
        return {"status": "connected", "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch events: {str(e)}")


@router.delete("/events/{EID}", tags=["event"])
async def delete_event(eid: str):
    eve_resource = EventResource(config=None)
    try:
        success = eve_resource.delete_event(eid)
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event deletion failed: {str(e)}")