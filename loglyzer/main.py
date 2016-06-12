#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import gevent.monkey
gevent.monkey.patch_all()

import settings
from receiver import RedisReceiver
from archiver import LogArchiver


def main():
    r = RedisReceiver(    # 创建一个接收器
        settings.REDIS_HOST,
        settings.REDIS_PORT,
        settings.REDIS_DB,
        settings.REDIS_FWD_PREFIX)

    for cname, processors in settings.LOG_PROCESSORS.items():  # 存储接收的信息
        for p in processors:
            t = p.pop('type')
            if t == "archive":
                for dir_name in settings.DIRS:
                    a = LogArchiver(cname.format(dirname=dir_name), local_dir=p["local_dir"].format(dirname=dir_name))      # 从队列中get数据,创建一个LogArchiver对象
                    r.register(cname.format(dirname=dir_name), a)  # 把LogArchiver对象加到channels里

    r.poll()  # 从channels取出redis数据库的keys,根据keys到数据库找相应的信息,再put到队列中


if __name__ == "__main__":
    main()

# vim: ts=4 sw=4 sts=4 expandtab
