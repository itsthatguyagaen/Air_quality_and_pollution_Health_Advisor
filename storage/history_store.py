import json
from pathlib import Path
from datetime import datetime

class LocationHistoryStore:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "history.json"
        self.favourites_file = self.data_dir / "favourites.json"
        self.advisories_file = self.data_dir / "advisories.json"

    def _load_json(self, path, default):
        try:
            if not path.exists():
                return default
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except (OSError, json.JSONDecodeError):
            return default

    def _save_json(self, path, data):
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def save_reading(self, reading, risk):
        history = self._load_json(self.history_file, [])
        record = reading.to_dict()
        record["risk_level"] = risk["level"]
        record["saved_at"] = datetime.now().isoformat(timespec="seconds")
        history.append(record)
        self._save_json(self.history_file, history)

    def load_history(self):
        return self._load_json(self.history_file, [])

    def save_favourite(self, location):
        favourites = self._load_json(self.favourites_file, [])
        if location not in favourites:
            favourites.append(location)
            self._save_json(self.favourites_file, favourites)

    def load_favourites(self):
        return self._load_json(self.favourites_file, [])

    def save_advisory(self, location, advisory):
        advisories = self._load_json(self.advisories_file, [])
        advisories.append({
            "location": location,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "advisory": advisory,
        })
        self._save_json(self.advisories_file, advisories)
