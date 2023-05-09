#!/usr/bin/python3
"""
Function that queries the Reddit API and prints the titles
of the first 10 hot posts listed for a given subreddit.
"""

import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries the Reddit API and returns a list containing the titles of all hot articles for a given subreddit.
    If no results are found for the given subreddit, the function returns None.
    """
    headers = {"User-Agent": "Custom"}
    params = {"limit": 100}

    if after:
        params['after'] = after

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get("data")
        if not data:
            return None

        posts = data.get("children")
        if not posts:
            return hot_list

        for post in posts:
            hot_list.append(post.get("data").get("title"))

        after = data.get("after")
        if after:
            return recurse(subreddit, hot_list, after=after)

        return hot_list
    else:
        return None
