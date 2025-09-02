"""
Data loader module for Auto Intel Project
Handles loading and preprocessing of scraped data from CSV files
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Loads and preprocesses scraped automotive data"""
    
    def __init__(self, article_news_path: str, car_reviews_path: str):
        """
        Initialize DataLoader with paths to CSV files
        
        Args:
            article_news_path: Path to article_news CSV file
            car_reviews_path: Path to car_reviews CSV file
        """
        self.article_news_path = article_news_path
        self.car_reviews_path = car_reviews_path
        self.article_news_df = None
        self.car_reviews_df = None
        
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load both datasets from CSV files
        
        Returns:
            Tuple of (article_news_df, car_reviews_df)
        """
        try:
            logger.info("Loading article news data...")
            self.article_news_df = pd.read_csv(self.article_news_path)
            logger.info(f"Loaded {len(self.article_news_df)} article news records")
            
            logger.info("Loading car reviews data...")
            self.car_reviews_df = pd.read_csv(self.car_reviews_path)
            logger.info(f"Loaded {len(self.car_reviews_df)} car review records")
            
            return self.article_news_df, self.car_reviews_df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def preprocess_article_news(self) -> pd.DataFrame:
        """
        Preprocess article news data
        
        Returns:
            Preprocessed article news DataFrame
        """
        if self.article_news_df is None:
            self.load_data()
            
        df = self.article_news_df.copy()
        
        # Convert publication_date to datetime
        df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
        
        # Clean text fields
        df['title'] = df['title'].astype(str).str.strip()
        df['content'] = df['content'].astype(str).str.strip()
        df['author'] = df['author'].astype(str).str.strip()
        df['source'] = df['source'].astype(str).str.strip()
        
        # Remove rows with missing essential data
        df = df.dropna(subset=['title', 'content'])
        
        # Add text length features
        df['title_length'] = df['title'].str.len()
        df['content_length'] = df['content'].str.len()
        
        # Add word count features
        df['title_word_count'] = df['title'].str.split().str.len()
        df['content_word_count'] = df['content'].str.split().str.len()
        
        logger.info(f"Preprocessed {len(df)} article news records")
        return df
    
    def preprocess_car_reviews(self) -> pd.DataFrame:
        """
        Preprocess car reviews data
        
        Returns:
            Preprocessed car reviews DataFrame
        """
        if self.car_reviews_df is None:
            self.load_data()
            
        df = self.car_reviews_df.copy()
        
        # Convert publication_date to datetime
        df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
        
        # Clean text fields
        df['title'] = df['title'].astype(str).str.strip()
        df['verdict'] = df['verdict'].astype(str).str.strip()
        df['author'] = df['author'].astype(str).str.strip()
        df['source'] = df['source'].astype(str).str.strip()
        
        # Clean numeric fields
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Remove rows with missing essential data
        df = df.dropna(subset=['title', 'verdict'])
        
        # Add text length features
        df['title_length'] = df['title'].str.len()
        df['verdict_length'] = df['verdict'].str.len()
        
        # Add word count features
        df['title_word_count'] = df['title'].str.split().str.len()
        df['verdict_word_count'] = df['verdict'].str.split().str.len()
        
        # Create price categories
        df['price_category'] = pd.cut(
            df['price'], 
            bins=[0, 20000, 40000, 60000, 80000, float('inf')],
            labels=['Budget', 'Mid-range', 'Premium', 'Luxury', 'Ultra-luxury']
        )
        
        # Create rating categories
        df['rating_category'] = pd.cut(
            df['rating'],
            bins=[0, 2.5, 3.5, 4.5, 5.0],
            labels=['Poor', 'Average', 'Good', 'Excellent']
        )
        
        logger.info(f"Preprocessed {len(df)} car review records")
        return df
    
    def get_data_summary(self) -> dict:
        """
        Get summary statistics for both datasets
        
        Returns:
            Dictionary with summary statistics
        """
        if self.article_news_df is None or self.car_reviews_df is None:
            self.load_data()
            
        article_df = self.preprocess_article_news()
        reviews_df = self.preprocess_car_reviews()
        
        summary = {
            'article_news': {
                'total_records': len(article_df),
                'date_range': {
                    'start': article_df['publication_date'].min(),
                    'end': article_df['publication_date'].max()
                },
                'sources': article_df['source'].value_counts().to_dict(),
                'avg_title_length': article_df['title_length'].mean(),
                'avg_content_length': article_df['content_length'].mean(),
                'missing_data': article_df.isnull().sum().to_dict()
            },
            'car_reviews': {
                'total_records': len(reviews_df),
                'date_range': {
                    'start': reviews_df['publication_date'].min(),
                    'end': reviews_df['publication_date'].max()
                },
                'sources': reviews_df['source'].value_counts().to_dict(),
                'avg_rating': reviews_df['rating'].mean(),
                'avg_price': reviews_df['price'].mean(),
                'price_range': {
                    'min': reviews_df['price'].min(),
                    'max': reviews_df['price'].max()
                },
                'rating_distribution': reviews_df['rating_category'].value_counts().to_dict(),
                'price_distribution': reviews_df['price_category'].value_counts().to_dict(),
                'missing_data': reviews_df.isnull().sum().to_dict()
            }
        }
        
        return summary


def load_sample_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load sample data for testing and development
    
    Returns:
        Tuple of (article_news_df, car_reviews_df)
    """
    loader = DataLoader(
        article_news_path='project_data/article_news_202507212152.csv',
        car_reviews_path='project_data/car_reviews_202507231630.csv'
    )
    
    return loader.load_data()


if __name__ == "__main__":
    # Test the data loader
    loader = DataLoader(
        article_news_path='project_data/article_news_202507212152.csv',
        car_reviews_path='project_data/car_reviews_202507231630.csv'
    )
    
    # Load and preprocess data
    article_df, reviews_df = loader.load_data()
    processed_article_df = loader.preprocess_article_news()
    processed_reviews_df = loader.preprocess_car_reviews()
    
    # Get summary
    summary = loader.get_data_summary()
    print("Data Summary:")
    print(f"Article News: {summary['article_news']['total_records']} records")
    print(f"Car Reviews: {summary['car_reviews']['total_records']} records")
