---
name: build-fix
description: "빌드 에러 수정해줘, 타입 에러 고쳐줘, tsc 실패 수정 요청 시 사용. 점진적 빌드 에러 수정. 리팩토링은 별도 단계로 분리."
allowed-tools: Bash, Read, Edit
---

# Build and Fix

Incrementally fix build/type errors — any stack (tsc, gradle/javac, mypy, cargo 등). 예시는 TS 기준.

## Use Cases

**1. 빌드 에러 수정**
- Input: "/build-fix"
- Action: npm run build → 에러 파싱 → 파일별 그룹핑 → 순차 수정 → 재빌드 검증
- Output: 수정 요약 (N개 해결, M개 잔존)

**2. 특정 에러만 수정**
- Input: "/build-fix TS2322"
- Action: 해당 에러 코드만 필터링 → 집중 수정
- Output: 타겟 에러 해결 + 새 에러 여부 확인

**3. CI 빌드 실패 복구**
- Input: "/build-fix" (CI 에러 로그 첨부)
- Action: 에러 로그 분석 → 로컬 재현 → 수정 → 빌드 성공 확인
- Output: CI 통과 가능한 상태로 복구


## Workflow

1. Run the project's build/type-check command (npm run build, ./gradlew compileJava, mypy, cargo check 등 — 프로젝트 CLAUDE.md 우선)

2. Parse error output:
   - Group by file
   - Sort by severity

3. For each error:
   - Show error context (5 lines before/after)
   - Explain the issue
   - Propose fix
   - Apply fix
   - Re-run build
   - Verify error resolved

4. Stop if:
   - Fix introduces new errors
   - 재빌드 후 동일 에러 코드가 잔존하거나 3회 연속 같은 에러가 반복됨

   - User requests pause

5. Show summary:
   - Errors fixed
   - Errors remaining
   - New errors introduced

원칙:
- 한 번에 하나의 에러만 수정한다. 여러 파일을 동시에 손대면 어떤 변경이 어떤 에러를 해결했는지 추적이 어려워진다.
- 에러와 무관한 코드는 손대지 않는다. 리팩토링은 별도 단계에서 수행.

## Done When

- 빌드가 성공하거나, 잔존 에러가 보고됨
- 수정/잔존/신규 에러 수가 요약됨
- 에러: 같은 에러 3회 반복 시 사용자에게 알림 후 중단

## Composability

- 빌드 성공 후 데드코드 정리는 별도 단계
- 에러 수정 완료 후 커밋 전 리뷰: code-reviewer 플러그인
