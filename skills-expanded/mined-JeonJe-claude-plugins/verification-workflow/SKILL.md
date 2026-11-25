---
name: verification-workflow
description: 요구사항 → 리서치 → 계획 → 구현 → 테스트 → 리뷰 → 커밋 게이트로 이어지는 검증 워크플로우. 복잡도 기반 단계 선택, 리스크 레벨별 검증 강제, 커밋 전 체크리스트, 자동 수정 루프 포함. 기능 구현 계획, 커밋 전 검증, 코드 검증 절차, 리뷰 게이트 확인 시 사용.
---

# Verification Workflow

A risk-gated pipeline from requirement to commit. The review/verification stages can be implemented by any agent roster — role names below (researcher, architect, reviewer, executor) are roles, not specific agents. Simple one-off work needs only self-verification (lint/type/test) plus the commit gate.

## Full flow

```
요구사항 입력
    ↓
[모호함 체크] → 해당 시 사용자에게 질문
    ↓
[복잡도 판단] → 단순(1-2파일): 계획 직행 / 복잡(3+파일): Research 단계 진입
    ↓
★ Research (복잡 작업 필수) — 대상 영역 분석 → research.md → 사용자 확인
    ↓
★ 계획 — 계획 출력 템플릿 준수, 유사 기존 구현 참조 필수 → plan.md
    ↓
★ Annotation Cycle (복잡 작업 필수, 1-3회)
  → 사용자 주석/피드백 → 계획 갱신 → "아직 구현하지 마라"
    ↓
★ 계획 검증 — 결함·누락 / 보안 / 정책 정합성 관점의 독립 리뷰
    ↓
[공유 모듈 변경?] → YES: 영향 모듈 식별
    ↓
구현 (외과적·최소 diff·컨벤션 준수)
    ↓
테스트 단계 (references/testing.md) — 요구사항 기반·예외/경계·회귀·커버리지
    ↓
린트/타입/테스트 (스택별 fresh 출력)
    ↓
★ 코드 검증 — 독립 리뷰. CERTAIN 지적은 자동 수정 / QUESTION은 사용자 확인
    ↓
[E2E 필요 시] 브라우저/실환경 검증 (액션 후 스크린샷 증거)
    ↓
커밋 전 검증 체크리스트 (아래) → Commit
    ↓
[검증 실패] → 자동 수정 루프 (아래)
```

## Research 단계 (복잡 작업 필수)

**트리거**: 3개+ 파일 변경 예상, 또는 기존 아키텍처 이해가 필요한 작업

1. 대상 코드를 깊이 분석 (관련 클래스, 의존성, 호출 흐름)
2. 분석 결과를 `docs/{key}/research.md` 등 프로젝트 문서 위치에 기록:
   현재 구조 요약 / 데이터 흐름 / 제약 조건 / 변경 영향 범위
3. **사용자에게 research.md 검토 요청** → 잘못된 이해를 사전 차단
4. 사용자 승인 후에만 계획 단계로 진행

**핵심**: 잘못된 리서치는 이후 모든 단계를 망친다. 가장 비용이 큰 실패를 여기서 차단.
**스킵 조건**: 단순 버그 수정, 1-2파일 변경, 사용자가 "skip research" 명시

## 계획 출력 템플릿 (필수 준수)

```markdown
## 1. 변경 파일 목록      — path + 변경 이유 한줄
## 2. 참조한 기존 구현    — path + 이 패턴을 따르는 이유
## 3. 핵심 코드 스니펫    — 주요 시그니처/핵심 로직 스케치
## 4. 대안 및 트레이드오프 — 선택 vs 대안 (최소 1개), 각각 장단점 (기록 구조: references/design-decisions.md)
## 5. 리스크             — 회귀 가능성, 성능 영향, 마이그레이션 여부
## 6. 예상 소요과 컷라인  — Phase별 구현/테스트 예상 + 근거(참조 구현 크기·파일 수·미지수),
##                        시간 초과 시 자를 순서 (동작 우선 → 기본 기능 → 심화)
```

**참조 구현 패턴**: 계획 작성 전 기존 코드에서 유사 구현을 먼저 검색한다 — 동일 도메인 유사 기능 → 동일 패턴의 다른 모듈 → 기존 설계 문서. 기존 패턴과 다르게 구현하면 반드시 이유를 트레이드오프 섹션에 기록.

## Annotation Cycle (복잡 작업 필수)

**트리거**: 3개+ 파일 변경, 아키텍처 결정 포함, 새로운 패턴 도입

계획 완료 → 사용자 검토 요청 → 피드백 반영 갱신 → 승인("LGTM", "진행해")까지 반복(최대 3회).

**"Don't implement yet" 규칙**: Annotation Cycle 중에는 절대 코드를 작성하지 않는다. 계획 확정 전 코드를 쓰면 잘못된 방향에 고착된다.

**스킵 조건**: 단순 작업, 사용자가 "바로 구현해" 명시, 이미 상세한 요구사항 제공

