import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://airbnb_api:8502")

API_TOKEN = os.getenv("API_TOKEN", "CHANGE_ME")

st.title("🏙️ Airbnb NYC Price Prediction (MLOps)")

neighbourhood_group = st.selectbox("Neighbourhood Group", ["Manhattan","Brooklyn","Queens","Bronx","Staten Island"])
room_type = st.selectbox("Room Type", ["Entire home/apt","Private room","Shared room"])

minimum_nights = st.number_input("Minimum Nights", min_value=1, value=2)
number_of_reviews = st.number_input("Number of Reviews", min_value=0, value=10)
reviews_per_month = st.number_input("Reviews per Month", min_value=0.0, value=1.2)
calculated_host_listings_count = st.number_input("Host Listings Count", min_value=0, value=1)
availability_365 = st.number_input("Availability 365", min_value=0, max_value=365, value=120)
latitude = st.number_input("Latitude", value=40.67)
longitude = st.number_input("Longitude", value=-73.95)

payload = {
    "neighbourhood_group": neighbourhood_group,
    "room_type": room_type,
    "minimum_nights": float(minimum_nights),
    "number_of_reviews": float(number_of_reviews),
    "reviews_per_month": float(reviews_per_month),
    "calculated_host_listings_count": float(calculated_host_listings_count),
    "availability_365": float(availability_365),
    "latitude": float(latitude),
    "longitude": float(longitude),
}

col1, col2 = st.columns(2)

with col1:
    if st.button("Predict"):
        r = requests.post(
            f"{API_URL}/predict/",
            headers={"X-Token": API_TOKEN},
            json=payload,
            timeout=10,
        )
        if r.status_code != 200:
            st.error(f"API error: {r.status_code} - {r.text}")
        else:
            st.success(f"Predicted price: ${r.json()['prediction']:.2f}")

with col2:
    if st.button("Run Drift Check (sample batch)"):
        # drift expects list[dict]
        batch = [payload] * 200
        r = requests.post(
            f"{API_URL}/drift/",
            headers={"X-Token": API_TOKEN},
            json=batch,
            timeout=20,
        )
        if r.status_code != 200:
            st.error(f"API error: {r.status_code} - {r.text}")
        else:
            st.json(r.json())
