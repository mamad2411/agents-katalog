---
name: implementing-issues
description: 이 프로젝트의 승인된 작업 항목(Issue)을 Issue 번호나 명시한 참조로 받아 조사·설계·구현한다. 기존 Issue의 진행·구현·작업·마무리 요청에 사용하며, 현재 단계의 SDD·경계·검증 절차를 연결한다. 새 Issue만 작성할 때는 사용하지 않는다.
---

Trivial/Small 현재/수동 작업은 [간결 경로](../../process/small-work.md)의 닫힌 읽기 집합·실행 의무·세 기록을 따른다. 아래 전체 본문은 그 경로의 예외가 해당 절을 열 때만 적용하며 간결 형식/면제는 유지한다. 격상 후에는 해당 등급의 전체 계약을 따른다.

외부 적용: 먼저 `W/activation.md`의 선택·소유·경로 계약을 적용한다. 아래 고정 사본·생성 hard guard 참조는 그 계약의 호환 의미를 따른다. 미선택 작업에는 이 스킬을 적용하지 않는다.

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `W`), `M`(고정 공통 원칙 `M`)이다. 현재 폴더나 W의 상위 폴더로 P·M을 추측하지 않는다. P의 hard guard와 적용 선언을 따르고, Issue·댓글·라벨·PR이라는 말은 `W/../project/tracker.md`가 선언한 `W/tracker/` 방식으로 바꿔 읽는다. 낯선 용어는 [용어집](../../glossary.md)에서 찾는다.

# Implementing Issues

## Issue dispatch

1. 지정된 Issue의 현재 본문·라벨부터 읽는다. 열린 Issue 전체 목록부터 뒤지지 않는다.
2. Issue를 실행 기준으로 삼고 Priority·grade·단계별 의존성·수정 허용/금지 경로(allowed/forbidden)·완료 기준·Visual Spec·공통 계약 참조를 유지한다. 이미 정해진 요구를 다시 탐색하거나 사용자에게 다시 입력하게 하지 않는다.
3. Epic 관리 문서이면 `managing-issues`의 `Epic 조율`로 작업 구성·의존성을 갱신하고 해당 하위 실행 Issue로 들어간다. 하위 Issue가 없으면 필요한 만큼 정의하고 조사한다. 관리 문서 자체에는 구현 claim·실행 등급·AS-IS/PLAN/BREAKDOWN 리뷰를 요구하지 않는다.

## Inputs

같은 실행(run)에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 적용됐다고 확인할 수 없으면 그 절부터 읽는다. 이미 확인한 같은 버전은 다시 쓴다.

필수 입력은 현재 Issue, `W/process/sdd/grade.md`·`W/process/sdd/entry.md`·`W/process/sdd/issue.md`의 현재 등급·진입·사람 판단 조건, `W/../project/sdd-workflow.md`의 적용·권한·실제 경로다. 조사에는 Issue와 직접 연결된 business·architecture 문서, 대상 코드·직접 계약·호출하는 쪽과 호출되는 쪽(caller/callee)을 읽는다.

SDD를 쓰는 설계, Medium 구현 진입, 별도 IMPLEMENT 문맥에서는 해당 `README.md`의 문제·전제·불변조건·남은 위험을 필요한 절과 기준 revision으로 직접 확인한다. 사람을 위한 문서라고 해서 Agent가 읽지 않아도 되는 것은 아니다. 다만 README 전체나 조건부 조사 이력을 일률적으로 읽지는 않는다. 리뷰 역할에는 기존 단계·방식별 허용 입력과 Blind Audit 격리를 그대로 적용한다.

아래 원본은 **그 행동을 할 때 필요한 절만** 읽는다. 이 목록을 미리 전부 읽을 목록으로 쓰지 않는다.

| 행동 | 읽을 원본 |
| --- | --- |
| 최초 SDD 배치 | `W/process/sdd-artifacts.md` |
| AS-IS 조사·근거 작성 | `W/process/sdd/as-is.md` |
| PLAN 결정·trade-off 작성 | `W/process/sdd/to-be.md` |
| 구현 명세 작성·소비 | `W/process/sdd/agent-spec.md` |
| 구현 중 전제 오류·진행 중 정책 변경 | `W/process/sdd/plan-change.md` |
| Large AS-IS/PLAN 게시·리뷰·재확인 | `W/process/design-review.md`의 현재 단계와 검토 대상에 해당하는 절 |
| 검증 계획·실행·PASS 재사용·코드 리뷰 판정 | `W/process/verification.md`와 P 적용 문서 `build.md`의 해당 검증 |
| 지금 맡은 역할의 적격 확인, 모델·추론·위임·대체 모델 선택 | `W/skills/_shared/execution-routing.md`의 해당 역할·선택 경로 |
| 작업자 인계·Result/Review 소비·선언된 영향 분석 결과 사용 | `W/skills/_shared/execution-packets.md`의 해당 Packet·영향 결과 절 |
| SDD·테스트·코드 등 P 작업 파일 첫 쓰기의 claim·lane·격리 | `W/skills/parallel-development/SKILL.md`의 해당 절 |
| 공유·루트 경계, 수명이 정해진 문서 판단 | W/P `module-boundaries.md`의 관련 경계 |
| 지시 충돌·코드와 business 문서 불일치·승인 범위 해석 불가 | W/P `agent-instruction-policy.md`의 해당 충돌 절 |
| 사람용 현황·계획·변경 설명 작성 | `W/process/agent-instruction-policy.md`의 `사람용 문서의 시각적 작성` |

시작·문제 발견·중단·인계에는 `W/process/observations.md`의 해당 절을 적용한다. 토큰 기록(token checkpoint)은 `W/process/token-diagnostic.md`가 켜져 있을 때 현재 단계 사건에 맞춰 남긴다. 작업 관리 도구를 쓸 수 없으면 토큰 기록만 생략하며, 다른 관측 기록은 생략하지 않는다.

## 입력 재사용과 조회

- 같은 실행에서 읽었고 바뀌지 않은 Issue·정책·소스·Issue/PR 메타데이터는 다시 쓴다.
- 다음 신호가 있으면 그 판단에 필요한 입력만 새로 읽는다: 검토 대상 SHA 변경, 현재 lane push로 바뀐 PR head, Issue/PR의 병합·닫힘·다시 열림·라벨·담당자·상태 변경, base 변경 근거, webhook·깨우기·외부 도구 결과·사용자 지시로 알게 된 외부 상태 변경. 병합 직전과 병합 뒤 종료 확인 직전에도 필요한 메타데이터를 다시 읽는다.
- 상태·라벨·병합 가능 여부·head/base SHA만 필요하면 메타데이터만 읽거나 필요한 항목만 읽는 조회를 먼저 쓴다. 본문·댓글·diff는 그 내용이 판단 근거일 때만 읽고, 메타데이터를 읽은 뒤 무조건 전체를 또 읽는 이중 호출을 만들지 않는다. 메타데이터만으로 안전하게 판정할 수 없으면 필요한 범위를 더 읽는다.

## 조사와 제품 수정 진입

모든 등급의 첫 파일 편집(설계 문서 포함) 전에 M `supports/ordered-changes.md`를 읽고 변경할 파일·심볼·순서와 기준 요구·확인 방법을 응답 또는 계획 도구의 짧은 목록에 연결한다. 기존 계획의 연결은 참조하고 부족한 부분만 보완하되 파일·심볼·순서는 목록에 유지한다. 단순 변경은 한 문장으로 충분하며 별도 계획 파일·ID·표·추가 리뷰나 승인 단계는 요구하지 않는다. 같은 run에서 확인한 동일 버전은 재사용한다.

