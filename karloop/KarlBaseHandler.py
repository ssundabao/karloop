# coding=utf-8

import json
import logging
from cache_memery.cache_memery import cache
from KarlBaseResponse import BaseResponse

__author__ = 'lizhihao'


class BaseHandler(BaseResponse):
    def set_cache(self, key, value):
        """

        :param key:
        :param value:
        :return:

        """
        cache[key] = value

    def get_cache(self, key):
        """

        :param key:
        :return:

        """
        try:
            return cache[key] if key in cache.keys() else None
        except Exception, e:
            logging.error(e)
            return None

    def response_as_json(self, body=None, ensure_ascii=False):
        if not (isinstance(body, dict) and isinstance(ensure_ascii, bool)):
            raise TypeError
        response_data = json.dumps(body, ensure_ascii=ensure_ascii)
        return self.response(response_data)
