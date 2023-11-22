
# Prosta aplikacja Streamlit
import streamlit as st

# ustawmy tytuł aplikacji
st.title("Przykładowa aplikacja Streamlit")

# suwak
slider_val = st.slider("Podaj liczbę", min_value=0, max_value=100, value=50)

# selectbox do wyboru operacji
oper = st.selectbox("Wybierz operację", ["podwojenie","potęgowanie do kw."])

# przycisk do submitowania formularza
calculate = st.button("Oblicz")

if calculate:
    if oper == "podwojenie":
        result = slider_val * 2
    elif oper == "potęgowanie do kw.":
        result = slider_val ** 2
    st.write(f"Wynik operacji {oper} dla liczby {slider_val} wynosi:{result}")


