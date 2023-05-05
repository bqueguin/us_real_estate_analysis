import json

import folium
import streamlit as st
from streamlit_folium import st_folium

from config import logger
from header import display_footer, set_page_config
from load_data import (filter_df, get_data, get_dates, get_indicator,
                       get_region, get_value_bins)

logger.debug("New run of app.py")
set_page_config()
DB_CONN = st.experimental_connection('real_estate_db', type='sql')


def main() -> None:

    # GET SOURCE DATA
    df = get_data(DB_CONN)
    region_name = get_region(df)
    indicator_name = get_indicator(df)
    dates = get_dates(df)
    default_date = max(dates)

    st.title("Zillow Home Value Index Analysis")
    tab1, tab2 = st.tabs(["🌎 Map", "📈 Line Chart"])

    with tab1:
        col1_1, _ = st.columns([1, 3])
        selected_indicator_map = col1_1.selectbox("Indicator", indicator_name, key='indicator_map')
        col1_2, _ = st.columns([1, 1])
        selected_date_map = col1_2.select_slider("Date", dates, value=default_date)
        # Map creation
        m = folium.Map(location=[40, -95], zoom_start=4)

        us_states_json = json.load(open('data/us-states.json'))
        # Add GeoJSON layer for the US
        folium.GeoJson(us_states_json, name='geojson').add_to(m)

        df_map = df.loc[(df['Indicator Name'] == selected_indicator_map) & (df['Date'] == selected_date_map)]
        cp = folium.Choropleth(
            geo_data=us_states_json,
            name='choropleth',
            data=df_map,
            columns=['Region Name', 'Value'],
            key_on='feature.properties.name',
            bins=get_value_bins(df, selected_indicator_map),
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=str(selected_date_map) + ' - ' + selected_indicator_map + " ($)",
            highlight=True
        ).add_to(m)

        # creating a state indexed version of the dataframe so we can lookup values
        state_data_indexed = df_map.set_index('Region Name')

        # looping thru the geojson object and adding a new property(unemployment)
        # and assigning a value from our dataframe
        for s in cp.geojson.data['features']:
            try:
                s['properties']['Value'] = int(state_data_indexed.loc[s['properties']['name'], 'Value'])
            except KeyError:
                s['properties']['Value'] = 'No data'

        # and finally adding a tooltip/hover to the choropleth's geojson
        folium.GeoJsonTooltip(['name', 'Value'], labels=False).add_to(cp.geojson)

        folium.LayerControl().add_to(m)
        # Display the map
        st_folium(m, width=1000)

    with tab2:
        col1_3, _ = st.columns([1, 1])
        selected_indicator_chart = col1_3.selectbox("Indicator", indicator_name, key='indicator')
        selected_states = col1_3.multiselect("States", region_name, ['New York', 'Nevada'])

        df_filter = filter_df(df, selected_states, selected_indicator_chart)
        st.line_chart(df_filter, y=selected_states, height=750)

    display_footer()


if __name__ == '__main__':
    main()
