"""
Created 11/15 by Dylan Lawrence
#This file will hold most/all (for now) query and response models for events
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel


class Event(BaseModel):
    """
    Base class to store an event
    """
    event_for: int
    event_name: str
    event_description: Optional[str]
    event_date: date