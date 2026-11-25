---
name: pencil-update
description: |
  Pencil MCP로 .pen 파일의 기존 화면을 수정합니다. 속성 변경, 노드 교체/삽입/삭제/이동/복사, 이미지 생성 등 모든 수정 작업을 안내합니다.
  "디자인 수정", "화면 변경", "레이아웃 조정", "Pencil 수정", "노드 업데이트" 요청에 트리거됩니다.
  기존 .pen 화면의 텍스트, 색상, 레이아웃, 컴포넌트를 변경하고 싶다면 이 스킬을 사용하세요. 새 화면 생성은 pencil-screen을 사용합니다.
---

# Pencil 디자인 수정

## 개요

Pencil MCP 도구를 사용하여 .pen 파일의 기존 화면을 수정한다.
수정 전 반드시 스크린샷으로 현재 상태를 확인하고, 수정 후 결과를 검증한다.

## 왜 이 워크플로우인가?

Pencil 노드를 직접 수정하면 의도하지 않은 레이아웃 변경이 발생할 수 있습니다.
수정 전 스크린샷으로 현재 상태를 확인하고, placeholder 모드에서 작업한 뒤, 수정 후 스크린샷으로 결과를 검증하는 3단계 안전장치가 필요합니다.
특히 Copy(C) 후 자식 노드 ID가 새로 생성되므로, batch_get으로 구조를 먼저 파악해야 합니다.

## 사용법

### Step 1: 에디터 상태 확인

```
get_editor_state(include_schema: false)
```

### Step 2: 대상 노드 파악

```
batch_get(nodeIds: [대상_노드_ID], readDepth: 2-3)
```

- 수정할 노드와 자식 구조를 파악
- descendants override에 필요한 ID 경로 확인

### Step 3: 현재 상태 스크린샷

```
get_screenshot(nodeId: 대상_프레임_ID)
```

- 수정 전 상태를 반드시 확인

### Step 4: placeholder 설정

```
batch_design([
  U(대상_프레임_ID, {placeholder: true})
])
```

### Step 5: 수정 실행

| 목적 | Operation | 예시 |
|------|-----------|------|
| 속성 변경 | `U(id, {...})` | `U("abc", {content: "새 텍스트"})` |
| 노드 교체 | `R(id, {...})` | `R("abc", {type: "text", ...})` |
| 노드 삽입 | `I(parent, {...})` | `I("abc", {type: "frame", ...})` |
| 노드 삭제 | `D(id)` | `D("abc")` |
| 노드 이동 | `M(id, parent, idx)` | `M("abc", "def", 2)` |
| 노드 복사 | `C(id, parent, {...})` | `C("abc", "def", {...})` |
| 이미지 생성 | `G(id, "ai", "설명")` | `G("abc", "ai", "ocean sunset")` |

### Step 6: 결과 검증

```
batch_design([
  U(대상_프레임_ID, {placeholder: false})
])
get_screenshot(nodeId: 대상_프레임_ID)
```

## 입출력

| 입력 | 출력 |
|------|------|
| 수정 대상 노드 ID 또는 프레임 이름 | 수정된 .pen 파일 |
| 변경 요구사항 | 수정 전후 스크린샷 |

## 화면 ID 매핑

프로젝트별 화면 ID와 주요 노드 정보는 Read 도구로 `references/screen-ids.md`를 읽어서 참조하세요.

## 핵심 규칙

- **수정 전 스크린샷 필수** - 현재 상태 파악
- **placeholder 설정 후 작업** - 편집 모드 진입
- **Copy 후 Update 주의** - C()로 복사한 노드의 자식 ID는 새로 생성됨
- **descendants 접근** - 인스턴스 내부 수정은 `U(instance+"/childId", {...})`
- **최대 25 ops/call** - 대규모 수정은 분할
- **Desktop + Mobile 동시 수정** - 한 화면 수정 시 쌍 화면도 확인

## 체크리스트

- [ ] 수정 전 스크린샷 확인
- [ ] batch_get으로 노드 구조 파악
- [ ] placeholder 설정
- [ ] 수정 ops 실행
- [ ] placeholder 해제
- [ ] 수정 후 스크린샷 검증
- [ ] Desktop/Mobile 쌍 일관성 확인

## 관련 스킬

- `pencil-screen`: 새 화면 생성
- `pencil-to-code`: 디자인을 코드로 변환
