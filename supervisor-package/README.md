# Auto Intel Project - Docker Deployment

A web scraping project for automotive news and reviews using Scrapy, containerized with Docker for easy deployment.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (for cloning)

### Deployment Steps

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd auto_intel_project
   ```

2. **Build and test the Docker image**
   ```bash
   docker-compose build auto-intel-scrapy
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
   ```

3. **Run the spiders**
   ```bash
   # List available spiders
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list
   
   # Run all spiders
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
   
   # Run specific spider
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_news
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_reviews
   ```

## 📁 Project Structure

```
auto_intel_project/
├── auto_intel/                 # Scrapy project
│   ├── __init__.py
│   ├── items.py               # Data models
│   ├── middlewares.py         # Custom middlewares
│   ├── settings.py            # Scrapy configuration
│   └── spiders/               # Spider implementations
│       ├── __init__.py
│       ├── auto_news.py       # News spider
│       └── auto_reviews.py    # Reviews spider
├── tests/                     # Test suite
│   ├── test_items.py         # Item tests
│   └── test_models.py        # Spider tests
├── logs/                      # Application logs
├── data/                      # Scraped data
├── scrapy.cfg                # Scrapy project config
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container definition
├── docker-compose.yaml      # Docker orchestration
├── entrypoint.sh            # Container entrypoint
├── .dockerignore            # Docker build exclusions
├── pytest.ini              # Test configuration
└── README.md               # This file
```

## 🎯 Features

### Scrapy Spiders

1. **AutoNewsSpider** (`auto_news`)
   - Scrapes automotive news from:
     - Car Magazine UK (20 pages)
     - PistonHeads (1 page)
     - Auto Express (8 pages)
   - Extracts: title, link, author, publication date, source, content

2. **AutoReviewsSpider** (`auto_reviews`)
   - Scrapes car reviews from:
     - Auto Express (30 pages)
     - Carbuyer (30 pages)
   - Extracts: title, link, author, publication date, source, verdict, rating, price

### Docker Containerization

- **Base Image**: Python 3.11-slim
- **Health Checks**: Container monitoring
- **Volume Mounts**: Persistent logs and data
- **Flexible Entrypoint**: Multiple operation modes

## 📊 Usage

### Container Commands

```bash
# List available spiders
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list

# Run specific spider
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_news
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_reviews

# Run all spiders
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all

# Run tests
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test

# Access container shell
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh shell
```

### Data Models

**ArticleItem** (for news articles):
```python
{
    'title': str,           # Article title
    'link': str,            # Article URL
    'author': str,          # Author name
    'publication_date': date, # Publication date
    'source': str,          # Source website
    'content': str          # Article content
}
```

**CarReviewItem** (for car reviews):
```python
{
    'title': str,           # Review title
    'link': str,            # Review URL
    'author': str,          # Author name
    'publication_date': date, # Publication date
    'source': str,          # Source website
    'verdict': str,         # Review verdict
    'rating': float,        # Numerical rating
    'price': int           # Car price in GBP
}
```

## 🧪 Testing

### Run All Tests
```bash
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
```

### Test Coverage
- **23/23 tests passing**
- Tests cover item creation, spider functionality, and compatibility
- Automated testing in containerized environment

## 📈 Monitoring

### View Logs
```bash
# Container logs
docker-compose logs auto-intel-scrapy

# Follow logs in real-time
docker-compose logs -f auto-intel-scrapy
```

### Health Checks
```bash
# Container status
docker-compose ps

# Resource usage
docker stats
```

## 🔧 Configuration

### Scrapy Settings (`auto_intel/settings.py`)
- `DOWNLOAD_DELAY`: 1 second between requests
- `CONCURRENT_REQUESTS_PER_DOMAIN`: 16 concurrent requests
- `ROBOTSTXT_OBEY`: True (respects robots.txt)
- `USER_AGENTS`: List of user agents for rotation
- `AUTOTHROTTLE_ENABLED`: True (automatic throttling)

### Docker Configuration
- **Volumes**: `./logs:/app/logs`, `./data:/app/data`
- **Health Checks**: Container health monitoring
- **Entrypoint**: Flexible command interface

## 🛠️ Troubleshooting

### Common Issues

1. **Build Issues**
   ```bash
   # Rebuild without cache
   docker-compose build --no-cache auto-intel-scrapy
   ```

2. **Permission Issues**
   ```bash
   # Fix permissions
   chmod +x entrypoint.sh
   ```

3. **Container Issues**
   ```bash
   # Check container logs
   docker-compose logs auto-intel-scrapy
   
   # Access container shell
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh shell
   ```

## ✅ Success Indicators

Your deployment is working correctly when:
- ✅ `docker-compose build auto-intel-scrapy` completes successfully
- ✅ `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test` passes all tests
- ✅ `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list` shows both spiders
- ✅ `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all` runs without errors

## 📋 Files Included

### Core Application
- `auto_intel/` - Complete Scrapy project with spiders and items
- `tests/` - Comprehensive test suite
- `requirements.txt` - Python dependencies

### Docker Configuration
- `Dockerfile` - Container definition
- `docker-compose.yaml` - Docker orchestration
- `entrypoint.sh` - Container entrypoint script
- `.dockerignore` - Build optimizations

### Configuration
- `scrapy.cfg` - Scrapy project configuration
- `pytest.ini` - Test configuration
- `README.md` - This documentation

---

**Ready for deployment! 🚀**

This package contains everything needed to run the Auto Intel Project in a Docker container, with comprehensive testing and monitoring capabilities. 