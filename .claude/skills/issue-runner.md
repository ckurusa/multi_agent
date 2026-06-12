---
name: issue-runner
description: 열린 이슈를 확인하고 하나를 처리한 뒤 닫습니다
---

# issue-runner

열려 있는 GitHub 이슈 중 하나를 골라 구현하고, 커밋과 함께 이슈를 닫는다.

## 1단계 — 열린 이슈 확인

```bash
gh issue list --state open
```

목록이 비어 있으면 "처리할 열린 이슈가 없습니다"라고 보고하고 종료한다.

## 2단계 — 이슈 하나 선택 → 구현

- 영향이 크고 의존성이 적은 이슈를 우선한다. 여러 개면 사용자에게 어떤 것을 처리할지 묻는다.
- 선택한 이슈의 본문(작업 항목 체크리스트)을 기준으로 코드를 수정한다.
- 변경 후 `python orchestrator.py "..."` 등으로 동작을 검증한다.

## 3단계 — 커밋 + 이슈 닫기

커밋 메시지에 `closes #N`을 포함하면 푸시 시 이슈가 자동으로 닫힌다:

```bash
git add -A
git commit -m "fix: <변경 요약> (closes #N)"
git push
```

`closes`로 자동 종료되지 않은 경우 수동으로 닫는다:

```bash
gh issue close N --comment "구현 완료: <커밋 해시 또는 요약>"
```

## 규칙

- 한 번에 이슈 하나만 처리한다.
- 커밋 메시지 끝에 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`를 붙인다.
- 처리 완료 후 닫힌 이슈 번호와 변경 요약을 사용자에게 보고한다.
