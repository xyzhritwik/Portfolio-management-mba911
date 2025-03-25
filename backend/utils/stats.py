import numpy as np
import pandas as pd

def calculate_portfolio_stats(df):
    df = df.dropna(subset=['Buy Price', 'Current Price', 'Quantity'])

    df['Investment'] = df['Buy Price'] * df['Quantity']
    df['Current Value'] = df['Current Price'] * df['Quantity']
    df['Returns'] = (df['Current Price'] - df['Buy Price']) / df['Buy Price']

    total_investment = df['Investment'].sum()
    total_value = df['Current Value'].sum()
    cagr = ((total_value / total_investment) ** (1/1)) - 1

    portfolio_return = df['Returns'].mean()
    market_return = 0.10
    beta = 1.1
    alpha = portfolio_return - (0.03 + beta * (market_return - 0.03))
    sharpe = (portfolio_return - 0.03) / df['Returns'].std()
    downside_returns = df[df['Returns'] < 0]['Returns']
    sortino = (portfolio_return - 0.03) / downside_returns.std() if not downside_returns.empty else np.nan

    return {
        "cagr": round(cagr * 100, 2),
        "alpha": round(alpha, 3),
        "beta": round(beta, 3),
        "sharpe": round(sharpe, 3),
        "sortino": round(sortino, 3)
    }