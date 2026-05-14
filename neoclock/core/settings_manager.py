import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

THEMES_FILE = Path(__file__).parent.parent / "assets" / "themes" / "presets.json"

DEFAULTS = {
    "background_color": "#0c0e14",
    "text_color": "#ece8f4",
    "font": "Consolas",
    "font_size": 72,
    "show_seconds": True,
    "format": "24h",
    "quote_date": "",
    "quote_text": "",
    "active_preset": "void",
    "audio_lofi_on": False,
    "audio_rain": "off",
    "audio_hourly_on": False,
    "audio_lofi_volume": 0.75,
    "audio_rain_volume": 0.75,
    "audio_hourly_volume": 0.75,
}

def _preset_ids(presets: dict) -> set:
    ids = set()
    for group in ("dark", "light"):
        for p in presets.get(group, []):
            ids.add(p["id"])
    return ids


class SettingsManager:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        self._data = self._load()
        self._presets = self._load_presets()
        self._ensure_valid_preset()
        self._sync_active_preset_from_file()

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

    def _ensure_valid_preset(self):
        valid = _preset_ids(self._presets)
        if not valid:
            return
        current = self._data.get("active_preset")
        if current in valid and current != "custom":
            return
        first = (self._presets.get("dark") or self._presets.get("light") or [None])[0]
        if not first:
            return
        self.apply_preset(first["id"])

    def _sync_active_preset_from_file(self):
        """Garante que fundo e texto coincidem com presets.json (corrige settings antigos)."""
        pid = self._data.get("active_preset")
        for preset in self.all_presets():
            if preset["id"] == pid:
                bg = preset["background_color"]
                fg = preset["text_color"]
                if (
                    self._data.get("background_color") != bg
                    or self._data.get("text_color") != fg
                ):
                    self._data["background_color"] = bg
                    self._data["text_color"] = fg
                    self.save()
                return

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