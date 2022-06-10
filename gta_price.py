import pandas as pd


def weekly(exchange, tidm):
    '''Weekly closing prices from SharePad csv file of daily prices.'''
    df = pd.read_csv(
        f'{exchange}_{tidm}_prices.csv',
        header=0,
        names=['date', 'open', 'high', 'low', 'close'],
        index_col=0,
        usecols=[0, 1, 2, 3, 4],
        parse_dates=True,
        dayfirst=True,
    )
    df = df.sort_index()
    functions = dict(open='first', high='max', low='min', close='last')
    df = df.resample('W-FRI').agg(functions)
    df = df / 100
    return df
