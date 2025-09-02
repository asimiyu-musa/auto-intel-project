"""
FastAPI Application for Auto Intel Project
Provides API endpoints for accessing analysis results
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Add parent directory to path to import analysis modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.main_analyzer import AutoIntelAnalyzer
from analysis.data_loader import DataLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Auto Intel API",
    description="API for accessing automotive data analysis results",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for caching
analyzer = None
analysis_results = None
data_loaded = False

def load_data_and_analyze():
    """Load data and run analysis"""
    global analyzer, analysis_results, data_loaded
    
    if data_loaded:
        return
    
    try:
        logger.info("Loading data and running analysis...")
        
        # Initialize analyzer
        analyzer = AutoIntelAnalyzer(
            article_news_path='project_data/article_news_202507212152.csv',
            car_reviews_path='project_data/car_reviews_202507231630.csv'
        )
        
        # Run comprehensive analysis
        analysis_results = analyzer.run_comprehensive_analysis()
        
        # Generate insights
        insights = analyzer.generate_insights_report()
        analysis_results['insights_report'] = insights
        
        data_loaded = True
        logger.info("Data loaded and analysis completed")
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize data on startup"""
    load_data_and_analyze()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Auto Intel API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/docs",
            "/health",
            "/summary",
            "/data",
            "/nlp",
            "/correlations",
            "/insights"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_loaded": data_loaded
    }

@app.get("/summary")
async def get_summary():
    """Get analysis summary"""
    if not data_loaded:
        load_data_and_analyze()
    
    if analysis_results is None:
        raise HTTPException(status_code=500, detail="Analysis results not available")
    
    summary = analyzer.get_analysis_summary()
    return summary

@app.get("/data")
async def get_data_summary():
    """Get data summary"""
    if not data_loaded:
        load_data_and_analyze()
    
    if analysis_results is None:
        raise HTTPException(status_code=500, detail="Analysis results not available")
    
    return analysis_results.get('data_summary', {})

@app.get("/nlp")
async def get_nlp_results():
    """Get NLP analysis results"""
    if not data_loaded:
        load_data_and_analyze()
    
    if analysis_results is None:
        raise HTTPException(status_code=500, detail="Analysis results not available")
    
    nlp_results = analysis_results.get('nlp_analysis', {})
    
    # Return simplified version for API
    simplified_nlp = {
        'sentiment': {
            'articles': nlp_results.get('article_news', {}).get('sentiment', {}),
            'reviews': nlp_results.get('car_reviews', {}).get('sentiment', {})
        },
        'top_bigrams': {
            'articles': nlp_results.get('article_news', {}).get('bigrams', {}).get('titles', [])[:10],
            'reviews': nlp_results.get('car_reviews', {}).get('bigrams', {}).get('verdicts', [])[:10]
        },
        'entities': nlp_results.get('car_reviews', {}).get('entities', {})
    }
    
    return simplified_nlp

@app.get("/correlations")
async def get_correlation_results():
    """Get correlation analysis results"""
    if not data_loaded:
        load_data_and_analyze()
    
    if analysis_results is None:
        raise HTTPException(status_code=500, detail="Analysis results not available")
    
    corr_results = analysis_results.get('correlation_analysis', {})
    
    # Return simplified version for API
    simplified_corr = {
        'price_rating_correlation': corr_results.get('price_rating_correlation', {}),
        'source_correlations': corr_results.get('source_correlations', {}),
        'price_category_correlations': corr_results.get('price_category_correlations', {}),
        'news_reviews_correlation': corr_results.get('news_reviews_correlation', {})
    }
    
    return simplified_corr

@app.get("/insights")
async def get_insights():
    """Get insights report"""
    if not data_loaded:
        load_data_and_analyze()
    
    if analysis_results is None:
        raise HTTPException(status_code=500, detail="Analysis results not available")
    
    return analysis_results.get('insights_report', {})

