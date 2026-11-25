---
name: finishing-issues
description: 구현을 마친 이 프로젝트의 Issue 작업을 종료한다. 최종 diff 검토, business 문서 동기화, 검증·CI gate, SDD 정리, PR 종료 구문, merge 확인, lane 해제에 사용한다. 구현이 종료 준비되기 전에는 사용하지 않는다.
---

Trivial/Small 현재/수동 작업은 [간결 경로](../../process/small-work.md)의 닫힌 읽기 집합·실행 의무·세 기록을 따른다. 아래 전체 본문은 그 경로의 예외가 해당 절을 열 때만 적용하며 간결 형식/면제는 유지한다. 격상 후에는 해당 등급의 전체 계약을 따른다.

외부 적용: 먼저 `W/activation.md`의 선택·소유·경로 계약을 적용한다. 아래 고정 사본·생성 hard guard 참조는 그 계약의 호환 의미를 따른다. 미선택 작업에는 이 스킬을 적용하지 않는다.

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `W`), `M`(고정 공통 원칙 `M`)이다. 현재 폴더나 W의 상위 폴더로 P·M을 추측하지 않는다. P의 hard guard와 적용 선언을 따르고, Issue·댓글·라벨·PR이라는 말은 `W/../project/tracker.md`가 선언한 `W/tracker/` 방식으로 바꿔 읽는다. 낯선 용어는 [용어집](../../glossary.md)에서 찾는다.

# Finishing Issues

Epic 관리 문서의 종료는 `managing-issues`의 `Epic 조율`에서 전체 목표 달성 근거를 확인한다. 아래 제품 변경 종료 순서를 코드·PR·CI·SDD·claim이 없는 관리 문서 자체에 요구하지 않는다. 하위 Issue가 닫혔다는 표시만으로 Epic을 닫지 않는다.

## Inputs

같은 실행(run)에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 적용됐다고 확인할 수 없으면 그 절부터 읽는다. 구현 단계에서 확인했고 바뀌지 않은 입력·검증 결과는 다시 쓴다. 조회·갱신은 `implementing-issues`의 `입력 재사용과 조회` 절을 적용하며 그 스킬 전체를 다시 읽지 않는다.

필수 입력은 현재 Issue 본문·라벨, 현재 diff, `W/process/sdd/completion.md`·`W/process/sdd/issue.md`의 종료 순서·SUMMARY 계약(등급을 다시 판정하면 `W/process/sdd/grade.md`), P 적용 선언의 권한·경로·검증이다. PR이 있으면 필요한 PR·CI 메타데이터를, 실행 동작이 바뀌었으면 직접 관련된 business 문서를 읽는다.

아래 순서에서 필요한 원본의 **해당 절만** 읽는다.

| 행동 | 읽을 원본 |
| --- | --- |
| Large AS-IS/PLAN 근거 유효성 확인 | `W/process/design-review.md`의 현재 검토 대상·다음 단계 조건·재확인 절 |
| 검증·등급별 코드 리뷰·PASS 재사용 | `W/process/verification.md`와 P 적용 문서 `build.md`의 해당 검증 |
| Packet·구현 문맥 전환·선언된 영향 분석 결과 소비 | `W/skills/_shared/execution-packets.md`의 해당 Packet·영향 결과 절 |
| 이미 맡은 종료 역할의 유지나 리뷰어 배정의 적격 확인 | `W/skills/_shared/execution-routing.md`의 해당 역할·선택 경로 |
| SDD의 결정·구현 명세 확인 | `W/process/sdd/to-be.md`·`W/process/sdd/agent-spec.md` 중 확인할 계약 |
| business 문서 수명·공유·루트 경계 판단 | W/P `module-boundaries.md`의 관련 경계 |
| 지시·diff와 Issue·코드와 business 문서 충돌 | W/P `agent-instruction-policy.md`의 해당 충돌 절 |
| 관측 취합·SDD 삭제 전 보존·제품 완료 관측 | `W/process/observations.md`의 해당 단계 절 |
| 켜져 있는 토큰 기록의 중단·재개·종료 | `W/process/token-diagnostic.md`의 해당 사건 |
| worktree 정리·담당 해제 | `W/skills/parallel-development/SKILL.md`의 Release와 해당 정리 절 |

