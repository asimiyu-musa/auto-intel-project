# Quick Deployment Guide

## Prerequisites
- Docker and Docker Compose installed

## Steps to Deploy

1. **Extract the package**
   ```bash
   # If you received this as a zip file
   unzip auto_intel_project.zip
   cd auto_intel_project
   ```

2. **Build the Docker image**
   ```bash
   docker-compose build auto-intel-scrapy
   ```

3. **Run tests to verify everything works**
   ```bash
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
   ```

4. **List available spiders**
   ```bash
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list
   ```

5. **Run the spiders**
   ```bash
   # Run all spiders
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
   
   # Or run specific spiders
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_news
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_reviews
   ```

## What This Package Contains

- **Scrapy Project**: Complete web scraping application
- **Docker Configuration**: Ready-to-deploy container setup
- **Test Suite**: Comprehensive testing (23/23 tests passing)
- **Documentation**: Complete usage guide

## Features

- **Two Spiders**: News and reviews scraping
- **Data Models**: Structured data extraction
- **Docker Containerization**: Easy deployment
- **Comprehensive Testing**: Quality assurance
- **Monitoring**: Logs and health checks

## Success Indicators

✅ All tests pass: `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test`
✅ Spiders detected: `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list`
✅ Spiders run: `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all`

## Support

For any issues, check:
1. Docker logs: `docker-compose logs auto-intel-scrapy`
2. Container status: `docker-compose ps`
3. Test results: `docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test`
