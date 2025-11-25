"""
Correlation analysis module for analyzing sentiment-price relationships.

Calculates correlations between sentiment indicators and stock returns.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class CorrelationAnalyzer:
    """Analyze correlations between sentiment and stock movements."""

    def __init__(self):
        """Initialize correlation analyzer."""
        pass

    def pearson_correlation(
        self, x: pd.Series, y: pd.Series
    ) -> Tuple[float, float]:
        """
        Calculate Pearson correlation coefficient and p-value.

        Parameters
        ----------
        x : pd.Series
            First variable
        y : pd.Series
            Second variable

        Returns
        -------
        Tuple[float, float]
            (correlation coefficient, p-value)
        """
        # Remove NaN values
        mask = ~(x.isna() | y.isna())
        x_clean = x[mask]
        y_clean = y[mask]

        if len(x_clean) < 2:
            return np.nan, np.nan

        corr, pvalue = stats.pearsonr(x_clean, y_clean)
        return corr, pvalue

    def spearman_correlation(
        self, x: pd.Series, y: pd.Series
    ) -> Tuple[float, float]:
        """
        Calculate Spearman correlation coefficient and p-value.

        Parameters
        ----------
        x : pd.Series
            First variable
        y : pd.Series
            Second variable

        Returns
        -------
        Tuple[float, float]
            (correlation coefficient, p-value)
        """
        mask = ~(x.isna() | y.isna())
        x_clean = x[mask]
        y_clean = y[mask]

        if len(x_clean) < 2:
            return np.nan, np.nan

        corr, pvalue = stats.spearmanr(x_clean, y_clean)
        return corr, pvalue

    def analyze_sentiment_return_correlation(
        self, daily_sentiment: pd.DataFrame, daily_returns: pd.DataFrame
    ) -> Dict:
        """
        Analyze correlation between daily sentiment and returns.

        Parameters
        ----------
        daily_sentiment : pd.DataFrame
            Daily aggregated sentiment data
        daily_returns : pd.DataFrame
            Daily stock returns data

        Returns
        -------
        Dict
            Correlation analysis results
        """
        logger.info("Analyzing sentiment-return correlation")

        # Ensure both dataframes have matching dates
        merged = pd.merge(
            daily_sentiment, daily_returns, left_on="date", right_index=True, how="inner"
        )

        if len(merged) < 2:
            logger.warning("Insufficient data for correlation analysis")
            return {}

        results = {
            "correlation_metrics": {},
            "analysis_period": {
                "start_date": merged["date"].min(),
                "end_date": merged["date"].max(),
                "data_points": len(merged),
            },
        }

        # Pearson correlation
        pearson_corr, pearson_pval = self.pearson_correlation(
            merged["avg_polarity"], merged["daily_return"]
        )
        results["correlation_metrics"]["pearson"] = {
            "coefficient": pearson_corr,
            "p_value": pearson_pval,
            "significant": pearson_pval < 0.05 if not np.isnan(pearson_pval) else False,
        }

        # Spearman correlation
        spearman_corr, spearman_pval = self.spearman_correlation(
            merged["avg_polarity"], merged["daily_return"]
        )
        results["correlation_metrics"]["spearman"] = {
            "coefficient": spearman_corr,
            "p_value": spearman_pval,
            "significant": spearman_pval < 0.05 if not np.isnan(spearman_pval) else False,
        }

        return results, merged

    def lagged_correlation(
        self, sentiment: pd.Series, returns: pd.Series, max_lag: int = 5
    ) -> Dict:
        """
        Calculate lagged correlations between sentiment and returns.

        Parameters
        ----------
        sentiment : pd.Series
            Sentiment scores (indexed by date)
        returns : pd.Series
            Stock returns (indexed by date)
        max_lag : int
            Maximum lag to test

        Returns
        -------
        Dict
            Lagged correlation results
        """
        logger.info(f"Calculating lagged correlations (max lag: {max_lag} days)")

        results = {}

        for lag in range(0, max_lag + 1):
            # Shift sentiment forward to check if past sentiment predicts future returns
            shifted_sentiment = sentiment.shift(lag)

            corr, pval = self.pearson_correlation(shifted_sentiment, returns)

            results[f"lag_{lag}"] = {
                "correlation": corr,
                "p_value": pval,
                "significant": pval < 0.05 if not np.isnan(pval) else False,
            }

        return results

    def correlation_by_sentiment_category(
        self, df: pd.DataFrame
    ) -> Dict:
        """
        Analyze returns separately for positive vs negative sentiment days.

        Parameters
        ----------
        df : pd.DataFrame
            Combined sentiment and returns data

        Returns
        -------
        Dict
            Returns statistics by sentiment category
        """
        logger.info("Analyzing returns by sentiment category")

        results = {}

        for sentiment in ["positive", "negative", "neutral"]:
            subset = df[df["sentiment_label"] == sentiment]

            if len(subset) == 0:
                continue

            results[sentiment] = {
                "avg_return": subset["daily_return"].mean(),
                "median_return": subset["daily_return"].median(),
                "std_return": subset["daily_return"].std(),
                "days_count": len(subset),
                "positive_return_days": (subset["daily_return"] > 0).sum(),
            }

            if len(subset) > 0:
                results[sentiment]["positive_return_pct"] = (
                    results[sentiment]["positive_return_days"] / len(subset) * 100
                )

        return results

    def create_correlation_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create correlation matrix for multiple variables.

        Parameters
        ----------
        df : pd.DataFrame
            Data with sentiment and price indicators

        Returns
        -------
        pd.DataFrame
            Correlation matrix
        """
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        correlation_matrix = df[numeric_cols].corr()

        return correlation_matrix

    def get_strongest_correlations(
        self, correlation_matrix: pd.DataFrame, threshold: float = 0.3
    ) -> list:
        """
        Get strongest correlations from correlation matrix.

        Parameters
        ----------
        correlation_matrix : pd.DataFrame
            Correlation matrix
        threshold : float
            Minimum absolute correlation value

        Returns
        -------
        list
            List of (var1, var2, correlation) tuples
        """
        correlations = []

        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]

                if abs(corr_value) >= threshold:
                    correlations.append(
                        (
                            correlation_matrix.columns[i],
                            correlation_matrix.columns[j],
                            corr_value,
                        )
                    )

        # Sort by absolute correlation value
        correlations.sort(key=lambda x: abs(x[2]), reverse=True)

        return correlations
