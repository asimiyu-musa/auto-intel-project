import pytest
from unittest.mock import Mock, patch
from scrapy.http import Request, Response, TextResponse
from auto_intel.spiders.auto_news import AutoNewsSpider
from auto_intel.spiders.auto_reviews import AutoReviewsSpider


class TestAutoNewsSpider:
    """Test cases for AutoNewsSpider"""

    def setup_method(self):
        """Set up test fixtures"""
        self.spider = AutoNewsSpider()

    def test_spider_name(self):
        """Test that spider has correct name"""
        assert self.spider.name == "auto_news"

    def test_allowed_domains(self):
        """Test that spider has correct allowed domains"""
        expected_domains = ["carmagazine.co.uk", "pistonheads.com", "autoexpress.co.uk"]
        assert self.spider.allowed_domains == expected_domains

    def test_start_requests(self):
        """Test that start_requests generates correct requests"""
        requests = list(self.spider.start_requests())
        
        # Should generate requests for Car Magazine (20 pages)
        car_magazine_requests = [req for req in requests if "carmagazine.co.uk" in req.url]
        assert len(car_magazine_requests) == 20
        
        # Should generate requests for PistonHeads (1 page)
        pistonheads_requests = [req for req in requests if "pistonheads.com" in req.url]
        assert len(pistonheads_requests) == 1
        
        # Should generate requests for AutoExpress (8 pages total - 4 each for car-news and consumer-issues)
        autoexpress_requests = [req for req in requests if "autoexpress.co.uk" in req.url]
        assert len(autoexpress_requests) == 8

    @patch('auto_intel.spiders.auto_news.dateparser.parse')
    def test_parse_carmagazine(self, mock_dateparser):
        """Test parsing Car Magazine articles"""
        mock_dateparser.return_value.date.return_value = "2024-01-15"
        
        # Mock response
        response = Mock(spec=TextResponse)
        response.url = "https://www.carmagazine.co.uk/car-news/"
        
        # Mock article with proper get() method that accepts default parameter
        mock_article = Mock()
        def mock_css(selector):
            mock_result = Mock()
            if selector == "h3.title a::attr(href)":
                mock_result.get.return_value = "/article1"
            elif selector == "h3.title a::text":
                mock_result.get.return_value = "Test Article"
            elif selector == "span.date::text":
                mock_result.get.return_value = "15 Jan 2024"
            elif selector == "span.author::text":
                mock_result.get.return_value = "John Doe"
            return mock_result
        
        mock_article.css.side_effect = mock_css
        response.css.return_value = [mock_article]
        response.urljoin.return_value = "https://www.carmagazine.co.uk/article1"
        
        items = list(self.spider.parse_carmagazine(response))
        
        assert len(items) == 1
        item = items[0]
        assert item['title'] == "Test Article"
        assert item['link'] == "https://www.carmagazine.co.uk/article1"
        assert item['author'] == "John Doe"
        assert item['source'] == "Car Magazine UK"

    def test_parse_method_routing(self):
        """Test that parse method routes to correct parser based on domain"""
        spider = AutoNewsSpider()
        
        # Test Car Magazine routing
        car_magazine_response = Mock(spec=TextResponse)
        car_magazine_response.url = "https://www.carmagazine.co.uk/car-news/"
        
        with patch.object(spider, 'parse_carmagazine') as mock_parse_carmagazine:
            list(spider.parse(car_magazine_response))
            mock_parse_carmagazine.assert_called_once_with(car_magazine_response)
        
        # Test PistonHeads routing
        pistonheads_response = Mock(spec=TextResponse)
        pistonheads_response.url = "https://www.pistonheads.com/news"
        
        with patch.object(spider, 'parse_pistonheads') as mock_parse_pistonheads:
            list(spider.parse(pistonheads_response))
            mock_parse_pistonheads.assert_called_once_with(pistonheads_response)
        
        # Test AutoExpress routing
        autoexpress_response = Mock(spec=TextResponse)
        autoexpress_response.url = "https://www.autoexpress.co.uk/car-news"
        
        with patch.object(spider, 'parse_autoexpress') as mock_parse_autoexpress:
            list(spider.parse(autoexpress_response))
            mock_parse_autoexpress.assert_called_once_with(autoexpress_response)


