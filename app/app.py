import streamlit as st
import folium
from folium.plugins import Draw
from config import logger
from header import set_page_config
from streamlit_folium import st_folium


logger.debug("New run of app.py")
set_page_config()


def main() -> None:
    st.title("Welcome to the flight comparator 2.0")
    col1, col2 = st.columns(2)
    with col1:
        m = folium.Map(location=[0, 0], zoom_start=5)
        Draw(export=True).add_to(m)
        output = st_folium(m)
    with col2:
        st.write(output)


if __name__ == '__main__':
    main()
