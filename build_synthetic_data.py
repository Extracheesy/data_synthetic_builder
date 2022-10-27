import pandas as pd
import numpy as np
import config

import plot_data

def fill_df_date(df, start_date, end_date):
    lst_index_date = pd.date_range(start=start_date, end=end_date, freq='1H')
    # df_date = pd.date_range(start=start_date, periods=len(y), freq='1H')
    df['time'] = lst_index_date

    return df

def fill_df_sinusoid(df, column, amplitude=1, frequency=.1, phi=0, height = 0):
    x = np.arange(len(df))
    y = amplitude*np.sin(frequency*x+phi)+height
    df[column] = y
    return df

def fill_df_constant(amplitude, length):
    return amplitude * np.ones(length)

def fill_df_linear(df, column, a, b):
    x = np.arange(len(df))
    y = a*x + b
    df[column] = y
    return df

def fill_ohlv(df):
    df['open'] = df['close'].shift()
    df['high'] = df['close'] + 0.1
    df['low'] = df['open'] - 0.1

def add_noise(y, amplitude):
    return np.array(y+amplitude*np.random.randn(len(y)))

def add_df_ohlv_noise(df, amplitude):
    df['close'] = np.array(df['close'] + abs(amplitude * np.random.randn(len(df))))
    df['open'] = df['close'].shift()

    df['high'] = np.array(df['close'] + abs(amplitude * np.random.randn(len(df))))
    df['low'] = np.array(df['open'] - abs(amplitude * np.random.randn(len(df))))

    df['high'] = np.where(df['close'] < df['open'],
                          df['open'] + df['open'] - df['low'],
                          df['high'])
    df['low'] = np.where(df['close'] < df['open'],
                         df['close'] + df['close'] - df['high'],
                         df['low'])

    return df

def build_synthetic_data(interval):
    df_synthetic = pd.DataFrame(columns=['time', 'sinus_1', 'sinus_2', 'linear'])

    df_synthetic = fill_df_date(df_synthetic, interval[0], interval[1])

    freq = 10 / len(df_synthetic)
    # freq = 10 / len(df_synthetic) / 3.2
    df_synthetic = fill_df_sinusoid(df_synthetic, 'sinus_1', config.sinus_1_amplitude, freq, 0, config.sinus_1_height)

    df_synthetic = fill_df_sinusoid(df_synthetic, 'sinus_2', config.sinus_2_amplitude, config.sinus_2_freq, 0, config.sinus_2_height)

    df_synthetic = fill_df_linear(df_synthetic, 'linear', config.a, config.b)
    if config.NO_LINEAR:
        df_synthetic['linear'] = 0

    df_ohlv = pd.DataFrame(columns=['time', 'close'])
    for columns in df_synthetic.columns.tolist():
        if columns == 'time':
            df_ohlv['time'] = df_synthetic['time']
        else:
            df_ohlv.fillna(0, inplace=True)
            df_ohlv['close'] = df_ohlv['close'] + df_synthetic[columns]

    plot_data.plot_df_sinus(df_synthetic, 'sinus_1')
    plot_data.plot_df_sinus(df_synthetic, 'sinus_2')
    plot_data.plot_df_sinus(df_synthetic, 'linear')
    plot_data.plot_df_sinus(df_ohlv, 'close')

    fill_ohlv(df_ohlv)
    filename = 'ohlc_no_noise'
    plot_data.plot_ohlc(df_ohlv, filename)
    df_ohlv.to_csv(config.OUTPUT_DIRECTORY + 'ohlc_no_noise.csv')

    amplitude = 0.1
    df_ohlv = add_df_ohlv_noise(df_ohlv, amplitude)
    filename = 'ohlc_with_noise'
    plot_data.plot_ohlc(df_ohlv, filename)
    df_ohlv.to_csv(config.OUTPUT_DIRECTORY + 'ohlc_with_noise.csv')
