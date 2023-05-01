import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium

from config import logger
from header import set_page_config
from load_data import get_data, get_region, get_indicator, filter_df

logger.debug("New run of app.py")
set_page_config()
DB_CONN = st.experimental_connection('snowpark', type='sql', url="snowflake://brunoqueguiner:5CmCSaMVgOtfPO4e0yL7@qo18497.eu-west-2.aws/REAL_ESTATE_DATA_ATLAS/REALESTATE")


def main() -> None:
    st.title("Welcome to the awesome app")
    df = get_data(DB_CONN)
    st.dataframe(df)
    region_name = get_region(df)
    region_id = get_region(df, type="id")
    indicator_name = get_indicator(df)
    selected_states = st.multiselect("States", region_name, ['New York', 'Nevada'])
    selected_indicator = st.selectbox("Indicator", indicator_name)

    df_filter = filter_df(df, selected_states, selected_indicator)
    st.dataframe(df_filter)
    st.line_chart(df_filter, y=selected_states)


if __name__ == '__main__':
    main()