## 요구사항 명확화 (질문 필수)

하나라도 해당하면 반드시 사용자에게 확인: 모듈/패키지 선택 모호 · DB 스키마/데이터 모델 변경 · API 스펙 불명확(페이징? 정렬? 에러 응답?) · 테스트 범위(단위? 통합? Mock 전략?) · 프로젝트 특화 설정(다중 DB, 모노레포 빌드 타겟 등)

## 커밋 전 검증 체크리스트 (CRITICAL)

> 이건 커밋 직전 "통과 확인 게이트"다. 테스트를 *어떻게 작성하나*는 `references/testing.md` 소관 — 여기서는 결과 통과만 confirm한다. 하나라도 실패하면 커밋하지 않는다.

### Phase 1: 기본 검증 (매 커밋 필수)

- [ ] **스테이징 완전성**: `git status`로 변경 파일 전부 스테이징 확인. 연관 파일 누락 금지 (단, `git add -A`/`.` 금지 — 명시 add)
- [ ] **린트/포맷팅**: lint 실행 → 실패 시 자동 수정 후 재확인
- [ ] **타입 체크**: 타입 체커 실행 → 에러 0건. **Why**: 런타임 테스트는 타입 에러를 못 잡는다 — CI 빌드에서 터지는 주요 원인
- [ ] **테스트**: 변경 파일 관련 테스트 전부 통과 (작성 기준은 `references/testing.md`)

### Phase 2: 리뷰 (Risk Level에 따라 — `references/code-factory-gate.md`)

> Risk Level은 변경 경로·범위로 판단 — HIGH(결제·인증·DB 스키마·공유 모듈) / MEDIUM(도메인 로직) / LOW(주석·문서·설정·포맷)

- **HIGH/MEDIUM**: 독립 코드 리뷰 필수. CERTAIN(Critical/Warning)은 자동 수정, QUESTION은 사용자 확인. 보안(인증/인가·입력검증·외부 API·토큰)·FE↔BE 계약이 코드 단계에서 변경됐으면 계획 검증 관점 재확인
- **LOW**: Phase 1만 통과하면 커밋 가능

### Phase 3: 최종 확인

- [ ] Phase 1~2 전부 통과
- [ ] `git diff --staged`로 의도치 않은 변경 최종 확인
- [ ] 커밋 단위 적절성 확인 (`references/commit-units.md`) → 프로젝트 커밋 컨벤션으로 메시지 작성 → 커밋

### 프레임워크별 명령 매핑 (참고)

| 프레임워크 | lint | 타입 체크 | 빌드 | 테스트 |
|-----------|------|----------|------|--------|
| Nuxt 3 / Vue 3 + Vite | `npm run lint` | `npx vue-tsc --noEmit` | `npm run build` | `npm run test` |
| Next.js/Vite | `npm run lint` | `npx tsc --noEmit` | `npm run build` | `npm run test:run` |
| Java/Gradle | `./gradlew spotlessCheck` | 컴파일 시 검증 | `./gradlew clean build` | `./gradlew :module:test` |
| Python | `ruff check` | `mypy` | - | `pytest` |

**항상 프로젝트 CLAUDE.md의 Build Commands를 우선 참조할 것.**

## 자동 수정 루프 (검증 실패 시)

| 실패 유형 | 대응 | 최대 반복 | 초과 시 |
|----------|------|----------|--------|
| **Build/Type** | 최소 diff 수정 → 재빌드 | 3회 | 사용자 보고 |
| **Test** | 구현 수정 (테스트는 미변경) → 재실행 | 3회 | 사용자 보고 |
| **Lint/Format** | 자동 수정 명령 → 재검증 | 2회 | 사용자 보고 |
| **리뷰 지적(CERTAIN)** | 지적 수정 + 회귀 테스트 추가 | 2회 | 사용자 보고 |
| **Integration (멀티 모듈)** | 영향 분석 → 클린 빌드 → 모듈별 격리 테스트 → 스키마/타입 동기화 확인 | 3회 | 사용자 보고 |

## References index

| File | Read when |
|---|---|
| `references/design-decisions.md` | 기술 선택이 갈리는 지점 — 트레이드오프 결정을 기록으로 남길 때 |
| `references/testing.md` | 단위/통합/E2E 테스트를 작성·검증할 때 |
| `references/test-assertion-style.md` | Java 테스트 단언을 쓰거나 리뷰할 때 |
| `references/code-factory-gate.md` | 리스크 분류·검증 강제·stale check·regression→test 학습 루프 |
| `references/commit-units.md` | 커밋을 몇 개로 나눌지 결정할 때 — 의도 단위, 순서, add 규율 |
| `references/mistake-prevention.md` | 버그/BLOCK/회귀에서 배운 패턴을 룰로 축적하는 템플릿 |
| `references/performance-redis.md` | Redis 원자성/Lua 판단이 필요할 때 |
