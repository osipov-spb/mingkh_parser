import pandas as pd
import numpy as np
from db import *


def get_mean_by_floors(floors):
    return get_mean(get_apart_by_floors(floors))


def get_mean(data_array):
    if len(data_array) == 0:
        return 0
    df = pd.DataFrame(data_array)  # read_csv('dram.csv')
    res = hampel(df)
    res = res[res != 'outlier']
    return int(pd.Series.mean(res).values[0])


def hampel(vals_orig):
    vals = vals_orig.copy()
    difference = np.abs(vals.median()-vals)
    median_abs_deviation = difference.median()
    threshold = 3 * median_abs_deviation
    outlier_idx = difference > threshold
    vals[outlier_idx] = 'outlier'
    return vals


def fill_zero_apart():
    i = 1
    while i < 30:
        update_apart(get_mean_by_floors(i), i)
        i = i + 1




