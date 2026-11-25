---
name: parallel-development
description: 이 프로젝트의 병렬 agent 작업의 claim·격리·동기화·해제·통합을 관리한다. 실행 Issue의 SDD·테스트·코드 등 P 작업 파일 최초 수정 전, branch/worktree 생성, 경로 충돌 확인, 공유 contract 처리에 사용한다. Issue 초안이나 읽기 전용 조사만 수행할 때는 사용하지 않는다.
---

Trivial/Small 현재/수동 작업은 [간결 경로](../../process/small-work.md)의 닫힌 읽기 집합·실행 의무·세 기록을 따른다. 아래 전체 본문은 그 경로의 예외가 해당 절을 열 때만 적용하며 간결 형식/면제는 유지한다. 격상 후에는 해당 등급의 전체 계약을 따른다.

외부 적용: 먼저 `W/activation.md`의 선택·소유·경로 계약을 적용한다. 아래 고정 사본·생성 hard guard 참조는 그 계약의 호환 의미를 따른다. 미선택 작업에는 이 스킬을 적용하지 않는다.

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `W`), `M`(고정 공통 원칙 `M`)이다. 현재 폴더나 W의 상위 폴더로 P·M을 추측하지 않는다. P의 hard guard(`P/AGENTS.md`의 `## 항상 적용 hard guard`)와 적용 선언(`W/../project/sdd-workflow.md`)을 적용한다. Issue·댓글·라벨·PR이라는 말은 `W/../project/tracker.md`가 선언한 작업 관리 방식(`W/tracker/`)으로 바꿔 읽는다. 낯선 용어는 [용어집](../../glossary.md)에서 찾는다.

# Parallel Development

## 읽기 전용 조사와 수정 진입

같은 파일을 여럿이 읽는 것은 수정 경로 충돌이 아니다. 읽기 전용 조사만 하려면 새 lane·branch/worktree·수정 claim을 만들지 않는다. 조사 자체의 접근 권한·현재 지시·확정된 선행 조건을 확인하고 기준 revision을 남긴다. 아직 정해지지 않은 공통 규칙의 결론은 그 결과에 기대는 구현·통합·배포 전에 확보한다.

아래 Inputs·신규 lane·Claim은 실제로 lane을 만들거나, 실행 Issue의 P 저장소 작업 파일을 처음 만들거나 고치거나 지우기 전에 적용한다. 현재 Issue의 SDD, 테스트, 제품 코드도 포함한다. 조사하다가 파일을 쓰기 시작하면 현재 단계의 작업 지시·의존성·경계를 확인하고 lane·claim을 확보한다. 같은 Issue의 기존 claim도 확인해 두 담당자가 같은 SDD나 branch에 동시에 쓰지 않게 한다.

SDD를 쓸 때는 그 작성 단계의 조건만 적용한다. AS-IS를 쓰기 위한 claim에 AS-IS/PLAN 리뷰 PASS나 이후 구현 준비 완료를 요구하지 않는다. 제품 구현은 필요한 등급 관문과 구현 의존성을 충족한 뒤 시작한다. 수명이 정해진 문서의 경로 표기 예외는 claim 면제가 아니다.

작업 관리 방식의 Issue·관측·claim/release 기록과 Epic 관리 문서 자체는 기존 관리 절차를 따른다. "이 기록을 쓰려면 먼저 구현 claim이 있어야 한다"는 순환 조건을 만들지 않는다. "읽기 전용"이라는 설명으로 기존 쓰기 경계나 필수 리뷰를 면제하지 않는다.

## Inputs

같은 실행(run)에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 적용됐다고 확인할 수 있으면 다시 읽지 않는다. 단독 실행이나 하위 에이전트로 시작해 확인할 수 없으면 그 절부터 읽고 진행한다. 공통 정책 문서는 충돌 조건이 없으면 미리 전체로 읽지 않는다.

필수:
1. 현재 Issue 본문·라벨의 `수정 허용` / `수정 금지`
2. 현재 Issue의 담당자, 최근 댓글, 연결되거나 열려 있는 PR
3. 같은 저장소의 진행 중 claim·PR 중 경로 겹침 판단에 필요한 메타데이터

구현 단계에서 이미 Issue 경계와 공유 경로 여부를 확인했다면 그대로 다시 쓴다.

