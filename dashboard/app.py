"""
Streamlit Dashboard for Auto Intel Project
Interactive dashboard for visualizing analysis results
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime
import sys

# Add parent directory to path to import analysis modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.main_analyzer import AutoIntelAnalyzer
from analysis.data_loader import DataLoader

# Page configuration
st.set_page_config(
    page_title="Auto Intel Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the data"""
    try:
        loader = DataLoader(
            article_news_path='project_data/article_news_202507212152.csv',
            car_reviews_path='project_data/car_reviews_202507231630.csv'
        )
        article_df, reviews_df = loader.load_data()
        processed_article_df = loader.preprocess_article_news()
        processed_reviews_df = loader.preprocess_car_reviews()
        return processed_article_df, processed_reviews_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

@st.cache_data
def run_analysis(article_df, reviews_df):
    """Run analysis and cache results"""
    try:
        analyzer = AutoIntelAnalyzer(
            article_news_path='project_data/article_news_202507212152.csv',
            car_reviews_path='project_data/car_reviews_202507231630.csv'
        )
        analyzer.processed_article_df = article_df
        analyzer.processed_reviews_df = reviews_df
        results = analyzer.run_comprehensive_analysis()
        insights = analyzer.generate_insights_report()
        return results, insights
    except Exception as e:
        st.error(f"Error running analysis: {e}")
        return None, None

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🚗 Auto Intel Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Automotive Data Analysis Platform")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Overview", "Data Analysis", "NLP Insights", "Correlations", "Trends", "Raw Data"]
    )
    
    # Load data
    with st.spinner("Loading data..."):
        article_df, reviews_df = load_data()
    
    if article_df is None or reviews_df is None:
        st.error("Failed to load data. Please check the data files.")
        return
    
    # Run analysis
    with st.spinner("Running analysis..."):
        results, insights = run_analysis(article_df, reviews_df)
    
    if results is None:
        st.error("Failed to run analysis.")
        return
    
    # Page routing
    if page == "Overview":
        show_overview(article_df, reviews_df, results, insights)
    elif page == "Data Analysis":
        show_data_analysis(article_df, reviews_df)
    elif page == "NLP Insights":
        show_nlp_insights(results)
    elif page == "Correlations":
        show_correlations(results, reviews_df)
    elif page == "Trends":
        show_trends(article_df, reviews_df, results)
    elif page == "Raw Data":
        show_raw_data(article_df, reviews_df)

