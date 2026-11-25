---
name: managing-issues
description: 이 프로젝트의 작업 항목(Issue)을 생성·분류·우선순위 재조정·본문 재작성하고 선택적 Epic의 작업 구성·의존성을 조율할 때 사용한다. Priority/실행 grade 판정, 작업 경계, Mermaid 흐름 판단, UI/UX HTML Visual Spec 연결에 쓴다. 코드 구현에는 사용하지 않는다.
---

Trivial/Small 현재/수동 작업은 [간결 경로](../../process/small-work.md)의 닫힌 읽기 집합·실행 의무·세 기록을 따른다. 아래 전체 본문은 그 경로의 예외가 해당 절을 열 때만 적용하며 간결 형식/면제는 유지한다. 격상 후에는 해당 등급의 전체 계약을 따른다.

외부 적용: 먼저 `W/activation.md`의 선택·소유·경로 계약을 적용한다. 아래 고정 사본·생성 hard guard 참조는 그 계약의 호환 의미를 따른다. 미선택 작업에는 이 스킬을 적용하지 않는다.

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `W`), `M`(고정 공통 원칙 `M`)이다. 현재 폴더나 W의 상위 폴더로 P·M을 추측하지 않는다. P의 hard guard(`P/AGENTS.md`의 `## 항상 적용 hard guard`)와 적용 선언(`W/../project/sdd-workflow.md`)을 적용한다. Issue·댓글·라벨·PR이라는 말은 `W/../project/tracker.md`가 선언한 작업 관리 방식(`W/tracker/`)의 해당 기능으로 바꿔 읽는다. 낯선 용어는 [용어집](../../glossary.md)에서 찾는다.

# Managing Issues

## Inputs

같은 실행(run)에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 이미 적용됐다고 확인할 수 있으면 다시 읽지 않는다. 단독 실행이나 하위 에이전트로 시작해 확인할 수 없으면 그 절부터 읽고 진행한다.

먼저 읽을 것:

1. 현재 사용자 요청
2. `W/process/issue-priority.md`의 `## Priority 판정 순서`·`## 증거가 부족할 때`와 `W/../project/issue-priority.md`의 현재 단계·제품 적용. 새로 만들면 W의 `## 신규 Issue 필수 본문`·`## 필수 라벨`, 우선순위를 다시 정하면 W의 `## Priority 변경`
3. `W/process/sdd/grade.md`와 `W/../project/sdd-workflow.md`의 제품별 `### 자동 격상`. Issue 변경·사람 판단·미결 의존성은 `W/process/sdd/issue.md`(정규화 규칙도 여기)
4. `W/process/issue-writing-guide.md`의 `## 근거 기록 규칙`, `## Mermaid 생성 조건`, `## HTML Visual Spec 생성 조건`과 `W/../project/issue-writing-guide.md`의 `## 근거 기록 규칙`(개인정보·허용 근거). HTML이 필요할 때만 제품의 저장 위치·의존성 제한도 확인한다.
5. 기존 Issue를 바꾸면 그 Issue의 현재 본문·라벨·담당자·댓글·연결된 PR

제목(절) 단위로 읽을 수 없는 실행 도구에서는 위 파일을 전체로 읽어도 된다. 절 단위로 읽을 수 있는데도 "프로젝트를 전반적으로 이해하려고" 세 파일 전체를 미리 읽지 않는다.

필요할 때만 읽을 것:

- 제품·공유·루트 경로의 소유나 통합 판단이 필요할 때만 `W/process/module-boundaries.md`의 공통 경계·수명 계약과 `W/../project/module-boundaries.md`의 실제 제품 경계.
- 지시 충돌, 코드와 business 문서의 불일치, 모호한 범위가 실제로 생겼을 때만 `W/process/agent-instruction-policy.md`(공통 계약·수행법)와 `W/../project/agent-instruction-policy.md`(제품 적용·권한·검증).
- 같은 실행에서 이미 확인했고 바뀌지 않은 입력은 다시 쓴다.

