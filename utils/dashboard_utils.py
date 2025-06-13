import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import pycountry
from numerize import numerize

conn = sqlite3.connect('salaries.db', check_same_thread=False)
cursor = conn.cursor()

def get_df():
    df = pd.read_csv('./data/ds_salaries.csv')
    return df

def get_payments_by_year(year):
    query = """
    SELECT SUM(salary_in_usd) FROM salaries_view
    WHERE work_year = ?
"""
    result = pd.read_sql_query(query, conn, params=(year,))
    return result

def salary_infos():
    query = """
    SELECT salary_in_usd, job_title, experience_level, work_year FROM salaries_view
"""
    result = pd.read_sql_query(query, conn)
    df_filtered2 = result.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
    df_filtered2 = df_filtered2.sort_values(['work_year', 'job_title'])
    df_filtered2['growth%'] = (df_filtered2.groupby('job_title')['salary_in_usd'].pct_change() * 100)
    df_filtered2 = df_filtered2.dropna(subset=['growth%'])
    df_filtered2 = (df_filtered2.groupby('job_title')['growth%'].mean().sort_values(ascending=False).reset_index())
    return result

def salary_map(choice, df, year, tab):

    match tab:
        case 'median':
            title = f'Average salary by {choice.lower().replace('_', ' ')} | {year}'
            label = f'Average salary'
        case 'sum':
            title = f'Total salary by {choice.lower().replace('_', ' ')} | {year}'
            label = f'Total salary'
        case 'count':
            title = f'Number of employees by {choice.lower().replace('_', ' ')} | {year}'
            label = 'Number of employees'

    if year != 'All':
        df = df.loc[df['work_year']==year]
    
    choice = choice.lower().replace(' ', '_')
    df_map = df.groupby([choice]).aggregate(salary_in_usd=('salary_in_usd', tab)).reset_index()
    df_map['full_country_name'] = df_map[choice].apply(alpha3_to_full_name)
    fig = px.choropleth(
        df_map,
        locations=choice,
        locationmode='ISO-3',
        color='salary_in_usd',
        hover_name=choice,
        color_continuous_scale='blues',
        title=title,
        labels={'salary_in_usd':label},
        custom_data=['full_country_name'],
        projection='equirectangular'
    )

    match tab:
        case 'mean':
            fig.update_traces(
            hovertemplate=(
                    f"{choice.capitalize().replace('_', ' ')}: %{{location}}<br>"
                    "Country: %{customdata[0]}<br>"
                    f"{label}: $%{{z:,.2f}}<br>"
                )
            )
        case 'sum':
            fig.update_traces(
            hovertemplate=(
                    f"{choice.capitalize().replace('_', ' ')}: %{{location}}<br>"
                    "Country: %{customdata[0]}<br>"
                    f"{label}: $%{{z:,.2f}}<br>"
                )
            )
        case 'count':
            fig.update_traces(
            hovertemplate=(
                    f"{choice.capitalize().replace('_', ' ')}: %{{location}}<br>"
                    "Country: %{customdata[0]}<br>"
                    f"{label}: %{{z:,.0f}}<br>"
                )
            )

    fig.update_layout(
        margin=dict(l=0, r=0, t=24, b=0)
    )
    fig.update_coloraxes(colorbar_tickprefix = '$')
    st.plotly_chart(fig)
 

def alpha2_to_alpha3(alpha2_code):
    try:
        country = pycountry.countries.get(alpha_2=alpha2_code)
        return country.alpha_3 if country else None
    except (AttributeError, LookupError):
        return None
    
def alpha3_to_full_name(alpha3_code):
    try:
        country = pycountry.countries.get(alpha_3=alpha3_code)
        return country.name if country else alpha3_code
    except (AttributeError, LookupError):
        return alpha3_code
    
def companies_diff_salaries():
    query = """
    SELECT AVG(salary_in_usd) as "Média Salarial", company_size FROM salaries_view
    WHERE company_size = 'S'
    UNION
    SELECT AVG(salary_in_usd) as "Média Salarial", company_size FROM salaries_view
    WHERE company_size = 'M'
    UNION
    SELECT AVG(salary_in_usd) as "Média Salarial", company_size FROM salaries_view
    WHERE company_size = 'L'
"""
    result = pd.read_sql_query(query, conn)
    fig = px.bar(result, x='company_size', y='Média Salarial', labels={'company_size':'Tamanho da Empresa'})
    st.plotly_chart(fig)

def employment_type_mean():
    query = """
    SELECT AVG(salary_in_usd) as "Média Salarial", employment_type FROM salaries_view
    GROUP BY employment_type
"""
    result = pd.read_sql_query(query, conn)
    fig = px.bar(result, x='employment_type', y='Média Salarial', labels={'employment_type':'Tipo de Contrato'})
    st.plotly_chart(fig)

def linechart_jobtitle(df, year, choice, tab):

    match tab:
        case 'median':
            title = f'Average job salary by {choice.lower().replace('_', ' ')} | {year}'
            label = f'Average salary'
        case 'sum':
            title = f'Total job salary by {choice.lower().replace('_', ' ')} | {year}'
            label = f'Total salary'
        case 'count':
            title = f'Number of job employees by {choice.lower().replace('_', ' ')} | {year}'
            label = 'Number of employees'

    if year != 'All':
        df = df.loc[df['work_year'] == year]
    choice = choice.lower().replace(' ', '_')
    df = df.groupby([choice, 'job_title']).aggregate(average_salary=('salary_in_usd', tab)).reset_index()
    fig = px.bar(
                df, 
                 x='job_title', 
                 y='average_salary', 
                 color=choice, 
                 barmode='group',
                 labels={choice: choice.capitalize().replace('_', ' '), 'average_salary': label, 'job_title': 'Job title'},
                 title = title
                 )
    fig.update_xaxes(tickangle= 45, categoryorder='category ascending')
    st.plotly_chart(fig)
