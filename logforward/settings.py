#!/usr/bin/env python2
# -*- coding:utf-8 -*-

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0

REDIS_PREFIX = "lgfwd_"

LOG_SOURCES = {
    '{dirname}': {
        'type': "file",
        "filename": "/var/log/nginx/yiban/{dirname}/access.log",
    },
    'rsync': {
        'type': "systemd-journal",
        "unitname": "rsync.service",
    }
}

DIRS = ["card", "library", "icqu", "found"]

try:
    from settings_local import *
except:
    pass

# vim: ts=4 sw=4 sts=4 expandtab
