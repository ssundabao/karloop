# coding=utf-8

__author__ = 'lizhihao'


import sys


def parse_command_line(application, default):
    args = sys.argv
    for arg in args:
        if "--port=" in arg:
            try:
                default = arg.split("=")[1]
            except Exception, e:
                print e
                print "listen port error"
                exit()
    application.listen(default)
