from datetime import datetime, timedelta
import pytest

from newscover.newsapi import fetch_latest_news


class TestNewsApi:
    API_KEY = "insert-key-here"

    def test_no_news_keywords(self):
        """Test that API raises an exception if news_keywords parameter is empty."""
        with pytest.raises(ValueError):
            fetch_latest_news(self.API_KEY, [])

    def test_within_lookback_days(self):
        """Test that API returns news articles within the lookback_days."""
        articles = fetch_latest_news(self.API_KEY, ["trump"], lookback_days=2)

        after_date = datetime.now() - timedelta(days=3)

        for article in articles:
            publish_date = datetime.strptime(
                article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
            assert publish_date > after_date

    def test_non_alpha_char(self):
        """Test that API fails when keyword contains non-alphabetic character."""
        with pytest.raises(ValueError):
            fetch_latest_news(self.API_KEY, ["trump!"])
