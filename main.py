from feed_parser import parse_rss_feeds
from news_processor import process_article

rss_feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
]

articles = parse_rss_feeds(rss_feeds)

for article in articles:
    process_article.delay(article)
