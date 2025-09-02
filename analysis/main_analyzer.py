"""
Main Analysis Orchestrator for Auto Intel Project
Combines all analysis modules and provides a unified interface
"""

import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os

from .data_loader import DataLoader
from .nlp_analysis import NLPAnalyzer, run_nlp_analysis
from .correlation_analysis import CorrelationAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoIntelAnalyzer:
    """Main analyzer that orchestrates all analysis components"""
    
    def __init__(self, article_news_path: str, car_reviews_path: str):
        """
        Initialize the main analyzer
        
        Args:
            article_news_path: Path to article news CSV file
            car_reviews_path: Path to car reviews CSV file
        """
        self.article_news_path = article_news_path
        self.car_reviews_path = car_reviews_path
        
        # Initialize components
        self.data_loader = DataLoader(article_news_path, car_reviews_path)
        self.nlp_analyzer = NLPAnalyzer()
        self.correlation_analyzer = CorrelationAnalyzer()
        
        # Data storage
        self.article_df = None
        self.reviews_df = None
        self.processed_article_df = None
        self.processed_reviews_df = None
        
        # Analysis results
        self.analysis_results = {}
        
    def load_and_preprocess_data(self) -> None:
        """Load and preprocess all data"""
        logger.info("Loading and preprocessing data...")
        
        # Load raw data
        self.article_df, self.reviews_df = self.data_loader.load_data()
        
        # Preprocess data
        self.processed_article_df = self.data_loader.preprocess_article_news()
        self.processed_reviews_df = self.data_loader.preprocess_car_reviews()
        
        logger.info("Data loading and preprocessing completed")
    
    def run_nlp_analysis(self) -> Dict:
        """Run NLP analysis on both datasets"""
        logger.info("Running NLP analysis...")
        
        if self.processed_article_df is None or self.processed_reviews_df is None:
            self.load_and_preprocess_data()
        
        # Run NLP analysis
        nlp_results = run_nlp_analysis(self.processed_article_df, self.processed_reviews_df)
        
        self.analysis_results['nlp_analysis'] = nlp_results
        logger.info("NLP analysis completed")
        
        return nlp_results
    
    def run_correlation_analysis(self) -> Dict:
        """Run correlation analysis"""
        logger.info("Running correlation analysis...")
        
        if self.processed_article_df is None or self.processed_reviews_df is None:
            self.load_and_preprocess_data()
        
        # Get sentiment scores for correlation analysis
        sentiment_scores = []
        for verdict in self.processed_reviews_df['verdict'].dropna():
            scores = self.nlp_analyzer.analyze_sentiment(verdict)
            sentiment_scores.append(scores['compound'])
        
        # Run correlation analysis
        correlation_results = self.correlation_analyzer.run_comprehensive_correlation_analysis(
            self.processed_article_df, 
            self.processed_reviews_df, 
            sentiment_scores
        )
        
        self.analysis_results['correlation_analysis'] = correlation_results
        logger.info("Correlation analysis completed")
        
        return correlation_results
    
    def run_comprehensive_analysis(self) -> Dict:
        """Run all analysis components"""
        logger.info("Starting comprehensive analysis...")
        
        # Load and preprocess data
        self.load_and_preprocess_data()
        
        # Get data summary
        data_summary = self.data_loader.get_data_summary()
        self.analysis_results['data_summary'] = data_summary
        
        # Run NLP analysis
        nlp_results = self.run_nlp_analysis()
        
        # Run correlation analysis
        correlation_results = self.run_correlation_analysis()
        
        # Add analysis metadata
        self.analysis_results['metadata'] = {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_articles': len(self.processed_article_df),
            'total_reviews': len(self.processed_reviews_df),
            'analysis_components': ['nlp_analysis', 'correlation_analysis', 'data_summary']
        }
        
        logger.info("Comprehensive analysis completed")
        return self.analysis_results
    
    def generate_insights_report(self) -> Dict:
        """Generate insights report from analysis results"""
        logger.info("Generating insights report...")
        
        if not self.analysis_results:
            logger.warning("No analysis results available. Run comprehensive analysis first.")
            return {}
        
        insights = {
            'key_findings': [],
            'recommendations': [],
            'trends': [],
            'anomalies': []
        }
        
        # Extract key findings from NLP analysis
        if 'nlp_analysis' in self.analysis_results:
            nlp_data = self.analysis_results['nlp_analysis']
            
            # Sentiment insights
            article_sentiment = nlp_data['article_news']['sentiment']['contents']
            review_sentiment = nlp_data['car_reviews']['sentiment']['verdicts']
            
            if article_sentiment['compound'] > 0.1:
                insights['key_findings'].append("Overall positive sentiment in automotive news articles")
            elif article_sentiment['compound'] < -0.1:
                insights['key_findings'].append("Overall negative sentiment in automotive news articles")
            else:
                insights['key_findings'].append("Neutral sentiment in automotive news articles")
            
            if review_sentiment['compound'] > 0.1:
                insights['key_findings'].append("Overall positive sentiment in car reviews")
            elif review_sentiment['compound'] < -0.1:
                insights['key_findings'].append("Overall negative sentiment in car reviews")
            else:
                insights['key_findings'].append("Neutral sentiment in car reviews")
            
            # Top entities
            if 'entities' in nlp_data['car_reviews']:
                car_entities = nlp_data['car_reviews']['entities'].get('CAR_BRAND', [])
                if car_entities:
                    insights['key_findings'].append(f"Most mentioned car brands: {', '.join(car_entities[:5])}")
        
        # Extract insights from correlation analysis
        if 'correlation_analysis' in self.analysis_results:
            corr_data = self.analysis_results['correlation_analysis']
            
            # Price-rating correlation
            price_rating_corr = corr_data['price_rating_correlation']['pearson_correlation']
            if abs(price_rating_corr) > 0.3:
                if price_rating_corr > 0:
                    insights['key_findings'].append("Strong positive correlation between price and rating")
                else:
                    insights['key_findings'].append("Strong negative correlation between price and rating")
            else:
                insights['key_findings'].append("Weak correlation between price and rating")
            
            # Source insights
            if 'source_correlations' in corr_data:
                sources = corr_data['source_correlations']
                best_source = max(sources.items(), key=lambda x: x[1]['avg_rating'])
                insights['key_findings'].append(f"Highest average rating from: {best_source[0]} ({best_source[1]['avg_rating']:.2f})")
        
        # Generate recommendations
        if 'correlation_analysis' in self.analysis_results:
            corr_data = self.analysis_results['correlation_analysis']
            
            # Price category recommendations
            if 'price_category_correlations' in corr_data:
                categories = corr_data['price_category_correlations']
                best_category = max(categories.items(), key=lambda x: x[1]['avg_rating'])
                insights['recommendations'].append(f"Focus on {best_category[0]} category for best ratings")
        
        # Identify trends
        if 'correlation_analysis' in self.analysis_results:
            corr_data = self.analysis_results['correlation_analysis']
            
            if 'time_series_correlations' in corr_data:
                time_data = corr_data['time_series_correlations']
                if 'time_correlations' in time_data:
                    rating_trend = time_data['time_correlations'].get('rating_trend', {})
                    if rating_trend.get('slope', 0) > 0:
                        insights['trends'].append("Upward trend in ratings over time")
                    elif rating_trend.get('slope', 0) < 0:
                        insights['trends'].append("Downward trend in ratings over time")
        
        self.analysis_results['insights_report'] = insights
        logger.info("Insights report generated")
        
        return insights
    
    def save_analysis_results(self, output_dir: str = "analysis_results") -> None:
        """Save analysis results to files"""
        logger.info(f"Saving analysis results to {output_dir}...")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Save comprehensive results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        results_file = os.path.join(output_dir, f"analysis_results_{timestamp}.json")
        with open(results_file, 'w') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
        
        # Save insights report
        insights_file = os.path.join(output_dir, f"insights_report_{timestamp}.json")
        if 'insights_report' in self.analysis_results:
            with open(insights_file, 'w') as f:
                json.dump(self.analysis_results['insights_report'], f, indent=2)
        
        # Save data summary
        summary_file = os.path.join(output_dir, f"data_summary_{timestamp}.json")
        if 'data_summary' in self.analysis_results:
            with open(summary_file, 'w') as f:
                json.dump(self.analysis_results['data_summary'], f, indent=2, default=str)
        
        logger.info(f"Analysis results saved to {output_dir}")
    
    def get_analysis_summary(self) -> Dict:
        """Get a summary of the analysis results"""
        if not self.analysis_results:
            return {"status": "No analysis performed"}
        
        summary = {
            "status": "Analysis completed",
            "timestamp": self.analysis_results.get('metadata', {}).get('analysis_timestamp'),
            "data_points": {
                "articles": self.analysis_results.get('metadata', {}).get('total_articles', 0),
                "reviews": self.analysis_results.get('metadata', {}).get('total_reviews', 0)
            },
            "components_analyzed": self.analysis_results.get('metadata', {}).get('analysis_components', [])
        }
        
        # Add key metrics
        if 'nlp_analysis' in self.analysis_results:
            nlp_data = self.analysis_results['nlp_analysis']
            summary['nlp_metrics'] = {
                'article_sentiment': nlp_data['article_news']['sentiment']['contents']['compound'],
                'review_sentiment': nlp_data['car_reviews']['sentiment']['verdicts']['compound']
            }
        
        if 'correlation_analysis' in self.analysis_results:
            corr_data = self.analysis_results['correlation_analysis']
            summary['correlation_metrics'] = {
                'price_rating_correlation': corr_data['price_rating_correlation']['pearson_correlation']
            }
        
        return summary


