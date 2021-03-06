# -*- coding: utf-8 -*-
"""
    longboxed.frontend.pull_list
    ~~~~~~~~~~~~~~~~~~

    Pull List blueprints
"""
import sys
from json import dumps

from flask import (current_app, Blueprint, jsonify, render_template, Response,
                   request)
from flask.ext.login import current_user, login_required
from sqlalchemy import desc

from . import route
from ..forms import AddToPullList
from ..helpers import current_wednesday, next_wednesday, two_wednesdays
from ..models import Bundle, Publisher, Title


bp = Blueprint('pull_list', __name__)


@route(bp, '/pull_list', methods=['GET', 'POST'])
@login_required
def pull_list():
    form = AddToPullList()
    bundles = current_user.bundles.order_by(desc(Bundle.release_date)).limit(10)
    return render_template('pull_list.html', form=form, bundles=bundles)


@route(bp, '/ajax/typeahead')
@login_required
def typeahead():
    """
    AJAX method

    Gets title names for all titles. This should go away someday
    """
    disabled_pubs = current_app.config.get('DISABLED_PUBS', [])
    ts = Title.query.join(Title.publisher)\
                    .filter(Publisher.name.notin_(disabled_pubs))\
                    .order_by(Title.name)\
                    .all()
    titles = [
        {
            'id': title.id,
            'title': title.name,
            'publisher': title.publisher.name,
            'users': title.users.count()
        }
        for title in ts
    ]
    return Response(dumps(titles), mimetype='application/json')


@route(bp, '/ajax/remove_from_pull_list', methods=['POST'])
@login_required
def remove_from_pull_list():
    """
    AJAX method

    Remove a favorite title from your pull list
    """
    try:
        # Get the index of the book to delete
        title = Title.query.get(long(request.form['id']))
        # Delete comic at desired index
        current_user.pull_list.remove(title)
        # Save updated user
        current_user.save()
        Bundle.refresh_user_bundle(current_user, current_wednesday())
        Bundle.refresh_user_bundle(current_user, next_wednesday())
        Bundle.refresh_user_bundle(current_user, two_wednesdays())
        response = {
            'status': 'success',
            'message': title.name+' removed from your pull list'
        }
    except:
        print "Unexpected error:", sys.exc_info()[1]
        response = {
            'status': 'error',
            'message': 'Something went wrong...'
        }
    return jsonify(response)


@route(bp, '/ajax/add_to_pull_list', methods=['POST'])
@login_required
def add_to_pull_list():
    form = AddToPullList()
    response = {'status': 'fail', 'message': 'Title not being tracked by Longboxed'}
    title_id = request.form.get('id', False) # Support both adding methods
    if form.validate_on_submit() or title_id:

        if title_id:
            title = Title.query.get_or_404(title_id)
        else:
            title = Title.query.filter_by(name=request.form['title']).first_or_404()

        if title and title not in current_user.pull_list:
            current_user.pull_list.append(title)
            current_user.save()
            Bundle.refresh_user_bundle(current_user, current_wednesday())
            Bundle.refresh_user_bundle(current_user, next_wednesday())
            Bundle.refresh_user_bundle(current_user, two_wednesdays())
            response = {
                'status': 'success',
                'message': '<strong>'+title.name+'</strong> has been added to your pull list!',
                'data': {
                    'title': title.name,
                    'title_id': title.id
                }
            }
        else:
            response = {
                'status': 'fail',
                'message': '<strong>'+title.name+'</strong> is already on your pull list!',
                'data': {
                    'title': title.name,
                    'title_id': title.id
                }
            }
    return jsonify(response)
