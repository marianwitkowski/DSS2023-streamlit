from io import StringIO
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Funkcja do wczytywania danych
def load_data(ticker, start_date, end_date):
    try:
        start_date = str(start_date).replace("-", "")
        end_date = str(end_date).replace("-", "")
        url = f"https://stooq.pl/q/d/l/?s={ticker}&d1={start_date}&d2={end_date}&i=d"
        response = requests.get(url)
        if response.status_code == 200:
            data_string = StringIO(response.content.decode('utf-8'))
            data = pd.read_csv(data_string)
            data['Data'] = pd.to_datetime(data['Data'])
            return data
        else:
            st.error(f"Błąd podczas wczytywania danych: Status code {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Błąd podczas wczytywania danych: {e}")
        return pd.DataFrame()

# Funkcja do obliczania statystyk
def calculate_stats(data, months, stat, column):
    resampled_data = data.resample(f'{months}M', on='Data')
    if stat == 'Najwyższa':
        return resampled_data[column].max()
    elif stat == 'Najniższa':
        return resampled_data[column].min()
    else:  # Średnia
        return resampled_data[column].mean()

# Funkcja do obliczania zmian
def calculate_changes(data):
    last_day_change = data.iloc[-1]['Zamkniecie'] - data.iloc[-2]['Zamkniecie']
    last_day_change_percent = (last_day_change / data.iloc[-2]['Zamkniecie']) * 100
    last_month = data.set_index('Data').last('1M')
    previous_month = data.set_index('Data').last('2M')[:-len(last_month)]
    month_to_month_change = last_month['Zamkniecie'].iloc[-1] - previous_month['Zamkniecie'].iloc[-1]
    month_to_month_change_percent = (month_to_month_change / previous_month['Zamkniecie'].iloc[-1]) * 100
    last_year = data.set_index('Data').last('1Y')
    previous_year = data.set_index('Data').last('2Y')[:-len(last_year)]
    year_to_year_change = last_year['Zamkniecie'].iloc[-1] - previous_year['Zamkniecie'].iloc[-1]
    year_to_year_change_percent = (year_to_year_change / previous_year['Zamkniecie'].iloc[-1]) * 100
    return last_day_change, last_day_change_percent, month_to_month_change, month_to_month_change_percent, year_to_year_change, year_to_year_change_percent

# Główna funkcja Streamlit
def main():
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame()

    col1, col2, _ = st.columns(3)
    with col1.form("load_ticker_form"):
        ticker = st.text_input("Wprowadź ticker spółki")
        start_date = st.date_input("Data początkowa", datetime.now() - timedelta(days=5*365))
        end_date = st.date_input("Data końcowa", datetime.now().date())
        submitted = st.form_submit_button("Załaduj dane")

    if submitted:
        st.session_state['data'] = load_data(ticker, start_date, end_date)

    data_loaded = not st.session_state['data'].empty
    if data_loaded:
        data = st.session_state['data']
        st.title(f'{ticker.upper()} - dane giełdowe')


        ldd_change, ldd_change_percent, mtm_change, mtm_change_percent, yty_change, yty_change_percent = calculate_changes(data)
        col1, col2, col3 = st.columns(3)
        col1.metric("Zmiana 1D", f"{ldd_change:.2f}", f"{ldd_change_percent:.2f}%")
        col2.metric("Zmiana 1M", f"{mtm_change:.2f}", f"{mtm_change_percent:.2f}%")
        col3.metric("Zmiana 1Y", f"{yty_change:.2f}", f"{yty_change_percent:.2f}%")
        st.header("Dane historyczne")
        st.dataframe(data, use_container_width=True, hide_index=True)

    # Filtry boczne
    st.sidebar.title("Filtry")
    disabled = not data_loaded
    months = st.sidebar.slider('Wybierz okres (w miesiącach)', min_value=1, max_value=12, value=3, disabled=disabled)
    column = st.sidebar.radio("Wybierz kolumnę", ('Otwarcie', 'Najwyzszy', 'Najnizszy', 'Zamkniecie', 'Wolumen'), disabled=disabled)
    columns_maps = [('Wartość najwyższa', 'Najwyższa'), ('Wartość najniższa', 'Najniższa'), ('Wartość średnia', 'Średnia')]
    stat = st.sidebar.selectbox('Rodzaj agregacji', options=columns_maps, format_func=lambda x: x[0], disabled=disabled)[1]

    if st.sidebar.button('Oblicz statystyki', disabled=disabled):
        stats = calculate_stats(data, months, stat, column)
        st.header("Statystyki")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f'Statystyki dla okresu {months} m-c i kolumny "{column}":')
            st.write(stats)
        with col2:
            fig = px.line(stats, x=stats.index, y=stats, labels={'y': f'{stat} wartość {column}', 'x': 'Data'}, title=f'Wykres "{stat}" dla kolumny {column}')
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
