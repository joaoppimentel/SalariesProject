import streamlit as st
from utils.database import execute_query ,create_table, fill_table
from utils.table_functions import create_view

def main():
    st.set_page_config(page_title="Sistema Academia", layout="wide")

    create_table()
    table_count = execute_query("SELECT COUNT(*) FROM salaries", fetch=True)[0][0]
    if table_count == 0:
        fill_table()
    
    create_view()

    dashboard_page = st.Page("./frontend/dashboard.py", title="Dashboard", icon="🏠", default=True)

    pg = st.navigation([dashboard_page,])
    pg.run()


if __name__ == "__main__":
    main()