# coding=utf-8

import sys
import asyncore
import socket
import datetime
import threading
import functools
import logging

from base_configure import base_settings
from karloop.KarlBaseRequest import BaseRequest
from karloop.KarlParseStatic import ParseStatic

__author__ = 'karl'


def async(function):
    """ async methods

    :param function: function's reference
    :return: wrapper

    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        new_thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        new_thread.start()
    return wrapper


class EchoHandler(asyncore.dispatcher):
    def __init__(self, client, addr, server, handlers, settings):
        asyncore.dispatcher.__init__(self, client)
        self.handlers = handlers
        self.settings = settings
        self.async_parse_data = None

    def handle_read(self):
        data = self.recv(1024)
        self.async_parse_data = AsyncParseData(self, data, self.handlers, self.settings)
        self.handle_write()

    def writable(self):
        return False

    def handle_write(self):
        self.async_parse_data.run()

    def handle_close(self):
        self.close()


class HTTPServer(asyncore.dispatcher):
    def __init__(self, addr, handlers, settings):
        self.handlers = handlers
        self.settings = settings
        self.addr = addr
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(self.addr)
        self.listen(5)
        print 'Listening on port %d' % addr[1]

    def handle_accept(self):
        (client, addr) = self.accept()
        print 'Request from %s:%s' % (addr[0], addr[1])
        EchoHandler(client, addr, self, self.handlers, self.settings)


class BaseApplication(object):
    settings = {}
    handlers = {}

    # init method
    def __init__(self, handlers=None, settings=None):
        """

        :param handlers: the application's settings about handlers
        :param settings: the application's configuration
        :return: None

        """
        if handlers:
            self.handlers = handlers
        if settings:
            self.settings = settings
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = base_settings["port"]
        if settings and ("ip" in settings.keys()):
            self.ip = settings["ip"]
        else:
            self.ip = ''
        base_settings["ip"] = self.ip
        if settings and ("cookie_code" in settings.keys()):
            base_settings["cookie_code"] = settings["cookie_code"]

    # listen the port and set max request number
    def listen(self, port=None):
        """ the application listen to the port that developer defined

        :param port: listen port
        :return: None

        """
        if port:
            self.port = port
        base_settings["host"] = str(self.ip) + ":" + str(self.port)

    # run the server
    def run(self):
        """ run the application

        :return: None

        """
        print "run the server on:", self.ip if self.ip else "0.0.0.0", ":", self.port
        HTTPServer((self.ip, self.port), self.handlers, self.settings)
        asyncore.loop()


class AsyncParseData(object):
    def __init__(self, connection, data, handlers, settings):
        """ init method

        :param connection: socket connection
        :param data: http data
        :param handlers: the application's settings about handlers
        :param settings: the application's configuration
        :return: None

        """
        self.connection = connection
        self.data = data
        self.parse_data = ParseData(handlers=handlers, settings=settings)

    def run(self):
        response_data = self.parse_data.parse_data(buffer_data=self.data)
        response_data_size = sys.getsizeof(response_data)
        lock_time = response_data_size / (1024 * 256)
        if len(self.data) > 4:
            response_url = self.data.split("\r\n")[0].split(" ")[1]
        else:
            response_url = ""
        if response_url.endswith(".mp3") or response_url.endswith(".ogg") or response_url.endswith(".mp4"):
            self.connection.socket.settimeout(None)
        else:
            self.connection.socket.settimeout(lock_time + 5)
        try:
            self.connection.socket.sendall(response_data)
            self.connection.socket.shutdown(socket.SHUT_RD)
        except Exception, e:
            logging.warning(e)


class ParseData(object):
    # url mapping
    handlers = {}

    # template and static files settings
    settings = {}

    # http response headers
    headers = "HTTP/1.1 %s %s\r\n" \
              "Date: %s\r\n" \
              "Host: %s\r\n" \
              "Connection: keep-alive\r\n" \
              "Content-Type: text/html;charset=UTF-8\r\n" \
              "Set-Cookie: server=run;\r\n\r\n"

    # static file name list
    static_file_extension = [
        "jpeg", "jpg", "gif", "png", "css", "js", "mp3", "ogg", "mp4",
        "JPEG", "JPG", "GIF", "PNG", "CSS", "JS", "MP3", "OGG", "MP4"
    ]

    # init method
    def __init__(self, handlers, settings):
        """ init database

        :param handlers: the application's settings about handlers
        :param settings: the application's configuration
        :return: None

        """
        self.handlers = handlers
        self.parse_static = ParseStatic(settings=settings)
        self.settings = settings

    # parse the data from client
    def parse_data(self, buffer_data):
        """ parse http data

        :param buffer_data: http data
        :return: result

        """
        now = datetime.datetime.now()
        now_time = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        if not buffer_data:
            return self.headers % (200, "OK", now_time, base_settings["host"])
        buffer_data_convert = buffer_data.split("\r\n")
        request = BaseRequest(buffer_data_convert)
        method = request.get_request_method()
        url = request.get_request_url()
        extension_name = url.split(".")[-1]
        if extension_name in self.static_file_extension:
            media_range = request.get_content_range()
            static_file_data = self.parse_static.parse_static(file_url=url, media_range=media_range)
            return static_file_data
        url_list = self.handlers.keys()
        data = request.get_http_data()
        if url not in url_list:
            response = self.headers % (404, '"request url not found"', now_time, base_settings["host"])
            response += "<p>404 ERROR</p>"
            return response
        handler = self.handlers[url]
        init_handler = handler(data, self.settings)
        try:
            function = getattr(init_handler, method)
            result = function()
        except Exception, e:
            logging.warning(e)
            response = self.headers % (500, '"server error"', now_time, base_settings["host"])
            response += "<p>500 ERROR!</p>"
            return response
        if result is None:
            response = self.headers % (405, '"request method not allowed"', now_time, base_settings["host"])
            response += "<p>405 ERROR</p>"
            return response
        return result
