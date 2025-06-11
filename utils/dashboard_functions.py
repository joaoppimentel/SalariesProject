import pandas as pd
import streamlit as st
import sqlite3
import plotly.express as px

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

def highest_average_salary(df, year, column):
    
    if year == 'All':
        column_average = df.groupby([column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_column = column_average.iloc[column_average['average_salary'].idxmax()]
        salary = round(highest_column['average_salary'], 2)
        column_name = highest_column[column]
        highest_average_metric = st.metric(
            label=f'Highest average salary {column.replace('_', ' ')}',
            value= f'{salary}$ | {column_name}'
        )  
    elif (year-1) in df['work_year'].values:
        column_average_current_year = df.loc[df['work_year'] == year].groupby([column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        column_average_last_year = df.loc[df['work_year'] == year-1].groupby([column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_column_current_year = column_average_current_year.iloc[column_average_current_year['average_salary'].idxmax()]
        highest_column_last_year = column_average_last_year.iloc[column_average_last_year['average_salary'].idxmax()]
        salary_current_year = round(highest_column_current_year['average_salary'], 2)
        salary_last_year = round(highest_column_last_year['average_salary'], 2)
        delta = round(salary_current_year - salary_last_year, 2)
        delta_percentage = round((delta/salary_last_year)*100, 2)
        column_current_year = highest_column_current_year[column]
        column_last_year = highest_column_last_year[column]
        highest_average_metric = st.metric(
            label=f'Highest average salary {column.replace('_', ' ')}',
            value=f'{salary_current_year}$ | {column_current_year}',
            delta=f'{delta_percentage}% | {column_last_year}'
        )
    else:
        column_average = df.loc[df['work_year'] == year].groupby([column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
        highest_column = column_average.iloc[column_average['average_salary'].idxmax()]
        salary = round(highest_column['average_salary'], 2)
        column_name = highest_column[column]
        highest_average_metric = st.metric(
            label=f'Highest average salary {column.replace('_', ' ')}',
            value= f'{salary}$ | {column_name}'
        )

def most_frequent():
    pass

def full_counts(df, year, column):
    pass

def average_groupby_linechart(df, column):
    test = df.groupby(['work_year', 'remote_ratio', column]).aggregate(average_salary=('salary_in_usd','mean')).reset_index()
    test['work_year'] = test['work_year'].astype('str')
    fig = px.line(test, x='work_year', y='average_salary', color='remote_ratio', symbol='remote_ratio', facet_col=column, markers=True, labels={'work_year':'Work year', 'remote_ratio' : 'Remote ratio', 'average_salary':'Average salary'}, title=f'Average salary by {column.replace('_', ' ')} throughout the years')
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig)