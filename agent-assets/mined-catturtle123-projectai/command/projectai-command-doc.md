---
description: Generate and open API documentation (Swagger)
---

# Documentation

Swagger UI를 통해 API 문서를 확인합니다.

## Usage

```bash
./gradlew bootRun
# 브라우저에서 http://localhost:8080/swagger-ui.html 접속
```

## Details

- SpringDoc OpenAPI를 통한 자동 API 문서 생성
- Swagger UI에서 실시간 API 테스트 가능
- DTO의 `@Schema` 어노테이션으로 문서화
