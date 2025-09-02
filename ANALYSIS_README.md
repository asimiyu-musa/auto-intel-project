# Auto Intel Analysis Platform

This document provides a comprehensive guide to the Auto Intel Analysis Platform, which includes AI-powered analysis, interactive dashboards, and API services for automotive data insights.

## 🎯 Overview

The Auto Intel Analysis Platform is a comprehensive solution that transforms scraped automotive data into actionable insights through:

1. **AI Analysis** - NLP, sentiment analysis, correlation analysis
2. **Interactive Dashboard** - Streamlit-based visualization platform
3. **API Services** - FastAPI-based REST API for data access
4. **Docker Deployment** - Containerized deployment solution

## 📁 Project Structure

```
auto_intel_project/
├── analysis/                    # Analysis modules
│   ├── __init__.py
│   ├── data_loader.py          # Data loading and preprocessing
│   ├── nlp_analysis.py         # NLP and sentiment analysis
│   ├── correlation_analysis.py # Correlation analysis
│   └── main_analyzer.py        # Main analysis orchestrator
├── dashboard/                   # Streamlit dashboard
│   └── app.py                  # Main dashboard application
├── api/                        # FastAPI application
│   └── app.py                  # API endpoints
├── project_data/               # CSV data files
│   ├── article_news_*.csv
│   └── car_reviews_*.csv
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install spaCy Model (for NLP)

```bash
python -m spacy download en_core_web_sm
```

### 3. Run Analysis

```bash
# Run comprehensive analysis
python -m analysis.main_analyzer

# Or run individual components
python -m analysis.data_loader
python -m analysis.nlp_analysis
python -m analysis.correlation_analysis
```

### 4. Launch Dashboard

```bash
streamlit run dashboard/app.py
```

### 5. Start API Server

```bash
python api/app.py
```

## 🔍 AI Analysis Features

### 1. NLP Analysis (`analysis/nlp_analysis.py`)

**Bigrams & Trigrams Analysis**
- Extracts most common word pairs and triplets
- Identifies trending automotive terminology
- Analyzes language patterns in titles and content

**Sentiment Analysis**
- VADER sentiment analysis for articles and reviews
- Sentiment tracking over time
- Positive/negative/neutral classification

**Named Entity Recognition (NER)**
- Extracts car brands, models, and locations
- Identifies key automotive entities
- Tracks brand mentions and trends

**Usage Example:**
```python
from analysis.nlp_analysis import NLPAnalyzer

analyzer = NLPAnalyzer()
results = analyzer.analyze_article_news(article_df)
print(f"Sentiment: {results['sentiment']['contents']}")
print(f"Top Bigrams: {results['bigrams']['titles'][:5]}")
```

### 2. Correlation Analysis (`analysis/correlation_analysis.py`)

**Price-Rating Correlation**
- Analyzes relationship between car prices and ratings
- Statistical significance testing
- Correlation strength assessment

**Source-based Analysis**
- Compares ratings across different sources
- Identifies source bias patterns
- Quality assessment by publication

**Time Series Analysis**
- Tracks trends over time
- Seasonal pattern identification
- Market trend analysis

**Usage Example:**
```python
from analysis.correlation_analysis import CorrelationAnalyzer

analyzer = CorrelationAnalyzer()
results = analyzer.run_comprehensive_correlation_analysis(article_df, reviews_df)
print(f"Price-Rating Correlation: {results['price_rating_correlation']['pearson_correlation']}")
```

### 3. Data Preprocessing (`analysis/data_loader.py`)

**Data Cleaning**
- Handles missing values
- Standardizes date formats
- Removes duplicates and outliers

**Feature Engineering**
- Creates price categories (Budget, Mid-range, Premium, etc.)
- Generates rating categories (Poor, Average, Good, Excellent)
- Calculates text length metrics

**Data Validation**
- Schema validation
- Data type checking
- Quality assessment

## 📊 Interactive Dashboard

### Features

1. **Overview Page**
   - Key metrics and KPIs
   - Data distribution charts
   - Source analysis

2. **Data Analysis Page**
   - Time series analysis
   - Text length distributions
   - Publication trends

3. **NLP Insights Page**
   - Sentiment analysis visualization
   - Bigram/trigram charts
   - Entity extraction results

4. **Correlations Page**
   - Price vs rating scatter plots
   - Source-based analysis
   - Correlation matrices

5. **Trends Page**
   - Time series trends
   - Rating and price trends
   - Market analysis

6. **Raw Data Page**
   - Data explorer
   - Download functionality
   - Statistical summaries

### Usage

```bash
# Start the dashboard
streamlit run dashboard/app.py

