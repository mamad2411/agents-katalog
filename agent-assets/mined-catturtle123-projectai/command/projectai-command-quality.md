---
description: 전체 코드 품질 검사 (포맷팅, 컴파일, 테스트, 빌드)
---

# /quality - 코드 품질 검사 명령어

전체 코드 품질을 점검합니다.

## 검사 항목

1. **포맷팅** - `./gradlew ktlintCheck`
2. **컴파일** - `./gradlew compileKotlin`
3. **테스트** - `./gradlew test`
4. **빌드** - `./gradlew build`

## 결과 보고

```
품질 검사 결과:
[ ] 포맷팅: PASS/FAIL
[x] 컴파일: PASS/FAIL
[x] 테스트: PASS/FAIL (N/M 통과)
[ ] 빌드: PASS/FAIL
```

## 자동 수정

- 포맷팅 문제: 자동 수정 (`./gradlew ktlintFormat`)
- 컴파일 에러: 에러 메시지 분석 및 수정 제안
- 테스트 실패: TDD 원칙에 따라 분석

## 커밋 전 필수 실행

이 명령어는 커밋 전에 실행하여 모든 품질 기준을 만족하는지 확인합니다.
