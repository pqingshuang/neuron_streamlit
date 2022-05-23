
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from typing import Callable, Any, Union, Tuple
import random
import numpy as np


def Time(x: int):
    x = str(x)
    if len(x) < 2:
        x = "0" + x
    return x


st.set_page_config(page_title="Chiller Optimization", layout='wide')

col1, col2 = st.columns([1, 1])

if False:
    sns.set_theme()
    with col1:
        np.random.seed(0)
        uniform_data = np.random.rand(20, 20)
        fig = plt.figure(figsize=(10, 8))
        plt.title("Chilled Water Supply Temperature Distribution Heatmap")
        ax = sns.heatmap(uniform_data, cmap="YlGnBu")
        st.pyplot(fig)

    with col2:
        np.random.seed(1)
        uniform_data = np.random.rand(20, 20)
        fig = plt.figure(figsize=(10, 8))
        plt.title("CO2 Concentration Distribution heatmap")
        ax = sns.heatmap(uniform_data)
        st.pyplot(fig)

else:
    with col1:
        uniform_data = np.random.rand(20, 24)
        fig = go.Figure(data=go.Heatmap(
                        z=uniform_data))
        fig.update_layout(
            title={
                'text': "Chilled Water Supply Temperature Distribution Heatmap",
                'y': 0.9,  # new
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'  # new
            },
            autosize=False,
            width=500,
            height=800,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ),
            paper_bgcolor="Black",
            yaxis=dict(
                title_text="Floor",
                ticktext=[str(i)+"/F" for i in range(20)],
                tickvals=[i for i in range(20)],
                tickmode="array",
                titlefont=dict(size=30),
            ), xaxis=dict(
                title_text="time",
                ticktext=[f"{Time(i)}:00" for i in range(24)],
                tickvals=[i for i in range(24)],
                tickmode="array",
                titlefont=dict(size=30),
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        uniform_data = np.random.rand(20, 24)
        fig = go.Figure(data=go.Heatmap(
                        z=uniform_data, colorscale='Viridis'))
        fig.update_layout(
            title={
                'text': "CO2 Concentration Distribution heatmap",
                'y': 0.9,  # new
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'  # new
            },
            autosize=False,
            width=500,
            height=800,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ),
            paper_bgcolor="Black",

            yaxis=dict(
                title_text="Floor",
                ticktext=[str(i)+"/F" for i in range(20)],
                tickvals=[i for i in range(20)],
                tickmode="array",
                titlefont=dict(size=30),
            ), xaxis=dict(
                title_text="time",
                ticktext=[f"{Time(i)}:00" for i in range(24)],
                tickvals=[i for i in range(24)],
                tickmode="array",
                titlefont=dict(size=30),
            )
        )
        st.plotly_chart(fig, use_container_width=True)
# if submit_button:
#     print(cooling_load, wet_bulb)

# st.plotly_chart(fig, height = 1000, width=1000)

# @st.cache
# def get_data():
#     path = r'C:\Users\marcu\Downloads\latestSwireTest\newDataRules\RawData (AHU).xlsx'
#     return pd.read_excel(path)

# @st.cache
# def get_data2():
#     path = r'C:\Users\marcu\Downloads\latestSwireTest\DataRules\AHU_CO2_data.xlsx'
#     df = pd.read_excel(path)
#     df['Timestamp'] = pd.to_datetime(df['Timestamp'])
#     df = df.reindex(sorted(df.columns), axis=1)
#     df.index = df['Timestamp']
#     del df['Timestamp']
#     return df

# df = get_data()
# df2 = get_data2()

# st.title("Raw AHU Supply Temp and Return Temp data")

# col1 = st.columns(1)


# Equipment = st.selectbox("Equipment", df["Sort"].unique().tolist(), index=0)
# Temp = st.selectbox("AirTemp", df["name"][df['Sort'] == Equipment].unique().tolist(), index=0)

# st.dataframe(df.head())

# df_final=df[df["name"]==Temp]

# st.line_chart(df_final['FloatVALUE'])


# fig, ax = plt.subplots()
# sns.heatmap(df2.T , ax=ax)
# st.write(fig)

# HtmlFile = open("index.html", 'r', encoding='utf-8')
# source_code = HtmlFile.read()
# components.html(source_code, height=1000, width=1000)


# col1, col2, col3 = st.columns(3)

# with col1:
#     components.html(source_code, height=800, width=800)

# with col2:
#     components.html(source_code, height=800, width=800)

# with col3:
#     components.html(source_code, height=800, width=800)
