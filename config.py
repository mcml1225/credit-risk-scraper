"""
Configuration file for the Credit Risk Scraper project.
Contains all constants, URLs, and settings used across the application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================== SCRAPING CONFIGURATION ====================

# Browser headers to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# Request timeout in seconds
REQUEST_TIMEOUT = 15

# Number of retry attempts for failed requests
MAX_RETRIES = 3

# Delay between requests to avoid rate limiting (seconds)
REQUEST_DELAY = 2

# ==================== SOURCE URLs ====================

# Moody's Investor Services
MOODYS_BASE_URL = "https://www.moodys.com"
MOODYS_NEWS_URL = "https://www.moodys.com/news-and-events/news"
MOODYS_RESEARCH_URL = "https://www.moodys.com/research"

# Fitch Ratings
FITCH_BASE_URL = "https://www.fitchratings.com"
FITCH_RESEARCH_URL = "https://www.fitchratings.com/research"
FITCH_RATING_ACTIONS_URL = "https://www.fitchratings.com/rating-actions"

# S&P Global Ratings
SP_BASE_URL = "https://www.spglobal.com"
SP_INSIGHTS_URL = "https://www.spglobal.com/ratings/en/research-insights"
SP_RATINGS_URL = "https://www.spglobal.com/ratings/en/ratings-direct"

# ==================== KEYWORDS FOR FILTERING ====================

# Keywords related to credit risk for filtering relevant news
CREDIT_RISK_KEYWORDS = [
    'credit risk', 'credit rating', 'credit quality',
    'default', 'default rate', 'default probability',
    'downgrade', 'upgrade', 'rating action',
    'outlook', 'negative outlook', 'positive outlook',
    'sovereign debt', 'corporate debt', 'structured finance',
    'credit spread', 'credit default swap', 'CDS',
    'non-performing loan', 'NPL', 'distressed debt',
    'bankruptcy', 'insolvency', 'restructuring',
    'credit cycle', 'credit migration', 'rating transition'
]

# Keywords to exclude (false positives)
EXCLUDED_KEYWORDS = [
    'sports', 'entertainment', 'weather', 'politics',
    'advertisement', 'sponsored', 'opinion'
]

# ==================== DATA PATHS ====================

# Base directory for data storage
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ==================== DASHBOARD CONFIGURATION ====================

DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", 8050))
DASHBOARD_DEBUG = os.getenv("DASHBOARD_DEBUG", "False").lower() == "true"

# Refresh interval for dashboard (milliseconds)
DASHBOARD_REFRESH_INTERVAL = 3600000  # 1 hour

# ==================== LOGGING CONFIGURATION ====================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "scraper.log"

# ==================== NOTIFICATIONS (Optional) ====================

# Email configuration (if using email alerts)
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")

# Telegram configuration (if using Telegram alerts)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")