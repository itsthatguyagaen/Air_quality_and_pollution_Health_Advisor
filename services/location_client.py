import re
import requests

class LocationError(Exception):
    pass

class LocationClient:
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    def search(self, location):
        if not isinstance(location, str) or not location.strip():
            raise LocationError("Location cannot be empty.")

        if not re.fullmatch(r"[A-Za-zÀ-ÿ0-9 .,'’()\-]{2,100}", location.strip()):
            raise LocationError("Please enter a valid location name.")

        try:
            response = requests.get(
                self.BASE_URL,
                params={"name": location.strip(), "count": 1, "language": "en", "format": "json"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise LocationError(f"Could not contact the location service: {e}") from e
        except ValueError as e:
            raise LocationError("The location service returned invalid JSON.") from e

        results = data.get("results")
        if not results:
            raise LocationError(f"Could not find '{location}'.")

        result = results[0]
        return {
            "name": result.get("name", location.strip()),
            "country": result.get("country", ""),
            "latitude": float(result["latitude"]),
            "longitude": float(result["longitude"]),
        }
