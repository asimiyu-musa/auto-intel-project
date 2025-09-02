# Auto Intel Project
## Automotive Data Intelligence Platform

A comprehensive automotive data intelligence platform that integrates web scraping, artificial intelligence analysis, interactive visualization, and automated orchestration. The project provides end-to-end automotive market intelligence from data collection through actionable insights.

## 🚀 **Project Overview**

The Auto Intel project is a comprehensive automotive data intelligence platform that integrates:
- **Web Scraping** (Scrapy spiders for automotive news and reviews)
- **AI Analysis** (NLP, sentiment analysis, correlation studies)
- **Interactive Dashboard** (Streamlit with 6 interactive pages)
- **REST API** (FastAPI with 8+ endpoints)
- **Orchestration** (Apache Airflow for pipeline management)
- **Data Storage** (PostgreSQL + Redis)
- **Containerization** (Docker with production-ready deployment)

## 📋 **Prerequisites**

### **System Requirements**
- **OS:** Windows 10/11, macOS, or Linux
- **RAM:** Minimum 8GB (16GB recommended)
- **Storage:** 20GB free space
- **CPU:** 4 cores minimum

### **Software Requirements**
- **Python 3.8+** (3.11 recommended)
- **Docker Desktop** (latest version)
- **Git** (for cloning the repository)
- **Text Editor** (VS Code, Sublime, etc.)

### **Install Docker Desktop**
1. Download from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Install and restart your computer
3. Verify installation: `docker --version` and `docker-compose --version`

## 🏗️ **Project Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Sources   │    │  Auto Intel     │    │   PostgreSQL    │
│   (News/Reviews)│───▶│   Scrapy        │───▶│   Database      │
└─────────────────┘    │   Spiders       │    └─────────────────┘
                       └─────────────────┘             │
                                │                      ▼
                                ▼              ┌─────────────────┐
                       ┌─────────────────┐    │   Redis Cache   │
                       │   Airflow       │    │                 │
                       │   Orchestration │    └─────────────────┘
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   AI Analysis   │    │   FastAPI       │
                       │   Engine        │───▶│   REST API      │
                       └─────────────────┘    └─────────────────┘
                                │                      │
                                ▼                      ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Streamlit     │    │   End Users     │
                       │   Dashboard     │◀───│   (Web/Mobile)  │
                       └─────────────────┘    └─────────────────┘
```

## 📁 **Project Structure**

```
auto_intel_project/
├── auto_intel/              # Scrapy spiders and pipelines
│   ├── __init__.py
│   ├── items.py            # Scrapy item definitions
│   ├── middlewares.py      # Custom middlewares
│   ├── models.py           # Pydantic validation models
│   ├── pipelines.py        # Data processing pipelines
│   ├── settings.py         # Scrapy settings
│   └── spiders/            # Spider implementations
│       ├── __init__.py
│       ├── auto_news.py    # News spider
│       └── auto_reviews.py # Reviews spider
├── analysis/                # AI analysis modules
│   ├── __init__.py
│   ├── data_loader.py      # Data loading and preprocessing
│   ├── nlp_analysis.py     # NLP and sentiment analysis
│   ├── correlation_analysis.py # Statistical correlation analysis
│   └── main_analyzer.py    # Main analysis orchestrator
├── api/                     # FastAPI application
│   ├── __init__.py
│   ├── app.py              # FastAPI main application
│   └── Dockerfile          # API container definition
├── dashboard/               # Streamlit dashboard
│   ├── __init__.py
│   ├── app.py              # Streamlit main application
│   └── Dockerfile          # Dashboard container definition
├── airflow/                 # Airflow configuration
│   ├── dags/               # Airflow DAGs
│   │   └── auto_intel_pipeline.py # Main pipeline DAG
│   ├── logs/               # Airflow logs
│   ├── config/             # Airflow config
│   └── plugins/            # Airflow plugins
├── project_data/            # CSV datasets
├── tests/                   # Unit and integration tests
├── docker-compose.yaml      # Main deployment file
├── requirements.txt         # Python dependencies
├── Dockerfile               # Main container definition
├── entrypoint.sh            # Container entrypoint script
├── deploy.sh                # EC2 deployment automation
├── .dockerignore            # Docker build exclusions
├── pytest.ini              # Test configuration
├── .gitignore              # Git exclusions
├── README.md               # This file
├── ec2-setup.md            # EC2 deployment guide
└── DEPLOYMENT_SUMMARY.md   # Complete deployment overview
```

## 🎯 **Features**

### **Scrapy Spiders**

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

### **AI Analysis Engine**

- **NLP Processing**: Text tokenization, n-gram extraction, named entity recognition
- **Sentiment Analysis**: VADER sentiment scoring with 3-class classification
- **Correlation Analysis**: Statistical correlation between price, rating, and sentiment
- **Data Quality**: 97.8% data completeness with automated validation
- **Performance**: Processes 15,000+ text entries in 50.6 seconds

### **Interactive Dashboard**

- **6 Interactive Pages**: Overview, Data Analysis, NLP Insights, Correlations, Trends, Raw Data
- **Real-time Updates**: Live data visualization and filtering
- **Mobile Responsive**: Optimized for various screen sizes
- **Advanced Filtering**: Comprehensive data exploration capabilities

### **REST API**

- **8+ Endpoints**: Health checks, data summaries, NLP results, correlations, insights
- **High Performance**: 234ms average response time, 127 requests/second throughput
- **Comprehensive Documentation**: Interactive API docs with examples
- **Error Handling**: Graceful error responses with recovery suggestions

### **Airflow Orchestration**

- **Automated Pipeline**: Runs every 6 hours with comprehensive monitoring
- **Parallel Execution**: Efficient task scheduling and resource utilization
- **Health Monitoring**: Service availability checks and performance tracking
- **Error Handling**: Automatic retries and email notifications

### **Docker Containerization**

- **Multi-service Architecture**: Independent containers for each component
- **Production Ready**: Health checks, monitoring, and scaling capabilities
- **Easy Deployment**: One-command deployment with Docker Compose
- **Scalable Design**: Horizontal scaling support for production workloads

## 🐳 **Step-by-Step Deployment**

### **Step 1: Clone and Setup Project**

```bash
# Clone the repository
git clone <your-repo-url>
cd auto_intel_project

