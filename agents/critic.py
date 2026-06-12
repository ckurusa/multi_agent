"""Critic — reviews research notes for gaps and weak claims."""
from __future__ import annotations

from agents.base import BaseAgent


class Critic(BaseAgent):
    name = "critic"
    system = (
        "You are a critic agent. You review research notes for gaps, inaccuracies, "
        "missing perspectives, and unsupported claims. Return a short, concrete list "
        "of improvements the writer should incorporate. Be specific; do not rewrite "
        "the notes yourself."
    )

    def run(self, topic: str, research: str, **kwargs) -> str:
        prompt = (
            f"Topic:\n{topic}\n\n"
            f"Research notes:\n{research}\n\n"
            "Critique these notes and list concrete improvements."
        )
        return self._complete(prompt, **kwargs)
