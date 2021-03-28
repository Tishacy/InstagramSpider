# -*- coding: utf-8 -*-
# Author: Tishacy
# Date: 2021-03-26
import logging
import requests
import json
import time

from .common import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('query')


class Query:
    """Query class of instagram api.
    :argument parser_cls: a parser class
    """
    def __init__(self, parser_cls):
        self._parser_cls = parser_cls
        self._proxies = self._init_proxies()
        self._sess = self._init_sess()
        self._base_api = "https://www.instagram.com/graphql/query/?query_hash=%s&variables=%s"

    @staticmethod
    def _init_sess():
        sess = requests.Session()
        sess.headers.update({
            'User-Agent': USER_AGENT,
            'Cookie': COOKIE
        })
        return sess

    @staticmethod
    def _init_proxies():
        proxies = {}
        if HTTP_PROXY:
            proxies['http'] = HTTP_PROXY
        if HTTPS_PROXY:
            proxies['https'] = HTTPS_PROXY
        return proxies

    def query_batch(self, query_hash, variables):
        """Query batch data.
        :param query_hash: (Str) query hash code
        :param variables: (Dict) query variables
        :rtype Tuple[List[Dict], Dict, Dict]:
        """
        dump_variables = json.dumps(variables)
        filled_api = self._base_api % (query_hash, dump_variables)

        res = self._sess.get(filled_api, proxies=self._proxies)
        data = json.loads(res.content.decode())

        while 'status' in data and data['status'] != 'ok':
            # return [], variables, { 'has_next': True }
            time.sleep(5)
            logger.info("Retrying...")
            res = self._sess.get(filled_api, proxies=self._proxies)
            data = json.loads(res.content.decode())

        parser = self._parser_cls(data, variables)
        parsed_data = parser.parse_data()
        next_variables = parser.parse_next_variables()
        page_info = parser.parse_page_info()
        return parsed_data, next_variables, page_info

    def query_all(self, query_hash, variables, total_count=None):
        """Query batch data.
        :param query_hash: (Str) query hash code
        :param variables: (Dict) query variables
        :param total_count: (Int) max number of data
        :rtype List[Dict]:
        """
        all_data = []
        parsed_data, variables, page_info = self.query_batch(query_hash, variables)
        all_data.extend(parsed_data)
        logger.info("Current count of data: %s, has next: %s" % (len(all_data), page_info['has_next']))

        while page_info['has_next']:
            parsed_data, variables, page_info = self.query_batch(query_hash, variables)
            all_data.extend(parsed_data)
            logger.info("Current count of data: %s, has next: %s" % (len(all_data), page_info['has_next']))

            if total_count and len(all_data) >= total_count:
                break

        if total_count and total_count < len(all_data):
            return all_data[:total_count]
        return all_data
