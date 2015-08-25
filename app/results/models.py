from __future__ import absolute_import
from __future__ import unicode_literals

import json
import time

from app import db
from app.util import now


class Result:
    def __init__(self, created=None, source_ip=None, destination_ip=None, result=None):
        self.created = created
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.result = result

    def __repr__(self):
        return '<Result %r:%r>' % (self.source_ip, self.destination_ip)

    @classmethod
    def add(cls, source_ip, destination_ip, result):
        created = "%s" % now()
        new_ip = cls(
            source_ip=source_ip,
            destination_ip=destination_ip,
            result=result,
            created=created
        )

        db.set(
            "result:%s:%s:%s" % (source_ip, destination_ip, time.strftime("%Y%m%d%H%M%S", time.localtime())),
            json.dumps({
                "created": created,
                "source_ip": source_ip,
                "destination_ip": destination_ip,
                "result": result
            })
        )

        return new_ip