필요할 때만:
- 단독으로 호출됐거나, 수정 허용 경로가 P 적용 문서 `module-boundaries.md`의 공유·루트 후보(루트 빌드·설정 포함)를 포함하면 `W/process/module-boundaries.md`의 공통 경계·수명 계약과 `W/../project/module-boundaries.md`의 실제 제품 경계 중 관련 부분을 확인한다.
- 지시·소유 충돌을 기존 규칙으로 판정할 수 없을 때만 `W/process/agent-instruction-policy.md`(공통 계약·수행법)와 `W/../project/agent-instruction-policy.md`(제품 적용·권한·검증)를 읽는다.

Issue에 수정 허용/금지 경로가 없으면 새 lane을 만들거나 claim하지 않고 Issue 관리 절차로 정규화한다.

## 신규 lane 생성과 isolation

이 절차는 새 Issue branch나 worktree를 만들 때만 적용한다. 새 lane의 기준(base)은 P `tracker.md`에 선언한 `<code-remote>/<base-branch>`를 방금 fetch한 것이다. 현재 로컬 HEAD, 로컬 기준 branch, 이전 Issue branch를 암묵적인 기준으로 쓰지 않는다.

1. 현재 저장소와 원격이 예상한 대상인지 확인하고, 현재 worktree·branch, 미커밋 변경(dirty) 상태, branch·worktree 경로 충돌을 확인한다. 이 로컬 상태는 오염·충돌 안전 확인에만 쓰고 기준 선택에는 쓰지 않는다.
2. Issue의 수정 허용 경로를 진행 중인 `[CLAIM]`·열린 PR과 비교하고, 통합 작업 전용인 공유·루트 경계를 확인한다. 겹치거나 허용되지 않은 공유 경계면 branch·worktree를 만들지 않고 해당 멈춤 조건으로 멈춘다.
3. branch·worktree를 만들기 직전에 현재 셸에서 `git fetch <code-remote> refs/heads/<base-branch>`을 실행한다. 실패하면 `BLOCKED: declared base fetch failed`로 멈추고, 기존 원격 추적 ref·로컬 기준 branch·현재 HEAD로 대신하지 않는다.
4. fetch가 성공하면 바로 `git rev-parse --verify 'FETCH_HEAD^{commit}'`로 기준 SHA를 확정하고 작업 근거에 남긴다. SHA를 확인할 수 없으면 branch·worktree를 만들지 않는다.
5. 확인한 기준 SHA를 명시적 시작점으로 쓴다.
   - 같은 로컬 clone에서 lane이 둘 이상이면 Issue별 branch와 저장소 밖 worktree를 `git worktree add <path> -b <branch> <base-sha>`로 함께 만든다.
   - 독립된 클라우드 clone·sandbox면 추가 worktree를 만들지 않고 `git switch -c <branch> <base-sha>`로 Issue branch를 만든 뒤 sandbox 자체를 lane으로 쓴다.
   - Windows 로컬 worktree는 짧은 경로를 쓴다(P 적용 문서 `sdd-workflow.md`의 `worktree root`).
6. 외부 설치이면 새 checkout에도 그 checkout 전용 하네스 연결을 설치하고 check한다. 기존 checkout의 연결 파일을 경로만 바꿔 다시 쓰거나, lock 하나로 두 checkout의 입구를 덮어쓰지 않는다. claim 조율을 위해 tracker_root는 공유한다.
7. 만든 lane의 HEAD가 기록한 기준 SHA와 같은지 확인한 뒤, 그 lane에서 아래 Claim 절차를 한다.

W·M 고정 사본(`W`, `M`)은 lane 작업에서 고치지 않는다.


- fetch와 branch·worktree 생성 사이에 다른 기준을 고르거나 로컬 기준 branch의 checkout·pull을 끼워 넣지 않는다.
- 두 agent가 같은 branch에 동시에 commit하지 않는다.
- 이미 만들어져 진행 중인 branch·worktree를 이 규칙 때문에 자동으로 rebase하거나 다시 만들지 않는다. 기존 lane 갱신은 Synchronization 절차만 적용한다.

