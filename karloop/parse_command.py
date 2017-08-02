# coding=utf-8


import sys
import logging

__author__ = 'lizhihao'


def parse_command_line(application, default):
    """ parse the command line

    :param application: the application developer created
    :param default: default port
    :return:

    """
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
