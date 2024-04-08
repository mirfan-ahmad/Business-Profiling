from linkedIn import LinkedIn
from business_profiling import WebScraper
import streamlit as st


if __name__ == '__main__':
    page_dict = {
        "Business Listing": WebScraper,
        "LinkedIn": LinkedIn,
    }
    selected_page = st.sidebar.selectbox("Select a Page", list(page_dict.keys()))
    page_dict[selected_page]()
