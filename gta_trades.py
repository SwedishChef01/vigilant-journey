import numpy as np
import pandas as pd


def trade_list(close, entry_flag, exit_flag):
    '''Generate trade list'''
    frame = pd.concat([close, entry_flag, exit_flag], axis=1)
    frame.columns = ['close', 'entry_flag', 'exit_flag']
    entry_price = frame.close[frame.entry_flag == 1]
    exit_price = frame.close[frame.exit_flag == 1]
    entry_count = len(entry_price)
    exit_count = len(exit_price)
    if exit_count != entry_count:
        last_price = pd.Series(data=frame.close[-1:], index=frame.index[-1:])
        exit_price = exit_price.append(last_price)
        exit_count = len(exit_price)
    df = pd.DataFrame(columns=['entry_price', 'exit_date', 'exit_price'])
    df.entry_price = entry_price
    df.exit_date = exit_price.index
    df.exit_price = exit_price.values
    return df
