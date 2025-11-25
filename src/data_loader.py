"""
Data loader module for financial news and stock data.

This module handles loading and initial validation of the FNSPID dataset
and stock price data from various sources.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import yfinance as yf
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load financial news and stock price data."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize DataLoader.

        Parameters
        ----------
        data_dir : str, optional
            Base directory for data files
        """
        self.data_dir = Path(data_dir) if data_dir else Path("data")
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"

    def load_news_data(self, filepath: str) -> pd.DataFrame:
        """
        Load financial news data.

        Parameters
        ----------
        filepath : str
            Path to news CSV file

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: headline, url, publisher, date, stock
        """
        logger.info(f"Loading news data from {filepath}")

        df = pd.read_csv(filepath)

        # Validate required columns
        required_cols = ["headline", "url", "publisher", "date", "stock"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Convert date to datetime
        df["date"] = pd.to_datetime(df["date"], utc=True)

        logger.info(f"Loaded {len(df)} news articles")
        return df

    def load_stock_data(
        self, ticker: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        Load stock price data using yfinance.

        Parameters
        ----------
        ticker : str
            Stock ticker symbol (e.g., 'AAPL')
        start_date : str
            Start date in format 'YYYY-MM-DD'
        end_date : str
            End date in format 'YYYY-MM-DD'

        Returns
        -------
        pd.DataFrame
            DataFrame with OHLCV data
        """
        logger.info(f"Loading stock data for {ticker} from {start_date} to {end_date}")

        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            logger.info(f"Loaded {len(df)} trading days for {ticker}")
            return df
        except Exception as e:
            logger.error(f"Error loading data for {ticker}: {str(e)}")
            raise

    def load_multiple_stocks(
        self, tickers: list, start_date: str, end_date: str
    ) -> dict:
        """
        Load stock price data for multiple tickers.

        Parameters
        ----------
        tickers : list
            List of stock ticker symbols
        start_date : str
            Start date in format 'YYYY-MM-DD'
        end_date : str
            End date in format 'YYYY-MM-DD'

        Returns
        -------
        dict
            Dictionary with ticker as key and DataFrame as value
        """
        stock_data = {}
        for ticker in tickers:
            try:
                stock_data[ticker] = self.load_stock_data(ticker, start_date, end_date)
            except Exception as e:
                logger.warning(f"Failed to load {ticker}: {str(e)}")
                continue

        return stock_data

    def get_date_range_from_news(self, news_df: pd.DataFrame) -> Tuple[str, str]:
        """
        Extract date range from news dataset.

        Parameters
        ----------
        news_df : pd.DataFrame
            News dataframe with 'date' column

        Returns
        -------
        Tuple[str, str]
            (start_date, end_date) in format 'YYYY-MM-DD'
        """
        min_date = news_df["date"].min()
        max_date = news_df["date"].max()

        return min_date.strftime("%Y-%m-%d"), max_date.strftime("%Y-%m-%d")

    def save_data(self, df: pd.DataFrame, filepath: str) -> None:
        """
        Save DataFrame to CSV.

        Parameters
        ----------
        df : pd.DataFrame
            Data to save
        filepath : str
            Output filepath
        """
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=True)
        logger.info(f"Saved data to {filepath}")
