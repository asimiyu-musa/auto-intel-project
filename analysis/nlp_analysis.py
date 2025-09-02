"""
NLP Analysis module for Auto Intel Project
Handles Bigrams, Trigrams, Sentiment Analysis, and NER
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# NLP libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
from textblob import TextBlob

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please install: python -m spacy download en_core_web_sm")
    nlp = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NLPAnalyzer:
    """NLP Analysis for automotive text data"""
    
    def __init__(self):
        """Initialize NLP analyzer with required components"""
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()
        
        # Add automotive-specific stop words
        self.stop_words.update([
            'car', 'cars', 'vehicle', 'vehicles', 'review', 'reviews',
            'test', 'testing', 'drive', 'driving', 'road', 'roads'
        ])
        
        # Automotive brands and models for NER
        self.car_brands = {
            'bmw', 'mercedes', 'audi', 'volkswagen', 'volvo', 'porsche',
            'ferrari', 'lamborghini', 'toyota', 'honda', 'ford', 'chevrolet',
            'nissan', 'hyundai', 'kia', 'mazda', 'subaru', 'lexus', 'infiniti',
            'acura', 'buick', 'cadillac', 'chrysler', 'dodge', 'jeep', 'ram',
            'tesla', 'rivian', 'lucid', 'polestar', 'nio', 'xpeng', 'li auto'
        }
        
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for analysis
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        if pd.isna(text) or text == '':
            return ''
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep apostrophes
        text = re.sub(r'[^a-zA-Z\s\']', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_ngrams(self, text: str, n: int = 2, top_k: int = 20) -> List[Tuple[str, int]]:
        """
        Extract n-grams from text
        
        Args:
            text: Input text
            n: N-gram size (2 for bigrams, 3 for trigrams)
            top_k: Number of top n-grams to return
            
        Returns:
            List of (ngram, count) tuples
        """
        if not text:
            return []
            
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Tokenize
        tokens = word_tokenize(processed_text)
        
        # Remove stop words
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        # Generate n-grams
        ngram_list = list(ngrams(tokens, n))
        
        # Count n-grams
        ngram_counts = Counter(ngram_list)
        
        # Return top k n-grams
        return ngram_counts.most_common(top_k)
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text using VADER
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment scores
        """
        if not text:
            return {'compound': 0, 'pos': 0, 'neg': 0, 'neu': 0}
            
        # Get VADER sentiment scores
        scores = self.sia.polarity_scores(text)
        
        return scores
    
    def get_sentiment_label(self, compound_score: float) -> str:
        """
        Convert compound sentiment score to label
        
        Args:
            compound_score: VADER compound score
            
        Returns:
            Sentiment label
        """
        if compound_score >= 0.05:
            return 'Positive'
        elif compound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities using spaCy
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with entity types and values
        """
        if not nlp or not text:
            return {}
            
        doc = nlp(text)
        entities = defaultdict(list)
        
        for ent in doc.ents:
            entities[ent.label_].append(ent.text)
        
        # Extract car brands and models
        car_entities = self.extract_car_entities(text)
        if car_entities:
            entities['CAR_BRAND'] = car_entities
        
        return dict(entities)
    
    def extract_car_entities(self, text: str) -> List[str]:
        """
        Extract car brands and models from text
        
        Args:
            text: Input text
            
        Returns:
            List of car brands/models found
        """
        if not text:
            return []
            
        text_lower = text.lower()
        found_brands = []
        
        for brand in self.car_brands:
            if brand in text_lower:
                found_brands.append(brand.title())
        
        return found_brands
    
    def analyze_corpus_ngrams(self, texts: List[str], n: int = 2, top_k: int = 50) -> List[Tuple[str, int]]:
        """
        Analyze n-grams across entire corpus
        
        Args:
            texts: List of text documents
            n: N-gram size
            top_k: Number of top n-grams to return
            
        Returns:
            List of (ngram, count) tuples
        """
        all_ngrams = []
        
        for text in texts:
            if text and not pd.isna(text):
                ngrams = self.extract_ngrams(text, n, top_k)
                all_ngrams.extend(ngrams)
        
        # Count across all documents
        corpus_counts = Counter()
        for ngram, count in all_ngrams:
            corpus_counts[ngram] += count
        
        return corpus_counts.most_common(top_k)
    
    def analyze_corpus_sentiment(self, texts: List[str]) -> Dict[str, float]:
        """
        Analyze sentiment across entire corpus
        
        Args:
            texts: List of text documents
            
        Returns:
            Dictionary with average sentiment scores
        """
        all_scores = []
        
        for text in texts:
            if text and not pd.isna(text):
                scores = self.analyze_sentiment(text)
                all_scores.append(scores)
        
        if not all_scores:
            return {'compound': 0, 'pos': 0, 'neg': 0, 'neu': 0}
        
        # Calculate average scores
        avg_scores = {}
        for key in ['compound', 'pos', 'neg', 'neu']:
            avg_scores[key] = np.mean([score[key] for score in all_scores])
        
        return avg_scores
    
    def analyze_article_news(self, df: pd.DataFrame) -> Dict:
        """
        Perform comprehensive NLP analysis on article news data
        
        Args:
            df: Article news DataFrame
            
        Returns:
            Dictionary with analysis results
        """
        logger.info("Starting NLP analysis on article news data...")
        
        # Extract texts
        titles = df['title'].dropna().tolist()
        contents = df['content'].dropna().tolist()
        
        # Analyze bigrams and trigrams
        title_bigrams = self.analyze_corpus_ngrams(titles, n=2, top_k=30)
        title_trigrams = self.analyze_corpus_ngrams(titles, n=3, top_k=20)
        content_bigrams = self.analyze_corpus_ngrams(contents, n=2, top_k=30)
        content_trigrams = self.analyze_corpus_ngrams(contents, n=3, top_k=20)
        
        # Analyze sentiment
        title_sentiment = self.analyze_corpus_sentiment(titles)
        content_sentiment = self.analyze_corpus_sentiment(contents)
        
        # Extract entities from sample texts
        sample_contents = contents[:100]  # Sample for performance
        entities = defaultdict(list)
        for content in sample_contents:
            content_entities = self.extract_entities(content)
            for entity_type, entity_list in content_entities.items():
                entities[entity_type].extend(entity_list)
        
        # Remove duplicates
        for entity_type in entities:
            entities[entity_type] = list(set(entities[entity_type]))
        
        results = {
            'bigrams': {
                'titles': title_bigrams,
                'contents': content_bigrams
            },
            'trigrams': {
                'titles': title_trigrams,
                'contents': content_trigrams
            },
            'sentiment': {
                'titles': title_sentiment,
                'contents': content_sentiment
            },
            'entities': dict(entities),
            'summary': {
                'total_articles': len(df),
                'avg_title_length': df['title'].str.len().mean(),
                'avg_content_length': df['content'].str.len().mean()
            }
        }
        
        logger.info("Completed NLP analysis on article news data")
        return results
    
    def analyze_car_reviews(self, df: pd.DataFrame) -> Dict:
        """
        Perform comprehensive NLP analysis on car reviews data
        
        Args:
            df: Car reviews DataFrame
            
        Returns:
            Dictionary with analysis results
        """
        logger.info("Starting NLP analysis on car reviews data...")
        
        # Extract texts
        titles = df['title'].dropna().tolist()
        verdicts = df['verdict'].dropna().tolist()
        
        # Analyze bigrams and trigrams
        title_bigrams = self.analyze_corpus_ngrams(titles, n=2, top_k=30)
        title_trigrams = self.analyze_corpus_ngrams(titles, n=3, top_k=20)
        verdict_bigrams = self.analyze_corpus_ngrams(verdicts, n=2, top_k=30)
        verdict_trigrams = self.analyze_corpus_ngrams(verdicts, n=3, top_k=20)
        
        # Analyze sentiment
        title_sentiment = self.analyze_corpus_sentiment(titles)
        verdict_sentiment = self.analyze_corpus_sentiment(verdicts)
        
        # Extract entities from sample texts
        sample_verdicts = verdicts[:100]  # Sample for performance
        entities = defaultdict(list)
        for verdict in sample_verdicts:
            verdict_entities = self.extract_entities(verdict)
            for entity_type, entity_list in verdict_entities.items():
                entities[entity_type].extend(entity_list)
        
        # Remove duplicates
        for entity_type in entities:
            entities[entity_type] = list(set(entities[entity_type]))
        
        # Correlation analysis with ratings and prices
        sentiment_correlation = self.analyze_sentiment_correlation(df)
        
        results = {
            'bigrams': {
                'titles': title_bigrams,
                'verdicts': verdict_bigrams
            },
            'trigrams': {
                'titles': title_trigrams,
                'verdicts': verdict_trigrams
            },
            'sentiment': {
                'titles': title_sentiment,
                'verdicts': verdict_sentiment
            },
            'entities': dict(entities),
            'correlation_analysis': sentiment_correlation,
            'summary': {
                'total_reviews': len(df),
                'avg_rating': df['rating'].mean(),
                'avg_price': df['price'].mean(),
                'avg_title_length': df['title'].str.len().mean(),
                'avg_verdict_length': df['verdict'].str.len().mean()
            }
        }
        
        logger.info("Completed NLP analysis on car reviews data")
        return results
    
    def analyze_sentiment_correlation(self, df: pd.DataFrame) -> Dict:
        """
        Analyze correlation between sentiment and ratings/prices
        
        Args:
            df: Car reviews DataFrame
            
        Returns:
            Dictionary with correlation analysis
        """
        correlations = {}
        
        # Calculate sentiment scores for each review
        sentiment_scores = []
        for verdict in df['verdict'].dropna():
            scores = self.analyze_sentiment(verdict)
            sentiment_scores.append(scores['compound'])
        
        # Add sentiment scores to dataframe
        df_with_sentiment = df.copy()
        df_with_sentiment['sentiment_score'] = sentiment_scores
        
        # Calculate correlations
        if len(sentiment_scores) > 0:
            correlations['sentiment_rating'] = df_with_sentiment['sentiment_score'].corr(df_with_sentiment['rating'])
            correlations['sentiment_price'] = df_with_sentiment['sentiment_score'].corr(df_with_sentiment['price'])
            correlations['rating_price'] = df_with_sentiment['rating'].corr(df_with_sentiment['price'])
        
        return correlations


def run_nlp_analysis(article_df: pd.DataFrame, reviews_df: pd.DataFrame) -> Dict:
    """
    Run complete NLP analysis on both datasets
    
    Args:
        article_df: Article news DataFrame
        reviews_df: Car reviews DataFrame
        
    Returns:
        Dictionary with complete analysis results
    """
    analyzer = NLPAnalyzer()
    
    # Analyze both datasets
    article_analysis = analyzer.analyze_article_news(article_df)
    reviews_analysis = analyzer.analyze_car_reviews(reviews_df)
    
    return {
        'article_news': article_analysis,
        'car_reviews': reviews_analysis
    }


if __name__ == "__main__":
    # Test the NLP analyzer
    from data_loader import load_sample_data
    
    # Load data
    article_df, reviews_df = load_sample_data()
    
    # Run analysis
    results = run_nlp_analysis(article_df, reviews_df)
    
    print("NLP Analysis Results:")
    print(f"Article News - Top Bigrams: {results['article_news']['bigrams']['titles'][:5]}")
    print(f"Car Reviews - Top Bigrams: {results['car_reviews']['bigrams']['titles'][:5]}")
    print(f"Article Sentiment: {results['article_news']['sentiment']['contents']}")
    print(f"Reviews Sentiment: {results['car_reviews']['sentiment']['verdicts']}")
