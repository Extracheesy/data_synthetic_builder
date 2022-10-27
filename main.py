import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

import config

import build_synthetic_data

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def get_list_csv(path):
    all_files = os.listdir(path)
    csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
    return csv_files

def get_df_data_from_csv(path, lst_csv):
    path_backup = os.getcwd()
    os.chdir(path)
    print('directory: ', os.getcwd())
    lst_df = []
    for csvfile in lst_csv:
        df = pd.read_csv(csvfile)
        lst_df.append(df)
    os.chdir(path_backup)
    return lst_df

def get_price_symbol(path, symbol):
    path_backup = os.getcwd()
    os.chdir(path)
    print('directory: ', os.getcwd())
    lst_file = get_list_csv('./')
    for filename in lst_file:
        formatted_symbol = symbol.replace('/','_')
        if filename.startswith(formatted_symbol):
            df = pd.read_csv(filename)
            df_return = pd.DataFrame(columns=['time', 'close', 'buying_price', 'selling_price'])
            df_return['time'] = df['timestamp']
            df_return['close'] = df['close']
            os.chdir(path_backup)
            return df_return


def process_df(df):
    lst_symbol = df['symbol'].tolist()
    lst_symbol = list(dict.fromkeys(lst_symbol))

    df_cp = df.copy()
    for symbol in lst_symbol:
        df_filtered_buy = pd.DataFrame(columns= ['time', 'close', 'buying_price', 'selling_price'])
        df_filtered_sell = pd.DataFrame(columns=['time', 'close', 'buying_price', 'selling_price'])
        df_cp = df_cp.loc[df_cp['symbol'] == symbol]
        df_buy = df_cp.loc[df_cp['type'] == 'SOLD']
        df_filtered_buy['time'] = df_buy['time']
        df_filtered_buy['buying_price'] = df_buy['buying_price']
        df_sell = df_cp.loc[df_cp['type'] == 'SELL']
        df_filtered_sell['time'] = df_sell['time']
        df_filtered_sell['selling_price'] = df_sell['symbol_price']
        df_filtered = pd.concat([df_filtered_buy, df_filtered_sell])
        df_filtered = df_filtered.sort_values(by=['time'], ascending=True)
        df_filtered.reset_index(inplace=True)
        df_filtered.fillna(0, inplace=True)

        symbol = symbol.replace('/', '_')
        print('directory: ', os.getcwd())

        fig = px.scatter(df_filtered, x="time", y=["buying_price", "selling_price"])
        # fig.show()
        # fig.write_image('./result/' + symbol + "1.png")
        # fig.write_image("result/fig1.jpeg")
        fig.show()
        fig.write_html('./result/' + symbol + "1.html")
        # fig.to_image("result/fig1.jpeg")

        df_price_symbol = get_price_symbol('price',symbol)
        df_filtered = pd.concat([df_filtered, df_price_symbol])
        df_filtered = df_filtered.sort_values(by=['time'], ascending=True)
        df_filtered.reset_index(inplace=True)
        df_filtered.fillna(0, inplace=True)

        fig2 = px.scatter(df_filtered, x="time", y=["close", "buying_price", "selling_price"])
        fig2.show()
        fig2.write_html('./result/' + symbol + "2.html")
        # fig2.write_image("result/fig2.jpeg")


    print(lst_symbol)

if __name__ == '__main__':
    interval = ['2022-06-15', '2022-10-08']

    build_synthetic_data.build_synthetic_data(interval)

    if config.CRAG_ANALYSER:
        data_path = './data'
        lst_csv = get_list_csv(data_path)
        print(lst_csv)
        lst_df = get_df_data_from_csv(data_path, lst_csv)

        for df in lst_df:
            process_df(df)

    print_hi('PyCharm')