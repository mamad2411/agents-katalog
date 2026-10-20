---
description: 테스트 실행 및 결과 분석
---

# /test - 테스트 실행 명령어

테스트를 실행하고 결과를 분석합니다.

## 실행 단계

1. `./gradlew test` - 모든 테스트 실행
2. 실패한 테스트 분석
3. 필요시 수정 제안

## 옵션

- `/test` - 모든 테스트 실행
- `/test [className]` - 특정 테스트 클래스만 실행
- `/test [className.methodName]` - 특정 테스트 메서드만 실행

## 실패 시 행동

1. 실패한 테스트 식별
2. 관련 코드 분석
3. TDD 원칙에 따라 수정안 제시
4. 사용자 승인 후 수정

## 출력 형식

```
테스트 결과: X passed, Y failed
실패한 테스트:
- TestClassName.testMethodName: 실패 원인
```
