
# Filtrowanie danych

import streamlit as st
import pandas as pd

st.set_page_config('wide')

# Przykładowe dane o samochodach
data = {
    "Brand": ["Toyota", "Honda", "Ford", "Toyota", "Honda"],
    "Model": ["Camry", "Civic", "Mustang", "Corolla", "Accord"],
    "Year": [2021, 2020, 2019, 2018, 2021],
    "Price": [30000, 25000, 35000, 28000, 32000],
}
df = pd.DataFrame(data)

# Ustawianie tytułu aplikacji
st.title("Aplikacja z filtrowaniem danych")

# Lewy panel z filtrami
with st.sidebar:
    st.header("Filtry")
    selected_brand = st.multiselect("Marka", df["Brand"].unique())

    min_year, max_year = min(df["Year"]), max(df["Year"])
    sel_min_year, sel_max_year = st.slider("Rok", min_year, max_year, (min_year, max_year) )

    min_price, max_price = min(df["Price"]), max(df["Price"])
    sel_min_price, sel_max_price = st.slider("Cena", min_price, max_price, (min_price, max_price) )

#################################
# filtrowanie
filtered_df = df.copy()
if len(selected_brand):
    filtered_df = filtered_df.query(f"Brand in {selected_brand}")
filtered_df = filtered_df.query(f"Price>={sel_min_price} and Price<={sel_max_price} ")
filtered_df = filtered_df.query(f"Year>={sel_min_year} and Year<={sel_max_year} ")

st.header("Dane o samochodach")
st.write(filtered_df)

html_table = filtered_df.to_html(classes=["table", "table-striped", "table-hover"], index=False, border=0)

# Dodawanie stylów CSS do ustawienia szerokości kolumn
html_table = f"""
<style>
    .table {{
        width: 100%;
    }}
    .table td:nth-child(1), .table th:nth-child(1) {{
        width: 20%;
    }}
    .table td:nth-child(2), .table th:nth-child(2) {{
        width: 30%;
    }}
    .table td:nth-child(3), .table th:nth-child(3) {{
        width: 50%;
    }}
</style>
{html_table}
"""

# Wyświetlanie tabeli z ustawioną szerokością kolumn
st.write(html_table, unsafe_allow_html=True)

