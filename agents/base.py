"""BaseAgent — a thin wrapper around a single Claude call.

Each concrete agent sets its own ``name`` and ``system`` prompt and shapes the
user prompt in its ``run`` method. All agents share one Anthropic client so the
orchestrator can reuse a single connection.
"""
from __future__ import annotations

import anthropic

from config import MAX_RETRIES, MAX_TOKENS, MODEL


class BaseAgent:
    name: str = "base"
    system: str = "You are a helpful assistant."

    def __init__(self, client: anthropic.Anthropic | None = None) -> None:
        # A bare Anthropic() resolves ANTHROPIC_API_KEY from the environment.
        self.client = client or anthropic.Anthropic(max_retries=MAX_RETRIES)

    def _complete(self, prompt: str, max_tokens: int | None = None) -> str:
        response = self.client.messages.create(
            model=MODEL,
            max_tokens=max_tokens or MAX_TOKENS,
            system=self.system,
            messages=[{"role": "user", "content": prompt}],
        )
        # response.content is a list of content blocks; keep the text ones.
        return "".join(b.text for b in response.content if b.type == "text").strip()

    def run(self, prompt: str, **kwargs) -> str:
        """Default behavior: send the prompt as-is. Subclasses override this."""
        return self._complete(prompt, **kwargs)
