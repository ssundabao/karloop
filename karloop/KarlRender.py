# coding=utf-8

__author__ = 'karl'

import datetime
import re
from karloop.base_configure import base_settings


class Render(object):
    # init method
    def __init__(self, template):
        self.template = template
        self.header = "HTTP/1.1 %s %s\r\n" \
                      "Host: %s\r\n" \
                      "Date: %s\r\n" \
                      "Connection: keep-alive\r\n" \
                      "Content-Type: text/html;charset=UTF-8\r\n" \
                      "Set-Cookie: server=run;\r\n\r\n"

    # read the template file
    def parse_template(self, value_dict=None):
        now = datetime.datetime.now()
        now_time = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        try:
            f = open(self.template)
            template_data = f.read()
            f.close()
        except IOError:
            header = self.header % (500, "template error", now_time)
            return header
        if not value_dict:
            header = self.header % (200, "OK", now_time)
            data = header + template_data
            return data
        param_list = re.findall(r"\{\{(.+?)\}\}", template_data)
        for param in param_list:
            if "." in param:
                param_object = param.split(".")[0]
                param_param = param.split(".")[1]
                object_param = value_dict[param_object]
                template_data = template_data.replace("{{%s}}" % param, str(eval("object_param."+param_param)))
            elif "[\"" in param or "['" in param:
                param_object = param.split("[")[0]
                param_key = "[" + param.split("[")[1]
                param_object = str(value_dict[param_object])
                param_value = param_object + param_key
                template_data = template_data.replace("{{%s}}" % param, eval(param_value))
            elif "[" in param:
                param_object = param.split("[")[0]
                param_value = param.replace(param_object, str(value_dict[param_object]))
                template_data = template_data.replace("{{%s}}" % param, eval(param_value))
            else:
                template_data = template_data.replace("{{%s}}" % param, value_dict[param])
        header = self.header % (200, "OK", base_settings["host"], now_time)
        data = header + template_data
        return data
