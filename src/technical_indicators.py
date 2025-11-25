"""
Technical indicators module for financial analysis.

Calculates moving averages, RSI, MACD, and other indicators using TA-Lib.
"""

import pandas as pd
import numpy as np
import talib
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """Calculate technical indicators for stock analysis."""

    def __init__(self):
        """Initialize technical indicators calculator."""
        pass

    def simple_moving_average(
        self, df: pd.DataFrame, period: int = 20, column: str = "Close"
    ) -> pd.Series:
        """
        Calculate Simple Moving Average (SMA).

        Parameters
        ----------
        df : pd.DataFrame
            Price data
        period : int
            SMA period
        column : str
            Column to calculate SMA for

        Returns
        -------
        pd.Series
            SMA values
        """
        return talib.SMA(df[column], timeperiod=period)

    def exponential_moving_average(
        self, df: pd.DataFrame, period: int = 12, column: str = "Close"
    ) -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA).

        Parameters
        ----------
        df : pd.DataFrame
            Price data
        period : int
            EMA period
        column : str
            Column to calculate EMA for

        Returns
        -------
        pd.Series
            EMA values
        """
        return talib.EMA(df[column], timeperiod=period)

    def relative_strength_index(
        self, df: pd.DataFrame, period: int = 14, column: str = "Close"
    ) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).

        Parameters
        ----------
        df : pd.DataFrame
            Price data
        period : int
            RSI period
        column : str
            Column to calculate RSI for

        Returns
        -------
        pd.Series
            RSI values (0-100)
        """
        return talib.RSI(df[column], timeperiod=period)

    def macd(
        self,
        df: pd.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
        column: str = "Close",
    ) -> tuple:
        """
        Calculate MACD (Moving Average Convergence Divergence).

        Parameters
        ----------
        df : pd.DataFrame
            Price data
        fast_period : int
            Fast EMA period
        slow_period : int
            Slow EMA period
        signal_period : int
            Signal line EMA period
        column : str
            Column to calculate MACD for

        Returns
        -------
        tuple
            (MACD line, Signal line, Histogram)
        """
        macd_line, signal_line, histogram = talib.MACD(
            df[column],
            fastperiod=fast_period,
            slowperiod=slow_period,
            signalperiod=signal_period,
        )
        return macd_line, signal_line, histogram

    def bollinger_bands(
        self,
        df: pd.DataFrame,
        period: int = 20,
        std_dev: int = 2,
        column: str = "Close",
    ) -> tuple:
        """
        Calculate Bollinger Bands.

        Parameters
        ----------
        df : pd.DataFrame
            Price data
        period : int
            Moving average period
        std_dev : int
            Number of standard deviations
        column : str
            Column to calculate bands for

        Returns
        -------
        tuple
            (Upper band, Middle band, Lower band)
        """
        upper, middle, lower = talib.BBANDS(
            df[column], timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev
        )
        return upper, middle, lower

    def add_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add all technical indicators to dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            Stock data with OHLCV columns

        Returns
        -------
        pd.DataFrame
            Data with technical indicators added
        """
        logger.info("Calculating all technical indicators")

        df = df.copy()

        # Moving Averages
        df["SMA_20"] = self.simple_moving_average(df, 20)
        df["SMA_50"] = self.simple_moving_average(df, 50)
        df["EMA_12"] = self.exponential_moving_average(df, 12)
        df["EMA_26"] = self.exponential_moving_average(df, 26)

        # RSI
        df["RSI_14"] = self.relative_strength_index(df, 14)

        # MACD
        macd_line, signal_line, histogram = self.macd(df)
        df["MACD"] = macd_line
        df["MACD_Signal"] = signal_line
        df["MACD_Histogram"] = histogram

        # Bollinger Bands
        upper, middle, lower = self.bollinger_bands(df)
        df["BB_Upper"] = upper
        df["BB_Middle"] = middle
        df["BB_Lower"] = lower

        # Bollinger Band position
        df["BB_Position"] = (df["Close"] - df["BB_Lower"]) / (df["BB_Upper"] - df["BB_Lower"])

        logger.info("Technical indicators calculated")
        return df

    def calculate_volatility(self, df: pd.DataFrame, period: int = 20) -> pd.Series:
        """
        Calculate rolling volatility (standard deviation of returns).

        Parameters
        ----------
        df : pd.DataFrame
            Price data with 'Close' column
        period : int
            Rolling window period

        Returns
        -------
        pd.Series
            Volatility values
        """
        returns = df["Close"].pct_change()
        volatility = returns.rolling(window=period).std()
        return volatility * 100  # As percentage

    def calculate_atr(
        self, df: pd.DataFrame, period: int = 14
    ) -> pd.Series:
        """
        Calculate Average True Range (ATR).

        Parameters
        ----------
        df : pd.DataFrame
            Stock data with High, Low, Close columns
        period : int
            ATR period

        Returns
        -------
        pd.Series
            ATR values
        """
        return talib.ATR(df["High"], df["Low"], df["Close"], timeperiod=period)

    def get_indicator_summary(self, df: pd.DataFrame) -> dict:
        """
        Get summary statistics for technical indicators.

        Parameters
        ----------
        df : pd.DataFrame
            Data with indicators

        Returns
        -------
        dict
            Summary statistics
        """
        summary = {
            "rsi_current": df["RSI_14"].iloc[-1] if "RSI_14" in df.columns else None,
            "rsi_avg": df["RSI_14"].mean() if "RSI_14" in df.columns else None,
            "macd_current": df["MACD"].iloc[-1] if "MACD" in df.columns else None,
            "price_sma_ratio": (
                df["Close"].iloc[-1] / df["SMA_20"].iloc[-1]
                if "SMA_20" in df.columns
                else None
            ),
        }
        return summary
