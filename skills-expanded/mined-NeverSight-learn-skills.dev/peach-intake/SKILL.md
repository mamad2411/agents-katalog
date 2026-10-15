---
name: peach-intake
description: |
  PeachSolution 개발 요청이나 PRD를 구현 전에 접수·분류하여 필요한 다음 스킬 경로를 판정하는 게이트 스킬.
  "어떤 스킬로 시작할까", "요청 분석", "PRD 분석", "개발 경로 판단", "Spec/DB/proto 필요 여부 판단",
  "작업 규모 판단", "intake" 키워드로 트리거.
  코드 구현, 마이그레이션 생성, ui-proto 생성, E2E 실행은 하지 않고 peach-gen-spec, peach-gen-db,
  peach-team-ui-proto, peach-team-dev, peach-team-e2e 중 어떤 흐름을 탈지 결정한다.
---

# Peach Intake

PeachSolution 개발 요청을 실제 구현 전에 분류하고 다음 실행 경로를 정한다.

## 역할

`peach-intake`는 구현 스킬이 아니라 **판정 게이트**다. 사용자의 자연어 요청, PRD, 기존 문서, Spec/proto/schema 존재 여부를 읽고 어떤 기준을 먼저 보강해야 하는지 판단한다.

이 스킬은 다음을 수행한다.

- 작업 유형과 규모를 판정한다.
- Spec, DB, ui-proto 필요 여부를 판단한다.
- 바로 개발해도 되는지, 기준 보강이 필요한지 분리한다.
- 후속 스킬 호출 순서를 제안한다.
- 막힘 항목을 `*_REQUIRED`로 보고한다.

이 스킬은 다음을 하지 않는다.

- 코드 구현
- DB 마이그레이션 생성
- Spec 장문 생성
- ui-proto 화면 생성
- E2E 시나리오 작성/실행

## 입력

```bash
/peach-intake "요청 자연어"
/peach-intake prd=<PRD 경로>
/peach-intake spec=<Spec 경로> [proto=<ui-proto 경로>] [schema=<schema 경로>]
/peach-intake "기존 기능에 승인/반려 상태 추가"
```

| 입력 | 의미 |
|------|------|
| 자연어 요청 | 아직 정제되지 않은 개발 요청 |
| `prd` | PRD 원천 문서. 구현 기준이 아니라 누락 확인용 원천 |
| `spec` | 이미 작성된 구현 기준 |
| `proto` | ui-proto 태스크 폴더 |
| `schema` | DB schema 또는 migration 기준 |

입력이 너무 짧거나 모호하면 바로 질문한다. 단, 질문은 1~3개로 제한하고 구현으로 넘어가지 않는다.

## 판정 기준

상세 판단표는 `references/decision-matrix.md`를 참조한다.

### 작업 규모

| 규모 | 기준 | 권장 경로 |
|------|------|-----------|
| 소 | 단일 파일, 명확한 버그, DB/권한/상태 변경 없음 | 직접 수정 또는 `peach-team-3a` |
| 중 | 단일 모듈, API/Store/UI 중 2개 이하, 기준 일부 존재 | 필요한 기준 보강 후 `peach-team-dev` |
| 대 | 신규 모듈, 다중 화면, 상태 전이, 권한, DB 변경, PRD 기반 | `peach-gen-spec`부터 시작 |

### 기준 필요 여부

| 기준 | 필요 신호 |
|------|-----------|
| Spec | 권한, 상태 전이, 오류 케이스, API 기대값, TEST_ID가 필요함 |
| DB | 신규 테이블/컬럼/인덱스/상태값 또는 데이터 이력 구조가 필요함 |
| ui-proto | 신규 복잡 화면, 다단계 폼, 다중 모달, 탭, 차트, 기획자 화면 검토가 필요함 |
| E2E | 사용자 흐름, 권한별 화면 차이, 저장 후 결과 확인, 통합 흐름 검증이 필요함 |

## 처리 흐름

