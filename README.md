# multi_agent

> 오케스트레이터가 Researcher · Critic · Writer 에이전트를 순서대로 조율해, 주어진 주제에 대한 최종 답변을 만드는 멀티 에이전트 파이프라인.

## 설치

```bash
pip install -r requirements.txt
```

API 키를 환경 변수로 설정합니다:

```bash
# macOS / Linux
export ANTHROPIC_API_KEY=...
# Windows PowerShell
$env:ANTHROPIC_API_KEY="..."
```

(또는 `.env.example`을 `.env`로 복사해 채워 넣으세요.)

## 사용법

```bash
python orchestrator.py "양자 컴퓨팅이 암호화에 미치는 영향"
```

인자를 생략하면 대화형으로 주제를 입력받습니다.

진행 로그는 `stderr`로, 최종 답변은 `stdout`으로 출력됩니다.

### 옵션

| 플래그 | 설명 |
|--------|------|
| `-v`, `--verbose` | research·critique 중간 단계 결과도 함께 출력 |
| `--json` | 전체 result(topic/research/critique/answer)를 JSON으로 출력 |

```bash
python orchestrator.py --verbose "양자 컴퓨팅이 암호화에 미치는 영향"
python orchestrator.py --json "..." > result.json
```

## 파일 구조

```
orchestrator.py      진입점 — research → critique → write 파이프라인 조율
agents/
  base.py            BaseAgent (단일 Claude 호출 래퍼)
  researcher.py      핵심 사실·관점 수집
  critic.py          리서치 노트 검토
  writer.py          최종 답변 작성
config.py            모델 ID·토큰 설정
```

## 더 보기

- 설계 원칙: [SOUL.md](SOUL.md)
- 에이전트 운영 가이드: [CLAUDE.md](CLAUDE.md)
