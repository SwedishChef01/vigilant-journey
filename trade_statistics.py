import numpy as np
import pandas as pd


def summary(instrument_id, indicator, position_size, trade_list):
    """Generate trade performance summary statistcs."""
    df = pd.Series(dtype="string")

    # Calculations.
    start_date = indicator[indicator.notnull()].index[0]
    end_date = indicator.index[-1]
    analysis_years = (end_date - start_date) / np.timedelta64(1, "Y")
    analysis_days = (end_date - start_date) / np.timedelta64(1, "D")
    annual_pct = (((position_size + trade_list.cum_profit[-1]) / position_size) ** (365 / analysis_days) - 1) * 100
    total_trades = len(trade_list.index)
    winning_trades = len(trade_list[trade_list.chg_pct > 0])
    losing_trades = len(trade_list[trade_list.chg_pct < 0])

    # Tradable Instrument Display Mnemonic
    df["TIDM"] = instrument_id

    # Analysis period.
    df["Start Date"] = start_date.strftime("%Y-%m-%d")
    df["End Date"] = end_date.strftime("%Y-%m-%d")
    df["Analysis Years"] = "{0:.1f}".format(analysis_years)

    # Trade performance.
    df["Position Size"] = "{0:,.2f}".format(position_size)
    df["Net Profit"] = "{0:,.2f}".format(trade_list.loc[trade_list.index[-1], "cum_profit"])
    df["Annual %"] = "{0:.1f}".format(annual_pct)
    df["Charges"] = "{0:,.2f}".format(trade_list.charges.sum())
    df["Stamp Duty"] = "{0:,.2f}".format(trade_list.stamp_duty.sum())

    # Overall trade statistics.
    df["Total Trades"] = "{0:.0f}".format(total_trades)
    df["Winning Trades"] = "{0:.0f}".format(winning_trades)
    df["Losing Trades"] = "{0:.0f}".format(losing_trades)
    df["Winning %"] = "{0:.1f}".format((winning_trades / total_trades) * 100)
    df["Trades per Year"] = "{0:.1f}".format(total_trades / analysis_years)

    # Average trade statistics.
    df["Average Profit %"] = "{0:.1f}".format(trade_list.chg_pct.mean())
    df["Average Profit"] = "{0:,.2f}".format(trade_list.profit.mean())
    df["Average Weeks"] = "{0:.1f}".format(trade_list.weeks.mean())

    # Winning trade statistics.
    df["Average Winning Profit %"] = "{0:.1f}".format(trade_list.chg_pct[trade_list.chg_pct > 0].mean())
    df["Average Winning Profit"] = "{0:,.2f}".format(trade_list.profit[trade_list.profit > 0].mean())
    df["Average Winning Weeks"] = "{0:.1f}".format(trade_list.weeks[trade_list.chg_pct > 0].mean())

    # Losing trade statistics.
    df["Average Losing Profit %"] = "{0:.1f}".format(trade_list.chg_pct[trade_list.chg_pct < 0].mean())
    df["Average Losing Profit"] = "{0:,.2f}".format(trade_list.profit[trade_list.profit < 0].mean())
    df["Average Losing Weeks"] = "{0:.1f}".format(trade_list.weeks[trade_list.chg_pct < 0].mean())
    return df