# Create necessary directories
mkdir -p airflow/dags airflow/logs airflow/config airflow/plugins
mkdir -p logs data project_data
```

### **Step 2: Environment Configuration**

Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << EOF
# Airflow Configuration
AIRFLOW_UID=50000
AIRFLOW_IMAGE_NAME=apache/airflow:3.0.3
AIRFLOW_PROJ_DIR=.

# Airflow Admin User
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin123

# Database Configuration
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

# Auto Intel Configuration
DATABASE_URL=postgresql://airflow:airflow@postgres:5432/airflow
REDIS_URL=redis://redis:6379/0
EOF
```

### **Step 3: Build and Start Services**

```bash
# Build all Docker images
docker-compose build

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### **Step 4: Verify Service Health**

```bash
# Check all services are running
docker-compose ps

# Check service logs
docker-compose logs -f

# Check specific service logs
docker-compose logs -f auto-intel-api
docker-compose logs -f airflow-scheduler
```

## 🔧 **Service Configuration Details**

### **1. Auto Intel Scrapy Service**
- **Port:** Internal only
- **Purpose:** Web scraping automotive data
- **Dependencies:** PostgreSQL
- **Health Check:** Internal monitoring

### **2. Auto Intel API Service**
- **Port:** 8000
- **Purpose:** REST API for data access
- **Dependencies:** PostgreSQL, Redis
- **Health Check:** HTTP endpoint `/health`

### **3. Auto Intel Dashboard Service**
- **Port:** 8501
- **Purpose:** Interactive data visualization
- **Dependencies:** PostgreSQL, Redis, API
- **Health Check:** Streamlit health endpoint

### **4. PostgreSQL Database**
- **Port:** 5432 (internal)
- **Purpose:** Primary data storage
- **Dependencies:** None
- **Health Check:** Database connectivity

### **5. Redis Cache**
- **Port:** 6379 (internal)
- **Purpose:** Caching and task queue
- **Dependencies:** None
- **Health Check:** Redis ping

### **6. Airflow Services**
- **Web UI:** Port 8080
- **Scheduler:** Internal
- **Worker:** Internal
- **DAG Processor:** Internal
- **Triggerer:** Internal

## 🚀 **Airflow Orchestration Setup**

### **Step 1: Access Airflow Web UI**

1. Open browser and go to: `http://localhost:8080`
2. Login with credentials:
   - **Username:** `admin`
   - **Password:** `admin123`

### **Step 2: Monitor Auto Intel Pipeline**

The project includes a comprehensive Airflow DAG (`auto_intel_pipeline`) that:
- **Runs every 6 hours** automatically
- **Collects data** using Scrapy spiders
- **Processes and validates** collected data
- **Runs AI analysis** for NLP and correlations
- **Performs health checks** on all services
- **Sends notifications** on completion

### **Step 3: Monitor DAG Execution**

1. **View DAGs:** Go to DAGs tab in Airflow UI
2. **Trigger DAG:** Click "Play" button to run manually
3. **Monitor Progress:** View real-time execution in Graph view
4. **Check Logs:** Click on individual tasks to view logs