Issue 분류에 필요하지 않으면 제품 코드를 넓게 뒤지지 않는다.

## Conversation-content gate

작업 관리 방식에 기록을 쓰기 전과 쓴 뒤에 반드시 확인한다.

- 대화 로그를 통째로든 일부든 인용·번역하거나, 원문을 되살릴 수 있는 요약을 기록하지 않는다. 사람이 작업을 위해 준 요구사항과 확정 결정의 최소 기록은 W `issue-writing-guide.md`의 `근거 기록 규칙`을 따른다.
- 요구사항 원천·확정 결정과, 조사 요청·제안을 구별한다. 허용된 작업 내용과 ID·메타데이터·측정값·원문을 되살릴 수 없는 분류 이름을 근거로 쓰며, 프로젝트가 금지한 내용은 요구사항이라는 이름으로도 옮기지 않는다.
- 세부 허용 목록은 `issue-writing-guide.md`의 `근거 기록 규칙`을 따른다.
- 금지 내용 없이 근거를 만들 수 없으면 `BLOCKED`.
- 쓴 뒤에 기록을 다시 확인한다.
- 이미 금지 내용이 쓰였으면 P의 근거 기록 규칙과 작업 관리 방식이 허용하는 제거 방법을 따른다. 제거할 수 없으면 사람에게 알리며, 다른 기록을 통째로 지우지 않는다.

## Create a new Issue

