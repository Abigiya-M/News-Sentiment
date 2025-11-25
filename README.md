# Predicting Price Moves with News Sentiment

A comprehensive financial analysis project that discovers how headlines shape stock price movements through sentiment analysis, technical indicators, and correlation studies.

## Project Overview

This project focuses on analyzing the relationship between financial news sentiment and stock market movements. We'll:

1. **Perform Sentiment Analysis** - Quantify the tone and sentiment in financial news headlines
2. **Calculate Technical Indicators** - Use TA-Lib for moving averages, RSI, MACD analysis
3. **Analyze Correlations** - Establish statistical correlations between sentiment scores and stock returns
4. **Generate Insights** - Develop actionable investment strategies based on findings

## Dataset: FNSPID

**Financial News and Stock Price Integration Dataset** includes:
- `headline`: Article title with key financial actions
- `url`: Direct link to full news article
- `publisher`: Author/creator of article
- `date`: Publication date and time (UTC-4)
- `stock`: Stock ticker symbol (e.g., AAPL)

## Project Structure

```
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── sentiment_analyzer.py
│   ├── technical_indicators.py
│   └── correlation_analyzer.py
├── notebooks/
│   ├── __init__.py
│   ├── README.md
│   ├── 01_EDA_Data_Understanding.ipynb
│   ├── 02_Technical_Indicators_Analysis.ipynb
│   └── 03_Sentiment_Correlation_Analysis.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_preprocessor.py
│   └── test_sentiment_analyzer.py
├── scripts/
│   ├── __init__.py
│   ├── README.md
│   └── run_analysis.py
├── data/
│   ├── raw/
│   └── processed/
└── reports/
    ├── interim_report.md
    └── final_report.md
```

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git and GitHub account
- Virtual environment (recommended)
- ~2GB disk space for data and models
- Internet connection for yfinance and NLTK downloads

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "News Sentiment"
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Linux/Mac)
   source venv/bin/activate
   
   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
   **Note**: If TA-Lib fails, install via:
   ```bash
   # For Windows
   pip install --no-cache-dir TA-Lib
   
   # For macOS (using Homebrew)
   brew install ta-lib
   pip install TA-Lib
   
   # For Linux
   sudo apt-get install python3-talib
   ```

4. **Download NLTK data** (for sentiment analysis)
   ```bash
   python -c "
   import nltk
   nltk.download('punkt', quiet=True)
   nltk.download('averaged_perceptron_tagger', quiet=True)
   nltk.download('wordnet', quiet=True)
   print('✓ NLTK data downloaded successfully')
   "
   ```

5. **Verify installation**
   ```bash
   python -c "
   import pandas as pd
   import yfinance as yf
   import talib
   from textblob import TextBlob
   print('✓ All dependencies loaded successfully')
   "
   ```

## Workflow & Branches

- `main`: Production-ready code (stable releases)
- `task-1`: EDA and data understanding (exploratory phase)
- `task-2`: Technical indicators and analysis (quantitative phase)
- `task-3`: Sentiment analysis and correlation (integration phase)

### Branch Workflow Example

```bash
# Create and switch to task-1 branch
git checkout -b task-1

# Work on analysis, commit frequently
git add .
git commit -m "feat: add EDA notebook with headline analysis"
git commit -m "feat: implement publisher distribution analysis"

# Push to remote
git push origin task-1

# Create Pull Request to main on GitHub
# After review, merge to main
```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature (e.g., "feat: add sentiment scoring")
fix: fix a bug
docs: documentation changes
refactor: code refactoring
test: add or update tests
chore: maintenance tasks
```

Example:
```bash
git commit -m "feat: implement TextBlob sentiment analysis for 500 headlines"
git commit -m "fix: resolve date alignment issues between news and stock data"
git commit -m "docs: update README with installation instructions"
```

## Running the Analysis

### Method 1: Using Jupyter Notebooks (Recommended for Analysis)

```bash
# Start Jupyter Lab
jupyter lab

# Navigate to notebooks/
# Open each notebook in sequence:
# 1. 01_EDA_Data_Understanding.ipynb
# 2. 02_Technical_Indicators_Analysis.ipynb
# 3. 03_Sentiment_Correlation_Analysis.ipynb

# Run cells sequentially (Shift + Enter)
# Or run all: Kernel → Restart Kernel and Run All Cells
```

### Method 2: Using Python Scripts

```bash
# Run the main analysis script
python scripts/run_analysis.py \
    --data data/raw/ \
    --output data/processed/ \
    --sentiment \
    --indicators \
    --correlation
```

### Method 3: Using CLI

```bash
# Task 1: EDA only
python -m src.data_loader --mode=eda

# Task 2: Technical indicators
python -m src.technical_indicators --ticker=AAPL --start=2025-01-01

# Task 3: Sentiment analysis
python -m src.sentiment_analyzer --headlines_file=data/raw/news.csv
```

## Data Format

### Input Data Structure

**News Data** (`data/raw/news_data.csv`):
```csv
headline,url,publisher,date,stock
"Apple stock hits new high amid strong sales","https://...",Reuters,"2025-11-20",AAPL
"Microsoft reports record earnings","https://...",Bloomberg,"2025-11-19",MSFT
```

**Stock Data** (via yfinance - automatic download):
```
Date        Open    High     Low    Close      Volume
2025-11-25  234.50  235.80  234.20  235.42  52346200
2025-11-24  233.80  234.60  233.20  234.10  48932100
```

### Output Data Structure

**Daily Sentiment** (`data/processed/daily_sentiment.csv`):
```csv
date,stock,avg_polarity,std_polarity,article_count,positive_count,positive_pct
2025-11-25,AAPL,0.156,0.234,5,3,60.0
```

**Correlated Data** (`data/processed/correlation_data.csv`):
```csv
date,stock,Close,Daily_Return,avg_polarity,article_count
2025-11-25,AAPL,235.42,1.23,0.156,5
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_sentiment_analyzer.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Project Structure Details

