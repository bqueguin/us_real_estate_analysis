import pandas as pd
import streamlit as st
from streamlit.connections.sql_connection import SQLConnection
from datetime import timedelta


@st.cache_data(ttl=timedelta(weeks=1), show_spinner="Loading data from Snowpark DB...")
def get_data(_conn: SQLConnection) -> pd.DataFrame:
    df = _conn.query("""SELECT * FROM ZRHVI2020JUL WHERE "RegionType" = 'State'""", )
    return df


@st.cache_data(ttl=timedelta(weeks=1))
def get_region(df: pd.DataFrame, type: str = 'name') -> list[str]:
    if type == 'name':
        return list(df["Region Name"].unique())
    elif type == 'id':
        return list(df["RegionId"].unique())


@st.cache_data(ttl=timedelta(weeks=1))
def get_indicator(df: pd.DataFrame, type: str = 'name') -> list[str]:
    if type == 'name':
        return list(df["Indicator Name"].unique())
    elif type == 'id':
        return list(df["Indicator"].unique())


def filter_df(df: pd.DataFrame, state_list: list[str], indicator: str):
    filter = (df['Indicator Name'] == indicator) & (df['Region Name'].isin(state_list))
    df_filter = df.loc[filter, ['Date', 'Region Name', 'Value']].drop_duplicates()
    df_pivot = df_filter.pivot(columns='Region Name', values='Value', index='Date')
    return df_pivot
