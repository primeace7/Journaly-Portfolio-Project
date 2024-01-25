#!/usr/bin/env python3
"""Implement utility functions required by the app views"""
from ...models import storage
from datetime import timedelta, datetime, timezone


def fetch_user(username_email):
    """fetch a user object from the database. 

    Args:
        username_email (str): A user's username or password that will be checked
            against the details of the users in the database.

    Returns (object): a user object, or None if user doesn't exist
    """
    all_users = storage.all('User') #storage.all returns a list of dict of dicts

    found = None
    for user in all_users:
        obj = list(user)[0]
        if obj.username == username_email or obj.email == username_email:
            return obj
    return found


def current_month_insights(user_id):
    """get all of a user's insight objects for the current month and
    return them as a list of objects"""

    all_user_insights = storage.all_user_insights(user_id)
    all_insight_objs = [list(item)[0] for item in all_user_insights]

    current_date = datetime.now()
    interval = timedelta(
        days=current_date.day-1, hours=current_date.hour,
        minutes=current_date.minute, seconds=current_date.second,
        microseconds=current_date.microsecond-0.1
    )
    benchmark = current_date - interval
    current_month_insights = [obj for obj in all_insight_objs
                              if obj.created_at > benchmark]
    return current_month_insights


def current_month_entries(user_id):
    """get all of a user's entry objects for the current month and return them
    as a list of objects"""

    all_user_entries = storage.all_user_entries(user_id)
    all_entry_objs = [list(item)[0] for item in all_user_entries]

    current_date = datetime.now()
    interval = timedelta(
        days=current_date.day-1, hours=current_date.hour,
        minutes=current_date.minute, seconds=current_date.second,
        microseconds=current_date.microsecond-0.1
    )
    benchmark = current_date - interval
    current_month_entries = [
        obj for obj in all_entry_objs if obj.created_at > benchmark]

    return current_month_entries


def current_month_journals(user_obj):
    """Fetch a user's journal entries and insights for the current
    month and segment them by creation dates
    """

    this_month_entries = current_month_entries(user_obj.id)
    this_month_insights = current_month_insights(user_obj.id)
 
    all_month_data = this_month_entries
#    if len(this_month_insights) > 0:
#        all_month_data.extend(this_month_insights)

    all_month_data.sort(key=lambda obj: obj.created_at)

    segmented_entries = {}
    fmt = '%A %B %d, %Y'

    for obj in all_month_data:
        pretty_date = obj.created_at.strftime(fmt)
        if pretty_date not in segmented_entries:
            segmented_entries[pretty_date] = [obj.to_dict()]
        else:
            segmented_entries[pretty_date].append(obj.to_dict())

    return segmented_entries
