"""
Moody's Investor Services Web Scraper 
Extracts credit risk news and insights from Moody's dedicated credit risk page.
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from loguru import logger
from config import HEADERS, REQUEST_TIMEOUT, CREDIT_RISK_KEYWORDS

class MoodysScraper:
    """Scraper for Moody's credit risk insights page."""
    
    def __init__(self):
        self.insights_url = "https://www.moodys.com/web/en/us/insights/credit-risk.html"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def scrape_news(self, max_articles: int = 30) -> pd.DataFrame:
        """
        Scrape news and insights from Moody's Credit Risk page.
        
        Args:
            max_articles: Maximum number of articles to scrape.
            
        Returns:
            DataFrame containing scraped articles.
        """
        news_data = []
        
        try:
            logger.info(f"Scraping Moody's insights from {self.insights_url}")
            response = self.session.get(self.insights_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Method 1: Look for all article-like structures
            # Find all research headlines (they are in <h3>, <h4>, <h5> tags)
            headlines = soup.find_all(['h3', 'h4', 'h5'])
            
            for headline in headlines:
                # Get the text of the headline
                title = headline.get_text(strip=True)
                
                # Filter out section headers and short titles
                if not title or len(title) < 15:
                    continue
                
                # Skip navigation/section titles
                skip_words = ['featured topics', 'credit market topics', 'discover more', 
                             'private credit', 'digital economy', 'commercial real estate',
                             'data centers', 'emerging markets', 'sustainable finance',
                             'leveraged finance', 'macro views', 'outlooks']
                
                if any(skip_word in title.lower() for skip_word in skip_words):
                    continue
                
                # Find the link associated with this headline
                link = headline.find('a')
                url = ""
                if link and link.get('href'):
                    url = link.get('href')
                    if url.startswith('/'):
                        url = "https://www.moodys.com" + url
                else:
                    # Check if the headline is inside a link
                    parent_link = headline.find_parent('a')
                    if parent_link and parent_link.get('href'):
                        url = parent_link.get('href')
                        if url.startswith('/'):
                            url = "https://www.moodys.com" + url
                
                # Find the article type/category
                content_type = "Research"
                type_elem = headline.find_previous(['span', 'div'], class_=re.compile(r'type|category|tag|label', re.I))
                if type_elem:
                    type_text = type_elem.get_text(strip=True).lower()
                    if 'data story' in type_text:
                        content_type = "Data Story"
                    elif 'article' in type_text:
                        content_type = "Article"
                    elif 'research' in type_text:
                        content_type = "Research"
                
                # Find date (try to find nearby date element)
                date = datetime.now().strftime("%Y-%m-%d")
                # Look for date in parent elements
                parent = headline.find_parent(['div', 'section', 'article'])
                if parent:
                    date_elem = parent.find(['time', 'span', 'div'], class_=re.compile(r'date|time|published', re.I))
                    if date_elem:
                        date_text = date_elem.get_text(strip=True)
                        # Try to parse common date formats
                        date_match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', date_text)
                        if date_match:
                            date = date_match.group(0)
                
                # Check relevance
                if self._is_relevant_article(title):
                    news_data.append({
                        'source': 'Moody\'s',
                        'title': title,
                        'content_type': content_type,
                        'url': url,
                        'date': date,
                        'scraped_at': datetime.now().isoformat()
                    })
                    
                    logger.debug(f"Found article: {title[:50]}...")
                    
                if len(news_data) >= max_articles:
                    break
            
            # Method 2: Also look in the "Discover more" section specifically
            discover_section = soup.find('section', class_=re.compile(r'discover|more', re.I))
            if discover_section:
                discover_items = discover_section.find_all(['div', 'article'], class_=re.compile(r'card|item', re.I))
                for item in discover_items:
                    title_elem = item.find(['h3', 'h4', 'h5', 'h6'])
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = item.find('a')
                        url = link.get('href') if link else ""
                        if url and url.startswith('/'):
                            url = "https://www.moodys.com" + url
                        
                        if title and len(title) > 15 and self._is_relevant_article(title):
                            # Avoid duplicates
                            if not any(existing['title'] == title for existing in news_data):
                                news_data.append({
                                    'source': 'Moody\'s',
                                    'title': title,
                                    'content_type': "Research",
                                    'url': url,
                                    'date': datetime.now().strftime("%Y-%m-%d"),
                                    'scraped_at': datetime.now().isoformat()
                                })
            
            logger.info(f"Extracted {len(news_data)} relevant articles from Moody's")
            
        except requests.RequestException as e:
            logger.error(f"Error scraping Moody's: {e}")
            
        return pd.DataFrame(news_data)
    
    def _is_relevant_article(self, title: str) -> bool:
        """
        Check if article is relevant to credit risk.
        
        Args:
            title: Article title to check
            
        Returns:
            Boolean indicating relevance
        """
        title_lower = title.lower()
        
        # Moody's page is focused on credit risk, but we still filter
        credit_terms = [
            'credit', 'default', 'downgrade', 'upgrade', 'rating', 'outlook',
            'risk', 'debt', 'bond', 'spread', 'liquidity', 'volatility',
            'transparency', 'capital', 'investment', 'economy', 'market',
            'real estate', 'data center', 'sustainable', 'leveraged',
            'corporate', 'sovereign', 'emerging', 'commercial'
        ]
        
        # Must contain at least one credit-related term
        has_credit_term = any(term in title_lower for term in credit_terms)
        
        # Exclude very generic or navigation items
        exclude_terms = ['menu', 'cookie', 'consent', 'subscribe', 'newsletter']
        is_excluded = any(term in title_lower for term in exclude_terms)
        
        return has_credit_term and not is_excluded and len(title) > 10

    def get_rating_actions(self) -> pd.DataFrame:
        """Get recent rating actions (placeholder for future implementation)."""
        logger.warning("Rating actions API not yet implemented for Moody's")
        return pd.DataFrame()
    
    def get_credit_ratings_summary(self) -> pd.DataFrame:
        """Get credit ratings summary (placeholder for future implementation)."""
        logger.warning("Credit ratings summary API not yet implemented for Moody's")
        return pd.DataFrame()