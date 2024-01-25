#!/usr/bin/env python3
"""Definition of Insights to represent an insight generated from a user's entries
"""

from sqlalchemy import Text, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone, timedelta
from .basemodel import BaseModel, Base


class Insights(BaseModel, Base):
    """Implementation of Insights model representing a single
    generated insight"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dates = self.set_dates()



    __tablename__ = 'insights'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('user.id'))
    insight = mapped_column(Text, nullable=False)
    user = relationship('User', back_populates='insights')


    def set_dates(self):
        """Set default dates for the date of the first entry and the date
        of the last entry used to generate the insight
        (start_date and end_date respectively).

        By default (for autogeneration of insight), start_date is first
        day of previous month or the earliest entry date, whichever is
        most recent, while end_date is last day of previous month.
        """
        current_date = datetime.now(tz=timezone.utc)
        if getattr(self, 'user', None) is None:
            return (None, None)
        all_user_entries = getattr(self.user, 'entries', default=None)
        if all_user_entries is None:
            return (None, None)
        all_entry_dates = [obj.created_at for obj in all_user_entries]
        earliest_entry_date = min(all_entry_dates)

        if current_date.day == 1:
            default_end_date = current_date - timedelta(
                hours=current_date.hour,
                minutes=current_date.minute,
                seconds=current_date.minute,
                microseconds=0.9+current_date.microsecond
            )
            first_month_day = default_end_date - timedelta(
                days=default_end_date.day, hours=default_end_date.hour,
                minutes=default_end_date.minute,
                seconds=default_end_date.second,
                microseconds=0.000001
            )
            default_start_date = min(first_month_day, earliest_entry_date)

        result = (default_start_date.isoformat(), default_end_date.isoformat())

        return result

    def __str__(self):
        return f'Insight for user_id {self.user_id}: {self.insight}'