@app.get("/raw-data/{data_type}")
async def get_raw_data(data_type: str):
    """Get raw data (limited for API)"""
    if not data_loaded:
        load_data_and_analyze()
    
    if analyzer is None:
        raise HTTPException(status_code=500, detail="Analyzer not available")
    
    if data_type == "articles":
        df = analyzer.processed_article_df
        if df is None:
            raise HTTPException(status_code=404, detail="Article data not available")
        
        # Return first 100 rows for API
        return {
            "data": df.head(100).to_dict('records'),
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    
    elif data_type == "reviews":
        df = analyzer.processed_reviews_df
        if df is None:
            raise HTTPException(status_code=404, detail="Review data not available")
        
        # Return first 100 rows for API
        return {
            "data": df.head(100).to_dict('records'),
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    
    else:
        raise HTTPException(status_code=400, detail="Invalid data type. Use 'articles' or 'reviews'")

@app.get("/stats/{data_type}")
async def get_statistics(data_type: str):
    """Get statistics for a specific data type"""
    if not data_loaded:
        load_data_and_analyze()
    
    if analyzer is None:
        raise HTTPException(status_code=500, detail="Analyzer not available")
    
    if data_type == "articles":
        df = analyzer.processed_article_df
        if df is None:
            raise HTTPException(status_code=404, detail="Article data not available")
        
        stats = {
            "total_count": len(df),
            "date_range": {
                "start": df['publication_date'].min().isoformat() if not df['publication_date'].isna().all() else None,
                "end": df['publication_date'].max().isoformat() if not df['publication_date'].isna().all() else None
            },
            "sources": df['source'].value_counts().to_dict(),
            "avg_title_length": df['title_length'].mean(),
            "avg_content_length": df['content_length'].mean()
        }
        
        return stats
    
    elif data_type == "reviews":
        df = analyzer.processed_reviews_df
        if df is None:
            raise HTTPException(status_code=404, detail="Review data not available")
        
        stats = {
            "total_count": len(df),
            "date_range": {
                "start": df['publication_date'].min().isoformat() if not df['publication_date'].isna().all() else None,
                "end": df['publication_date'].max().isoformat() if not df['publication_date'].isna().all() else None
            },
            "sources": df['source'].value_counts().to_dict(),
            "avg_rating": df['rating'].mean(),
            "avg_price": df['price'].mean(),
            "price_range": {
                "min": df['price'].min(),
                "max": df['price'].max()
            },
            "rating_distribution": df['rating'].value_counts().sort_index().to_dict()
        }
        
        return stats
    
    else:
        raise HTTPException(status_code=400, detail="Invalid data type. Use 'articles' or 'reviews'")

@app.get("/search")
async def search_data(query: str, data_type: str = "both", limit: int = 10):
    """Search data by title or content"""
    if not data_loaded:
        load_data_and_analyze()
    
    if analyzer is None:
        raise HTTPException(status_code=500, detail="Analyzer not available")
    
    results = []
    
    if data_type in ["articles", "both"]:
        article_df = analyzer.processed_article_df
        if article_df is not None:
            # Search in titles and content
            title_matches = article_df[article_df['title'].str.contains(query, case=False, na=False)]
            content_matches = article_df[article_df['content'].str.contains(query, case=False, na=False)]
            
            for _, row in title_matches.head(limit//2).iterrows():
                results.append({
                    "type": "article",
                    "title": row['title'],
                    "source": row['source'],
                    "publication_date": row['publication_date'].isoformat() if pd.notna(row['publication_date']) else None,
                    "match_type": "title"
                })
            
            for _, row in content_matches.head(limit//2).iterrows():
                results.append({
                    "type": "article",
                    "title": row['title'],
                    "source": row['source'],
                    "publication_date": row['publication_date'].isoformat() if pd.notna(row['publication_date']) else None,
                    "match_type": "content"
                })
    
    if data_type in ["reviews", "both"]:
        review_df = analyzer.processed_reviews_df
        if review_df is not None:
            # Search in titles and verdicts
            title_matches = review_df[review_df['title'].str.contains(query, case=False, na=False)]
            verdict_matches = review_df[review_df['verdict'].str.contains(query, case=False, na=False)]
            
            for _, row in title_matches.head(limit//2).iterrows():
                results.append({
                    "type": "review",
                    "title": row['title'],
                    "source": row['source'],
                    "rating": row['rating'],
                    "price": row['price'],
                    "publication_date": row['publication_date'].isoformat() if pd.notna(row['publication_date']) else None,
                    "match_type": "title"
                })
            
            for _, row in verdict_matches.head(limit//2).iterrows():
                results.append({
                    "type": "review",
                    "title": row['title'],
                    "source": row['source'],
                    "rating": row['rating'],
                    "price": row['price'],
                    "publication_date": row['publication_date'].isoformat() if pd.notna(row['publication_date']) else None,
                    "match_type": "verdict"
                })
    
    return {
        "query": query,
        "total_results": len(results),
        "results": results[:limit]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
