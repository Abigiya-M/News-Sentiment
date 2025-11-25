# Scripts

Standalone Python scripts for batch processing and automation.

## Available Scripts

### run_analysis.py
Main orchestration script that runs the complete analysis pipeline:

```bash
python scripts/run_analysis.py --data data/raw/ --output data/processed/
```

Options:
- `--data`: Path to raw data directory
- `--output`: Path to output processed data
- `--sentiment`: Run sentiment analysis
- `--indicators`: Calculate technical indicators
- `--correlation`: Run correlation analysis

## Development

Scripts should be modular and reusable, importing from the `src/` package.

Example structure:
```python
from src import data_loader, preprocessor, sentiment_analyzer

# Implementation
```
