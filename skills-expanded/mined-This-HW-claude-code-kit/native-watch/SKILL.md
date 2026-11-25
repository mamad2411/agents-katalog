---
name: native-watch
description: Audit Claude Code native feature absorption. Use to compare the kit's components against the latest Claude Code releases and propose absorption-ledger updates. Trigger with /native-watch or on a schedule.
model: sonnet
effort: medium
---

# Native Watch

네이티브 흡수 감시 루틴 — `docs/native-absorption.md`(SSOT 대조표)를 Claude Code
최신 릴리스와 대조해 "네이티브가 흡수한 것 vs kit 자체 구현"의 드리프트를 잡는다.

> 철학: 기술부채의 최대 원천은 네이티브가 하는 일의 중복 구현이다. 이 스킬은 그
> 드리프트를 **정기 루틴**으로 만든다 (일회성 수동 감사 → 반복 가능 절차 — spec: `docs/specs/2026-07-07-toolkit-improvement-batch.md`).

## 절차

### 1. 대조표 로드

`docs/native-absorption.md`를 읽는다. 없으면 중단하고 사용자에게 보고
(대조표가 SSOT — 스킬이 임의로 재생성하지 않는다).

### 2. 릴리스 정보 수집

web-research 경로로 최신 정보를 조회한다 (가용한 것 우선):

- Claude Code 공식 문서/체인지로그: `code.claude.com/docs` (릴리스 노트, 신기능)
- `anthropics/claude-code` GitHub CHANGELOG
- 필요 시 WebSearch로 최근 발표 보강

수집 실패(네트워크/도구 부재) 시 **fail-open이되 보고 필수**: 대조표는 건드리지
않고 "수집 실패 — 다음 주기에 재시도"를 명시적으로 출력한다. 조용한 성공 위장 금지.

### 3. Diff 분석

대조표의 각 행에 대해:

- `kit-only`/`watch` 행: 새 네이티브 프리미티브가 요구를 충족하기 시작했는가?
  → **흡수 후보**로 플래그 (근거 링크 포함)
- `native-adopted` 행: 네이티브 규격 변경(deprecation, 시그니처 변경)이 kit 콘텐츠를
  깨뜨리는가? → **호환성 경고**로 플래그
- 표에 없는 신규 kit 컴포넌트(스킬/훅/스크립트 추가분): → **누락 행 추가** 제안

### 4. 리포트 출력

```
## Native Watch 리포트 (YYYY-MM-DD)
- 흡수 후보: [컴포넌트] — [새 네이티브 기능] (근거: 링크)
- 호환성 경고: [컴포넌트] — [변경 사항]
- 대조표 누락: [신규 컴포넌트]
- 변경 없음: N행 확인
```

### 5. 대조표 갱신 제안

발견이 있으면 `docs/native-absorption.md` 수정 diff를 **제안**한다 — 상태 변경
(예: `kit-only` → `watch`)과 근거/확인일 갱신, 전수 검토 기록 행 추가 포함.

> 실제 흡수 작업(kit 구현 제거·위임 전환)은 이 스킬의 범위 밖이다 — 별도 Work로
> 분리한다 (brainstorming → plan-task 체인). 이 스킬은 **감지와 제안**까지만.

### 6. 주기 실행 안내

자체 스케줄러를 구현하지 않는다 (zero-debt — spec:
`docs/specs/2026-07-07-toolkit-improvement-batch.md`). 사용자에게 네이티브 `/schedule`
스킬로 월 1회 루틴 생성을 안내한다 — 정확한 구문은 사용자의 Claude Code 버전의
`/schedule` 안내를 따른다 (예: "/schedule 로 매월 /native-watch 실행 루틴 생성").

## 완료 기준

- 대조표 전 행 확인 + 리포트 출력 (변경 없어도 "변경 없음 N행" 명시)
- 발견 시: 대조표 갱신 diff 제안 (적용은 사용자/메인 세션 승인 후)
