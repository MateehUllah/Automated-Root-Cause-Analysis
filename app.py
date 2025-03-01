import streamlit as st

st.set_page_config(page_title="AI Network Monitor & Chatbot", layout="wide")


from components.network_weather import display_network_weather
# from components.chatbot import display_chatbot


st.title("AI Network Monitoring & Voice Chatbot")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Network Monitor & Weather", "AI Chatbot"])

if page == "Network Monitor & Weather":
    display_network_weather()
elif page == "Chatbot":
    pass
    # display_chatbot()