# Access at http://localhost:8501
```

## 🔌 API Services

### Endpoints

1. **GET /** - API information
2. **GET /health** - Health check
3. **GET /summary** - Analysis summary
4. **GET /data** - Data summary
5. **GET /nlp** - NLP analysis results
6. **GET /correlations** - Correlation analysis
7. **GET /insights** - Key insights
8. **GET /raw-data/{type}** - Raw data access
9. **GET /stats/{type}** - Statistics
10. **GET /search** - Search functionality

### Usage Examples

```bash
# Get analysis summary
curl http://localhost:8000/summary

# Get NLP results
curl http://localhost:8000/nlp

# Search for specific terms
curl "http://localhost:8000/search?query=tesla&limit=10"

# Get statistics
curl http://localhost:8000/stats/reviews
```

### API Documentation

Access interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the analysis image
docker build -t auto-intel-analysis .

# Run the analysis container
docker run -p 8501:8501 -p 8000:8000 auto-intel-analysis

# Or use docker-compose
docker-compose up analysis
```

### Docker Compose Configuration

```yaml
services:
  analysis:
    build: .
    ports:
      - "8501:8501"  # Streamlit dashboard
      - "8000:8000"  # FastAPI
    volumes:
      - ./project_data:/app/project_data
      - ./analysis_results:/app/analysis_results
```

## 📈 Analysis Results

### Output Files

The analysis generates several output files:

1. **analysis_results_YYYYMMDD_HHMMSS.json** - Complete analysis results
2. **insights_report_YYYYMMDD_HHMMSS.json** - Key insights and findings
3. **data_summary_YYYYMMDD_HHMMSS.json** - Data statistics

### Key Metrics

- **Data Volume**: Total articles and reviews analyzed
- **Sentiment Scores**: Overall sentiment for articles and reviews
- **Correlation Coefficients**: Price-rating relationships
- **Trend Indicators**: Time-based patterns and changes
- **Entity Frequencies**: Most mentioned brands and models

## 🔧 Configuration

### Environment Variables

```bash
# Database configuration (if using PostgreSQL)
POSTGRES_HOST=localhost
POSTGRES_DB=auto_intel
POSTGRES_USER=user
POSTGRES_PASSWORD=password

# Analysis configuration
ANALYSIS_CACHE_ENABLED=true
ANALYSIS_OUTPUT_DIR=analysis_results
```

### Customization

1. **Add New Analysis Modules**
   - Create new Python files in `analysis/`
   - Implement analysis methods
   - Update `main_analyzer.py`

2. **Extend Dashboard**
   - Add new pages in `dashboard/app.py`
   - Create custom visualizations
   - Implement new features

3. **API Extensions**
   - Add new endpoints in `api/app.py`
   - Implement additional data access methods
   - Create new search functionalities

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test modules
pytest tests/test_analysis.py
pytest tests/test_dashboard.py
pytest tests/test_api.py
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=analysis --cov=dashboard --cov=api tests/
```

## 📊 Performance Optimization

### Caching

- Streamlit caching for data loading
- FastAPI response caching
- Analysis result caching

### Memory Management

- Lazy loading for large datasets
- Chunked processing for big data
- Memory-efficient data structures

### Scalability

- Modular architecture
- Containerized deployment
- Horizontal scaling support

## 🔒 Security Considerations

1. **API Security**
   - Input validation
   - Rate limiting
   - CORS configuration

2. **Data Privacy**
   - Data anonymization
   - Access controls
   - Secure storage

3. **Deployment Security**
   - Environment variable management
   - Container security
   - Network isolation

## 📚 API Documentation

### Authentication

Currently, the API is open access. For production deployment, implement authentication:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    # Implement token verification
    pass
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

## 🚀 Production Deployment

### Recommended Setup

1. **Load Balancer**: Nginx or HAProxy
2. **Application Server**: Gunicorn with uvicorn workers
3. **Database**: PostgreSQL for persistent storage
4. **Monitoring**: Prometheus + Grafana
5. **Logging**: ELK Stack or similar

### Environment Configuration

```bash
# Production environment variables
export ENVIRONMENT=production
export LOG_LEVEL=INFO
export API_HOST=0.0.0.0
export API_PORT=8000
export DASHBOARD_PORT=8501
```

## 📞 Support and Maintenance

### Monitoring

- Health check endpoints
- Performance metrics
- Error tracking
- Usage analytics

### Logging

- Structured logging
- Error reporting
- Performance monitoring
- Audit trails

### Updates

- Regular dependency updates
- Security patches
- Feature enhancements
- Bug fixes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Add tests
5. Submit a pull request

## 📄 License

[Add your license information here]

---

## 🎉 Success Indicators

Your analysis platform is working correctly when:

- ✅ All analysis modules run without errors
- ✅ Dashboard loads and displays data correctly
- ✅ API endpoints return expected responses
- ✅ Docker containers start successfully
- ✅ Analysis results are generated and saved
- ✅ Visualizations render properly
- ✅ Search functionality works as expected

**Happy Analyzing! 🚗📊**
