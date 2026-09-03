from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class AirReading:
    location: str
    country: str
    latitude: float
    longitude: float
    measured_at: str
    aqi: Optional[float]
    pm25: Optional[float]
    pm10: Optional[float]
    ozone: Optional[float]
    no2: Optional[float]
    forecast: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self):
        return {
            "location": self.location,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "measured_at": self.measured_at,
            "aqi": self.aqi,
            "pm25": self.pm25,
            "pm10": self.pm10,
            "ozone": self.ozone,
            "no2": self.no2,
        }
