import pandas as pd
import sqlite3
from utils.dashboard_utils import alpha2_to_alpha3

def execute_query(query, params=None, fetch=False, db_path='salaries.db'):
    """
    Executa uma query no banco SQLite.

    Args:
        query (str): Comando SQL a ser executado.
        params (tuple, optional): Parâmetros para query parametrizada. Default é None.
        fetch (bool, optional): Se True, retorna os resultados da query (ex: SELECT). Default é False.
        db_path (str, optional): Caminho para o arquivo do banco SQLite. Default é 'salaries.db'.

    Returns:
        list: Resultados da query, se fetch=True. Caso contrário, None.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if fetch:
                results = cursor.fetchall()
                return results
            else:
                conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")
        return None
    
def create_table():
    execute_query('''
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

def fill_table():
    df = pd.read_csv('./data/ds_salaries.csv')
    df['company_location'] = df['company_location'].apply(alpha2_to_alpha3)
    df['employee_residence'] = df['employee_residence'].apply(alpha2_to_alpha3)
    
    query = """
    INSERT INTO salaries (
        work_year, experience_level, employment_type, job_title,
        salary, salary_currency, salary_in_usd,
        employee_residence, remote_ratio, company_location, company_size
    ) VALUES
    """
    df_dict = df.to_dict('index')
    params = []
    for item in df_dict.values():
        params.append(f"""(
            {item['work_year']},
            '{item['experience_level']}',
            '{item['employment_type']}',
            '{item['job_title']}',
            {item['salary']},
            '{item['salary_currency']}',
            {item['salary_in_usd']},
            '{item['employee_residence']}',
            {item['remote_ratio']},
            '{item['company_location']}',
            '{item['company_size']}'
        )""")
    execute_query(f"{query} {" ,".join(params)};")