종료 역할에 들어갈 때, 이미 실행 중이거나 사람이 고른 모델(current/manual)을 그대로 쓰는 경우에도 `execution-routing.md`로 그 역할의 공통 금지(canonical DENY)·실제 명시 기록·최신 능력 기준(floor)을 확인한다. 같은 실행의 같은 역할에서 여전히 유효한 근거는 다시 쓰며, 모델을 바꾸지 않는다는 이유로 이 확인을 생략하지 않는다.

## Finish in fixed order

### 1. Confirm actual change

1. base/head SHA와 현재 head의 **전체 변경 파일 목록(inventory)**을 직접 확인하고 diff를 읽는다. 작업자가 골라 준 목록만 믿지 않는다. Result Packet을 받았다면 `execution-packets.md`로 현재 diff·파일 목록·근거의 유효성을 검증한다.
2. 동작 변경과 포맷팅·주석·생성 파일 변경을 구분하고, 실제 변경 하나하나를 Issue 완료 기준에 연결한다. `verification.md`의 "기준 요구 → 검증" 대응을 거꾸로도 확인해, 빠진 진입점·조건, 약해지거나 실행하지 않은 검증의 대체 근거와 공백을 SUMMARY에 드러낸다.
3. 사람 결정(Human Decision)·구현 명세·diff를 대조한다. 사람이 정하지 않은 새 중요한 결정이나 의미 변경이 있으면 P의 `[HUMAN DECISION REQUIRED]` 절차로 영향받는 작업과 종료를 멈춘다. Agent끼리의 합의나 리뷰 PASS를 사람의 결정으로 대신하지 않는다.
4. Large는 `design-review.md`에 따라 AS-IS와 PLAN 각각의 현재 검토 대상 근거가 유효하고, 필요한 재확인·reconciliation이 끝났는지 확인한다(P의 `review.large_mode`가 정한 방식 기준). 빠지거나 낡은 PASS, 분리·선택·격리 실패를 "이미 구현했다"는 사실로 정당화하지 않으며, 유효한 근거가 없으면 종료를 멈춘다. 사람에게 상세 리뷰 전체를 다시 읽으라고 요구하지 않는다.
5. 범위 밖 변경은 수정 허용 경로 안에서 안전하게 되돌리거나 `BLOCKED`한다. W·M 고정 사본을 고쳐야만 풀리면 공통 문제로 보고한다.

구현 문맥 전환 근거와 대체 한계도 해당 Packet 계약으로 확인한다. 필수 근거를 잃은 압축·인계를 성공으로 추정하지 않으며 로그 전문을 다시 모으지 않는다. 반복 정체로 멈춘 차단 요인은 `design-review.md`가 정한 해결 근거나 사람의 범위 결정 없이 종료하지 않는다.

사람용 변경 문서와 아래 PR·완료 요약은 `agent-instruction-policy.md`의 `사람용 문서의 시각적 작성`을 같은 자체·필수 리뷰에서 확인한다. 추가 승인·리뷰 회차·그림 개수 같은 관문을 만들지 않고 단순한 설명은 짧게 둔다.

### 2. Synchronize business documents

실행 동작이 바뀐 경우에만 직접 영향을 받는 P의 business 규칙·주제를 확인한다. Issue·SDD의 설명 대신 **최종 코드**로 실제 동작을 확인하고, 바뀐 기존 규칙만 갱신한다.

같은 business 파일을 진행 중인 다른 lane·PR이 고치고 있으면 `BLOCKED: documentation lane conflict`다. 수명이 정해진 문서의 허용 범위는 `module-boundaries.md`를 따른다. 실행·제품 동작이 바뀌지 않았으면 동기화를 이유로 business 문서를 만들거나 고치지 않는다.

### 3. Verify before SDD cleanup

