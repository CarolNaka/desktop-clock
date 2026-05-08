import json
from pathlib import Path

# Localiza a pasta data/ relativa a este arquivo
DATA_DIR = Path(__file__).parent.parent / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULTS = {
    "cor_fundo": "#1a1a2e",
    "cor_texto": "#e0e0e0",
    "fonte": "Consolas",
    "tamanho_fonte": 72,
    "mostrar_segundos": True,
    "formato": "24h",
    "quote_date": "",
    "quote_text": "" 
}

class SettingsManager:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        self._data = self._carregar()

    def _carregar(self) -> dict:
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                # Garante que chaves novas do DEFAULTS existam
                return {**DEFAULTS, **dados}
            except (json.JSONDecodeError, OSError):
                pass
        return DEFAULTS.copy()

    def salvar(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)

    def get(self, chave: str):
        return self._data.get(chave, DEFAULTS.get(chave))

    def set(self, chave: str, valor):
        self._data[chave] = valor
        self.salvar()

    def all(self) -> dict:
        return self._data.copy()