1. 입력 자료를 확인한다.
2. 작업 유형을 판정한다.
3. 작업 규모를 소/중/대로 분류한다.
4. Spec, DB, ui-proto, E2E 필요 여부를 판단한다.
5. 기준 충돌이나 모호한 항목을 `*_REQUIRED`로 분리한다.
6. 후속 스킬 실행 순서를 제안한다.
7. Intake 결과를 보고한다.

## 결과 분류

| 분류 | 의미 | 처리 |
|------|------|------|
| `READY_FOR_DEV` | 구현 기준이 충분함 | `peach-team-dev`로 진행 |
| `SPEC_REQUIRED` | 구현 기준이 부족함 | `peach-gen-spec` 실행 |
| `SPEC_REVIEW_REQUIRED` | Spec은 있으나 TEST_ID/권한/상태/오류 기준이 약함 | Spec 보강 |
| `DB_REQUIRED` | DB 구조 생성이 필요함 | `peach-gen-db` 실행 |
| `DB_DECISION_REQUIRED` | DB 판단이 모호함 | 사용자 결정 후 DB 단계 진행 |
| `PROTO_RECOMMENDED` | ui-proto가 1차 완성도를 높임 | `peach-team-ui-proto` 권장 |
| `PROTO_REQUIRED` | 화면 해석 검증 없이는 재작업 가능성이 큼 | ui-proto 선행 |
| `E2E_REQUIRED` | 사용자 흐름 검증이 필요함 | 구현 후 `peach-team-e2e` |
| `PRD_TO_SPEC_REQUIRED` | PRD에는 있으나 Spec에 없는 요구가 있음 | Spec 보강 후 진행 |
| `DECISION_REQUIRED` | 권한/정책/상태 전이 판단이 필요함 | 사용자 확인 |

## 출력 형식

```markdown
# Intake 결과

## 작업 판정
- 유형: [신규 기능/기존 기능 수정/버그/E2E 검증/문서화]
- 규모: [소/중/대]
- 영향 범위: [backend/frontend/fullstack/e2e/docs]
- 기준 신뢰도: [높음/중간/낮음]

## 기준 필요 여부
| 기준 | 판정 | 근거 |
|------|------|------|
| Spec | 필요/불필요/보강 필요 | ... |
| DB | 필요/불필요/결정 필요 | ... |
| UI Proto | 필수/권장/생략 가능 | ... |
| E2E | 필요/선택/불필요 | ... |

## 권장 실행 경로
1. [후속 스킬 또는 직접 수정]
2. [...]

## 차단 항목
| 분류 | 내용 | 필요한 결정 |
|------|------|-------------|
| DECISION_REQUIRED | ... | ... |

## Intake 판단 근거
- ...

## 사후 피드백 포인트
- 실제 개발 중 이 판정이 맞았는가
- 누락된 기준은 무엇인가
- 다음 intake에서 추가로 확인해야 할 질문은 무엇인가
```

## 후속 스킬 매핑

| 상황 | 다음 스킬 |
|------|-----------|
| 요구사항 정제 필요 | `peach-gen-spec` |
| DB schema/migration 필요 | `peach-gen-db` |
| 기획 검토용 Mock 화면 필요 | `peach-team-ui-proto` |
| 본 개발 필요 | `peach-team-dev` |
| 최종 흐름 검증 필요 | `peach-team-e2e` |
| 작은 단일 기능 | `peach-team-3a` |
| 기존 기능 분석 필요 | `peach-doc-feature` |
| 단독 DB 확인 필요 | `peach-db-query` |

## 완료 기준

- 작업 규모와 유형을 판정했다.
- Spec/DB/ui-proto/E2E 필요 여부를 근거와 함께 밝혔다.
- 구현 전에 막히는 기준을 `*_REQUIRED`로 분리했다.
- 다음 실행 스킬과 순서를 제안했다.
- 코드, DB, proto, E2E 산출물을 직접 생성하지 않았다.
