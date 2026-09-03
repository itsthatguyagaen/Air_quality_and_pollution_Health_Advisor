from datetime import datetime

class ForecastAnalyzer:
    def best_time(self, reading):
        candidates = [
            item for item in reading.forecast
            if item.get("aqi") is not None
        ]

        if not candidates:
            return None

        # Prefer daytime hours, because the user is asking when to go outside.
        daytime = []
        for item in candidates:
            try:
                hour = datetime.fromisoformat(item["time"]).hour
                if 6 <= hour <= 18:
                    daytime.append(item)
            except (ValueError, TypeError):
                continue

        pool = daytime or candidates
        best = min(pool, key=lambda x: x["aqi"])

        try:
            dt = datetime.fromisoformat(best["time"])
            return f"{dt.strftime('%A, %B %d at %I:%M %p')} (forecast AQI: {best['aqi']:.0f})"
        except (ValueError, TypeError):
            return f"{best['time']} (forecast AQI: {best['aqi']})"
