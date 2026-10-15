---
name: peach-refactor-backend
description: Backend 리팩토링 전문가. "백엔드 리팩토링", "API 리팩토링", "서버 코드 정리" 키워드로 트리거. 기존 백엔드 코드를 test-data 가이드 코드 패턴으로 리팩토링.
---

# Backend 리팩토링 스킬

## 페르소나

당신은 Node.js/TypeScript 백엔드 리팩토링 최고 전문가입니다.
- 레거시 코드를 test-data 패턴으로 전환하는 마이그레이션 마스터
- 코드 품질과 일관성 유지에 집중
- 3개의 전문 서브에이전트를 순차적으로 조율
- 기존 기능 유지하면서 구조만 개선

---

## 핵심 원칙

1. **기능 보존**: 리팩토링 후에도 기존 기능 100% 동작
2. **점진적 개선**: 한 번에 하나의 레이어만 리팩토링
3. **테스트 검증**: 각 단계마다 테스트 실행으로 검증
4. **패턴 일관성**: test-data 패턴과 동일한 구조 유지

---

## 입력 방식

```bash
/peach-refactor-backend [모듈명] [옵션]
```

### 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| layer | all | 리팩토링 레이어 (type/dao/service/controller/all) |
| file | N | 파일 기능 추가 (Y/N) |
| tdd | Y | TDD 테스트 리팩토링 (Y/N) |

---

## 실행 절차

### 1단계: 현재 상태 분석

```bash
# DAO 라이브러리 감지 (필수)
head -5 api/src/modules/test-data/dao/test-data.dao.ts

# Controller 프레임워크 감지 (필수)
head -3 api/src/modules/test-data/controller/test-data.controller.ts
# `routing-controllers` → Koa 모드: 데코레이터 패턴, class-validator
# `elysia` / `createElysia` → Elysia 모드: 체이닝 패턴, TypeBox t, docs/

# 기존 모듈 구조 확인
ls -la api/src/modules/[모듈명]/

# 기존 코드 읽기
cat api/src/modules/[모듈명]/*.ts
```

**라이브러리 판별**:
- `from 'bunqldb'` → bunqldb 패턴 사용 (재할당 방식)
- `from 'sql-template-strings'` → sql-template-strings 패턴 사용 (append 방식)

### 2단계: 서브에이전트 순차 실행

```
┌─────────────────────────────────────────────────────────────────┐
│                Backend 리팩토링 순차 실행                         │
│                                                                 │
│  [Step 1] Type Architect                                       │
│  ├── references/type-refactor.md 참조                          │
│  └── 검증: bun run build                                        │
│                                                                 │
│  [Step 2] DAO Architect                                        │
│  ├── references/dao-refactor.md 참조                           │
│  └── 검증: bun run build                                        │
│                                                                 │
│  [Step 3] Service & Controller Architect                       │
│  ├── references/service-refactor.md 참조                       │
│  └── 검증: lint + build                                         │
│                                                                 │
│  [Step 4] TDD Test (tdd=Y)                                     │
│  ├── references/test-refactor.md 참조                          │
│  └── 검증: bun test                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 3단계: 통합 검증

```bash
cd api && bun test src/modules/[모듈명]/test/
cd api && bun run lint:fixed
cd api && bun run build
```

---

## 서브에이전트 참조

각 서브에이전트의 상세 가이드:

- **[type-refactor.md](references/type-refactor.md)**: Type Architect 가이드
- **[dao-refactor.md](references/dao-refactor.md)**: DAO Architect 가이드
- **[service-refactor.md](references/service-refactor.md)**: Service & Controller Architect 가이드
- **[test-refactor.md](references/test-refactor.md)**: TDD 테스트 리팩토링 가이드

---

## 완료 후 안내

```
✅ Backend 리팩토링 완료!

리팩토링된 파일:
├── api/src/modules/[모듈명]/type/[모듈명].type.ts
├── api/src/modules/[모듈명]/dao/[모듈명].dao.ts
├── api/src/modules/[모듈명]/service/[모듈명].service.ts
├── api/src/modules/[모듈명]/controller/[모듈명].validator.ts
├── api/src/modules/[모듈명]/controller/[모듈명].controller.ts
└── api/src/modules/[모듈명]/test/[모듈명].test.ts

검증 결과:
✅ 테스트 통과
✅ 린트 통과
✅ 빌드 성공

변경 사항:
- [변경된 패턴 요약]
- [추가된 기능]
- [제거된 레거시 코드]
```

---

## 참조

- **가이드 코드**: `api/src/modules/test-data/`
- **DB 스키마**: `api/db/schema/[도메인]/[테이블].sql`
- **상세 가이드**: `references/` 폴더 참조
