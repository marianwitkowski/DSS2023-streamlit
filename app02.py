import streamlit as st
import datetime

def apply_custom_css():
    custom_css = '''
    <style>

        h1 {
            color: #0000FF;
        }

        .stButton>button {
            background-color: #FF0000;
            color: white;
        }
    </style>
    '''
    st.markdown(custom_css, unsafe_allow_html=True)

#st.set_page_config(layout="wide")

apply_custom_css()
st.title("Example Streamlit form")
st.write("Some form description")

with st.form("my_form1"):
    st.write("Form 1")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)

with st.form("my_form2"):
    st.write("Form 2")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")
    text_input = st.text_input("Input text:")
    memo = st.text_area("Memo:", "Hello world!")
    number_input = st.number_input("Input number:", min_value=0, max_value=100, value=50)

    # Pole jednorazowego wyboru
    radio_options = ["Option 1", "Option 2", "Option 3"]
    radio_choice = st.radio("Choose option:", radio_options)

    # Pole wielokrotnego wyboru
    multi_options = ["Element 1", "Element 2", "Element 3", "Element 4"]
    multi_choice = st.multiselect("Choose elements:", multi_options)

    slider_discrete = st.select_slider('Pick the color', options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])

    date_input = st.date_input("Input date:", value=datetime.date.today())
    time_input = st.time_input("Input time:", value=datetime.time(6,45))

    submit_button = st.form_submit_button("Send form")

    if submit_button:
        st.info('Results', icon="ℹ️")
        st.write("Wprowadzone wartości:")
        st.write(f"Tekst: {text_input}")
        st.write(f"Liczba: {number_input}")
        st.write(f"Jednorazowy wybór: {radio_choice}")
        st.write(f"Wielokrotny wybór: {', '.join(multi_choice) if multi_choice else 'Brak'}")
        st.write(f"Suwak: {slider_discrete}")
        st.write(f"Data: {date_input}")
