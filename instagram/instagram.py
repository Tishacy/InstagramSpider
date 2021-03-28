# -*- coding: utf-8 -*-
# Author: Tishacy
# Date: 2021-03-26
import os
import logging
import pandas as pd

from .query import Query
from .parser import PostParser, CommentParser, TagPostParser
from .downloader import Downloader, Resource
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


def task_fetch_posts(
        author_id,
        count=28,
        posts_out='data/posts_data.xlsx'):
    """[Task] Fetch a specific number of posts of the given author and the comments
    of these posts, and save them to files.

    :param author_id: author id
    :param count: number of posts to fetch
    :param posts_out: out file of the posts data
    :return None:
    """

    # Create query instances for posts
    post_query = Query(PostParser)

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


def task_fetch_tag_posts(
        tag_name,
        count=100,
        posts_out='data/tag_posts_data.xlsx'):
    """[Task] Fetch a specific number of posts of the given tag and the comments
    of these posts, and save them to files.

    :param tag_name: tag name
    :param count: number of posts to fetch
    :param posts_out: out file of the posts data
    :return None:
    """
    # Create query instances for posts
    post_query = Query(TagPostParser)

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


def task_download_resources(data_fpath, url_field='display_image_url', out_fields=None, out_dir='pics', overwrite=False):
    """[Task] Download all pics to files.
    :param data_fpath: data file path
    :param url_field: field of pic urls in the data file.
    :param out_fields: fields of output names in the data file, using '-' to join these fields.
    :param out_dir: output directory of downloaded pics.
    :param overwrite: whether to overwrite the existing files
    :return None:
    """
    if data_fpath is None or not isinstance(data_fpath, str):
        raise ValueError("data_fpath must be a string.")

    if not os.path.exists(data_fpath):
        raise FileNotFoundError("data_fpath is not found.")

    _, ext = os.path.splitext(data_fpath)
    if ext not in ['.xls', '.xlsx']:
        raise TypeError("data_fpath must be an excel file path with the extension of .xls or .xlsx, but got %s" % ext)

    if out_fields is None:
        out_fields = ['short_code']

    data_df = pd.read_excel(data_fpath)
    resources = []
    for i, item in data_df.iterrows():
        url = item[url_field]
        if not url or pd.isna(url):
            continue
        _, ext = os.path.splitext(url.split("?")[0])
        out_fname = '-'.join([item[out_field] for out_field in out_fields]) + ext
        out = os.path.join(out_dir, out_fname)
        resources.append(Resource(url, out))

    downloader = Downloader(max_workers=100)
    downloader.download(resources)


if __name__ == "__main__":
    author_id = "1596900784"
    task_fetch_posts(author_id, 1000, f'data/{author_id}.xlsx')
    task_download_resources(f'data/{author_id}.xlsx', 'display_image_url', ['short_code'], out_dir=f'pics/{author_id}', overwrite=False)
    task_download_resources(f'data/{author_id}.xlsx', 'video_url', ['short_code'], out_dir=f'videos/{author_id}', overwrite=False)

    tag_name = 'computerscience'
    task_fetch_tag_posts(tag_name, 1000, f'data/{tag_name}.xlsx')
    task_download_resources(f'data/{tag_name}.xlsx', 'display_image_url', ['short_code'], out_dir=f'pics/{tag_name}', overwrite=False)
