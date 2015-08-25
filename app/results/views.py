from __future__ import absolute_import
from __future__ import unicode_literals

from app import api
from app.restful import Unauthorized, BadRequest, NotFound
from app.util import is_safe_url

from .models import Result


@api.resource('/v1/result/')
class ResultResource:
    aliases = {
        'created': 'created',
        'source_ip': 'source_ip',
        'destination_ip': 'destination_ip',
        'result': 'result'
    }

    @api.grant()
    def create(self):
        source_ip = self.data.get("source_ip", None)
        destination_ip = self.data.get("destination_ip", None)
        result = self.data.get("result", None)

        # Check
        if not source_ip:
            raise BadRequest("Missing required parameter 'source_ip'")
        if not destination_ip:
            raise BadRequest("Missing required parameter 'destination_ip'")
        if not result:
            raise BadRequest("Missing required parameter 'result'")

        return Result.add(
            source_ip=source_ip, destination_ip=destination_ip, result=result
        )
