"""
Quantitative Risk-Return Analysis Module

This module provides financial analysis metrics for technical indicator evaluation
using industry-standard formulas (PyNance framework).

Key Metrics Calculated:
- Sharpe Ratio: Risk-adjusted returns (return per unit of risk)
- Sortino Ratio: Downside risk-adjusted returns
- Calmar Ratio: Return per unit of max drawdown
- Maximum Drawdown: Largest peak-to-trough decline
- Win Rate: Percentage of profitable trading days
- Profit Factor: Ratio of gains to losses
- Information Ratio: Excess return vs. tracking error
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List


class RiskReturnAnalyzer:
    """Calculate comprehensive risk-return metrics for stock price series."""
    
    ANNUAL_TRADING_DAYS = 252  # Standard trading days per year
    RISK_FREE_RATE = 0.02  # 2% annual risk-free rate
    
    def __init__(self, price_series: np.ndarray, name: str = "Stock"):
        """
        Initialize analyzer with price series.
        
        Args:
            price_series: Array of closing prices
            name: Stock ticker or identifier
        """
        self.price_series = np.array(price_series)
        self.name = name
        self.returns = self._calculate_returns()
        
    def _calculate_returns(self) -> np.ndarray:
        """Calculate daily returns from price series."""
        clean_prices = self.price_series[~np.isnan(self.price_series)]
        if len(clean_prices) < 2:
            raise ValueError(f"Insufficient price data for {self.name}")
        return np.diff(clean_prices) / clean_prices[:-1]
    
    def sharpe_ratio(self) -> float:
        """
        Calculate Sharpe Ratio.
        
        Measures risk-adjusted return. Higher values indicate better risk-adjusted performance.
        
        Formula: (Mean Return - Risk-Free Rate) / Std Dev of Returns
        
        Returns:
            Annualized Sharpe Ratio
        """
        daily_risk_free = (1 + self.RISK_FREE_RATE) ** (1 / self.ANNUAL_TRADING_DAYS) - 1
        excess_returns = self.returns - daily_risk_free
        
        if np.std(excess_returns) == 0:
            return np.nan
            
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(self.ANNUAL_TRADING_DAYS)
    
    def sortino_ratio(self) -> float:
        """
        Calculate Sortino Ratio.
        
        Like Sharpe but only penalizes downside volatility.
        More useful for strategies that limit losses.
        
        Returns:
            Annualized Sortino Ratio
        """
        daily_risk_free = (1 + self.RISK_FREE_RATE) ** (1 / self.ANNUAL_TRADING_DAYS) - 1
        downside_returns = self.returns[self.returns < daily_risk_free]
        
        if len(downside_returns) == 0:
            return np.nan
            
        downside_deviation = np.std(downside_returns) * np.sqrt(self.ANNUAL_TRADING_DAYS)
        
        if downside_deviation == 0:
            return np.nan
            
        return (np.mean(self.returns) - daily_risk_free) / downside_deviation * np.sqrt(self.ANNUAL_TRADING_DAYS)
    
    def max_drawdown(self) -> float:
        """
        Calculate Maximum Drawdown.
        
        Largest peak-to-trough decline as percentage.
        Indicates worst-case loss scenario.
        
        Returns:
            Maximum drawdown as percentage (negative value)
        """
        cumulative = np.cumprod(1 + self.returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        
        return np.min(drawdown) * 100
    
    def calmar_ratio(self) -> float:
        """
        Calculate Calmar Ratio.
        
        Return per unit of maximum drawdown.
        Useful for comparing strategies with different risk profiles.
        
        Formula: Annualized Return / Absolute Max Drawdown
        
        Returns:
            Calmar Ratio
        """
        annualized_return = (1 + np.mean(self.returns)) ** self.ANNUAL_TRADING_DAYS - 1
        max_dd = self.max_drawdown()
        
        if max_dd == 0:
            return np.nan
            
        return annualized_return / abs(max_dd)
    
    def win_rate(self) -> float:
        """
        Calculate Win Rate.
        
        Percentage of days with positive returns.
        
        Returns:
            Win rate as percentage (0-100)
        """
        return (self.returns > 0).sum() / len(self.returns) * 100
    
    def profit_factor(self) -> float:
        """
        Calculate Profit Factor.
        
        Ratio of sum of gains to sum of losses.
        PF > 1.0 means more gains than losses.
        
        Returns:
            Profit factor ratio
        """
        gains = self.returns[self.returns > 0].sum()
        losses = abs(self.returns[self.returns < 0].sum())
        
        if losses == 0:
            return np.nan
            
        return gains / losses
    
    def information_ratio(self, benchmark_return: float = 0.001) -> float:
        """
        Calculate Information Ratio.
        
        Excess return vs tracking error against benchmark.
        
        Returns:
            Information ratio (annualized)
        """
        tracking_error = np.std(self.returns - benchmark_return) * np.sqrt(self.ANNUAL_TRADING_DAYS)
        
        if tracking_error == 0:
            return np.nan
            
        excess_return = np.mean(self.returns) - benchmark_return
        return excess_return / tracking_error * np.sqrt(self.ANNUAL_TRADING_DAYS)
    
    def get_all_metrics(self) -> Dict[str, float]:
        """
        Calculate all metrics at once.
        
        Returns:
            Dictionary with all risk-return metrics
        """
        annualized_return = (1 + np.mean(self.returns)) ** self.ANNUAL_TRADING_DAYS - 1
        volatility = np.std(self.returns) * np.sqrt(self.ANNUAL_TRADING_DAYS)
        total_return = (self.price_series[-1] - self.price_series[0]) / self.price_series[0]
        
        return {
            'total_return_pct': total_return * 100,
            'annualized_return_pct': annualized_return * 100,
            'volatility_pct': volatility * 100,
            'sharpe_ratio': self.sharpe_ratio(),
            'sortino_ratio': self.sortino_ratio(),
            'max_drawdown_pct': self.max_drawdown(),
            'calmar_ratio': self.calmar_ratio(),
            'win_rate_pct': self.win_rate(),
            'profit_factor': self.profit_factor(),
            'information_ratio': self.information_ratio(),
        }


class IndicatorCorrelationAnalyzer:
    """Analyze correlation between technical indicators and returns."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with OHLCV + indicator dataframe.
        
        Args:
            df: DataFrame with Close, Daily_Return, and indicator columns
        """
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare and clean data for analysis."""
        # Ensure Daily_Return exists
        if 'Daily_Return' not in self.df.columns:
            if 'Close' in self.df.columns:
                self.df['Daily_Return'] = self.df['Close'].pct_change() * 100
            else:
                raise ValueError("Close or Daily_Return column required")
    
    def correlate_indicators(self, indicator_cols: List[str]) -> Dict[str, float]:
        """
        Calculate correlation between indicators and daily returns.
        
        Args:
            indicator_cols: List of indicator column names
            
        Returns:
            Dictionary mapping indicator name to correlation coefficient
        """
        correlations = {}
        
        for col in indicator_cols:
            if col in self.df.columns:
                valid_data = self.df[[col, 'Daily_Return']].dropna()
                
                if len(valid_data) > 2:
                    corr = valid_data[col].corr(valid_data['Daily_Return'])
                    correlations[col] = corr
        
        return correlations
    
    def rank_indicators(self, indicator_cols: List[str]) -> List[Tuple[str, float]]:
        """
        Rank indicators by correlation strength.
        
        Args:
            indicator_cols: List of indicator column names
            
        Returns:
            List of (indicator, correlation) sorted by absolute correlation
        """
        correlations = self.correlate_indicators(indicator_cols)
        return sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)


def classify_risk_level(sharpe_ratio: float) -> str:
    """
    Classify investment based on Sharpe Ratio.
    
    Args:
        sharpe_ratio: Calculated Sharpe Ratio
        
    Returns:
        Risk classification string with emoji
    """
    if sharpe_ratio > 2.0:
        return "⭐⭐⭐ EXCELLENT - Very high risk-adjusted returns"
    elif sharpe_ratio > 1.5:
        return "⭐⭐ GOOD - High risk-adjusted returns"
    elif sharpe_ratio > 1.0:
        return "⭐ ACCEPTABLE - Moderate risk-adjusted returns"
    elif sharpe_ratio > 0:
        return "⚠️ WEAK - Low risk-adjusted returns"
    else:
        return "❌ NEGATIVE - Negative risk-adjusted returns"
