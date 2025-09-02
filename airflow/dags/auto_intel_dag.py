from __future__ import annotations

import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

# Constants (UPPER_SNAKE_CASE convention)
SCRAPY_PROJECT_PATH = "/opt/airflow/projects/auto_intel_project"
CONTAINER_PYTHON_PATH = "/usr/local/bin/python"

with DAG(
    dag_id="auto_intel_scraper_dag",
    start_date=pendulum.datetime(2025, 7, 24, tz="Europe/London"),
    schedule="@daily",
    catchup=False,
    tags=["scraping", "auto_intel"],
) as dag:
    # Task 1: Run auto_reviews spider
    run_auto_reviews_spider = BashOperator(
        task_id="run_auto_reviews_spider",
        bash_command=(
            f'cd "{SCRAPY_PROJECT_PATH}" && '
            f"{CONTAINER_PYTHON_PATH} -m scrapy crawl auto_reviews"
        ),
    )

    # Task 2: Run auto_news spider
    run_auto_news_spider = BashOperator(
        task_id="run_auto_news_spider",
        bash_command=(
            f'cd "{SCRAPY_PROJECT_PATH}" && '
            f"{CONTAINER_PYTHON_PATH} -m scrapy crawl auto_news"
        ),
    )

    # Task dependencies (using bit-shift operator)
    run_auto_reviews_spider >> run_auto_news_spider