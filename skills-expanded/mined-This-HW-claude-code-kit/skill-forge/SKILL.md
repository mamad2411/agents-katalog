---
name: skill-forge
description: Distill a hard problem you just solved into a reusable skill draft - proposal-only, behind a three-condition threshold. Use after finishing a non-trivial task whose procedure would otherwise die with the session. Trigger with /skill-forge.
model: opus
effort: high
---

# Skill Forge — 성공 경험을 재사용 자산으로

kit의 학습 루프는 **비대칭**이다. 실패는 ledger → LESSONS → `/self-improve`로 흐르는데,
성공은 아무 데도 안 남는다. 어려운 문제를 푼 세션의 절차 지식이 세션 종료와 함께
소멸하고, 다음에 같은 문제를 만나면 처음부터 다시 푼다.

이 스킬은 그 절반을 메운다 — 단, **아무 성공이나 스킬이 되지는 않는다.**

<HARD-GATE>
1. **proposal-only.** 사용자가 초안을 보고 **명시적으로 승인**하기 전에는
   `plugins/common/skills/` 아래에 어떤 파일도 만들지 않는다. 초안은 대화창 또는
   `docs/works/idea/` 에만 존재한다.
2. **포징 임계 3조건 AND.** 하나라도 미충족이면 스킬을 만들지 않고 강등한다.
3. **자동 커밋 금지.** 커밋은 항상 사용자의 별도 결정이다.
</HARD-GATE>

> **적용 범위**: 승인 후 적용 단계(스킬 파일 생성 + 3표면 동기화 + 카운트/버전 게이트)는
> **kit 레포 자체의 개발**을 전제한다. 소비자 프로젝트에서는 3조건 판정과 초안 작성까지가
> 유효하며, 산출한 초안은 그 프로젝트의 `.claude/skills/`에 사용자가 직접 배치한다.

## 포징 임계 (3조건 — AND)

| 조건 | 판정 질문 | 미충족 시 강등 경로 |
| --- | --- | --- |
| **재현성** | 이 절차를 그 세션의 맥락 없이 그대로 다시 실행할 수 있는가? | `./scripts/feedback.sh upsert`로 ledger 한 줄 |
| **반복성** | 앞으로 **다시** 마주칠 문제인가? (1회성 마이그레이션·특정 사고 대응은 아니다) | Work 문서(`progress.md`/`decisions.md`)에 기록 |
| **비중복** | 기존 스킬로 커버되지 않는가? | 기존 스킬 **보강 제안**으로 전환 (새 스킬 만들지 않음) |

> 세 번째 조건이 가장 자주 걸린다. "새 스킬이 있으면 편하겠다"는 거의 항상
> "기존 스킬에 한 절이 빠져 있다"의 오독이다. 스킬 개수는 자산이 아니라 **비용**이다 —
> 트리거 맵이 커질수록 어느 것도 안 걸린다.

## 절차

### 1. 후보 서술 [건너뛰기 금지]

무엇을 풀었는지가 아니라 **"다음 사람이 같은 상황에서 무엇을 해야 하는가"**로 쓴다.
전자는 회고이고 후자만 스킬이다.

### 2. 3조건 판정 [건너뛰기 금지]

각 조건에 **근거와 함께** 판정을 적는다. "그럴 것 같다"는 판정이 아니다.

비중복 판정은 실제 목록과 대조한다:

```bash
ls plugins/common/skills/                       # kit 스킬
ls ~/.claude/plugins/*/*/skills/ 2>/dev/null    # 설치된 다른 플러그인 (없으면 건너뛴다)
```

> **다른 플러그인의 존재를 가정하지 않는다.** superpowers 등이 설치돼 있으면 그
> 목록과도 대조하고, 없으면 그 단계를 조용히 건너뛴다 (fail-open). 특정 플러그인이
> 있어야만 동작하는 절차는 consumer-first 위반이다.

미충족이면 **여기서 멈추고** 강등 경로를 실행한 뒤 보고한다.

### 3. 초안 작성 (파일로 남기지 않는다)

`/skill-creator`의 템플릿 규약을 따른다:

- frontmatter: `name`(kebab-case, 파일 경로와 일치) · `description`(**영문**, 트리거
  조건 포함) · `model` · `effort`
- 본문: 사용 시점 표 → 절차(각 단계에 `[건너뛰기 금지]` 여부 명시) → 실패 모드 →
  delegation signal
- **정직한 한계 절을 반드시 넣는다** — 이 스킬이 보장하지 *않는* 것.

### 4. 사용자 승인 대기 [건너뛰기 금지]

초안 전문과 3조건 판정 근거를 함께 제시하고 승인을 받는다.
승인 없는 상태에서 다음 단계로 넘어가지 않는다.

### 5. 승인 후 적용 (동반 갱신이 계약이다)

스킬 파일 하나만 만들면 문서 카운트 게이트가 깨진다. 아래를 **함께** 갱신한다:

```bash
# 1) 스킬 파일 생성
# 2) 세 표면 동기화 (F-025): CLAUDE.md Key Skills 표 · README · using-claude-code-kit 트리거 맵
# 3) 카운트 검사
python3 scripts/check_doc_counts.py
# 4) 버전 범프 + CHANGELOG (플러그인 캐시는 버전으로 키잉된다)
# 5) 완료 게이트
scripts/verify-done.sh
```

## 정직한 한계

- 이 스킬은 **경험의 질을 판정하지 않는다.** 3조건은 "자산화할 가치가 있는가"의
  하한선일 뿐, 절차가 옳다는 보증이 아니다. 검증은 실사용이 한다.
- 새 스킬에는 eval 커버리지가 **없다.** 행동 회귀 안전망이 필요하면 `/eval-forge`로
  대응 시나리오를 함께 만든다.
- `/self-improve`와 역할이 다르다 — 그쪽은 **결함**을 정의 파일에 반영하고,
  이쪽은 **성공**을 새 자산으로 승격한다. 둘 다 proposal-only다.
