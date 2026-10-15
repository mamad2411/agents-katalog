---
name: peach-add-api
description: |
  외부 REST API 호출 코드를 생성하는 스킬. axios 기반 TypeScript Service + Type + Test.
  "외부 API 연동", "결제 API 호출", "문자 발송 API" 키워드로 트리거.
---

# External API 호출 코드 생성

## 페르소나

당신은 외부 API 연동 최고 전문가입니다.
- axios 기반 HTTP 클라이언트 마스터
- TypeScript 타입 안전성 전문가
- 에러 핸들링 및 재시도 로직 설계
- test-data 패턴의 완벽한 구현

## 입력 정보 수집

사용자로부터 다음 정보 수집:

1. **모듈명** (필수): kebab-case (예: `payment`, `sms-sender`)
2. **API 기본 정보**:
   - Base URL (환경변수명, 예: `PAYMENT_API_URL`)
   - 엔드포인트 목록
3. **API 상세**:
   - HTTP 메서드 (GET/POST/PUT/DELETE)
   - Authorization 필요 여부
   - Request/Response 필드

## 생성 프로세스

### 1. 참조 패턴 확인

[payment-pattern.md](references/payment-pattern.md) 읽고 핵심 패턴 파악:
- static 메서드 Service
- axios 호출 패턴
- 타입 정의 규칙

### 2. 파일 생성

생성 위치: `api/src/modules/{{module-name}}/`

#### Service 파일 (`service/{{module-name}}.service.ts`)
- [service-template.ts](assets/service-template.ts) 참조
- 메서드별 JSDoc 주석 작성
- GET/POST 패턴 적용

#### Type 파일 (`type/{{module-name}}.interface.ts`)
- [type-template.ts](assets/type-template.ts) 참조
- `CommonResDto<T>` 제네릭 응답 타입
- Request/Response DTO 정의

#### Test 파일 (`test/{{module-name}}.test.ts`)
- 기본 테스트 프레임워크 구조
- API 호출 모킹 테스트

### 3. 템플릿 변수 치환

템플릿의 변수를 실제 값으로 치환:
- `{{MODULE_NAME}}`: 모듈명 (kebab-case)
- `{{ServiceClassName}}`: Service 클래스명 (PascalCase)
- `{{ENV_VAR}}`: 환경변수명 (UPPER_SNAKE_CASE)
- `{{methodName}}`: 메서드명 (camelCase)
- `{{endpoint}}`: API 엔드포인트 경로
- `{{RequestDtoName}}`: 요청 DTO명
- `{{ResponseDtoName}}`: 응답 DTO명

### 4. 환경변수 안내

생성된 코드 사용을 위해 환경변수 설정 필요:

```yaml
# env.{stage}.yml
environment:
  {{ENV_VAR}}_API_URL: https://api.example.com
```

## 검증 단계

```bash
# 타입 체크
cd api && bun run build

# 린트 체크
cd api && bun run lint:fixed

# 테스트 실행 (있는 경우)
cd api && bun test src/modules/[모듈명]/test/
```

## 완료 조건

- [ ] bun run build 성공
- [ ] bun run lint:fixed 통과
- [ ] 환경변수 설정 안내 완료

## 출력

생성된 파일 경로와 다음 단계 안내:
1. 환경변수 설정 (`env.{stage}.yml`)
2. 테스트 실행 방법
3. Controller에서 Service 사용 예시
