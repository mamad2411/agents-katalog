---
description: 통합 테스트(E2E) 실행
---

# /e2e-test - E2E 테스트 실행 명령어

통합 테스트(E2E)를 실행합니다.

## 실행 단계

1. PostgreSQL 연결 확인
2. `./gradlew test --tests "*IntegrationTest*"` - 통합 테스트 실행
3. 결과 분석 및 보고

## 사전 조건

- PostgreSQL이 실행 중이어야 합니다
- `application-test.yml`에 테스트 DB 설정이 필요합니다

## 사용 예시

```
/e2e-test               # 모든 통합 테스트
/e2e-test [도메인명]    # 특정 도메인 통합 테스트
```
