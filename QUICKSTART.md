# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Setup (2 minutes)

```bash
# Clone repository
git clone <your-repo-url>
cd "News Sentiment"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt')"
```

## Step 2: Run Notebooks (2 minutes)

```bash
# Start Jupyter
jupyter lab

# Open and run: 01_EDA_Data_Understanding.ipynb
# Then: 02_Technical_Indicators_Analysis.ipynb
# Finally: 03_Sentiment_Correlation_Analysis.ipynb
```

## Step 3: View Results (1 minute)

Notebooks will display:
- ✓ Data statistics and distributions
- ✓ Publisher and stock analysis charts
- ✓ Technical indicator visualizations
- ✓ Sentiment scores and distributions
- ✓ Correlation analysis results
- ✓ Strategy backtest performance

## Common Commands

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests
pytest tests/ -v

# Format code (optional)
black src/ notebooks/ scripts/

# Lint code (optional)
flake8 src/ --max-line-length=100

# Check dependencies
pip list

# Deactivate environment
deactivate
```

## Troubleshooting

### Issue: TA-Lib installation fails

**Solution**:
```bash
# Try binary installation
pip install --only-binary :all: ta-lib

# Or use anaconda
conda install -c conda-forge ta-lib
```

### Issue: yfinance timeout

**Solution**: Check internet connection or retry:
```python
import yfinance as yf
yf.download('AAPL', start='2025-01-01', retries=5)
```

### Issue: No data in notebooks

**Solution**: Ensure dates are correct:
```python
# Adjust start/end dates for available data
stock_data = yf.download('AAPL', start='2023-01-01', end='2025-11-25')
```

## Next Steps

1. **Customize Analysis**:
   - Add your own stocks to analyze
   - Modify technical indicator parameters
   - Adjust sentiment classification thresholds

2. **Extend Features**:
   - Add more data sources
   - Implement additional indicators
   - Create custom visualizations

3. **Deploy to Production**:
   - Create API endpoints with FastAPI
   - Schedule sentiment updates
   - Integrate with trading system

4. **Improve Results**:
   - Train custom sentiment models
   - Optimize strategy parameters
   - Add risk management rules

## Documentation

- **README.md**: Full project documentation
- **notebooks/**: Interactive analysis notebooks
- **reports/**: Interim and final analysis reports
- **src/**: Python module documentation (docstrings)

## Support & Questions

- **Slack**: #all-week1 (project team)
- **Office Hours**: Mon-Fri, 08:00-15:00 UTC
- **Issues**: Create GitHub issues for bugs/questions

---

**Happy analyzing!** 🚀
