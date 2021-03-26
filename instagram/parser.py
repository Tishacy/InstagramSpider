# -*- coding: utf-8 -*-
# Entities used by query.py
# Author: Tishacy
# Date: 2021-03-26
from abc import ABC, abstractmethod
from datetime import datetime


class Parser(ABC):
    """Abstract Parser class
    A parser will parse the given data with the given variables.
    An explicit parser has to implements the following methods:
        parse_data() -> List[Dict]
        parse_next_variables() -> Dict
        parse_page_info() -> Dict
    """
    def __init__(self, data, variables):
        self.data = data
        self.variables = variables

    @abstractmethod
    def parse_data(self):
        """Parse the raw data to generate the parsed data."""
        pass

    @abstractmethod
    def parse_next_variables(self):
        """Parse the variables to generate the next variables."""
        pass

    @abstractmethod
    def parse_page_info(self):
        """Parse the raw data to get the page info."""
        pass


class PostParser(Parser):
    """A post parser"""
    def __init__(self, data, variables):
        super().__init__(data, variables)

    def parse_data(self):
        edges = self.data['data']['user']['edge_owner_to_timeline_media']['edges']

        parsed_data = []
        for edge in edges:
            node_info = self.get_info(edge['node'])
            parsed_data.append(node_info)
        return parsed_data

    def parse_next_variables(self):
        next_variable = self.variables.copy()
        next_variable['after'] = self.data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        return next_variable

    def parse_page_info(self):
        raw_page_info = self.data['data']['user']['edge_owner_to_timeline_media']['page_info']
        page_info = {
            'after_post_token': raw_page_info['end_cursor'],
            'has_next': raw_page_info['has_next_page']
        }
        return page_info

    @staticmethod
    def get_info(node):
        return {
            'id': node['id'],
            'short_code': node['shortcode'],
            'text': node['edge_media_to_caption']['edges'][0]['node']['text'],
            'display_image_url': node['display_url'],
            'timestamp': node['taken_at_timestamp'],
            'formatted-time': datetime.fromtimestamp(int(node['taken_at_timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
            'likes_count': node['edge_media_preview_like']['count'],
            'comments_count': node['edge_media_to_comment']['count']
        }


class CommentParser(Parser):
    """A comment parser"""
    def __init__(self, data, variables):
        super().__init__(data, variables)

    def parse_data(self):
        try:
            edges = self.data['data']['shortcode_media']['edge_media_to_parent_comment']['edges']

            parsed_data = []
            for edge in edges:
                node_info = self.get_info(edge['node'])
                parsed_data.append(node_info)
            return parsed_data
        except Exception:
            print(self.data)
            return []

    def parse_next_variables(self):
        next_variable = self.variables.copy()
        next_variable['after'] = self.data['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
        return next_variable

    def parse_page_info(self):
        raw_page_info = self.data['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']
        page_info = {
            'after_comment_token': raw_page_info['end_cursor'],
            'has_next': raw_page_info['has_next_page']
        }
        return page_info

    @staticmethod
    def get_info(node):
        return {
            'id': node['id'],
            'timestamp': node['created_at'],
            'formatted-time': datetime.fromtimestamp(int(node['created_at'])).strftime('%Y-%m-%d %H:%M:%S'),
            'text': node['text'],
            'username': node['owner']['username'],
            'likes_count': node['edge_liked_by']['count']
        }


class TagPostParser(Parser):
    """A tag post parser"""
    def __init__(self, data, variables):
        super().__init__(data, variables)

    def parse_data(self):
        edges = self.data['data']['hashtag']['edge_hashtag_to_media']['edges']

        parsed_data = []
        for edge in edges:
            node_info = self.get_info(edge['node'])
            parsed_data.append(node_info)
        return parsed_data

    def parse_next_variables(self):
        next_variable = self.variables.copy()
        next_variable['after'] = self.data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        return next_variable

    def parse_page_info(self):
        raw_page_info = self.data['data']['hashtag']['edge_hashtag_to_media']['page_info']
        page_info = {
            'after_post_token': raw_page_info['end_cursor'],
            'has_next': raw_page_info['has_next_page']
        }
        return page_info

    @staticmethod
    def get_info(node):
        return {
            'id': node['id'],
            'short_code': node['shortcode'],
            'text': node['edge_media_to_caption']['edges'][0]['node']['text'],
            'display_image_url': node['display_url'],
            'timestamp': node['taken_at_timestamp'],
            'formatted-time': datetime.fromtimestamp(int(node['taken_at_timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
            'likes_count': node['edge_media_preview_like']['count'],
            'comments_count': node['edge_media_to_comment']['count']
        }
