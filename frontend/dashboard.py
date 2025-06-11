import streamlit as st
import pandas as pd
from utils.dashboard_utils import get_df, salary_infos,salary_map, alpha2_to_alpha3, companies_diff_salaries, employment_type_mean, linechart_jobtitle
import seaborn as sns


st.title("Dashoard 🏠")

df = get_df()
st.write(df)

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

# filters = st.sidebar.multiselect('Filtragem por ano', )

df_filtered = salary_infos()
df_filtered = df_filtered.groupby(['job_title', 'experience_level']).agg(mean=('salary_in_usd', 'mean'), median=('salary_in_usd', 'median'), std=('salary_in_usd', 'std'))

df_filtered2 = salary_infos()
df_filtered2 = df_filtered2.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
df_filtered2 = df_filtered2.sort_values(['work_year', 'job_title'])
df_filtered2['growth%'] = (df_filtered2.groupby('job_title')['salary_in_usd'].pct_change() * 100)
df_filtered2 = df_filtered2.dropna(subset=['growth%'])
df_filtered2 = (df_filtered2.groupby('job_title')['growth%'].mean().sort_values(ascending=False).reset_index())

df['alpha3_employees_residence'] = df['employee_residence'].apply(alpha2_to_alpha3)
df['alpha3_company_location'] = df['company_location'].apply(alpha2_to_alpha3)

with col1:
    tab1, tab2, tab3, tab4 = st.tabs(['2023', '2022', '2021', '2020'])
    # st.metric('Total pago ($)')

with col4:
    st.markdown("### Informações salariais por experiência e cargo")
    st.write(df_filtered)

with col5:
    escolha = st.selectbox('Média Salarial',['Por países', 'Por tamanho da empresa', 'Por tipo de contrato'])
    if escolha == 'Por países':
        salary_map()
    elif escolha == 'Por tipo de contrato':
        employment_type_mean()
    else:
        companies_diff_salaries()


linechart_jobtitle()
