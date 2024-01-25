#!/usr/bin/env python3
"""Implement the all_entries, where a user sees all their entries so far"""

from flask import g, Blueprint, redirect, url_for
from .utilities import storage

all_entries_handler = Blueprint('all_entries_handler', __name__)

@all_entries_handler.route('/<username>/all-entries',
                           strict_slashes=False)
def all_entries(username):
    """Handle the all-entries view of the application where users can
       see all their entries so far
    """
    if not g.user:
        return redirect(url_for('app_views.login_handler.login'))

    all_user_entries = storage.all_user_entries(g.user.id)
    all_entry_objs = [list(obj)[0] for obj in all_user_entries]

    all_entry_objs.sort(key=lambda obj: obj.created_at)
    segmented = segment_entries(all_entry_objs)
    return segmented


def segment_entries(entry_objs):
    """Segment a list of entry objects into a dict structure of the form:
    {'Year': {'Month': [{entry object as dict},{entry object as dict} ...]}}"""

    segmented = {}

    for obj in entry_objs:
        year = obj.created_at.year
        month = obj.created_at.strftime('%B')
        if not year in segmented:
            segmented[year] = {}
            segmented[year][month] = []
            segmented[year][month].append(obj.to_dict())
        else:
            if not month in segmented[year]:
                segmented[year][month] = []
                segmented[year][month].append(obj.to_dict())
            else:
                segmented[year][month].append(obj.to_dict())

    return segmented
