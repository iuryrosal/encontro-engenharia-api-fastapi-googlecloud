import streamlit as st
from api_client import ApiClient
import pandas as pd


def collect_data():
    api_client = ApiClient()
    return api_client.get_customers()


st.write("Exemplo de Dashboard")
json_data = collect_data()
df = pd.json_normalize(json_data)
st.dataframe(df)
