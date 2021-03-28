# -*- coding: utf-8 -*-
# Author: Tishacy
# Date: 2021-03-26

import configparser

# Load configurations
config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")

sess_config = config['HttpSession']
query_config = config['QueryAPI']

# Global variables
# Http session
USER_AGENT = sess_config['UserAgent']
COOKIE = sess_config['Cookie']
HTTP_PROXY = sess_config['HttpProxy'] if config.has_option('HttpSession', 'HttpProxy') else None
HTTPS_PROXY = sess_config['HttpsProxy'] if config.has_option('HttpSession', 'HttpsProxy') else None

# Query api hash codes
POSTS_QUERY_HASH_PARAM = query_config['PostsQueryHash']
COMMENTS_QUERY_HASH_PARAM = query_config['CommentsQueryHash']
TAG_POSTS_QUERY_HASH_PARAM = query_config['TagPostsQueryHash']
