import numpy as np
import pandas as pd
import gta_price
import gta_indicator


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


def donchian(tidm):
    '''Calculate Donchian trade signals.'''
    def remainder_zero(series, divisor):
        def increment_dividend(dividend, divisor):
            while dividend % divisor != 0:
                dividend += 1
            return dividend
        series = series.map(lambda x: increment_dividend(x, divisor))
        return series


    # Trade parameters.
    exchange = 'LSE'
    periods = [48, 24, 12, 6]  # System look back periods.
    position_size = 7500  # Position size in major currency unit.
    risk_pct = 0.2  # Percentage risk per trade.
    commission = 11.95  # Commission per trade.
    sduty = 0.5  # Stamp Duty percentage.
    
    # Import weekly prices.
    prices = gta_price.weekly(exchange, tidm)
    
    # Trade signals.
    signals = []
    for sys, period in enumerate(periods):

        # Donchian channel.
        dc = gta_indicator.donchian(prices, period)
        dc['sys'] = sys
        dc['period'] = period

        # Raw entry & exit signals.
        if sys == 0:
            dc['entry'] = np.where(dc.close > dc.upr, 1, 0)
        else:
            dc['entry'] = buy
        dc['exit'] = np.where(dc.close < dc.mid, 1, 0)

        # State variable.
        dc['state'] = 0
        for i in range(period, len(dc)):
            if dc.loc[dc.index[i], 'entry'] == 1 and dc.loc[dc.index[i - 1], 'state'] == 0:
                dc.loc[dc.index[i], 'state'] = 1
            elif dc.loc[dc.index[i], 'exit'] == 1:
                dc.loc[dc.index[i], 'state'] = 0
            else:
                dc.loc[dc.index[i], 'state'] = dc.loc[dc.index[i - 1], 'state']

        # Buy & sell signals.
        dc['buy'] = np.where(np.logical_and(dc.state == 1, dc.state.shift(periods=1) == 0), 1, 0)
        buy = dc.buy
        dc['sell'] = np.where(np.logical_and(dc.state == 0, dc.state.shift(periods=1) == 1), 1, 0)

        # Filter signals.
        if sys == 0:
            dc = pd.concat([dc[dc.buy == 1] , dc[dc.sell == 1]], axis=0)
        else:
            dc = dc[dc.sell == 1]
        signals.append(dc)

    # Trade list indexed by date.
    td = pd.concat(signals)
    td = td.sort_index()
    
    # Position size (buy side).
    td['volatility'] = np.where(td.buy == 1, abs((td.mid - td.close) / td.close), 0)
    td['risk_raw'] = np.where(td.buy == 1, ((position_size * risk_pct) / td.volatility), 0)
    td['shares_raw'] = np.where(td.buy == 1, (td.risk_raw / td.close).astype('int'), 0)
    td['shares'] = remainder_zero(td.shares_raw, len(periods)) # Adjust shares to be divisible by number of systems.
    td['risk'] = td.close * td.shares # Adjust risk amount for revised share count.

    # Position size (sell side).
    for index, row in td.iterrows():
        if row['buy'] == 1:
            shares = row['shares']
        else:
            td.at[index, 'shares'] = int(shares / 4)
    
    # Charges.
    td['charges'] = td.index.values
    td.charges = td.charges.shift()
    td.charges = np.where(td.index == td.charges.values, 0, commission)

    # Stamp duty.
    td['sduty'] = np.where(td.buy==1, ((sduty / 100) * td.close * td.shares), 0)

    # Cost to buy.
    td['cost'] = np.where(td.buy == 1, (td.risk + td.charges + td.sduty), 0)

    # Cost to sell.
    for index, row in td.iterrows():
        if row['buy'] == 1:
            cost = row['cost']
        else:
            td.at[index, 'cost'] = (cost / 4)
            
    # Returns.
    td['value'] = np.where(td.sell == 1, ((td.close * td.shares) - td.charges), 0)
    td['profit'] = np.where(td.sell == 1, td.value - td.cost, 0)
    td['pct'] = np.where(td.sell == 1, (td.profit / td.cost), 0)

    # Trade duration.
    td['days'] = 0
    for index, row in td.iterrows():
        if row['entry'] == 1:
            start_date = index
        else:
            td.at[index, 'days'] = index - start_date
    td.days = td.days.astype('timedelta64[D]')
    td.days = td.days.dt.days

    # Annual percentage return.
    td['annual'] = ((np.power(1 + td.profit / td.cost, (365 / td.days)) - 1))

    # Trade list indexed by trade.
    td = td.reset_index()
    td.insert(0, 'trade', td.state.cumsum())

    return td