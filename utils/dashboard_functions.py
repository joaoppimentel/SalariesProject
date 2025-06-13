import pandas as pd
import streamlit as st
import sqlite3
import plotly.express as px
from numerize import numerize

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

def return_df():

    conn = sqlite3.connect('salaries.db', check_same_thread=False)

    df = pd.read_sql_query("SELECT * FROM salaries_view", conn)

    conn.close()
    return df

def highest_average_salary(df, year, column):
    
    column = column.lower().replace(' ', '_')

    if year == 'All':
        column_average = df.groupby([column]).aggregate(average_salary=('salary_in_usd','median')).reset_index()
        highest_column = column_average.iloc[column_average['average_salary'].idxmax()]
        salary = round(highest_column['average_salary'], 2)
        column_name = highest_column[column]
        highest_average_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with highest average salary | {year}',
            value= f'${numerize.numerize(salary)} | {column_name}'
        )  
    elif (year-1) in df['work_year'].values:
        column_average_current_year = df.loc[df['work_year'] == year].groupby([column]).aggregate(average_salary=('salary_in_usd','median')).reset_index()
        column_average_last_year = df.loc[df['work_year'] == year-1].groupby([column]).aggregate(average_salary=('salary_in_usd','median')).reset_index()
        highest_column_current_year = column_average_current_year.iloc[column_average_current_year['average_salary'].idxmax()]
        highest_column_last_year = column_average_last_year.iloc[column_average_last_year['average_salary'].idxmax()]
        salary_current_year = round(highest_column_current_year['average_salary'], 2)
        salary_last_year = round(highest_column_last_year['average_salary'], 2)
        delta = round(salary_current_year - salary_last_year, 2)
        delta_percentage = round((delta/salary_last_year)*100, 2)
        column_current_year = highest_column_current_year[column]
        column_last_year = highest_column_last_year[column]
        highest_average_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with highest average salary | {year}',
            value=f'${numerize.numerize(salary_current_year)} | {column_current_year}',
            delta=f'{delta_percentage}% | {column_last_year} | {year-1}',
            help=f"The delta refers to last year's {column.replace('_', ' ')} with highest average salary"
        )
    else:
        column_average = df.loc[df['work_year'] == year].groupby([column]).aggregate(average_salary=('salary_in_usd','median')).reset_index()
        highest_column = column_average.iloc[column_average['average_salary'].idxmax()]
        salary = round(highest_column['average_salary'], 2)
        column_name = highest_column[column]
        highest_average_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with highest average salary | {year}',
            value= f'${numerize.numerize(salary)} | {column_name}'
        )

def highest_total_salary(df, year, column):
    
    column = column.lower().replace(' ', '_')

    if year == 'All':
        column_total = df.groupby([column]).aggregate(total_salary=('salary_in_usd','sum')).reset_index()
        highest_column = column_total.iloc[column_total['total_salary'].idxmax()]
        salary = round(highest_column['total_salary'], 2)
        column_name = highest_column[column]
        highest_total_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with highest total salary | {year}',
            value= f'${numerize.numerize(salary)} | {column_name}'
        )  
    elif (year-1) in df['work_year'].values:
        column_total_current_year = df.loc[df['work_year'] == year].groupby([column]).aggregate(total_salary=('salary_in_usd','sum')).reset_index()
        column_total_last_year = df.loc[df['work_year'] == year-1].groupby([column]).aggregate(total_salary=('salary_in_usd','sum')).reset_index()
        highest_column_current_year = column_total_current_year.iloc[column_total_current_year['total_salary'].idxmax()]
        highest_column_last_year = column_total_last_year.iloc[column_total_last_year['total_salary'].idxmax()]
        salary_current_year = round(highest_column_current_year['total_salary'], 2)
        salary_last_year = round(highest_column_last_year['total_salary'], 2)
        delta = round(salary_current_year - salary_last_year, 2)
        delta_percentage = round((delta/salary_last_year)*100, 2)
        column_current_year = highest_column_current_year[column]
        column_last_year = highest_column_last_year[column]
        highest_total_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with highest total salary | {year}',
            value=f'${numerize.numerize(salary_current_year)} | {column_current_year}',
            delta=f'{delta_percentage}% | {column_last_year} | {year-1}',
            help=f"The delta refers to last year's {column.replace('_', ' ')} with highest total salary"
        )
    else:
        column_total = df.loc[df['work_year'] == year].groupby([column]).aggregate(total_salary=('salary_in_usd','sum')).reset_index()
        highest_column = column_total.iloc[column_total['total_salary'].idxmax()]
        salary = round(highest_column['total_salary'], 2)
        column_name = highest_column[column]
        highest_total_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with highest total salary | {year}',
            value= f'${numerize.numerize(salary)} | {column_name}'
        )