1. 선언된 영향 분석 결과를 쓰면 `execution-packets.md`의 `공통 영향 결과 참조와 로컬 소비`로 최신성·완전성을 확인한다. 낡은 결과로 필수 검증을 줄이거나 이전 SHA의 리뷰 PASS를 물려받지 않는다.
2. SDD를 지우기 전에 구현의 필수 검증 근거를 확인하고, 빠지거나 무효가 된 검증을 실행한다. 입력이 바뀐 뒤의 좁은(targeted) 재실행, 필수 넓은(broad) 재실행, 입력이 그대로일 때의 PASS 재사용은 `verification.md`를 따른다. 이 시점의 확인으로 정리 후 최종 후보의 CODE Review·완료 판정을 대신하지 않는다. business 동기화 전에 CODE Review가 있었다면 과거 근거로 보존하고, 새 후보의 CODE Review는 5단계에서 판정한다.
3. 빌드·테스트 명령 전에 `build-preflight.md`와 `verification.md`의 `검증 환경`을 적용한다. 환경 실패를 제품 회귀로 단정하지 않으며, 선언된 실제 빌드 JVM 확인과 허용된 이번 프로세스 한정 교정 결과만 정식 근거로 쓴다. 실행하지 않았거나 환경 때문에 막힌 것을 PASS로 기록하지 않는다.
4. 명령·결과와 필요한 CI를 확인한다.
   - 필수 검증이 실패했거나 미실행이면 해당 필수 명령과 확인한 결과를 완료 보고에 명시하고 미완료로 둔다.
   - 명령명이나 결과 근거가 없으면 그 정보가 없음을 밝히고 필요한 근거를 확인하기 전까지 미완료로 둔다. 명령명이나 결과를 추측하지 않는다.
   - Trivial 등 그 등급에 필요 없는 빌드나 선택 사항인 Device QA/Runtime QA·보고서가 없으면 나머지 완료 조건에 따라 종료를 계속한다. 이 부재는 새 관문이 아니다.
5. 전체 변경 경로가 Issue의 수정 허용/금지 경로와 맞는지 다시 확인한다. Result Packet이 있으면 `execution-packets.md`의 현재 head 기준 검증 근거와 PLAN Implementation finding 해결 조건을 충족해야 한다. "명령이 성공했다"는 자기 보고만으로 PASS를 증명하지 않는다.
6. 외부 차단 요인은 상태와 재개 조건을 기록하고 `observations.md`와, 켜져 있으면 `token-diagnostic.md`의 BLOCKED/RESUME을 적용한다. 해소 근거 없이 재개하거나 자동으로 다시 확인하거나 기록을 반복하지 않는다.

### 4. Remove temporary SDD

