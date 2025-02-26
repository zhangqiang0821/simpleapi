# -*- coding: utf-8 -*-

import os
import multiprocessing

APP_NAME = "simpleapi-%s" % os.getenv('%s_NODE' % 'simpleapi'.upper(), '1')

bind = "unix:/var/run/%s.sock" % APP_NAME

# workers = multiprocessing.cpu_count()+1
workers = 1
worker_class = "gevent"
worker_connections = 2000
timeout = 60

daemon = False
pidfile = "/var/run/%s.pid" % APP_NAME
chdir = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
 
logconfig = os.path.join(os.path.dirname(__file__), "logging.ini")
loglevel = "INFO"
