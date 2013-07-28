# -*- coding: utf-8 -*-
"""
    longboxed.frontend.comics
    ~~~~~~~~~~~~~~~~~~

    Comics blueprints
"""
import sys
from datetime import datetime, timedelta

from flask import abort, Blueprint, jsonify, redirect, render_template, request, url_for
from flask.ext.login import (current_user, login_required)
from flask.ext.wtf import Form, BooleanField, SelectField, SelectMultipleField

from . import route
from ..services import comics as _comics


bp = Blueprint('comics', __name__)


@route(bp,'/comics')
def comics():
    start, end = get_current_week()
    dates = {}
    dates['today'] = end.strftime('%B %-d, %Y')
    dates['lastweek'] = start.strftime('%B %-d, %Y')
    dates['start'] = start
    dates['end'] = end
    comicList, matches = _comics.find_relevent_comics_in_date_range(start, end, current_user)
    print comicList[0].diamondid
    return render_template('comics.html', dates=dates, comicList=comicList, calendarenable=1, matches=None)


@route(bp, '/issue/<diamondid>')
def issue(diamondid):
    """Individual issue page"""
    issue = _comics.find_comic_with_diamondid(diamondid)
    if issue:
        return render_template('issue.html', issue=issue)
    return abort(404)


@route(bp, '/ajax/get_comicpage', methods=['POST'])
def get_comicpage():
    start = datetime.strptime(request.form['start'], '%B %d, %Y')
    end = datetime.strptime(request.form['end'], '%B %d, %Y')

    # comicList = find_comics_in_date_range(start, end)
    comicList, matches = _comics.find_relevent_comics_in_date_range(start, end, current_user)

    try:
        nav = render_template('comicsidenav.html', comicList=comicList)
    except:
        nav = None
    try:
        clist = render_template('comiclist.html', comicList=comicList)
    except:
        clist = None
    try:
        if matches:
            matches = render_template('favorite_matches.html', matches=matches)
    except:
        matches = None

    # return the html as json for jquery to insert
    return jsonify(nav=nav, clist=clist, matches=matches)



def get_current_week():
    today = datetime.today()
    day_of_week = today.weekday()
    to_beginning_of_week = timedelta(days=day_of_week)
    beginning_of_week = (today - to_beginning_of_week).replace(hour=0, minute=0, second=0, microsecond=0)
    to_end_of_week = timedelta(days= (6 - day_of_week))
    end_of_week = (today + to_end_of_week).replace(hour=0, minute=0, second=0, microsecond=0)
    return (beginning_of_week, end_of_week)
