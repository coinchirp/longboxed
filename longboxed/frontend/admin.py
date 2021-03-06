# -*- coding: utf-8 -*-
"""
    longboxed.frontend.admin
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Administrative interface

"""
from datetime import datetime

from flask import flash
from flask.ext.security import current_user
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.actions import action
from flask.ext.admin.babel import gettext, lazy_gettext
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.sqla.ajax import QueryAjaxModelLoader

from ..core import db
from ..helpers import current_wednesday, last_wednesday, next_wednesday
from ..models import (Creator, Issue, Publisher, Title, User, Role,
                      Bundle, DiamondList)


class LongboxedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

class AdministratorBase(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class SuperUserBase(ModelView):
    def is_accessible(self):
        return (current_user.has_role('admin') and
                current_user.has_role('super'))


class IssueAdmin(AdministratorBase):
    edit_template = 'edit_issue_model.html'
    # List of columns that can be sorted
    column_sortable_list = ('issue_number', 'complete_title', 'on_sale_date',
                            ('title',Title.name), ('publisher', Publisher.name))
    column_searchable_list = ('complete_title', 'diamond_id')
    column_list = ('on_sale_date', 'prospective_release_date', 'diamond_id',
                   'old_diamond_id', 'issue_number', 'issues', 'complete_title',
                   'title', 'publisher')
    form_excluded_columns = ('cover_image', 'bundles')

    form_ajax_refs = {
            'title': QueryAjaxModelLoader(
                'title',
                db.session,
                Title,
                fields=['name'],
                page_size=10),
            'publisher': QueryAjaxModelLoader(
                'publisher',
                db.session,
                Publisher,
                fields=['name'],
                page_size=10),
            'creators': QueryAjaxModelLoader(
                'creators',
                db.session,
                Creator,
                fields=['name'],
                page_size=10)
    }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(IssueAdmin, self).__init__(Issue, session)

    def on_model_change(self, form, model):
        """Sets last_updated attribute of issue object"""
        model.last_updated = datetime.now()
        return

    def set_on_sale_date(self, ids, date):
        try:
            issues = Issue.query.filter(Issue.id.in_(*ids)).all()
            for issue in issues:
                issue.update(**{'on_sale_date': date})
        except Exception, ex:
            flash(gettext('Failed to set date %(error)s', error=str(ex)), 'error')
        return

    @action('set_cover_image', lazy_gettext('Set Cover Image'), lazy_gettext('Are you sure you want to set the cover image?'))
    def set_cover_image(self, ids):
        try:
            issues = Issue.query.filter(Issue.id.in_(ids)).all()
            for issue in issues:
                issue.set_cover_image_from_url(issue.big_image, True)
                issue.find_or_create_thumbnail(width=250)
        except Exception, ex:
            flash(gettext('Failed to set cover image %(errors)s', error=str(ex)), 'error')
        return

    @action('current_wednesday', lazy_gettext('This Wed | %(date)s', date=current_wednesday()), lazy_gettext('Are you sure? | %(date)s', date=current_wednesday()))
    def action_current_wednesday(self, ids):
        self.set_on_sale_date(ids, current_wednesday())

    @action('next_wednesday', lazy_gettext('Next Wed | %(date)s', date=next_wednesday()), lazy_gettext('Are you sure? | %(date)s', date=next_wednesday()))
    def action_next_wednesday(self, ids):
        self.set_on_sale_date(ids, next_wednesday())

    @action('last_wednesday', lazy_gettext('Last Wed | %(date)s', date=last_wednesday()), lazy_gettext('Are you sure? | %(date)s', date=last_wednesday()))
    def action_last_wednesday(self, ids):
        self.set_on_sale_date(ids, last_wednesday())

    @action('no_date', lazy_gettext('No Date'), lazy_gettext('Are you sure? | No Date'))
    def action_no_date(self, ids):
        self.set_on_sale_date(ids, None)

class PublisherAdmin(AdministratorBase):
    def __init__(self, session):
        # Just call parent class with predefined model.
        super(PublisherAdmin, self).__init__(Publisher, session)

    form_excluded_columns = ('titles', 'comics')
    form_ajax_refs = {
        'users': QueryAjaxModelLoader(
            'users',
            db.session,
            User,
            fields=['email'],
            page_size=10),
    }


class TitleAdmin(AdministratorBase):
    column_sortable_list= ('name', ('publisher', Publisher.name))
    def __init__(self, session):
        # Just call parent class with predefined model.
        super(TitleAdmin, self).__init__(Title, session)

    form_ajax_refs = {
        'users': QueryAjaxModelLoader(
            'users',
            db.session,
            User,
            fields=['email'],
            page_size=10),
        'issues': QueryAjaxModelLoader(
            'issues',
            db.session,
            Issue,
            fields=['complete_title'],
            page_size=10),
        'publisher': QueryAjaxModelLoader(
            'publisher',
            db.session,
            Publisher,
            fields=['name'],
            page_size=10)
    }


class CreatorAdmin(AdministratorBase):
    def __init__(self, session):
        # Just call parent class with predefined model.
        super(CreatorAdmin, self).__init__(Creator, session)

    form_excluded_columns = ('issues')


class BundleAdmin(AdministratorBase):
    def __init__(self, session):
        # Just call parent class with predefined model.
        super(BundleAdmin, self).__init__(Bundle, session)

    form_ajax_refs = {
        'issues': QueryAjaxModelLoader(
            'issues',
            db.session,
            Issue,
            fields=['complete_title'],
            page_size=10),
        'user': QueryAjaxModelLoader(
            'user',
            db.session,
            User,
            fields=['email'],
            page_size=10)
    }


class UserAdmin(SuperUserBase):
    column_list = ('email', 'last_seen', 'login_count', 'pull_list', 'roles')
    column_searchable_list = ('email',)

    form_excluded_columns = ('bundles',)
    form_ajax_refs = {
        'pull_list': QueryAjaxModelLoader(
            'pull_list',
            db.session,
            Title,
            fields=['name'],
            page_size=10)
    }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(UserAdmin, self).__init__(User, session)


class RoleAdmin(SuperUserBase):
    def __init__(self, session):
        # Just call parent class with predefined model.
        super(RoleAdmin, self).__init__(Role, session)

    form_ajax_refs = {
        'users': QueryAjaxModelLoader(
            'users',
            db.session,
            User,
            fields=['email'],
            page_size=10)
    }


class DiamondListAdmin(SuperUserBase):
    def __init__(self, session):
        super(DiamondListAdmin, self).__init__(DiamondList, session)

    form_ajax_refs = {'issues': QueryAjaxModelLoader('issues', db.session,
        Issue, fields=['complete_title'], page_size=10)}
    column_list = ('date_created', 'date', 'revision', 'hash_string',)
    form_ajax_refs = {
        'issues': QueryAjaxModelLoader(
            'issues',
            db.session,
            Issue,
            fields=['complete_title'],
            page_size=10),
    }

def init_app(app):
    admin = Admin(app, index_view=LongboxedAdminIndexView())
    admin.add_view(UserAdmin(db.session))
    admin.add_view(IssueAdmin(db.session))
    admin.add_view(PublisherAdmin(db.session))
    admin.add_view(TitleAdmin(db.session))
    admin.add_view(CreatorAdmin(db.session))
    admin.add_view(RoleAdmin(db.session))
    admin.add_view(BundleAdmin(db.session))
    admin.add_view(DiamondListAdmin(db.session))