SDD나 로컬 결과에만 있는 발견 사건은 지우기 전에 `observations.md`의 [문제 발견 시 기록과 종료 연결](../../process/observations.md#문제-발견-시-기록과-종료-연결)로 기존 Issue에 보존한다. 검토한 SDD를 사건 장부로 고치지 않는다. 보존에 실패하면 인계·종료에 드러내고 계속한다(새 관문 아님).

Trivial·Small은 해당 없다. SDD가 있으면:

1. business 동기화와 필요한 검증을 마친 뒤 **현재 Issue의 SDD만** 정리한다. 연결된 진행 중 Issue·계획의 직접 참조를 확인하고, 쓰이고 있는 계약·결정 근거는 아래 참조 보존 조건을 적용한 뒤 지운다. 검토 문서는 지운 뒤에도 삭제 직전의 정확한 커밋에서 계속 조회할 수 있어야 하며, 일부만 지우거나 설계를 고친 것을 "정리"로 숨기지 않는다.
2. P가 선언한 문서 목차와 관련 문서에서 필요 없어진 링크를 지운다. 진행 중인 소비자가 필요한 링크는 지우지 말고 조회 가능한 고정 참조나 계속 관리되는 계약 문서로 바꾼다.
3. 과거 리뷰 기록의 바뀔 수 있는 상태값이 낡았으면 그 상태값만 갱신한다.

**참조 보존 조건:** 지우기 전에 정확한 revision·경로로 소비자가 필요한 원문과 직접 의존 문서를 실제로 조회할 수 있는지 확인한다. 계속 관리되는 문서로 옮기면 의미가 유지되는지 확인한다. 다른 lane의 문서를 고칠 때는 그 담당·claim과 조율하며, 링크만 바꾸는 작업으로 계약 변경을 숨기지 않는다. 필요한 참조 전환을 지금 끝낼 수 없으면 현재 SDD 폴더를 보존하고 기존 SUMMARY에 소비 Issue, 보존 이유, 정리 담당, 해제 조건(소비자의 참조 전환 또는 의존 종료)을 남긴다. 담당 인계·조회 가능성이 확인된 보존은 허용된 정리 완료로 처리하고 계속한다(새 관문 아님).

접근 가능한 원문이나 정리 담당을 확보하지 못했으면 허용된 보존으로 처리하지 않는다. 담당은 해제 조건이 채워진 뒤 기존 권한·claim 안에서 정리하며, Epic 전체 종료까지 무조건 남겨 두거나 완료 뒤 남은 파일을 허락 없이 지우지 않는다.

### 5. Prepare/verify PR closure

business 동기화, 현재 SDD 삭제 또는 위 조건에 따른 보존, 링크·리뷰 상태 정리처럼 예정된 저장소 파일 변경을 먼저 끝낸다. 그 결과를 commit하고 현재 base/head·전체 diff·파일 목록을 최종 리뷰 후보로 고정한다. 과거 CODE Review의 대상과 다른 후보를 기존 PASS로 완료 처리하지 않는다.

1. CODE Review·자체 리뷰 전에 `verification.md`의 필수 넓은 검증 명령 묶음에 대해 현재 후보에 유효한 PASS 근거를 확보한다. 3단계에서 입력이 그대로인 PASS는 실행 기록을 보존해 다시 쓰고, 정리한 문서를 읽는 정적 검사기처럼 빠지거나 무효가 된 검증만 해당 계약의 순서로 실행한다. 검증 보정으로 파일이 바뀌면 새 후보와 그 검증 근거를 먼저 확정한다.
2. `verification.md`의 `Grade별 review gate`를 현재 후보에 적용한다. Trivial·Small은 해당 자체 리뷰, Medium은 `Independent Review` 판정, Large는 범위를 정한 독립 코드 리뷰 1회의 유효한 결과를 확인한다. Trivial 조건을 벗어나면 최소 Small로 다시 판정한다. 같은 후보에서 이미 유효한 리뷰는 다시 쓰며 기본 CODE 리뷰에 Review B를 더하지 않는다.
3. 필수 리뷰어에게 앞서 확보한 검증 근거를 포함한 `execution-packets.md`의 현재 CODE Review Packet을 준다. 리뷰어는 검증 근거의 유효성·재사용 조건, 전체 파일 목록과 PLAN 인계 항목의 완전성, 현재 코드·fixture로 해결됐는지를 독립적으로 확인한다. 지운 SDD의 검토 원문은 삭제 직전의 정확한 커밋으로 참조한다. 필요한 근거가 없거나 반드시 해결할 지적·INVALID/STALE이 남으면 병합·완료로 가지 않는다.
4. 리뷰 뒤 현재 후보의 리뷰·검증 근거가 모두 유효한지 확인한다. 리뷰 지적 반영 등으로 저장소 파일이 바뀌면 새 후보를 고정하고, 영향받은 검증을 갱신한 뒤 그 후보의 CODE Review·자체 리뷰 근거를 확보한다. 입력이 바뀌지 않은 검증은 반복하지 않으며, 빌드 PASS 재사용을 이전 CODE Review 대상의 자동 승계로 넓히지 않는다.

아래 PR·SUMMARY 기록은 위 후보의 유효한 리뷰·검증 근거에 연결한다. PR 메타데이터만 바뀌고 저장소 후보가 그대로면 같은 CODE Review를 다시 하지 않는다.

1. PR 범위를 Issue 경계·완료 기준과 대조하고 이 Issue의 closing reference(`Closes #{issue-number}`, 선언한 작업 관리 방식의 표기)를 넣는다.
2. 기존 `[IMPLEMENTATION SUMMARY]` 하나에 결정 준수·실행 이탈·사람에게 올린 판단·검증·남은 위험을 정리한다. 이미 있으면 갱신하며 새 문서나 사람 승인 관문을 더하지 않는다.
3. 같은 SUMMARY에 `observations.md`의 종료·작성 모델·발견 사건 규칙을 적용한다. 최초 문제·담당·조치와 결과·원본 참조를 보존하고 PR 이후 CI·리뷰 사건도 모은다. 사건이 없으면 빈 사건 목록을 만들지 않는다.
4. 관측 시작 기록·실제 지원·사용·공백·비용 출처·작성 모델·다음 판단을 원본 형식으로 연결한다. 모델 미확인·관측 미수집에도 계속한다([새 관문 아님](../../process/observations.md)). 합성 평가 PASS나 자기 보고를 효과의 증거로 기록하지 않는다.
5. Large PR은 P의 사람 판단 지점에 따라 사람이 직접 병합하거나 그 PR의 병합을 명시적으로 지시한 경우에만 병합한다. 일반 진행 지시·리뷰 PASS·CI 통과만으로 병합하지 않는다.
6. 필수 CI·리뷰와 나머지 완료 조건이 채워지기 전에는 완료라고 말하지 않는다.

### 6. Merge confirmation and release

1. 병합 직전과 병합 뒤 종료 확인 시점에 필요한 메타데이터를 새로 읽고, 실제로 PR이 병합되고 Issue가 닫혔는지 확인한다.
2. 정리 전에 관측 시작 기록·SUMMARY·필요한 원본을 오래 보존되는 위치에서 다시 조회한다. 결과와 조회 공백은 `observations.md`의 제품 완료 관측으로 SUMMARY에 남긴다. 로컬 worktree를 이후 관측의 유일한 원본으로 남기지 않는다.
3. `observations.md`의 [종료 관측 점검](../../process/observations.md#종료-관측-점검)을 적용한다. 이 릴리스의 `observation-check unavailable reason=not-shipped` 결과와 필요한 최초 출력·재실행 이유를 준비하고 계속한다(새 관문 아님).
4. 위 점검 결과와, P가 선언한 병합 대상 branch에 실제로 병합된 PR의 종료 구문·병합 SHA로 `[PRODUCT COMPLETE]`를 한 번 기록한다. 첫 줄 태그 다음에 선언한 작업 관리 방식 형식의 `product-complete:` JSON을 둔다(GitHub은 `{"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40자리 SHA"}`). 제품 완료와 로컬 정리·담당 해제는 별개이며, 같은 수명 주기의 완료 기록을 중복으로 만들지 않는다.
5. `parallel-development`의 Release·Merged local worktree cleanup을 실행한다. 등록 제거 전에는 이번 실행이 만든 것인지, 생성 파일인지 어느 쪽으로도 증명되지 않은 미추적 진단·정체불명 파일이 없는지 확인한다. 그런 파일은 사용자 상태로 보존하고 등록 제거·RELEASE를 멈춰 lane 해제 미완료로 보고한다.
6. "산출물 없음" 예외, 빌드 정리, 등록·실제 폴더 각각의 부재 확인, 허용된 잔여 정리와 담당 해제 순서는 그 원본을 따른다. 현재 claim·환경 근거를 다시 쓰고, 강제 정리나 대량 파일의 개별 삭제 반복문으로 보호 정책을 우회하지 않는다.
7. 정리·해제가 pending이면 정확한 경로·상태·재개 조건을 보고하고 제품 완료 상태를 유지한다. 정리만의 후속 갱신은 `[LOCAL CLEANUP]`에 남기고 제품 완료 기록을 다시 쓰지 않는다.
8. 제품 완료가 확인되면 로컬 정리와 별개로, 켜져 있으면 `token-diagnostic.md`의 END를 적용한다. `not-planned`는 병합 대신 최종 종료가 확정될 때 같은 원본의 해당 종료 형식을 쓴다.

## Incomplete conditions

다음이면 제품 Issue를 완료라고 하지 않는다.

- 완료 기준 실패·불명, 필수 CI 실패, 필수 리뷰 미완료, 반드시 해결할 지적 미해결
- `design-review.md`의 필수 현재 검토 대상 근거 누락·낡음, 필수 reconciliation 미완료, Human Decision/Execution-contract blocker 미해결
- `execution-packets.md`의 필수 PLAN 인계 항목·코드/fixture 해결·검증 근거의 누락·미해결·INVALID/STALE
- 필수 business 문서가 최종 코드와 모순되거나 documentation lane conflict
- 필수 SDD 정리 미완료, PR 종료 구문 없음, 미해결 제품 작업 BLOCKED

`CLEANUP_BLOCKED`, 등록·실제 폴더 잔여, 정체불명 파일은 로컬 정리 미완료로 따로 보고한다. 사용자 파일 삭제 금지는 그대로 적용한다.

관측·모델 기록 미확인에도 계속한다([새 관문 아님](../../process/observations.md)). 필수가 아닌 기기 확인은 각 원본의 비차단 조건을 유지한다.

## Output

- 실제 변경 경로 / 완료 기준 결과 / business 문서 상태
- 검증·CI·필수 리뷰와 현재 검토 대상·Packet 근거의 유효성
- SDD 정리 / PR·Issue·제품 완료 / 관측 취합 참조
- 켜져 있으면 토큰 BLOCKED/RESUME/END 기록 또는 미수집 이유
- 로컬 정리·lane 해제 / 미검증·BLOCKED와 재개 조건