def most_frequent(df, year, column):

    column = column.lower().replace(' ', '_')

    if year == 'All':
        column_frequency = df.groupby([column]).aggregate(frequency=('salary_in_usd','count')).reset_index()
        total = column_frequency['frequency'].sum()
        highest_column = column_frequency.iloc[column_frequency['frequency'].idxmax()]
        frequency = highest_column['frequency']
        frequency_percentage = round((frequency/total)*100, 2)
        column_name = highest_column[column]
        highest_frequency_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with most employees | {year}',
            value= f'{frequency} | {column_name} | {frequency_percentage}%'
        )  
    elif (year-1) in df['work_year'].values:
        column_frequency_current_year = df.loc[df['work_year'] == year].groupby([column]).aggregate(frequency=('salary_in_usd','count')).reset_index()
        column_frequency_last_year = df.loc[df['work_year'] == year-1].groupby([column]).aggregate(frequency=('salary_in_usd','count')).reset_index()
        total = column_frequency_current_year['frequency'].sum()
        highest_column_current_year = column_frequency_current_year.iloc[column_frequency_current_year['frequency'].idxmax()]
        highest_column_last_year = column_frequency_last_year.iloc[column_frequency_last_year['frequency'].idxmax()]
        frequency_current_year = highest_column_current_year['frequency']
        frequency_current_year_percentage = round((frequency_current_year/total)*100, 2)
        frequency_last_year = highest_column_last_year['frequency']
        delta = frequency_current_year - frequency_last_year
        delta_percentage = round((delta/frequency_last_year)*100, 2)
        column_current_year = highest_column_current_year[column]
        column_last_year = highest_column_last_year[column]
        highest_frequency_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with most employees | {year}',
            value=f'{frequency_current_year} | {column_current_year} | {frequency_current_year_percentage}%',
            delta=f'{delta_percentage}% | {column_last_year} | {year-1}',
            help=f"The delta refers to last year's {column.replace('_', ' ')} with most employees"
        )
    else:
        column_frequency = df.loc[df['work_year'] == year].groupby([column]).aggregate(frequency=('salary_in_usd','count')).reset_index()
        total = column_frequency['frequency'].sum()
        highest_column = column_frequency.iloc[column_frequency['frequency'].idxmax()]
        frequency = highest_column['frequency']
        frequency_percentage = round((frequency/total)*100, 2)
        column_name = highest_column[column]
        highest_frequency_metric = st.metric(
            label=f'{column.capitalize().replace('_', ' ')} with most employees | {year}',
            value= f'{frequency} | {column_name} | {frequency_percentage}%'
        )

def full_counts(df, year):
    if year == 'All':
        total_employees = df.shape[0]
        total_employees_metric = st.metric(
            label=f'Total employees',
            value= f'{total_employees}'
        )  
    elif (year-1) in df['work_year'].values:
        total_employees_current_year = df.loc[df['work_year'] == year].shape[0]
        total_employees_last_year = df.loc[df['work_year'] == year-1].shape[0]
        delta = round(total_employees_current_year - total_employees_last_year, 2)
        delta_percentage = round((delta/total_employees_last_year)*100, 2)
        total_employees_metric = st.metric(
            label=f'Total employees',
            value=f'{total_employees_current_year}',
            delta=f'{delta_percentage}% | {delta}'
        )
    else:
        total_employees = df.loc[df['work_year'] == year].shape[0]
        total_employees_metric = st.metric(
            label=f'Total emplyees',
            value= f'{total_employees}'
        )

def full_averages(df, year):
    if year == 'All':
        average_salary = round(df['salary_in_usd'].median(), 2)
        average_salary_metric = st.metric(
            label=f'Overall average salary',
            value= f'${numerize.numerize(average_salary)}'
        )  
    elif (year-1) in df['work_year'].values:
        average_salary_current_year = round(df['salary_in_usd'].loc[df['work_year'] == year].median(), 2)
        average_salary_last_year = round(df['salary_in_usd'].loc[df['work_year'] == year-1].median(), 2)
        delta = round(average_salary_current_year - average_salary_last_year, 2)
        delta_percentage = round((delta/average_salary_last_year)*100, 2)
        total_employees_metric = st.metric(
            label=f'Overall average salary',
            value=f'${numerize.numerize(average_salary_current_year)}',
            delta=f'{delta_percentage}% | ${delta}'
        )
    else:
        average_salary = round(df['salary_in_usd'].loc[df['work_year'] == year].median(), 2)
        average_salary_metric = st.metric(
            label=f'Overall average salary',
            value= f'${numerize.numerize(average_salary)}'
        )

