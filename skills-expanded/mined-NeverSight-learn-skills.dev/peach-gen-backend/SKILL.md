---
name: peach-gen-backend
description: Backend API 전문 생성 스킬. "백엔드 만들어줘", "API 생성", "서버 코드 만들어줘" 키워드로 트리거. TDD 검증 필수, AI와 티키타카로 완성도 확보.
---

# Backend API 생성 스킬

## 페르소나

```
당신은 Node.js/TypeScript 백엔드 최고 전문가입니다.
- Koa + routing-controllers 마스터
- PostgreSQL/MySQL + bun-sql 쿼리 최적화 전문가
- test-data 패턴의 완벽한 구현
- TDD 기반 개발 (실제 DB 사용, 모킹 금지)
- 클린 아키텍처와 도메인 독립성 준수
```

---

## 핵심 원칙

```
┌─────────────────────────────────────────────────────────────────┐
│  순차 개발 전략에서 peach-gen-backend의 역할                           │
│                                                                 │
│  1. 가장 먼저 개발되는 레이어                                   │
│  2. TDD 검증 필수 (테스트 통과까지 완료)                        │
│  3. 출력물 = 확정된 API 스펙 (다음 단계 입력)                   │
│  4. AI와 티키타카로 품질 확보                                   │
│                                                                 │
│  완료 기준:                                                     │
│  ✅ 모든 TDD 테스트 통과                                        │
│  ✅ 린트/타입 체크 통과                                         │
│  ✅ 빌드 성공                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ 필수: DB 종류 판별

**스킬 실행 시 가장 먼저 env 파일을 읽어 DB 종류를 판별합니다.**

```bash
# env 파일 위치
cat api/src/environments/env.local.yml
```

```yaml
# DATABASE_URL 확인
DATABASE_URL: 'postgresql://...'  # → PostgreSQL 모드
DATABASE_URL: 'mysql://...'       # → MySQL 모드
```

**판별 결과에 따라:**
- PostgreSQL → DAO에서 쌍따옴표(`"`) 사용, `::text` 캐스팅
- MySQL → DAO에서 백틱(`` ` ``) 사용, `CAST()` 함수

---

## ⚠️ 필수: Controller 프레임워크 감지

**스킬 실행 시 test-data Controller를 확인하여 프레임워크를 감지합니다.**

```bash
head -3 api/src/modules/test-data/controller/test-data.controller.ts
```

### 판별 기준

| Import 패턴 | 프레임워크 | Controller 스타일 | Validator 스타일 |
|-------------|-----------|-----------------|-----------------|
| `routing-controllers` | Koa | 클래스 데코레이터 | class-validator |
| `elysia` / `createElysia` | Elysia | 체이닝 | TypeBox `t` |

**판별 결과에 따라:**
- Koa → 데코레이터 패턴 + class-validator + `controller-pattern.md` (Koa 섹션)
- Elysia → createElysia 체이닝 + TypeBox `t` + `docs/` 파일 추가 + `controller-pattern.md` (Elysia 섹션)

---

## ⚠️ 필수: DAO 라이브러리 감지

**스킬 실행 시 test-data DAO의 import 문을 확인하여 라이브러리를 감지합니다.**

```bash
# test-data DAO import 확인
head -5 api/src/modules/test-data/dao/test-data.dao.ts
```

### 판별 기준

| Import 패턴 | 라이브러리 | 쿼리 조합 방식 |
|-------------|-----------|---------------|
| `from 'bunqldb'` | bunqldb (기본값) | `query = sql\`${query} AND ...\`` (재할당) |
| `from 'sql-template-strings'` | sql-template-strings | `query.append(sql\`AND ...\`)` |

### 기본값
- **bunqldb** (권장): 현대적인 타입 안전 쿼리 빌더, 재할당 방식
- **sql-template-strings** (레거시): append 방식, 타입 캐스팅 필요

**⚠️ 중요**: 감지된 라이브러리에 맞는 [dao-pattern.md](references/dao-pattern.md) 섹션을 참조하여 코드 생성

---

## 입력 방식

```bash
/peach-gen-backend [테이블명] [옵션]
```

### 옵션
| 옵션 | 기본값 | 설명 |
|------|--------|------|
| file | N | 파일 업로드 기능 (Y/N) |
| excel | N | 엑셀 업로드 기능 (Y/N) |
| controllerTdd | N | Controller TDD API 노출 (Y/N) - Store TDD 진행 시 필요 |

---

## 워크플로우

### 1단계: DB 종류 판별

```bash
cat api/src/environments/env.local.yml | grep DATABASE_URL
```

### 2단계: DAO 라이브러리 감지

```bash
head -5 api/src/modules/test-data/dao/test-data.dao.ts
```

- `from 'bunqldb'` → bunqldb 패턴 사용
- `from 'sql-template-strings'` → sql-template-strings 패턴 사용

### 2.5단계: Controller 프레임워크 감지

```bash
head -3 api/src/modules/test-data/controller/test-data.controller.ts
```

- `routing-controllers` → Koa 모드 (데코레이터 패턴)
- `elysia` / `createElysia` → Elysia 모드 (체이닝 패턴, docs/ 추가)

### 3단계: 스키마 확인

```bash
cat api/db/schema/[도메인]/[테이블].sql
```

스키마 파일이 없으면:
```
⚠️ 스키마 파일이 없습니다!
먼저 /peach-gen-db [테이블명] 실행 후 bun run db:up-dev 하세요.
```

### 3.5단계: 도메인 분석 (Analyze)

test-data와 대상 도메인의 차이를 분석합니다:

1. **스키마 비교**: test-data 대비 필드 수, 타입 복잡도, 관계성
2. **비즈니스 로직 판단**: 단순 CRUD vs 상태 전이/계산 필드/조건부 검증 필요 여부
3. **적응 결정**:
   - Must Follow → 그대로 (모듈 경계, 네이밍, 타입 원칙, 에러 처리)
   - May Adapt → 도메인 맞춤 (service 분리, DAO 쿼리, validator 배치)

### 4단계: 코드 생성

**⚠️ 중요: test-data 가이드코드를 기준 골격으로 참조하되, 도메인 특성에 맞게 Bounded Autonomy 범위 내에서 적응**

참조 템플릿:
- `api/src/modules/test-data/type/test-data.type.ts`
- `api/src/modules/test-data/dao/test-data.dao.ts`
- `api/src/modules/test-data/service/test-data.service.ts`
- `api/src/modules/test-data/controller/test-data.validator.ts`
- `api/src/modules/test-data/controller/test-data.controller.ts`
- `api/src/modules/test-data/test/test-data.test.ts`

### 5단계: TDD 검증 (필수)

```bash
# 테스트 실행
cd api && bun test src/modules/[모듈명]/test/

# 린트 체크
cd api && bun run lint:fixed

# 빌드 확인
cd api && bun run build
```

### 6단계: 티키타카

```
테스트 실패 시:
1. 실패 원인 분석
2. 코드 수정
3. 다시 테스트
4. 통과할 때까지 반복

⚠️ 테스트 통과 없이 완료 선언 금지!
```

---

## 생성 파일 구조

```
# Koa 모드 (routing-controllers)
api/src/modules/[모듈명]/
├── type/[모듈명].type.ts            ← Entity, DTO 타입
├── dao/[모듈명].dao.ts              ← 데이터 접근 계층
├── service/
│   ├── [모듈명].service.ts          ← 비즈니스 로직
│   └── [모듈명]-tdd.service.ts      ← TDD 헬퍼 서비스
├── controller/
│   ├── [모듈명].validator.ts        ← class-validator
│   └── [모듈명].controller.ts       ← 데코레이터 패턴
└── test/
    ├── [모듈명].test.ts             ← TDD 테스트 (실행기 스타일)
    ├── test-file.txt                ← 테스트용 파일 (file=Y)
    └── test-image.png               ← 테스트용 이미지 (file=Y)

# Elysia 모드 (createElysia) - docs/ 추가
api/src/modules/[모듈명]/
├── type/[모듈명].type.ts
├── dao/[모듈명].dao.ts
├── service/
│   ├── [모듈명].service.ts
│   └── [모듈명]-tdd.service.ts
├── controller/
│   ├── [모듈명].validator.ts        ← TypeBox t
│   └── [모듈명].controller.ts       ← createElysia 체이닝
├── docs/[모듈명].docs.ts            ← API 문서 (Elysia만)
└── test/
    ├── [모듈명].test.ts
    ├── test-file.txt                ← (file=Y)
    └── test-image.png               ← (file=Y)
```

---

## 상세 가이드 참조

각 레이어별 상세 패턴은 references 폴더 참조:

- **[type-pattern.md](references/type-pattern.md)**: Type 레이어 패턴 (Entity, DTO 구조)
- **[dao-pattern.md](references/dao-pattern.md)**: DAO 레이어 패턴 (SQL, DB 분기)
- **[service-pattern.md](references/service-pattern.md)**: Service 레이어 패턴 (파일 처리 포함)
- **[controller-pattern.md](references/controller-pattern.md)**: Controller + Validator 패턴
- **[test-pattern.md](references/test-pattern.md)**: TDD 테스트 패턴 (실행기 스타일)
- **[tdd-service-pattern.md](references/tdd-service-pattern.md)**: TDD 헬퍼 서비스 패턴
- **[file-option.md](references/file-option.md)**: file 옵션 처리 가이드
- **[excel-pattern.md](references/excel-pattern.md)**: excel 옵션 처리 가이드 (엑셀 업로드 API)

---

## ⚠️ 조건부 참조 가이드 (토큰 절약)

> **중요**: 선택된 옵션의 참조 파일만 읽으세요!
> 모든 references를 한 번에 로드하지 마세요.

### 필수 참조 (항상)

| 파일 | 용도 |
|------|------|
| type-pattern.md | Entity, DTO 타입 정의 |
| dao-pattern.md | SQL 쿼리 패턴 |
| service-pattern.md | 비즈니스 로직 |
| controller-pattern.md | API 엔드포인트 |
| test-pattern.md | TDD 테스트 |
| tdd-service-pattern.md | TDD 헬퍼 서비스 |

### 옵션별 추가 참조

| 옵션 | 읽어야 할 파일 |
|------|---------------|
| file=Y | file-option.md |
| excel=Y | excel-pattern.md |
| controllerTdd=Y | controller-pattern.md (TDD 섹션) |

### 프레임워크별 추가 참조

| 프레임워크 | 읽어야 할 파일 |
|-----------|--------------|
| Koa | controller-pattern.md (Koa 섹션) |
| Elysia | controller-pattern.md (Elysia 섹션) |

---

## 레이어별 체크리스트

### Type 레이어
→ [type-pattern.md](references/type-pattern.md) 상세 참조
- [ ] Entity, SearchDto, PagingDto, InsertDto, UpdateDto 정의
- [ ] file=Y: EntityDetail, File Interface 추가
- [ ] excel=Y: ExcelUploadDto Interface 추가

### DAO 레이어
→ [dao-pattern.md](references/dao-pattern.md) 상세 참조
- [ ] findPaging, findList, findOne, insert, update, updateUse, softDelete, hardDelete
- [ ] **숫자 파라미터 필터: Number() 변환 필수**
- [ ] file=Y: findFileUuidOne, findFileParentList, updateFileParent, reSetFileParent

### Service 레이어
→ [service-pattern.md](references/service-pattern.md) 상세 참조
- [ ] CRUD + updateUse, softDelete, hardDelete
- [ ] file=Y: detailOne, #parentCode, #parentCodeImage, #fileSetting
- [ ] excel=Y: excelUpload (중복 체크 후 insert/update)

### Controller + Validator 레이어
→ [controller-pattern.md](references/controller-pattern.md) 상세 참조
- [ ] 표준 API: paging, list, detail, insert, update, delete, use
- [ ] **INSERT/UPDATE만 Validator 적용** (조회/상태변경 불필요)
- [ ] controllerTdd=Y: /tdd/init, /tdd/cleanup/:seq 추가

### TDD 레이어
→ [tdd-service-pattern.md](references/tdd-service-pattern.md), [test-pattern.md](references/test-pattern.md) 상세 참조
- [ ] TddService: init, cleanup (file=Y: uploadTestFiles, deleteUploadedFiles)
- [ ] 테스트: 실행기 스타일 단일 통합 테스트 (초기화→CRUD→정리)

---

## Bounded Autonomy (자율 적응 규칙)

### Must Follow (절대 준수)
- 모듈 경계: `_common`만 import
- 네이밍: snake_case(테이블), kebab-case(파일), PascalCase(타입), camelCase(변수)
- 타입: 옵셔널(`?`), `null`, `undefined` 금지
- Service: static 메서드, FK 금지
- 에러: 기능오류 → 200 + `{success:false}`, 시스템예외 → `ErrorHandler`

### May Adapt (분석 후 보완)
- Service 메서드 분리 (복잡한 비즈니스 로직 시)
- DAO 쿼리 구성 (JOIN, 서브쿼리, 조건부 필터 등)
- Validator 구조 (필드 수에 따른 그룹핑)
- 테스트 시나리오 (도메인 고유 엣지 케이스)

### Adapt 조건
보완 시 반드시: (1) 이유 설명 (2) Must Follow 미침범 (3) test/lint/build 통과

---

## 완료 조건

```
┌─────────────────────────────────────────────────────────────────┐
│  ✅ 완료 체크리스트                                              │
│                                                                 │
│  □ 모든 TDD 테스트 통과                                         │
│  □ 숫자 필터 파라미터 Number() 변환 적용 확인                   │
│  □ bun run lint:fixed 통과                                      │
│  □ bun run build 성공                                           │
│                                                                 │
│  위 4가지 모두 통과해야 완료!                                    │
│  실패 시 AI와 티키타카로 수정                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 완료 후 안내

```
🎉 Backend API 생성 완료!

DB 종류: [PostgreSQL/MySQL]

생성된 파일:
├── api/src/modules/[모듈명]/
│   ├── type/[모듈명].type.ts
│   ├── dao/[모듈명].dao.ts
│   ├── service/[모듈명].service.ts
│   ├── service/[모듈명]-tdd.service.ts
│   ├── controller/[모듈명].validator.ts
│   ├── controller/[모듈명].controller.ts
│   └── test/[모듈명].test.ts

검증 결과:
✅ TDD 테스트 통과 (X/X)
✅ 린트 통과
✅ 빌드 성공

📌 확정된 API 스펙:
- GET    /[모듈명]/paging       - 페이징 목록
- GET    /[모듈명]/list         - 전체 목록
- GET    /[모듈명]/:seq         - 상세 조회
- POST   /[모듈명]              - 등록
- PUT    /[모듈명]/:seq         - 수정
- DELETE /[모듈명]/:seq         - 삭제
- PATCH  /[모듈명]/:seq/use     - 활성화/비활성화
- POST   /[모듈명]/excel/upload - 엑셀 업로드 (excel=Y)
- POST   /[모듈명]/tdd/init     - TDD 초기화 (controllerTdd=Y)
- DELETE /[모듈명]/tdd/cleanup/:seq - TDD 정리 (controllerTdd=Y)

📌 Store TDD 필요 시:
→ peach-gen-store storeTdd=Y 실행
→ Backend controllerTdd=Y가 전제조건입니다

다음 단계:
→ /peach-gen-store [모듈명] 실행하여 Frontend Store 생성

📌 테스트 전략 안내:
- Backend TDD: 비즈니스 로직 완전 검증 ✅ (완료)
- Frontend Store TDD: 선택적 (복잡한 클라이언트 로직 있을 때만)
- 대부분의 Store는 API Wrapper이므로 Backend TDD만으로 충분
```

---

## 참조

- **가이드 코드**: `api/src/modules/test-data/`
- **스키마**: `api/db/schema/[도메인]/[테이블].sql`
- **상세 가이드**: `references/` 폴더 참조
