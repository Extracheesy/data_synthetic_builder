import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import config

def plot_df_sinus(df, column_name):
    # fig = px.scatter(df, x="time", y=["sinus"])
    fig = px.line(df, x="time", y=[column_name])

    fig.update_layout(
        autosize=False,
        width=800,
        height=800,
        # margin=dict(
        #     l=50,
        #     r=50,
        #     b=100,
        #     t=100,
        #     pad=4
        # ),
        paper_bgcolor="LightSteelBlue",
    )

    # fig.show()

    fig.write_html(config.OUTPUT_DIRECTORY + column_name + ".html")
    # fig.to_image("result/fig1.jpeg")


def plot_ohlc(df, filename):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    ))

    fig.write_html(config.OUTPUT_DIRECTORY + filename + ".html")