# Analysis Notebooks

## Overview
This directory contains Jupyter notebooks for different stages of the sentiment analysis project.

## Notebook Structure

### 1. Exploratory Data Analysis (EDA)
**File**: `01_EDA_Data_Understanding.ipynb`

Focuses on understanding the dataset structure and initial insights:
- Dataset overview and structure
- Missing value analysis
- Descriptive statistics for text length
- Publisher distribution
- Time series patterns
- Text analysis and topic modeling

### 2. Technical Indicators Analysis
**File**: `02_Technical_Indicators_Analysis.ipynb`

Stock market technical analysis:
- Stock data loading via yfinance
- TA-Lib indicators (Moving Averages, RSI, MACD)
- PyNance financial metrics
- Visualization of price movements and indicators
- Correlation of indicators with price movements

### 3. Sentiment Analysis & Correlation
**File**: `03_Sentiment_Correlation_Analysis.ipynb`

Core analysis linking sentiment to stock movements:
- Date alignment between news and stock data
- Sentiment scoring using TextBlob/NLTK
- Daily return calculations
- Correlation analysis
- Statistical significance testing
- Investment strategy recommendations

## Running Notebooks

1. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

2. **Start Jupyter**
   ```bash
   jupyter lab
   ```

3. **Open desired notebook** and run cells sequentially

## Data Requirements

Place raw data in `../data/raw/` with the following structure:
```
data/
├── raw/
│   ├── news_data.csv          # Headlines with dates and stocks
│   └── stock_prices.csv       # Historical price data
```

## Output

Processed data and analysis results are saved to `../data/processed/`
Charts and visualizations are saved to `../reports/`
