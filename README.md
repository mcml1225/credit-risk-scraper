# Credit Risk Intelligence Dashboard

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dashboard](https://img.shields.io/badge/Dashboard-Plotly%2FDash-green)](https://plotly.com/dash/)

## Real-time Credit Risk Monitoring System

Automated web scraping and visualization dashboard for credit risk news from the world's leading rating agencies: **Moody's, Fitch Ratings, and S&P Global**.

## Features

- **Automated Scraping**: Daily extraction of credit risk news and research at 10:00 AM GMT-5
- **Smart Date Filtering**: Only collects articles from the last 48 hours (today and yesterday)
- **Multi-Source Aggregation**: Collects data from all three major rating agencies
- **Interactive Dashboard**: Real-time visualizations with Plotly/Dash
- **GitHub Actions Automation**: Runs twice daily without manual intervention
- **Historical Data Storage**: CSV and JSON formats for further analysis
- **Fault Tolerance**: Graceful fallback to sample data when scrapers fail
- **Configurable Scheduling**: Easy to modify execution time and frequency

## Technology Stack

| Category | Technologies |
|----------|-------------|
| **Scraping** | Python, Requests, BeautifulSoup4, Selenium |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Dash, Dash Bootstrap Components |
| **Automation** | GitHub Actions, Schedule |
| **Testing** | Pytest, Pytest-cov |
| **Logging** | Loguru |

## Project Structure
credit-risk-scraper/
├── .github/workflows/ # GitHub Actions automation
│ └── scrape_daily.yml # Daily scraping workflow (10:00 AM GMT-5)
├── src/
│ ├── scrapers/ # Individual scrapers for each agency
│ │ ├── moodys_scraper.py # Moody's - Real data extraction
│ │ ├── fitch_scraper.py # Fitch - Sample data fallback
│ │ └── sp_scraper.py # S&P Global - Sample data fallback
│ ├── dashboard/ # Interactive dashboard
│ │ └── app.py # Full dashboard application
│ └── utils/ # Utility functions
│ └── data_processor.py # Data cleaning and aggregation
├── data/ # Data storage
│ ├── raw/ # Unprocessed scraped data (CSV)
│ └── processed/ # Cleaned and aggregated data (JSON)
├── logs/ # Application logs
├── dashboard_simple.py # Simplified working dashboard
├── test_simple.py # Test script for all scrapers
├── main.py # Main execution with scheduler
├── config.py # Configuration settings
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore rules
└── README.md # This file


## Installation

### Prerequisites
- Python 3.11 or higher
- Git
- pip package manager

### Local Setup


# Clone the repository
git clone https://github.com/mmonto37/credit-risk-scraper.git
cd credit-risk-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run initial scrape
python main.py once

# Launch dashboard
python dashboard_simple.py
Usage Examples
Run a one-time scrape

python main.py once
Run with scheduler (waits for next execution)

python main.py
Run only the dashboard

python dashboard_simple.py
Test all scrapers

python test_simple.py
View collected data
python
import pandas as pd
df = pd.read_csv('data/raw/all_articles_*.csv')
print(df[['source', 'title', 'date']].head())
Dashboard Features
The interactive dashboard provides:

Key Metrics Cards

Total articles collected

Number of active sources

Last update timestamp

Source Distribution Chart

Bar chart comparing news volume by agency

Color-coded by rating agency

Temporal Analysis

Time-series line chart of news volume

Shows trends from last 48 hours

Content Type Distribution

Pie chart showing types of content (Research, Data Story, Report, etc.)

Latest Headlines Feed

List of most recent articles

Shows source, title, and date

Automation with GitHub Actions
The scraper runs automatically at 10:00 AM GMT-5 daily.

Manual Trigger
Go to your repository on GitHub

Click on "Actions" tab

Select "Daily Credit Risk Scraper"

Click "Run workflow" -> "Run workflow"

Viewing Results
After each run, the workflow:

Executes all three scrapers

Filters articles from last 48 hours only

Processes and cleans the data

Commits new data to the repository

Updates the data/ directory

Data Schema
Raw Data (data/raw/all_articles_*.csv)
csv
source,title,content_type,url,date,scraped_at
Moody's,"Private credit volatility intensifies",Research,https://...,2026-04-24,2026-04-24T10:00:00
Processed Summary (data/processed/summary_*.json)
json
{
  "timestamp": "2026-04-24T10:00:00",
  "total_articles": 12,
  "articles_by_source": {
    "Moody's": 3,
    "S&P Global": 5,
    "Fitch": 4
  },
  "date_range": {
    "start": "2026-04-23",
    "end": "2026-04-24"
  }
}
Monitored Keywords
The system tracks these credit risk indicators:

Primary Terms
credit risk, default, downgrade, upgrade

rating action, outlook, credit quality

Market Segments
sovereign debt, corporate debt, structured finance

credit spread, CDS, non-performing loan

Risk Indicators
bankruptcy, insolvency, restructuring

credit cycle, rating transition, distressed debt

Configuration
Edit config.py to customize:

python
# Change execution time (in main.py)
schedule.every().day.at("10:00").do(run_scraping)

# Modify date range for filtering (in each scraper)
self.cutoff_date = datetime.now().date() - timedelta(days=1)

# Adjust request timeout
REQUEST_TIMEOUT = 15

# Add custom keywords for filtering
CREDIT_RISK_KEYWORDS = ['custom_keyword1', 'custom_keyword2']
Testing

# Run the simple test script
python test_simple.py

# Test individual scraper
python -c "from src.scrapers.moodys_scraper import MoodysScraper; s = MoodysScraper(); df = s.get_articles_last_48h(); print(f'Found {len(df)} articles')"
Troubleshooting
Common Issues & Solutions
Issue	Solution
Moody's scraper finds 0 articles	Website structure may have changed. Update CSS selectors in moodys_scraper.py
S&P Global returns 403 error	S&P blocks automated requests. The scraper automatically falls back to sample data
Dashboard won't load	Ensure port 8050 is free: netstat -ano | findstr :8050
Module not found errors	Run pip install -r requirements.txt
Date filtering not working	Check system timezone is set correctly for GMT-5
Debug Mode
python
# In config.py
LOG_LEVEL = "DEBUG"

# This will show detailed scraping logs
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

Development Guidelines
Follow PEP 8 style guide

Add docstrings to new functions

Update tests for new features

Keep dependencies minimal

License
Distributed under the MIT License. See LICENSE file for more information.

Authors
Your Name - @mmonto37

Acknowledgments
Moody's Investor Services for credit risk insights

Fitch Ratings for research publications

S&P Global Ratings for market analysis

Plotly/Dash team for visualization framework

All open-source contributors

Disclaimer
This project is for educational and research purposes only. Always respect:

Website terms of service

robots.txt files

Rate limiting guidelines

Copyright and intellectual property rights

The authors assume no liability for misuse of this software or violation of website policies.