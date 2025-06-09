import streamlit as st
import pandas as pd

st.title("Tabela ANAC ✈️")

df = pd.read_csv('./data/anac.csv', encoding='latin-1', delimiter=";")
df

