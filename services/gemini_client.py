import requests

class GeminiError(Exception):
    pass

class GeminiClient:
    # Uses Gemini's REST API so the project only needs requests.
    URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    def __init__(self, api_key):
        self.api_key = api_key.strip()

    def generate_advice(self, reading, risk):
        prompt = f"""
You are an air-quality health education assistant.

Location: {reading.location}, {reading.country}
European AQI: {reading.aqi}
PM2.5: {reading.pm25} µg/m³
PM10: {reading.pm10} µg/m³
Ozone: {reading.ozone} µg/m³
Nitrogen dioxide: {reading.no2} µg/m³
Program risk category: {risk['level']}

Explain these numbers in simple language for an ordinary person.
Explain what they mean for:
1. healthy adults
2. children
3. older adults
4. people with asthma or other respiratory conditions

Give practical advice about outdoor activity, windows/indoor air, and reducing exposure.
Do not diagnose anyone or claim the advice replaces medical care.
Keep the answer concise and easy to read.
"""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            response = requests.post(
                self.URL,
                params={"key": self.api_key},
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise GeminiError(f"Gemini request failed: {e}") from e
        except ValueError as e:
            raise GeminiError("Gemini returned invalid JSON.") from e

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            raise GeminiError("Gemini returned an unexpected response.")
