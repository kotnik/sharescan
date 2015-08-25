from __future__ import absolute_import
from __future__ import unicode_literals

from restless.fl import FlaskResource
from restless.preparers import FieldsPreparer
from restless.exceptions import BadRequest, NotFound, Unauthorized
from .http_errors import PreconditionFailed, PreconditionRequired
import six

# Abstract the exceptions
BadRequest = BadRequest
NotFound = NotFound
Unauthorized = Unauthorized
PreconditionRequired = PreconditionRequired
PreconditionFailed = PreconditionFailed


class Resource(FlaskResource):
    def __init__(self, api):
        self.api = api
        self.app = api.app
        self.auth = api.auth

    def is_debug(self):
        return self.app.debug

    def bubble_exceptions(self):
        return self.app.config.get('TESTING')

    def prepare(self, data):
        # ``data`` is the object/dict to be exposed.
        # We'll call ``super`` to prep the data, then we'll mask the email.
        prepped = super(Resource, self).prepare(data)

        # Remove empty values from response
        not_null_data = dict()
        for k, v in six.iteritems(prepped):
            if v:
                not_null_data[k] = v

        return not_null_data

    def is_authenticated(self):
        if not self.auth:
            return True


class Api:
    """Provides an abstraction from the rest API framework being used"""

    def __init__(self, app=None, auth=None):
        if app:
            self.init_app(app, auth)

    def init_app(self, app, auth=None):
        self.app = app
        self.auth = auth

    def public(self, view):
        """Define the class method as public.

        Otherwise, if auth is defined all methods require
        the user to be authenticated
        """
        view.public = True
        return view

    def grant(self, *roles):
        """Grant method authorization to the specified roles"""
        def view(fn):
            fn.roles = roles
            return fn

        return view

    def resource(self, prefix):
        """Decorator to simplify API creation.

        The same rules as in restless apply (see http://restless.readthedocs.org/en/latest/tutorial.html)

        However to define a resource it suffices with using the decorator to specify it

        @api.resource('/api/posts')
        class PostResource:
            aliases = {
                'id': 'id',
                'title': 'title',
                'author': 'user.username',
                'body': 'content',
                'posted_on': 'posted_on',
            }

            def detail(self, pk):
                return Post.objects.get(id=pk)
        """
        def wrapper(cls):
            # Save the original init
            clsinit = getattr(cls, '__init__', lambda self: None)

            # Dirty trick, make the class belong to the type restful.Resource
            cls = type(cls.__name__, (Resource,), dict(cls.__dict__))

            aliases = getattr(cls, 'aliases', None)
            if isinstance(aliases, dict) and len(aliases) > 0:
                cls.preparer = FieldsPreparer(fields=aliases)

            # Rename self for using inside __init__
            api = self

            def __init__(self, *args, **kwargs):
                # Call Resource constructor
                super(cls, self).__init__(api)

                # Initialize the instance
                clsinit(self, *args, **kwargs)

            cls.__init__ = __init__

            # Add the resource to the API
            cls.add_url_rules(self.app, prefix)

            return cls

        return wrapper
