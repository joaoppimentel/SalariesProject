import streamlit as st
import pandas as pd
from utils.dashboard_utils import salary_infos, salary_map, companies_diff_salaries, employment_type_mean, linechart_jobtitle
from utils.dashboard_functions import year_filter, return_df, highest_average_salary, most_frequent, full_counts, average_groupby_linechart, full_averages, average_groupby_barchart, full_sums
import seaborn as sns


st.title("📊 Salaries Dashboard")
year = year_filter()
df = return_df()

st.header(f'Summary | {year}', divider='gray')
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        full_averages(df, year)

with col2:
    with st.container(border=True):
        full_sums(df, year)

with col3:
    with st.container(border=True):
        full_counts(df, year)



st.header('Charts', divider='gray')

with st.container(border=True):
    st.subheader('Average salary by category')
    col5, _, _ = st.columns(3)
    with col5:
        choice2 = st.selectbox('Average salary throughout the years by:', ['Employment Type', 'Experience Level', 'Company Size'])
    if choice2 == 'Employment Type':
        average_groupby_linechart(df, 'employment_type')
        average_groupby_barchart(df, year, 'employment_type')
    elif choice2 == 'Experience Level':
        average_groupby_linechart(df, 'experience_level')
        average_groupby_barchart(df, year, 'experience_level')
    else:
        average_groupby_linechart(df, 'company_size')
        average_groupby_barchart(df, year, 'company_size')

st.divider()

with st.container(border=True):
    col6, _, _ = st.columns(3)
    with col6:
        choice3 = st.selectbox('Average throughout the years by:', ['Company Location', 'Employee Residence'])
    salary_map(choice3, df, year)

st.divider()


with st.container(border=True):
    st.markdown('### ')
    linechart_jobtitle(year)







































