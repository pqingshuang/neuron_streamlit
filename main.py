
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from typing import Callable, Any, Union, Tuple
import random

st.set_page_config(page_title="Chiller Optimization",layout='wide')
st.title("Chiller Optimization Sequencing")


def modelFunction(cl: Union[float, str], wb: Union[float, str]) -> Tuple[int, pd.DataFrame]:
    try:
        cl = float(cl)
        wb = float(wb)
    except ValueError:
        pass
    if isinstance(cl, str) and isinstance(wb, str):
        return 0, pd.DataFrame(columns=["Name", "FLA", "SetPoint"])
    ls = [['CH0'+ str(i+1), str(random.randint(60, 90)) + '%', str(random.randint(12, 18)/2)] for i in range(5)]
    return 5, pd.DataFrame(ls, columns=["Name", "FLA", "SetPoint"])

@st.cache
def get_data():
    path = r'./visual.csv'
    return pd.read_csv(path)

visual = get_data()


def _set_block_container_style(
    max_width: int = 1200,
    max_width_100_percent: bool = False,
    padding_top: int = 1,
    padding_right: int = 1,
    padding_left: int = 1,
    padding_bottom: int = 1,
    ):
    if max_width_100_percent:
        max_width_str = f"max-width: 100%;"
    else:
        max_width_str = f"max-width: {max_width}px;"
    
    background = ' background-color: #0c0080; '
    styl = f"""
    <style>
        .reportview-container .main .block-container{{
            {max_width_str}
            padding-top: {padding_top}rem;
            padding-right: {padding_right}rem;
            padding-left: {padding_left}rem;
            padding-bottom: {padding_bottom}rem;
        }}
        .st-at {background}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)

_set_block_container_style()


ms = visual['cnt'].values
ms[ms>=15] = 15
ms[ms<=10] = 10
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=visual['CL_bin'],
    y=visual['WB_bin'],
    mode="markers",
    marker=go.scatter.Marker(
        size=ms,
        color=visual['Total_kWh mean'],
        opacity=0.6,
        showscale=True,
        colorscale="Viridis",
        colorbar={'title':'EN Mean, kW', 'title_font':dict(color='#000000'), 'tickfont': dict(color='#000000')}
    ),
    hovertemplate = '<i>CL_bin: %{x}<br>WB_bin: %{y}</i><br><br>%{text}',
    text = visual['text'].values,
    showlegend = False
))

fig.update_xaxes(title_text = 'Cooling Load', title_font=dict(color='#000000'), ticks="inside", color='#000000',gridcolor = '#46495C')
fig.update_yaxes(title_text = 'Wet Bulb Temp',title_font=dict(color='#000000'), ticks="inside", color='#000000',gridcolor = '#46495C')

fig.update_layout(
    hoverlabel_align = 'left',
    autosize=True,
    width=1000,
    height=800,
    plot_bgcolor='#1a1e2e',
    paper_bgcolor='rgba(0,0,0,0)',
    title_text = "Mode Table - UT2",
    title_font=dict(color='#000000'),
    yaxis=dict(type='category',categoryorder='category ascending'),
        xaxis=dict(type='category',categoryarray=[
                                 '(700.0, 800.0]',
                                 '(800.0, 900.0]',
                                 '(900.0, 1000.0]',
                                 '(1000.0, 1100.0]',
                                 '(1100.0, 1200.0]',
                                 '(1200.0, 1300.0]',
                                 '(1300.0, 1400.0]',
                                 '(1400.0, 1500.0]',
                                 '(1500.0, 1600.0]',
                                 '(1600.0, 1700.0]',
                                 '(1700.0, 1800.0]'
                   ]),
)

def onCLInputCallback(*args, **kwargs):
    return 

def onWBInputCallback(*args, **kwargs):
    return 

def onClickCallback(*args, modelFunction: Callable[[float, float], Any] = modelFunction, **kwargs):
    try:
        cooling_load = float(kwargs.get("cooling_load"))
        wet_bulb = float(kwargs.get("wet_bulb"))
    except ValueError:
        if kwargs.get("cooling_load") == "" and kwargs.get("wet_bulb") == "":
            html_str = '<div style="color: Red">Please input cooling load and wet bulb temperature</div>'
            st.markdown(html_str, unsafe_allow_html=True)
            return 
        else:
            html_str = '<div style="color: Red">Please input numbers</div>'
            st.markdown(html_str, unsafe_allow_html=True)
            return 
    
    return modelFunction(cooling_load, wet_bulb)
    

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Real-time Settings")
    with st.form(key="parameters"):
        cooling_load = st.text_input("Cooling Load", value="", max_chars=6)
        wet_bulb = st.text_input("Wet Bulb Temp", value="", max_chars=4)
        submit_button = st.form_submit_button("Submit", 
            on_click=onClickCallback, 
            kwargs={'cooling_load': cooling_load, "wet_bulb": wet_bulb})
    st.header("Recommendation")
    if submit_button:
        st.subheader(f"""Today's Recommendation: 
                Number of Chiller To Operate: {modelFunction(cooling_load, wet_bulb)[0]}""")
        st.dataframe(modelFunction(cooling_load, wet_bulb)[1], width=1800)
    else:
        
        st.subheader("No data")
        st.dataframe(modelFunction(cooling_load, wet_bulb)[1], width=1800)




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

