
# Prezentacja danych na mapie
import streamlit as st
import pandas as pd
import pydeck as pdk

import folium
from streamlit.components.v1 import html

# Tworzenie przykładowego dataframe z koordynatami GPS
data = {
    "Latitude": [37.7749, 37.8049, 37.7849, 37.7949],
    "Longitude": [-122.4194, -122.4494, -122.4294, -122.4394],
    "Description": ["Location A", "Location B", "Location C", "Location D"]
}
df = pd.DataFrame(data)

# Ustawianie tytułu aplikacji
st.title("Przykładowa aplikacja Streamlit z wizualizacją na mapie koordynat GPS")

# Wyświetlanie dataframe
st.subheader("Dane z koordynatami GPS:")
st.write(df)

# Tworzenie wartwy punktów na mapie
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["Longitude","Latitude"],
    get_radius = 100,
    get_fill_color = [255, 0, 0, 160],
    pickable = True,
)

# Ustawianie widoku  mapy
view_state = pdk.ViewState(
    latitude=df.Latitude.mean(),
    longitude=df.Longitude.mean(),
    zoom=12
)

st.subheader("Mapy z koordynatami:")
deck = pdk.Deck(layers=[point_layer], initial_view_state=view_state, tooltip={"text": "{Description}"})
st.pydeck_chart(deck)

# utworzenie mapy
m = folium.Map(location=[df.Latitude.mean(), df.Longitude.mean()], zoom_start=13)

# dodanie znacznikow do mapy
for _, row in df.iterrows():
    folium.Marker(
        location=[row["Latitude"],row["Longitude"] ],
        popup=row["Description"],
        icon=folium.Icon(color="red")
    ).add_to(m)

# renderowanie mapy Folium
st.subheader("Mapa folium:")
html(m._repr_html_(), width=800, height=600)