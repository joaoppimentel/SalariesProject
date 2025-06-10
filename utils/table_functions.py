import pandas as pd
import sqlite3

def create_view():
    conn = sqlite3.connect('salaries.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(""" 
        CREATE VIEW IF NOT EXISTS salaries_view AS
        SELECT
            id,
            work_year,
            CASE experience_level
                WHEN 'EN' THEN 'Entry-level'
                WHEN 'MI' THEN 'Mid-level'
                WHEN 'SE' THEN 'Senior-level'
                WHEN 'EX' THEN 'Executive-level'
            END AS experience_level,
            CASE employment_type
                WHEN 'PT' THEN 'Part-time'
                WHEN 'FT' THEN 'Full-time'
                WHEN 'CT' THEN 'Contract'
                WHEN 'FL' THEN 'Freelance'
            END AS employment_type,
            job_title,
            salary,
            salary_currency,
            employee_residence,
            CASE remote_ratio
                WHEN 0 THEN 'On-site'
                WHEN 50 THEN 'Hybrid'
                WHEN 100 THEN 'Remote'
            END AS remote_ratio,
            company_location,
            CASE company_size
                WHEN 'S' THEN 'Small'
                WHEN 'M' THEN 'Medium'
                WHEN 'L' THEN 'Large'
            END AS company_size
        FROM salaries           
    """)
    conn.commit()
    conn.close()

def return_df_view():
    conn = sqlite3.connect('salaries.db', check_same_thread=False)

    df = pd.read_sql_query("SELECT * FROM salaries_view", conn)

    conn.close()
    return df

def return_unique(df, column):
    choices = ['All']
    choices.extend(df[column].unique())
    return tuple(choices)

def filter_df(df, work_year=None, experience_level=None, employment_type=None, job_title=None, salary=None, salary_currency=None, salary_in_usd=None, employee_residence=None, remote_ratio=None, company_location=None, company_size=None):

    if work_year is not None and work_year != 'All':
        work_year = int(work_year)
        df = df.loc[df['work_year'] == work_year]
    if experience_level is not None and experience_level != 'All':
        df = df.loc[df['experience_level'] == experience_level]
    if employment_type is not None and employment_type != 'All':
        df = df.loc[df['employment_type'] == employment_type]
    if job_title is not None and job_title != 'All':
        df = df.loc[df['job_title'] == job_title]
    if salary is not None and salary > 0.0:
        df = df.loc[df['salary'] == salary]
    if salary_currency is not None and salary_currency != 'All':
        df = df.loc[df['salary_currency'] == salary_currency]
    if salary_in_usd is not None and salary_in_usd > 0.0:
        df = df.loc[df['salary_in_usd'] == salary_in_usd]
    if employee_residence is not None and employee_residence != 'All':
        df = df.loc[df['employe_residence'] == employee_residence]
    if remote_ratio is not None and remote_ratio != 'All':
        df = df.loc[df['remote_ratio'] == remote_ratio]
    if company_location is not None and company_location != 'All':
        df = df.loc[df['company_location'] == company_location]
    if company_size is not None and company_size != 'All':
        df = df.loc[df['company_size'] == company_size]
    
    return df