def show_overview(article_df, reviews_df, results, insights):
    """Show overview page"""
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Articles",
            value=f"{len(article_df):,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Total Reviews",
            value=f"{len(reviews_df):,}",
            delta=None
        )
    
    with col3:
        avg_rating = reviews_df['rating'].mean()
        st.metric(
            label="Average Rating",
            value=f"{avg_rating:.2f}/5.0",
            delta=None
        )
    
    with col4:
        avg_price = reviews_df['price'].mean()
        st.metric(
            label="Average Price",
            value=f"£{avg_price:,.0f}",
            delta=None
        )
    
    # Key insights
    st.subheader("🔍 Key Insights")
    
    if insights and 'key_findings' in insights:
        for finding in insights['key_findings'][:5]:  # Show top 5 findings
            st.markdown(f'<div class="insight-box">• {finding}</div>', unsafe_allow_html=True)
    
    # Data distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Rating Distribution")
        rating_counts = reviews_df['rating'].value_counts().sort_index()
        fig = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            title="Car Review Ratings Distribution",
            labels={'x': 'Rating', 'y': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Price Distribution")
        fig = px.histogram(
            reviews_df,
            x='price',
            nbins=30,
            title="Car Price Distribution",
            labels={'price': 'Price (£)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Source analysis
    st.subheader("📰 Source Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Article sources
        article_sources = article_df['source'].value_counts()
        fig = px.pie(
            values=article_sources.values,
            names=article_sources.index,
            title="Article Sources Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Review sources
        review_sources = reviews_df['source'].value_counts()
        fig = px.pie(
            values=review_sources.values,
            names=review_sources.index,
            title="Review Sources Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

def show_data_analysis(article_df, reviews_df):
    """Show data analysis page"""
    
    st.subheader("📈 Data Analysis")
    
    # Date range analysis
    st.write("### 📅 Publication Date Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Articles over time
        article_df['publication_date'] = pd.to_datetime(article_df['publication_date'])
        article_df['month'] = article_df['publication_date'].dt.to_period('M')
        monthly_articles = article_df.groupby('month').size().reset_index(name='count')
        monthly_articles['month'] = monthly_articles['month'].astype(str)
        
        fig = px.line(
            monthly_articles,
            x='month',
            y='count',
            title="Articles Published Over Time",
            labels={'month': 'Month', 'count': 'Number of Articles'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Reviews over time
        reviews_df['publication_date'] = pd.to_datetime(reviews_df['publication_date'])
        reviews_df['month'] = reviews_df['publication_date'].dt.to_period('M')
        monthly_reviews = reviews_df.groupby('month').size().reset_index(name='count')
        monthly_reviews['month'] = monthly_reviews['month'].astype(str)
        
        fig = px.line(
            monthly_reviews,
            x='month',
            y='count',
            title="Reviews Published Over Time",
            labels={'month': 'Month', 'count': 'Number of Reviews'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Text analysis
    st.write("### 📝 Text Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Article content length
        fig = px.histogram(
            article_df,
            x='content_length',
            nbins=30,
            title="Article Content Length Distribution",
            labels={'content_length': 'Content Length (characters)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Review verdict length
        fig = px.histogram(
            reviews_df,
            x='verdict_length',
            nbins=30,
            title="Review Verdict Length Distribution",
            labels={'verdict_length': 'Verdict Length (characters)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)

def show_nlp_insights(results):
    """Show NLP insights page"""
    
    st.subheader("🧠 NLP Analysis Insights")
    
    if 'nlp_analysis' not in results:
        st.warning("NLP analysis results not available.")
        return
    
    nlp_data = results['nlp_analysis']
    
    # Sentiment analysis
    st.write("### 😊 Sentiment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Article sentiment
        article_sentiment = nlp_data['article_news']['sentiment']['contents']
        sentiment_data = pd.DataFrame([
            {'Sentiment': 'Positive', 'Score': article_sentiment['pos']},
            {'Sentiment': 'Neutral', 'Score': article_sentiment['neu']},
            {'Sentiment': 'Negative', 'Score': article_sentiment['neg']}
        ])
        
        fig = px.bar(
            sentiment_data,
            x='Sentiment',
            y='Score',
            title="Article Content Sentiment Distribution",
            color='Sentiment',
            color_discrete_map={'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Review sentiment
        review_sentiment = nlp_data['car_reviews']['sentiment']['verdicts']
        sentiment_data = pd.DataFrame([
            {'Sentiment': 'Positive', 'Score': review_sentiment['pos']},
            {'Sentiment': 'Neutral', 'Score': review_sentiment['neu']},
            {'Sentiment': 'Negative', 'Score': review_sentiment['neg']}
        ])
        
        fig = px.bar(
            sentiment_data,
            x='Sentiment',
            y='Score',
            title="Review Verdict Sentiment Distribution",
            color='Sentiment',
            color_discrete_map={'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top bigrams and trigrams
    st.write("### 🔤 Most Common Phrases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Article bigrams
        if 'bigrams' in nlp_data['article_news']:
            title_bigrams = nlp_data['article_news']['bigrams']['titles'][:10]
            bigram_data = pd.DataFrame(title_bigrams, columns=['Bigram', 'Count'])
            bigram_data['Bigram'] = bigram_data['Bigram'].apply(lambda x: ' '.join(x))
            
            fig = px.bar(
                bigram_data,
                x='Count',
                y='Bigram',
                orientation='h',
                title="Top Article Title Bigrams"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Review bigrams
        if 'bigrams' in nlp_data['car_reviews']:
            verdict_bigrams = nlp_data['car_reviews']['bigrams']['verdicts'][:10]
            bigram_data = pd.DataFrame(verdict_bigrams, columns=['Bigram', 'Count'])
            bigram_data['Bigram'] = bigram_data['Bigram'].apply(lambda x: ' '.join(x))
            
            fig = px.bar(
                bigram_data,
                x='Count',
                y='Bigram',
                orientation='h',
                title="Top Review Verdict Bigrams"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_correlations(results, reviews_df):
    """Show correlations page"""
    
    st.subheader("🔗 Correlation Analysis")
    
    if 'correlation_analysis' not in results:
        st.warning("Correlation analysis results not available.")
        return
    
    corr_data = results['correlation_analysis']
    
    # Price vs Rating correlation
    st.write("### 💰 Price vs Rating Correlation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot
        fig = px.scatter(
            reviews_df,
            x='price',
            y='rating',
            title="Price vs Rating Scatter Plot",
            labels={'price': 'Price (£)', 'rating': 'Rating'},
            trendline="ols"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Correlation metrics
        price_rating_corr = corr_data['price_rating_correlation']
        st.metric(
            label="Pearson Correlation",
            value=f"{price_rating_corr['pearson_correlation']:.3f}",
            delta=None
        )
        st.metric(
            label="P-value",
            value=f"{price_rating_corr['pearson_p_value']:.3f}",
            delta=None
        )
        st.metric(
            label="R-squared",
            value=f"{price_rating_corr['r_squared']:.3f}",
            delta=None
        )
    
    # Source correlations
    if 'source_correlations' in corr_data:
        st.write("### 📊 Source-based Analysis")
        
        source_data = []
        for source, data in corr_data['source_correlations'].items():
            source_data.append({
                'Source': source,
                'Sample Size': data['sample_size'],
                'Avg Rating': data['avg_rating'],
                'Avg Price': data['avg_price'],
                'Price-Rating Correlation': data['price_rating_correlation']
            })
        
        source_df = pd.DataFrame(source_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                source_df,
                x='Source',
                y='Avg Rating',
                title="Average Rating by Source",
                color='Avg Rating',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                source_df,
                x='Source',
                y='Avg Price',
                title="Average Price by Source",
                color='Avg Price',
                color_continuous_scale='plasma'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Price category analysis
    if 'price_category_correlations' in corr_data:
        st.write("### 🏷️ Price Category Analysis")
        
        category_data = []
        for category, data in corr_data['price_category_correlations'].items():
            category_data.append({
                'Category': category,
                'Sample Size': data['sample_size'],
                'Avg Rating': data['avg_rating'],
                'Avg Price': data['avg_price']
            })
        
        category_df = pd.DataFrame(category_data)
        
        fig = px.scatter(
            category_df,
            x='Avg Price',
            y='Avg Rating',
            size='Sample Size',
            color='Category',
            title="Average Rating vs Price by Category",
            labels={'Avg Price': 'Average Price (£)', 'Avg Rating': 'Average Rating'}
        )
        st.plotly_chart(fig, use_container_width=True)

def show_trends(article_df, reviews_df, results):
    """Show trends page"""
    
    st.subheader("📈 Trend Analysis")
    
    # Time series trends
    st.write("### ⏰ Time Series Trends")
    
    # Convert dates
    article_df['publication_date'] = pd.to_datetime(article_df['publication_date'])
    reviews_df['publication_date'] = pd.to_datetime(reviews_df['publication_date'])
    
    # Monthly trends
    article_df['month'] = article_df['publication_date'].dt.to_period('M')
    reviews_df['month'] = reviews_df['publication_date'].dt.to_period('M')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Article volume trend
        monthly_articles = article_df.groupby('month').size().reset_index(name='count')
        monthly_articles['month'] = monthly_articles['month'].astype(str)
        
        fig = px.line(
            monthly_articles,
            x='month',
            y='count',
            title="Article Publication Volume Trend",
            labels={'month': 'Month', 'count': 'Number of Articles'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Review volume trend
        monthly_reviews = reviews_df.groupby('month').size().reset_index(name='count')
        monthly_reviews['month'] = monthly_reviews['month'].astype(str)
        
        fig = px.line(
            monthly_reviews,
            x='month',
            y='count',
            title="Review Publication Volume Trend",
            labels={'month': 'Month', 'count': 'Number of Reviews'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Rating trends over time
    st.write("### ⭐ Rating Trends")
    
    monthly_ratings = reviews_df.groupby('month')['rating'].agg(['mean', 'count']).reset_index()
    monthly_ratings['month'] = monthly_ratings['month'].astype(str)
    
    fig = px.line(
        monthly_ratings,
        x='month',
        y='mean',
        title="Average Rating Trend Over Time",
        labels={'month': 'Month', 'mean': 'Average Rating'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Price trends over time
    st.write("### 💰 Price Trends")
    
    monthly_prices = reviews_df.groupby('month')['price'].agg(['mean', 'count']).reset_index()
    monthly_prices['month'] = monthly_prices['month'].astype(str)
    
    fig = px.line(
        monthly_prices,
        x='month',
        y='mean',
        title="Average Price Trend Over Time",
        labels={'month': 'Month', 'mean': 'Average Price (£)'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_raw_data(article_df, reviews_df):
    """Show raw data page"""
    
    st.subheader("📋 Raw Data Explorer")
    
    # Data selection
    data_type = st.selectbox("Select Data Type", ["Article News", "Car Reviews"])
    
    if data_type == "Article News":
        st.write("### Article News Data")
        st.dataframe(article_df, use_container_width=True)
        
        # Download button
        csv = article_df.to_csv(index=False)
        st.download_button(
            label="Download Article News CSV",
            data=csv,
            file_name="article_news_data.csv",
            mime="text/csv"
        )
    else:
        st.write("### Car Reviews Data")
        st.dataframe(reviews_df, use_container_width=True)
        
        # Download button
        csv = reviews_df.to_csv(index=False)
        st.download_button(
            label="Download Car Reviews CSV",
            data=csv,
            file_name="car_reviews_data.csv",
            mime="text/csv"
        )
    
    # Data statistics
    st.write("### 📊 Data Statistics")
    
    if data_type == "Article News":
        st.write(article_df.describe())
    else:
        st.write(reviews_df.describe())

if __name__ == "__main__":
    main()
