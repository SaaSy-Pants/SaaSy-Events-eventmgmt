# router/health.py
from fastapi import APIRouter, HTTPException
from app.services.service_factory import ServiceFactory

from app.resources.event_resource import EventResource

router = APIRouter()

@router.get("/health", tags=["health"])
async def health_check():
    # Get the database service
    data_service = ServiceFactory.get_service("EventResourceDataService")
    eve_resource = EventResource(config=None)

    # Test database connection with a simple query
    try:
        result = eve_resource.get_all_events()
        return {"status": "connected", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
