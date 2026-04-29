#!/usr/bin/env python3
"""
Advanced Malaysia Stock tracker script with color output, exports, and multiple timeframes
Tracks stocks on Kuala Lumpur Stock Exchange (KLSE)
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import sys
import json
import os
from colorama import Fore, Style, init
import argparse

# Initialize colorama for cross-platform color support
init(autoreset=True)

CONFIG_FILE = "stock_config.json"

# Malaysia Stock Exchange (KLSE) tickers with .KL suffix
DEFAULT_TICKERS = [
    'MAYBANK.KL', 'TENAGA.KL', 'PETRONAS.KL', 'CIMB.KL', 'PUBLIC.KL',
    'AXIATA.KL', 'GENM.KL', 'KLCC.KL', 'MAXIS.KL', 'IHH.KL',
    'AMMB.KL', 'MISC.KL', 'DIGI.KL', 'BIMB.KL', 'UMW.KL'
]

TIMEFRAMES = {
    '1h': {'days': 5, 'interval': '1h'},      # Fetch 5 days for hourly data
    '1d': {'days': 5, 'interval': '1d'},      # Fetch 5 days, use last 1 day
    '1w': {'days': 10, 'interval': '1d'},     # Fetch 10 days, use last 7 days
    '1m': {'days': 40, 'interval': '1d'},     # Fetch 40 days, use last 30 days
    '3m': {'days': 100, 'interval': '1d'},    # Fetch 100 days, use last 90 days
    '1y': {'days': 375, 'interval': '1d'},    # Fetch 375 days, use last 365 days
}


def load_config():
    """Load stock list from config file if it exists"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('tickers', DEFAULT_TICKERS)
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not load config file: {e}{Style.RESET_ALL}")
    return DEFAULT_TICKERS


def save_config(tickers):
    """Save stock list to config file"""
    try:
        config = {'tickers': tickers}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"{Fore.GREEN}Config saved to {CONFIG_FILE}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving config: {e}{Style.RESET_ALL}")


def get_timeframe_dates(timeframe):
    """Get start and end dates for a given timeframe"""
    end_date = datetime.now()
    days = TIMEFRAMES[timeframe]['days']
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def get_price_data(tickers, timeframe='1d'):
    """Fetch stock data for a given timeframe"""
    start_date, end_date = get_timeframe_dates(timeframe)
    interval = TIMEFRAMES[timeframe]['interval']
    
    try:
        if interval == '1h':
            # For 1-hour data, use 1-hour interval
            data = yf.download(tickers, start=start_date, end=end_date, interval='1h', progress=False)
        else:
            # For daily and longer periods
            data = yf.download(tickers, start=start_date, end=end_date, progress=False)
    except Exception as e:
        print(f"{Fore.RED}Error downloading data: {e}{Style.RESET_ALL}")
        return None
    
    if data is None or data.empty:
        print(f"{Fore.YELLOW}No data returned from yfinance{Style.RESET_ALL}")
        return None
    
    return data


def color_percentage(value):
    """Color-code percentage gains/losses"""
    try:
        percent = float(value.strip('%'))
        if percent > 0:
            return f"{Fore.GREEN}{value}{Style.RESET_ALL}"
        elif percent < 0:
            return f"{Fore.RED}{value}{Style.RESET_ALL}"
        else:
            return f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
    except:
        return value


def color_price_change(value):
    """Color-code price changes"""
    try:
        # Extract the number from the string like "$2.59"
        price_str = value.strip('$')
        price = float(price_str)
        if price > 0:
            return f"{Fore.GREEN}{value}{Style.RESET_ALL}"
        elif price < 0:
            return f"{Fore.RED}{value}{Style.RESET_ALL}"
        else:
            return f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
    except:
        return value


