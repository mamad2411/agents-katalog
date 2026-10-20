---
description: 포맷팅 → 린트 → 빌드 실행
---

# /build - Kotlin 빌드 명령어

프로젝트를 빌드하고 결과를 보고합니다.

## 실행 단계

1. `./gradlew ktlintFormat` - 포맷팅 적용
2. `./gradlew ktlintCheck` - 린트 검사
3. `./gradlew build -x test` - 빌드 실행

## 실패 시

- 포맷팅 오류: 자동 수정 후 재시도
- Ktlint 경고: 문제 파일과 수정 방법 제시
- 빌드 에러: 에러 메시지 분석 및 해결책 제안
