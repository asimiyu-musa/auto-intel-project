"""
Correlation Analysis module for Auto Intel Project
Analyzes correlations between price, score, sentiment, and other variables
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CorrelationAnalyzer:
    """Analyzes correlations between various automotive data variables"""
    
    def __init__(self):
        """Initialize correlation analyzer"""
        self.correlation_results = {}
        
    def analyze_price_rating_correlation(self, df: pd.DataFrame) -> Dict:
        """
        Analyze correlation between price and rating
        
        Args:
            df: Car reviews DataFrame
            
        Returns:
            Dictionary with correlation analysis results
        """
        logger.info("Analyzing price-rating correlation...")
        
        # Clean data
        clean_df = df.dropna(subset=['price', 'rating'])
        
        if len(clean_df) == 0:
            return {'correlation': 0, 'p_value': 1, 'sample_size': 0}
        
        # Calculate correlation
        correlation, p_value = stats.pearsonr(clean_df['price'], clean_df['rating'])
        
        # Calculate Spearman correlation for non-linear relationships
        spearman_corr, spearman_p = stats.spearmanr(clean_df['price'], clean_df['rating'])
        
        # Calculate R-squared
        r_squared = correlation ** 2
        
        results = {
            'pearson_correlation': correlation,
            'pearson_p_value': p_value,
            'spearman_correlation': spearman_corr,
            'spearman_p_value': spearman_p,
            'r_squared': r_squared,
            'sample_size': len(clean_df),
            'price_stats': {
                'mean': clean_df['price'].mean(),
                'std': clean_df['price'].std(),
                'min': clean_df['price'].min(),
                'max': clean_df['price'].max()
            },
            'rating_stats': {
                'mean': clean_df['rating'].mean(),
                'std': clean_df['rating'].std(),
                'min': clean_df['rating'].min(),
                'max': clean_df['rating'].max()
            }
        }
        
        logger.info(f"Price-Rating correlation: {correlation:.3f} (p={p_value:.3f})")
        return results
    
    def analyze_sentiment_correlations(self, df: pd.DataFrame, sentiment_scores: List[float]) -> Dict:
        """
        Analyze correlations between sentiment and other variables
        
        Args:
            df: Car reviews DataFrame
            sentiment_scores: List of sentiment scores
            
        Returns:
            Dictionary with sentiment correlation analysis
        """
        logger.info("Analyzing sentiment correlations...")
        
        # Add sentiment scores to dataframe
        df_with_sentiment = df.copy()
        df_with_sentiment['sentiment_score'] = sentiment_scores
        
        # Clean data
        clean_df = df_with_sentiment.dropna(subset=['sentiment_score'])
        
        correlations = {}
        
        # Sentiment vs Rating
        if 'rating' in clean_df.columns:
            rating_corr, rating_p = stats.pearsonr(
                clean_df['sentiment_score'], 
                clean_df['rating']
            )
            correlations['sentiment_rating'] = {
                'correlation': rating_corr,
                'p_value': rating_p
            }
        
        # Sentiment vs Price
        if 'price' in clean_df.columns:
            price_corr, price_p = stats.pearsonr(
                clean_df['sentiment_score'], 
                clean_df['price']
            )
            correlations['sentiment_price'] = {
                'correlation': price_corr,
                'p_value': price_p
            }
        
        # Sentiment vs Text Length
        if 'verdict_length' in clean_df.columns:
            length_corr, length_p = stats.pearsonr(
                clean_df['sentiment_score'], 
                clean_df['verdict_length']
            )
            correlations['sentiment_length'] = {
                'correlation': length_corr,
                'p_value': length_p
            }
        
        return correlations
    
    def analyze_source_correlations(self, df: pd.DataFrame) -> Dict:
        """
        Analyze correlations by source
        
        Args:
            df: Car reviews DataFrame
            
        Returns:
            Dictionary with source-based correlation analysis
        """
        logger.info("Analyzing source-based correlations...")
        
        source_analysis = {}
        
        for source in df['source'].unique():
            source_df = df[df['source'] == source]
            
            if len(source_df) < 10:  # Skip sources with too few samples
                continue
                
            # Analyze price-rating correlation for this source
            price_rating_corr = self.analyze_price_rating_correlation(source_df)
            
            source_analysis[source] = {
                'sample_size': len(source_df),
                'avg_rating': source_df['rating'].mean(),
                'avg_price': source_df['price'].mean(),
                'price_rating_correlation': price_rating_corr['pearson_correlation'],
                'price_rating_p_value': price_rating_corr['pearson_p_value']
            }
        
        return source_analysis
    
    def analyze_time_series_correlations(self, df: pd.DataFrame) -> Dict:
        """
        Analyze correlations over time
        
        Args:
            df: Car reviews DataFrame with publication_date
            
        Returns:
            Dictionary with time series correlation analysis
        """
        logger.info("Analyzing time series correlations...")
        
        # Ensure publication_date is datetime
        df['publication_date'] = pd.to_datetime(df['publication_date'])
        
        # Group by month
        df['month'] = df['publication_date'].dt.to_period('M')
        monthly_stats = df.groupby('month').agg({
            'rating': ['mean', 'count'],
            'price': ['mean', 'count']
        }).reset_index()
        
        # Flatten column names
        monthly_stats.columns = ['month', 'avg_rating', 'rating_count', 'avg_price', 'price_count']
        
        # Calculate correlations over time
        time_correlations = {}
        
        if len(monthly_stats) > 1:
            # Rating trend over time
            rating_trend = stats.linregress(
                range(len(monthly_stats)), 
                monthly_stats['avg_rating']
            )
            time_correlations['rating_trend'] = {
                'slope': rating_trend.slope,
                'r_squared': rating_trend.rvalue ** 2,
                'p_value': rating_trend.pvalue
            }
            
            # Price trend over time
            price_trend = stats.linregress(
                range(len(monthly_stats)), 
                monthly_stats['avg_price']
            )
            time_correlations['price_trend'] = {
                'slope': price_trend.slope,
                'r_squared': price_trend.rvalue ** 2,
                'p_value': price_trend.pvalue
            }
        
        return {
            'monthly_stats': monthly_stats.to_dict('records'),
            'time_correlations': time_correlations
        }
    
    def analyze_price_category_correlations(self, df: pd.DataFrame) -> Dict:
        """
        Analyze correlations by price categories
        
        Args:
            df: Car reviews DataFrame with price_category
            
        Returns:
            Dictionary with price category correlation analysis
        """
        logger.info("Analyzing price category correlations...")
        
        if 'price_category' not in df.columns:
            return {}
        
        category_analysis = {}
        
        for category in df['price_category'].unique():
            if pd.isna(category):
                continue
                
            category_df = df[df['price_category'] == category]
            
            if len(category_df) < 5:  # Skip categories with too few samples
                continue
            
            # Analyze rating distribution for this category
            category_analysis[category] = {
                'sample_size': len(category_df),
                'avg_rating': category_df['rating'].mean(),
                'rating_std': category_df['rating'].std(),
                'avg_price': category_df['price'].mean(),
                'price_std': category_df['price'].std(),
                'rating_distribution': category_df['rating'].value_counts().to_dict()
            }
        
        return category_analysis
    
    def analyze_news_reviews_correlation(self, article_df: pd.DataFrame, reviews_df: pd.DataFrame) -> Dict:
        """
        Analyze correlations between news articles and reviews
        
        Args:
            article_df: Article news DataFrame
            reviews_df: Car reviews DataFrame
            
        Returns:
            Dictionary with news-reviews correlation analysis
        """
        logger.info("Analyzing news-reviews correlations...")
        
        # Convert dates to datetime
        article_df['publication_date'] = pd.to_datetime(article_df['publication_date'])
        reviews_df['publication_date'] = pd.to_datetime(reviews_df['publication_date'])
        
        # Group by month for both datasets
        article_df['month'] = article_df['publication_date'].dt.to_period('M')
        reviews_df['month'] = reviews_df['publication_date'].dt.to_period('M')
        
        # Count articles and reviews per month
        monthly_articles = article_df.groupby('month').size().reset_index(name='article_count')
        monthly_reviews = reviews_df.groupby('month').size().reset_index(name='review_count')
        
        # Merge monthly data
        monthly_data = pd.merge(monthly_articles, monthly_reviews, on='month', how='outer').fillna(0)
        
        # Calculate correlation between article and review counts
        if len(monthly_data) > 1:
            correlation, p_value = stats.pearsonr(
                monthly_data['article_count'], 
                monthly_data['review_count']
            )
            
            return {
                'correlation': correlation,
                'p_value': p_value,
                'monthly_data': monthly_data.to_dict('records')
            }
        
        return {'correlation': 0, 'p_value': 1, 'monthly_data': []}
    
    def create_correlation_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create correlation matrix for numeric variables
        
        Args:
            df: DataFrame with numeric variables
            
        Returns:
            Correlation matrix DataFrame
        """
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Create correlation matrix
        correlation_matrix = df[numeric_cols].corr()
        
        return correlation_matrix
    
    def run_comprehensive_correlation_analysis(self, article_df: pd.DataFrame, reviews_df: pd.DataFrame, sentiment_scores: List[float] = None) -> Dict:
        """
        Run comprehensive correlation analysis on both datasets
        
        Args:
            article_df: Article news DataFrame
            reviews_df: Car reviews DataFrame
            sentiment_scores: Optional list of sentiment scores for reviews
            
        Returns:
            Dictionary with comprehensive correlation analysis results
        """
        logger.info("Starting comprehensive correlation analysis...")
        
        results = {
            'price_rating_correlation': self.analyze_price_rating_correlation(reviews_df),
            'source_correlations': self.analyze_source_correlations(reviews_df),
            'time_series_correlations': self.analyze_time_series_correlations(reviews_df),
            'price_category_correlations': self.analyze_price_category_correlations(reviews_df),
            'news_reviews_correlation': self.analyze_news_reviews_correlation(article_df, reviews_df),
            'correlation_matrix': self.create_correlation_matrix(reviews_df).to_dict()
        }
        
        # Add sentiment correlations if sentiment scores provided
        if sentiment_scores and len(sentiment_scores) == len(reviews_df):
            results['sentiment_correlations'] = self.analyze_sentiment_correlations(reviews_df, sentiment_scores)
        
        logger.info("Completed comprehensive correlation analysis")
        return results


