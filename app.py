import streamlit as st
from utils.database import execute_query ,create_tables, fill_tables

def main():
    st.set_page_config(page_title="Salários", layout="wide")

    create_tables()
    fill_tables()

    table_anac = st.Page("./frontend/table_anac.py", title="Tabela ANAC", icon="✈️", default=True)

    pg = st.navigation([table_anac,])
    pg.run()


if __name__ == "__main__":
    main()