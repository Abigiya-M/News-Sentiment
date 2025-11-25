"""
Data preprocessing module for cleaning and preparing data.

Handles data validation, missing value treatment, and normalization.
"""

import pandas as pd
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocess financial news and stock data."""

    def __init__(self):
        """Initialize preprocessor."""
        pass

    def clean_news_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean news dataset.

        Parameters
        ----------
        df : pd.DataFrame
            Raw news data

        Returns
        -------
        pd.DataFrame
            Cleaned news data
        """
        logger.info("Cleaning news data")
        df = df.copy()

        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=["headline", "date", "stock"])
        logger.info(f"Removed {initial_count - len(df)} duplicate rows")

        # Handle missing values
        df = df.dropna(subset=["headline", "date", "stock"])

        # Strip whitespace
        for col in df.select_dtypes(include="object"):
            df[col] = df[col].str.strip()

        # Ensure date is datetime
        df["date"] = pd.to_datetime(df["date"], utc=True)

        # Normalize stock ticker to uppercase
        df["stock"] = df["stock"].str.upper()

        logger.info(f"Cleaned data: {len(df)} rows remaining")
        return df

    def clean_stock_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean stock price data.

        Parameters
        ----------
        df : pd.DataFrame
            Raw stock OHLCV data

        Returns
        -------
        pd.DataFrame
            Cleaned stock data
        """
        logger.info("Cleaning stock data")
        df = df.copy()

        # Handle missing values (forward fill then backward fill)
        df = df.fillna(method="ffill").fillna(method="bfill")

        # Remove any remaining NaN
        df = df.dropna()

        # Ensure numeric columns
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        logger.info(f"Cleaned stock data: {len(df)} rows")
        return df

    def align_dates(
        self, news_df: pd.DataFrame, stock_df: pd.DataFrame, forward_days: int = 5
    ) -> pd.DataFrame:
        """
        Align news dates with trading dates.

        For each news article, find the corresponding trading dates
        (same day or next trading day).

        Parameters
        ----------
        news_df : pd.DataFrame
            News data with 'date' column
        stock_df : pd.DataFrame
            Stock data with datetime index
        forward_days : int
            Number of days to look ahead for price impact

        Returns
        -------
        pd.DataFrame
            News data with aligned trading dates
        """
        logger.info("Aligning news dates with trading dates")

        news_aligned = news_df.copy()
        news_aligned["trading_date"] = None
        news_aligned["trading_dates"] = None

        trading_dates = stock_df.index.normalize()

        for idx, row in news_aligned.iterrows():
            news_date = row["date"].normalize()

            # Find closest trading date (same day or next)
            future_dates = trading_dates[trading_dates >= news_date]
            if len(future_dates) > 0:
                trading_date = future_dates[0]
                news_aligned.at[idx, "trading_date"] = trading_date

                # Get forward dates for impact analysis
                forward_mask = (trading_dates > trading_date) & (
                    trading_dates <= trading_date + pd.Timedelta(days=forward_days)
                )
                forward_trading_dates = trading_dates[forward_mask].tolist()
                news_aligned.at[idx, "trading_dates"] = forward_trading_dates

        # Remove rows without valid trading dates
        before = len(news_aligned)
        news_aligned = news_aligned.dropna(subset=["trading_date"])
        logger.info(
            f"Aligned {len(news_aligned)} out of {before} articles with trading dates"
        )

        return news_aligned

    def calculate_daily_returns(self, stock_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate daily percentage returns.

        Parameters
        ----------
        stock_df : pd.DataFrame
            Stock data with 'Close' column

        Returns
        -------
        pd.DataFrame
            Original data with added 'daily_return' column
        """
        logger.info("Calculating daily returns")

        df = stock_df.copy()
        df["daily_return"] = df["Close"].pct_change() * 100  # Percentage

        return df

    def normalize_text(self, text: str) -> str:
        """
        Normalize headline text for analysis.

        Parameters
        ----------
        text : str
            Raw headline text

        Returns
        -------
        str
            Normalized text
        """
        # Convert to lowercase
        text = text.lower()

        # Remove extra whitespace
        text = " ".join(text.split())

        return text

    def extract_headline_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from headlines.

        Parameters
        ----------
        df : pd.DataFrame
            Data with 'headline' column

        Returns
        -------
        pd.DataFrame
            Data with additional feature columns
        """
        logger.info("Extracting headline features")

        df = df.copy()
        df["headline_length"] = df["headline"].str.len()
        df["word_count"] = df["headline"].str.split().str.len()

        return df
