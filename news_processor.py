
from celery import Celery
from celery.signals import after_setup_logger
from celery.utils.log import get_task_logger
from database_storage import session, NewsArticle
import logging
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

app = Celery('news_processor', broker='pyamqp://guest:guest@localhost//')
logger = get_task_logger(__name__)

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.handlers = []
    logger.addHandler(logging.FileHandler('app.log'))
    logger.setLevel(logging.INFO)

@app.task
def process_article(article):
    # Implementing NLP sentiment analysis to determine the category
    sentiment_score = analyze_sentiment(article['content'])
    category = classify_sentiment_category(sentiment_score)
    
    article_in_db = session.query(NewsArticle).filter_by(id=article['hash']).first()
    article_in_db.category = category
    session.commit()

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    return sentiment_score

def classify_sentiment_category(sentiment_score):
    # Classification of the article based on sentiment score
    if sentiment_score >= 0.05:
        return 'Positive/Uplifting'
    elif sentiment_score <= -0.05:
        return 'Terrorism/Protest/Political Unrest/Riot'
    else:
        return 'Others'
