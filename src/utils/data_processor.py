"""
Data Processing Utilities
Handles cleaning, transformation, aggregation, and storage of scraped data
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import Counter
from loguru import logger
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR


class DataProcessor:
    """Process and manage scraped credit risk data"""
    
    def __init__(self, raw_path: Path = RAW_DATA_DIR, processed_path: Path = PROCESSED_DATA_DIR):
        """
        Initialize DataProcessor with paths
        
        Args:
            raw_path: Path for raw data storage
            processed_path: Path for processed data storage
        """
        self.raw_path = Path(raw_path)
        self.processed_path = Path(processed_path)
        
        # Ensure directories exist
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        self.required_columns = ['source', 'title', 'date', 'url']
        
    def save_raw_data(self, df: pd.DataFrame, source: str) -> Path:
        """
        Save raw scraped data to CSV
        
        Args:
            df: DataFrame with raw data
            source: Source identifier (moodys, fitch, sp)
            
        Returns:
            Path to saved file
        """
        if df.empty:
            logger.warning(f"No data to save for {source}")
            return None
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{source}_raw_{timestamp}.csv"
        filepath = self.raw_path / filename
        
        df.to_csv(filepath, index=False)
        logger.info(f"Saved raw data for {source}: {filepath}")
        
        return filepath
    
    def process_news_data(self, dfs_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Process and combine news data from multiple sources
        
        Args:
            dfs_dict: Dictionary mapping source names to DataFrames
            
        Returns:
            Processed and combined DataFrame
        """
        if not dfs_dict:
            logger.warning("No data to process")
            return pd.DataFrame()
        
        # Combine all DataFrames
        combined_df = pd.concat(dfs_dict.values(), ignore_index=True)
        
        logger.info(f"Processing {len(combined_df)} total articles")
        
        # Clean and standardize data
        combined_df = self._clean_data(combined_df)
        
        # Add derived columns
        combined_df = self._add_derived_columns(combined_df)
        
        # Extract keywords from titles
        combined_df['extracted_keywords'] = combined_df['title'].apply(self._extract_keywords)
        
        # Save processed data
        output_file = self.processed_path / f"processed_news_{datetime.now().strftime('%Y%m%d')}.csv"
        combined_df.to_csv(output_file, index=False)
        logger.info(f"Saved processed data: {output_file}")
        
        # Generate and save summary statistics
        stats = self.generate_summary_stats(combined_df)
        self._save_stats(stats)
        
        return combined_df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize DataFrame
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Remove duplicates based on title and source
        df = df.drop_duplicates(subset=['title', 'source'], keep='first')
        
        # Handle missing values
        df['title'] = df['title'].fillna('No Title')
        df['url'] = df['url'].fillna('')
        df['summary'] = df.get('summary', '').fillna('')
        
        # Standardize date column
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['date'] = df['date'].fillna(datetime.now())
        else:
            df['date'] = datetime.now()
        
        # Remove rows with invalid data
        df = df[df['title'].str.len() > 5]  # Remove very short titles
        
        return df
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add derived columns for analysis
        
        Args:
            df: Cleaned DataFrame
            
        Returns:
            DataFrame with additional columns
        """
        # Time-based columns
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['week'] = df['date'].dt.isocalendar().week
        df['day_of_week'] = df['date'].dt.day_name()
        
        # Title features
        df['title_length'] = df['title'].str.len()
        df['word_count'] = df['title'].str.split().str.len()
        
        # Sentiment indicators (simplified)
        positive_words = ['upgrade', 'positive', 'improvement', 'stable', 'strong']
        negative_words = ['downgrade', 'negative', 'deterioration', 'default', 'risk']
        
        df['positive_indicators'] = df['title'].str.lower().apply(
            lambda x: sum(1 for word in positive_words if word in x)
        )
        df['negative_indicators'] = df['title'].str.lower().apply(
            lambda x: sum(1 for word in negative_words if word in x)
        )
        
        return df
    
    def _extract_keywords(self, title: str) -> str:
        """
        Extract relevant keywords from title
        
        Args:
            title: Article title
            
        Returns:
            Comma-separated keywords
        """
        credit_terms = [
            'default', 'downgrade', 'upgrade', 'outlook', 'rating',
            'credit', 'risk', 'sovereign', 'corporate', 'debt',
            'bond', 'spread', 'cds', 'loan', 'capital', 'liquidity',
            'stress', 'crisis', 'recovery', 'bankruptcy', 'insolvency'
        ]
        
        title_lower = title.lower()
        found_keywords = [term for term in credit_terms if term in title_lower]
        
        return ', '.join(found_keywords) if found_keywords else 'general'