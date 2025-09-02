# This file makes the spiders directory a Python package

# Explicitly import spiders to ensure they are discovered by Scrapy
from .auto_news import AutoNewsSpider
from .auto_reviews import AutoReviewsSpider

__all__ = ['AutoNewsSpider', 'AutoReviewsSpider'] 