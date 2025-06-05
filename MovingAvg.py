import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

df = yf.download('SPY')
print(df.head())

TICKER = 'POOL'
WINDOW = 20

def get_data():
    df = yf.download(TICKER)
    df.columns = df.columns.get_level_values(0)

    df['MovingAvg'] = df['Close'].rolling(WINDOW).mean()
    return df.dropna()


def add_strategy(df):
    df.columns = df.columns.get_level_values(0)
    df['Strategy'] = np.where(df['Close'] > df['MovingAvg'], 1, -1)
    df['Strategy'] = df['Strategy'].shift(1)
    return df

def test_strategy(df):
    df['asset_cumulative'] = np.cumprod(1 + df['Close'].pct_change()) -1
    df['strategy_cumulative'] = np.cumprod(1 + df['Close'].pct_change() * df['Strategy']) -1
    
    #plot the returns
    plt.plot(df['asset_cumulative'])
    plt.plot(df['strategy_cumulative'])
    plt.legend([f'{TICKER} Cumulative returns', f'{WINDOW} Moving Average Cumulative returns'])
    return df

def main():
    df = get_data()
    df = add_strategy(df)
    df = test_strategy(df)
    return df

main()