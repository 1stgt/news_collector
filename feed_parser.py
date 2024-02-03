# feed_parser.py

import feedparser
import hashlib

def parse_rss_feeds(urls):
    articles = []
    
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            article = {
                'title': entry.title,
                'content': entry.summary,
                'published_date': entry.published,
                'source_url': entry.link,
                'hash': hashlib.sha256((entry.title + entry.link).encode('utf-8')).hexdigest()
            }
            articles.append(article)

    return articles
