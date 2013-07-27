# -*- coding: utf-8 -*-
"""
    longboxed.frontend
    ~~~~~~~~~~~~~~~~~~

    launchpad frontend application package
"""

from functools import wraps

from flask import render_template

from .. import factory
from . import assets


def create_app(settings_override=None):
    """Returns the Longboxed dashboard application instance"""
    app = factory.create_app(__name__, __path__, settings_override)

    # Init assets
    assets.init_app(app)

    # Register custom error handlers
    if not app.debug:
        for e in [500, 404]:
            print 'IN CREATE_APP_FRONTEND'
            # app.errorhandler(e)(handle_error)

    return app


# def handle_error(e):
#     print e
#     return render_template('errors/%s.html' % e.code), e.code


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator