---
name: plan-quick
description: "구현 계획 세워줘, 설계해줘, 작업 계획 요청 시 사용. 요구사항 재정의 + 리스크 평가 + 단계별 구현 계획. 코드 작성 전 사용자 확인 필수. Skip when requirements are already crisp. PRD 정리는 requirements-analysis 사용."
---

# Plan Command

구현 전 계획 수립. 코드 작성 전 사용자 승인 대기 (승인 없이 진입 시 의도와 다른 결과 위험).

## Use Cases

**1. 신규 기능 계획**
- Input: "/plan 실시간 알림 기능 추가"
- Action: 요구사항 재정의 → 리스크 분석 → Phase별 계획 → 사용자 확인 대기
- Output: 구조화된 구현 계획 + 리스크 + 복잡도 평가

**2. 리팩토링 계획**
- Input: "/plan 인증 시스템 리팩토링"
- Action: 현재 코드 분석 → 의존성 파악 → 단계별 마이그레이션 계획
- Output: 안전한 마이그레이션 로드맵 + 롤백 전략

**3. 복잡한 버그 수정**
- Input: "/plan 결제 동시성 이슈 해결"
- Action: 원인 분석 → 해결 옵션 2-3개 → 트레이드오프 비교
- Output: 옵션별 장단점 + 추천 방안
- **(조건부) How tree**: 실질 대안이 2개 이상이면 문제 → 접근 갈래 → 구체안으로 대안을 *생성*하고(떠오른 것 나열 X) 같은 레벨끼리 비교한다. 선택지 하나뿐이면 생략. 비교표는 Risk Gate Output의 Options 블록에 채운다.

**4. Risky change gate**
- Input: "/plan DB schema 변경", "/plan public API 수정", auth/security/payment/production/3+파일 변경
- Action: 근거 수집 → 영향 범위 확인 → 승인 필요한 계획으로 정리 → 코드 작성 금지
- Output: approval-ready plan + impact/risk/verification

**5. Impact check**
- Input: "/plan 이 API 변경 영향 봐줘", "/plan symbol rename 영향 확인"
- Action: 변경 계약(symbol/endpoint/schema/env/config/DTO/route) 식별 → 참조·테스트·문서·FE/BE 영향 확인
- Output: CLEAR/WATCH/BLOCK verdict + 근거


## How It Works

계획 수행자(본 세션 인라인, 또는 워크스페이스에 planner 에이전트가 있으면 그것)는 다음을 수행한다:

1. **Analyze the request** — 요구사항을 명확히 재정의
2. **Break down into phases** — 실행 가능한 단계로 분해 (접근이 갈리면 phases를 How tree(문제 → 접근 갈래 → 구체안) 형태로 분해해 갈래별 단계를 비교)
3. **Identify dependencies** — 컴포넌트 간 의존성 파악
4. **Assess risks** — 잠재 블로커와 리스크 평가
5. **Estimate complexity & duration** — High/Medium/Low + Phase별 구현/테스트 예상 소요와 근거(참조 구현 크기, 변경 파일 수, 미지수 개수). 근거 없는 숫자는 예상이 아니라 희망이다
6. **Present the plan** — "WAITING FOR CONFIRMATION" 표시 후 사용자 명시적 승인 대기
7. **Gate risky changes** — DB/auth/security/API/payment/production/3+ files require explicit approval before edits
8. **Check impact** — for public contracts, list references, affected tests/docs, FE/BE or cross-repo impact


## Confirmation Protocol

- 승인: `yes` / `proceed` / 긍정 응답 → 구현 시작
- 수정 요청:
  - `modify: [변경사항]`
  - `different approach: [대안]`
  - `skip phase 2 and do phase 3 first`

사용자가 명시적으로 승인하기 전에는 코드 변경/파일 작성 금지. 이유는 계획 단계의 잘못된 가정이 코드에 박히면 되돌리기 비용이 크기 때문.
위험 작업(DB schema, auth/security, public API, payment, production config, 3+ files, 2+ repos)은 반드시 계획 단계에서 멈춘다. 구현은 승인 후 별도 단계에서만 진행한다.


## Integration with Other Commands

계획 후:
- 구현: 직접 구현 또는 executor 위임 (ma-pipeline 플러그인의 dispatch)
- 빌드 에러: `/build-fix`
- 코드 리뷰: code-reviewer 플러그인

## Risk Gate Output

```text
Scope:
- ...

Evidence:
- path:line or source → fact

Impact:
- Contract:
- References checked:
- Affected tests/docs:
- FE/BE or cross-repo impact:

Options (조건부 — 대안 2+; How tree: 문제 → 접근 갈래 → 구체안):
| 옵션 | 비용 | 리스크 | 롤백 | 영향범위 |
|------|------|--------|------|----------|
| A    |      |        |      |          |
| B    |      |        |      |          |
→ 채택: <근거> | 기각: <각 근거>

Plan:
1. ...

Estimate (Phase별 구현/테스트 예상 소요 + 근거):
| Phase | 구현 | 테스트 | 근거 (참조 구현 크기·파일 수·미지수) |
|------|------|--------|----------------------------------|
→ 미지수(처음 쓰는 라이브러리·불명확한 스펙)가 있는 Phase는 예상을 범위로 쓰고 스파이크를 먼저 배치

Cutline (시간 제약 시 지키는 순서):
1. Make it Work — 빌드·기동·핵심 경로 1개
2. Basic Features — 요구된 기능 + 핵심 제약(동시성 등)
3. Deep Thought — 설계 문서화·추가 구현·최적화
→ 시간이 모자라면 아래부터 자른다. 3을 위해 1·2를 희생하지 않는다
→ 평가가 필수/선택 과제로 분리된 형식이면: 필수=1·2, 선택=3에 대응 — 선택 과제는 필수 전체가 검증된 후에만

Risks:
- ...

Verification:
- smallest check → broader check

Verdict:
- CLEAR | WATCH | BLOCK

Needs approval:
- yes/no, and why
```
---

## Done When

- 구현 계획이 Phase별로 출력 PASS
- 사용자가 "yes/proceed" 승인 또는 수정 요청 PASS
- 요구사항 모호 시 AskUserQuestion으로 명확화 후 재계획

## 작업 원칙

- 코드 작성 전 사용자 확인 필수 (승인 없이 진입 시 회귀 위험)
- 요구사항을 명확히 재정의하고 Phase별 구체적 계획 수립
- 리스크와 복잡도를 평가해 우선순위 제시
- 계획 단계에서 모든 구현 세부를 결정하지 않음 (지나친 사전 결정은 over-engineering)
- 단순 작업에 과도한 계획 수립 회피 — 직접 구현이 적절
