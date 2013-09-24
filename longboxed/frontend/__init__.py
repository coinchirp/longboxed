# -*- coding: utf-8 -*-
"""
    longboxed.frontend
    ~~~~~~~~~~~~~~~~~~

    launchpad frontend application package
"""

from flask.ext.debugtoolbar import DebugToolbarExtension
from functools import wraps

from .. import factory
from . import assets
from . import admin


def create_app(settings_override=None):
    """Returns the Longboxed dashboard application instance"""
    app = factory.create_app(__name__, __path__, settings_override)

    # Init assets
    assets.init_app(app)
    # Flask-Admin
    admin.init_app(app)

    # Flask-DebugToolbar
    DebugToolbarExtension(app)

    # Register custom error handlers
    if not app.debug:
        for e in [500, 404]:
            pass
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
