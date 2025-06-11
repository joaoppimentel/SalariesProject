import streamlit as st
import pandas as pd
from utils.dashboard_utils import salary_infos,salary_map, companies_diff_salaries, employment_type_mean, linechart_jobtitle
from utils.dashboard_functions import year_filter, return_df_view_by_year, highest_average_salary, most_frequent, full_counts, average_groupby_linechart
import seaborn as sns


st.title("Dashoard 🏠")
year = year_filter()
df = return_df_view_by_year()

st.markdown('### Big Numbers')
col1, col2, col3 = st.columns(3)
st.divider()
st.markdown('### Graphs')
col4, col5 = st.columns(2)

col6 = st.columns(1)


with col1.container(border=True):
    highest_average_salary(df, year,'remote_ratio')

with col2.container(border=True):
    highest_average_salary(df, year, 'company_location')

with col3.container(border=True):
    most_frequent(df, year, 'remote_ratio')


with st.container(border=True):
    choice2 = st.selectbox('Average Salary Throughout The Year By:', ['Employment Type', 'Experience Level', 'Company Size'])
    if choice2 == 'Employment Type':
        average_groupby_linechart(df, 'employment_type')
    elif choice2 == 'Experience Level':
        average_groupby_linechart(df, 'experience_level')
    else:
        average_groupby_linechart(df, 'company_size')

st.divider()

with st.container(border=True):
    choice3 = st.selectbox('Average Salary By:', ['Company Location', 'Employees Residence'])
    st.markdown(f"### Average Salary By: {choice3}")
    salary_map(choice3)

st.divider()


with st.container(border=True):
    st.markdown('### ')
    linechart_jobtitle()







































