---
name: sync-tech-stack
description: >
  Use this skill when the user says "sync tech stack", "detect stack",
  "update stack", "refresh stack", "스택 감지", "기술 스택 업데이트",
  or when another skill needs a shared project stack file.
  Detects project tech stacks and frameworks, writes `.agents/tech-stack.md`,
  and updates it when the stack changes.
---

# Sync Tech Stack

## Invocation

```
/sync-tech-stack
```

인수가 없어도 된다. 실행할 때마다 현재 프로젝트를 다시 확인해 `.agents/tech-stack.md`를 생성 또는 갱신한다.

---

## Step 1: 기존 파일 확인

프로젝트 루트의 `.agents/tech-stack.md` 존재 여부를 확인한다.

- 파일이 있으면 현재 내용을 읽어 기존 요약과 `## Manual Notes` 섹션을 확인한다
- 파일이 없으면 새로 생성할 준비를 한다

이 파일은 다른 스킬이 기술 스택을 참조하는 **단일 진실 공급원(source of truth)** 이다.

---

## Step 2: 프로젝트 스택 재탐지

프로젝트 루트와 필요한 서브 디렉토리를 탐색해 현재 기술 스택을 다시 감지한다.

- 감지 규칙은 `references/tech-stack-detection.md`를 따른다
- 모노레포인 경우 스택 영역별로 따로 기록한다
- 각 영역마다 다음 정보를 수집한다:
  - 영역 이름
  - 루트 경로
  - 주요 스택
  - 언어
  - 빌드/패키지 도구
  - 단위 테스트 프레임워크
  - E2E 프레임워크
  - 감지 근거 신호
  - 주요 소스/테스트 디렉토리

### 모호한 경우

감지 결과가 충돌하거나 불확실하면 바로 질문한다:

```
감지된 스택 후보:
- [후보 A]
- [후보 B]

어떤 스택/영역을 기준으로 작업할까요?
```

PAUSE. 확인 후 계속한다.

### 감지되지 않는 경우

아무 스택도 감지되지 않으면 질문한다:

```
프로젝트 스택을 감지할 수 없습니다.
다음 중 하나를 알려주세요:
- typescript-react
- kotlin-spring
- java-spring
- python-fastapi
- 기타 (직접 설명)
```

PAUSE. 확인 후 계속한다.

---

## Step 3: `.agents/tech-stack.md` 작성 또는 갱신

수집한 결과를 `.agents/tech-stack.md`에 저장한다.

- 파일 형식은 `references/tech-stack-file-format.md`를 따른다
- 기존 파일이 있으면 감지 결과를 기준으로 내용을 갱신한다
- 기존 `## Manual Notes` 섹션이 있으면 유지한다
- 날짜 메타데이터(`생성`, `마지막 업데이트`)를 갱신한다

이 파일은 **간결하게 유지**한다. 장황한 설명보다 다른 스킬이 바로 사용할 수 있는 구조화된 요약을 우선한다.

---

## Step 4: 결과 표시

완료 후 다음 형식으로 짧게 표시한다:

```markdown
✅ 기술 스택 동기화 완료 → `.agents/tech-stack.md`

감지된 영역:
- [영역명] [스택] ([경로])
- [영역명] [스택] ([경로])

변경 사항:
- [새로 추가된 스택 또는 프레임워크]
- [업데이트된 항목]
```

변경 사항이 없으면:

```markdown
✅ `.agents/tech-stack.md`가 이미 최신입니다.
```

---

## 다른 스킬과의 연결 규칙

- `tdd-plan`은 Step 2에서 이 스킬을 호출해 `.agents/tech-stack.md`를 최신 상태로 만든 뒤 그 파일을 읽는다
- `tdd-task`는 세션 시작 시 `.agents/tech-stack.md`를 우선 로드하고, 파일이 없거나 개발자가 `update stack`을 요청하면 이 스킬을 호출한다
- 기술 스택이 바뀌는 작업(새 빌드 파일, 새 프레임워크 도입, 모듈 추가)이 있은 뒤에는 이 스킬을 다시 실행한다

---

## 참조 파일

| 파일 | 사용 시점 |
|------|---------|
| `.agents/skills/sync-tech-stack/references/tech-stack-detection.md` | Step 2 재탐지 시 |
| `.agents/skills/sync-tech-stack/references/tech-stack-file-format.md` | Step 3 파일 작성/갱신 시 |
