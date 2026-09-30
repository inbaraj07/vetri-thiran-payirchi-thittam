import json
import re
from typing import Any
from app.config import get_settings
from app.models import RecommendationResponse
from app.services.fallback import home_fallback, party_fallback, jewelry_fallback

class GeminiService:
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        if self.settings.gemini_api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.settings.gemini_api_key)
            except Exception:
                self.client = None

    @property
    def enabled(self):
        return self.client is not None

    def prompt(self, planner: str, data: dict, image: bool = False) -> str:
        schema = json.dumps(RecommendationResponse.model_json_schema(), ensure_ascii=False)
        return (
            "You are PocketSmart AI, a budget-aware recommendation assistant.\n"
            f"Planner: {planner}\n"
            f"User input:\n{json.dumps(data, ensure_ascii=False, indent=2)}\n"
            f"Return ONLY valid JSON matching this schema:\n{schema}\n"
            "Rules: respect the total budget; recommendation prices must fit the plan; "
            "give practical reasons; platforms must be Amazon, Flipkart, IKEA, Swiggy, "
            "Zomato or OYO where relevant; generate search links only; never claim live "
            "stock or live prices; clearly state that prices are estimates; for jewelry "
            f"use outfit text and image context when supplied. Image supplied: {image}"
        )

    def generate(self, planner: str, data: dict, image_bytes: bytes | None = None, mime_type: str | None = None):
        if not self.enabled:
            return self.fallback(planner, data, bool(image_bytes))
        try:
            from google.genai import types
            contents: list[Any] = [self.prompt(planner, data, bool(image_bytes))]
            if image_bytes:
                contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type or "image/jpeg"))
            response = self.client.models.generate_content(
                model=self.settings.gemini_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RecommendationResponse,
                    temperature=0.3,
                    max_output_tokens=4096,
                ),
            )
            result = RecommendationResponse.model_validate_json(self.clean(response.text or ""))
            return result.model_copy(update={"ai_generated": True})
        except Exception:
            return self.fallback(planner, data, bool(image_bytes))

    @staticmethod
    def clean(text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        return text

    @staticmethod
    def fallback(planner: str, data: dict, has_image: bool):
        if planner == "home":
            return home_fallback(data)
        if planner == "party":
            return party_fallback(data)
        return jewelry_fallback(data, has_image)
