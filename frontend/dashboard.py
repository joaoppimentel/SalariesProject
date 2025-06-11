import streamlit as st
import pandas as pd
from utils.dashboard_utils import salary_infos, salary_map, companies_diff_salaries, employment_type_mean, linechart_jobtitle
from utils.dashboard_functions import year_filter, return_df, highest_average_salary, most_frequent, full_counts, average_groupby_linechart, full_averages
import seaborn as sns


st.title("📊 Salaries Dashboard")
year = year_filter()
df = return_df()

st.header('Big Numbers')
col1, col2, col3 = st.columns(3)

with col1:
    full_averages(df, year)

with col2:
    pass

with col3:
    full_counts(df, year)

st.divider()



st.header('Graphs')

with st.container(border=True):
    col5, _, _ = st.columns(3)
    with col5:
        choice2 = st.selectbox('Average salary throughout the years by:', ['Employment Type', 'Experience Level', 'Company Size'])
    if choice2 == 'Employment Type':
        average_groupby_linechart(df, 'employment_type')
    elif choice2 == 'Experience Level':
        average_groupby_linechart(df, 'experience_level')
    else:
        average_groupby_linechart(df, 'company_size')

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







































