"""
News Sentiment Analysis Project

A comprehensive analysis of financial news sentiment and stock market movements.
"""

__version__ = "0.1.0"
__author__ = "Nova Financial Solutions"

from . import data_loader, preprocessor, sentiment_analyzer, technical_indicators

__all__ = [
    "data_loader",
    "preprocessor",
    "sentiment_analyzer",
    "technical_indicators",
]
