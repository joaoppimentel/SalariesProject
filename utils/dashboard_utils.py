import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import plotly.express as px
import pycountry
import seaborn as sns

conn = sqlite3.connect('salaries.db', check_same_thread=False)
cursor = conn.cursor()

def get_df():
    df = pd.read_csv('./data/ds_salaries.csv')
    return df

def get_payments_by_year(year):
    query = """
    SELECT SUM(salary_in_usd) FROM salaries
    WHERE work_year = ?
"""
    result = pd.read_sql_query(query, conn, params=(year,))
    return result

def salary_infos():
    query = """
    SELECT salary_in_usd, job_title, experience_level, work_year FROM salaries
"""
    result = pd.read_sql_query(query, conn)
    df_filtered2 = result.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
    df_filtered2 = df_filtered2.sort_values(['work_year', 'job_title'])
    df_filtered2['growth%'] = (df_filtered2.groupby('job_title')['salary_in_usd'].pct_change() * 100)
    df_filtered2 = df_filtered2.dropna(subset=['growth%'])
    df_filtered2 = (df_filtered2.groupby('job_title')['growth%'].mean().sort_values(ascending=False).reset_index())
    return result

def salary_map(choice):
    df = get_df()
    df['alpha3_employees_residence'] = df['employee_residence'].apply(alpha2_to_alpha3)
    df['alpha3_company_location'] = df['company_location'].apply(alpha2_to_alpha3)

    if choice == 'Employees Residence':
        df_map = df.groupby('alpha3_employees_residence')['salary_in_usd'].mean().reset_index()
        fig = px.choropleth(
        df_map,
        locations='alpha3_employees_residence', 
        locationmode='ISO-3',            
        color='salary_in_usd',           
        hover_name='alpha3_employees_residence', 
        color_continuous_scale='Viridis',
    )
        fig.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )

        st.plotly_chart(fig)
    else:
        df_map = df.groupby('alpha3_company_location')['salary_in_usd'].mean().reset_index()
        fig = px.choropleth(
        df_map,
        locations='alpha3_company_location', 
        locationmode='ISO-3',            
        color='salary_in_usd',           
        hover_name='alpha3_company_location', 
        color_continuous_scale='Viridis',
    )
        fig.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )

        st.plotly_chart(fig)


def alpha2_to_alpha3(alpha2_code):
    try:
        country = pycountry.countries.get(alpha_2=alpha2_code)
        return country.alpha_3 if country else None
    except (AttributeError, LookupError):
        return None

def companies_diff_salaries():
    query = """
    SELECT AVG(salary_in_usd) as "Média Salarial", company_size FROM salaries
    WHERE company_size = 'S'
    UNION
    SELECT AVG(salary_in_usd) as "Média Salarial", company_size FROM salaries
    WHERE company_size = 'M'
    UNION
    SELECT AVG(salary_in_usd) as "Média Salarial", company_size FROM salaries
    WHERE company_size = 'L'
"""
    result = pd.read_sql_query(query, conn)
    fig = px.bar(result, x='company_size', y='Média Salarial', labels={'company_size':'Tamanho da Empresa'})
    st.plotly_chart(fig)

def employment_type_mean():
    query = """
    SELECT AVG(salary_in_usd) as "Média Salarial", employment_type FROM salaries
    GROUP BY employment_type
"""
    result = pd.read_sql_query(query, conn)
    fig = px.bar(result, x='employment_type', y='Média Salarial', labels={'employment_type':'Tipo de Contrato'})
    st.plotly_chart(fig)

def linechart_jobtitle():
    query = """
    SELECT job_title, COUNT(*) as "Quantidade", company_size, AVG(salary_in_usd) as "media" FROM salaries
    GROUP BY job_title, company_size
"""
    result = pd.read_sql_query(query, conn)
    fig = px.bar(result, x='job_title', y='media', color='company_size', barmode='group')
    fig.update_xaxes(tickangle= 45)
    st.plotly_chart(fig)
