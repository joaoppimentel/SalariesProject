import streamlit as st
import pandas as pd
from utils.dashboard_utils import salary_map, linechart_jobtitle
from utils.dashboard_functions import year_filter, return_df, highest_average_salary, most_frequent, full_counts, average_groupby_linechart, full_averages, average_groupby_barchart, full_sums, highest_total_salary


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
tab1, tab12, tab13 = st.tabs(['Average salary', 'Total salary expenditure', 'Number of employees'])

# median
with tab1:
    with st.container(border=True):
        st.subheader('Average salary by category')
        col5, col52, col53 = st.columns([1, 1.5, 1.5], gap='large')
        with col5:
            choice2 = st.selectbox('Average salary throughout the years by:', ['Company Size', 'Experience Level', 'Employment Type'])
        with col52:
            highest_average_salary(df, year, choice2)
        with col53:
            highest_average_salary(df, year, 'remote_ratio')

        if choice2 == 'Employment Type':
            average_groupby_linechart(df, 'employment_type', 'median')
            average_groupby_barchart(df, year, 'employment_type', 'median')
        elif choice2 == 'Experience Level':
            average_groupby_linechart(df, 'experience_level', 'median')
            average_groupby_barchart(df, year, 'experience_level', 'median')
        else:
            average_groupby_linechart(df, 'company_size', 'median')
            average_groupby_barchart(df, year, 'company_size', 'median')

    st.divider()

    with st.container(border=True):
        st.subheader('Average salary by country')
        col6, col62 = st.columns([1,2], gap='large')
        with col6:
            choice3 = st.selectbox('Average salary by country of:', ['Company Location', 'Employee Residence'])

        with col62:
            highest_average_salary(df, year, choice3)

        salary_map(choice3, df, year, 'median')

    st.divider()


    with st.container(border=True):
        st.subheader('Average job salary by category')
        col7, col72 = st.columns([1,2], gap='large')
        
        with col7:
            choice = st.selectbox('Avarage job salary by:', ['Company Size', 'Experience Level', 'Employment Type', 'Remote Ratio'])
        
        with col72:
            highest_average_salary(df, year, 'job_title')

        linechart_jobtitle(df, year, choice, 'median')
# Sum
with tab12:
    with st.container(border=True):
        st.subheader('Total salary expenditure by category')
        col5, col52, col53 = st.columns([1, 1.5, 1.5], gap='large')
        with col5:
            choice2 = st.selectbox('Total salary expenditure throughout the years by:', ['Company Size', 'Experience Level', 'Employment Type'])
        with col52:
            highest_total_salary(df, year, choice2)
        with col53:
            highest_total_salary(df, year, 'remote_ratio')
            
        if choice2 == 'Employment Type':
            average_groupby_linechart(df, 'employment_type', 'sum')
            average_groupby_barchart(df, year, 'employment_type', 'sum')
        elif choice2 == 'Experience Level':
            average_groupby_linechart(df, 'experience_level', 'sum')
            average_groupby_barchart(df, year, 'experience_level', 'sum')
        else:
            average_groupby_linechart(df, 'company_size', 'sum')
            average_groupby_barchart(df, year, 'company_size', 'sum')

    st.divider()

    with st.container(border=True):
        st.subheader('Total salary expenditure by country')
        col6, col62 = st.columns([1,2], gap='large')
        with col6:
            choice3 = st.selectbox('Total salary expenditure by country of:', ['Company Location', 'Employee Residence'])

        with col62:
            highest_total_salary(df, year, choice3)

        salary_map(choice3, df, year, 'sum')

    st.divider()


    with st.container(border=True):
        st.subheader('Total job salary expenditure by category')
        col7, col72 = st.columns([1,2], gap='large')
        
        with col7:
            choice = st.selectbox('Total job salary expenditure by:', ['Company Size', 'Experience Level', 'Employment Type', 'Remote Ratio'])
        
        with col72:
            highest_total_salary(df, year, 'job_title')

        linechart_jobtitle(df, year, choice, 'sum')

# Count
with tab13:
    with st.container(border=True):
        st.subheader('Number of employees by category')
        col5, col52, col53 = st.columns([1,1.5,1.5], gap='large')
        with col5:
            choice2 = st.selectbox('Number of employees throughout the years by:', ['Company Size', 'Experience Level', 'Employment Type'])
        with col52:
            most_frequent(df, year, choice2)
        with col53:
            most_frequent(df, year, 'remote_ratio')

        if choice2 == 'Employment Type':
            average_groupby_linechart(df, 'employment_type', 'count')
            average_groupby_barchart(df, year, 'employment_type', 'count')
        elif choice2 == 'Experience Level':
            average_groupby_linechart(df, 'experience_level', 'count')
            average_groupby_barchart(df, year, 'experience_level', 'count')
        else:
            average_groupby_linechart(df, 'company_size', 'count')
            average_groupby_barchart(df, year, 'company_size', 'count')

    st.divider()

    with st.container(border=True):
        st.subheader('Number of employees by country')
        col6, col62 = st.columns([1,2], gap='large')
        with col6:
            choice3 = st.selectbox('Number of employees by:', ['Company Location', 'Employee Residence'])

        with col62:
            most_frequent(df, year, choice3)

        salary_map(choice3, df, year, 'count')

    st.divider()


    with st.container(border=True):
        st.subheader('Number of employees by job title')
        col7, col72 = st.columns([1,2], gap='large')
        
        with col7:
            choice = st.selectbox('Number of job employees by:', ['Company Size', 'Experience Level', 'Employment Type', 'Remote Ratio'])
        
        with col72:
            most_frequent(df, year, 'job_title')

        linechart_jobtitle(df, year, choice, 'count')







































