# Auto Intel Project - Complete Deployment Guide

## 🚀 Overview

This guide provides comprehensive instructions for deploying the Auto Intel project, including all components: Scrapy spiders, FastAPI, Streamlit dashboard, and Airflow orchestration.

## 📋 Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows 10+
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **Python**: 3.11+
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 50GB+ available space
- **Network**: Stable internet connection

### Software Installation
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version
```

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Sources   │    │  News Websites  │    │ Car Review Sites│
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     Scrapy Spiders        │
                    │  (AutoNewsSpider)         │
                    │  (AutoReviewsSpider)      │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Data Validation         │
                    │   (Pydantic Models)       │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   PostgreSQL Database     │
                    └─────────────┬─────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
┌─────────▼─────────┐  ┌─────────▼─────────┐  ┌─────────▼─────────┐
│   Analysis Engine │  │   FastAPI Server  │  │ Streamlit Dashboard│
│   (NLP, Corr.)    │  │   (REST API)      │  │   (Web UI)        │
└─────────┬─────────┘  └─────────┬─────────┘  └─────────┬─────────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Apache Airflow          │
                    │   (Orchestration)         │
                    └───────────────────────────┘
```

## 🔧 Local Development Setup

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd auto_intel_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install spaCy model
python -m spacy download en_core_web_sm
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```bash
# Database Configuration
DATABASE_URL=postgresql://airflow:airflow@localhost:5432/airflow
REDIS_URL=redis://localhost:6379/0

# Airflow Configuration
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=.

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Dashboard Configuration
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8501

# Scrapy Configuration
SCRAPY_LOG_LEVEL=INFO
SCRAPY_DELAY=1
```

### 3. Database Setup
```bash
# Start PostgreSQL and Redis
docker-compose up postgres redis -d

# Wait for services to be ready
docker-compose ps

# Initialize Airflow database
docker-compose up airflow-init
```

## 🐳 Docker Deployment

### 1. Build All Services
```bash
# Build all Docker images
docker-compose build

# Or build specific services
docker-compose build auto-intel-scrapy
docker-compose build auto-intel-api
docker-compose build auto-intel-dashboard
```

### 2. Start All Services
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Service URLs
After deployment, services will be available at:
- **Airflow Web UI**: http://localhost:8080
- **FastAPI**: http://localhost:8000
- **Streamlit Dashboard**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

## 🔄 Production Deployment

### 1. Production Environment Variables
Create `production.env`:
```bash
# Production Database
DATABASE_URL=postgresql://user:password@prod-db:5432/auto_intel
REDIS_URL=redis://prod-redis:6379/0

# Security
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# SSL/TLS
SSL_CERT_FILE=/path/to/cert.pem
SSL_KEY_FILE=/path/to/key.pem

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=WARNING
```

### 2. Production Docker Compose
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - auto-intel-api
      - auto-intel-dashboard

  auto-intel-api:
    build:
      context: .
      dockerfile: api/Dockerfile
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
    networks:
      - auto-intel-network

  auto-intel-dashboard:
    build:
      context: .
      dockerfile: dashboard/Dockerfile
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    restart: unless-stopped
    networks:
      - auto-intel-network

networks:
  auto-intel-network:
    driver: bridge
