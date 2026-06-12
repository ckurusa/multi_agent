---
name: doc-optimizer
description: CLAUDE·SOUL·README의 중복·낡은 내용을 SSOT·Minimum·Freshness 기준으로 정리합니다
---

# doc-optimizer

세 문서(`SOUL.md`, `README.md`, `CLAUDE.md`)를 검토해 중복·낡음·과잉을 제거하고 각 문서가 자기 역할만 담도록 정리한다.

## 문서별 역할 (SSOT 경계)

| 문서 | 단일 소스로 소유하는 내용 |
|------|--------------------------|
| `SOUL.md` | 존재 이유, 판단 기준, 하지 않는 것 |
| `README.md` | 설치, 사용법, 파일 구조 (인간 온보딩, 30초 안에 읽힘) |
| `CLAUDE.md` | SOUL 링크, 핵심 파일 표, 스킬 목록, 작업 규칙 (에이전트 운영) |

## 점검 기준

1. **SSOT (Single Source of Truth)** — 같은 정보가 두 문서에 있으면, 소유 문서에만 남기고 나머지는 링크로 대체한다.
   - 예: 설치/사용법이 CLAUDE.md에도 있으면 → README로 일원화하고 CLAUDE은 링크만.
2. **Minimum** — 읽는 사람의 결정에 영향을 주지 않는 문장은 지운다. 특히 README는 짧게.
3. **Freshness** — 코드와 어긋나는 내용을 찾는다.
   - 핵심 파일 표가 실제 `agents/`·루트 파일과 일치하는가?
   - 스킬 목록이 `.claude/skills/` 실제 파일과 일치하는가?
   - 모델 ID·플래그·명령어가 현재 코드와 같은가?

## 절차

1. 세 문서와 실제 파일 트리(`agents/`, `.claude/skills/`, 루트)를 읽는다.
2. 위 세 기준으로 불일치·중복·과잉을 목록화한다.
3. 각 문서를 수정한다 (중복 제거 → 링크화, 낡은 항목 갱신, 군더더기 삭제).
4. 수정 요약을 사용자에게 보고하고, 변경이 있으면 커밋한다.

## 규칙

- 정보를 옮길 뿐 삭제로 잃지 않는다 — 다른 문서가 소유한 내용은 링크로 연결한다.
- 커밋 메시지 끝에 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`를 붙인다.
