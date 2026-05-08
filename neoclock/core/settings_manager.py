import json
from pathlib import Path

# Locate the data/ folder relative to this file
DATA_DIR = Path(__file__).parent.parent / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULTS = {
    "background_color": "#1a1a2e",
    "text_color": "#e0e0e0",
    "font": "Consolas",
    "font_size": 72,
    "show_seconds": True,
    "format": "24h",
    "quote_date": "",
    "quote_text": ""
}

class SettingsManager:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        self._data = self._load()

    def _load(self) -> dict:
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Ensure new keys from DEFAULTS exist
                return {**DEFAULTS, **data}

            except (json.JSONDecodeError, OSError):
                pass

        return DEFAULTS.copy()

    def save(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)

    def get(self, key: str):
        return self._data.get(key, DEFAULTS.get(key))

    def set(self, key: str, value):
        self._data[key] = value
        self.save()

    def all(self) -> dict:
        return self._data.copy()