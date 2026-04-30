#!/usr/bin/env python3
"""
Stock Analysis Quick Launcher
Choose between CLI analysis and GUI dashboard
"""

import sys
import argparse
from stock_analysis import StockAnalyzer, analyze_multiple_stocks
import json
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


def print_report(ticker, report):
    """Pretty print analysis report"""
    if 'error' in report:
        print(f"{Fore.RED}Error: {report['error']}{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{report['ticker']} - Stock Analysis Report{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    # Basic Info
    print(f"{Fore.CYAN}CURRENT PRICE & CHANGES:{Style.RESET_ALL}")
    print(f"  Price:        ${report['current_price']:.2f}")
    
    change_1d = report['price_change_1d']
    color = Fore.GREEN if change_1d >= 0 else Fore.RED
    print(f"  1-Day:        {color}{change_1d:+.2f}%{Style.RESET_ALL}")
    
    change_1w = report['price_change_1w']
    color = Fore.GREEN if change_1w >= 0 else Fore.RED
    print(f"  1-Week:       {color}{change_1w:+.2f}%{Style.RESET_ALL}")
    
    # Technical Indicators
    print(f"\n{Fore.CYAN}TECHNICAL INDICATORS:{Style.RESET_ALL}")
    
    rsi = report['rsi']
    if rsi > 70:
        rsi_status = f"{Fore.RED}OVERBOUGHT{Style.RESET_ALL}"
    elif rsi < 30:
        rsi_status = f"{Fore.GREEN}OVERSOLD{Style.RESET_ALL}"
    else:
        rsi_status = f"{Fore.YELLOW}NEUTRAL{Style.RESET_ALL}"
    print(f"  RSI (14):     {rsi:.2f} - {rsi_status}")
    
    macd = report['macd']
    macd_signal = report['macd_signal']
    macd_status = f"{Fore.GREEN}BULLISH{Style.RESET_ALL}" if macd > macd_signal else f"{Fore.RED}BEARISH{Style.RESET_ALL}"
    print(f"  MACD:         {macd_status}")
    
    atr = report['atr']
    print(f"  ATR (14):     {atr:.4f}")
    
    adx = report['adx']
    if adx > 25:
        adx_status = f"{Fore.GREEN}STRONG{Style.RESET_ALL}"
    else:
        adx_status = f"{Fore.YELLOW}WEAK{Style.RESET_ALL}"
    print(f"  ADX (14):     {adx:.2f} - {adx_status}")
    
    volatility = report['volatility']
    print(f"  Volatility:   {volatility:.2f}%")
    
    # Trend Analysis
    trend_data = report['trend_analysis']
    print(f"\n{Fore.CYAN}TREND ANALYSIS:{Style.RESET_ALL}")
    print(f"  Trend:        {Fore.YELLOW}{trend_data['trend']}{Style.RESET_ALL}")
    print(f"  Position:     {trend_data['position']}")
    print(f"  EMA Signal:   {Fore.GREEN if trend_data['ema_signal'] == 'BULLISH' else Fore.RED}{trend_data['ema_signal']}{Style.RESET_ALL}")
    
    # Support & Resistance
    sr = report['support_resistance']
    print(f"\n{Fore.CYAN}SUPPORT & RESISTANCE:{Style.RESET_ALL}")
    print(f"  Support:      ${sr['support']:.2f} ({sr['distance_to_support']:+.2f}%)")
    print(f"  Resistance:   ${sr['resistance']:.2f} ({sr['distance_to_resistance']:+.2f}%)")
    
    # Performance Metrics
    perf = report['performance_metrics']
    print(f"\n{Fore.CYAN}PERFORMANCE METRICS:{Style.RESET_ALL}")
    
    total_return = perf['total_return']
    color = Fore.GREEN if total_return >= 0 else Fore.RED
    print(f"  Total Return: {color}{total_return:+.2f}%{Style.RESET_ALL}")
    
    annual_return = perf['annual_return']
    color = Fore.GREEN if annual_return >= 0 else Fore.RED
    print(f"  Annual Ret:   {color}{annual_return:+.2f}%{Style.RESET_ALL}")
    
    sharpe = perf['sharpe_ratio']
    print(f"  Sharpe Ratio: {sharpe:.3f}")
    
    sortino = perf['sortino_ratio']
    print(f"  Sortino Ratio:{sortino:.3f}")
    
    max_dd = perf['max_drawdown']
    color = Fore.RED if max_dd < -20 else Fore.YELLOW
    print(f"  Max Drawdown: {color}{max_dd:.2f}%{Style.RESET_ALL}")
    
    win_rate = perf['win_rate']
    print(f"  Win Rate:     {win_rate:.2f}%")
    
    # Trading Signals
    signals = report['trading_signals']
    print(f"\n{Fore.CYAN}TRADING SIGNALS:{Style.RESET_ALL}")
    
    for signal_name, signal_value in signals.items():
        if "BUY" in signal_value or "BULLISH" in signal_value:
            color = Fore.GREEN
        elif "SELL" in signal_value or "BEARISH" in signal_value:
            color = Fore.RED
        else:
            color = Fore.YELLOW
        
        print(f"  {signal_name.upper():12} {color}{signal_value}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extreme Stock Analysis Suite (US & Malaysia Markets)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher.py AAPL               # Analyze AAPL in CLI
  python launcher.py AAPL MSFT GOOGL   # Analyze multiple US stocks in CLI
  python launcher.py --gui              # Launch GUI dashboard (US market)
  python launcher.py --gui -m MALAYSIA  # Launch GUI dashboard (Malaysia market)
  python launcher.py --gui MAYBANK.KL   # Launch GUI with Malaysian stock
  python launcher.py -p 3mo AAPL        # 3-month analysis
  python launcher.py MAYBANK.KL TENAGA.KL -m MALAYSIA  # Malaysia CLI analysis
        """
    )
    
    parser.add_argument('tickers', nargs='*', help='Stock ticker symbols')
    parser.add_argument('-g', '--gui', action='store_true', help='Launch GUI dashboard')
    parser.add_argument('-m', '--market', choices=['US', 'MALAYSIA'], default='US', 
                       help='Market selection (default: US)')
    parser.add_argument('-p', '--period', default='1y', help='Analysis period (default: 1y)')
    parser.add_argument('-j', '--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Launch GUI if requested
    if args.gui:
        try:
            from stock_gui import StockAnalysisGUI
            import tkinter as tk
            
            root = tk.Tk()
            market = args.market.upper() if args.market else 'US'
            # Load ticker if provided
            app = StockAnalysisGUI(root, market=market)
            if args.tickers:
                app.ticker_var.set(args.tickers[0].upper())
                app.period_var.set(args.period)
            root.mainloop()
        except ImportError:
            print(f"{Fore.RED}Error: tkinter not available{Style.RESET_ALL}")
            sys.exit(1)
        return
    
    # CLI Analysis
    if not args.tickers:
        print(f"{Fore.YELLOW}No tickers provided. Use --gui for GUI or provide tickers.{Style.RESET_ALL}")
        parser.print_help()
        sys.exit(1)
    
    print(f"{Fore.CYAN}Analyzing {len(args.tickers)} stock(s) with period: {args.period}{Style.RESET_ALL}\n")
    
    # Analyze stocks
    results = analyze_multiple_stocks(args.tickers, args.period)
    
    if args.json:
        # Output as JSON
        # Convert numpy types to python types for JSON serialization
        def convert_types(obj):
            import numpy as np
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_types(item) for item in obj]
            return obj
        
        json_output = convert_types(results)
        print(json.dumps(json_output, indent=2))
    else:
        # Pretty print
        for ticker, report in results.items():
            print_report(ticker, report)
    
    print(f"{Fore.GREEN}Analysis complete!{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
