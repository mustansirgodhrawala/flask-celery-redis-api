import feedparser
import requests
import os
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="create_task")
def crawler_func(ticker):
    # Base NASDAQ news url
    base_url = "https://www.nasdaq.com/feed/rssoutbound?symbol={}"

    # The NASDAQ page seems to only work with certain User Agents and times out with others.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533+ (KHTML, like Gecko)"
    }

    # Making requests with 10 seconds timeout
    try:
        data = requests.get(base_url.format(ticker), timeout=10, headers=headers)
    except requests.exceptions.Timeout:
        print("[red]Timeout, retrying[red]")
        time.sleep(5)

    # Scraping Headlines from website with feedparser.
    try:
        data = get_headlines(data)
    except Exception as e:
        print(f"[red]Could not parse because of {e}[/red]")

    # Returning Headlines
    return data


def get_headlines(data):
    # Initialized Empty List
    headlines = []
    timestamp = []

    # Using the feedparser library to work through rss feed.
    news = feedparser.parse(data.content)

    # This is the title of the RSS feed when the ticker is invalid.
    if not news.feed.title == "Latest Article Feed":

        # Using for loop to iterate through news items.
        for i in range(len(news.entries)):
            # Appending news items to list.
            headlines.append(news.entries[i].title)
            timestamp.append(news.entries[i].published)

        # Returning List of headlines and timestamps.
        return [headlines, timestamp]

    else:
        return ["Invalid Ticker Supplied."]