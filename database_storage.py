from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    
    id = Column(String, primary_key=True)
    title = Column(String)
    content = Column(String)
    published_date = Column(DateTime)
    source_url = Column(String)
    category = Column(String, default='Others')  

engine = create_engine('sqlite:///news_articles.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def store_in_database(articles):
    for article in articles:
        if not session.query(NewsArticle).filter_by(id=article['hash']).first():
            news_article = NewsArticle(
                id=article['hash'],
                title=article['title'],
                content=article['content'],
                published_date=article['published_date'],
                source_url=article['source_url']
            )
            session.add(news_article)
            session.commit()
