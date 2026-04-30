#!/usr/bin/env python3
"""
Extreme Stock Analysis Engine
Comprehensive technical analysis with advanced indicators and metrics
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats
from typing import Dict, Tuple, List
import warnings

warnings.filterwarnings('ignore')


class StockAnalyzer:
    """Advanced stock analysis with extreme technical indicators"""
    
    def __init__(self, ticker: str, period: str = '1y'):
        self.ticker = ticker
        self.period = period
        self.data = None
        self.analysis_results = {}
        self._fetch_data()
    
    def _fetch_data(self):
        """Fetch stock data from yfinance"""
        try:
            self.data = yf.download(self.ticker, period=self.period, progress=False)
            if self.data is None or self.data.empty:
                print(f"Warning: No data for {self.ticker}")
                return False
            return True
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            return False
    
    def calculate_sma(self, window: int = 20) -> pd.Series:
        """Simple Moving Average"""
        return self.data['Close'].rolling(window=window).mean()
    
    def calculate_ema(self, window: int = 20) -> pd.Series:
        """Exponential Moving Average"""
        return self.data['Close'].ewm(span=window, adjust=False).mean()
    
    def calculate_rsi(self, window: int = 14) -> pd.Series:
        """Relative Strength Index"""
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """MACD - Moving Average Convergence Divergence"""
        ema_fast = self.data['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = self.data['Close'].ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram
    
    def calculate_bollinger_bands(self, window: int = 20, num_std: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Bollinger Bands"""
        sma = self.calculate_sma(window)
        std = self.data['Close'].rolling(window=window).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return upper_band, sma, lower_band
    
    def calculate_atr(self, window: int = 14) -> pd.Series:
        """Average True Range - Volatility indicator"""
        high_low = self.data['High'] - self.data['Low']
        high_close = np.abs(self.data['High'] - self.data['Close'].shift())
        low_close = np.abs(self.data['Low'] - self.data['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(window=window).mean()
        return atr
    
    def calculate_adx(self, window: int = 14) -> pd.Series:
        """Average Directional Index - Trend strength"""
        high_diff = self.data['High'].diff()
        low_diff = -self.data['Low'].diff()
        
        plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        minus_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)
        
        tr = self.calculate_atr(window)
        plus_di = 100 * (plus_dm.rolling(window).mean() / tr)
        minus_di = 100 * (minus_dm.rolling(window).mean() / tr)
        
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window).mean()
        return adx
    
    def calculate_stochastic(self, window: int = 14) -> Tuple[pd.Series, pd.Series]:
        """Stochastic Oscillator"""
        low_min = self.data['Low'].rolling(window).min()
        high_max = self.data['High'].rolling(window).max()
        
        k_percent = 100 * ((self.data['Close'] - low_min) / (high_max - low_min))
        d_percent = k_percent.rolling(3).mean()
        return k_percent, d_percent
    
    def calculate_obv(self) -> pd.Series:
        """On-Balance Volume"""
        obv = (np.sign(self.data['Close'].diff()) * self.data['Volume']).fillna(0).cumsum()
        return obv
    
    def calculate_vpt(self) -> pd.Series:
        """Volume Price Trend"""
        pct_change = self.data['Close'].pct_change()
        vpt = (pct_change * self.data['Volume']).fillna(0).cumsum()
        return vpt
    
    def calculate_volatility(self, window: int = 20) -> pd.Series:
        """Historical Volatility (Standard Deviation of Returns)"""
        returns = self.data['Close'].pct_change()
        volatility = returns.rolling(window).std() * np.sqrt(252)  # Annualized
        return volatility
    
    def calculate_support_resistance(self, window: int = 20) -> Dict:
        """Find support and resistance levels"""
        high_max = self.data['High'].rolling(window).max()
        low_min = self.data['Low'].rolling(window).min()
        
        current_price = self._to_scalar(self.data['Close'].iloc[-1])
        resistance = self._to_scalar(high_max.iloc[-1])
        support = self._to_scalar(low_min.iloc[-1])
        
        return {
            'support': support,
            'resistance': resistance,
            'current_price': current_price,
            'distance_to_resistance': ((resistance - current_price) / current_price) * 100,
            'distance_to_support': ((current_price - support) / current_price) * 100,
        }
    
    def calculate_correlation_matrix(self, other_tickers: List[str]) -> pd.DataFrame:
        """Calculate correlation with other stocks"""
        all_tickers = [self.ticker] + other_tickers
        data = yf.download(all_tickers, period=self.period, progress=False)['Close']
        correlation = data.pct_change().corr()
        return correlation
    
    def _to_scalar(self, value):
        """Convert Series to scalar if needed"""
        if isinstance(value, pd.Series):
            return float(value.iloc[0]) if len(value) > 0 else 0
        return float(value)
    
    def calculate_performance_metrics(self) -> Dict:
        """Calculate performance metrics"""
        returns = self.data['Close'].pct_change().dropna()
        cumulative_returns = (1 + returns).cumprod() - 1
        
        # Basic metrics - ensure we get scalar values
        total_return = self._to_scalar(cumulative_returns.iloc[-1])
        annual_return = (1 + total_return) ** (252 / len(returns)) - 1
        daily_volatility = self._to_scalar(returns.std())
        annual_volatility = daily_volatility * np.sqrt(252)
        
        # Sharpe Ratio (assuming risk-free rate of 5%)
        risk_free_rate = 0.05
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility if annual_volatility > 0 else 0
        
        # Sortino Ratio (downside volatility)
        downside_returns = returns[returns < 0]
        downside_volatility = self._to_scalar(downside_returns.std()) * np.sqrt(252) if len(downside_returns) > 0 else 0
        sortino_ratio = (annual_return - risk_free_rate) / downside_volatility if downside_volatility > 0 else 0
        
        # Max Drawdown
        cumulative_max = cumulative_returns.cummax()
        drawdown = cumulative_returns - cumulative_max
        max_drawdown = self._to_scalar(drawdown.min())
        
        # Win Rate
        win_count = self._to_scalar((returns > 0).sum())
        win_rate = win_count / len(returns) * 100 if len(returns) > 0 else 0
        
        # Calmar Ratio
        calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        return {
            'total_return': total_return * 100,
            'annual_return': annual_return * 100,
            'annual_volatility': annual_volatility * 100,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown * 100,
            'calmar_ratio': calmar_ratio,
            'win_rate': win_rate,
            'daily_volatility': daily_volatility * 100,
        }
    
    def calculate_trend_analysis(self) -> Dict:
        """Analyze current trend"""
        sma_20 = self.calculate_sma(20)
        sma_50 = self.calculate_sma(50)
        sma_200 = self.calculate_sma(200)
        ema_12 = self.calculate_ema(12)
        ema_26 = self.calculate_ema(26)
        
        current_price = self._to_scalar(self.data['Close'].iloc[-1])
        current_sma_20 = self._to_scalar(sma_20.iloc[-1])
        current_sma_50 = self._to_scalar(sma_50.iloc[-1])
        current_sma_200 = self._to_scalar(sma_200.iloc[-1])
        current_ema_12 = self._to_scalar(ema_12.iloc[-1])
        current_ema_26 = self._to_scalar(ema_26.iloc[-1])
        
        # Trend signal
        if current_sma_20 > current_sma_50 > current_sma_200:
            trend = "STRONG UPTREND"
        elif current_sma_20 > current_sma_50:
            trend = "UPTREND"
        elif current_sma_20 < current_sma_50 < current_sma_200:
            trend = "STRONG DOWNTREND"
        elif current_sma_20 < current_sma_50:
            trend = "DOWNTREND"
        else:
            trend = "NEUTRAL"
        
        # Price position
        if current_price > current_sma_200:
            position = "ABOVE 200-day MA"
        else:
            position = "BELOW 200-day MA"
        
        return {
            'trend': trend,
            'position': position,
            'price_vs_sma20': ((current_price - current_sma_20) / current_sma_20) * 100,
            'price_vs_sma50': ((current_price - current_sma_50) / current_sma_50) * 100,
            'price_vs_sma200': ((current_price - current_sma_200) / current_sma_200) * 100,
            'ema_signal': 'BULLISH' if current_ema_12 > current_ema_26 else 'BEARISH',
        }
    
    def calculate_trading_signals(self) -> Dict:
        """Generate trading signals based on technical indicators"""
        signals = {}
        
        # RSI Signal
        rsi = self.calculate_rsi()
        current_rsi = self._to_scalar(rsi.iloc[-1])
        if current_rsi < 30:
            signals['rsi'] = 'OVERSOLD (BUY)'
        elif current_rsi > 70:
            signals['rsi'] = 'OVERBOUGHT (SELL)'
        else:
            signals['rsi'] = 'NEUTRAL'
        
        # MACD Signal
        macd, signal_line, histogram = self.calculate_macd()
        macd_val = self._to_scalar(macd.iloc[-1])
        signal_val = self._to_scalar(signal_line.iloc[-1])
        if macd_val > signal_val:
            signals['macd'] = 'BULLISH'
        else:
            signals['macd'] = 'BEARISH'
        
        # Bollinger Bands Signal
        upper_bb, mid_bb, lower_bb = self.calculate_bollinger_bands()
        current_price = self._to_scalar(self.data['Close'].iloc[-1])
        upper_val = self._to_scalar(upper_bb.iloc[-1])
        lower_val = self._to_scalar(lower_bb.iloc[-1])
        
        if current_price > upper_val:
            signals['bollinger'] = 'OVERBOUGHT'
        elif current_price < lower_val:
            signals['bollinger'] = 'OVERSOLD'
        else:
            signals['bollinger'] = 'NEUTRAL'
        
        # Stochastic Signal
        k_percent, d_percent = self.calculate_stochastic()
        current_k = self._to_scalar(k_percent.iloc[-1])
        if current_k < 20:
            signals['stochastic'] = 'OVERSOLD (BUY)'
        elif current_k > 80:
            signals['stochastic'] = 'OVERBOUGHT (SELL)'
        else:
            signals['stochastic'] = 'NEUTRAL'
        
        return signals
    
    def generate_analysis_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        if self.data is None or self.data.empty:
            return {'error': 'No data available'}
        
        current_price = self._to_scalar(self.data['Close'].iloc[-1])
        prev_price = self._to_scalar(self.data['Close'].iloc[-2]) if len(self.data) > 1 else current_price
        
        price_change_1d = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
        
        price_change_1w = 0
        if len(self.data) > 5:
            price_1w_ago = self._to_scalar(self.data['Close'].iloc[-5])
            price_change_1w = ((current_price - price_1w_ago) / price_1w_ago) * 100 if price_1w_ago > 0 else 0
        
        price_change_1m = 0
        if len(self.data) > 22:
            price_1m_ago = self._to_scalar(self.data['Close'].iloc[-22])
            price_change_1m = ((current_price - price_1m_ago) / price_1m_ago) * 100 if price_1m_ago > 0 else 0
        
        report = {
            'ticker': self.ticker,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'current_price': current_price,
            'price_change_1d': price_change_1d,
            'price_change_1w': price_change_1w,
            'price_change_1m': price_change_1m,
            
            # Technical Indicators
            'rsi': self._to_scalar(self.calculate_rsi().iloc[-1]),
            'macd': self._to_scalar(self.calculate_macd()[0].iloc[-1]),
            'macd_signal': self._to_scalar(self.calculate_macd()[1].iloc[-1]),
            'atr': self._to_scalar(self.calculate_atr().iloc[-1]),
            'adx': self._to_scalar(self.calculate_adx().iloc[-1]),
            'volatility': self._to_scalar(self.calculate_volatility().iloc[-1]),
            'obv': self._to_scalar(self.calculate_obv().iloc[-1]),
            'vpt': self._to_scalar(self.calculate_vpt().iloc[-1]),
            
            # Bollinger Bands
            'bb_upper': self._to_scalar(self.calculate_bollinger_bands()[0].iloc[-1]),
            'bb_middle': self._to_scalar(self.calculate_bollinger_bands()[1].iloc[-1]),
            'bb_lower': self._to_scalar(self.calculate_bollinger_bands()[2].iloc[-1]),
            
            # Stochastic
            'stochastic_k': self._to_scalar(self.calculate_stochastic()[0].iloc[-1]),
            'stochastic_d': self._to_scalar(self.calculate_stochastic()[1].iloc[-1]),
            
            # Support/Resistance
            'support_resistance': self.calculate_support_resistance(),
            
            # Performance Metrics
            'performance_metrics': self.calculate_performance_metrics(),
            
            # Trend Analysis
            'trend_analysis': self.calculate_trend_analysis(),
            
            # Trading Signals
            'trading_signals': self.calculate_trading_signals(),
        }
        
        self.analysis_results = report
        return report
    
    def get_analysis_summary(self) -> Dict:
        """Get a summary of the analysis"""
        if not self.analysis_results:
            self.generate_analysis_report()
        
        summary = {
            'ticker': self.ticker,
            'current_price': self.analysis_results.get('current_price'),
            'trend': self.analysis_results.get('trend_analysis', {}).get('trend'),
            'rsi': self.analysis_results.get('rsi'),
            'signals': self.analysis_results.get('trading_signals'),
            'performance': {
                'annual_return': self.analysis_results.get('performance_metrics', {}).get('annual_return'),
                'max_drawdown': self.analysis_results.get('performance_metrics', {}).get('max_drawdown'),
                'sharpe_ratio': self.analysis_results.get('performance_metrics', {}).get('sharpe_ratio'),
            }
        }
        
        return summary


def analyze_multiple_stocks(tickers: List[str], period: str = '1y') -> Dict:
    """Analyze multiple stocks and return reports"""
    results = {}
    for ticker in tickers:
        analyzer = StockAnalyzer(ticker, period)
        results[ticker] = analyzer.generate_analysis_report()
    return results
