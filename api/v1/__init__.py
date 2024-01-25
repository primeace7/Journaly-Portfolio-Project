#!/usr/bin/env python3

from flask import Blueprint, session, g
from .bp_status import status_handler
from .bp_login import login_handler
from .bp_register import register_handler
from .bp_all_entries import all_entries_handler
from .bp_all_insights import all_insights_handler
from .bp_journal_area import journal_area_handler
from .bp_update_user import update_user_handler
from .bp_logout import logout_handler
from .bp_generate_insights import generate_insight_handler
from ...models import storage

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

app_views.register_blueprint(status_handler)
app_views.register_blueprint(login_handler)
app_views.register_blueprint(register_handler)
app_views.register_blueprint(journal_area_handler)
app_views.register_blueprint(all_entries_handler)
app_views.register_blueprint(all_insights_handler)
app_views.register_blueprint(update_user_handler)
app_views.register_blueprint(logout_handler)
app_views.register_blueprint(generate_insight_handler)

@app_views.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user_dict = storage.get('User', user_id)
        g.user = list(user_dict)[0]
