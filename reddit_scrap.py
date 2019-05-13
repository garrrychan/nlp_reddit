import datetime
from time import sleep
import pandas as pd
import requests

# https://www.reddit.com/r/ShittyLifeProTips/
# https://www.reddit.com/r/LifeProTips/

def fetch_page(URL, after=''):
    '''Returns JSON of top posts of all time'''
    # URL = f'https://www.reddit.com/r/{subreddit}/top/.json?sort=top&t=all'
    headers = {'User-agent': 'webscraping bot'}
    params = {'after': after}
    r = requests.get(URL, headers=headers, params=params)
    return r.json()['data']['children']

def parse_post(post):
    '''Return a post with desired features only'''
    keep = ['subreddit', 'title', 'score', 'num_comments', 'author', "name"]
    data = post['data']
    return {k: v for k, v in data.items() if k in keep}

def parse_page(page):
    '''Return a tuple of list of posts from a page, and the name of the last post in JSON'''
    parsed_posts = []
    after = ''
    for post in page:
        p = parse_post(post)
        after = p['name']
        parsed_posts.append(p)
    # after becomes the last post's name, this is way to solve for pagination in the following function
    # e.g. https://www.reddit.com/r/lifeprotip.json?after=t3_b9073a
    return parsed_posts, after

def fetch_subreddit(URL, pages=4):
    '''Return all_posts from subreddit, of the first n pages, each page contains 25 posts'''
    all_posts = []
    after = ''
    for i in range(pages):
        print(f'Fetching Page {i + 1}')
        page = fetch_page(URL, after)
        parsed_posts, after = parse_page(page)
        all_posts.extend(parsed_posts)
        sleep(5)
    return all_posts

if __name__ == "__main__":
    ''' scrap the following subreddits '''

    all_posts = fetch_subreddit("https://www.reddit.com/r/lifeprotips/top/.json?sort=top&t=all", pages=40)
    pd.DataFrame(all_posts).to_csv("./data/lpt.csv", index=False)

    all_posts = fetch_subreddit("https://www.reddit.com/r/unethicallifeprotips/top/.json?sort=top&t=all", pages=40)
    pd.DataFrame(all_posts).to_csv("./data/unlpt.csv",index=False)
