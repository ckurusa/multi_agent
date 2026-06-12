"""Researcher — gathers key facts and angles for a topic."""
from __future__ import annotations

from agents.base import BaseAgent


class Researcher(BaseAgent):
    name = "researcher"
    system = (
        "You are a research agent. Given a topic or question, produce a concise, "
        "well-structured set of key facts, considerations, and distinct angles. "
        "Use bullet points. Be factual, cite reasoning, and explicitly flag any "
        "claim you are uncertain about."
    )

    def run(self, topic: str, **kwargs) -> str:
        prompt = f"Research the following topic and list the key points:\n\n{topic}"
        return self._complete(prompt, **kwargs)
