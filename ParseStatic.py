# coding=utf-8

__author__ = 'karl'


import datetime


class ParseStatic(object):
    # define the response head
    header = "HTTP/1.1 %s %s\r\n" \
             "Date: %s\r\n" \
             "Content-Type: %s\r\n\r\n"

    # define static file content type
    content_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "css": "text/css",
        "js": "text/js",
        "mp3": "audio/mp3",
        "ogg": "audio/ogg",
        "mp4": "video/mp4"
    }

    # init method
    def __init__(self, settings=None):
        if settings:
            self.settings = settings
        else:
            self.settings = {}

    # read the static files
    def parse_static(self, file_url):
        file_abstract_path = self.settings["static"] + file_url
        f = open(file_abstract_path)
        data = f.read()
        f.close()
        file_extension = file_url.split(".")[-1]
        now = datetime.datetime.now()
        now_time = now.strftime("%a %d %m %Y %H:%M:%S")
        content_type = self.content_type[file_extension] if (file_extension in self.content_type) else ""
        header = self.header % (200, "OK", now_time, content_type)
        header += data
        return header