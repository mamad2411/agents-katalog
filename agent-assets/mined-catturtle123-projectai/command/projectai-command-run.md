---
description: Run the Spring Boot server locally
---

# Run Server

Spring Boot 서버를 로컬에서 실행합니다.

## Usage

```bash
./gradlew bootRun
```

## Options

- 특정 프로필로 실행: `./gradlew bootRun --args='--spring.profiles.active=dev'`
- 디버그 로그: `./gradlew bootRun --args='--logging.level.root=DEBUG'`
