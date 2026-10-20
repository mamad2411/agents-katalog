---
name: test-coverage-check
description: |
  변경된 Java/Kotlin 소스 파일의 테스트 커버리지를 자동 분석하고, 누락된 테스트를 생성하는 2단계 파이프라인.
  review-test-coverage 에이전트로 커버리지 갭을 식별한 뒤, test-generator 에이전트로 누락 테스트를 자동 생성한다.
  "테스트 커버리지 체크", "커버리지 점검", "테스트 점검", "테스트 빠진거 없나", "누락 테스트 확인" 요청 시 트리거.
  작업 완료 후 테스트가 충분한지 확인하고 싶을 때, 코드 리뷰 전 테스트 상태를 점검하고 싶을 때,
  또는 "방금 수정한 코드 테스트 있어?", "테스트 부족한거 채워줘" 같은 맥락에서도 이 스킬을 사용하라.
paths:
  - "**/src/test/**"
  - "**/*Test.java"
  - "**/*Spec.kt"
  - "**/*Tests.java"
---

# Test Coverage Check

작업 완료 후 변경된 코드에 테스트가 충분한지 자동으로 점검하고, 부족하면 생성까지 해주는 스킬이다.
코드를 작성한 뒤 "테스트 빠진 거 없나?" 하고 확인하는 과정을 자동화한 것이라고 생각하면 된다.

## 왜 이 스킬이 필요한가

테스트 없이 커밋하면 회귀 버그를 잡을 수 없고, 수동으로 커버리지를 확인하려면 파일을 하나하나 뒤져봐야 한다.
이 스킬은 git diff로 변경 파일을 자동 식별하고, 전문 에이전트에게 분석과 생성을 위임해서 이 과정을 자동화한다.

---

## 워크플로우 개요

```
Step 1: git diff로 변경된 Java/Kotlin 소스 파일 식별
    ↓
Step 2: [review-test-coverage 에이전트] 커버리지 분석 → 누락 목록 도출
    ↓ (누락 있을 때만)
Step 3: [test-generator 에이전트] 누락 테스트 자동 생성
    ↓
Step 4: 결과 통합 보고
```

---

## Step 1: 변경 파일 식별

변경된 Java/Kotlin 소스 파일을 식별한다. 테스트 파일 자체는 분석 대상에서 제외한다 — 관심사는 "프로덕션 코드에 테스트가 있는가"이기 때문이다.

```bash
# staged 변경
git diff --cached --name-only -- '*.java' '*.kt' | grep -v 'src/test/'
# unstaged 변경
git diff --name-only -- '*.java' '*.kt' | grep -v 'src/test/'
# 새로 추가된 untracked 파일
git ls-files --others --exclude-standard -- '*.java' '*.kt' | grep -v 'src/test/'
```

변경된 소스 파일이 없으면 "변경된 Java/Kotlin 소스 파일이 없습니다"로 종료한다.

---

## Step 2: 커버리지 분석

`review-test-coverage` 에이전트를 **foreground**로 디스패치한다. 결과가 다음 단계의 입력이 되므로 반드시 완료를 기다린다.

에이전트 프롬프트와 우선순위 기준은 `references/agent-prompts.md`를 참조하라.

핵심 분석 항목:
- 각 소스 파일에 대응하는 테스트 파일 존재 여부
- 주요 public 메서드별 테스트 존재 여부
- 누락된 테스트 시나리오 (경계값, 예외, 정상 케이스)
- 우선순위 판정: Critical > High > Medium > Low

누락 테스트가 없으면 "모든 변경 파일의 테스트 커버리지가 충분합니다"로 종료한다.

---

## Step 3: 테스트 생성

누락 테스트가 있을 때만 `test-generator` 에이전트를 **foreground**로 디스패치한다.
Critical/High 우선순위만 생성하는 이유는, Low 우선순위(getter, 단순 위임)까지 생성하면 유지보수 부담만 늘기 때문이다.

에이전트 프롬프트 상세는 `references/agent-prompts.md`를 참조하라.

생성 원칙:
- Critical/High 우선순위 테스트만 생성
- 기존 테스트 파일이 있으면 해당 파일에 추가, 없으면 새로 생성
- 프로젝트의 기존 테스트 컨벤션을 따름 (JUnit5, AssertJ, Mockito 등)
- 생성 후 `git add`로 staging (commit은 하지 않음)

---

## Step 4: 결과 보고

분석과 생성 결과를 통합하여 아래 형식으로 보고한다:

```markdown
## 테스트 커버리지 체크 결과

### 분석 대상
- 변경 파일: {N}개
- 분석 일시: {날짜}

### 커버리지 현황

| 소스 파일 | 테스트 파일 | 기존 상태 | 조치 | 추가된 테스트 |
|-----------|------------|----------|------|-------------|

### 요약
- 분석 파일: {N}개
- 테스트 충분: {N}개
- 테스트 생성: {N}개
- 생성 건너뜀 (Low 우선순위): {N}개
```

---

## 엣지 케이스

- **테스트 프레임워크 미설정**: build.gradle/pom.xml에 JUnit 의존성이 없으면 분석만 수행하고 생성은 건너뜀
- **변경 파일이 DTO/Config만**: 단순 DTO나 설정 클래스만 변경된 경우 Low 우선순위로 분류, 생성 건너뜀
- **기존 테스트 수정 시**: 기존 테스트가 깨지지 않도록 주의 — 새 테스트 메서드만 추가

---

## 참조 문서

- [references/agent-prompts.md](references/agent-prompts.md): 에이전트 프롬프트 템플릿 및 우선순위 판정 기준
