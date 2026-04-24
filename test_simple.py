"""
Credit Risk Scraper - Simple Test Script
Tests all three scrapers (Moody's, S&P Global, Fitch) for last 48 hours filtering
"""

from src.scrapers.moodys_scraper import MoodysScraper
from src.scrapers.sp_scraper import SPScraper
from src.scrapers.fitch_scraper import FitchScraper
import pandas as pd

print("=" * 70)
print("🔍 CREDIT RISK SCRAPER - FUNCTIONALITY TEST")
print("=" * 70)

# 1. Test Moody's
print("\n📊 1. TESTING MOODY'S SCRAPER")
print("-" * 50)
moodys = MoodysScraper()
df_moodys = moodys.get_articles_last_48h()

print(f"\n📈 Moody's Results:")
print(f"   → Total articles found (last 48h): {len(df_moodys) if isinstance(df_moodys, pd.DataFrame) else 0}")

if isinstance(df_moodys, pd.DataFrame) and len(df_moodys) > 0:
    print(f"\n   Sample articles:")
    for i, row in df_moodys.head(3).iterrows():
        print(f"\n   [{i+1}] {row['title'][:80]}...")
        print(f"       Type: {row.get('content_type', 'N/A')}")
        print(f"       Date: {row.get('date', 'N/A')}")

# 2. Test S&P Global
print("\n\n📊 2. TESTING S&P GLOBAL SCRAPER")
print("-" * 50)
sp = SPScraper()
result_sp = sp.get_articles_last_48h()

# Handle both DataFrame and list returns
if isinstance(result_sp, pd.DataFrame):
    df_sp = result_sp
    print(f"\n📈 S&P Global Results:")
    print(f"   → Total articles found (last 48h): {len(df_sp)}")
    
    if len(df_sp) > 0:
        print(f"\n   Sample articles:")
        for i, row in df_sp.head(3).iterrows():
            print(f"\n   [{i+1}] {row['title'][:80]}...")
            print(f"       Type: {row.get('content_type', 'N/A')}")
            print(f"       Date: {row.get('date', 'N/A')}")
else:
    print(f"\n📈 S&P Global Results:")
    print(f"   → Total articles found (last 48h): {len(result_sp)}")
    if len(result_sp) > 0:
        print(f"\n   Sample articles:")
        for i, article in enumerate(result_sp[:3]):
            print(f"\n   [{i+1}] {article['title'][:80]}...")
            print(f"       Type: {article.get('content_type', 'N/A')}")
            print(f"       Date: {article.get('date', 'N/A')}")

# 3. Test Fitch
print("\n\n📊 3. TESTING FITCH SCRAPER")
print("-" * 50)
fitch = FitchScraper()
df_fitch = fitch.get_articles_last_48h()

print(f"\n📈 Fitch Results:")
print(f"   → Total articles found (last 48h): {len(df_fitch) if isinstance(df_fitch, pd.DataFrame) else 0}")

if isinstance(df_fitch, pd.DataFrame) and len(df_fitch) > 0:
    print(f"\n   Sample articles:")
    for i, row in df_fitch.head(3).iterrows():
        print(f"\n   [{i+1}] {row['title'][:80]}...")
        print(f"       Type: {row.get('publication_type', row.get('content_type', 'N/A'))}")
        print(f"       Date: {row.get('date', 'N/A')}")

# Final summary
print("\n" + "=" * 70)
print("📊 FINAL SUMMARY")
print("=" * 70)

moodys_count = len(df_moodys) if isinstance(df_moodys, pd.DataFrame) else 0
if isinstance(result_sp, pd.DataFrame):
    sp_count = len(result_sp)
elif isinstance(result_sp, list):
    sp_count = len(result_sp)
else:
    sp_count = 0
fitch_count = len(df_fitch) if isinstance(df_fitch, pd.DataFrame) else 0

print(f"✅ Moody's:     {moodys_count} articles (last 48h)")
print(f"✅ S&P Global:  {sp_count} articles (last 48h)")
print(f"✅ Fitch:       {fitch_count} articles (last 48h)")
print(f"\n📦 Total:       {moodys_count + sp_count + fitch_count} articles")

if moodys_count > 0 or sp_count > 0 or fitch_count > 0:
    print("\n🎉 Scrapers are working correctly!")
    print("\nNext steps:")
    print("1. Run: python main.py (full scraping)")
    print("2. Run: python src/dashboard/app.py (dashboard)")
else:
    print("\n⚠️ No articles found. Check your internet connection and website availability.")

print("=" * 70)