"""Orchestrator — runs the research -> critique -> write pipeline.

Usage:
    python orchestrator.py "your topic or question"
    python orchestrator.py            # interactive prompt

Requires ANTHROPIC_API_KEY in the environment.
"""
from __future__ import annotations

import argparse
import json
import sys

import anthropic

# Windows consoles default to a legacy codepage (e.g. cp949) that can't encode
# characters the model may emit (em-dash, smart quotes). Force UTF-8 output.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

from config import MAX_RETRIES
from agents.critic import Critic
from agents.researcher import Researcher
from agents.writer import Writer


class PipelineError(RuntimeError):
    """An agent's API call failed. Carries which stage failed and the cause."""

    def __init__(self, stage: str, original: Exception) -> None:
        self.stage = stage
        self.original = original
        super().__init__(f"{stage} 단계 실패: {original}")


class Orchestrator:
    """Coordinates the three agents in a fixed pipeline."""

    def __init__(self) -> None:
        # One shared client for all agents; SDK retries 429/5xx/connection errors.
        client = anthropic.Anthropic(max_retries=MAX_RETRIES)
        self.researcher = Researcher(client)
        self.critic = Critic(client)
        self.writer = Writer(client)

    def _stage(self, label: str, fn, *args):
        print(f"{label} 실행 중...", file=sys.stderr)
        try:
            return fn(*args)
        except anthropic.APIError as err:
            # Re-raise with the failing stage's name so the caller can report it.
            raise PipelineError(label, err) from err

    def run(self, topic: str) -> dict[str, str]:
        research = self._stage("[1/3] researcher", self.researcher.run, topic)
        critique = self._stage("[2/3] critic", self.critic.run, topic, research)
        answer = self._stage("[3/3] writer", self.writer.run, topic, research, critique)

        return {
            "topic": topic,
            "research": research,
            "critique": critique,
            "answer": answer,
        }


def _section(title: str, body: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(body)


def _friendly_error(err: Exception) -> str:
    """Map an Anthropic API error to a short, actionable message."""
    if isinstance(err, anthropic.AuthenticationError):
        return "인증 실패: ANTHROPIC_API_KEY 환경 변수를 확인하세요."
    if isinstance(err, anthropic.RateLimitError):
        return "요청 한도 초과(rate limit). 잠시 후 다시 시도하세요."
    if isinstance(err, anthropic.APIConnectionError):
        return "네트워크 연결 오류. 인터넷 연결을 확인하세요."
    if isinstance(err, anthropic.APIStatusError):
        return f"API 오류 (status {err.status_code}): {err.message}"
    return str(err)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="멀티 에이전트 파이프라인 (research → critique → write)"
    )
    parser.add_argument("topic", nargs="*", help="주제/질문 (생략 시 대화형 입력)")
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="research·critique 중간 단계 결과도 함께 출력",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="전체 result(딕셔너리)를 JSON으로 출력",
    )
    args = parser.parse_args()

    topic = " ".join(args.topic).strip() or input("주제/질문을 입력하세요: ").strip()
    if not topic:
        print("주제가 비어 있습니다. 입력 후 다시 실행하세요.")
        return

    try:
        result = Orchestrator().run(topic)
    except PipelineError as e:
        print(f"{e.stage} 단계에서 실패 — {_friendly_error(e.original)}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.verbose:
        _section("[research] 리서치 노트", result["research"])
        _section("[critique] 비평", result["critique"])
    _section("최종 답변", result["answer"])


if __name__ == "__main__":
    main()
