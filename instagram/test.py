# -*- coding: utf-8 -*-
# Test file
# Author: Tishacy
# Date: 2021-03-26
import pandas as pd

from .query import *
from .parser import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger('test')


def test2():
    post_query = Query(PostParser)
    parsed_data, next_variables, page_info = post_query.query_batch(POSTS_QUERY_HASH_PARAM, {
        "id": "586319507",
        "first": 50,
    })
    print("Count of data: %d" % len(parsed_data))
    print(next_variables)
    print(page_info)
    print(parsed_data[-1])


def test3():
    post_query = Query(PostParser)
    data = post_query.query_all(POSTS_QUERY_HASH_PARAM, {
        "id": "586319507",
        "first": 50,
    }, None)
    print("Count of data: %d" % len(data))
    print(data[-1])


def test4():
    comment_query = Query(CommentParser)
    parsed_data, next_variables, page_info = comment_query.query_batch(COMMENTS_QUERY_HASH_PARAM, {
        "shortcode": "CMh2irVJW1b",
        "first": 50,
    })
    print("Count of data: %d" % len(parsed_data))
    print(next_variables)
    print(page_info)
    print(parsed_data[-1])


def test5():
    comment_query = Query(CommentParser)
    data = comment_query.query_all(COMMENTS_QUERY_HASH_PARAM, {
        "shortcode": "CMh2irVJW1b",
        "first": 50,
    })
    print("Count of data: %d" % len(data))
    print(data[-1])


def test6():
    post_query = Query(TagPostParser)
    comment_query = Query(CommentParser)

    post_data = post_query.query_all(TAG_POSTS_QUERY_HASH_PARAM, {
        "tag_name": "pringles",
        "first": 50,
    }, 100)
    print("Count of data: %d" % len(post_data))
    post_data_df = pd.DataFrame(post_data)
    post_data_df.to_excel('data/tag_post_data.xlsx', encoding='utf-8')

    comment_data = []
    for i, post in enumerate(post_data):
        print("Get comment of %d %s" % (i, post['short_code']))
        comment_data_of_one_post = comment_query.query_all(COMMENTS_QUERY_HASH_PARAM, {
            "shortcode": post['short_code'],
            "first": 50,
        }, 100)
        for comment in comment_data_of_one_post:
            comment['post_short_code'] = post['short_code']
        comment_data.extend(comment_data_of_one_post)
        print("Count of comment_data: %d" % len(comment_data))
    comment_data_df = pd.DataFrame(comment_data)
    comment_data_df.to_excel('data/tag_comment_data.xlsx', encoding='utf-8')


if __name__ == "__main__":
    # test2()
    # test3()
    # test4()
    test5()
    # test6()
