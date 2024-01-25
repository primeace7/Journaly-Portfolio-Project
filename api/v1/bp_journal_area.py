#!/usr/bin/env python3
"""Implement the journal area, where a user sees their entries for
   the current month and can make new entries"""

from flask import request, g, Blueprint
from .utilities import storage, current_month_insights,\
    current_month_entries, current_month_journals

journal_area_handler = Blueprint('journal_area_handler', __name__)

@journal_area_handler.route('/<username>/entries', strict_slashes=False,
                         methods=['GET', 'POST', 'PATCH', 'DELETE'])

def journal_area(username):
    """Handle the main chat area view of the application where users can
       can see their entries for the last 30 days and make new ones
    """
    if not g.user:
        return {'Error': 'User not logged in'}

    if request.method == 'GET':
        current_month_journal = current_month_journals(g.user)
        return current_month_journal

    elif request.method == 'POST':
        data = request.json
        entries_obj = storage.classes.get('Entries')
        new_entry = entries_obj(user_id=getattr(g.user, 'id'), entry=data['entry'])
        storage.add(new_entry)
        storage.save()
        latest_entry = storage.all_user_entries(g.user.id)
        latest_entry_dict = list(latest_entry[-1].values())[0]
        storage.close()
        return latest_entry_dict, 201

    elif request.method == 'PATCH':
        data = request.json
        entry_to_modify = list(storage.get('Entries', data['id']))[0]
        entry_to_modify.entry = data['entry']
        storage.add(entry_to_modify)
        storage.save()
        latest_entry = storage.all_user_entries(g.user.id)
        modified_entry_dict = list(latest_entry[-1].values())[0]
        storage.close()
        return modified_entry_dict, 201

    elif request.method == 'DELETE':
        data = request.json
        entry = list(storage.get('Entries', data['id']))
        if len(entry) == 0:
            entry_to_delete = None
        else:
            entry_to_delete = entry[0]
        storage.delete(entry_to_delete)
        storage.save()
        storage.close()
        return {'success': 'OK'}, 204