1. 현재 요청이 읽기 전용 조사인지 제품 수정인지 구분하고, 그 단계에 필요한 의존성·차단 요인을 확인한다. 조사 자체의 접근 권한·사람 판단 조건은 유지한다. 상위의 미결 결론은 그것을 쓰는 구현·통합·배포를 기다리게 할 뿐 조사 시작을 막지 않는다.
2. 읽기 전용 조사에는 수정 claim을 요구하지 않는다. 같은 경로를 여럿이 읽는 것은 수정 충돌이 아니다. SDD·테스트·코드 등 실행 Issue의 P 작업 파일을 처음 만들거나 고치거나 지우기 전에는 `parallel-development`로 lane·claim을 확보한다. 현재 단계의 지시·의존성·경계를 적용하며, SDD를 쓰려는 claim에 아직 쓰지 않은 AS-IS/PLAN의 PASS를 요구하지 않는다. 작업 관리 기록과 Epic 관리 문서 자체의 기존 예외는 유지한다.
3. 제품 코드를 고치기 전에 Issue의 필수 본문, Priority·grade와 라벨의 일치, 수정 허용/금지 경로, 완료 기준, 현재 구현 의존성을 확인하고 `W/process/sdd/entry.md`의 구현 시작 조건과 `parallel-development` claim을 충족한다. 하나라도 빠지면 제품 코드를 고치지 않는다.
4. 각 원본이 정한 시작·변경 전 지점에서 `observations.md`의 시작 기록과, 켜져 있으면 `token-diagnostic.md`의 START를 남긴다. 재개·인계는 기존 시작 기록을 참조하며, 새 작업의 관측을 이전 작업에서 물려받지 않는다.
5. 현재 단계·역할에 들어갈 때는, 이미 실행 중이거나 사람이 고른 모델(current/manual)을 그대로 쓰는 경우에도 `execution-routing.md`의 해당 적격 경로를 확인한다. 공통 금지(canonical DENY)·실제 명시 기록 확인은 모델 전환 여부와 상관없이 생략하지 않으며, 현재 능력 기준(floor)을 확인할 때는 그 원본의 일반 Trivial/Small 예외를 적용한다. 같은 실행의 같은 역할에서 여전히 유효한 근거는 다시 쓰고, 아직 들어가지 않은 미래 단계의 모델 PASS를 지금 시작 조건으로 요구하지 않는다.

## 조사·설계와 grade별 진행

상위·관련 분석은 `W/process/sdd/entry.md`의 `기존 분석 재사용`에 따라 기준 revision·범위·전제·근거를 확인하고 부족하거나 달라진 부분만 보완한다. 재사용해도 해당 등급의 검토는 면제되지 않는다. 공통 변경은 그것을 쓰는 작업의 적용·호환성·전환 영향까지 담당 Issue의 범위와 검증에 넣는다.

1. 선언한 기준 revision에서 관찰한 코드를 AS-IS로, 현재 Issue가 요청한 것을 TO-BE로 삼는다. 직접 관련된 business 문서만 비교하며, 문서와 다르다는 이유로 코드를 예전 동작으로 되돌리지 않는다. 기준 구현·외부 동작·운영 소비자가 판단에 영향을 주면 `W/process/sdd/as-is.md`의 `판단에 필요한 조사`를 적용한다.
2. Issue와 architecture·완료 기준이 충돌하면 `agent-instruction-policy.md`로 판단하고, 풀리지 않으면 `BLOCKED: instruction conflict`로 멈춘다.
3. 저장소 파일의 첫 쓰기 전에 lane·claim을 확보한 뒤 아래 순서에 맞춰 현재 산출물을 쓴다. 최초 배치는 `W/process/sdd-artifacts.md`, 현재 산출물 작성은 위 표의 직접 경로를 따른다. 선택지를 만들려고 넓게 탐색하지 않는다.

| grade | 실행 순서 |
| --- | --- |
| Trivial | 조건을 확인하고 대상 텍스트·메타데이터와 직접 검증 근거만 조사한다. 별도 SDD나 제품 AS-IS 조사를 더하지 않으며, 조건을 벗어나면 고치기 전에 최소 Small로 다시 판정한다. |
| Small | Issue를 계획으로 쓰고 별도 SDD 없이 진행한다. |
| Medium | 필요한 SDD·검증 계획을 쓰고 충돌이 없으면 추가 승인 없이 구현한다. SDD 배치는 P의 `sdd.medium_artifacts` 값을 따른다. |
| Large | AS-IS 작성 → 그 단계의 유효한 설계 리뷰 → PLAN 작성 → 그 단계의 유효한 설계 리뷰 → 구현 순서로 진행한다. |

