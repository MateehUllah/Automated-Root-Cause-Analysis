import streamlit as st

st.set_page_config(page_title="Automated Root Cause Analysis", layout="wide")


from components.network_weather import display_network_weather
from components.chatbot import display_chatbot


st.title("Automated Root Cause Analysis")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Network Monitor & Weather", "Netbot"])

if page == "Network Monitor & Weather":
    display_network_weather()
elif page == "Netbot":
    display_chatbot()
