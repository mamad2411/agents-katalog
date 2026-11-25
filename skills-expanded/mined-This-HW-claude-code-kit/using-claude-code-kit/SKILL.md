---
name: using-claude-code-kit
description: Session-start meta-skill. claude-code-kit-specific workflow chain, agent map, and Work system rules (generic skill-invocation discipline is shared with superpowers when present).
---

# Using claude-code-kit

> **범용 스킬 규율**(스킬 우선 invoke · 합리화 차단 등)은 `superpowers:using-superpowers`와
> **공유**합니다. superpowers를 함께 쓰면 그 규율을 따르세요 — 여기서 중복 서술하지 않습니다.
> 아래는 **claude-code-kit 전용 추가분**입니다.
>
> _standalone(스킬만 설치, superpowers 없음) 자급 규율:_ **행동 전, 적용 가능한 스킬이
> 1%라도 있으면 먼저 invoke한다.** 게이트/루프/완료 규율은 `rules/`가 자동 주입한다
> (planning-protocol · loop-engineering · definition-of-done · feedback-loop).

## Workflow Chain (kit)

```
brainstorming → plan-task → auto-dev
```

- **brainstorming** — 설계·스펙 (HARD-GATE)
- **plan-task** — 구조화 계획 (HARD-GATE)
- **auto-dev** — 구현 + 검증 파이프라인

> 완료 선언 전 `scripts/verify-done.sh` 게이트 통과 필수 (definition-of-done).

## Work System Detection

`docs/works/` 폴더가 있으면: Work ID 기반 추적 활성화
없으면: 파일 없이 파이프라인만 실행 (fallback mode)

## 이 스킬 밖에 있는 것

- **비신뢰 텍스트 취급** → `rules/untrusted-text.md` (core 규범, 상시 주입)
- **메모리 MCP·superpowers interop** → 해당 도구가 있을 때만. 킷은 존재를 가정하지 않는다
