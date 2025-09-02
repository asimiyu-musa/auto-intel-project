import pytest
from auto_intel.items import ArticleItem, CarReviewItem


class TestArticleItem:
    """Test cases for ArticleItem"""

    def test_article_item_creation(self):
        """Test creating an ArticleItem with all fields"""
        item = ArticleItem(
            title="Test Article",
            link="https://example.com/article",
            author="John Doe",
            publication_date="2024-01-15",
            source="Test Source",
            content="This is test content"
        )
        
        assert item['title'] == "Test Article"
        assert item['link'] == "https://example.com/article"
        assert item['author'] == "John Doe"
        assert item['publication_date'] == "2024-01-15"
        assert item['source'] == "Test Source"
        assert item['content'] == "This is test content"

    def test_article_item_partial_creation(self):
        """Test creating an ArticleItem with minimal fields"""
        item = ArticleItem(
            title="Test Article",
            link="https://example.com/article"
        )
        
        assert item['title'] == "Test Article"
        assert item['link'] == "https://example.com/article"
        assert 'author' not in item
        assert 'publication_date' not in item
        assert 'source' not in item
        assert 'content' not in item

    def test_article_item_fields(self):
        """Test that ArticleItem has the correct field names"""
        item = ArticleItem()
        expected_fields = {'title', 'link', 'author', 'publication_date', 'source', 'content'}
        assert set(item.fields.keys()) == expected_fields


class TestCarReviewItem:
    """Test cases for CarReviewItem"""

    def test_car_review_item_creation(self):
        """Test creating a CarReviewItem with all fields"""
        item = CarReviewItem(
            title="Test Car Review",
            link="https://example.com/review",
            author="Jane Smith",
            publication_date="2024-01-15",
            source="Test Source",
            verdict="Great car!",
            rating=4.5,
            price=25000
        )
        
        assert item['title'] == "Test Car Review"
        assert item['link'] == "https://example.com/review"
        assert item['author'] == "Jane Smith"
        assert item['publication_date'] == "2024-01-15"
        assert item['source'] == "Test Source"
        assert item['verdict'] == "Great car!"
        assert item['rating'] == 4.5
        assert item['price'] == 25000

    def test_car_review_item_partial_creation(self):
        """Test creating a CarReviewItem with minimal fields"""
        item = CarReviewItem(
            title="Test Car Review",
            link="https://example.com/review"
        )
        
        assert item['title'] == "Test Car Review"
        assert item['link'] == "https://example.com/review"
        assert 'author' not in item
        assert 'publication_date' not in item
        assert 'source' not in item
        assert 'verdict' not in item
        assert 'rating' not in item
        assert 'price' not in item

    def test_car_review_item_fields(self):
        """Test that CarReviewItem has the correct field names"""
        item = CarReviewItem()
        expected_fields = {'title', 'link', 'author', 'publication_date', 'source', 'verdict', 'rating', 'price'}
        assert set(item.fields.keys()) == expected_fields

    def test_car_review_item_numeric_fields(self):
        """Test that numeric fields accept various numeric types"""
        item = CarReviewItem(
            rating=4,
            price=25000.0
        )
        
        assert item['rating'] == 4
        assert item['price'] == 25000.0
        
        # Test with string numbers (should work as Scrapy fields are flexible)
        item2 = CarReviewItem(
            rating="4.5",
            price="30000"
        )
        
        assert item2['rating'] == "4.5"
        assert item2['price'] == "30000"


class TestItemCompatibility:
    """Test compatibility between items"""

    def test_items_are_different_types(self):
        """Test that ArticleItem and CarReviewItem are different types"""
        article_item = ArticleItem()
        review_item = CarReviewItem()
        
        assert type(article_item) != type(review_item)
        assert len(article_item.fields) != len(review_item.fields)

    def test_items_have_common_fields(self):
        """Test that both items have common fields"""
        article_item = ArticleItem()
        review_item = CarReviewItem()
        
        common_fields = {'title', 'link', 'author', 'publication_date', 'source'}
        article_fields = set(article_item.fields.keys())
        review_fields = set(review_item.fields.keys())
        
        assert common_fields.issubset(article_fields)
        assert common_fields.issubset(review_fields)
