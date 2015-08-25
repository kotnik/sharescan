from __future__ import absolute_import
from __future__ import unicode_literals

import flask

from app import app, api
from app.restful import Unauthorized, BadRequest, NotFound
from app.util import is_safe_url, uuid

from .models import Ip


@api.resource('/v1/ip/')
class IpResource:
    aliases = {
        'created': 'created',
        'ip': 'ip',
    }

    @api.grant()
    def list(self):
        return Ip.get_all()

    # /v1/ip/<pk>/
    @api.grant()
    def detail(self, pk):
        return Ip.get(pk)

    @api.grant()
    def create(self):
        new_ip = self.data.get("ip", None)

        # Check
        if not new_ip:
            raise BadRequest("Missing required parameter 'ip'")

        return Ip.add(ip=new_ip)