Large의 게시·리뷰 방식(P의 `review.large_mode`)·A/B·지적 등급·blind 격리·재확인·반복 정체는 `design-review.md` 한 곳에서 판정한다. 각 단계에서 현재 검토 대상의 근거와 `W/process/sdd/issue.md`의 `미결 사항과 단계별 의존성`을 확인하고, 필요한 결론이 확보된 작업은 진행하고, 결론이 아직 없는 경우 그 결론에 의존하는 작업만 기다린다. 빠지거나 낡은(stale) 근거를 과거 PASS로 대신하지 않는다. 재검토 전에는 같은 원본의 "검토 대상 유지 조건"부터 적용하며, 이 절차를 Medium 이하나 기본 CODE 리뷰에 더하지 않는다.

제품 파일을 고치기 전에 `verification.md`에 따라 기준 요구와 완료 기준을 검증에 연결하고 등급별 `Independent Review` 판정을 확보한다. Medium 이상의 Human Decision Contract는 `W/process/sdd/to-be.md`, 구현 명세는 `W/process/sdd/agent-spec.md`를 따른다. 증명할 수 없는 완료 기준이나 허용 경계 밖의 필수 검증은 `BLOCKED`다. 선택 사항인 Device QA/Runtime QA를 구현·PR·병합의 관문으로 만들지 않는다.

M `core.md`의 `사람 판단` 최소 요건도 적용한다. 그 판단에 의존하는 작업만 멈추고 묻고, 물을 수 없는 실행 환경이면 그 작업을 멈춘 채 질문을 미결로 기록한다.

사람 판단은 P 적용 선언의 `사람 판단 지점`을 직접 확인한다. 새 중요한 제품·설계 결정이나 확정 범위의 변경은 `[HUMAN DECISION REQUIRED]`로 영향받는 작업을 멈추고, 사람이 밝힌 결정을 Human View와 필요한 Issue 본문에 반영한 뒤 재개한다. 파일이 있다는 사실, Agent끼리의 합의, 리뷰 PASS를 사람의 결정으로 추정하지 않는다. 확정된 의미·불변조건 안의 실행 세부는 계속 처리한다.

## Implement

구현·검증 중에 PLAN의 전제 오류를 발견하거나 진행 중 작업의 정책이 바뀌면 `W/process/sdd/plan-change.md`를 적용한다. SUMMARY에 설명만 남기고 잘못된 PLAN을 실행 기준으로 계속 쓰지 않는다.

1. 이미 맡은 구현 역할을 유지하거나, 위임·모델 전환을 할 때 `execution-routing.md`로 현재 역할의 적격 근거를 확인하고 적격한 경우 그 원본의 일반 Trivial/Small 예외를 적용한다. 같은 실행에서 확보한 유효한 근거는 다시 쓴다. 지원되지 않는 대체 모델, 필수 리뷰어 분리, 사람이 고른 Review B 모델의 사용 불가는 그 원본의 조건과 상태를 그대로 따른다.
2. Packet으로 인계받았다면 첫 수정 전에 `execution-packets.md`의 `구현 진입의 문맥·최신성 확인`을 한다. 필수 입력·guard·claim·직접 원본을 증명하는 VALID 결과 없이 구현하지 않는다.
3. 제품 파일은 수정 허용 경로에 있고 수정 금지 경로에 없는 것만 고친다. 완료 기준 밖의 기능·리팩터링·이름 변경·포맷팅·의존성을 더하지 않는다. W·M 고정 사본은 고치지 않고 공통 문제로 보고한다.
4. 통합 작업에서만 고치는 공유·루트 경로가 필요해지면 직접 고치지 않고 `module-boundaries.md`에 따라 통합 의존성으로 돌린다. 수명이 정해진 문서도 그 원본이 허용한 범위만 바꾼다.
5. 테스트 준비와 첫 검증
   1. **준비:** P `build.md`의 테스트 수명·수행 주체를 적용해 허용 경로 안에 직접 회귀 테스트나 선언된 동등 검증을 준비한다. 테스트를 두지 않는(none) 프로젝트는 대체 근거를 확보한다.
   2. **첫 검증: 직접 관련 test class 또는 소유 모듈 테스트를 첫 검증으로 실행한다.** 이를 위해 `verification.md`의 구현 루프에 따라 검증에 영향을 주는 변경 파일(verification-affecting changed file)마다 소유 모듈을 먼저 확인한다.
   3. **범위:** 검증 범위는 같은 원본의 조건을 따르며, 구체적인 의존성·직접 영향·실제 실패 근거 없이 저장소 전체를 뒤지거나 검증을 넓히지 않는다.

   - **임시 테스트 수명:** 임시(temporary) 테스트는 보존·재조회한 뒤 지운다.
