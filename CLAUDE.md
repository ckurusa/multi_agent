# multi_agent

오케스트레이터가 여러 전문 에이전트(Researcher · Critic · Writer)를 순서대로 조율해, 주어진 주제에 대한 최종 답변을 생성하는 멀티 에이전트 파이프라인.

## 핵심 파일

| 파일 | 역할 |
|------|------|
| [orchestrator.py](orchestrator.py) | 진입점. research → critique → write 파이프라인을 조율 |
| [agents/base.py](agents/base.py) | `BaseAgent` — 단일 Claude 호출 래퍼 (모든 에이전트의 부모) |
| [agents/researcher.py](agents/researcher.py) | 주제의 핵심 사실·관점 수집 |
| [agents/critic.py](agents/critic.py) | 리서치 노트의 빈틈·부정확성 검토 |
| [agents/writer.py](agents/writer.py) | 리서치 + 피드백을 종합해 최종 답변 작성 |
| [config.py](config.py) | 모델 ID(`claude-opus-4-8`) 및 토큰 설정 |

## 빠른 사용법

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # PowerShell: $env:ANTHROPIC_API_KEY="..."
python orchestrator.py "양자 컴퓨팅이 암호화에 미치는 영향"
```

인자를 생략하면 대화형으로 주제를 입력받습니다.

## 메모

- 모든 에이전트는 하나의 Anthropic 클라이언트를 공유합니다.
- 새 에이전트를 추가하려면 `agents/`에 `BaseAgent` 서브클래스를 만들고 `orchestrator.py`의 파이프라인에 끼워넣으세요.
