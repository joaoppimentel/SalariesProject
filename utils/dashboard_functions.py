import pandas as pd
import streamlit as st
import sqlite3

def year_filter():

    conn = sqlite3.connect('salaries.db', check_same_thread=False)

    df = pd.read_sql_query("SELECT DISTINCT work_year AS years FROM salaries ORDER BY work_year DESC", conn)

    conn.close()

    years = ['All']
    years.extend(df['years'])
    years = tuple(years)

    year = st.sidebar.selectbox('Select the work year', years)
    if year != 'All':
        year = int(year)
    
    return year

def return_df_view_by_year():

    conn = sqlite3.connect('salaries.db', check_same_thread=False)

    df = pd.read_sql_query("SELECT * FROM salaries_view", conn)

    conn.close()
    return df

def highest_avarage_remote_ratio(df, year):
    
    if year == 'All':
        remote_ratio_average = df.groupby(['remote_ratio']).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_remote_ratio = remote_ratio_average.iloc[remote_ratio_average['average_salary'].idxmax()]
        salary = round(highest_remote_ratio['average_salary'], 2)
        remote_ratio = highest_remote_ratio['remote_ratio']
        highest_average_metric = st.metric(
            label='Highest average salary remote ratio',
            value= f'{salary}$ | {remote_ratio}'
        )  
    elif (year-1) in df['work_year'].values:
        remote_ratio_average_current_year = df.loc[df['work_year'] == year].groupby(['remote_ratio']).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        remote_ratio_average_last_year = df.loc[df['work_year'] == year-1].groupby(['remote_ratio']).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_remote_ratio_current_year = remote_ratio_average_current_year.iloc[remote_ratio_average_current_year['average_salary'].idxmax()]
        highest_remote_ratio_last_year = remote_ratio_average_last_year.iloc[remote_ratio_average_last_year['average_salary'].idxmax()]
        salary_current_year = round(highest_remote_ratio_current_year['average_salary'], 2)
        salary_last_year = round(highest_remote_ratio_last_year['average_salary'], 2)
        delta = round(salary_current_year - salary_last_year, 2)
        remote_ratio_current_year = highest_remote_ratio_current_year['remote_ratio']
        remote_ratio_last_year = highest_remote_ratio_last_year['remote_ratio']
        highest_average_metric = st.metric(
            label='Highest average salary remote ratio',
            value=f'{salary_current_year}$ | {remote_ratio_current_year}',
            delta=f'{delta}$ | {remote_ratio_last_year}'
        )
    else:
        remote_ratio_average = df.loc[df['work_year'] == year].groupby(['remote_ratio']).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_remote_ratio = remote_ratio_average.iloc[remote_ratio_average['average_salary'].idxmax()]
        salary = round(highest_remote_ratio['average_salary'], 2)
        remote_ratio = highest_remote_ratio['remote_ratio']
        highest_average_metric = st.metric(
            label='Highest average salary remote ratio',
            value= f'{salary}$ | {remote_ratio}'
        )