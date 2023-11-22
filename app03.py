
# Wyświetlanie danych tabelarycznych

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# Tworzenie przykładowego dataframe
data = {
    "Kolumna A": np.random.randint(0, 100, 10),
    "Kolumna B": np.random.randint(0, 100, 10),
    "Kolumna C": np.random.randint(0, 100, 10),
}
df = pd.DataFrame(data)

# Wyświetlenie tytułu aplikacji
st.title("Aplikacja z dataframe, statycznymi tabelami i metrykami")

st.subheader("Dataframe:")
st.write(df)

# Wyświetlenie statycznych tabel
st.subheader("Statyczne tabele:")
table_data = [
    ["Wiersz 1", "Element A", "Element B"],
    ["Wiersz 2", "Element C", "Element D"],
    ["Wiersz 3", "Element E", "Element F"],
]
st.table(table_data)

# Obliczanie metryk
mean_a = df["Kolumna A"].mean()
mean_b = df["Kolumna B"].mean()
mean_c = df["Kolumna C"].mean()

with st.container():
    col1, col2, col3 = st.columns(3)
    col1.metric("średnia kol. A", mean_a, "red" if mean_a < 50 else "green")
    col2.metric("średnia kol. B", mean_b, "red" if mean_a < 50 else "green")
    col3.metric("średnia kol. C", mean_c, "red" if mean_a < 50 else "green")
