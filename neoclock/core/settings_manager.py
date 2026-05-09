import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

THEMES_FILE = Path(__file__).parent.parent / "assets" / "themes" / "presets.json"

DEFAULTS = {
    "background_color": "#0f0f1a",
    "text_color": "#e0d9f5",
    "font": "Consolas",
    "font_size": 72,
    "show_seconds": True,
    "format": "24h",
    "quote_date": "",
    "quote_text": "",
    "active_preset": "void",
}

class SettingsManager:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        self._data = self._load()
        self._presets = self._load_presets()

    def _load(self) -> dict:
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return {**DEFAULTS, **data}
            except (json.JSONDecodeError, OSError):
                pass
        return DEFAULTS.copy()

    def _load_presets(self) -> dict:
        if THEMES_FILE.exists():
            try:
                with open(THEMES_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {"dark": [], "light": []}

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

    def all_presets(self) -> list:
        return self._presets.get("dark", []) + self._presets.get("light", [])

    def apply_preset(self, preset_id: str):
        for preset in self.all_presets():
            if preset["id"] == preset_id:
                self._data["background_color"] = preset["background_color"]
                self._data["text_color"] = preset["text_color"]
                self._data["active_preset"] = preset_id
                self.save()
                return

    def presets_by_group(self) -> dict:
        return self._presets