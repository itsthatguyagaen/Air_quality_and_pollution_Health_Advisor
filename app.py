import streamlit as st
from datetime import datetime

from services.location_client import LocationClient, LocationError
from services.air_quality_client import AirQualityClient, AirQualityError
from services.gemini_client import GeminiClient, GeminiError
from analysis.health_analyzer import HealthRiskAnalyzer
from analysis.forecast_analyzer import ForecastAnalyzer
from storage.history_store import LocationHistoryStore
from models.air_reading import AirReading


st.set_page_config(page_title="Air Quality Health Advisor", page_icon="🌍", layout="wide")

location_client = LocationClient()
air_client = AirQualityClient()
health_analyzer = HealthRiskAnalyzer()
forecast_analyzer = ForecastAnalyzer()
history_store = LocationHistoryStore()

@st.cache_data(ttl=600)
def get_reading(location_name):
    location = location_client.search(location_name)
    return air_client.get_current_and_forecast(
        location["latitude"], location["longitude"], location["name"], location["country"]
    )

def display_reading(reading):
    risk = health_analyzer.analyze(reading)

    st.subheader(f"🌍 {reading.location}, {reading.country}")
    cols = st.columns(5)
    cols[0].metric("European AQI", reading.aqi if reading.aqi is not None else "N/A")
    cols[1].metric("PM2.5", f"{reading.pm25:.1f} µg/m³" if reading.pm25 is not None else "N/A")
    cols[2].metric("PM10", f"{reading.pm10:.1f} µg/m³" if reading.pm10 is not None else "N/A")
    cols[3].metric("Ozone", f"{reading.ozone:.1f} µg/m³" if reading.ozone is not None else "N/A")
    cols[4].metric("NO₂", f"{reading.no2:.1f} µg/m³" if reading.no2 is not None else "N/A")

    if risk["level"] == "Good":
        st.success(f"🟢 {risk['level']}: {risk['outdoor_activity']}")
    elif risk["level"] == "Moderate":
        st.warning(f"🟡 {risk['level']}: {risk['outdoor_activity']}")
    else:
        st.error(f"🔴 {risk['level']}: {risk['outdoor_activity']}")

    st.write("### 🩺 Health advice")
    st.write(risk["general_advice"])

    st.write("**Sensitive groups:**")
    st.write(risk["sensitive_advice"])

    best = forecast_analyzer.best_time(reading)
    st.write("### 🌤️ Cleanest time to go outside")
    if best:
        st.info(best)
    else:
        st.info("There is not enough hourly data to determine a cleanest time.")

    st.write("### 🛡️ Simple protective steps")
    for item in risk["protection"]:
        st.write(f"- {item}")

    with st.expander("View hourly forecast"):
        if reading.forecast:
            rows = []
            for item in reading.forecast[:48]:
                rows.append({
                    "Time": item["time"],
                    "AQI": item.get("aqi"),
                    "PM2.5": item.get("pm25"),
                    "PM10": item.get("pm10"),
                    "Ozone": item.get("ozone"),
                    "NO₂": item.get("no2"),
                })
            st.dataframe(rows, use_container_width=True)
        else:
            st.write("No forecast data available.")

    return risk


st.title("🌍 Air Quality & Pollution Health Advisor")
st.caption("Current conditions, forecasts, health guidance, comparisons and local history.")

tab1, tab2, tab3 = st.tabs(["🔎 Check air quality", "⚖️ Compare locations", "⭐ Favourites & history"])

with tab1:
    location_input = st.text_input("Enter a city or location", placeholder="e.g. Abuja")

    if st.button("Check air quality", type="primary"):
        if not location_input.strip():
            st.error("Please enter a location.")
        else:
            try:
                with st.spinner("Getting air-quality data..."):
                    reading = get_reading(location_input.strip())
                risk = display_reading(reading)
                history_store.save_reading(reading, risk)
                st.session_state["last_reading"] = reading
            except (LocationError, AirQualityError) as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Unexpected error: {e}")

with tab2:
    c1, c2 = st.columns(2)
    loc1 = c1.text_input("Location 1", placeholder="Abuja", key="compare1")
    loc2 = c2.text_input("Location 2", placeholder="Lagos", key="compare2")

    if st.button("Compare", type="primary"):
        if not loc1.strip() or not loc2.strip():
            st.error("Enter both locations.")
        else:
            try:
                with st.spinner("Comparing locations..."):
                    r1 = get_reading(loc1.strip())
                    r2 = get_reading(loc2.strip())

                st.subheader("Comparison")
                comparison = st.columns(2)
                for col, reading in zip(comparison, [r1, r2]):
                    with col:
                        st.write(f"### {reading.location}, {reading.country}")
                        st.metric("European AQI", reading.aqi if reading.aqi is not None else "N/A")
                        st.metric("PM2.5", f"{reading.pm25:.1f} µg/m³" if reading.pm25 is not None else "N/A")
                        st.metric("PM10", f"{reading.pm10:.1f} µg/m³" if reading.pm10 is not None else "N/A")

                if r1.aqi is not None and r2.aqi is not None:
                    better = r1.location if r1.aqi < r2.aqi else r2.location if r2.aqi < r1.aqi else "Both locations"
                    st.success(f"Cleaner right now: **{better}**")
            except (LocationError, AirQualityError) as e:
                st.error(str(e))

with tab3:
    st.subheader("⭐ Favourite locations")
    favourites = history_store.load_favourites()

    if favourites:
        for fav in favourites:
            st.write(f"• {fav}")
    else:
        st.write("No favourites yet.")

    new_favourite = st.text_input("Add a favourite location", key="fav_input")
    if st.button("Save favourite"):
        if new_favourite.strip():
            history_store.save_favourite(new_favourite.strip())
            st.success("Favourite saved.")
            st.rerun()

    st.subheader("📈 Past readings")
    history = history_store.load_history()
    if history:
        st.dataframe(history, use_container_width=True)
    else:
        st.write("No saved readings yet.")

    st.subheader("🤖 AI explanation")
    api_key = st.text_input("Gemini API key (optional)", type="password")
    selected_location = st.text_input("Location to explain", key="ai_location")

    if st.button("Generate AI explanation"):
        if not api_key:
            st.warning("Enter your Gemini API key first.")
        elif not selected_location.strip():
            st.warning("Enter a location first.")
        else:
            try:
                with st.spinner("Asking Gemini..."):
                    reading = get_reading(selected_location.strip())
                    risk = health_analyzer.analyze(reading)
                    explanation = GeminiClient(api_key).generate_advice(reading, risk)
                st.markdown(explanation)
                history_store.save_advisory(reading.location, explanation)
            except (LocationError, AirQualityError, GeminiError) as e:
                st.error(str(e))

st.divider()
st.caption("Group 27 Air Quality and Pollution Helath Advisor")
