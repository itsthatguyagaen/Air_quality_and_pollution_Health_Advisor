# Air Quality & Pollution Health Advisor

A Python + Streamlit application that retrieves air-quality data from Open-Meteo, analyzes the conditions, saves local history/favourites, compares locations, finds a cleaner forecast time, and optionally uses Gemini to explain the readings.

## Features

- Search a location by name
- Current/forecast PM2.5, PM10, ozone, NO2 and European AQI
- Health-risk interpretation
- Guidance for sensitive groups
- Cleanest daytime forecast time
- Protective advice
- Compare two locations
- Save favourite locations locally
- Save past readings locally as JSON
- Generate AI explanations with Gemini
- Exception handling for network/API/JSON problems
- Regular-expression validation for location input
- OOP with separate client, model, analyzer and storage classes

## Setup

Create and activate your virtual environment, then:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## Gemini

Gemini is optional for the rest of the application. To use the AI explanation feature, provide a Gemini API key in the Streamlit interface.

## Important

The application uses the European AQI returned by Open-Meteo. AQI scales differ between countries, so the label "European AQI" is intentional.

The health guidance is educational and should not replace professional medical advice.
