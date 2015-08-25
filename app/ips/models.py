from __future__ import absolute_import
from __future__ import unicode_literals

import json

from app import db
from app.util import now
from app.restful import BadRequest, NotFound


class Ip:
    def __init__(self, ip=None, created=None):
        self.ip = ip
        self.created = created

    def __repr__(self):
        return '<Ip %r>' % (self.ip)

    @classmethod
    def add(cls, ip):
        created = "%s" % now()
        new_ip = cls(ip=ip, created=created)

        if db.sismember("ips", ip):
            raise BadRequest("IP address %s already registered" % ip)
        db.sadd("ips", ip)
        db.set("ip:%s" % ip, json.dumps({"created": created}))

        return new_ip

    @classmethod
    def get(cls, ip):
        if not db.sismember("ips", ip):
            raise NotFound("IP address %s not registered" % ip)

        db_values = db.get("ip:%s" % ip)
        if not db_values:
            raise NotFound("IP address %s not registered" % ip)

        ip_info = json.loads(db_values)
        return cls(ip=ip, created=ip_info["created"])

    @classmethod
    def get_all(cls):
        result = []
        for ip in db.smembers("ips"):
            result.append(Ip.get(ip))

        return result
