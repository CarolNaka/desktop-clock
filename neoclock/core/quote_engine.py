import os
import random
from datetime import date
from dotenv import load_dotenv
from google import genai

load_dotenv()

IDIOMAS = ["português", "inglês"]

class QuoteEngine:
    def __init__(self, settings_manager):
        self.sm = settings_manager

        api_key = os.getenv("GEMINI_API_KEY")

        print(
            f"[QuoteEngine] API key carregada: "
            f"{'OK' if api_key else 'NÃO ENCONTRADA'}"
        )

        self.client = genai.Client(api_key=api_key)

    def obter_frase(self) -> str:
        hoje = str(date.today())

        print(
            f"[QuoteEngine] Hoje: {hoje} | "
            f"quote_date salvo: {self.sm.get('quote_date')}"
        )

        if self.sm.get("quote_date") == hoje:
            print("[QuoteEngine] Reutilizando frase do dia.")
            return self.sm.get("quote_text") or ""

        print("[QuoteEngine] Gerando nova frase...")

        frase = self._gerar()

        print(f"[QuoteEngine] Frase gerada: {frase}")

        self.sm.set("quote_date", hoje)
        self.sm.set("quote_text", frase)

        return frase

    def _gerar(self) -> str:
        idioma = random.choice(IDIOMAS)

        prompt = (
            f"Gere uma única frase filosófica curta e reflexiva em {idioma}. "
            "Deve ser original, profunda e inspiradora. "
            "Responda apenas com a frase, sem aspas, sem autor, sem explicação."
        )

        try:
            resposta = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
)

            print("[QuoteEngine] Resposta completa:", resposta)

            if hasattr(resposta, "text") and resposta.text:
                return resposta.text.strip()

            return "Nenhuma frase disponível."

        except Exception as e:
            print("[QuoteEngine] Erro Gemini:", e)
            return "O silêncio também responde."