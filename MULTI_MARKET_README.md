# Multi-Market Stock Analysis - US & Malaysia Support

## 📍 Market Support

The GUI now supports both **US (NASDAQ/NYSE)** and **Malaysia (KLSE)** stock markets with quick selection and preset portfolios.

### Quick Start

#### **US Market (Default)**
```bash
# GUI for US stocks
python launcher.py --gui

# US market with specific stock
python launcher.py AAPL MSFT GOOGL

# Preset: US Top 5 Tech
python launcher.py -m US AAPL MSFT NVDA GOOGL TSLA
```

#### **Malaysia Market**
```bash
# GUI for Malaysia stocks
python launcher.py --gui -m MALAYSIA

# Note: Malaysia stocks use different ticker formats
# Available through GUI preset buttons
```

## 🌍 Market Features

### US Market
- **Default Market**: Automatically selected
- **Quick Tickers**: AAPL, MSFT, GOOGL, AMZN, NVDA
- **Presets Available**: US Top 5 Tech
- **Symbol Format**: Standard (AAPL, TSLA, GOOGL, etc.)
- **Data**: Real-time from NASDAQ/NYSE
- **Hours**: 9:30 AM - 4:00 PM EST

### Malaysia Market (KLSE)
- **Market Name**: Kuala Lumpur Stock Exchange
- **Quick Selection**: Available in GUI dropdown
- **Preset Tickers**: 
  - MAYBANK (Major Banking)
  - TENAGA (National Energy)
  - PETRONAS (Oil & Gas)
  - CIMB (Banking)
  - PUBLIC (Banking)
- **Symbol Format**: Depends on data provider
- **Data**: Via yfinance
- **Note**: Some symbols may require specific formatting

## 🎯 GUI Usage

### Single Stock Analysis

1. **Select Market**:
   - Click dropdown: "US" or "MALAYSIA"
   - Quick buttons update automatically

2. **Choose Stock**:
   - Click quick ticker button (AAPL, MSFT, etc.)
   - Or type ticker manually
   - Select time period

3. **Analyze**:
   - Click "Analyze" button
   - View results in tabs

### Multi-Stock Portfolio

1. **Go to "Multi-Stock" Tab**

2. **Select Market**:
   - US or MALAYSIA in dropdown

3. **Use Presets**:
   - "US Top 5" → AAPL,MSFT,GOOGL,AMZN,NVDA
   - "Malaysia Top 5" → Preset Malaysia portfolio

4. **Custom Selection**:
   - Edit ticker list
   - Separate with commas

5. **Click "Analyze All"**

## 📊 Switching Markets

### In GUI

```
Market Selection:
┌─────────────────────────────────┐
│ Market: [US ▼]                  │
│ Quick: [AAPL] [MSFT] [GOOGL]... │
└─────────────────────────────────┘
```

Click dropdown to switch:
- **US**: Default market
- **MALAYSIA**: Kuala Lumpur Stock Exchange

Quick buttons automatically update based on selected market.

### In CLI

```bash
# US stocks (default)
python launcher.py AAPL MSFT

# Malaysia stocks
python launcher.py -m MALAYSIA <tickers>

# GUI with Malaysia market
python launcher.py --gui -m MALAYSIA
```

## 🔍 Stock Lists

### US Market Stocks (Available)
```
Technology:  AAPL, MSFT, GOOGL, NVDA, TSLA, META, NFLX
Financials:  JPM, BAC, GS, WFC
Energy:      XOM, CVX, COP
Retail:      AMZN, WMT, TGT
Healthcare:  JNJ, PFE, UNH
And 1000+ more...
```

### Malaysia Market Stocks
```
Banking:     MAYBANK.KL, CIMB.KL, PUBLIC.KL, AMMB.KL, BIMB.KL
Energy:      TENAGA.KL, PETRONAS.KL, MISC.KL
Telecom:     MAXIS.KL, DIGI.KL, AXIATA.KL
Property:    KLCC.KL, UMW.KL, GENM.KL
Healthcare:  IHH.KL
```

