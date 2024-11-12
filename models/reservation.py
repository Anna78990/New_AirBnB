#!/usr/bin/python
""" holds class Reservation """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Reservation(BaseModel, Base):
    """Representation of a Reservation"""
    if models.storage_t == 'db':
        __tablename__ = 'reservations'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        start_date = Column(DateTime, nullable=False)
        end_date = Column(DateTime, nullable=False)

        user = relationship("User", back_populates="reservations")
        place = relationship("Place", back_populates="reservations")
    else:
        user_id = ""
        place_id = ""
        start_date = None
        end_date = None

    def __init__(self, *args, **kwargs):
        """initializes Reservation"""
        super().__init__(*args, **kwargs)
