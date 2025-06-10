import streamlit as st
from utils.dashboard_functions import highest_avarage_remote_ratio, return_df_view_by_year, year_filter

st.title("Dashoard 🏠")
year = year_filter()

df = return_df_view_by_year()