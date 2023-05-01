import streamlit as st
from PIL import Image


def set_page_config() -> None:
    # TODO set a favicon
    # favicon = Image.open('../images/favicon_ffn.ico')
    st.set_page_config(page_title="My awesome application",
                       # page_icon=favicon,
                       layout="wide",
                       menu_items={
                           'About': 'https://gitlab.com/bqueguin/snowflake-summit',
                           'Report a bug': "mailto:bruno.queguiner@seenovate.com"
                       })
