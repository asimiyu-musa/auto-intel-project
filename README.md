# Auto Intel Project

A comprehensive web scraping project for automotive news and reviews using Scrapy and Apache Airflow for orchestration, now fully containerized and ready for EC2 deployment.

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd auto_intel_project

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run spiders
scrapy crawl auto_news
scrapy crawl auto_reviews
```

### Docker Deployment
```bash
# Build and run with Docker
docker-compose build auto-intel-scrapy
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
```

### EC2 Deployment
```bash
# Deploy to EC2 (see ec2-setup.md for detailed instructions)
chmod +x deploy.sh entrypoint.sh
./deploy.sh full
```

## 📁 Project Structure

```
auto_intel_project/
├── auto_intel/                 # Main Scrapy project
│   ├── __init__.py
│   ├── items.py               # Scrapy item definitions
│   ├── middlewares.py         # Custom middlewares
│   ├── settings.py            # Scrapy settings
│   └── spiders/               # Spider implementations
│       ├── __init__.py        # Spider package initialization
│       ├── auto_news.py       # News spider
│       └── auto_reviews.py    # Reviews spider
├── airflow/                   # Apache Airflow configuration
│   ├── config/
│   ├── dags/
│   │   └── auto_intel_dag.py  # Airflow DAG for orchestration
│   ├── logs/
│   └── plugins/
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_items.py         # Tests for Scrapy items
│   └── test_models.py        # Tests for spider models
├── logs/                      # Application logs
├── data/                      # Scraped data storage
├── scrapy.cfg                # Scrapy project configuration
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker container definition
├── docker-compose.yaml      # Docker orchestration
├── entrypoint.sh            # Container entrypoint script
├── deploy.sh                # EC2 deployment automation
├── .dockerignore            # Docker build exclusions
├── pytest.ini              # Test configuration
├── .gitignore              # Git exclusions
├── README.md               # This file
├── ec2-setup.md            # EC2 deployment guide
└── DEPLOYMENT_SUMMARY.md   # Complete deployment overview
```

## 🎯 Features

### Scrapy Spiders

1. **AutoNewsSpider** (`auto_news`)
   - Scrapes automotive news from:
     - Car Magazine UK (20 pages)
     - PistonHeads (1 page)
     - Auto Express (8 pages total - car news and consumer issues)
   - Extracts: title, link, author, publication date, source, content

2. **AutoReviewsSpider** (`auto_reviews`)
   - Scrapes car reviews from:
     - Auto Express (30 pages)
     - Carbuyer (30 pages)
   - Extracts: title, link, author, publication date, source, verdict, rating, price

### Airflow Orchestration

- **auto_intel_scraper_dag**: Daily scheduled DAG that runs both spiders
- Sequential execution: reviews spider → news spider
- Configurable project paths and Python environments
- Web UI for monitoring and manual triggers

### Docker Containerization

- **Multi-stage build** with Python 3.11-slim
- **Flexible entrypoint** for different operations
- **Health checks** and monitoring
- **Volume mounts** for persistent data
- **Integrated** with existing Airflow setup

### Custom Middlewares

- **RandomUserAgentMiddleware**: Rotates user agents to avoid detection
- **AutoIntelDownloaderMiddleware**: Standard downloader middleware

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auto_intel_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the setup**
   ```bash
   # Run tests
   pytest tests/
   
   # Test spiders individually
   scrapy crawl auto_news
   scrapy crawl auto_reviews
   ```

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose build auto-intel-scrapy
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
   ```

2. **Run spiders in container**
   ```bash
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
   ```

3. **Access container shell**
   ```bash
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh shell
   ```

### EC2 Deployment

1. **Launch EC2 instance** (t3.medium or larger recommended)
2. **Clone repository** to EC2
3. **Run deployment script**
   ```bash
   chmod +x deploy.sh entrypoint.sh
   ./deploy.sh full
   ```
4. **Access Airflow UI** at `http://your-ec2-ip:8080`

See `ec2-setup.md` for detailed EC2 deployment instructions.

## 📊 Usage

### Running Spiders Manually

```bash
# Local development
scrapy crawl auto_news
scrapy crawl auto_reviews

# Docker container
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_news
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_reviews
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
```

### Running Tests

```bash
# Local development
pytest tests/

# Docker container
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
```

### Airflow DAG Management

```bash
# Check DAG status
airflow dags list

# Trigger DAG manually
airflow dags trigger auto_intel_scraper_dag

# View DAG logs
airflow tasks logs auto_intel_scraper_dag run_auto_reviews_spider latest
```

### Docker Commands

