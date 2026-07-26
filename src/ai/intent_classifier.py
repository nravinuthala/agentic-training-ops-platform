from __future__ import annotations

import json
import logging
import os
from typing import Any

from pydantic import BaseModel, Field

from src.ai.prompts import INTENT_PROMPT

logger = logging.getLogger(__name__)


class UserIntent(BaseModel):
    """Structured intent from a user question."""

    intent_type: str = Field(..., description="Supported intent name")
    entity: str | None = Field(default=None, description="Extracted entity or skill")
    entity_code: str | None = Field(default=None, description="Extracted entity code if present")
    confidence: float = Field(default=0.0, description="Confidence score")


class IntentClassifier:
    """Classifies a natural-language question into a supported business intent."""

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self._client = None

    def classify(self, question: str) -> UserIntent:
        """Classify the question and return a structured intent model."""
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        should_use_llm = bool(api_key and base_url and api_key != "demo-key")

        if should_use_llm:
            try:
                from langchain_openai import ChatOpenAI
                from langchain_core.messages import HumanMessage
            except ImportError as exc:
                raise RuntimeError("LangChain/OpenAI dependencies are not available") from exc

            if self._client is None:
                self._client = ChatOpenAI(
                    model=self.model_name,
                    temperature=0.0,
                    api_key=api_key,
                    base_url=base_url,
                )

            prompt = f"{INTENT_PROMPT}\n\nUser question: {question}"
            response = self._client.invoke([HumanMessage(content=prompt)])
            content = response.content if hasattr(response, "content") else str(response)

            try:
                parsed = json.loads(content)
                return UserIntent(**parsed)
            except (TypeError, json.JSONDecodeError) as exc:
                logger.warning("Falling back to heuristic classifier: %s", exc)

        return self._heuristic_classify(question)

    def _heuristic_classify(self, question: str) -> UserIntent:
        text = question.lower().strip()
        entity = self._extract_entity(question)
        entity_code = self._extract_entity_code(question)

        if any(keyword in text for keyword in ["who are the experts", "experts in", "expert in"]):
            return UserIntent(intent_type="EXPERT_SEARCH", entity=entity, entity_code=entity_code, confidence=0.7)
        if any(keyword in text for keyword in ["show profile", "tell me about trainer", "trainer profile", "show trainer"]):
            return UserIntent(intent_type="TRAINER_PROFILE", entity=entity, entity_code=entity_code, confidence=0.8)
        if any(keyword in text for keyword in ["recommend", "best trainer", "who should teach"]):
            return UserIntent(intent_type="TRAINER_RECOMMENDATION", entity=entity, entity_code=entity_code, confidence=0.7)
        if any(keyword in text for keyword in ["teach"]):
            if entity_code and entity_code.startswith("CRS"):
                return UserIntent(intent_type="TRAINER_RECOMMENDATION", entity=entity, entity_code=entity_code, confidence=0.7)
            return UserIntent(intent_type="TRAINER_SEARCH", entity=entity, entity_code=entity_code, confidence=0.75)
        if any(keyword in text for keyword in ["course", "courses", "show", "list"]):
            if entity_code and entity_code.startswith("CRS"):
                return UserIntent(intent_type="COURSE_PROFILE", entity=entity, entity_code=entity_code, confidence=0.8)
            if any(keyword in text for keyword in ["terraform", "kubernetes", "azure", "devops", "python", "java", "aws", "cloud", "security", "ml", "ai"]):
                return UserIntent(intent_type="COURSE_SEARCH", entity=self._extract_skill(text), entity_code=entity_code, confidence=0.8)
            return UserIntent(intent_type="COURSE_SEARCH", entity=entity, entity_code=entity_code, confidence=0.7)
        if any(keyword in text for keyword in ["who knows", "find trainers", "can teach", "trainer for", "trainers for"]):
            return UserIntent(intent_type="TRAINER_SEARCH", entity=entity, entity_code=entity_code, confidence=0.8)
        return UserIntent(intent_type="TRAINER_SEARCH", entity=entity, entity_code=entity_code, confidence=0.5)

    def _extract_entity(self, question: str) -> str | None:
        import re

        code_matches = re.findall(r"\b(?:CRS|TRN)[A-Z0-9]+\b", question.upper())
        if code_matches:
            return code_matches[0]

        text = question.strip()
        if not text:
            return None

        for prefix in [
            "who can teach ",
            "who knows ",
            "find trainers for ",
            "find trainer for ",
            "who are the experts in ",
            "experts in ",
            "expert in ",
            "show profile for ",
            "show trainer ",
            "show course ",
            "show courses ",
            "show ",
            "list ",
            "find ",
            "search ",
            "recommend trainer for ",
            "who should teach ",
            "best trainer for ",
            "tell me about trainer ",
            "tell me about ",
            "for ",
        ]:
            if text.lower().startswith(prefix):
                text = text[len(prefix) :].strip()
                break

        text = text.rstrip("?.")
        lowered = text.lower()
        for suffix in [" courses", " course", " trainers", " trainer"]:
            if lowered.endswith(suffix):
                text = text[: -len(suffix)].strip()
                lowered = text.lower()
                break
        return text or None

    def _extract_entity_code(self, question: str) -> str | None:
        import re

        code_matches = re.findall(r"\b(?:CRS|TRN)[A-Z0-9]+\b", question.upper())
        if code_matches:
            return code_matches[0]
        return None

    def _extract_skill(self, question: str) -> str | None:
        lowered = question.lower()
        for keyword in ["terraform", "kubernetes", "azure", "devops", "python", "java", "aws", "cloud", "security", "ml", "ai"]:
            if keyword in lowered:
                return keyword.capitalize()
        return None
