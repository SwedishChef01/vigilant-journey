import numpy as np
import pandas as pd


def rsi(close, period):
    """Relative Strength Index (RSI)."""
    df = pd.DataFrame(close)
    df["chg"] = df.close.diff()
    df["gain"] = df.chg.clip(lower=0)
    df["loss"] = df.chg.clip(upper=0).abs()
    df["avg_gain"] = np.nan
    df["avg_loss"] = np.nan
    df.avg_gain.iloc[period] = df.gain[0:period].sum() / period
    df.avg_loss.iloc[period] = df.loss[0:period].sum() / period

    for i in range(period + 1, df.shape[0]):
        df["avg_gain"].iloc[i] = (
            df["avg_gain"].iloc[i - 1] * (period - 1) + df["gain"].iloc[i]
        ) / period

        df["avg_loss"].iloc[i] = (
            df["avg_loss"].iloc[i - 1] * (period - 1) + df["loss"].iloc[i]
        ) / period

    df["rs"] = df.avg_gain / df.avg_loss
    df["rsi"] = 100 - 100 / (1 + df.rs)
    return df.rsi
