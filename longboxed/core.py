# -*- coding: utf-8 -*-
"""
    longboxed.core
    ~~~~~~~~~~~~~~

    Core module contains basic classes that all applications
    depend on
"""
import werkzeug

from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security
from flask.ext.social import Social
from flask_mail import Mail
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
from sqlalchemy_imageattach.stores.s3 import S3Store

from .settings import USE_AWS, AWS_S3_BUCKET, AWS_SECRET_KEY, AWS_ACCESS_KEY_ID

#: Flask-Bootstrap extension instance
bootstrap = Bootstrap()

#: Flask-SQLAlchemy extension instance
db = SQLAlchemy()

#: Flask-Security extension instance
security = Security()

#: Flask-Social exetension instance
social = Social()

#: Flask Mail Extension Instance
mail = Mail()

#: Image Filesystem
if USE_AWS:
    store = S3Store(AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_KEY)
else:
    store = HttpExposedFileSystemStore('store', 'images')

class LongboxedError(Exception):
    """Base application error class"""

    def __init__(self, msg):
        self.msg = msg

class LongboxedFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors

class Service(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.

        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        if type(model) == werkzeug.local.LocalProxy:
            model = model._get_current_object()
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def count(self):
        """Returns the number of rows in the models table
        """
        return self.__model__.query.count()

    def save(self, model):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.__model__.query.all()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get(id)

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get_or_404(id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def filter(self, *criterion):
        """Returns a list of instances of the service's model with the specified
        criterion

        :param *ids: instance ids
        """
        return self.__model__.query.filter(*criterion).all()

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.__model__.query.filter_by(**kwargs)

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def first_or_404(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments or
        raises an 404 error if an instance with the specified id does not exist.

        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first_or_404()

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param **kwargs: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()
