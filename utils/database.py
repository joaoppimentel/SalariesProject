import pandas as pd
import sqlite3

def execute_query(query, params=None, fetch=False, db_path='salaries'):
    """
    Executa uma query no banco SQLite.

    Args:
        query (str): Comando SQL a ser executado.
        params (tuple, optional): Parâmetros para query parametrizada. Default é None.
        fetch (bool, optional): Se True, retorna os resultados da query (ex: SELECT). Default é False.
        db_path (str, optional): Caminho para o arquivo do banco SQLite. Default é 'salaries'

    Returns:
        list: Resultados da query, se fetch=True. Caso contrário, None.
    """
    try:
        with sqlite3.connect(db_path+".db") as conn:
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
    
def create_tables():
    create_table_salaries()
    # create_tables_anac()

def create_table_salaries():
    execute_query('''
    CREATE TABLE IF NOT EXISTS salaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        work_year INTEGER,
        experience_level TEXT,
        employment_type TEXT,
        job_title TEXT,
        salary REAL,
        salary_currency TEXT,
        salary_in_usd REAL,
        employee_residence TEXT,
        remote_ratio INTEGER,
        company_location TEXT,
        company_size TEXT
    )''', db_path='salaries')

def create_tables_anac():
    execute_query('''
    CREATE TABLE IF NOT EXISTS empresas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sigla TEXT,
        nome TEXT,
        nacionalidade TEXT
    )''', db_path='anac')

    execute_query('''
    CREATE TABLE IF NOT EXISTS aeroportos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sigla TEXT,
        uf TEXT,
        regiao TEXT,
        pais TEXT,
        continente TEXT
    )''', db_path='anac')

    execute_query('''
        CREATE TABLE IF NOT EXISTS voos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa_id INTEGER,
        ano INTEGER,
        mes INTEGER,
        aeroporto_origem_id INTEGER,
        aeroporto_destino_id INTEGER,
        natureza TEXT,
        grupo_voo TEXT,
        passageiros_pagos INTEGER,
        passageiros_gratis INTEGER,
        carga_paga INTEGER,
        carga_gratis INTEGER,
        correio INTEGER,
        ask INTEGER,
        rpk INTEGER,
        atk INTEGER,
        rtk INTEGER,
        combustivel_litros INTEGER,
        distancia_voada_km INTEGER,
        decolagens INTEGER,
        carga_paga_km INTEGER,
        carga_gratis_km INTEGER,
        correio_km INTEGER,
        assentos INTEGER,
        payload INTEGER,
        horas_voadas INTEGER,
        bagagem_kg INTEGER,
        FOREIGN KEY (empresa_id) REFERENCES empresas(id),
        FOREIGN KEY (aeroporto_origem_id) REFERENCES aeroportos(id),
        FOREIGN KEY (aeroporto_destino_id) REFERENCES aeroportos(id)
    )''', db_path='anac')

def fill_salaries():
    df = pd.read_csv('./data/ds_salaries.csv')
    
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

def fill_anac():
    df = pd.read_csv('./data/anac.csv')
    
    query = """
    INSERT INTO anac (
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

def fill_tables():
    salaries_count = execute_query("SELECT COUNT(*) FROM salaries", fetch=True)[0][0]
    if salaries_count == 0:
        fill_salaries()