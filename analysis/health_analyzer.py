class HealthRiskAnalyzer:
    def analyze(self, reading):
        aqi = reading.aqi

        if aqi is None:
            return {
                "level": "Unknown",
                "outdoor_activity": "Use caution because AQI is unavailable.",
                "general_advice": "Some pollutant information is missing, so avoid assuming conditions are completely safe.",
                "sensitive_advice": "Sensitive people should be more cautious when pollutant data is incomplete.",
                "protection": ["Check again later when complete data is available."]
            }

        if aqi <= 20:
            level = "Good"
            outdoor = "Generally safe for outdoor activity."
            general = "Air pollution is low. Most people can carry out normal outdoor activities."
            sensitive = "Children, older adults, and people with respiratory conditions can generally enjoy normal outdoor activity, while still paying attention to symptoms."
        elif aqi <= 40:
            level = "Fair"
            outdoor = "Outdoor activity is generally okay, but sensitive people should pay attention to symptoms."
            general = "Air quality is acceptable, although some pollutants may be noticeable to sensitive people."
            sensitive = "Sensitive groups may want to reduce prolonged or intense outdoor exercise if they notice symptoms."
        elif aqi <= 60:
            level = "Moderate"
            outdoor = "Outdoor activity is possible, but consider reducing prolonged or intense exercise."
            general = "Pollution is elevated enough that some people may experience irritation."
            sensitive = "Children, older adults, and people with asthma or other respiratory conditions should consider shorter or less intense outdoor activity."
        elif aqi <= 80:
            level = "Poor"
            outdoor = "Consider limiting prolonged outdoor activity."
            general = "Air pollution is high enough that health effects are more likely, especially during strenuous activity."
            sensitive = "Sensitive groups should limit outdoor exertion and consider staying indoors when practical."
        else:
            level = "Very poor"
            outdoor = "Avoid prolonged outdoor activity where possible."
            general = "Air pollution is very high and outdoor exposure should be minimized."
            sensitive = "Sensitive groups should avoid strenuous outdoor activity and follow advice from their healthcare professionals."

        protection = [
            "Reduce long or intense outdoor exercise when pollution is elevated.",
            "Keep windows closed during periods of poor outdoor air if practical.",
            "Improve indoor ventilation when outdoor air is cleaner.",
            "If you use a mask for pollution, a well-fitting particulate respirator is more protective than a loose cloth mask.",
            "People with respiratory conditions should follow their personal medical action plan."
        ]

        return {
            "level": level,
            "outdoor_activity": outdoor,
            "general_advice": general,
            "sensitive_advice": sensitive,
            "protection": protection
        }
