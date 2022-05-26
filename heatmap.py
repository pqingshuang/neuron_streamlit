
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
import py2neo
import influxdb
import datetime


# chosenDate = datetime.datetime(2021,4,7)
# endChosenDate = chosenDate + datetime.timedelta(days=1)
# chosenDateStr = datetime.datetime.strftime(chosenDate, "%Y-%m-%dT%H:%M:%SZ")
# endChosenDateStr = datetime.datetime.strftime(endChosenDate, "%Y-%m-%dT%H:%M:%SZ")

# neo4jdbname = 'neo4j'
# auth = ("neo4j", "test")
# name = 'neo4j'
# url = f"bolt://18.163.30.4:7691/{neo4jdbname}"
# graph = py2neo.Graph(url,name=name, auth=auth)
# equipname = graph.run("match (n)-[:hasPoint]->(p) where n.name='AHU' return p.name as p").to_data_frame()
# equipList = list(equipname['p'])
# equipList = sorted(equipList)
# client = influxdb.DataFrameClient('18.163.30.4', 8086, database='ArupDemo')

# df_list = []
# res= client.query(f"""select mean("value") from OTP where "FunctionType"='AHU_Water_Supply_Temperature' 
# and time>'{chosenDateStr}' and time<'{endChosenDateStr}' group by "EquipmentName", time(60m) """)
# res2= client.query(f"""select mean("value") from OTP where "FunctionType"='AHU_Water_Return_Temperature' 
# and time>'{chosenDateStr}' and time<'{endChosenDateStr}' group by "EquipmentName", time(60m) """)
# floor = []
# for equip in equipList:
#     if equip.rsplit("-",1)[0] not in floor:
#         floor.append(equip.rsplit("-",1)[0])
#         df = res[('OTP',(('EquipmentName', equip),))]
#         df2 = res2[('OTP',(('EquipmentName', equip),))]
#         if len(df) == 0 or len(df2) == 0 :
#             continue
#         df = df.rename(columns={"mean": equip})
#         dff = pd.concat([df,df2], axis=1)
#         df[equip] = dff.apply(lambda x: x['mean'] - x[equip], axis=1)
#         df_list.append(df)


# df_list2 = []
# res3= client.query(f"""select mean("value") from OTP where "FunctionType"='AHU_Return_Air_CO2_Concentration' 
# and time>'{chosenDateStr}' and time<'{endChosenDateStr}' group by "EquipmentName", time(60m) """)
# floor2 = []
# for equip in equipList:
#     if equip.rsplit("-",1)[0] not in floor2:
#         floor2.append(equip.rsplit("-",1)[0])
#         df = res3[('OTP',(('EquipmentName', equip),))]
#         if len(df) == 0:
#             continue
#         df = df.rename(columns={"mean": equip})
#         df_list2.append(df)


# result2 = pd.concat(df_list2, axis=1)

# dateIndex = [i.tz_localize(None) for i in list(result2.index)]

# floorList = [i.split('-')[1]+ 'F' for i in floor]

# result = pd.concat(df_list, axis=1)

# dateIndex = [i.tz_localize(None) for i in list(result.index)]


def Time(x: int):
    x = str(x)
    if len(x) < 2:
        x = "0" + x
    return x


st.set_page_config(page_title="Chiller Optimization", layout='wide')

st.title("Heatmap Analysis")
chosenDate = st.selectbox("Select time",pd.date_range(start=datetime.datetime(2021,4,12), end=datetime.datetime(2021,5,11), freq='1d')) 
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
    
    endChosenDate = chosenDate + datetime.timedelta(days=1)
    chosenDateStr = datetime.datetime.strftime(chosenDate, "%Y-%m-%dT%H:%M:%SZ")
    endChosenDateStr = datetime.datetime.strftime(endChosenDate, "%Y-%m-%dT%H:%M:%SZ")

    neo4jdbname = 'neo4j'
    auth = ("neo4j", "test")
    name = 'neo4j'
    url = f"bolt://18.163.30.4:7691/{neo4jdbname}"
    graph = py2neo.Graph(url,name=name, auth=auth)
    equipname = graph.run("match (n)-[:hasPoint]->(p) where n.name='AHU' return p.name as p").to_data_frame()
    equipList = list(equipname['p'])
    equipList = sorted(equipList)
    client = influxdb.DataFrameClient('18.163.30.4', 8086, database='ArupDemo')

    df_list = []
    res= client.query(f"""select mean("value") from OTP where "FunctionType"='AHU_Water_Supply_Temperature' 
    and time>'{chosenDateStr}' and time<'{endChosenDateStr}' group by "EquipmentName", time(60m) """)
    res2= client.query(f"""select mean("value") from OTP where "FunctionType"='AHU_Water_Return_Temperature' 
    and time>'{chosenDateStr}' and time<'{endChosenDateStr}' group by "EquipmentName", time(60m) """)
    floor = []
    for equip in equipList:
        if equip.rsplit("-",1)[0] not in floor:
            floor.append(equip.rsplit("-",1)[0])
            df = res[('OTP',(('EquipmentName', equip),))]
            df2 = res2[('OTP',(('EquipmentName', equip),))]
            if len(df) == 0 or len(df2) == 0 :
                continue
            df = df.rename(columns={"mean": equip})
            dff = pd.concat([df,df2], axis=1)
            df[equip] = dff.apply(lambda x: x['mean'] - x[equip], axis=1)
            df_list.append(df)


    df_list2 = []
    res3= client.query(f"""select mean("value") from OTP where "FunctionType"='AHU_Return_Air_CO2_Concentration' 
    and time>'{chosenDateStr}' and time<'{endChosenDateStr}' group by "EquipmentName", time(60m) """)
    floor2 = []
    for equip in equipList:
        if equip.rsplit("-",1)[0] not in floor2:
            floor2.append(equip.rsplit("-",1)[0])
            df = res3[('OTP',(('EquipmentName', equip),))]
            if len(df) == 0:
                continue
            df = df.rename(columns={"mean": equip})
            df_list2.append(df)


    result2 = pd.concat(df_list2, axis=1)

    dateIndex = [i.tz_localize(None) for i in list(result2.index)]

    floorList = [i.split('-')[1]+ 'F' for i in floor]

    result = pd.concat(df_list, axis=1)

    dateIndex = [i.tz_localize(None) for i in list(result.index)]
    with col1:
        uniform_data = np.random.rand(20, 24)
        fig = go.Figure(data=go.Heatmap(
                        z=result.T))
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
                ticktext=floorList,
                tickvals=[i for i in range(len(floorList))],
                tickmode="array",
                titlefont=dict(size=30),
            ), xaxis=dict(
                title_text="time",
                ticktext=dateIndex,
                tickvals=[i for i in range(len(dateIndex))],
                tickmode="array",
                titlefont=dict(size=30),
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        uniform_data = np.random.rand(20, 24)
        fig = go.Figure(data=go.Heatmap(
                        z=result2.T, colorscale='Viridis'))
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
                ticktext=floorList,
                tickvals=[i for i in range(len(floorList))],
                tickmode="array",
                titlefont=dict(size=30),
            ), xaxis=dict(
                title_text="time",
                ticktext=dateIndex,
                tickvals=[i for i in range(len(dateIndex))],
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
