"""
S&P Global Ratings Web Scraper - Improved version based on actual page structure
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from loguru import logger
from config import HEADERS, REQUEST_TIMEOUT

class SPScraper:
    def __init__(self):
        self.research_url = "https://www.spglobal.com/ratings/en/research#q=&rows=20&pagenum=1&sort=es_unified_dt%20desc"
        self.base_url = "https://www.spglobal.com"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def scrape_insights(self, max_insights: int = 30) -> pd.DataFrame:
        """Scrape research insights from S&P Global."""
        insights_data = []
        
        try:
            logger.info(f"Scraping S&P Global research")
            response = self.session.get(self.research_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for article titles in the search results
            # Based on the HTML structure shown, articles have dates and titles
            
            # Find all elements that look like article titles
            # Common patterns on S&P's page
            title_candidates = soup.find_all(['h2', 'h3', 'a'], class_=re.compile(r'title|headline|result', re.I))
            
            for elem in title_candidates:
                title = elem.get_text(strip=True)
                
                # Filter for meaningful article titles
                if not title or len(title) < 20 or len(title) > 200:
                    continue
                
                # Skip generic text
                if any(skip in title.lower() for skip in ['sort by', 'filter', 'loading', 'cookie']):
                    continue
                
                # Get URL
                url = ""
                if elem.name == 'a' and elem.get('href'):
                    url = elem.get('href')
                elif elem.find('a'):
                    url = elem.find('a').get('href', '')
                
                if url and not url.startswith('http'):
                    url = self.base_url + url
                
                # Get date - look for date near this element
                date = datetime.now().strftime("%Y-%m-%d")
                parent = elem.find_parent(['div', 'li', 'article'])
                if parent:
                    date_match = parent.find(string=re.compile(r'\w{3}\s\d{1,2},\s\d{4}'))
                    if date_match:
                        date = date_match.strip()
                
                # Filter for credit-relevant content
                if self._is_relevant(title):
                    insights_data.append({
                        'source': 'S&P Global',
                        'title': title,
                        'content_type': 'Research Article',
                        'url': url,
                        'date': date,
                        'scraped_at': datetime.now().isoformat()
                    })
                    
                    if len(insights_data) >= max_insights:
                        break
            
            logger.info(f"Extracted {len(insights_data)} insights from S&P Global")
            
        except Exception as e:
            logger.error(f"Error scraping S&P: {e}")
            
        return pd.DataFrame(insights_data)
    
    def _is_relevant(self, title: str) -> bool:
        """Check if article is relevant to credit risk."""
        relevant_terms = [
            'credit', 'rating', 'default', 'debt', 'bond', 'risk',
            'economic', 'financial', 'sovereign', 'corporate',
            'structured', 'finance', 'outlook', 'downgrade', 'upgrade'
        ]
        return any(term in title.lower() for term in relevant_terms)
    
    def get_credit_ratings(self) -> pd.DataFrame:
        """Placeholder for credit ratings."""
        return pd.DataFrame()