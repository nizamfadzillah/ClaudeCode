#!/usr/bin/env python3
"""
Stock Analysis GUI
Interactive dashboard for viewing extreme stock analysis with charts
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import yfinance as yf
from stock_analysis import StockAnalyzer, analyze_multiple_stocks
from datetime import datetime
import threading
import json


class StockAnalysisGUI:
    
    # Market configurations
    MARKETS = {
        'US': {
            'name': 'US Market',
            'tickers': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 
                       'NFLX', 'BRK.B', 'JNJ', 'V', 'WMT', 'JPM', 'DIS', 'PYPL'],
            'default': 'AAPL',
        },
        'MALAYSIA': {
            'name': 'Malaysia (KLSE)',
            'tickers': ['MAYBANK.KL', 'TENAGA.KL', 'PETRONAS.KL', 'CIMB.KL', 'PUBLIC.KL',
                       'AXIATA.KL', 'GENM.KL', 'KLCC.KL', 'MAXIS.KL', 'IHH.KL',
                       'AMMB.KL', 'MISC.KL', 'DIGI.KL', 'BIMB.KL', 'UMW.KL'],
            'default': 'MAYBANK.KL',
        },
    }
    
    def __init__(self, root, market='US'):
        self.root = root
        self.root.title("Extreme Stock Analysis Dashboard (US & Malaysia)")
        self.root.geometry("1400x900")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.market = market
        self.current_analyzer = None
        self.analysis_data = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Create main UI structure"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Market Selection Frame
        market_frame = ttk.LabelFrame(main_frame, text="Market Selection", padding=10)
        market_frame.grid(row=0, column=0, sticky='ew', pady=(0, 5))
        market_frame.grid_columnconfigure(2, weight=1)
        
        ttk.Label(market_frame, text="Market:").grid(row=0, column=0, padx=5)
        self.market_var = tk.StringVar(value=self.market)
        market_combo = ttk.Combobox(market_frame, textvariable=self.market_var,
                                   values=['US', 'MALAYSIA'],
                                   width=12, state="readonly")
        market_combo.grid(row=0, column=1, padx=5)
        market_combo.bind('<<ComboboxSelected>>', self._on_market_changed)
        
        # Quick ticker buttons
        ttk.Label(market_frame, text="Quick Tickers:").grid(row=0, column=2, padx=(20, 5))
        self.quick_buttons_frame = ttk.Frame(market_frame)
        self.quick_buttons_frame.grid(row=0, column=3, columnspan=3, sticky='ew', padx=5)
        self._update_quick_buttons()
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Analysis Controls", padding=10)
        control_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        control_frame.grid_columnconfigure(1, weight=1)
        
        # Ticker input
        ttk.Label(control_frame, text="Stock Ticker:").grid(row=0, column=0, padx=5)
        self.ticker_var = tk.StringVar(value=self.MARKETS[self.market]['default'])
        self.ticker_entry = ttk.Entry(control_frame, textvariable=self.ticker_var, width=20)
        self.ticker_entry.grid(row=0, column=1, padx=5, sticky='w')
        
        # Period selection
        ttk.Label(control_frame, text="Period:").grid(row=0, column=2, padx=5)
        self.period_var = tk.StringVar(value="1y")
        period_combo = ttk.Combobox(control_frame, textvariable=self.period_var, 
                                    values=["1mo", "3mo", "6mo", "1y", "2y", "5y"], 
                                    width=10, state="readonly")
        period_combo.grid(row=0, column=3, padx=5)
        
        # Analyze button
        self.analyze_button = ttk.Button(control_frame, text="Analyze", command=self._analyze_stock)
        self.analyze_button.grid(row=0, column=4, padx=5)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready", foreground="blue")
        self.status_label.grid(row=0, column=5, padx=5)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, sticky='nsew')
        
        # Summary Tab
        self.summary_frame = ttk.Frame(notebook)
        notebook.add(self.summary_frame, text="Summary")
        self._create_summary_tab()
        
        # Technical Indicators Tab
        self.indicators_frame = ttk.Frame(notebook)
        notebook.add(self.indicators_frame, text="Technical Indicators")
        self._create_indicators_tab()
        
        # Charts Tab
        self.charts_frame = ttk.Frame(notebook)
        notebook.add(self.charts_frame, text="Charts")
        self._create_charts_tab()
        
        # Performance Tab
        self.performance_frame = ttk.Frame(notebook)
        notebook.add(self.performance_frame, text="Performance")
        self._create_performance_tab()
        
        # Signals Tab
        self.signals_frame = ttk.Frame(notebook)
        notebook.add(self.signals_frame, text="Trading Signals")
        self._create_signals_tab()
        
        # Multi-Stock Analysis Tab
        self.multi_frame = ttk.Frame(notebook)
        notebook.add(self.multi_frame, text="Multi-Stock")
        self._create_multi_stock_tab()
    
    def _update_quick_buttons(self):
        """Update quick ticker buttons based on selected market"""
        # Clear existing buttons
        for widget in self.quick_buttons_frame.winfo_children():
            widget.destroy()
        
        market_tickers = self.MARKETS[self.market_var.get()]['tickers'][:5]
        for ticker in market_tickers:
            btn = ttk.Button(self.quick_buttons_frame, text=ticker, width=8,
                           command=lambda t=ticker: self.ticker_var.set(t))
            btn.pack(side=tk.LEFT, padx=2)
    
    def _on_market_changed(self, event=None):
        """Handle market selection change"""
        self.market = self.market_var.get()
        self.ticker_var.set(self.MARKETS[self.market]['default'])
        self._update_quick_buttons()
    
    def _on_multi_market_changed(self, event=None):
        """Handle multi-stock market selection change"""
        if self.multi_market_var.get() == 'US':
            self.multi_ticker_var.set("AAPL,MSFT,GOOGL,AMZN,NVDA")
        else:
            self.multi_ticker_var.set("MAYBANK.KL,TENAGA.KL,PETRONAS.KL,CIMB.KL,PUBLIC.KL")
    
    def _create_summary_tab(self):
        """Create summary tab"""
        self.summary_frame.grid_rowconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(0, weight=1)
        
        # Create text widget with scrollbar
        self.summary_text = scrolledtext.ScrolledText(self.summary_frame, height=30, width=100, 
                                                      font=("Courier", 10), bg="#f0f0f0")
        self.summary_text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Configure tags for colors
        self.summary_text.tag_config("header", foreground="#0066cc", font=("Courier", 11, "bold"))
        self.summary_text.tag_config("positive", foreground="#00aa00")
        self.summary_text.tag_config("negative", foreground="#cc0000")
        self.summary_text.tag_config("neutral", foreground="#666666")
    
    def _create_indicators_tab(self):
        """Create technical indicators tab"""
        self.indicators_frame.grid_rowconfigure(0, weight=1)
        self.indicators_frame.grid_columnconfigure(0, weight=1)
        
        self.indicators_text = scrolledtext.ScrolledText(self.indicators_frame, height=30, width=100,
                                                         font=("Courier", 10), bg="#f0f0f0")
        self.indicators_text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        self.indicators_text.tag_config("indicator", foreground="#0066cc", font=("Courier", 10, "bold"))
        self.indicators_text.tag_config("value", foreground="#000000")
    
    def _create_charts_tab(self):
        """Create charts tab"""
        self.charts_frame.grid_rowconfigure(0, weight=1)
        self.charts_frame.grid_columnconfigure(0, weight=1)
        
        # Chart type selector
        control_frame = ttk.Frame(self.charts_frame)
        control_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        ttk.Label(control_frame, text="Chart Type:").pack(side=tk.LEFT, padx=5)
        self.chart_var = tk.StringVar(value="price")
        chart_combo = ttk.Combobox(control_frame, textvariable=self.chart_var,
                                   values=["price", "rsi", "macd", "bollinger", "volume"],
                                   width=15, state="readonly")
        chart_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Update Chart", command=self._update_chart).pack(side=tk.LEFT, padx=5)
        
        # Canvas for chart
        self.charts_canvas_frame = ttk.Frame(self.charts_frame)
        self.charts_canvas_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.charts_frame.grid_rowconfigure(1, weight=1)
    
    def _create_performance_tab(self):
        """Create performance tab"""
        self.performance_frame.grid_rowconfigure(0, weight=1)
        self.performance_frame.grid_columnconfigure(0, weight=1)
        
        self.performance_text = scrolledtext.ScrolledText(self.performance_frame, height=30, width=100,
                                                          font=("Courier", 10), bg="#f0f0f0")
        self.performance_text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        self.performance_text.tag_config("metric", foreground="#0066cc", font=("Courier", 10, "bold"))
        self.performance_text.tag_config("excellent", foreground="#00aa00")
        self.performance_text.tag_config("warning", foreground="#ff6600")
        self.performance_text.tag_config("danger", foreground="#cc0000")
    
    def _create_signals_tab(self):
        """Create trading signals tab"""
        self.signals_frame.grid_rowconfigure(0, weight=1)
        self.signals_frame.grid_columnconfigure(0, weight=1)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(self.signals_frame, bg="white")
        scrollbar = ttk.Scrollbar(self.signals_frame, orient="vertical", command=canvas.yview)
        self.signals_content = ttk.Frame(canvas, padding=10)
        
        self.signals_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.signals_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.signals_frame.grid_rowconfigure(0, weight=1)
        self.signals_frame.grid_columnconfigure(0, weight=1)
    
    def _create_multi_stock_tab(self):
        """Create multi-stock analysis tab"""
        control_frame = ttk.LabelFrame(self.multi_frame, text="Analyze Multiple Stocks", padding=10)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Market selector
        ttk.Label(control_frame, text="Market:").pack(side=tk.LEFT, padx=5)
        self.multi_market_var = tk.StringVar(value=self.market)
        multi_market_combo = ttk.Combobox(control_frame, textvariable=self.multi_market_var,
                                         values=['US', 'MALAYSIA'],
                                         width=12, state="readonly")
        multi_market_combo.pack(side=tk.LEFT, padx=5)
        multi_market_combo.bind('<<ComboboxSelected>>', self._on_multi_market_changed)
        
        # Preset buttons
        ttk.Label(control_frame, text="Presets:").pack(side=tk.LEFT, padx=(20, 5))
        
        def set_preset_us():
            self.multi_ticker_var.set("AAPL,MSFT,GOOGL,AMZN,NVDA")
        
        def set_preset_malaysia():
            self.multi_ticker_var.set("MAYBANK.KL,TENAGA.KL,PETRONAS.KL,CIMB.KL,PUBLIC.KL")
        
        self.preset_us_btn = ttk.Button(control_frame, text="US Top 5", command=set_preset_us)
        self.preset_us_btn.pack(side=tk.LEFT, padx=2)
        
        self.preset_my_btn = ttk.Button(control_frame, text="Malaysia Top 5", command=set_preset_malaysia)
        self.preset_my_btn.pack(side=tk.LEFT, padx=2)
        
        # Ticker input
        ttk.Label(control_frame, text="Tickers (comma-separated):").pack(side=tk.LEFT, padx=5)
        self.multi_ticker_var = tk.StringVar(value="AAPL,MSFT,GOOGL,AMZN,NVDA")
        multi_entry = ttk.Entry(control_frame, textvariable=self.multi_ticker_var, width=40)
        multi_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(control_frame, text="Analyze All", command=self._analyze_multiple).pack(side=tk.LEFT, padx=5)
        
        # Results area
        self.multi_frame.grid_rowconfigure(1, weight=1)
        self.multi_frame.grid_columnconfigure(0, weight=1)
        
        self.multi_text = scrolledtext.ScrolledText(self.multi_frame, height=30, width=100,
                                                    font=("Courier", 9), bg="#f0f0f0")
        self.multi_text.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    
    def _analyze_stock(self):
        """Analyze stock (run in thread)"""
        ticker = self.ticker_var.get().upper()
        period = self.period_var.get()
        
        if not ticker:
            messagebox.showerror("Error", "Please enter a ticker symbol")
            return
        
        self.analyze_button.config(state=tk.DISABLED)
        self.status_label.config(text="Analyzing...", foreground="orange")
        self.root.update()
        
        thread = threading.Thread(target=self._analyze_worker, args=(ticker, period))
        thread.daemon = True
        thread.start()
    
    def _analyze_worker(self, ticker, period):
        """Worker thread for analysis"""
        try:
            self.current_analyzer = StockAnalyzer(ticker, period)
            self.analysis_data = self.current_analyzer.generate_analysis_report()
            
            self._update_summary()
            self._update_indicators()
            self._update_performance()
            self._update_signals()
            self._update_chart()
            
            self.status_label.config(text=f"✓ Analysis Complete", foreground="green")
        except Exception as e:
            messagebox.showerror("Analysis Error", str(e))
            self.status_label.config(text="Error", foreground="red")
        finally:
            self.analyze_button.config(state=tk.NORMAL)
    
    def _update_summary(self):
        """Update summary tab"""
        if not self.analysis_data or 'error' in self.analysis_data:
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, "No data available", "neutral")
            return
        
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        
        data = self.analysis_data
        
        # Header
        self.summary_text.insert(tk.END, f"╔════════════════════════════════════════╗\n", "header")
        self.summary_text.insert(tk.END, f"║ STOCK ANALYSIS SUMMARY\n", "header")
        self.summary_text.insert(tk.END, f"╚════════════════════════════════════════╝\n\n", "header")
        
        # Basic Info
        self.summary_text.insert(tk.END, f"Ticker:          {data.get('ticker', 'N/A')}\n", "neutral")
        self.summary_text.insert(tk.END, f"Current Price:   ${data.get('current_price', 0):.2f}\n", "neutral")
        self.summary_text.insert(tk.END, f"Analysis Time:   {data.get('timestamp', 'N/A')}\n\n", "neutral")
        
        # Price Changes
        self.summary_text.insert(tk.END, "PRICE CHANGES:\n", "header")
        change_1d = data.get('price_change_1d', 0)
        color_1d = "positive" if change_1d >= 0 else "negative"
        self.summary_text.insert(tk.END, f"  1-Day:   {change_1d:+.2f}%\n", color_1d)
        
        change_1w = data.get('price_change_1w', 0)
        color_1w = "positive" if change_1w >= 0 else "negative"
        self.summary_text.insert(tk.END, f"  1-Week:  {change_1w:+.2f}%\n", color_1w)
        
        change_1m = data.get('price_change_1m', 0)
        color_1m = "positive" if change_1m >= 0 else "negative"
        self.summary_text.insert(tk.END, f"  1-Month: {change_1m:+.2f}%\n\n", color_1m)
        
        # Trend Analysis
        trend_data = data.get('trend_analysis', {})
        self.summary_text.insert(tk.END, "TREND ANALYSIS:\n", "header")
        self.summary_text.insert(tk.END, f"  Trend:           {trend_data.get('trend', 'N/A')}\n", "neutral")
        self.summary_text.insert(tk.END, f"  Position:        {trend_data.get('position', 'N/A')}\n", "neutral")
        self.summary_text.insert(tk.END, f"  Price vs SMA20:  {trend_data.get('price_vs_sma20', 0):+.2f}%\n", "neutral")
        self.summary_text.insert(tk.END, f"  Price vs SMA50:  {trend_data.get('price_vs_sma50', 0):+.2f}%\n", "neutral")
        self.summary_text.insert(tk.END, f"  Price vs SMA200: {trend_data.get('price_vs_sma200', 0):+.2f}%\n", "neutral")
        self.summary_text.insert(tk.END, f"  EMA Signal:      {trend_data.get('ema_signal', 'N/A')}\n\n", "neutral")
        
        # Support/Resistance
        sr_data = data.get('support_resistance', {})
        self.summary_text.insert(tk.END, "SUPPORT & RESISTANCE:\n", "header")
        self.summary_text.insert(tk.END, f"  Support:              ${sr_data.get('support', 0):.2f}\n", "positive")
        self.summary_text.insert(tk.END, f"  Resistance:           ${sr_data.get('resistance', 0):.2f}\n", "negative")
        self.summary_text.insert(tk.END, f"  Distance to Support:  {sr_data.get('distance_to_support', 0):+.2f}%\n", "neutral")
        self.summary_text.insert(tk.END, f"  Distance to Resist:   {sr_data.get('distance_to_resistance', 0):+.2f}%\n\n", "neutral")
    
    def _update_indicators(self):
        """Update indicators tab"""
        if not self.analysis_data or 'error' in self.analysis_data:
            self.indicators_text.delete(1.0, tk.END)
            self.indicators_text.insert(tk.END, "No data available", "neutral")
            return
        
        self.indicators_text.config(state=tk.NORMAL)
        self.indicators_text.delete(1.0, tk.END)
        
        data = self.analysis_data
        
        self.indicators_text.insert(tk.END, f"╔════════════════════════════════════════╗\n", "indicator")
        self.indicators_text.insert(tk.END, f"║ TECHNICAL INDICATORS\n", "indicator")
        self.indicators_text.insert(tk.END, f"╚════════════════════════════════════════╝\n\n", "indicator")
        
        # RSI
        rsi = data.get('rsi', 0)
        self.indicators_text.insert(tk.END, "RSI (14):\n", "indicator")
        self.indicators_text.insert(tk.END, f"  Value: {rsi:.2f}\n", "value")
        if rsi > 70:
            self.indicators_text.insert(tk.END, f"  Status: OVERBOUGHT (Sell Signal)\n\n", "negative")
        elif rsi < 30:
            self.indicators_text.insert(tk.END, f"  Status: OVERSOLD (Buy Signal)\n\n", "positive")
        else:
            self.indicators_text.insert(tk.END, f"  Status: NEUTRAL\n\n", "value")
        
        # MACD
        macd = data.get('macd', 0)
        macd_signal = data.get('macd_signal', 0)
        self.indicators_text.insert(tk.END, "MACD:\n", "indicator")
        self.indicators_text.insert(tk.END, f"  MACD Line:     {macd:.4f}\n", "value")
        self.indicators_text.insert(tk.END, f"  Signal Line:   {macd_signal:.4f}\n", "value")
        self.indicators_text.insert(tk.END, f"  Histogram:     {macd - macd_signal:.4f}\n", "value")
        signal_text = "BULLISH" if macd > macd_signal else "BEARISH"
        signal_color = "positive" if signal_text == "BULLISH" else "negative"
        self.indicators_text.insert(tk.END, f"  Signal:        {signal_text}\n\n", signal_color)
        
        # Bollinger Bands
        bb_upper = data.get('bb_upper', 0)
        bb_middle = data.get('bb_middle', 0)
        bb_lower = data.get('bb_lower', 0)
        self.indicators_text.insert(tk.END, "Bollinger Bands (20, 2):\n", "indicator")
        self.indicators_text.insert(tk.END, f"  Upper Band:    ${bb_upper:.2f}\n", "negative")
        self.indicators_text.insert(tk.END, f"  Middle Band:   ${bb_middle:.2f}\n", "value")
        self.indicators_text.insert(tk.END, f"  Lower Band:    ${bb_lower:.2f}\n\n", "positive")
        
        # Stochastic
        stoch_k = data.get('stochastic_k', 0)
        stoch_d = data.get('stochastic_d', 0)
        self.indicators_text.insert(tk.END, "Stochastic Oscillator:\n", "indicator")
        self.indicators_text.insert(tk.END, f"  %K:            {stoch_k:.2f}\n", "value")
        self.indicators_text.insert(tk.END, f"  %D:            {stoch_d:.2f}\n", "value")
        if stoch_k > 80:
            status = "OVERBOUGHT"
            color = "negative"
        elif stoch_k < 20:
            status = "OVERSOLD"
            color = "positive"
        else:
            status = "NEUTRAL"
            color = "value"
        self.indicators_text.insert(tk.END, f"  Status:        {status}\n\n", color)
        
        # ATR & ADX
        atr = data.get('atr', 0)
        adx = data.get('adx', 0)
        self.indicators_text.insert(tk.END, "Volatility & Trend Indicators:\n", "indicator")
        self.indicators_text.insert(tk.END, f"  ATR (14):      {atr:.4f}\n", "value")
        self.indicators_text.insert(tk.END, f"  ADX (14):      {adx:.2f}\n", "value")
        if adx > 25:
            self.indicators_text.insert(tk.END, f"  Trend Strength: STRONG\n\n", "positive")
        else:
            self.indicators_text.insert(tk.END, f"  Trend Strength: WEAK\n\n", "negative")
        
        # Volume Indicators
        obv = data.get('obv', 0)
        vpt = data.get('vpt', 0)
        self.indicators_text.insert(tk.END, "Volume Indicators:\n", "indicator")
        self.indicators_text.insert(tk.END, f"  OBV:           {obv:.0f}\n", "value")
        self.indicators_text.insert(tk.END, f"  VPT:           {vpt:.0f}\n", "value")
        
        # Volatility
        volatility = data.get('volatility', 0)
        self.indicators_text.insert(tk.END, f"  Volatility:    {volatility:.2f}%\n", "value")
    
    def _update_performance(self):
        """Update performance tab"""
        if not self.analysis_data or 'error' in self.analysis_data:
            self.performance_text.delete(1.0, tk.END)
            self.performance_text.insert(tk.END, "No data available")
            return
        
        self.performance_text.config(state=tk.NORMAL)
        self.performance_text.delete(1.0, tk.END)
        
        metrics = self.analysis_data.get('performance_metrics', {})
        
        self.performance_text.insert(tk.END, f"╔════════════════════════════════════════╗\n", "metric")
        self.performance_text.insert(tk.END, f"║ PERFORMANCE METRICS\n", "metric")
        self.performance_text.insert(tk.END, f"╚════════════════════════════════════════╝\n\n", "metric")
        
        # Return Metrics
        self.performance_text.insert(tk.END, "RETURNS:\n", "metric")
        total_ret = metrics.get('total_return', 0)
        color = "excellent" if total_ret >= 0 else "danger"
        self.performance_text.insert(tk.END, f"  Total Return:         {total_ret:+.2f}%\n", color)
        
        annual_ret = metrics.get('annual_return', 0)
        color = "excellent" if annual_ret >= 0 else "danger"
        self.performance_text.insert(tk.END, f"  Annualized Return:    {annual_ret:+.2f}%\n", color)
        
        win_rate = metrics.get('win_rate', 0)
        color = "excellent" if win_rate >= 50 else "danger"
        self.performance_text.insert(tk.END, f"  Win Rate:             {win_rate:.2f}%\n\n", color)
        
        # Risk Metrics
        self.performance_text.insert(tk.END, "RISK:\n", "metric")
        vol = metrics.get('annual_volatility', 0)
        color = "excellent" if vol <= 20 else "warning" if vol <= 40 else "danger"
        self.performance_text.insert(tk.END, f"  Annual Volatility:    {vol:.2f}%\n", color)
        
        max_dd = metrics.get('max_drawdown', 0)
        color = "excellent" if max_dd >= -20 else "warning" if max_dd >= -50 else "danger"
        self.performance_text.insert(tk.END, f"  Max Drawdown:         {max_dd:.2f}%\n\n", color)
        
        # Risk-Adjusted Returns
        self.performance_text.insert(tk.END, "RISK-ADJUSTED RETURNS:\n", "metric")
        sharpe = metrics.get('sharpe_ratio', 0)
        color = "excellent" if sharpe >= 1 else "warning" if sharpe >= 0 else "danger"
        self.performance_text.insert(tk.END, f"  Sharpe Ratio:         {sharpe:.3f}\n", color)
        
        sortino = metrics.get('sortino_ratio', 0)
        color = "excellent" if sortino >= 2 else "warning" if sortino >= 1 else "danger"
        self.performance_text.insert(tk.END, f"  Sortino Ratio:        {sortino:.3f}\n", color)
        
        calmar = metrics.get('calmar_ratio', 0)
        color = "excellent" if calmar >= 1 else "warning" if calmar >= 0 else "danger"
        self.performance_text.insert(tk.END, f"  Calmar Ratio:         {calmar:.3f}\n", color)
    
    def _update_signals(self):
        """Update trading signals tab"""
        if not self.analysis_data or 'error' in self.analysis_data:
            self.signals_content.destroy()
            self.signals_content = ttk.Label(self.signals_frame, text="No data available")
            return
        
        # Clear existing widgets
        for widget in self.signals_content.winfo_children():
            widget.destroy()
        
        signals = self.analysis_data.get('trading_signals', {})
        
        # Header
        header = ttk.Label(self.signals_content, text="TRADING SIGNALS", 
                          font=("Arial", 12, "bold"), foreground="#0066cc")
        header.pack(anchor=tk.W, pady=(0, 10))
        
        signal_map = {
            'rsi': ('RSI Signal', '#FF6B6B'),
            'macd': ('MACD Signal', '#4ECDC4'),
            'bollinger': ('Bollinger Bands Signal', '#45B7D1'),
            'stochastic': ('Stochastic Signal', '#FFA07A'),
        }
        
        for key, (label, color) in signal_map.items():
            signal_value = signals.get(key, 'NEUTRAL')
            
            frame = ttk.Frame(self.signals_content, relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, pady=5, padx=5)
            
            signal_label = tk.Label(frame, text=label, font=("Arial", 10, "bold"),
                                   bg=color, fg="white", anchor=tk.W)
            signal_label.pack(fill=tk.X, padx=10, pady=5)
            
            # Color code the signal
            if "BUY" in signal_value:
                signal_color = "#00aa00"
            elif "SELL" in signal_value:
                signal_color = "#cc0000"
            elif "BULLISH" in signal_value:
                signal_color = "#00aa00"
            elif "BEARISH" in signal_value:
                signal_color = "#cc0000"
            else:
                signal_color = "#666666"
            
            signal_value_label = tk.Label(frame, text=signal_value, font=("Arial", 11, "bold"),
                                         fg=signal_color, bg="white", pady=5)
            signal_value_label.pack(fill=tk.X, padx=10)
    
    def _update_chart(self):
        """Update chart"""
        if not self.current_analyzer or not self.current_analyzer.data is not None:
            return
        
        # Clear previous chart
        for widget in self.charts_canvas_frame.winfo_children():
            widget.destroy()
        
        chart_type = self.chart_var.get()
        fig = Figure(figsize=(12, 6), dpi=100)
        
        data = self.current_analyzer.data
        
        if chart_type == "price":
            ax = fig.add_subplot(111)
            ax.plot(data.index, data['Close'], label='Close Price', linewidth=2, color='#0066cc')
            
            # Add moving averages
            sma_20 = self.current_analyzer.calculate_sma(20)
            sma_50 = self.current_analyzer.calculate_sma(50)
            sma_200 = self.current_analyzer.calculate_sma(200)
            
            ax.plot(data.index, sma_20, label='SMA 20', alpha=0.7, color='#FF6B6B', linewidth=1)
            ax.plot(data.index, sma_50, label='SMA 50', alpha=0.7, color='#4ECDC4', linewidth=1)
            ax.plot(data.index, sma_200, label='SMA 200', alpha=0.7, color='#95E1D3', linewidth=1)
            
            ax.set_title(f'{self.ticker_var.get().upper()} - Price Chart', fontsize=14, fontweight='bold')
            ax.set_ylabel('Price ($)', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
        
        elif chart_type == "rsi":
            ax = fig.add_subplot(111)
            rsi = self.current_analyzer.calculate_rsi()
            ax.plot(data.index, rsi, label='RSI (14)', linewidth=2, color='#4ECDC4')
            ax.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Overbought (70)')
            ax.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='Oversold (30)')
            ax.fill_between(data.index, 30, 70, alpha=0.1, color='yellow')
            ax.set_title(f'{self.ticker_var.get().upper()} - RSI (14)', fontsize=14, fontweight='bold')
            ax.set_ylabel('RSI', fontsize=12)
            ax.set_ylim(0, 100)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
        
        elif chart_type == "macd":
            ax = fig.add_subplot(111)
            macd, signal, histogram = self.current_analyzer.calculate_macd()
            ax.plot(data.index, macd, label='MACD', linewidth=2, color='#0066cc')
            ax.plot(data.index, signal, label='Signal', linewidth=2, color='#FF6B6B')
            colors = ['green' if h > 0 else 'red' for h in histogram]
            ax.bar(data.index, histogram, label='Histogram', color=colors, alpha=0.3)
            ax.set_title(f'{self.ticker_var.get().upper()} - MACD', fontsize=14, fontweight='bold')
            ax.set_ylabel('MACD', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
        
        elif chart_type == "bollinger":
            ax = fig.add_subplot(111)
            upper, middle, lower = self.current_analyzer.calculate_bollinger_bands()
            ax.plot(data.index, data['Close'], label='Close', linewidth=2, color='#0066cc')
            ax.plot(data.index, upper, label='Upper Band', linewidth=1, color='red', alpha=0.5)
            ax.plot(data.index, middle, label='Middle Band', linewidth=1, color='gray', alpha=0.5)
            ax.plot(data.index, lower, label='Lower Band', linewidth=1, color='green', alpha=0.5)
            ax.fill_between(data.index, upper, lower, alpha=0.1, color='blue')
            ax.set_title(f'{self.ticker_var.get().upper()} - Bollinger Bands', fontsize=14, fontweight='bold')
            ax.set_ylabel('Price ($)', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
        
        elif chart_type == "volume":
            ax = fig.add_subplot(111)
            colors = ['green' if data['Close'].iloc[i] >= data['Close'].iloc[i-1] else 'red' 
                     for i in range(1, len(data))]
            ax.bar(data.index[1:], data['Volume'].iloc[1:], color=colors, alpha=0.6, label='Volume')
            ax.set_title(f'{self.ticker_var.get().upper()} - Volume', fontsize=14, fontweight='bold')
            ax.set_ylabel('Volume', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, master=self.charts_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _analyze_multiple(self):
        """Analyze multiple stocks"""
        tickers_str = self.multi_ticker_var.get()
        tickers = [t.strip().upper() for t in tickers_str.split(',')]
        
        self.multi_text.config(state=tk.NORMAL)
        self.multi_text.delete(1.0, tk.END)
        self.multi_text.insert(tk.END, "Analyzing multiple stocks...\n")
        self.root.update()
        
        thread = threading.Thread(target=self._multi_worker, args=(tickers,))
        thread.daemon = True
        thread.start()
    
    def _multi_worker(self, tickers):
        """Worker thread for multiple stock analysis"""
        try:
            results = analyze_multiple_stocks(tickers, self.period_var.get())
            
            self.multi_text.config(state=tk.NORMAL)
            self.multi_text.delete(1.0, tk.END)
            
            # Create comparison table
            self.multi_text.insert(tk.END, "╔════════════════════════════════════════════════════════════════════════════════╗\n")
            self.multi_text.insert(tk.END, "║ MULTI-STOCK ANALYSIS\n")
            self.multi_text.insert(tk.END, "╚════════════════════════════════════════════════════════════════════════════════╝\n\n")
            
            for ticker, data in results.items():
                if 'error' in data:
                    self.multi_text.insert(tk.END, f"\n{ticker}: ERROR - {data['error']}\n")
                    continue
                
                self.multi_text.insert(tk.END, f"\n{'='*80}\n")
                self.multi_text.insert(tk.END, f"{ticker}\n")
                self.multi_text.insert(tk.END, f"{'='*80}\n")
                
                price = data.get('current_price', 0)
                change_1d = data.get('price_change_1d', 0)
                rsi = data.get('rsi', 0)
                trend = data.get('trend_analysis', {}).get('trend', 'N/A')
                sharpe = data.get('performance_metrics', {}).get('sharpe_ratio', 0)
                
                self.multi_text.insert(tk.END, f"Price: ${price:.2f} | 1D Change: {change_1d:+.2f}% | ")
                self.multi_text.insert(tk.END, f"RSI: {rsi:.2f} | Trend: {trend} | Sharpe: {sharpe:.3f}\n")
                
                signals = data.get('trading_signals', {})
                self.multi_text.insert(tk.END, f"Signals: RSI={signals.get('rsi', 'N/A')} | ")
                self.multi_text.insert(tk.END, f"MACD={signals.get('macd', 'N/A')} | ")
                self.multi_text.insert(tk.END, f"Bollinger={signals.get('bollinger', 'N/A')}\n")
        
        except Exception as e:
            self.multi_text.config(state=tk.NORMAL)
            self.multi_text.delete(1.0, tk.END)
            self.multi_text.insert(tk.END, f"Error: {str(e)}")


def main():
    root = tk.Tk()
    app = StockAnalysisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
