import os
import random
from datetime import date
from dotenv import load_dotenv
from google import genai

load_dotenv()

LANGUAGES = ["Portuguese", "English"]

class QuoteEngine:
    def __init__(self, settings_manager):
        self.sm = settings_manager

        api_key = os.getenv("GEMINI_API_KEY")

        print(
            f"[QuoteEngine] API key loaded: "
            f"{'OK' if api_key else 'NOT FOUND'}"
        )

        self.client = genai.Client(api_key=api_key)

    def get_quote(self) -> str:
        today = str(date.today())

        print(
            f"[QuoteEngine] Today: {today} | "
            f"saved quote_date: {self.sm.get('quote_date')}"
        )

        if self.sm.get("quote_date") == today:
            print("[QuoteEngine] Reusing today's quote.")
            return self.sm.get("quote_text") or ""

        print("[QuoteEngine] Generating new quote...")

        quote = self._generate()

        print(f"[QuoteEngine] Generated quote: {quote}")

        self.sm.set("quote_date", today)
        self.sm.set("quote_text", quote)

        return quote

    def _generate(self) -> str:
        language = random.choice(LANGUAGES)

        prompt = (
            f"Generate a single short and reflective philosophical quote in {language}. "
            "It must be original, deep, and inspiring. "
            "Reply only with the quote, without quotation marks, without author, and without explanation."
        )

        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            print("[QuoteEngine] Full response:", response)

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            return "No quote available."

        except Exception as e:
            print("[QuoteEngine] Gemini error:", e)
            return "Silence also answers."