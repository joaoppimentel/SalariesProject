import streamlit as st
from utils.dashboard_functions import return_df_view_by_year, year_filter, highest_average_salary, average_groupby_linechart

st.title("Dashoard 🏠")
year = year_filter()

df = return_df_view_by_year()

bn_col1, bn_col2, bn_col3 = st.columns(3)

with bn_col1:
    highest_average_salary(df, year, 'remote_ratio')

with bn_col2:
    highest_average_salary(df, year, 'company_location')

with bn_col3:
    pass

average_groupby_linechart(df, 'employment_type')