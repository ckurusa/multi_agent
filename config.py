"""Shared configuration for the multi_agent pipeline."""
import os

# Default to the latest, most capable Claude model. Override with MULTI_AGENT_MODEL.
MODEL = os.environ.get("MULTI_AGENT_MODEL", "claude-opus-4-8")

# Per-agent output cap. Keep under the SDK's non-streaming timeout guard (~16K).
MAX_TOKENS = int(os.environ.get("MULTI_AGENT_MAX_TOKENS", "2000"))

# SDK auto-retries 429 / 5xx / connection errors with backoff. Default is 2.
MAX_RETRIES = int(os.environ.get("MULTI_AGENT_MAX_RETRIES", "2"))
