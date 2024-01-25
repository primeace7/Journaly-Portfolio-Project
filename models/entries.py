#!/usr/bin/env python3
"""Definition of Entries representing a user's journal entry"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, Integer, String, DateTime
from datetime import datetime, timezone
from .basemodel import BaseModel, Base


class Entries(BaseModel, Base):
    """Implementation of Entries model representing a single journal entry"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    __tablename__ = 'entries'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('user.id'))
    entry = mapped_column(Text, nullable=False)
    user = relationship('User', back_populates='entries')

    def __str__(self):
        return f'Entry from user_id {self.user_id}: {self.entry}'
