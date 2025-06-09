import pandas as pd
import sqlite3

conn = sqlite3.connect('salaries.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS salaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_year INTEGER NOT NULL,
    experience_level TEXT NOT NULL,
    employment_type TEXT NOT NULL,
    job_title TEXT NOT NULL,
    salary REAL NOT NULL,
    salary_currency TEXT NOT NULL,
    salary_in_usd REAL NOT NULL,
    employee_residence TEXT NOT NULL,
    remote_ratio INTEGER NOT NULL,
    company_location TEXT NOT NULL,
    company_size TEXT NOT NULL
)''')

df = pd.read_csv('./data/ds_salaries.csv')
df.to_sql('salaries', conn, if_exists='replace', index=False)

conn.commit()

conn.close()

