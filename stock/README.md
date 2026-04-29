# Advanced Stock Tracker

A powerful Python script that pulls real-time stock data with color-coded output, multiple timeframes, filtering, and export capabilities.

## New Features

✅ **Color-Coded Output** - Green for gains, red for losses  
✅ **Multiple Timeframes** - 1h, 1d, 1w, 1m, 3m, 1y gains  
✅ **Export to CSV/Excel** - Save results for analysis  
✅ **Smart Filtering** - Filter by gain %, price range  
✅ **Config File Support** - Save custom stock lists  
✅ **All Timeframes View** - See gains across all periods  

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### Track default popular stocks with 1-day gains:
```bash
python stock_tracker.py
```

### Track specific stocks:
```bash
python stock_tracker.py AAPL MSFT GOOGL TSLA
```

### Save custom stock list to config:
```bash
python stock_tracker.py AAPL MSFT NVDA --config
```

This creates `stock_config.json` and uses it for future runs.

## Advanced Options

### Different Timeframes
```bash
# 1-hour gains
python stock_tracker.py --timeframe 1h

# Weekly gains
python stock_tracker.py --timeframe 1w

# Monthly gains
python stock_tracker.py --timeframe 1m

# All timeframes at once
python stock_tracker.py --all-timeframes
```

### Filtering

Filter by gain percentage:
```bash
# Only stocks with gains between 0.5% and 5%
python stock_tracker.py --min-gain 0.5 --max-gain 5

# Only positive gainers
python stock_tracker.py --min-gain 0
```

Filter by price:
```bash
# Stocks between $100 and $500
python stock_tracker.py --min-price 100 --max-price 500

# Affordable stocks under $50
python stock_tracker.py --max-price 50
```

Combine filters:
```bash
python stock_tracker.py --min-gain 1 --min-price 50 --max-price 300
```

### Export Results

Export to CSV:
```bash
python stock_tracker.py --export-csv

# Custom filename
python stock_tracker.py --export-csv --output my_stocks.csv
```

Export to Excel:
```bash
python stock_tracker.py --export-xlsx

# Custom filename
python stock_tracker.py --export-xlsx --output my_stocks.xlsx
```

Export all timeframes to Excel (separate sheets):
```bash
python stock_tracker.py --all-timeframes --export-xlsx --output analysis.xlsx
```

## Examples

### Find tech stocks with biggest gains this week:
```bash
python stock_tracker.py AAPL MSFT GOOGL NVDA TSLA AMD INTC --timeframe 1w --export-xlsx
```

### Monitor S&P 500 tech gainers:
```bash
python stock_tracker.py AAPL MSFT GOOGL AMZN NVDA META NFLX --min-gain 0 --export-csv
```

### Penny stocks under $10 with daily gains:
```bash
python stock_tracker.py --max-price 10 --export-xlsx
```

## Features

- **Real-time Data**: Uses Yahoo Finance API for accurate stock prices
- **Multiple Timeframes**: 1h, 1d, 1w, 1m, 3m, 1y
- **Color Output**: 
  - 🟢 Green = Positive gains
  - 🔴 Red = Negative losses
  - 🟡 Yellow = No change
- **Sorting**: Automatically sorted by highest gains first
- **Company Names**: Shows full company names alongside tickers
- **Error Handling**: Gracefully handles invalid tickers
- **Flexible Filtering**: Filter by gain % and price range
- **Export Formats**: CSV and Excel (.xlsx) support
- **Config Management**: Save and load custom stock lists
- **Top Performers**: Highlights top 5 gainers

## Default Stocks Tracked

AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META, NFLX, GOOG, BRK.B, JNJ, V, WMT, JPM, DIS, PYPL, ADBE, CRM, INTC, AMD

## Output

The script displays:
- Ticker symbol
- Company name
- Current price
- Start price (for timeframe)
- Change in dollars and percentage
- Top 5 gainers highlighted
- Optional: Exported files

## Command-Line Arguments

```
--tickers TICKER1 TICKER2...  Stock tickers to track
--config                       Save current tickers to config file
--timeframe {1h,1d,1w,1m,3m,1y} Timeframe for gains (default: 1d)
--min-gain PERCENT            Filter: minimum gain percentage
--max-gain PERCENT            Filter: maximum gain percentage
--min-price PRICE             Filter: minimum stock price
--max-price PRICE             Filter: maximum stock price
--export-csv                  Export results to CSV
--export-xlsx                 Export results to Excel
--output FILENAME             Custom output filename for exports
--all-timeframes              Show results for all timeframes
```

## Requirements

- Python 3.7+
- yfinance (stock data)
- pandas (data processing)
- colorama (colored output)
- openpyxl (Excel export)