def calculate_gains(tickers, timeframe='1d'):
    """Calculate gains for tickers over a specific timeframe"""
    data = get_price_data(tickers, timeframe)
    
    if data is None:
        return None
    
    results = []
    
    # Determine if we have MultiIndex columns (multiple tickers)
    if isinstance(data.columns, pd.MultiIndex):
        tickers_to_process = list(set([col[1] for col in data.columns if col[0] == 'Close']))
    else:
        tickers_to_process = tickers if isinstance(tickers, list) else [tickers]
    
    # Calculate how many rows to look back based on timeframe
    days_in_period = TIMEFRAMES[timeframe]['days']
    if timeframe == '1h':
        lookback_period = TIMEFRAMES[timeframe]['days']  # hours for 1h
    else:
        lookback_period = TIMEFRAMES[timeframe]['days'] - 5  # days for others, subtract buffer
    
    for ticker in tickers_to_process:
        try:
            if isinstance(data.columns, pd.MultiIndex):
                closes = data[('Close', ticker)].dropna()
            else:
                closes = data['Close'].dropna()
            
            if len(closes) < 2:
                continue
            
            # Get the closes for the period
            if len(closes) > lookback_period:
                period_closes = closes[-lookback_period:]
            else:
                period_closes = closes
            
            if len(period_closes) < 2:
                continue
            
            current_price = period_closes.iloc[-1]
            previous_price = period_closes.iloc[0]
            
            price_change = current_price - previous_price
            percent_change = (price_change / previous_price) * 100
            
            # Get company name
            ticker_info = yf.Ticker(ticker)
            stock_name = ticker_info.info.get('longName', ticker)
            
            results.append({
                'Ticker': ticker,
                'Company': stock_name,
                'Current Price': f"${current_price:.2f}",
                'Start Price': f"${previous_price:.2f}",
                'Change $': f"${price_change:.2f}",
                'Change %': f"{percent_change:.2f}%",
                'Numeric Change': percent_change
            })
        
        except Exception as e:
            continue
    
    if not results:
        return None
    
    df = pd.DataFrame(results)
    df = df.sort_values('Numeric Change', ascending=False)
    df = df.drop('Numeric Change', axis=1)
    
    return df


def apply_filters(df, min_gain=None, max_gain=None, min_price=None, max_price=None):
    """Apply filters to the stock dataframe"""
    if df is None or df.empty:
        return df
    
    # Extract numeric values for filtering
    df_copy = df.copy()
    df_copy['gain_numeric'] = df_copy['Change %'].str.rstrip('%').astype(float)
    df_copy['price_numeric'] = df_copy['Current Price'].str.lstrip('$').astype(float)
    
    if min_gain is not None:
        df_copy = df_copy[df_copy['gain_numeric'] >= min_gain]
    if max_gain is not None:
        df_copy = df_copy[df_copy['gain_numeric'] <= max_gain]
    if min_price is not None:
        df_copy = df_copy[df_copy['price_numeric'] >= min_price]
    if max_price is not None:
        df_copy = df_copy[df_copy['price_numeric'] <= max_price]
    
    return df_copy.drop(['gain_numeric', 'price_numeric'], axis=1)


def export_to_csv(df, filename=None):
    """Export dataframe to CSV"""
    if df is None or df.empty:
        print(f"{Fore.YELLOW}No data to export{Style.RESET_ALL}")
        return
    
    if filename is None:
        filename = f"stocks_malaysia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        df.to_csv(filename, index=False)
        print(f"{Fore.GREEN}Data exported to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error exporting to CSV: {e}{Style.RESET_ALL}")


def export_to_excel(df, filename=None):
    """Export dataframe to Excel"""
    if df is None or df.empty:
        print(f"{Fore.YELLOW}No data to export{Style.RESET_ALL}")
        return
    
    if filename is None:
        filename = f"stocks_malaysia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    try:
        df.to_excel(filename, index=False, sheet_name='Malaysia Stocks')
        print(f"{Fore.GREEN}Data exported to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error exporting to Excel: {e}{Style.RESET_ALL}")


