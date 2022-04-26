import numpy as np
import pandas as pd


def state_signal(entry_signal, exit_signal, period):
    '''Calculate trade state signals.'''
    df = pd.concat([entry_signal, exit_signal], axis=1)
    df.columns = ['entry', 'exit']
    df['state'] = 0
    for i in range(period, len(df)):
        if df.loc[df.index[i], 'entry'] == 1 \
        and df.loc[df.index[i - 1], 'state'] == 0:
            df.loc[df.index[i], 'state'] = 1
        elif df.loc[df.index[i], 'exit'] == 1:
            df.loc[df.index[i], 'state'] = 0
        else:
            df.loc[df.index[i], 'state'] = df.loc[df.index[i - 1], 'state']
    return df.state
