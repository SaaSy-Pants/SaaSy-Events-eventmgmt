from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from datetime import datetime, date, timedelta


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
    GuestsRem: int = Field(..., ge=0, le=32767, description="Number of Guests remaining (smallint)")
    MaxGuestsPerTicket: int
    Price: int = Field(..., ge=0, description="Price of the event")

    @model_validator(mode='before')
    def serialize_fields(cls, values):
        event_date = values.get('EventDate')
        # Convert date and timedelta to strings before serialization
        if isinstance(event_date, str):
        # If EventDate is a string, convert it to a datetime object
            try:
                event_date = datetime.strptime(event_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("EventDate is not in the correct format")
        if 'EventDate' in values:
            values['EventDate'] = event_date.strftime('%Y-%m-%d')
        if 'EventTimeStart' in values:
            values['EventTimeStart'] = str(values['EventTimeStart'])
        if 'EventTimeEnd' in values:
            values['EventTimeEnd'] = str(values['EventTimeEnd'])
        return values

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
                "GuestsRem": 197,
                "MaxGuestsPerTicket": 3,
                "Price": 150
            }
        }
