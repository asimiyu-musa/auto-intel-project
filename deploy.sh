#!/bin/bash

# Auto Intel Project EC2 Deployment Script
# This script sets up the environment and deploys the project to EC2

set -e

echo "🚀 Starting Auto Intel Project deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt-get update -y

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    print_success "Docker installed successfully"
else
    print_status "Docker is already installed"
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    print_status "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed successfully"
else
    print_status "Docker Compose is already installed"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs data

# Set proper permissions
print_status "Setting permissions..."
sudo chown -R $USER:$USER logs data

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file..."
    cat > .env << EOF
# Airflow Configuration
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=.
AIRFLOW_IMAGE_NAME=apache/airflow:3.0.3

# Airflow User
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin123

# Additional Requirements (if needed)
_PIP_ADDITIONAL_REQUIREMENTS=
EOF
    print_success ".env file created"
else
    print_status ".env file already exists"
fi

# Build the Docker image
print_status "Building Docker image..."
docker-compose build auto-intel-scrapy

# Function to start services
start_services() {
    local profile=$1
    print_status "Starting services with profile: $profile"
    
    if [ "$profile" = "full" ]; then
        docker-compose --profile full up -d
    elif [ "$profile" = "scrapy" ]; then
        docker-compose --profile scrapy up -d
    else
        docker-compose up -d
    fi
}

# Function to check service health
check_health() {
    print_status "Checking service health..."
    
    # Wait for services to start
    sleep 30
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Services are running"
        
        # Show running containers
        print_status "Running containers:"
        docker-compose ps
        
        # Show Airflow UI info
        print_success "Airflow UI is available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
        print_status "Username: admin"
        print_status "Password: admin123"
        
    else
        print_error "Some services failed to start"
        docker-compose logs
        exit 1
    fi
}

# Function to run tests
run_tests() {
    print_status "Running tests in container..."
    docker-compose run --rm auto-intel-scrapy ./entrypoint.sh test
}

# Function to run spiders
run_spiders() {
    print_status "Running spiders..."
    docker-compose run --rm auto-intel-scrapy ./entrypoint.sh all
}

# Main deployment logic
case "${1:-full}" in
    "full")
        print_status "Deploying full stack (Airflow + Scrapy)..."
        start_services "full"
        check_health
        ;;
    "scrapy")
        print_status "Deploying Scrapy only..."
        start_services "scrapy"
        check_health
        ;;
    "test")
        print_status "Running tests..."
        run_tests
        ;;
    "spiders")
        print_status "Running spiders..."
        run_spiders
        ;;
    "logs")
        print_status "Showing logs..."
        docker-compose logs -f
        ;;
    "stop")
        print_status "Stopping services..."
        docker-compose down
        ;;
    "restart")
        print_status "Restarting services..."
        docker-compose restart
        ;;
    "help"|*)
        echo "Usage: $0 {full|scrapy|test|spiders|logs|stop|restart|help}"
        echo ""
        echo "Commands:"
        echo "  full     - Deploy full stack (Airflow + Scrapy)"
        echo "  scrapy   - Deploy Scrapy only"
        echo "  test     - Run tests"
        echo "  spiders  - Run spiders"
        echo "  logs     - Show logs"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  help     - Show this help message"
        exit 1
        ;;
esac

print_success "Deployment completed successfully!" 