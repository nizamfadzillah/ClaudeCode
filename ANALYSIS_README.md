# Extreme Stock Analysis Suite

A comprehensive stock analysis system with extreme technical indicators and an interactive GUI dashboard.

## Features

### 🔬 Extreme Analysis Engine (`stock_analysis.py`)

The analysis engine includes a comprehensive set of technical indicators:

#### **Moving Averages & Trends**
- Simple Moving Averages (SMA 20, 50, 200)
- Exponential Moving Averages (EMA 12, 26)
- Trend identification (Uptrend, Downtrend, Strong Uptrend/Downtrend)

#### **Momentum Indicators**
- **RSI (Relative Strength Index)** - Overbought/Oversold detection
- **MACD (Moving Average Convergence Divergence)** - Trend and momentum
- **Stochastic Oscillator** - Price momentum and reversal points

#### **Volatility Indicators**
- **Bollinger Bands** - Support/Resistance levels
- **ATR (Average True Range)** - Volatility measurement
- **Historical Volatility** - Annualized volatility calculation

#### **Trend Strength**
- **ADX (Average Directional Index)** - Trend strength (0-100)
- **Trend Direction** - Clear directional signals

#### **Volume Indicators**
- **OBV (On-Balance Volume)** - Volume-based trend confirmation
- **VPT (Volume Price Trend)** - Volume-weighted price tracking

#### **Support & Resistance**
- Dynamic support/resistance level calculation
- Distance to key levels in percentage

#### **Performance Metrics**
- **Total Return** - Overall performance
- **Annual Return** - Annualized returns
- **Annual Volatility** - Risk measurement
- **Sharpe Ratio** - Risk-adjusted returns (RF: 5%)
- **Sortino Ratio** - Downside risk-adjusted returns
- **Calmar Ratio** - Return vs drawdown ratio
- **Max Drawdown** - Largest peak-to-trough decline
- **Win Rate** - Percentage of winning days

#### **Trading Signals**
- RSI signals (Oversold/Overbought)
- MACD signals (Bullish/Bearish)
- Bollinger Bands signals (Overbought/Oversold)
- Stochastic signals (Oversold/Overbought)

### 🎨 Interactive GUI (`stock_gui.py`)

Modern Tkinter-based dashboard with multiple analysis views:

#### **Summary Tab**
- Current price and recent changes
- Trend analysis and positioning
- Support/Resistance levels
- Price relative to moving averages

#### **Technical Indicators Tab**
- All major technical indicators
- Real-time values and interpretations
- Color-coded signals

#### **Charts Tab**
- **Price Chart** - With SMA 20, 50, 200
- **RSI Chart** - With overbought/oversold zones
- **MACD Chart** - With signal line and histogram
- **Bollinger Bands Chart** - With price bands
- **Volume Chart** - Color-coded by price direction

#### **Performance Tab**
- Comprehensive performance metrics
- Risk-adjusted return ratios
- Maximum drawdown analysis
- Win rate statistics
- Color-coded interpretations

#### **Trading Signals Tab**
- All trading signals in a clear dashboard
- Color-coded buy/sell/neutral signals
- Easy-to-read signal cards

#### **Multi-Stock Analysis Tab**
- Analyze multiple stocks simultaneously
- Comparative performance table
- Side-by-side signal comparison

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

For detailed installation, the requirements include:
- `yfinance` - Stock data fetching
- `pandas` - Data manipulation
- `matplotlib` - Charting
- `scipy` - Statistical analysis
- `colorama` - Terminal colors
- `openpyxl` - Excel export

### 2. Verify Installation

```bash
python stock_analysis.py
python stock_gui.py
```

## Usage

### Command Line Analysis

```python
from stock_analysis import StockAnalyzer

# Analyze a single stock
analyzer = StockAnalyzer("AAPL", period="1y")
report = analyzer.generate_analysis_report()

# Access specific indicators
rsi = analyzer.calculate_rsi()
macd = analyzer.calculate_macd()
signals = analyzer.calculate_trading_signals()
```

### GUI Dashboard

```bash
python stock_gui.py
```

1. **Enter Ticker Symbol** - e.g., AAPL, MSFT, GOOGL
2. **Select Time Period** - 1mo, 3mo, 6mo, 1y, 2y, 5y
3. **Click Analyze** - Wait for analysis to complete
4. **Explore Tabs** - View different analysis perspectives
5. **Update Charts** - Select chart type and update

### Multi-Stock Analysis

