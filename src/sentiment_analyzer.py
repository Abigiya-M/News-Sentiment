"""
Sentiment analysis module for analyzing news headline sentiment.

Uses TextBlob and NLTK for sentiment scoring.
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
import nltk
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except LookupError:
    nltk.download("averaged_perceptron_tagger", quiet=True)


class SentimentAnalyzer:
    """Analyze sentiment of financial news headlines."""

    def __init__(self):
        """Initialize sentiment analyzer."""
        self.sentiment_scores = {}

    def textblob_sentiment(self, text: str) -> Tuple[float, float, str]:
        """
        Calculate sentiment using TextBlob.

        Parameters
        ----------
        text : str
            Text to analyze

        Returns
        -------
        Tuple[float, float, str]
            (polarity, subjectivity, label)
            - polarity: -1 (negative) to 1 (positive)
            - subjectivity: 0 (objective) to 1 (subjective)
            - label: 'positive', 'negative', or 'neutral'
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Categorize sentiment
        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"

        return polarity, subjectivity, label

    def analyze_headlines(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze sentiment for all headlines.

        Parameters
        ----------
        df : pd.DataFrame
            Data with 'headline' column

        Returns
        -------
        pd.DataFrame
            Data with sentiment columns added
        """
        logger.info(f"Analyzing sentiment for {len(df)} headlines")

        df = df.copy()

        # Apply sentiment analysis
        sentiments = df["headline"].apply(self.textblob_sentiment)

        # Unpack results
        df[["polarity", "subjectivity", "sentiment_label"]] = pd.DataFrame(
            sentiments.tolist(), index=df.index
        )

        logger.info("Sentiment analysis complete")
        return df

    def aggregate_daily_sentiment(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate sentiment scores to daily level.

        Parameters
        ----------
        df : pd.DataFrame
            Data with sentiment and 'date' columns

        Returns
        -------
        pd.DataFrame
            Daily aggregated sentiment data
        """
        logger.info("Aggregating sentiment to daily level")

        # Group by date
        daily_sentiment = (
            df.groupby(df["date"].dt.date)
            .agg(
                {
                    "polarity": ["mean", "std", "min", "max", "count"],
                    "subjectivity": "mean",
                    "sentiment_label": lambda x: (x == "positive").sum(),
                }
            )
            .reset_index()
        )

        daily_sentiment.columns = [
            "date",
            "avg_polarity",
            "std_polarity",
            "min_polarity",
            "max_polarity",
            "article_count",
            "avg_subjectivity",
            "positive_count",
        ]

        # Calculate positive percentage
        daily_sentiment["positive_pct"] = (
            daily_sentiment["positive_count"] / daily_sentiment["article_count"] * 100
        )

        return daily_sentiment

    def aggregate_by_stock_date(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate sentiment by stock and date.

        Parameters
        ----------
        df : pd.DataFrame
            Data with sentiment, 'stock', and 'date' columns

        Returns
        -------
        pd.DataFrame
            Stock-date level aggregated sentiment
        """
        logger.info("Aggregating sentiment by stock and date")

        grouped = (
            df.groupby([df["date"].dt.date, "stock"])
            .agg(
                {
                    "polarity": ["mean", "count"],
                    "sentiment_label": lambda x: (x == "positive").sum(),
                }
            )
            .reset_index()
        )

        grouped.columns = ["date", "stock", "avg_polarity", "article_count", "positive_count"]
        grouped["positive_pct"] = grouped["positive_count"] / grouped["article_count"] * 100

        return grouped

    def get_sentiment_stats(self, df: pd.DataFrame) -> Dict:
        """
        Generate sentiment statistics.

        Parameters
        ----------
        df : pd.DataFrame
            Data with sentiment columns

        Returns
        -------
        Dict
            Summary statistics
        """
        stats = {
            "total_articles": len(df),
            "avg_polarity": df["polarity"].mean(),
            "median_polarity": df["polarity"].median(),
            "std_polarity": df["polarity"].std(),
            "positive_count": (df["sentiment_label"] == "positive").sum(),
            "negative_count": (df["sentiment_label"] == "negative").sum(),
            "neutral_count": (df["sentiment_label"] == "neutral").sum(),
            "avg_subjectivity": df["subjectivity"].mean(),
        }

        stats["positive_pct"] = stats["positive_count"] / stats["total_articles"] * 100
        stats["negative_pct"] = stats["negative_count"] / stats["total_articles"] * 100
        stats["neutral_pct"] = stats["neutral_count"] / stats["total_articles"] * 100

        return stats