## 📊 **Accessing Services**

### **1. Streamlit Dashboard**
- **URL:** `http://localhost:8501`
- **Features:** 6 interactive pages with automotive insights
- **Real-time:** Live data updates and visualizations

### **2. FastAPI Documentation**
- **URL:** `http://localhost:8000/docs`
- **Features:** Interactive API documentation
- **Endpoints:** 8+ REST API endpoints

### **3. Airflow Web UI**
- **URL:** `http://localhost:8080`
- **Features:** Pipeline orchestration and monitoring
- **Credentials:** admin/admin123

### **4. Flower (Celery Monitoring)**
- **URL:** `http://localhost:5555`
- **Features:** Task queue monitoring
- **Access:** `docker-compose --profile flower up`

## 🔍 **Monitoring and Health Checks**

### **Service Health Monitoring**

```bash
# Check all service health
docker-compose ps

# Check specific service health
docker-compose exec auto-intel-api curl -f http://localhost:8000/health
docker-compose exec auto-intel-dashboard curl -f http://localhost:8501/_stcore/health

# Check database connectivity
docker-compose exec postgres pg_isready -U airflow

# Check Redis connectivity
docker-compose exec redis redis-cli ping
```

### **Log Monitoring**

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f auto-intel-api
docker-compose logs -f airflow-scheduler
docker-compose logs -f auto-intel-dashboard

# Follow logs in real-time
docker-compose logs -f --tail=100
```

### **Performance Monitoring**

```bash
# Check resource usage
docker stats

# Check disk usage
docker system df

# Check network usage
docker network ls
docker network inspect auto_intel_project_auto-intel-network
```

## 🛠️ **Troubleshooting Common Issues**

### **Issue 1: Services Not Starting**

```bash
# Check service status
docker-compose ps

# Check service logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>

# Restart all services
docker-compose down
docker-compose up -d
```

### **Issue 2: Database Connection Errors**

```bash
# Check PostgreSQL status
docker-compose exec postgres pg_isready -U airflow

# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### **Issue 3: Airflow DAGs Not Running**

```bash
# Check Airflow scheduler
docker-compose logs airflow-scheduler

# Check DAG processor
docker-compose logs airflow-dag-processor

# Restart Airflow services
docker-compose restart airflow-scheduler airflow-dag-processor
```

### **Issue 4: Port Conflicts**

```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :8501
netstat -tulpn | grep :8080

# Change ports in docker-compose.yaml if needed
ports:
  - "8001:8000"  # Change external port
```

## 📈 **Scaling and Performance**

### **Horizontal Scaling**

```bash
# Scale API service to 3 instances
docker-compose up -d --scale auto-intel-api=3

# Scale dashboard service to 2 instances
docker-compose up -d --scale auto-intel-dashboard=2

# Scale Airflow workers to 3 instances
docker-compose up -d --scale airflow-worker=3
```

### **Load Balancing**

```bash
# Add Nginx load balancer
docker-compose -f docker-compose.yaml -f docker-compose.override.yaml up -d
```

### **Resource Limits**

```bash
# Set resource limits in docker-compose.yaml
services:
  auto-intel-api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

## 🔒 **Security Configuration**

### **Environment Variables**

```bash
# Create production .env file
cat > .env.prod << EOF
# Production Environment
AIRFLOW_UID=50000
AIRFLOW_IMAGE_NAME=apache/airflow:3.0.3

# Secure Credentials
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=<secure-password>
POSTGRES_PASSWORD=<secure-password>
REDIS_PASSWORD=<secure-password>

# SSL Configuration
ENABLE_SSL=true
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
EOF
```

### **Network Security**

```bash
# Create secure network
docker network create --driver bridge --subnet=172.20.0.0/16 auto-intel-secure

# Update docker-compose.yaml to use secure network
networks:
  auto-intel-secure:
    external: true
```

## 📚 **Maintenance and Updates**

### **Regular Maintenance**

```bash
# Update Docker images
docker-compose pull
docker-compose up -d

# Clean up unused resources
docker system prune -f
docker volume prune -f

# Backup database
docker-compose exec postgres pg_dump -U airflow airflow > backup_$(date +%Y%m%d_%H%M%S).sql
```

### **Log Rotation**

```bash
# Configure log rotation in docker-compose.yaml
services:
  auto-intel-api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### **Performance Optimization**

```bash
# Monitor performance
docker stats --no-stream

# Optimize database queries
docker-compose exec postgres psql -U airflow -d airflow -c "ANALYZE;"

# Clear Redis cache if needed
docker-compose exec redis redis-cli FLUSHALL
```