## 💡 Tips

1. **Use Quick Buttons**: Faster than typing
2. **Preset Portfolios**: Compare market sectors
3. **Period Selection**: 
   - 1mo = Short-term traders
   - 1y = Medium-term investors
   - 5y = Long-term analysis
4. **Multi-Stock Tab**: Compare sectors across markets

## 🚀 Command Examples

### US Market Analysis
```bash
# Single stock
python launcher.py TSLA -p 1y

# Multiple stocks
python launcher.py AAPL MSFT GOOGL AMZN -p 6mo

# GUI
python launcher.py --gui

# JSON export
python launcher.py NVDA --json
```

### Malaysia Market Analysis
```bash
# GUI with Malaysia
python launcher.py --gui -m MALAYSIA

# CLI analysis
python launcher.py -m MALAYSIA <tickers>

# Multi-stock portfolio
python launcher.py -m MALAYSIA TICKER1 TICKER2
```

### Mixed Usage
```bash
# Launch GUI (defaults to US)
python launcher.py --gui

# Use dropdown to switch to Malaysia inside GUI

# Or launch GUI directly with Malaysia
python launcher.py --gui -m MALAYSIA
```

## 📈 Key Differences

| Feature | US Market | Malaysia Market |
|---------|-----------|-----------------|
| **Data Source** | NASDAQ/NYSE | KLSE |
| **Trading Hours** | 9:30-16:00 EST | 9:00-17:00 MYT |
| **Currency** | USD | MYR |
| **Volatility** | Higher | Varies |
| **Liquidity** | Very High | High |
| **Timezone** | Eastern | Malaysia |

## ⚙️ Configuration

### Default Markets
- **GUI**: Defaults to US market
- **CLI**: Defaults to US market
- **Override**: Use `-m MALAYSIA` flag

### Market Switching
GUI maintains separate selections for:
- Single stock analysis (uses main market selector)
- Multi-stock analysis (can differ from main)

### Preset Portfolios
Each market has preset buttons:
- **5 Quick Tickers** in main view
- **2 Preset Portfolios** in multi-stock tab

## 🔧 Customization

Edit `stock_gui.py` to add more markets or stocks:

```python
MARKETS = {
    'US': {
        'name': 'US Market',
        'tickers': ['AAPL', 'MSFT', ...],
        'default': 'AAPL',
    },
    'MALAYSIA': {
        'name': 'Malaysia (KLSE)',
        'tickers': ['MAYBANK.KL', ...],
        'default': 'MAYBANK.KL',
    },
    # Add more markets here
}
```

## 📚 Analysis Features (All Markets)

Regardless of market selected, all analysis features apply:
- ✅ 40+ Technical Indicators
- ✅ Price Charts with MA/EMA
- ✅ RSI, MACD, Bollinger Bands
- ✅ Support/Resistance Levels
- ✅ Performance Metrics
- ✅ Trading Signals
- ✅ Multi-Stock Comparison

## ⚠️ Notes

1. **Data Quality**: Market depth varies by exchange
2. **Liquidity**: Some Malaysia stocks may have lower liquidity
3. **Symbols**: Always verify correct symbol format
4. **Timezone**: Adjust time-based analysis for local timezone
5. **Currency**: Results in local currency of exchange

## 🆘 Troubleshooting

### "No data found for ticker"
- Verify ticker symbol spelling
- Check if stock is actively trading
- Try different time period

### "Symbol may be delisted"
- Stock may have been delisted
- Try alternative stock in same sector
- Check market website for available tickers

### Malaysia stocks not working
- Try alternative ticker format
- Use GUI preset buttons
- Check KLSE official website

## 🔄 Future Enhancements

Planned additions:
- [ ] Singapore Market (SGX)
- [ ] Hong Kong Market (HKEX)
- [ ] India Market (NSE/BSE)
- [ ] Thailand Market (SET)
- [ ] Regional comparison tools
- [ ] Currency conversion
- [ ] Cross-market correlation analysis

---

**Happy Trading Across Markets! 🌍📈**
