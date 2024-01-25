#!/usr/bin/env python3
"""Definition of user class to represent an application user"""

from .basemodel import Base, BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text
from typing import List
from datetime import datetime, timezone


class User(BaseModel, Base):
    """Implementation of user model representing an application user"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username = mapped_column(String(20), nullable=False, unique=True)
    firstname = mapped_column(String(50), nullable=False)
    lastname = mapped_column(String(50))
    email = mapped_column(String(50), nullable=False, unique=True)
    password = mapped_column(Text, nullable=False)
    entries: Mapped[List["Entries"]] = relationship(
        back_populates='user',cascade="all, delete, delete-orphan"
    )
    insights: Mapped[List["Insights"]] = relationship(
        back_populates='user', cascade="all, delete, delete-orphan"
    )
