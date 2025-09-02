#!/bin/bash
set -e

# Function to run a spider
run_spider() {
    local spider_name=$1
    echo "Starting spider: $spider_name"
    python -m scrapy crawl "$spider_name" -L INFO
}

# Function to run all spiders
run_all_spiders() {
    echo "Running all spiders..."
    run_spider "auto_news"
    run_spider "auto_reviews"
}

# Function to run tests
run_tests() {
    echo "Running tests..."
    python -m pytest tests/ -v
}

# Function to show available spiders
list_spiders() {
    echo "Available spiders:"
    python -m scrapy list
}

# Main script logic
case "${1:-help}" in
    "auto_news")
        run_spider "auto_news"
        ;;
    "auto_reviews")
        run_spider "auto_reviews"
        ;;
    "all")
        run_all_spiders
        ;;
    "test")
        run_tests
        ;;
    "list")
        list_spiders
        ;;
    "shell")
        exec /bin/bash
        ;;
    "help"|*)
        echo "Usage: $0 {auto_news|auto_reviews|all|test|list|shell}"
        echo ""
        echo "Commands:"
        echo "  auto_news    - Run the auto_news spider"
        echo "  auto_reviews - Run the auto_reviews spider"
        echo "  all          - Run all spiders"
        echo "  test         - Run the test suite"
        echo "  list         - List available spiders"
        echo "  shell        - Start an interactive shell"
        echo "  help         - Show this help message"
        exit 1
        ;;
esac 