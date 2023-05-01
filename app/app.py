import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
import pandas as pd
import json

from config import logger
from header import set_page_config
from load_data import get_data, get_region, get_indicator, filter_df

logger.debug("New run of app.py")
set_page_config()
DB_CONN = st.experimental_connection('snowpark', type='sql',
                                     url="snowflake://brunoqueguiner:5CmCSaMVgOtfPO4e0yL7@qo18497.eu-west-2.aws/REAL_ESTATE_DATA_ATLAS/REALESTATE")


def main() -> None:
    st.title("Welcome to the awesome app")
    tab1, tab2 = st.tabs(["Line Chart", "Map"])
    with tab1:
        df = get_data(DB_CONN)
        region_name = get_region(df)
        region_id = get_region(df, type="id")
        indicator_name = get_indicator(df)
        selected_states = st.multiselect("States", region_name, ['New York', 'Nevada'])
        selected_indicator = st.selectbox("Indicator", indicator_name)

        df_filter = filter_df(df, selected_states, selected_indicator)
        st.line_chart(df_filter, y=selected_states)

    with tab2:
        # # Création d'un DataFrame avec les valeurs pour chaque État
        # data = {'state': ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
        #                   'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        #                   'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
        #                   'VA', 'WA', 'WV', 'WI', 'WY'],
        #         'value': [5, 3, 10, 7, 25, 14, 8, 2, 18, 12, 1, 2, 13, 8, 4, 5, 6, 9, 3, 7, 12, 15, 7, 4, 8, 1, 3, 5, 2,
        #                   9, 20, 14, 3, 12, 7, 6, 15, 3, 8, 1, 2, 9, 4, 11, 6, 13, 8, 5, 7, 10]}
        # df = pd.DataFrame(data)

        # Création de la carte
        m = folium.Map(location=[37, -102], zoom_start=4)

        us_states_json = json.load(open('../data/us-states.json'))
        # Ajout de la couche GeoJSON pour les États-Unis
        folium.GeoJson(us_states_json, name='geojson').add_to(m)

        folium.Choropleth(
            geo_data=us_states_json,  # json
            name='choropleth',
            data=df,
            columns=['Region Name', 'Value'],  # columns to work on
            key_on='feature.properties.name',
            fill_color='YlGnBu',  # I passed colors Yellow,Green,Blue
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Real Estate KPI"
        ).add_to(m)

        # Affichage de la carte
        st_folium(m)


if __name__ == '__main__':
    main()
