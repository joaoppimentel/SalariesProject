import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Sistema Academia", layout="wide")

    df = pd.read_csv('./data/ds_salaries.csv')


if __name__ == "__main__":
    main()