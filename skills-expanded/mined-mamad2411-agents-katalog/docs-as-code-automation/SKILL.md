---
name: docs-as-code-automation
category: dx
description: "Docs as Code 자동화 가이드 — API 문서 자동화 (OpenAPI), 문서 품질 측정, Vale 린터 Use when working with dx 도메인의 패턴 / 구현 선택."
effort: low
deprecated: false
---

# Docs as Code 자동화 가이드

API 문서 자동화 (OpenAPI), 문서 품질 측정, Vale 린터

---

## API 문서 자동화

### OpenAPI Generator

```bash
# OpenAPI 스펙에서 문서 생성
npm install -g @openapitools/openapi-generator-cli

openapi-generator-cli generate \
  -i api/openapi.yaml \
  -g html2 \
  -o docs/api

# 또는 Redoc 사용
npm install -g redoc-cli
redoc-cli build api/openapi.yaml -o docs/api/index.html
```

### OpenAPI 스펙 예시

```yaml
# api/openapi.yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
  description: |
    # 개요
    이 API는 사용자 관리 기능을 제공합니다.

    ## 인증
    모든 요청에 Bearer 토큰이 필요합니다.

servers:
  - url: https://api.example.com/v1
    description: Production

paths:
  /users:
    get:
      summary: 사용자 목록 조회
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
          description: 최대 반환 개수
      responses:
        '200':
          description: 성공
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
              example:
                - id: 1
                  name: "홍길동"
                  email: "hong@example.com"

components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: integer
          description: 사용자 ID
        name:
          type: string
          description: 사용자 이름
        email:
          type: string
          format: email
          description: 이메일 주소

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### Swagger UI Kubernetes 배포

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: swagger-ui
spec:
  replicas: 1
  selector:
    matchLabels:
      app: swagger-ui
  template:
    metadata:
      labels:
        app: swagger-ui
    spec:
      containers:
        - name: swagger-ui
          image: swaggerapi/swagger-ui:latest
          ports:
            - containerPort: 8080
          env:
            - name: SWAGGER_JSON_URL
              value: "/api/openapi.yaml"
          volumeMounts:
            - name: spec
              mountPath: /api
      volumes:
        - name: spec
          configMap:
            name: openapi-spec
```

---

## 문서 품질 측정

### Vale (문서 린터)

```yaml
# .vale.ini
StylesPath = .vale/styles

MinAlertLevel = suggestion

Packages = Microsoft, write-good

[*.md]
BasedOnStyles = Vale, Microsoft, write-good
```

```bash
# 설치 및 실행
brew install vale
vale docs/
```

### 문서 커버리지

```python
# scripts/doc_coverage.py
import os
import yaml

def check_coverage():
    """API 엔드포인트 문서화 비율 확인"""
    # OpenAPI 스펙 로드
    with open('api/openapi.yaml') as f:
        spec = yaml.safe_load(f)

    total = 0
    documented = 0

    for path, methods in spec['paths'].items():
        for method, details in methods.items():
            if method in ['get', 'post', 'put', 'delete', 'patch']:
                total += 1
                if details.get('description') or details.get('summary'):
                    documented += 1

    coverage = (documented / total * 100) if total > 0 else 0
    print(f"API Documentation Coverage: {coverage:.1f}%")
    print(f"  Documented: {documented}/{total}")

    return coverage >= 80  # 80% 이상 필수

if __name__ == "__main__":
    import sys
    sys.exit(0 if check_coverage() else 1)
```

---

## Sources

- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [Docusaurus](https://docusaurus.io/)
- [Backstage TechDocs](https://backstage.io/docs/features/techdocs/)
- [Docs as Code](https://konghq.com/blog/learning-center/what-is-docs-as-code)
- [Technical Documentation Tools 2026](https://affine.pro/blog/best-technical-documentation-software-tools-for-developers)
- [Vale](https://vale.sh/)

## 참조 스킬

- `/docs-as-code` - Docs as Code 핵심 도구 (MkDocs, Docusaurus, Backstage TechDocs)
- `/backstage` - Backstage 플랫폼
- `/api-design` - API 설계
