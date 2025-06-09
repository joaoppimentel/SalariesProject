import streamlit as st
import pandas as pd
from utils.table_functions import create_view, return_df, filter_df, return_unique

create_view()

df = return_df()

st.title('Salary Report')
col1, col2, col3, col4 = st.columns(4)

enable_filters = st.checkbox('Filters', value=False)

if enable_filters:
    with col1:
        work_year = st.selectbox('Work year', return_unique(df, 'work_year'))
        salary = float(st.number_input('Salary', min_value=0.0, step=0.01))
        remote_ratio = st.selectbox('Remote ratio', return_unique(df, 'remote_ratio'))
    with col2:
        experience_level = st.selectbox('Experience level', return_unique(df, 'experience_level'))
        salary_currency = st.selectbox('Salary currency', return_unique(df, 'salary_currency'))
        company_location = st.selectbox('Company location', return_unique(df, 'company_location'))
    with col3:
        employment_type = st.selectbox('Employment type', return_unique(df, 'employment_type'))
        salary_in_usd = float(st.number_input('Salary in USD', min_value=0.0, step=0.01))
        company_size = st.selectbox('Company size', return_unique(df, 'company_size'))
    with col4:
        job_title = st.selectbox('Job title', return_unique(df, 'job_title'))
        employee_residence = st.selectbox('Employee residence', return_unique(df, 'employee_residence'))
        
else:
    work_year = None
    experience_level = None
    employment_type = None
    job_title = None
    salary = None
    salary_currency = None
    salary_in_usd = None
    employee_residence = None
    remote_ratio = None
    company_location = None
    company_size = None

filtered_df = filter_df(df, work_year=work_year, experience_level=experience_level, employment_type=employment_type, job_title=job_title, salary=salary, salary_currency=salary_currency, salary_in_usd=salary_in_usd, employee_residence=employee_residence, remote_ratio=remote_ratio, company_location=company_location, company_size=company_size)
st.dataframe(filtered_df)