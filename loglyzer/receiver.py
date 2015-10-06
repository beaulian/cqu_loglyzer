#!/usr/bin/env python2
# -*- coding:utf-8 -*-

"""
接收数据库中的处理过的日志信息
"""

import redis
import json
from datetime import datetime


class RedisReceiver(object):

    def __init__(self, host, port, db, prefix):
        self.r = redis.StrictRedis(host=host, port=port, db=db)  # 连接数据库
        self._prefix = prefix
        self.channels = {}    # 通道

    def register(self, cname, processor):
        bname = self._prefix + "buf_" + cname
        if bname not in self.channels:
            self.channels[bname] = [processor, ]   # processor为LogArchiver对象
        else:
            self.channels[bname].append(processor)

    def poll(self):
        keys = self.channels.keys()    # lgfwd_buf_nginx
        while 1:
            cname, jmsg = self.r.blpop(keys)
            msg = json.loads(jmsg)
            msg['t'] = datetime.fromtimestamp(float(msg['t']))

            if cname not in self.channels:
                continue
            for p in self.channels[cname]:
                p.push(msg)   # 调用LogArchiver类中的push方法增加msg到queue队列中


# vim: ts=4 sw=4 sts=4 expandtab
