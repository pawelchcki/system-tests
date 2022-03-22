# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

import unittest
import urllib
import string
import random

import requests

from utils.tools import logger, m


class _FailedResponse:
    def __init__(self, request):
        self.request = request
        self.status_code = None


class BaseTestCase(unittest.TestCase):
    _weblog_url_prefix = "http://weblog:7777"

    def weblog_get(self, path="/", params=None, headers=None, cookies=None, **kwargs):
        return self._weblog_request("GET", path, params=params, headers=headers, cookies=cookies, **kwargs)

    def weblog_post(self, path="/", params=None, data=None, headers=None, **kwargs):
        return self._weblog_request("POST", path, params=params, data=data, headers=headers, **kwargs)

    def _weblog_request(self, method, path="/", params=None, data=None, headers=None, stream=None, **kwargs):
        # rid = str(uuid.uuid4()) Do NOT use uuid, it sometimes can looks like credit card number
        rid = "".join(random.choices(string.ascii_uppercase, k=36))
        headers = headers or {}

        user_agent_key = "User-Agent"
        for k in headers:
            if k.lower() == "user-agent":
                user_agent_key = k
                break

        user_agent = headers.get(user_agent_key, "system_tests")
        headers[user_agent_key] = f"{user_agent} rid/{rid}"

        if method == "GET" and params:
            url = self._get_weblog_url(path, params)
        else:
            url = self._get_weblog_url(path)

        try:
            req = requests.Request(method, url, params=params, data=data, headers=headers, **kwargs)
            r = req.prepare()
            r.url = url
            logger.debug(f"Sending request {rid}: {method} {url}")

            r = requests.Session().send(r, timeout=5, stream=stream)
        except Exception as e:
            logger.error(f"Request {rid} raise an error: {e}")
            return _FailedResponse(request=r)

        logger.debug(f"Request {rid}: {r.status_code}")

        return r

    def _get_weblog_url(self, path, query=None):
        """ Return a query with the passed host
        """
        # Make all absolute paths to be relative
        if path.startswith("/"):
            path = path[1:]

        res = self._weblog_url_prefix + "/" + path  # urllib.parse.urljoin(self._weblog_url_prefix, path)

        if query:
            res += "?" + urllib.parse.urlencode(query)

        return res