```
News Sentiment/
├── .vscode/
│   └── settings.json          # VS Code configuration
├── .github/
│   └── workflows/
│       └── unittests.yml      # CI/CD pipeline
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Load news and stock data
│   ├── preprocessor.py        # Data cleaning and alignment
│   ├── sentiment_analyzer.py  # TextBlob sentiment scoring
│   ├── technical_indicators.py # TA-Lib indicators
│   └── correlation_analyzer.py # Statistical analysis
├── notebooks/
│   ├── 01_EDA_Data_Understanding.ipynb
│   ├── 02_Technical_Indicators_Analysis.ipynb
│   └── 03_Sentiment_Correlation_Analysis.ipynb
├── tests/
│   ├── test_data_loader.py
│   ├── test_preprocessor.py
│   └── test_sentiment_analyzer.py
├── scripts/
│   └── run_analysis.py        # Main orchestration script
├── data/
│   ├── raw/                   # Original data files
│   └── processed/             # Cleaned and transformed data
├── reports/
│   ├── interim_report.md      # Mid-week submission
│   └── final_report.md        # Final comprehensive report
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

## Key Features

- **Comprehensive EDA**: Headline analysis, publisher distribution, stock coverage patterns
- **Technical Analysis**: Moving averages, RSI, MACD, Bollinger Bands, ATR indicators
- **Sentiment Analysis**: TextBlob-based polarity and subjectivity scoring
- **Correlation Analysis**: Pearson, Spearman, and lagged correlation testing
- **Trading Signals**: Multi-factor strategy combining sentiment and technical indicators
- **Backtesting**: Historical performance validation with Sharpe ratio and drawdown metrics
- **Visualization**: Interactive plots with Plotly and static plots with Matplotlib
- **Documentation**: Detailed notebooks with inline explanations and insights
- **CI/CD**: GitHub Actions workflow for automated testing and validation
- **Modular Design**: Reusable Python modules for data processing and analysis

## Key Technologies

| Technology | Purpose | Version |
|-----------|---------|---------|
| Python | Core language | 3.9+ |
| pandas | Data manipulation | 2.1.3 |
| numpy | Numerical computing | 1.26.2 |
| yfinance | Stock data | 0.2.32 |
| TA-Lib | Technical indicators | 0.4.28 |
| TextBlob | Sentiment analysis | 0.17.1 |
| scikit-learn | ML utilities | 1.3.2 |
| Jupyter | Interactive notebooks | 1.0.0 |
| Plotly | Interactive plots | 5.18.0 |
| pytest | Testing framework | 7.4.3 |

## Learning Resources

### Stock Market & Financial Analysis
- [Investopedia: Stock Analysis](https://www.investopedia.com/terms/s/stock-analysis.asp)
- [Investopedia: Technical Analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [TA-Lib Documentation](https://github.com/ta-lib/ta-lib-python)

### Natural Language Processing & Sentiment
- [TextBlob Docs](https://textblob.readthedocs.io/)
- [NLTK Book](https://www.nltk.org/book/)
- [Sentiment Analysis Tutorial](https://realpython.com/sentiment-analysis-python/)

### Data Science & Statistics
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Guide](https://numpy.org/doc/)
- [SciPy Statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Hypothesis Testing](https://en.wikipedia.org/wiki/Hypothesis_testing)

### Git & Version Control
- [Git Branching](https://learngitbranching.js.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

### Testing & CI/CD
- [Pytest Guide](https://docs.pytest.org/)
- [Python Testing](https://realpython.com/python-testing/)
- [GitHub Actions](https://github.com/features/actions)

### Stock Market Analysis
- [Investopedia: Stock Market](https://www.investopedia.com/terms/s/stockmarket.asp)
- [Investopedia: Stock Analysis](https://www.investopedia.com/terms/s/stock-analysis.asp)

### Python Libraries
- [TextBlob Documentation](https://textblob.readthedocs.io/en/dev/)
- [TA-Lib Python](https://github.com/ta-lib/ta-lib-python)
- [PyNance](https://github.com/mqandil/pynance)

### Learning Resources
- [Python Testing Guide](https://realpython.com/python-testing/)
- [Git Branching](https://learngitbranching.js.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub CI/CD Setup](https://docs.github.com/en/actions)

## Milestones

- **Nov 23, 2025 (8:00 PM UTC)**: Interim Submission (Task 1 + Partial Task 2)
- **Nov 25, 2025 (8:00 PM UTC)**: Final Submission (All Tasks Complete)

## Report Format

- **Interim Report**: Max 3 pages (markdown format)
- **Final Report**: Max 10 pages with up to 10 plots (Medium blog style)

## Development Notes

- Document code thoroughly
- Use conventional commit messages
- Collaborate via GitHub issues and projects
- Regular testing with pytest
- Code quality checks with flake8 and black

## Support

For questions and discussion, join the Slack channel: `#all-week1`

**Office Hours**: Mon–Fri, 08:00–15:00 UTC

## License

Proprietary - Nova Financial Solutions

---

**Created**: November 2025  
**Challenge Duration**: Week 1 (Nov 19-25, 2025)
