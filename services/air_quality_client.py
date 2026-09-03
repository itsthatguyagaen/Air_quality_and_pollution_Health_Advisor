import requests
from datetime import datetime
from models.air_reading import AirReading

class AirQualityError(Exception):
    pass

class AirQualityClient:
    BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    def get_current_and_forecast(self, latitude, longitude, location, country):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "european_aqi,pm2_5,pm10,ozone,nitrogen_dioxide",
            "forecast_days": 3,
            "timezone": "auto",
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise AirQualityError(f"Air-quality request failed: {e}") from e
        except ValueError as e:
            raise AirQualityError("Air-quality API returned invalid JSON.") from e

        hourly = data.get("hourly", {})
        times = hourly.get("time", [])

        if not times:
            raise AirQualityError("The API returned no hourly air-quality data.")

        def value_at(index, key):
            values = hourly.get(key, [])
            return values[index] if index < len(values) else None

        # Find the hour closest to the API's current time.
        current_time = data.get("current", {}).get("time")
        index = 0
        if current_time and current_time in times:
            index = times.index(current_time)

        forecast = []
        for i, time in enumerate(times):
            forecast.append({
                "time": time,
                "aqi": value_at(i, "european_aqi"),
                "pm25": value_at(i, "pm2_5"),
                "pm10": value_at(i, "pm10"),
                "ozone": value_at(i, "ozone"),
                "no2": value_at(i, "nitrogen_dioxide"),
            })

        return AirReading(
            location=location,
            country=country,
            latitude=latitude,
            longitude=longitude,
            measured_at=times[index],
            aqi=value_at(index, "european_aqi"),
            pm25=value_at(index, "pm2_5"),
            pm10=value_at(index, "pm10"),
            ozone=value_at(index, "ozone"),
            no2=value_at(index, "nitrogen_dioxide"),
            forecast=forecast,
        )
