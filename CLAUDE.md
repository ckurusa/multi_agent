# CLAUDE.md — multi_agent 운영 가이드

오케스트레이터가 여러 전문 에이전트를 조율해 최종 답변을 생성하는 멀티 에이전트 파이프라인.

- **설계 원칙·판단 기준**: [SOUL.md](SOUL.md) — 변경 전 반드시 참조.
- **설치·사용법**: [README.md](README.md) (이 문서에 중복하지 않음).

## 핵심 파일

| 파일 | 역할 |
|------|------|
| [orchestrator.py](orchestrator.py) | 진입점. research → critique → write 파이프라인 조율 |
| [agents/base.py](agents/base.py) | `BaseAgent` — 단일 Claude 호출 래퍼 (모든 에이전트의 부모) |
| [agents/researcher.py](agents/researcher.py) | 핵심 사실·관점 수집 |
| [agents/critic.py](agents/critic.py) | 리서치 노트의 빈틈·부정확성 검토 |
| [agents/writer.py](agents/writer.py) | 리서치 + 피드백 종합해 최종 답변 작성 |
| [config.py](config.py) | 모델 ID(`claude-opus-4-8`) 및 토큰 설정 |

## 스킬

`.claude/skills/`에 자산화된 워크플로:

| 스킬 | 용도 |
|------|------|
| `issue-writer` | v0 약점을 분석해 GitHub 이슈로 등록 |
| `issue-runner` | 열린 이슈를 하나 처리하고 닫음 |
| `doc-optimizer` | CLAUDE·SOUL·README 문서를 SSOT·Minimum·Freshness 기준으로 정리 |
| `multi_agent-improver` | 위 스킬들을 하나의 개선 사이클로 묶은 통합 스킬 |

## 작업 규칙

- 새 에이전트는 `BaseAgent`를 상속해 `agents/`에 추가하고 `orchestrator.py` 파이프라인에 끼워넣는다.
- 조율 로직은 오케스트레이터에만, 에이전트는 단일 책임만 (→ [SOUL.md](SOUL.md)).
- 비밀 키는 `.env`로만 관리하고 절대 커밋하지 않는다.
- 커밋 메시지 끝에 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`를 붙인다.
