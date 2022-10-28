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
    df_synthetic = pd.DataFrame(columns=['time', 'sinus_1', 'sinus_2', 'linear_up', 'linear_down'])

    df_synthetic = fill_df_date(df_synthetic, interval[0], interval[1])

    df_synthetic = fill_df_sinusoid(df_synthetic, 'sinus_1', config.sinus_1_amplitude, config.sinus_1_freq, 0, config.sinus_1_height)

    freq = 6.3 / len(df_synthetic)
    df_synthetic = fill_df_sinusoid(df_synthetic, 'sinus_2', config.sinus_2_amplitude, freq, 0, config.sinus_2_height)

    df_synthetic = fill_df_sinusoid(df_synthetic, 'sinus_3', config.sinus_3_amplitude, config.sinus_3_freq, 0, config.sinus_3_height)

    freq = 6.3 / len(df_synthetic) / 2
    df_synthetic = fill_df_sinusoid(df_synthetic, 'sinus_4', config.sinus_4_amplitude, freq, 0, config.sinus_4_height)

    freq = 6.3 / len(df_synthetic) / 2
    df_synthetic = fill_df_sinusoid(df_synthetic, 'sinus_5', config.sinus_5_amplitude, freq, 0, config.sinus_5_height)
    df_synthetic['sinus_5'] = 1 - df_synthetic['sinus_5']

    df_synthetic = fill_df_linear(df_synthetic, 'linear_up', config.a, config.b)

    df_synthetic = fill_df_linear(df_synthetic, 'linear_down', -config.a, config.b)

    plot_data.plot_df_sinus(df_synthetic, 'sinus_1')
    plot_data.plot_df_sinus(df_synthetic, 'sinus_2')
    plot_data.plot_df_sinus(df_synthetic, 'sinus_3')
    plot_data.plot_df_sinus(df_synthetic, 'sinus_4')
    plot_data.plot_df_sinus(df_synthetic, 'sinus_5')
    plot_data.plot_df_sinus(df_synthetic, 'linear_up')
    plot_data.plot_df_sinus(df_synthetic, 'linear_down')

    df_ohlv = pd.DataFrame(columns=['time', 'close'])

    for type in config.TYPE:
        if type == 'SINGLE_SINUS_1_FLAT':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_1'] + 10
        if type == 'SINGLE_SINUS_2_FLAT':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_2'] + 10
        if type == 'MIXED_SINUS_FLAT':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_2'] + df_synthetic['sinus_3'] + 10
        if type == 'SINGLE_SINUS_1_UP':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_1'] + df_synthetic['linear_up'] + 10
        if type == 'SINGLE_SINUS_2_UP':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_2'] + df_synthetic['linear_up'] + 10
        if type == 'MIXED_SINUS_UP':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_2'] + df_synthetic['sinus_3'] + df_synthetic['linear_up'] + 10
        if type == 'SINGLE_SINUS_1_DOWN':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_1'] + df_synthetic['linear_down'] + 10
        if type == 'SINGLE_SINUS_2_DOWN':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_2'] + df_synthetic['linear_down'] + 10
        if type == 'MIXED_SINUS_DOWN':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_2'] + df_synthetic['sinus_3'] + df_synthetic['linear_down'] + 10
        if type == 'MIXED_SINUS_UP_DOWN':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_3'] + df_synthetic['sinus_4'] + 10
        if type == 'MIXED_SINUS_DOWN_UP':
            df_ohlv['time'] = df_synthetic['time']
            df_ohlv['close'] = df_synthetic['sinus_3'] + df_synthetic['sinus_5'] + 10


        fill_ohlv(df_ohlv)
        filename = 'ohlc_no_noise_' + type
        plot_data.plot_ohlc(df_ohlv, filename)
        df_ohlv.to_csv(config.OUTPUT_DIRECTORY + filename + '.csv')

        amplitude = 0.1
        df_ohlv = add_df_ohlv_noise(df_ohlv, amplitude)
        filename = 'ohlc_with_noise_' + type
        plot_data.plot_ohlc(df_ohlv, filename)
        df_ohlv.to_csv(config.OUTPUT_DIRECTORY + filename + '.csv')
