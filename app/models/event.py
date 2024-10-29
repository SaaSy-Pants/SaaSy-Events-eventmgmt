from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field
from datetime import date, timedelta


class Event(BaseModel):
    EID: str = Field(..., max_length=5, description="Event ID")
    OID: str = Field(..., max_length=5, description="Organizer ID")
    Name: str
    EventCategory: str
    EventDesc: str
    Location: str
    EventDate: date
    EventTimeStart: timedelta
    EventTimeEnd: timedelta
    TicketsAvb: int = Field(..., ge=0, le=32767, description="Available Tickets (smallint)")
    Price: int = Field(..., ge=0, description="Price of the event")

    class Config:
        json_schema_extra = {
            "example": {
                "EID": "E001",
                "OID": "O001",
                "Name": "Tech Conference 2024",
                "EventCategory": "Technology",
                "EventDesc": "A conference for tech professionals to discuss the latest trends in technology.",
                "Location": "Convention Center, City",
                "EventDate": "2024-05-15",
                "EventTimeStart": "09:00:00",
                "EventTimeEnd": "17:00:00",
                "TicketsAvb": 200,
                "Price": 150
            }
        }
