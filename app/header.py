from PIL import Image
import streamlit as st


def set_page_config_00() -> None:
    # TODO set a favicon
    # favicon = Image.open('../images/favicon_ffn.ico')
    st.set_page_config(page_title="Flight comparator 2.0",
                       # page_icon=favicon,
                       layout="wide",
                       menu_items={
                           'About': 'https://gitlab.com/bqueguin/snowflake-summit',
                           'Report a bug': "mailto:bruno.queguiner@seenovate.com"
                       })
