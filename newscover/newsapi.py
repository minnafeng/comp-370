import requests
from datetime import datetime, timedelta

QUERY_URL_TEMPLATE = "https://newsapi.org/v2/everything?q={}&from={}&apiKey={}"


def fetch_latest_news(api_key, news_keywords, lookback_days=10):
    """
    Queries the NewsAPI and returns a python list of english news articles
    (represented as dictionaries) containing those news keywords and published
    within the last <lookback_days>."""
    if not news_keywords:
        raise ValueError("news_keywords cannot be empty")

    # check if any non-alphabetical characters in news_keywords
    for keyword in news_keywords:
        if not keyword.isalpha():
            raise ValueError("news_keywords must contain only alphabetical characters")

    news_keywords = "+".join(news_keywords)

    # Get the date <lookback_days> ago and format it as YYYY-MM-DD
    earliest_date = datetime.now() - timedelta(days=lookback_days)
    earliest_date = earliest_date.strftime("%Y-%m-%d")

    # Query the API
    url = QUERY_URL_TEMPLATE.format(news_keywords, earliest_date, api_key)
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    articles = data["articles"]

    return articles
