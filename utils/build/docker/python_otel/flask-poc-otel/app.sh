#!/bin/bash

opentelemetry-instrument gunicorn -w 1 -b 0.0.0.0:7777 --access-logfile - app:app -k gevent