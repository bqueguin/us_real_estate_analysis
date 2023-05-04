import streamlit as st
from PIL import Image


def set_page_config() -> None:
    favicon = Image.open('../images/favicon.ico')
    st.set_page_config(page_title="US Real Estate",
                       page_icon=favicon,
                       layout="wide",
                       menu_items={
                           'About': 'https://gitlab.com/bqueguin/snowflake-summit',
                           'Report a bug': "mailto:bruno.queguiner@seenovate.com"
                       })


def display_footer() -> None:
    st.divider()
    st.markdown("Learn more about Zillow Home Value Index Methodology: Click [here](https://www.zillow.com/research/zhvi-methodology-2019-highlights-26221/) !")
    st.markdown("Check the source code of the app [here](https://gitlab.com/bqueguin/snowflake-summit.git)")
    st.markdown("Source code Gitlab repo: created by [Bruno Queguiner](https://fr.linkedin.com/in/bruno-quéguiner-3a1619137)")
