# -*- coding: utf-8 -*-
# Downloader
# Author: Tishacy
# Date: 2021-03-27
import os
import requests
import logging
import concurrent
from concurrent.futures import ThreadPoolExecutor
from collections import Iterable

from .common import USER_AGENT, COOKIE

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('downloader')


class Downloader:
    def __init__(self, max_workers=None):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._sess = self._init_sess()

    @staticmethod
    def _init_sess():
        sess = requests.Session()
        sess.headers.update({
            'User-Agent': USER_AGENT,
            'Cookie': COOKIE
        })
        return sess

    @staticmethod
    def _split_name(url):
        if url is None:
            return "data/resource"
        return url.split("?")[0].split("/")[-1]

    def _download_item(self, url, out=None, timeout=6, overwrite=False):
        """Download a resource from url to local file.
        :param url: (str) resource url to download
        :param out: (str|None) output file path.
        :param overwrite: (bool) whether to overwrite the existing file
        :rtype Bool:
        """
        if url is None or not isinstance(url, str):
            raise ValueError("Url must be a string type.")

        if out is not None and not isinstance(out, str):
            raise ValueError("Output must be a string type.")

        out = out or self._split_name(url)

        _dir, _ = os.path.split(out)
        if not os.path.exists(_dir):
            os.makedirs(_dir)

        if os.path.exists(out) and not overwrite:
            logger.info("File %s already exists." % out)
            return True

        # Fetch resource with the given url.
        try:
            logger.info("Fetch the url: %s." % url)
            res = self._sess.get(url, timeout=timeout)

            if str(res.status_code)[0] != '2':
                return False
            content = res.content
            with open(out, 'wb') as file:
                file.write(content)
                logger.info("Saved the url to %s." % out)
            return True

        except Exception:
            logger.warning("Failed to fetch the url: %s." % url)
            return False

    def download(self, resources, overwrite=False):
        """Download a bunch of resources from url to local file.
        :param resources: (Iterable[Resource]) A sequence of Resources.
        :param overwrite: (bool) whether to overwrite the existing file
        :rtype List[Future]:
        """
        if not isinstance(resources, Iterable):
            raise ValueError("Urls must be an iterable type.")

        if len(resources) == 0:
            raise ValueError("Urls' length must be greater than 0.")

        future_to_resource = {}
        for resource in resources:
            url, out = resource.url, resource.out
            future = self._executor.submit(self._download_item, url, out, 6, overwrite)
            future_to_resource[future] = resource

        resource_to_result = {}
        for future in concurrent.futures.as_completed(future_to_resource):
            resource = future_to_resource[future]
            try:
                is_success = future.result()
                resource_to_result[resource] = is_success
                logging.info("%s result: %s" % (resource, is_success))
            except Exception as e:
                logger.warning("%s generated an exception: %s" % (resource, e))

        return resource_to_result


class Resource:
    def __init__(self, url, out):
        self.url = url
        self.out = out

    def __repr__(self):
        return "Resource{out=%s}" % self.out

    def __str__(self):
        return self.__repr__()
