"""
Credit Risk Scraper - Main Execution Script
Runs daily at 10:00 AM GMT-5 and only collects articles from last 48 hours
"""

import schedule
import time
from datetime import datetime, timedelta
import pandas as pd
from loguru import logger
from pathlib import Path

from src.scrapers.moodys_scraper import MoodysScraper
from src.scrapers.fitch_scraper import FitchScraper
from src.scrapers.sp_scraper import SPScraper
from src.utils.data_processor import DataProcessor

# Configure logging
log_file = Path("logs") / f"scraper_{datetime.now().strftime('%Y%m%d')}.log"
log_file.parent.mkdir(exist_ok=True)

logger.add(
    log_file,
    rotation="1 day",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Define timezone offset for GMT-5
# Note: This assumes the system is running in GMT-5
# If not, you may need to install pytz: pip install pytz

def run_scraping():
    """
    Execute scraping for all agencies.
    Only collects articles from last 48 hours.
    """
    logger.info("=" * 60)
    logger.info(f"SCRAPING STARTED at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} GMT-5")
    logger.info("Filtering articles from last 48 hours only")
    logger.info("=" * 60)
    
    results = {}
    
    # Scrape Moody's
    try:
        logger.info("\n📊 Scraping Moody's...")
        moodys = MoodysScraper()
        df_moodys = moodys.get_articles_last_48h()
        results['Moody\'s'] = df_moodys
        logger.info(f"   ✅ Moody's: {len(df_moodys)} articles from last 48 hours")
        if len(df_moodys) > 0:
            logger.debug(f"   📅 Dates: {df_moodys['date'].unique()}")
    except Exception as e:
        logger.error(f"   ❌ Moody's failed: {e}")
        results['Moody\'s'] = pd.DataFrame()
    
    # Scrape Fitch
    try:
        logger.info("\n📊 Scraping Fitch...")
        fitch = FitchScraper()
        df_fitch = fitch.get_articles_last_48h() if hasattr(fitch, 'get_articles_last_48h') else fitch.scrape_research()
        results['Fitch'] = df_fitch
        logger.info(f"   ✅ Fitch: {len(df_fitch)} articles from last 48 hours")
    except Exception as e:
        logger.error(f"   ❌ Fitch failed: {e}")
        results['Fitch'] = pd.DataFrame()
    
    # Scrape S&P Global
    try:
        logger.info("\n📊 Scraping S&P Global...")
        sp = SPScraper()
        df_sp = sp.get_articles_last_48h() if hasattr(sp, 'get_articles_last_48h') else sp.scrape_insights()
        results['S&P Global'] = df_sp
        logger.info(f"   ✅ S&P Global: {len(df_sp)} articles from last 48 hours")
    except Exception as e:
        logger.error(f"   ❌ S&P Global failed: {e}")
        results['S&P Global'] = pd.DataFrame()
    
    # Process and save all data
    try:
        logger.info("\n📦 Processing and saving data...")
        processor = DataProcessor()
        
        # Combine all articles
        all_articles = pd.concat(results.values(), ignore_index=True)
        
        # Save raw data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_file = Path("data/raw") / f"all_articles_{timestamp}.csv"
        raw_file.parent.mkdir(parents=True, exist_ok=True)
        all_articles.to_csv(raw_file, index=False)
        logger.info(f"   💾 Raw data saved: {raw_file}")
        
        # Generate summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_articles': len(all_articles),
            'articles_by_source': {k: len(v) for k, v in results.items()},
            'date_range': {
                'start': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'end': datetime.now().strftime('%Y-%m-%d')
            }
        }
        
        # Save summary
        summary_file = Path("data/processed") / f"summary_{timestamp}.json"
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        logger.info(f"   📊 Summary saved: {summary_file}")
        
        # Print final summary
        logger.info("\n" + "=" * 60)
        logger.info("SCRAPING COMPLETED SUCCESSFULLY")
        logger.info(f"📈 Total articles collected: {len(all_articles)}")
        for source, df in results.items():
            logger.info(f"   • {source}: {len(df)} articles")
        logger.info(f"📅 Date range: Last 48 hours")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Error processing data: {e}")
    
    return results

def run_dashboard():
    """Run the dashboard server."""
    from src.dashboard.app import app
    logger.info("🚀 Starting dashboard server...")
    app.run_server(debug=False, host='0.0.0.0', port=8050)

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == 'dashboard':
        # Run dashboard only
        run_dashboard()
    elif len(sys.argv) > 1 and sys.argv[1] == 'once':
        # Run scraping once
        run_scraping()
    else:
        # Schedule daily execution at 10:00 AM GMT-5
        # Note: Schedule uses system time. Ensure system is set to GMT-5
        # or use pytz for timezone awareness
        
        logger.info("=" * 60)
        logger.info("CREDIT RISK SCRAPER - SCHEDULER STARTED")
        logger.info(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("Scheduled execution: Daily at 10:00 AM (GMT-5)")
        logger.info("=" * 60)
        
        # Run once immediately on startup
        logger.info("\n🚀 Running initial scrape...")
        run_scraping()
        
        # Schedule daily at 10:00 AM
        schedule.every().day.at("10:00").do(run_scraping)
        
        logger.info("\n⏰ Scheduler is running. Waiting for next scheduled time...")
        logger.info("Press CTRL+C to stop\n")
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute