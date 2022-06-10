import numpy as np
import pandas as pd


def remainder_zero(series, divisor):
    '''Increment number until remainder is zero.'''

    def increment_dividend(dividend, divisor):
        '''Increment dividend while remainder does not equal zero.'''
        while dividend % divisor != 0:
            dividend += 1
        return dividend

    series = series.map(lambda x: increment_dividend(x, divisor))
    return series
