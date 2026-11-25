---
name: cross-repo-impact
description: 한 repo의 변경이 다른 repo에 미치는 영향을 분석하고, 업데이트 체크리스트를 제공
user_invocable: true
---

# Cross-Repo Impact Analysis

변경사항의 영향 범위를 분석하고 필요한 후속 작업을 안내합니다.

## Dependency Graph

```
aerospike-py (standalone)
  ↓ 사용
aerospike-ce-kubernetes-operator (ACKO)
  ↓ submodule 포함, API 연동
aerospike-cluster-manager
  ↓ API/CRD를 skill 콘텐츠로 참조
aerospike-ce-ecosystem-plugins
```

## 분석 절차

### Step 1: 변경 대상 식별

변경이 발생한 repo와 변경 유형을 파악:

- **Public API 변경**: 함수 시그니처, 반환 타입, 예외 클래스, 상수
- **CRD/Spec 변경**: AerospikeCluster CR 필드 추가/삭제/변경
- **설정 변경**: 포트, 환경변수, 설정 파라미터
- **내부 리팩토링**: 외부 인터페이스 불변 → 영향 없음

내부 리팩토링이면 "cross-repo 영향 없음"으로 분석 종료.

### Step 2: 영향 범위 체크리스트

변경 repo에 따라 해당 체크리스트를 실행:

#### aerospike-py 변경 시

```
□ cluster-manager backend에서 해당 API 사용 여부
  → grep -r "<변경된 함수/클래스>" aerospike-cluster-manager/backend/
□ plugins skill 업데이트 필요 여부
  → aerospike-ce-ecosystem-plugins/skills/aerospike-py-api/
  → aerospike-ce-ecosystem-plugins/skills/aerospike-py-fastapi/
□ 반환 타입 변경 시 cluster-manager의 응답 파싱 코드 확인
□ 새 예외 클래스 추가 시 cluster-manager의 에러 핸들링 확인
□ 새 정책(Policy) 상수 추가 시 skill reference 업데이트
```

#### ACKO 변경 시

```
□ CRD 필드 변경 시 cluster-manager K8s 관리 UI 확인
  → grep -r "<변경된 필드>" aerospike-cluster-manager/
□ plugins skill 업데이트 필요 여부
  → aerospike-ce-ecosystem-plugins/skills/acko-deploy/
  → aerospike-ce-ecosystem-plugins/skills/acko-operations/
  → aerospike-ce-ecosystem-plugins/skills/acko-config-reference/
□ Webhook 검증 규칙 변경 시 config-reference 업데이트
□ Helm chart values 변경 시 deploy skill 예제 YAML 업데이트
□ 이벤트 추가/변경 시 operations skill의 이벤트 목록 업데이트
□ ACKO 내부 cluster-manager submodule 포인터 갱신 필요 여부
```

#### cluster-manager 변경 시

```
□ ACKO 내부 submodule 포인터 갱신 필요 여부
  → aerospike-ce-kubernetes-operator/.gitmodules 확인
□ Backend API 엔드포인트 변경 시 영향은 cluster-manager 내부에 한정 (cross-repo 영향 낮음)
```

#### plugins 변경 시

```
□ Skill 내용이 실제 repo의 현재 API/CRD와 일치하는지 검증
  → 변경 대상 skill이 참조하는 repo의 최신 코드 확인
□ cross-repo 영향 없음 (plugins는 의존 그래프 최하위)
```

### Step 3: 병합 순서 확인

cross-repo 변경이 필요한 경우, 반드시 이 순서로 병합:

```
1. aerospike-py (먼저)
2. ACKO
3. cluster-manager
4. plugins (마지막)
```

하위 repo의 PR이 상위 repo 변경에 의존하면, 상위 repo PR이 먼저 머지되어야 합니다.

### Step 4: 결과 보고

```
## Cross-Repo Impact 분석 결과

**변경 repo**: <repo 이름>
**변경 유형**: <Public API / CRD / 설정 / 내부 리팩토링>

### 영향받는 repo
- [ ] <repo>: <구체적 영향 내용>
- [ ] <repo>: <구체적 영향 내용>

### 필요한 후속 작업
1. <작업 내용> (repo: <대상>)
2. <작업 내용> (repo: <대상>)

### 병합 순서
<순서 안내>
```