```bash
# List available spiders
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list

# Run specific spider
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_news

# Run all spiders
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all

# Run tests
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test

# Access shell
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh shell
```

## ⚙️ Configuration

### Scrapy Settings

Key settings in `auto_intel/settings.py`:

- `DOWNLOAD_DELAY`: 1 second between requests
- `CONCURRENT_REQUESTS_PER_DOMAIN`: 16 concurrent requests
- `ROBOTSTXT_OBEY`: True (respects robots.txt)
- `USER_AGENTS`: List of user agents for rotation
- `AUTOTHROTTLE_ENABLED`: True (automatic throttling)

### Airflow Configuration

DAG settings in `airflow/dags/auto_intel_dag.py`:

- **Schedule**: Daily (`@daily`)
- **Start Date**: July 24, 2025
- **Timezone**: Europe/London
- **Project Path**: `/opt/airflow/projects/auto_intel_project`

### Docker Configuration

- **Base Image**: Python 3.11-slim
- **Volumes**: `./logs:/app/logs`, `./data:/app/data`
- **Health Checks**: Container health monitoring
- **Networks**: Integrated with Airflow network

## 📋 Data Models

### ArticleItem
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

### CarReviewItem
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

## 🔧 Development

### Adding New Spiders

1. Create new spider file in `auto_intel/spiders/`
2. Inherit from `scrapy.Spider`
3. Define `name`, `allowed_domains`, and parsing methods
4. Add corresponding tests in `tests/test_models.py`
5. Update `auto_intel/spiders/__init__.py` to import the new spider

### Adding New Items

1. Define new item class in `auto_intel/items.py`
2. Inherit from `scrapy.Item`
3. Define fields using `scrapy.Field()`
4. Add corresponding tests in `tests/test_items.py`

### Code Quality

```bash
# Format code
black auto_intel/ tests/

# Lint code
flake8 auto_intel/ tests/

# Run type checking (if using mypy)
mypy auto_intel/
```

## 🚀 Deployment

### Local Docker Deployment

```bash
# Build image
docker-compose build auto-intel-scrapy

# Run tests
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test

# Run spiders
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
```

### EC2 Deployment

```bash
# Deploy full stack
./deploy.sh full

# Deploy Scrapy only
./deploy.sh scrapy

# Run tests
./deploy.sh test

# View logs
./deploy.sh logs
```

### Production Considerations

1. **Security**: Change default passwords in `.env`
2. **Monitoring**: Set up CloudWatch or similar
3. **Backup**: Regular backups of data and logs
4. **Scaling**: Use larger instance types for production
5. **SSL**: Set up HTTPS with reverse proxy

## 📊 Monitoring & Logs

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs auto-intel-scrapy
docker-compose logs airflow-scheduler

# Follow logs in real-time
docker-compose logs -f
```

### Health Checks

```bash
# Container status
docker-compose ps

# Resource usage
docker stats

# Service health
docker-compose exec auto-intel-scrapy python -c "import scrapy; print('Scrapy OK')"
```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Check `PYTHONPATH` includes project root

2. **Spider Not Found**
   - Verify spider name matches class name
   - Check `scrapy.cfg` configuration
   - Ensure spider is imported in `__init__.py`

3. **Docker Issues**
   - Rebuild containers: `docker-compose build --no-cache`
   - Check logs: `docker-compose logs`
   - Clean up: `docker system prune -a`

4. **Airflow DAG Not Appearing**
   - Restart Airflow webserver
   - Check DAG file syntax
   - Verify file permissions

### Health Checks

```bash
# Quick health check
docker-compose ps && docker-compose logs --tail=50

# Run tests
./deploy.sh test

# Check spider discovery
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list
```

## 📚 Documentation

- **`ec2-setup.md`**: Detailed EC2 deployment guide
- **`DEPLOYMENT_SUMMARY.md`**: Complete deployment overview
- **`README.md`**: This file (project overview)
- **`requirements.txt`**: Python dependencies
- **`pytest.ini`**: Test configuration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run test suite: `pytest tests/`
5. Submit pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
- Check logs: `./deploy.sh logs`
- Run tests: `./deploy.sh test`
- Review documentation: `README.md`, `ec2-setup.md`
- Check container status: `docker-compose ps`
- Create GitHub issue for bugs or feature requests

---

## 🎉 Success Indicators

Your project is working correctly when:
- ✅ All tests pass: `pytest tests/`
- ✅ Spiders are detected: `scrapy list`
- ✅ Docker builds successfully: `docker-compose build`
- ✅ Containers run without errors: `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test`
- ✅ Airflow UI is accessible (if deployed)
- ✅ Spiders can be executed manually and via Airflow

**Happy Scraping! 🕷️**
