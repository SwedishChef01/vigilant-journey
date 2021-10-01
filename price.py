import pandas as pd


def weekly_close(exchange, tidm, start_date, end_date):
    """Generate weekly closing prices from SharePad csv file of daily prices."""
    df = pd.read_csv(
        f"{exchange}_{tidm}_prices.csv",
        header=0,
        names=["date", "close"],
        index_col=0,
        usecols=[0, 4],
        parse_dates=True,
        dayfirst=True,
    )
    df = df.sort_index()
    df = df.resample("W-FRI").agg(dict(close="last"))
    df = df / 100
    df = df.loc[start_date:end_date]
    return df
