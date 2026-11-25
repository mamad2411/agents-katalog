---
name: agent-teams
description: SUPERSEDED by control-loop (kept through claude-code-kit 2.x; removed in the successor hiway-kit) — large-scale parallel work guidance. Routes 10+ parallel independent tasks to native dynamic workflows, with legacy experimental Agent Teams as fallback. See control-loop for the current multi-session delegation discipline.
model: opus
effort: high
---

# Agent Teams / 대규모 병렬 처리 스킬

> **폐기 예고 (D-7 1단계, v2.19.0) — 2.x 에서는 제거되지 않는다.** 여기 담겨 있던
> 절차·규율은 `control-loop` 스킬로 흡수됐다 — 결정 대 조사를 페이즈로 나누고,
> 워커 디스패치·검증·병합을 다룬다. **`claude-code-kit` 2.x 는 이 스킬을 끝까지
> 유지한다**: 스킬 삭제는 그 자체로 파괴적 변경이고, 2.20.0 은 파괴적 변경 없이
> 닫는 최종 릴리스이기 때문이다. 실제 제거는 후속 킷
> [`hiway-kit`](https://github.com/This-HW/hiway-kit) 에서 일어났다 — 거기로 옮겨
> 갈 때 `control-loop` 로 갈아타면 된다.

> **Spec 2 / W-006 업데이트:** 대규모 병렬 오케스트레이션의 1순위는 이제 네이티브
> **dynamic workflow(`ultracode`)** 입니다. 실험적 자체 Agent Teams 조율은 네이티브가
> 흡수했으며, 이 스킬은 그 경로를 안내합니다.

---

## 사용 시점

```
✅ 대규모 병렬:
- Large 작업 (10개 이상 파일 변경)
- 병렬 가능한 독립 작업 (테스트 + 문서 + 구현)
- 장기 실행 작업

❌ 사용하지 않음:
- Small/Medium 작업 → auto-dev 스킬 주도 플랫 위임 (main이 Agent 병렬 dispatch)
- 순차 의존 작업 (A 완료 후 B)
```

> 오케스트레이션 모델 전체: `CLAUDE.md` → "Orchestration Model — Scale-Appropriate Primitives"

---

## 1순위: 네이티브 Dynamic Workflow (`ultracode`)

네이티브 워크플로우 엔진이 백그라운드에서 10~100+ 에이전트를 오케스트레이션하며,
main 컨텍스트를 소비하지 않습니다.

```
사용자가 프롬프트에 ultracode 키워드로 트리거:
  ultracode <대규모 작업 설명>

- 백그라운드 오케스트레이션 + 라이브 에이전트 카운트
- /workflows 로 실행 현황 확인
```

> ⚠️ `ultracode`는 **사용자 대화형 트리거 전용**입니다 — 스킬/비대화형에서 프로그래밍
> 호출이 불가합니다(2026.6 기준). 따라서 auto-dev는 Large 작업을 감지하면 청크로
> 분할해 안내하고, 실제 대규모 병렬은 사용자가 `ultracode`로 시작합니다.

### auto-dev와의 연계

auto-dev가 Work `size: Large`를 만나면:
1. 독립 청크로 분할 (blockedBy 기반)
2. 청크가 소수면 → 스킬 주도 병렬 dispatch
3. 청크가 다수(10+)면 → 사용자에게 `ultracode` 트리거 안내

---

## 역할 배분 가이드 (병렬 구성 참고)

| 작업 유형       | 병렬 구성 (Teammates/에이전트)                        |
| --------------- | ----------------------------------------------------- |
| **기능 구현**   | implement-code, write-tests, sync-docs                |
| **리팩토링**    | plan-refactor, implement-code, verify-code            |
| **다관점 리뷰** | `/multi-perspective-review` 사용 권장                 |

권장 병렬 수: 3-8개 (그 이상은 `ultracode`에 위임).

---

## 레거시: 실험적 Agent Teams (선택)

`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 환경에서 `TeamCreate` + `Task(team_name=...)`
조합이 여전히 동작할 수 있으나, **네이티브 `ultracode`로 대체**되었습니다. 신규 작업은
`ultracode`를 사용하세요. 이 경로는 하위호환을 위해서만 남아 있습니다.

---

## multi-perspective-review와의 관계

| 상황             | 사용                                              |
| ---------------- | ------------------------------------------------- |
| 다관점 리뷰      | `/multi-perspective-review`                       |
| 대규모 기능/리팩토링 | `ultracode` (네이티브) 또는 auto-dev 청크 분할 |

---

## 참조

| 문서                | 위치                                                    |
| ------------------- | ------------------------------------------------------- |
| 오케스트레이션 모델 | `CLAUDE.md` → Orchestration Model                       |
| auto-dev 파이프라인 | `plugins/common/skills/auto-dev/SKILL.md`               |
| MPR 스킬            | `plugins/common/skills/multi-perspective-review/SKILL.md` |
| **후속(이 스킬을 대체)** | `plugins/common/skills/control-loop/SKILL.md` |