```

### 3. Nginx Configuration
Create `nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server auto-intel-api:8000;
    }

    upstream dashboard {
        server auto-intel-dashboard:8501;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location /api/ {
            proxy_pass http://api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location / {
            proxy_pass http://dashboard/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## 🔍 Monitoring and Logging

### 1. Health Checks
```bash
# Check API health
curl http://localhost:8000/health

# Check dashboard health
curl http://localhost:8501/_stcore/health

# Check Airflow health
curl http://localhost:8080/health
```

### 2. Log Monitoring
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f auto-intel-api
docker-compose logs -f auto-intel-dashboard
docker-compose logs -f auto-intel-scrapy

# View Airflow logs
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler
```

### 3. Performance Monitoring
```bash
# Check resource usage
docker stats

# Monitor database connections
docker-compose exec postgres psql -U airflow -d airflow -c "SELECT * FROM pg_stat_activity;"

# Check Redis memory usage
docker-compose exec redis redis-cli info memory
```

## 🔒 Security Configuration

### 1. SSL/TLS Setup
```bash
# Generate SSL certificate (for development)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem -out ssl/cert.pem

# For production, use Let's Encrypt or commercial certificates
```

### 2. Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 3. Database Security
```bash
# Change default passwords
docker-compose exec postgres psql -U airflow -d airflow -c "ALTER USER airflow PASSWORD 'strong-password';"

# Enable SSL for database connections
# Add to DATABASE_URL: ?sslmode=require
```

## 📊 Scaling and Performance

### 1. Horizontal Scaling
```yaml
# docker-compose.scale.yml
services:
  auto-intel-api:
    deploy:
      replicas: 3
    environment:
      - WORKERS=4

  auto-intel-dashboard:
    deploy:
      replicas: 2
```

### 2. Load Balancing
```nginx
# nginx.conf with load balancing
upstream api {
    server auto-intel-api-1:8000;
    server auto-intel-api-2:8000;
    server auto-intel-api-3:8000;
}
```

### 3. Caching Strategy
```python
# Redis caching configuration
REDIS_CACHE_TTL = 3600  # 1 hour
REDIS_CACHE_PREFIX = "auto_intel:"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check what's using the ports
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :8501

# Kill processes if needed
sudo kill -9 <PID>
```

#### 2. Database Connection Issues
```bash
# Check database status
docker-compose exec postgres pg_isready -U airflow

# Reset database if needed
docker-compose down -v
docker-compose up postgres -d
docker-compose up airflow-init
```

#### 3. Memory Issues
```bash
# Check memory usage
docker stats

# Increase Docker memory limit
# In Docker Desktop: Settings > Resources > Memory
```

#### 4. Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x entrypoint.sh
```

### Debug Commands
```bash
# Enter running container
docker-compose exec auto-intel-api bash
docker-compose exec auto-intel-dashboard bash

# Check service logs
docker-compose logs --tail=100 auto-intel-api

# Restart specific service
docker-compose restart auto-intel-api

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📈 Performance Optimization

### 1. Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_article_news_publication_date ON article_news(publication_date);
CREATE INDEX idx_car_reviews_rating ON car_reviews(rating);
CREATE INDEX idx_car_reviews_price ON car_reviews(price);

-- Analyze tables
ANALYZE article_news;
ANALYZE car_reviews;
```

### 2. API Optimization
```python
# Enable response caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

### 3. Dashboard Optimization
```python
# Streamlit caching
@st.cache_data(ttl=3600)
def load_data():
    # Expensive data loading operation
    pass
```

## 🔄 CI/CD Pipeline

### 1. GitHub Actions Setup
```bash
# Add secrets to GitHub repository
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password
PRODUCTION_HOST=your-server-ip
PRODUCTION_USER=your-server-user
```

### 2. Automated Deployment
The CI/CD pipeline will:
- Run tests on every push
- Build Docker images
- Deploy to staging on develop branch
- Deploy to production on main branch

### 3. Rollback Strategy
```bash
# Rollback to previous version
docker-compose down
docker image tag your-registry/auto-intel-api:previous-version your-registry/auto-intel-api:latest
docker-compose up -d
```

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

### Monitoring Tools
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Sentry**: Error tracking
- **ELK Stack**: Log management

### Backup Strategy
```bash
# Database backup
docker-compose exec postgres pg_dump -U airflow airflow > backup_$(date +%Y%m%d_%H%M%S).sql

# Volume backup
docker run --rm -v auto_intel_project_data:/data -v $(pwd):/backup alpine tar czf /backup/data_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

---

## 🎯 Quick Start Checklist

- [ ] Install Docker and Docker Compose
- [ ] Clone repository and setup environment
- [ ] Configure environment variables
- [ ] Build Docker images
- [ ] Start services with docker-compose
- [ ] Verify all services are running
- [ ] Test API endpoints
- [ ] Access dashboard
- [ ] Configure Airflow DAGs
- [ ] Set up monitoring and logging
- [ ] Configure SSL/TLS (production)
- [ ] Set up backup strategy
- [ ] Configure CI/CD pipeline

---

*This deployment guide ensures a robust, scalable, and maintainable deployment of the Auto Intel project.*
