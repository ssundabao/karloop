# coding=utf-8

import re

__author__ = 'lizhihao'


class RegularBaseUtils(object):
    @staticmethod
    def base(string, regular):
        regex = re.compile(regular, re.IGNORECASE)
        result = re.findall(regex, string)
        return result


def is_valid_ip_address(ip, regular_expression=None):
    """ check ip address

    :param ip: ip address string
    :param regular_expression: the regular expression developer defined
    :return: bool

    """
    regular = regular_expression if regular_expression else r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    return RegularBaseUtils.base(ip, regular)


def is_valid_mobile_phone(phone, regular_expression=None):
    """ check phone number

    :param phone: cell phone number string
    :param regular_expression: the regular expression developer defined
    :return: bool

    """
    regular = regular_expression if regular_expression else r'1\d{10}'
    return RegularBaseUtils.base(phone, regular)


def is_valid_mail(mail, regular_expression=None):
    """ check mail

    :param mail: e-mail address string
    :param regular_expression: the regular expression developer defined
    :return: bool

    """
    regular = regular_expression if regular_expression else r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b"
    return RegularBaseUtils.base(mail, regular)


def is_valid_url(url, regular_expression=None):
    """

    :param url: url string
    :param regular_expression: the regular expression developer defined
    :return: bool

    """
    regular = regular_expression if regular_expression else r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return RegularBaseUtils.base(url, regular)


def is_valid_user(user_name, regular_expression=None):
    """

    :param user_name:
    :param regular_expression:
    :return:

    """
    regular = regular_expression if regular_expression else r"\b[a-zA-Z0-9._%+-]\b"
    return RegularBaseUtils.base(user_name, regular)