def create_correlation_visualizations(results: Dict, save_path: str = None) -> None:
    """
    Create correlation visualization plots
    
    Args:
        results: Correlation analysis results
        save_path: Optional path to save plots
    """
    # Set up the plotting style
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Correlation Analysis Results', fontsize=16, fontweight='bold')
    
    # 1. Price vs Rating Scatter Plot
    if 'price_rating_correlation' in results:
        corr_data = results['price_rating_correlation']
        axes[0, 0].scatter([corr_data['price_stats']['mean']], [corr_data['rating_stats']['mean']], 
                          s=100, alpha=0.7, color='blue')
        axes[0, 0].set_xlabel('Average Price')
        axes[0, 0].set_ylabel('Average Rating')
        axes[0, 0].set_title(f'Price vs Rating Correlation\n(r={corr_data["pearson_correlation"]:.3f})')
        axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Source-based Rating Distribution
    if 'source_correlations' in results:
        sources = list(results['source_correlations'].keys())
        avg_ratings = [results['source_correlations'][s]['avg_rating'] for s in sources]
        
        axes[0, 1].bar(sources, avg_ratings, color='green', alpha=0.7)
        axes[0, 1].set_xlabel('Source')
        axes[0, 1].set_ylabel('Average Rating')
        axes[0, 1].set_title('Average Rating by Source')
        axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 3. Price Category Analysis
    if 'price_category_correlations' in results:
        categories = list(results['price_category_correlations'].keys())
        avg_ratings = [results['price_category_correlations'][c]['avg_rating'] for c in categories]
        
        axes[1, 0].bar(categories, avg_ratings, color='orange', alpha=0.7)
        axes[1, 0].set_xlabel('Price Category')
        axes[1, 0].set_ylabel('Average Rating')
        axes[1, 0].set_title('Average Rating by Price Category')
        axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Time Series Trend
    if 'time_series_correlations' in results and 'monthly_stats' in results['time_series_correlations']:
        monthly_data = results['time_series_correlations']['monthly_stats']
        months = [str(item['month']) for item in monthly_data]
        avg_ratings = [item['avg_rating'] for item in monthly_data]
        
        axes[1, 1].plot(months, avg_ratings, marker='o', linewidth=2, markersize=6)
        axes[1, 1].set_xlabel('Month')
        axes[1, 1].set_ylabel('Average Rating')
        axes[1, 1].set_title('Rating Trend Over Time')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Correlation visualizations saved to {save_path}")
    
    plt.show()


if __name__ == "__main__":
    # Test the correlation analyzer
    from data_loader import load_sample_data
    
    # Load data
    article_df, reviews_df = load_sample_data()
    
    # Initialize analyzer
    analyzer = CorrelationAnalyzer()
    
    # Run comprehensive analysis
    results = analyzer.run_comprehensive_correlation_analysis(article_df, reviews_df)
    
    print("Correlation Analysis Results:")
    print(f"Price-Rating Correlation: {results['price_rating_correlation']['pearson_correlation']:.3f}")
    print(f"News-Reviews Correlation: {results['news_reviews_correlation']['correlation']:.3f}")
    
    # Create visualizations
    create_correlation_visualizations(results, 'correlation_analysis.png')
