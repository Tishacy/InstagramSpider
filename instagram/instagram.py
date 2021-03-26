# -*- coding: utf-8 -*-
# Author: Tishacy
# Date: 2021-03-26
import pandas as pd
import logging

from .query import Query
from .parser import PostParser, CommentParser, TagPostParser
from .common import POSTS_QUERY_HASH_PARAM, \
    COMMENTS_QUERY_HASH_PARAM, TAG_POSTS_QUERY_HASH_PARAM


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('instagram')


def task_fetch_posts_and_comments(
        author_id,
        count=28,
        posts_out='data/posts_data.xlsx',
        comments_out='data/comments_data.xlsx'):
    """[Task] Fetch a specific number of posts of the given author and the comments
    of these posts, and save them to files.

    :param author_id: author id
    :param count: number of posts to fetch
    :param posts_out: out file of the posts data
    :param comments_out: out file of the comments data
    :return None:
    """

    # Create query instances for posts and comments
    post_query = Query(PostParser)
    comment_query = Query(CommentParser)

    # Query posts data
    post_data = post_query.query_all(POSTS_QUERY_HASH_PARAM, {
        "id": author_id,
        "first": 50,
    }, count)
    logger.info("Count of posts data: %d" % len(post_data))

    # Save the posts data
    post_data_df = pd.DataFrame(post_data)
    post_data_df.to_excel(posts_out, encoding='utf-8', index=False)
    logger.info("Save the posts data to %s." % posts_out)

    # Query comments data of posts
    comment_data = []
    for i, post in enumerate(post_data):
        logger.info("Get comment of %d %s" % (i, post['short_code']))
        comment_data_of_one_post = comment_query.query_all(COMMENTS_QUERY_HASH_PARAM, {
            "shortcode": post['short_code'],
            "first": 50,
        }, None)
        for comment in comment_data_of_one_post:
            comment['post_short_code'] = post['short_code']
        comment_data.extend(comment_data_of_one_post)
        logger.info("Count of comment_data: %d" % len(comment_data))

    # Save the comments data
    comment_data_df = pd.DataFrame(comment_data)
    comment_data_df.to_excel(comments_out, encoding='utf-8', index=False)
    logger.info("Save the comments data to %s." % comments_out)


def task_fetch_tag_posts_and_comments(
        tag_name,
        count=100,
        posts_out='data/tag_posts_data.xlsx',
        comments_out='data/tag_comments_data.xlsx'):
    """[Task] Fetch a specific number of posts of the given tag and the comments
    of these posts, and save them to files.

    :param tag_name: tag name
    :param count: number of posts to fetch
    :param posts_out: out file of the posts data
    :param comments_out: out file of the comments data
    :return None:
    """

    # Create query instances for posts and comments
    post_query = Query(TagPostParser)
    comment_query = Query(CommentParser)

    # Query posts data
    post_data = post_query.query_all(TAG_POSTS_QUERY_HASH_PARAM, {
        "tag_name": tag_name,
        "first": 50,
    }, count)
    logger.info("Count of posts data: %d" % len(post_data))

    # Save the posts data
    post_data_df = pd.DataFrame(post_data)
    post_data_df.to_excel(posts_out, encoding='utf-8', index=False)
    logger.info("Save the posts data to %s." % posts_out)

    # Query comments data of posts
    comment_data = []
    for i, post in enumerate(post_data):
        logger.info("Get comment of %d %s" % (i, post['short_code']))
        comment_data_of_one_post = comment_query.query_all(COMMENTS_QUERY_HASH_PARAM, {
            "shortcode": post['short_code'],
            "first": 50,
        }, 100)
        for comment in comment_data_of_one_post:
            comment['post_short_code'] = post['short_code']
        comment_data.extend(comment_data_of_one_post)
        logger.info("Count of comment_data: %d" % len(comment_data))

    # Save the comments data
    comment_data_df = pd.DataFrame(comment_data)
    comment_data_df.to_excel(comments_out, encoding='utf-8', index=False)
    logger.info("Save the comments data to %s." % comments_out)


if __name__=="__main__":
    task_fetch_posts_and_comments("586319507", 28, 'data/posts_data.xlsx', 'data/comments_data.xlsx')
    task_fetch_tag_posts_and_comments("pringles", 100, 'data/tag_posts_data.xlsx', 'data/tag_comments_data.xlsx')
