import streamlit as st
import pandas as pd
from utils.salaries import get_df, get_payments


def main():
    st.set_page_config(page_title="Sistema Academia", layout="wide")

    col1, col2, col3 = st.columns(3)
    with col1:
        total_payment = get_payments()
        st.metric('Soma Total de Pagamentos ($)', value=float(total_payment['Total Pago']))
    st.markdown(" ### Base de dados")
    st.write(get_df())
    st.write()




if __name__ == "__main__":
    main()