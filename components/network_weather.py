import os
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import st_folium
from utils.alert_system import send_email_alert
from utils.recommendations import generate_network_failure_recommendations
import requests
from dotenv import load_dotenv

load_dotenv()  

@st.cache_resource
def load_model():
    """
    Loads a pre-trained machine learning model from a pickle file.

    This function caches the loaded model to optimize performance in a Streamlit app,
    preventing reloading the model on every script rerun.

    Returns:
        object: The machine learning model loaded from the pickle file.
    """

    with open("models/network_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()


API_KEY = os.getenv("OPEN_WEATHER_API")

def get_weather_data(lat=37.7749, lon=-122.4194):
    """
    Fetches current weather data for a given location.

    Args:
        lat (float, optional): Latitude of the location. Defaults to 37.7749.
        lon (float, optional): Longitude of the location. Defaults to -122.4194.

    Returns:
        dict: A dictionary containing the location name, temperature (in Celsius), humidity percentage, and weather condition description.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("main"):
        return {
            "location": response.get("name", "Unknown Location"),
            "temperature": response["main"]["temp"],
            "humidity": response["main"]["humidity"],
            "condition": response["weather"][0]["description"].capitalize(),
        }
    else:
        return None


def display_network_weather():
    """
    Displays a Streamlit app for AI Network Monitoring & Weather.

    The app takes input network data (packet loss, latency, jitter, bandwidth usage) and a location for weather data.
    It uses a pre-trained machine learning model to predict the risk of network failure based on the input data.
    If a high risk of failure is predicted, it provides recommendations to mitigate the failure and allows the user to send an email alert.

    The app uses the OpenWeatherMap API to fetch current weather data for a given location.
    """
    st.subheader("AI Network Monitoring & Weather")

    st.sidebar.header("Input Network Data")
    packet_loss = st.sidebar.slider("Packet Loss (%)", 0, 100, 5)
    latency = st.sidebar.slider("Latency (ms)", 0, 100, 5)
    jitter = st.sidebar.slider("Jitter (ms)", 0, 100, 5)
    bandwidth_usage = st.sidebar.slider("Bandwidth Usage (%)", 0, 100, 0)

    st.subheader("🌍 Select a Location for Weather Data")
    default_location = [20.5937, 78.9629]
    map_obj = folium.Map(location=default_location, zoom_start=3)
    map_data = st_folium(map_obj, height=500, width=700)

    if map_data and map_data["last_clicked"]:
        lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        weather_data = get_weather_data(lat, lon)

        if weather_data:
            st.write(f"📍 **Location:** {weather_data['location']}")
            st.write(f"🌡 **Temperature:** {weather_data['temperature']}°C")
            st.write(f"💧 **Humidity:** {weather_data['humidity']}%")
            st.write(f"🌦 **Condition:** {weather_data['condition']}")

            network_data = np.array([[packet_loss, latency, jitter, bandwidth_usage, weather_data["temperature"]]])
            failure_prediction = model.predict(network_data)[0]

            if failure_prediction == 1:
                st.error("⚠️ High Risk of Network Failure! Taking preventive action.")
                recommendations = generate_network_failure_recommendations(
                    {
                        "Packet_Loss": packet_loss,
                        "Latency": latency,
                        "Jitter": jitter,
                        "Bandwidth_Usage": bandwidth_usage,
                    },
                    weather_data,
                )

                st.subheader("Recommendations to mitigate the failure:")
                st.write(recommendations)
                if st.button("📩 Send Email Alert"):
                    send_email_alert("Network failure detected",f"⚠️ Network failure detected! Restart router, check hardware, reduce bandwidth.\n\nRecommendations:\n{recommendations}")
                    st.success("Email alert sent successfully!")

            else:
                st.success("Network is Stable")