In the GUI:
1. Go to **Multi-Stock** tab
2. Enter comma-separated tickers: `AAPL,MSFT,GOOGL,TSLA`
3. Click **Analyze All**
4. Compare performance and signals

## Analysis Report Structure

```python
{
    'ticker': 'AAPL',
    'current_price': 150.25,
    'price_change_1d': 1.23,
    'price_change_1w': -0.45,
    'price_change_1m': 5.67,
    
    # Technical Indicators
    'rsi': 65.23,
    'macd': 0.0234,
    'macd_signal': 0.0198,
    'atr': 2.34,
    'adx': 42.5,
    'volatility': 18.5,
    
    # Support & Resistance
    'support_resistance': {
        'support': 145.00,
        'resistance': 155.00,
        'distance_to_support': 3.5,
        'distance_to_resistance': 3.2,
    },
    
    # Performance Metrics
    'performance_metrics': {
        'total_return': 25.5,
        'annual_return': 25.5,
        'annual_volatility': 18.5,
        'sharpe_ratio': 1.35,
        'sortino_ratio': 2.15,
        'max_drawdown': -12.3,
        'calmar_ratio': 2.07,
        'win_rate': 55.2,
    },
    
    # Trend Analysis
    'trend_analysis': {
        'trend': 'STRONG UPTREND',
        'position': 'ABOVE 200-day MA',
        'ema_signal': 'BULLISH',
    },
    
    # Trading Signals
    'trading_signals': {
        'rsi': 'NEUTRAL',
        'macd': 'BULLISH',
        'bollinger': 'NEUTRAL',
        'stochastic': 'OVERSOLD (BUY)',
    }
}
```

## Signal Interpretation

### RSI Signals
- **< 30**: OVERSOLD (Potential BUY)
- **30-70**: NEUTRAL
- **> 70**: OVERBOUGHT (Potential SELL)

### MACD Signals
- **MACD > Signal**: BULLISH (Uptrend)
- **MACD < Signal**: BEARISH (Downtrend)

### Bollinger Bands
- **Price > Upper Band**: OVERBOUGHT
- **Price between bands**: NEUTRAL
- **Price < Lower Band**: OVERSOLD

### ADX Trend Strength
- **< 25**: Weak trend
- **25-40**: Strong trend
- **> 40**: Very strong trend

### Sharpe Ratio Interpretation
- **< 1**: Poor risk-adjusted returns
- **1-2**: Good risk-adjusted returns
- **> 2**: Excellent risk-adjusted returns

## Tips for Extreme Analysis

1. **Combine Multiple Indicators** - Don't rely on single signals
2. **Check Trend Direction** - Strong indicators aligned with trend are more reliable
3. **Monitor Volatility** - High volatility = higher risk
4. **Use Multi-Timeframe Analysis** - Analyze multiple periods for confirmation
5. **Sharpe Ratio Focus** - Higher is better for risk-adjusted returns
6. **Support/Resistance** - Key levels for entry/exit points
7. **Volume Confirmation** - Strong moves should have volume support

## Keyboard Shortcuts (GUI)

- `Ctrl+Q` - Quit application
- `Enter` - Analyze stock (after entering ticker)

## Export & Integration

The analysis engine returns structured dictionaries that can be:
- Converted to JSON for API integration
- Exported to CSV/Excel via pandas
- Integrated into trading bots
- Used for portfolio analysis

## Performance Optimization

For analyzing large numbers of stocks:

```python
from stock_analysis import analyze_multiple_stocks

tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
results = analyze_multiple_stocks(tickers, period='1y')
```

## Disclaimer

This analysis is for educational purposes only. Past performance does not guarantee future results. Always consult with a financial advisor before making investment decisions.

## Requirements

- Python 3.8+
- Internet connection (for real-time data)
- Tkinter (usually included with Python)

## Troubleshooting

**Q: No data returned for ticker**
A: Check ticker symbol is correct (e.g., AAPL not AAPl)

**Q: GUI won't open**
A: Ensure tkinter is installed: `pip install tk`

**Q: Import errors**
A: Reinstall all requirements: `pip install -r requirements.txt --upgrade`

**Q: Analysis takes too long**
A: Try shorter period like "1mo" or "3mo"

## Future Enhancements

- [ ] Real-time data streaming
- [ ] Machine learning predictions
- [ ] Portfolio optimization
- [ ] Backtesting framework
- [ ] Risk management alerts
- [ ] Discord/Telegram notifications
- [ ] Web-based dashboard