1. 요청을 실행 Issue 하나로 관리할지, 여러 Issue로 나눠 각각 배정·추적할지 정한다. 새 패키지나 큰 규모라는 이유만으로 나누지 않는다. 여러 Issue를 함께 관리할 때만 아래 `Epic 조율`을 적용한다.
2. W 공통 Priority 규칙과 P의 현재 단계·기능 사실로 Priority를 정한다.
3. W 공통 등급·일반 자동 격상과 P 제품 매핑으로 SDD grade를 정한다.
4. 실제 저장소 경로를 확인해 수정 허용(allowed)·수정 금지(forbidden) 경로를 쓴다. 제품·공유·루트 경계 판단이 필요할 때만 `module-boundaries.md`를 읽는다.
5. `W/process/issue-priority.md`에 정해진 신규 Issue 본문 절을 사용한다.
6. 각 완료 기준이 자동 테스트·CI와 등급별 리뷰로 성공·실패를 가릴 수 있는 조건인지 확인한다. 모든 Issue에 별도 Verification Strategy 절을 강제하지 않는다.
7. 본문과 일치하는 `priority:*`, `grade:*` 라벨을 각각 정확히 하나씩 붙인다.
8. Issue의 사람용 설명을 쓰거나 고칠 때 [사람용 문서의 시각적 작성](../../process/agent-instruction-policy.md#사람용-문서의-시각적-작성)을 적용한다. 핵심 변화부터 보여주고, 정책 비교나 소유·책임 경계도 필요한 표현으로 설명한다. 단순한 변경은 한 문장이면 된다. 같은 단계에서 `issue-writing-guide.md`의 Mermaid·HTML Visual Spec 조건을 판정하며 HTML을 만들고 저장하는 조건을 넓히지 않는다. 같은 실행에서 바뀌지 않은 기준은 다시 쓴다.
9. HTML이 필요하면 W `issue-writing-guide.md`의 `HTML 최소 내용`, `Visual Spec 링크 규칙`, `디자인 PR 병합·배포·정리`를 P 적용 문서 `issue-writing-guide.md`의 `Visual Spec`이 선언한 저장·게시 방식에 맞춰 적용한다. 선언이 없으면 HTML Visual Spec을 만들지 않는다. 디자인 병합을 앱 승인·완료로 보지 않으며, 게시·정리가 실패하면 마지막으로 성공한 단계와 남은 상태를 기록한다.
10. 완성된 Issue를 다시 읽어 본문 절·라벨·Visual Spec(해당할 때)·대화 내용 확인(위 gate)을 검증한다.

## Epic 조율

`W/process/sdd/epic.md`를 적용한다. Epic은 실행 등급이 아니며, 만들거나 나눌 때 독립 리뷰·원격 게시·A/B 통과를 요구하지 않는다. 실행 Issue를 만들 때의 등급·경로·구현 검증 항목을 관리 문서에 그대로 적용하지 않고, `issue-priority.md`의 Epic 본문·라벨 구분을 따른다.

- 전체 목표·완료 기준·공통 가이드와 하위 Issue 참조, 책임과 선후 관계, 미결 사항의 조사 담당과 그 결론이 필요한 후속 단계, 전체 완료 근거와 담당을 연결한다. 별도 분해(breakdown) 파일은 필수가 아니다.
- 목표 누락, 책임 공백, 의존성 모순, 미결 사항의 담당 누락을 스스로 점검한다. 미결 사항 자체는 하위 Issue의 조사 시작을 막지 않는다. 그 결론을 쓰는 구현·통합·배포 단계에만 의존성을 둔다.
- 공통 질문을 모으고 결정 뒤 하위 미결 표시를 갱신하는 일은 `W/process/sdd/issue.md`의 `미결 사항과 단계별 의존성`을 따른다. 기준 구현을 지정하는 요구의 이름과 운영 근거가 서로 어긋나면 `W/process/sdd/as-is.md`의 `판단에 필요한 조사`로 확인하고, 그 전제에 기대는 작업만 기다리게 한다.
- 공통 변경은 그것을 쓰는 작업과 전환 영향까지 담당 실행 Issue의 범위·완료 기준에 넣고 그 Issue의 등급을 정한다. 공통 설계를 관리 문서에만 남기고 검증 책임을 비워 두지 않는다.
- 조사 결과에 따라 위임받은 범위 안에서 작업을 나누거나 합치고, 책임·순서를 바꿀 수 있다. 진행 중인 lane의 경계는 담당에게 변경과 영향을 알리고 claim 충돌을 푼 뒤 조정한다. 목표·완료 기준을 줄이거나 기존 사람 결정을 바꾸는 일은 기존 사람 판단 규칙을 따른다.
- 전체 목표가 달성됐다는 근거를 확인하고 Epic을 닫는다. 구현용 PR·CI·SDD가 없는 관리 문서에 제품 변경 종료 절차를 강제하지 않는다.

## Triage / reprioritize

Epic 관리 문서는 위 `Epic 조율`로 책임·의존성·전체 완료 근거를 갱신하고 실행 등급을 붙이지 않는다. 아래는 실행 Issue에 적용한다.

1. 현재 Issue와 꼭 필요한 최소 근거만 읽는다.
2. 현재 규칙으로 Priority를 다시 판정한다.
3. 범위나 위험이 바뀐 경우에만 등급을 다시 판정한다.
4. 값을 바꾸면 본문과 라벨을 같은 작업에서 맞춘다.
5. 범위가 바뀌면 경계·Mermaid·Visual Spec·의존성·완료 기준도 다시 판정한다.
6. 바뀐 완료 기준을 자동 테스트·CI와 등급별 리뷰로 가릴 수 있는지 확인한다.
7. 완성된 Issue를 다시 읽는다.

## Stop conditions

다음이면 `BLOCKED`로 멈추고 구현하지 않는다.

- 필요한 경로를 확인할 수 없음
- `agent-instruction-policy.md`로도 풀리지 않는 지시 충돌
- 필수 Visual Spec이나 고정 링크를 만들 수 없음
- 문서의 기본값까지 적용해도 Priority를 정할 수 없음
- 진행 중인 다른 lane의 범위를 침범해야 함
- 대화 내용 확인(위 gate)을 통과하는 근거를 만들 수 없음

## Output

Issue 번호·제목, Priority·grade·라벨, 수정 허용·금지 경로, Mermaid·Visual Spec, 대화 내용 확인 결과, 의존성·BLOCKED를 짧게 보고한다. Epic 관리 문서는 grade 대신 작업 유형과 하위 책임·의존성·전체 완료 근거를 보고한다.