모든 claim/release 조작은 이 agent와 branch가 소유한 claim에만 적용한다. 메타데이터 변경 전에 소유권을 다시 확인하고 다른 lane의 claim·담당자·진행 상태를 지우지 않는다. 경쟁 claim 실패 시 이번 시도가 소유한 상태만 해제한다. 소유권을 분리할 수 없으면 편집을 멈추고 충돌 상태를 보존해 조율한다. local-docs에서는 owner/status 변경 전에 배타적 claim 파일을 확보하며 획득 실패 시 둘 다 바꾸지 않는다.

## Claim

1. Priority와 현재 사용자 지시·선행 조건으로 볼 때 지금 단계의 조사 결과 작성·설계·구현이 가능한지 확인한다. 나중 구현 단계의 미결 조건을 앞선 SDD 작성 claim의 차단 조건으로 쓰지 않는다.
2. 수정 허용 경로를 진행 중인 `[CLAIM]`·열린 PR의 경로와 비교한다.
3. 겹치면 `BLOCKED: overlapping lane`.
4. 일반 lane인데 통합 작업 전용 공유·루트 경로가 필요하면 claim하지 않는다.
5. 현재 agent를 담당자(assignee)로 설정한다.
6. `status:in-progress`를 붙인다.
7. 다음 형식으로 댓글을 남긴다.

```text
[CLAIM]
agent: <agent-id>
branch: <branch-name>
allowed:
- <path glob>
forbidden:
- <path glob>
```

8. 댓글·라벨·담당자·열린 PR을 다시 확인한다.
9. 경쟁 claim이 생겼으면 즉시 release하고, SDD를 포함한 작업 파일을 고치지 않는다.

## Synchronization

선언된 기준·병합 branch에 관련 변경이 들어온 뒤, 다음 push 전에:
1. P가 선언한 코드 원격·기준 branch와 병합 branch의 필요한 revision을 fetch한다.
2. rebase나 merge를 한다.
3. Issue의 수정 허용 경로 안에서만 충돌을 푼다.
4. 수정 금지·공유 경로가 필요하면 `BLOCKED`.
5. 영향받은 검증을 다시 실행한다.

## SDD review candidate publication