def print_results(df, timeframe, title_suffix=""):
    """Print results with color coding"""
    if df is None or df.empty:
        print(f"{Fore.YELLOW}No valid Malaysia stock data found{Style.RESET_ALL}")
        return
    
    print("\n" + "="*120)
    print(f"{Fore.CYAN}Malaysia Stock Gains (KLSE) ({timeframe.upper()}) - {title_suffix}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    print("="*120)
    
    # Create display dataframe with colored values
    display_df = df.copy()
    display_df['Change $'] = display_df['Change $'].apply(color_price_change)
    display_df['Change %'] = display_df['Change %'].apply(color_percentage)
    
    print(display_df.to_string(index=False))
    print("="*120)
    
    # Print top gainers
    print(f"\n{Fore.CYAN}Top 5 Gainers (KLSE) ({timeframe.upper()}){Style.RESET_ALL}:")
    display_top = df.head(5).copy()
    display_top['Change $'] = display_top['Change $'].apply(color_price_change)
    display_top['Change %'] = display_top['Change %'].apply(color_percentage)
    print(display_top.to_string(index=False))


def main():
    parser = argparse.ArgumentParser(
        description='Advanced Malaysia Stock Tracker - Track KLSE stocks with color output, exports, and multiple timeframes'
    )
    parser.add_argument('--tickers', nargs='+', help='Stock tickers to track (use .KL suffix for Malaysia stocks)')
    parser.add_argument('--config', action='store_true', help='Save current tickers to config file')
    parser.add_argument('--timeframe', default='1d', choices=list(TIMEFRAMES.keys()),
                        help='Timeframe for gains (1h, 1d, 1w, 1m, 3m, 1y)')
    parser.add_argument('--min-gain', type=float, help='Filter: minimum gain percentage')
    parser.add_argument('--max-gain', type=float, help='Filter: maximum gain percentage')
    parser.add_argument('--min-price', type=float, help='Filter: minimum stock price')
    parser.add_argument('--max-price', type=float, help='Filter: maximum stock price')
    parser.add_argument('--export-csv', action='store_true', help='Export results to CSV')
    parser.add_argument('--export-xlsx', action='store_true', help='Export results to Excel')
    parser.add_argument('--output', help='Custom output filename for exports')
    parser.add_argument('--all-timeframes', action='store_true', help='Show results for all timeframes')
    
    args = parser.parse_args()
    
    # Determine tickers to use
    if args.tickers:
        tickers = args.tickers
        if args.config:
            save_config(tickers)
    else:
        tickers = load_config()
    
    # Handle showing all timeframes
    if args.all_timeframes:
        all_dfs = {}
        for tf in TIMEFRAMES.keys():
            print(f"\nFetching {tf} data...")
            df = calculate_gains(tickers, tf)
            if df is not None:
                all_dfs[tf] = df
                print_results(df, tf, title_suffix=f"Updated: ")
        
        # Export combined results if requested
        if args.export_csv or args.export_xlsx:
            # Combine all timeframes into one Excel file with multiple sheets
            if args.export_xlsx:
                filename = args.output or f"stocks_malaysia_all_timeframes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                try:
                    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                        for tf, df in all_dfs.items():
                            df.to_excel(writer, sheet_name=tf, index=False)
                    print(f"{Fore.GREEN}Combined data exported to {filename}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error exporting to Excel: {e}{Style.RESET_ALL}")
            if args.export_csv:
                print(f"{Fore.YELLOW}CSV export with --all-timeframes uses separate files for each timeframe{Style.RESET_ALL}")
                for tf, df in all_dfs.items():
                    filename = args.output or f"stocks_malaysia_{tf}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    export_to_csv(df, filename)
    else:
        # Single timeframe
        timeframe = args.timeframe
        print(f"\n{Fore.CYAN}Fetching {timeframe} data...{Style.RESET_ALL}")
        df = calculate_gains(tickers, timeframe)
        
        # Apply filters
        if any([args.min_gain, args.max_gain, args.min_price, args.max_price]):
            df = apply_filters(df, args.min_gain, args.max_gain, args.min_price, args.max_price)
            if df is not None:
                print(f"{Fore.CYAN}Applied filters - {len(df)} stocks match criteria{Style.RESET_ALL}")
        
        print_results(df, timeframe, title_suffix="Updated: ")
        
        # Export if requested
        if args.export_csv:
            export_to_csv(df, args.output)
        if args.export_xlsx:
            export_to_excel(df, args.output)


if __name__ == "__main__":
    main()
