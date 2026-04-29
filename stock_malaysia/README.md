# Malaysia Stock Tracker (KLSE)

A powerful Python script that pulls real-time Malaysia stock data from Kuala Lumpur Stock Exchange (KLSE) with color-coded output, multiple timeframes, filtering, and export capabilities.

## Features

✅ **Malaysia Stock Focus** - Tracks stocks on Kuala Lumpur Stock Exchange (KLSE)  
✅ **Color-Coded Output** - Green for gains, red for losses  
✅ **Multiple Timeframes** - 1h, 1d, 1w, 1m, 3m, 1y gains  
✅ **Export to CSV/Excel** - Save results for analysis  
✅ **Smart Filtering** - Filter by gain %, price range  
✅ **Config File Support** - Save custom Malaysia stock lists  
✅ **All Timeframes View** - See gains across all periods  

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### Track default Malaysia stocks with 1-day gains:
```bash
python stock_tracker.py
```

Default Malaysia stocks include:
- **MAYBANK.KL** - Maybank
- **TENAGA.KL** - Tenaga Nasional (National Energy)
- **PETRONAS.KL** - Petronas
- **CIMB.KL** - CIMB Group
- **PUBLIC.KL** - Public Bank
- **AXIATA.KL** - Axiata Group
- **GENM.KL** - Genting Malaysia
- **KLCC.KL** - Kuala Lumpur City Centre
- **MAXIS.KL** - Maxis Communications
- **IHH.KL** - IHH Healthcare
- **AMMB.KL** - AmBank Group
- **MISC.KL** - MISC (Malaysia International Shipping Corporation)
- **DIGI.KL** - Digi Telecommunications
- **BIMB.KL** - Bank Islam
- **UMW.KL** - UMW Holdings

### Track specific Malaysia stocks:
```bash
python stock_tracker.py MAYBANK.KL TENAGA.KL PETRONAS.KL CIMB.KL
```

### Save custom Malaysia stock list to config:
```bash
python stock_tracker.py MAYBANK.KL TENAGA.KL AXIATA.KL --config
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

# Yearly gains
python stock_tracker.py --timeframe 1y
```

### Filtering
```bash
# Stocks with at least 2% gain
python stock_tracker.py --min-gain 2

# Stocks between 5 and 100 price
python stock_tracker.py --min-price 5 --max-price 100

# Combine filters
python stock_tracker.py --min-gain -5 --max-gain 5
```

### Export Results
```bash
# Export to CSV
python stock_tracker.py --export-csv

# Export to Excel
python stock_tracker.py --export-xlsx

# Custom filename
python stock_tracker.py --export-csv --output my_stocks.csv
```

### All Timeframes
```bash
# Show all timeframes at once
python stock_tracker.py --all-timeframes

# Export all timeframes to Excel (multiple sheets)
python stock_tracker.py --all-timeframes --export-xlsx
```

## Examples

### Track specific stocks with weekly gains:
```bash
python stock_tracker.py MAYBANK.KL TENAGA.KL CIMB.KL --timeframe 1w
```

### Export top gainers over 3 months:
```bash
python stock_tracker.py --timeframe 3m --export-xlsx --output top_gainers.xlsx
```

### Filter for positive movers and export:
```bash
python stock_tracker.py --min-gain 0.5 --export-csv
```

### Track blue-chip stocks with all timeframes:
```bash
python stock_tracker.py MAYBANK.KL TENAGA.KL PETRONAS.KL --all-timeframes --export-xlsx
```

## Notes

- All Malaysia stock tickers must use the **.KL** suffix
- Prices are displayed in USD (as per yfinance data)
- Data is fetched from Yahoo Finance in real-time
- Trading hours and data availability depend on KLSE operating hours
- Historical data goes back approximately 1 year

## Troubleshooting

**No data returned?**
- Check that tickers are correct and use .KL suffix
- Ensure internet connection is active
- Verify stocks are active on KLSE

**Import errors?**
- Run `pip install -r requirements.txt`
- Verify Python 3.7+ is installed

**Color output not showing?**
- Colorama is installed for Windows compatibility
- On some terminals, colors may need to be manually enabled