def full_sums(df, year):
    if year == 'All':
        salary_budget = round(df['salary_in_usd'].sum(), 2)
        average_salary_metric = st.metric(
            label=f'Total salary',
            value= f'${numerize.numerize(salary_budget)}'
        )  
    elif (year-1) in df['work_year'].values:
        salary_budget_current_year = round(df['salary_in_usd'].loc[df['work_year'] == year].sum(), 2)
        salary_budget_last_year = round(df['salary_in_usd'].loc[df['work_year'] == year-1].sum(), 2)
        delta = round(salary_budget_current_year - salary_budget_last_year, 2)
        delta_percentage = round((delta/salary_budget_last_year)*100, 2)
        total_employees_metric = st.metric(
            label=f'Total salary',
            value=f'${numerize.numerize(salary_budget_current_year)}',
            delta=f'{delta_percentage}% | ${numerize.numerize(delta)}'
        )
    else:
        salary_budget = round(df['salary_in_usd'].loc[df['work_year'] == year].sum(), 2)
        average_salary_metric = st.metric(
            label=f'Total salary',
            value= f'${numerize.numerize(salary_budget)}'
        )

def average_groupby_linechart(df, column, tab):

    match tab:
        case 'median':
            title = f'Average salary by {column.replace('_', ' ')} throughout the years'
            label = f'Average salary'
        case 'sum':
            title = f'Total salary by {column.replace('_', ' ')} throughout the years'
            label = f'Total salary'
        case 'count':
            title = f'Number of employees by {column.replace('_', ' ')} throughout the years'
            label = 'Number of employees'

    average_salary_groupby = df.groupby(['work_year', 'remote_ratio', column]).aggregate(average_salary=('salary_in_usd', tab)).reset_index()
    average_salary_groupby['work_year'] = average_salary_groupby['work_year'].astype('str')
    color_mapping = {'No Remote': '#ed4840', 'Parcially Remote': '#bcddf2', 'Full Remote': '#406ec1'}
    fig = px.line(
                average_salary_groupby, 
                x='work_year', 
                y='average_salary', 
                color='remote_ratio', 
                symbol='remote_ratio', 
                facet_col=column, 
                markers=True, 
                labels={'work_year':'Work year', 'remote_ratio' : 'Remote ratio', 'average_salary':label}, 
                title=title,
                color_discrete_map=color_mapping)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig)

def average_groupby_barchart(df, year, column, tab):
    color_mapping = {'No Remote': '#ed4840', 'Parcially Remote': '#bcddf2', 'Full Remote': '#406ec1'}

    match tab:
        case 'median':
            title = f'Average salary by {column.replace('_', ' ')} | {year}'
            label = f'Average salary'
        case 'sum':
            title = f'Total salary by {column.replace('_', ' ')} | {year}'
            label = f'Total salary'
        case 'count':
            title = f'Number of employees by {column.replace('_', ' ')} | {year}'
            label = 'Number of employees'

    if year == 'All':
        test = df.groupby([column, 'remote_ratio']).aggregate(average_salary=('salary_in_usd',tab)).reset_index()
        fig = px.bar(
                    test, 
                    x=column, 
                    y='average_salary', 
                    color='remote_ratio', 
                    barmode='group', 
                    labels={column:column.title().replace('_', ' '), 'remote_ratio' : 'Remote ratio', 'average_salary':label}, 
                    title=title,
                    color_discrete_map=color_mapping)
        fig.update_xaxes(categoryorder='category ascending')
        st.plotly_chart(fig)
    else:
        df_year = df.loc[df['work_year'] == year]
        test = df_year.groupby([column, 'remote_ratio']).aggregate(average_salary=('salary_in_usd',tab)).reset_index()
        fig = px.bar(
                    test, x=column, 
                    y='average_salary', 
                    color='remote_ratio', 
                    barmode='group', 
                    labels={column:column.title().replace('_', ' '), 'remote_ratio' : 'Remote ratio', 'average_salary':label}, 
                    title=title,
                    color_discrete_map=color_mapping)
        fig.update_xaxes(categoryorder='category ascending')
        st.plotly_chart(fig)