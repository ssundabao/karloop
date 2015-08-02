# coding=utf-8

__author__ = 'lizhihao'


import sys
import logging


def parse_command_line(application, default):
    args = sys.argv
    for arg in args:
        if "--port=" in arg:
            try:
                default = arg.split("=")[1]
                default = int(default)
            except Exception, e:
                logging.error(e)
                logging.error("listen port error")
                exit()
    application.listen(default)
