"""Writer — produces the final answer from research + critique."""
from __future__ import annotations

from agents.base import BaseAgent


class Writer(BaseAgent):
    name = "writer"
    system = (
        "You are a writer agent. Using the research notes and the critic's feedback, "
        "write a clear, accurate, well-organized final answer for the user. "
        "Incorporate the critic's improvements. Lead with the outcome, then supporting "
        "detail. Do not mention the agents or this process."
    )

    def run(self, topic: str, research: str, critique: str, **kwargs) -> str:
        prompt = (
            f"Topic:\n{topic}\n\n"
            f"Research notes:\n{research}\n\n"
            f"Critic feedback:\n{critique}\n\n"
            "Write the final answer."
        )
        return self._complete(prompt, **kwargs)
