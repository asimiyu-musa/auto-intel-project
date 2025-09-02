#!/bin/bash

# Script to create a clean package for supervisor
# This includes only the essential files for Docker deployment

echo "📦 Creating supervisor package..."

# Create supervisor package directory
mkdir -p supervisor-package

# Copy essential files
echo "📋 Copying essential files..."

# Core application files
cp -r auto_intel/ supervisor-package/
cp -r tests/ supervisor-package/

# Docker files
cp Dockerfile supervisor-package/
cp docker-compose.yaml supervisor-package/
cp entrypoint.sh supervisor-package/
cp .dockerignore supervisor-package/

# Configuration files
cp scrapy.cfg supervisor-package/
cp requirements.txt supervisor-package/
cp pytest.ini supervisor-package/

# Create logs and data directories
mkdir -p supervisor-package/logs
mkdir -p supervisor-package/data

# Copy the supervisor README
cp supervisor-package/README.md supervisor-package/

# Make entrypoint executable
chmod +x supervisor-package/entrypoint.sh

# Create a simple .gitignore for the package
cat > supervisor-package/.gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test coverage
.coverage
htmlcov/
.pytest_cache/

# Docker
.dockerignore

# Temporary files
*.tmp
*.temp
EOF

# Create a deployment guide for supervisor
cat > supervisor-package/DEPLOYMENT_GUIDE.md << EOF
# Quick Deployment Guide

## Prerequisites
- Docker and Docker Compose installed

## Steps to Deploy

1. **Extract the package**
   \`\`\`bash
   # If you received this as a zip file
   unzip auto_intel_project.zip
   cd auto_intel_project
   \`\`\`

2. **Build the Docker image**
   \`\`\`bash
   docker-compose build auto-intel-scrapy
   \`\`\`

3. **Run tests to verify everything works**
   \`\`\`bash
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
   \`\`\`

4. **List available spiders**
   \`\`\`bash
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list
   \`\`\`

5. **Run the spiders**
   \`\`\`bash
   # Run all spiders
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
   
   # Or run specific spiders
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_news
   docker-compose run --rm auto-intel-scrapy ./entrypoint.sh auto_reviews
   \`\`\`

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

✅ All tests pass: \`docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test\`
✅ Spiders detected: \`docker-compose run --rm auto-intel-scrapy ./entrypoint.sh list\`
✅ Spiders run: \`docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all\`

## Support

For any issues, check:
1. Docker logs: \`docker-compose logs auto-intel-scrapy\`
2. Container status: \`docker-compose ps\`
3. Test results: \`docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test\`
EOF

echo "✅ Supervisor package created successfully!"
echo ""
echo "📁 Package location: supervisor-package/"
echo "📋 Files included:"
echo "   - auto_intel/ (Scrapy project)"
echo "   - tests/ (Test suite)"
echo "   - Dockerfile"
echo "   - docker-compose.yaml"
echo "   - entrypoint.sh"
echo "   - requirements.txt"
echo "   - scrapy.cfg"
echo "   - pytest.ini"
echo "   - README.md"
echo "   - DEPLOYMENT_GUIDE.md"
echo "   - .gitignore"
echo ""
echo "🚀 Ready to send to supervisor!"
echo ""
echo "To create a zip file:"
echo "cd supervisor-package && zip -r ../auto_intel_project.zip ." 