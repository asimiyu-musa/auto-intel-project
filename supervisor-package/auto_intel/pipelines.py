import psycopg2
from decouple import config
from itemadapter import ItemAdapter
from pydantic import ValidationError
from scrapy.exceptions import DropItem

from .items import ArticleItem, CarReviewItem
from .models import ArticleModel, CarReviewModel


class PostgresPipeline:
    def open_spider(self, spider):
        """Connect to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                host=config('POSTGRES_HOST'),
                dbname=config('POSTGRES_DB'),
                user=config('POSTGRES_USER'),
                password=config('POSTGRES_PASSWORD')
            )
            self.cursor = self.connection.cursor()
            spider.logger.info("✅ Database connection established.")
        except (psycopg2.OperationalError, Exception) as e:
            spider.logger.critical(f"❌ DATABASE CONNECTION FAILED: {e}")
            raise e

    def close_spider(self, spider):
        """Close the database connection."""
        self.cursor.close()
        self.connection.close()
        spider.logger.info("✅ Database connection closed.")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        try:
            if isinstance(item, ArticleItem):
                # 1. Validate the item using the Pydantic model
                validated_data = ArticleModel(**adapter.asdict())
                
                # 2. Insert the validated data
                self.cursor.execute("""
                    INSERT INTO article_news (title, link, author, publication_date, source, content)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO NOTHING;
                """, (
                    validated_data.title,
                    str(validated_data.link),
                    validated_data.author,
                    validated_data.publication_date,
                    validated_data.source,
                    validated_data.content, # <-- ADD THIS VALUE
                ))
            
            elif isinstance(item, CarReviewItem):
                # 1. Validate the item using the Pydantic model
                validated_data = CarReviewModel(**adapter.asdict())
                
                # 2. Insert the validated data
                self.cursor.execute("""
                    INSERT INTO car_reviews (title, link, author, publication_date, source, verdict, rating, price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO NOTHING;
                """, (
                    validated_data.title,
                    str(validated_data.link),
                    validated_data.author,
                    validated_data.publication_date,
                    validated_data.source,
                    validated_data.verdict,
                    validated_data.rating,
                    validated_data.price
                ))

            # Commit the transaction to the database
            self.connection.commit()
            spider.logger.info(f"✅ Item stored: {adapter.get('title')}")
            return item

        except ValidationError as e:
            # Pydantic validation failed
            self.connection.rollback()
            spider.logger.error(f"❌ Pydantic Validation Failed for {adapter.get('link')}: {e}")
            raise DropItem(f"Validation failed for item: {adapter.get('title')}")

        except psycopg2.Error as e:
            # Database insertion failed
            self.connection.rollback()
            spider.logger.error(f"❌ DB Insert Failed for {adapter.get('link')}: {e}")
            raise DropItem(f"Database error for item: {adapter.get('title')}")