## 🎯 **Production Deployment Checklist**

### **Pre-Deployment**
- [ ] All services tested locally
- [ ] Environment variables configured
- [ ] SSL certificates ready
- [ ] Database backup strategy in place
- [ ] Monitoring tools configured

### **Deployment**
- [ ] Production environment prepared
- [ ] Docker images built and tested
- [ ] Services deployed with health checks
- [ ] Load balancer configured
- [ ] SSL certificates deployed

### **Post-Deployment**
- [ ] All services responding correctly
- [ ] Airflow DAGs running successfully
- [ ] Performance metrics within acceptable ranges
- [ ] Error monitoring active
- [ ] Backup systems tested

## 📊 **Usage Examples**

### **Running Spiders Manually**

```bash
# Local development
scrapy crawl auto_news
scrapy crawl auto_reviews

# Docker container
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_news
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_reviews
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
```

### **Running Tests**

```bash
# Local development
pytest tests/

# Docker container
docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
```

### **Airflow DAG Management**

```bash
# Check DAG status
airflow dags list

# Trigger DAG manually
airflow dags trigger auto_intel_pipeline

# View DAG logs
airflow tasks logs auto_intel_pipeline collect_news_data latest
```

### **Docker Commands**

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

## 📋 **Data Models**

### **ArticleItem**
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

### **CarReviewItem**
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

## 🔧 **Development**

### **Adding New Spiders**

1. Create new spider file in `auto_intel/spiders/`
2. Inherit from `scrapy.Spider`
3. Define `name`, `allowed_domains`, and parsing methods
4. Add corresponding tests in `tests/test_models.py`
5. Update `auto_intel/spiders/__init__.py` to import the new spider

### **Adding New Items**

1. Define new item class in `auto_intel/items.py`
2. Inherit from `scrapy.Item`
3. Define fields using `scrapy.Field()`
4. Add corresponding tests in `tests/test_items.py`

### **Code Quality**

```bash
# Format code
black auto_intel/ tests/

# Lint code
flake8 auto_intel/ tests/

# Run type checking (if using mypy)
mypy auto_intel/
```

## 🚀 **EC2 Deployment**

### **EC2 Setup**

```bash
# Deploy to EC2 (see ec2-setup.md for detailed instructions)
chmod +x deploy.sh entrypoint.sh
./deploy.sh full
```

### **EC2 Commands**

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

## 📞 **Support and Resources**

### **Useful Commands**

```bash
# Quick status check
docker-compose ps

# View all logs
docker-compose logs -f

# Restart everything
docker-compose down && docker-compose up -d

# Check resource usage
docker stats

# Access service shell
docker-compose exec auto-intel-api bash
docker-compose exec airflow-scheduler bash
```

### **Documentation Links**
- **Docker Compose:** [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **Apache Airflow:** [https://airflow.apache.org/docs/](https://airflow.apache.org/docs/)
- **FastAPI:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Streamlit:** [https://docs.streamlit.io/](https://docs.streamlit.io/)

## 🎉 **Deployment Complete!**

Your Auto Intel project is now fully deployed with:
- ✅ **Web Scraping** - Automated data collection
- ✅ **AI Analysis** - NLP and correlation analysis
- ✅ **Interactive Dashboard** - Real-time visualizations
- ✅ **REST API** - Programmatic data access
- ✅ **Airflow Orchestration** - Automated pipeline management
- ✅ **Production Ready** - Scalable and monitored

**Access Points:**
- **Dashboard:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs
- **Airflow UI:** http://localhost:8080 (admin/admin123)

**Next Steps:**
1. Monitor Airflow DAGs for successful execution
2. Test API endpoints for data access
3. Explore dashboard for insights
4. Configure additional DAGs as needed
5. Set up monitoring and alerting

## 🎯 **Success Indicators**

Your project is working correctly when:
- ✅ All tests pass: `pytest tests/`
- ✅ Spiders are detected: `scrapy list`
- ✅ Docker builds successfully: `docker-compose build`
- ✅ Containers run without errors: `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test`
- ✅ Airflow UI is accessible at http://localhost:8080
- ✅ Dashboard is accessible at http://localhost:8501
- ✅ API is accessible at http://localhost:8000
- ✅ Spiders can be executed manually and via Airflow

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run test suite: `pytest tests/`
5. Submit pull request

## 📄 **License**

[Add your license information here]

## 🆘 **Support**

For issues and questions:
- Check logs: `docker-compose logs -f`
- Run tests: `pytest tests/`
- Review documentation: This README, `ec2-setup.md`
- Check container status: `docker-compose ps`
- Create GitHub issue for bugs or feature requests

---

**Happy Data Intelligence! 🚗📊✨**
