#!/bin/bash

. venv/bin/activate
./venv/bin/gunicorn -b 0.0.0.0:8080 -k gevent --access-logfile - --error-logfile - --log-level debug --reload app:app