class TestAutoReviewsSpider:
    """Test cases for AutoReviewsSpider"""

    def setup_method(self):
        """Set up test fixtures"""
        self.spider = AutoReviewsSpider()

    def test_spider_name(self):
        """Test that spider has correct name"""
        assert self.spider.name == "auto_reviews"

    def test_allowed_domains(self):
        """Test that spider has correct allowed domains"""
        expected_domains = ["autoexpress.co.uk", "carbuyer.co.uk"]
        assert self.spider.allowed_domains == expected_domains

    def test_start_urls(self):
        """Test that spider has correct start URLs"""
        # Should have 60 start URLs total (30 each for autoexpress and carbuyer)
        assert len(self.spider.start_urls) == 60
        
        # Check AutoExpress URLs
        autoexpress_urls = [url for url in self.spider.start_urls if "autoexpress.co.uk" in url]
        assert len(autoexpress_urls) == 30
        
        # Check Carbuyer URLs
        carbuyer_urls = [url for url in self.spider.start_urls if "carbuyer.co.uk" in url]
        assert len(carbuyer_urls) == 30

    def test_parse_method(self):
        """Test that parse method extracts article links correctly"""
        # Mock response with proper getall() method
        response = Mock(spec=TextResponse)
        mock_css_result = Mock()
        mock_css_result.getall.return_value = ["/article1", "/article2", "https://example.com/article3"]
        response.css.return_value = mock_css_result
        response.urljoin.side_effect = lambda url: f"https://autoexpress.co.uk{url}" if url.startswith("/") else url
        response.follow = Mock()
        
        list(self.spider.parse(response))
        
        # Should call response.follow for each valid link
        assert response.follow.call_count == 3

    def test_parse_article_routing(self):
        """Test that parse_article routes to correct parser based on domain"""
        spider = AutoReviewsSpider()
        
        # Test AutoExpress routing
        autoexpress_response = Mock(spec=TextResponse)
        autoexpress_response.url = "https://www.autoexpress.co.uk/review"
        
        with patch.object(spider, 'parse_autoexpress_review') as mock_parse_autoexpress:
            list(spider.parse_article(autoexpress_response))
            mock_parse_autoexpress.assert_called_once()
        
        # Test Carbuyer routing
        carbuyer_response = Mock(spec=TextResponse)
        carbuyer_response.url = "https://www.carbuyer.co.uk/review"
        
        with patch.object(spider, 'parse_carbuyer_review') as mock_parse_carbuyer:
            list(spider.parse_article(carbuyer_response))
            mock_parse_carbuyer.assert_called_once()

    def test_parse_date(self):
        """Test date parsing functionality"""
        spider = AutoReviewsSpider()
        
        # Test valid date
        valid_date = spider.parse_date("15 Jan 2024")
        assert valid_date is not None
        
        # Test invalid date
        invalid_date = spider.parse_date("invalid date")
        assert invalid_date is None
        
        # Test None input
        none_date = spider.parse_date(None)
        assert none_date is None

    def test_extract_price(self):
        """Test price extraction functionality"""
        spider = AutoReviewsSpider()
        
        # Mock response with proper getall() method
        response = Mock(spec=TextResponse)
        mock_css_result = Mock()
        mock_css_result.getall.return_value = ["£25,000", "£30,000"]
        response.css.return_value = mock_css_result
        
        price = spider.extract_price(response)
        assert price == 25000  # Should extract first price and convert to int


class TestSpiderCompatibility:
    """Test compatibility between spiders"""

    def test_spiders_have_different_names(self):
        """Test that spiders have different names"""
        news_spider = AutoNewsSpider()
        reviews_spider = AutoReviewsSpider()
        
        assert news_spider.name != reviews_spider.name

    def test_spiders_have_different_domains(self):
        """Test that spiders target different domains"""
        news_spider = AutoNewsSpider()
        reviews_spider = AutoReviewsSpider()
        
        # Should have some overlap but not be identical
        news_domains = set(news_spider.allowed_domains)
        reviews_domains = set(reviews_spider.allowed_domains)
        
        # Both should target autoexpress.co.uk
        assert "autoexpress.co.uk" in news_domains
        assert "autoexpress.co.uk" in reviews_domains
        
        # But they should have different additional domains
        assert news_domains != reviews_domains
