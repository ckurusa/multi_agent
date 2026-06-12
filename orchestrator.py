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

from agents.critic import Critic
from agents.researcher import Researcher
from agents.writer import Writer


class Orchestrator:
    """Coordinates the three agents in a fixed pipeline."""

    def __init__(self) -> None:
        client = anthropic.Anthropic()  # one shared client for all agents
        self.researcher = Researcher(client)
        self.critic = Critic(client)
        self.writer = Writer(client)

    def run(self, topic: str) -> dict[str, str]:
        print("[1/3] researcher 실행 중...", file=sys.stderr)
        research = self.researcher.run(topic)

        print("[2/3] critic 실행 중...", file=sys.stderr)
        critique = self.critic.run(topic, research)

        print("[3/3] writer 실행 중...", file=sys.stderr)
        answer = self.writer.run(topic, research, critique)

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
    except anthropic.AuthenticationError:
        print(
            "인증 실패: ANTHROPIC_API_KEY 환경 변수가 설정되어 있는지 확인하세요.",
            file=sys.stderr,
        )
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
