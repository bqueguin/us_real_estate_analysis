import pandas as pd
import streamlit as st
from streamlit.connections.sql_connection import SQLConnection
from datetime import timedelta, date


@st.cache_data(ttl=timedelta(weeks=1), show_spinner="Loading data from Snowpark DB...")
def get_data(_conn: SQLConnection) -> pd.DataFrame:
    df = _conn.query("""SELECT * FROM ZRHVI2020JUL 
                        WHERE "RegionType" = 'State' AND "Region Name" != 'District of Columbia' """)
    df["year_datetime"] = pd.to_datetime(df["Date"])
    df["year"] = df["year_datetime"].dt.year
    return df


@st.cache_data(ttl=timedelta(weeks=1))
def get_region(df: pd.DataFrame, output_type: str = 'name') -> list[str]:
    if output_type == 'name':
        return list(df["Region Name"].unique())
    elif output_type == 'id':
        return list(df["RegionId"].unique())


@st.cache_data(ttl=timedelta(weeks=1))
def get_indicator(df: pd.DataFrame, output_type: str = 'name') -> list[str]:
    if output_type == 'name':
        return list(df["Indicator Name"].unique())
    elif output_type == 'id':
        return list(df["Indicator"].unique())


@st.cache_data(ttl=timedelta(weeks=1))
def filter_df(df: pd.DataFrame, state_list: list[str], indicator: str):
    df_filtered = df.loc[(df['Indicator Name'] == indicator) & (df['Region Name'].isin(state_list)),
                         ['Date', 'Region Name', 'Value']].drop_duplicates()
    df_pivot = df_filtered.pivot(columns='Region Name', values='Value', index='Date')
    return df_pivot


@st.cache_data(ttl=timedelta(weeks=1))
def get_dates(df: pd.DataFrame) -> list[date]:
    return list(sorted(df["Date"].unique()))


@st.cache_data(ttl=timedelta(weeks=1))
def get_value_bins(df: pd.DataFrame, indicator_name: str, nb_bins: int = 15) -> list[int]:
    min_value = int(min(df.loc[df['Indicator Name'] == indicator_name, 'Value']))
    max_value = int(max(df.loc[df['Indicator Name'] == indicator_name, 'Value'])) + 1
    value_range = max_value - min_value
    value_step = int(value_range / (nb_bins - 1)) + 1
    value_list = [min_value]
    for i in range(1, nb_bins):
        value_list.append(min_value + i * value_step)
    return value_list
