SHARE Foundation Scan Project
=============================

Usage
-----

```
virtualenv venv --distribute --no-site-packages -p /usr/bin/python2
source venv/bin/activate
pip install -r requirements.txt

python manage.py runserver
```

The server should now be running on [localhost:5000](http://localhost:5000)

Testing
-------

```
curl -XGET http://localhost:5000/v1/ip/
```

```
curl -XPOST -H "Content-Type: application/json" -d '{"ip": "192.168.44.1"}' http://localhost:5000/v1/ip/
```

```
curl -XPOST -H "Content-Type: application/json" -d '{"source_ip": "192.168.44.1", "destination_ip": "192.168.5.5", "result": "xxx"}' http://localhost:5000/v1/result/
```