P가 선언한 게시 저장소·branch에 AS-IS·PLAN 검토 후보를 올릴 때는 [설계 리뷰의 원격 후보 게시](../../process/design-review.md#원격-검토-후보-게시)를 적용한다. 후보와 문서를 원격에서 읽을 수 있다는 근거를 인계하고, 바뀐 후보의 재검토는 같은 문서의 의미·영향 판정을 따른다. 새 lane의 기준과 기존 claim·worktree 수명 주기는 위 절차를 유지한다.

## Shared contracts

일반 lane에서 공유·루트 경로를 바꿔야 한다는 사실이 새로 확인되면:
1. 그 경로를 고치지 않는다.
2. 필요한 계약·심볼·파일을 특정한다.
3. `W/process/module-boundaries.md`의 공통 경계·수명 계약과 `W/../project/module-boundaries.md`의 실제 제품 경계에서 통합 규칙을 확인한다.
4. 통합 Issue나 선행 변경으로 분리하고, 그에 기대는 lane을 멈추거나 release한다.
5. 공유 변경이 병합되면 선언한 통합 revision을 반영하고 재개한다.

local-docs 해제는 어댑터의 배타적 잠금 순서를 우선한다. 자기 claim을 보유한 상태에서 자기 메타데이터만 정리한 뒤 claim을 마지막에 제거한다. 잠금을 해제한 뒤 메타데이터를 뒤늦게 정리하지 않는다.

## Release

인계·중단·병합 후 정리 때는 먼저 미커밋·미push 상태, PR 상태, worktree 등록, 로컬·원격 branch 상태를 기록한다.

- 인계·중단으로 담당만 넘기는 경우, 미커밋·미병합 worktree를 지우거나 강제 삭제하지 않는다. `[RELEASE]` 댓글, `status:in-progress` 제거, 담당자 제거 뒤 worktree가 남아 있다는 사실을 따로 보고한다.
- 독립 클라우드 sandbox처럼 등록된 로컬 worktree가 없으면 상태를 기록한 뒤 일반 release 절차를 적용한다.
- 제품 반영 완료는 병합된 PR·닫힌 Issue와 `[PRODUCT COMPLETE]`로 판정한다. 로컬 정리와 담당 해제는 그와 별개이며, 정리 실패가 제품 완료를 취소하지 않는다. 로컬 정리·lane 해제는 아래 절차를 따른다.

### Merged local worktree cleanup

1. PR이 병합됐고 worktree가 깨끗한지 확인한다. 미커밋·미병합이면 지우지 않고 멈춘다.
2. 빌드 정리는 먼저 "산출물 없음" 예외를 판정해 처리한다.
   - **예외:** 그 lane에서 로컬 빌드 도구를 실행하지 않았다는 작업 근거가 있고, `git status --porcelain --untracked-files=all --ignored`가 비어 있어 추적·미추적·무시 파일과 사용자 파일이 하나도 없음을 확인했으면 빌드 정리를 건너뛰고 이유·근거를 남긴다. 하나라도 확인되지 않았거나 산출물이 있으면 이 예외를 쓰지 않는다.
   - **예외가 아니면:** 등록 제거 전에 P 적용 문서 `build.md`의 정리 명령을 확인한다.
     - 선언이 없으면 정리를 건너뛴 이유를 남긴다.
     - 있으면 `W/skills/_shared/build-preflight.md`를 적용(같은 실행의 JDK 재사용)하고 worktree에서 그 정리 명령을 실행해 기록한다.
3. preflight가 `BLOCKED: JDK unavailable`이면 등록 제거로 넘어가지 않고 그 상태로 멈춘다. JDK는 찾았지만 빌드 정리가 실패했거나 정리 뒤에도 미커밋 변경이 남으면 `CLEANUP_BLOCKED`로 멈춘다.
4. Windows worktree root는 P가 선언한 `worktree root` 형태의 짧은 경로를 유지한다. 제거 전에 이 명령에만 적용되는 `core.longpaths=true`가 유효한지 확인하고 결과를 남긴다. 긴 경로 지원을 확인할 수 없으면 `CLEANUP_BLOCKED`로 멈춘다.
5. 기본 clone에서 강제 옵션 없이 worktree를 제거한다. Windows에서는 `git -c core.longpaths=true worktree remove <exact-path>`를 쓴다.
   모든 worktree에 위 "산출물 없음" 예외와 나머지 정리 보호를 적용한다.
6. 제거 명령 결과와 별개로 다음 두 조건을 각각 확인한다.
   - `git worktree list --porcelain`에 그 정확한 경로의 등록이 없다.
   - 실제 폴더가 없다.
7. 둘 중 하나라도 남으면 그 정확한 root 아래를 읽기만 해서 다음 값을 기록한다.
   - 남은 파일 수와 폴더 수
   - 가장 긴 경로와 그 길이
   - worktree 등록 상태
   - 로컬·원격 branch 상태
8. 확인된 소수의 남은 파일이나 빈 폴더만 정해진 worktree root 아래에 남은 경우에만 하나씩 정리한 뒤 두 조건을 다시 확인할 수 있다. 수천 개처럼 하나씩 확인할 수 없는 대량 잔여물은 다른 재귀 삭제나 파일별 명령·반복문으로 우회하지 않고 `CLEANUP_BLOCKED`로 안전하게 멈춘다.
9. `[LOCAL CLEANUP]`에 `complete` 또는 `pending`과 함께 등록·실제 폴더 확인 결과, branch 상태, 근거·재개 조건을 남긴다. `complete`는 둘 다 없음이 확인된 경우에만 쓴다. 정리가 pending이어도 제품 완료·관측 수집을 막지 않는다. 등록과 실제 폴더가 모두 없음이 확인된 뒤에만 `[RELEASE]` 댓글, `status:in-progress` 제거, 담당자 제거를 한다. 하나라도 남으면 worktree 정리와 lane 해제는 미완료다. 이후 정리 상태만 바뀌면 `LOCAL CLEANUP`에 남기고 제품 완료 기록을 다시 쓰지 않는다. 사용자 파일 삭제·강제 제거 금지는 유지한다.

## Output

- claim 상태 / agent / branch
- 선언한 코드 원격·기준 branch의 fetch 결과 / 새 lane 기준 SHA
- 수정 허용 경로 / 충돌
- 격리 방식
- 공유 의존성
- release 상태
- JDK·빌드 도구 preflight·정리·재사용 결과
- Windows 긴 경로 확인 결과
- 로컬 worktree 등록·실제 폴더 정리 상태
- `CLEANUP_BLOCKED`이면 정확한 root, 남은 파일·폴더 수, 가장 긴 경로, 등록 상태, 로컬·원격 branch 상태
