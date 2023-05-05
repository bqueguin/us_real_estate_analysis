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
    st.markdown("❄ Data comes from Knoema [Real Estate Data Atlas](https://app.snowflake.com/marketplace/listing/GZSTZ491W11/knoema-real-estate-data-atlas?search=real%20estate). Loaded thanks to :blue[Snowflake].")
    st.markdown("🏘️ :red[*Learn more about Zillow Home Value Index Methodology*: **[Click here](https://www.zillow.com/research/zhvi-methodology-2019-highlights-26221/) !**]")
    st.markdown("💻 [**Gitlab source code**](https://gitlab.com/bqueguin/snowflake-summit.git)")
    st.markdown("👨‍💻 Created by [Bruno Queguiner](https://fr.linkedin.com/in/bruno-quéguiner-3a1619137)")