def run_auto_intel_analysis(article_news_path: str, car_reviews_path: str, save_results: bool = True) -> Dict:
    """
    Run complete Auto Intel analysis pipeline
    
    Args:
        article_news_path: Path to article news CSV file
        car_reviews_path: Path to car reviews CSV file
        save_results: Whether to save results to files
        
    Returns:
        Complete analysis results
    """
    logger.info("Starting Auto Intel analysis pipeline...")
    
    # Initialize analyzer
    analyzer = AutoIntelAnalyzer(article_news_path, car_reviews_path)
    
    # Run comprehensive analysis
    results = analyzer.run_comprehensive_analysis()
    
    # Generate insights
    insights = analyzer.generate_insights_report()
    
    # Save results if requested
    if save_results:
        analyzer.save_analysis_results()
    
    # Print summary
    summary = analyzer.get_analysis_summary()
    logger.info(f"Analysis Summary: {summary}")
    
    return results


if __name__ == "__main__":
    # Test the main analyzer
    article_path = "project_data/article_news_202507212152.csv"
    reviews_path = "project_data/car_reviews_202507231630.csv"
    
    # Run analysis
    results = run_auto_intel_analysis(article_path, reviews_path)
    
    print("Auto Intel Analysis Completed!")
    print(f"Articles analyzed: {results['metadata']['total_articles']}")
    print(f"Reviews analyzed: {results['metadata']['total_reviews']}")
    
    # Print key insights
    if 'insights_report' in results:
        print("\nKey Findings:")
        for finding in results['insights_report']['key_findings']:
            print(f"- {finding}")