6. 필수 UI Visual Spec은 Issue에 고정된 영구 링크를 쓴다. Trivial에서 실행 의미를 바꿔야 하면 최소 Small로 다시 판정한다.
7. PLAN의 Implementation finding은 `execution-packets.md`의 인계·Result 규칙으로 보존하고, 현재 head의 코드와 fixture·테스트로 해결된 근거를 확보한다. Non-blocking observation을 새 구현 관문으로 올리지 않는다.
8. 실제 문제를 발견하고 해결하면 `observations.md`로 기록하고, 최초 문제와 조치·결과를 원본 참조와 함께 인계한다. 정상 단계에 사건 기록이나 추가 SDD·승인 관문을 만들지 않는다.

PLAN에서 구현 문맥으로 넘어갈 때는 `execution-packets.md`의 `구현 진입의 문맥·최신성 확인`을 적용한다. 실제 전환 근거·최소 입력·대체 한계를 남기고, 지원되지 않는 분리나 실패한 압축을 성공으로 기록하지 않는다. 진행 중인 IMPLEMENT lane을 거슬러 초기화하지 않는다.

## Verify and handoff

1. 선언된 영향 분석 결과를 쓰면 `execution-packets.md`의 `공통 영향 결과 참조와 로컬 소비`로 최신성·완전성을 확인한다. 낡은 결과로 Issue·등급의 필수 검증을 줄이지 않는다.
2. `verification.md`의 현재 등급·변경 범위·검증 순서·PASS 유효성을 적용한다. 실패 수정은 좁은(targeted) 검증부터 하고, 안정된 최종 후보에서 필요한 넓은(broad) 검증을 마친다.
3. 빌드·테스트 명령 전에는 `build-preflight.md`와 `verification.md`의 `검증 환경`을 적용하고, 같은 실행에서 검증된 환경을 다시 쓴다. 실제 빌드 JVM·허용된 교정·재실행 결과를 확인하며, 환경 때문에 막혔거나 실행하지 않은 것을 PASS로 기록하지 않는다.
4. 필수 검증의 실패나 미실행을 PASS로 기록하지 않는다. 등급상 필요 없는 빌드 검증이나 선택 기기 보고서가 없다는 것을 새 차단 요인으로 만들지 않는다. 수정·검증 때문에 수정 금지 경로가 필요해지면 멈춘다.
5. diff와 전체 변경 경로를 Issue 경계·완료 기준에 대조한다. Packet을 썼다면 `execution-packets.md`의 Result 검증으로 현재 head·파일 목록(inventory)·검증 근거·모든 PLAN 인계 항목의 유효성을 확인한다. 빠졌거나 미해결이거나 낡았으면 완료로 인계하지 않는다.
6. `finishing-issues`에 확인한 Issue·경계·검증·필수 리뷰 근거와 간단한 Result를 넘긴다. 공통 문서나 작업자 로그를 처음부터 다시 모으지 않는다. 관측 시작 기록·현재 결과·공백·다음 조치는 `observations.md`의 인계 형식으로 보존한다.

외부 요인으로 멈추거나 재개할 때는 `token-diagnostic.md`의 BLOCKED/RESUME 조건과 `observations.md`의 인계를 적용한다. 같은 미해결 차단 요인을 자동으로 다시 확인하거나 기록을 반복하지 않는다.

## Output

- Issue / grade / 현재 단계와 관문 / claim·격리
- 실제 변경 경로 / 완료 기준 / 검증·필수 리뷰 결과와 미검증
- 사람 판단·범위 이탈·BLOCKED와 재개 조건
- 사용한 실행 배정·Packet의 적격·유효 결과와 필요한 고정 근거 참조
- 관측 시작·사건·인계 참조와, 켜져 있으면 토큰 기록 또는 미수집 이유
