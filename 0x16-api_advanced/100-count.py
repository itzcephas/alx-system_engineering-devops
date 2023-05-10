#!/usr/bin/python3
""" Module for storing the count_words function. """

import requests

def count_words(subreddit, word_list, count_dict=None, after=None):
    """Recursively queries the Reddit API and counts occurrences of given keywords in hot article titles"""

    # Initialize count_dict on first call
    if count_dict is None:
        count_dict = {}

    # Base case: subreddit is invalid
    if subreddit is None:
        return

    # Set up API request
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'limit': 100}
    if after:
        params['after'] = after
    url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)

    # Send API request and handle response
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    if response.status_code != 200:
        return
    data = response.json()['data']
    after = data['after']

    # Traverse all posts on this page and count occurrences of keywords in their titles
    for post in data['children']:
        title = post['data']['title'].lower()
        for word in word_list:
            if ' ' + word.lower() + ' ' in title:
                count_dict[word.lower()] = count_dict.get(word.lower(), 0) + 1

    # Recursive call with next page of results
    if after is not None:
        count_words(subreddit, word_list, count_dict, after)

    # Print results when all pages have been processed
    elif count_dict:
        sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(word, count)
