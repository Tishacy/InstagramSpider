# -*- coding: utf-8 -*-
# Author: Tishacy
# Date: 2021-03-26

import configparser

# Load configurations
config = configparser.ConfigParser()
config.read("config.ini")

sess_config = config['HttpSession']
query_config = config['QueryAPI']

# Global variables
# Http session
USER_AGENT = sess_config['UserAgent']
COOKIE = sess_config['Cookie']

# Query api hash codes
POSTS_QUERY_HASH_PARAM = query_config['PostsQueryHash']
COMMENTS_QUERY_HASH_PARAM = query_config['CommentsQueryHash']
TAG_POSTS_QUERY_HASH_PARAM = query_config['TagPostsQueryHash']
