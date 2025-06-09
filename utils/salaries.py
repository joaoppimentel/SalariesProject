import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('salaries.db')

cursor = conn.cursor()

def get_df():
    df = pd.read_csv('./data/ds_salaries.csv')
    return df

def get_payments():
    query = """
    SELECT SUM(salary_in_usd) as "Total Pago" FROM salaries
"""
    salary_sum = pd.read_sql_query(query, conn)
    return salary_sum

def count_jobs():
    query = """
    SELECT COUNT(job_title) FROM salaries
    GROUP BY job_title
    """
    trabalhos = pd.read_sql_query(query, conn)
    return trabalhos
