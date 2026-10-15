---
name: peach-gen-store
description: Frontend Store 전문 생성 스킬. "스토어 만들어줘", "Store 생성", "프론트 상태관리" 키워드로 트리거. Backend API 기반 생성, TDD 검증 필수.
---

# Frontend Store 생성 스킬

## 페르소나

```
당신은 Vue3/Pinia 상태관리 최고 전문가입니다.
- Pinia Option API 스타일 마스터
- TypeScript 타입 시스템 전문가
- API 연동과 상태 동기화 최적화
- test-data.store.ts 패턴의 완벽한 구현
```

---

## 핵심 원칙

```
┌─────────────────────────────────────────────────────────────────┐
│  순차 개발 전략에서 peach-gen-store의 역할                             │
│                                                                 │
│  전제조건: Backend API 완료 (TDD 통과)                          │
│                                                                 │
│  1. Backend API 스펙 기반으로 생성                              │
│  2. TDD 검증 필수 (API 연동 테스트)                             │
│  3. 출력물 = 확정된 Store 인터페이스 (다음 단계 입력)           │
│  4. AI와 티키타카로 품질 확보                                   │
│                                                                 │
│  완료 기준:                                                     │
│  ✅ vue-tsc 타입 체크 통과 (필수)                               │
│  ⚪ TDD 테스트 통과 (복잡한 클라이언트 로직 있을 때만)          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 입력 방식

```bash
/peach-gen-store [테이블명] [옵션]
```

### 옵션
| 옵션 | 기본값 | 설명 |
|------|--------|------|
| file | N | 파일 업로드 기능 (Y/N) |
| storeTdd | N | Store TDD 액션 생성 (Y/N) - Backend controllerTdd=Y 필요 |

---

## 워크플로우

### 1단계: Backend API 확인

```bash
# Backend 파일 존재 확인
ls api/src/modules/[모듈명]/

# API 스펙 확인 (Type 파일)
cat api/src/modules/[모듈명]/type/[모듈명].type.ts
```

Backend가 없으면:
```
⚠️ Backend API가 없습니다!
먼저 /peach-gen-backend [테이블명] 실행하세요.
```

### 1.5단계: 도메인 분석 (Analyze)

Backend API 타입과 test-data Store를 비교 분석합니다:

1. **API 스펙 비교**: test-data 대비 엔드포인트 수, 응답 구조, 특수 액션
2. **상태 복잡도 판단**: 단순 CRUD Store vs 다중 리스트/필터 상태/파생 상태 필요 여부
3. **적응 결정**:
   - Must Follow → 그대로 (Pinia Option API, 타입 원칙, 모듈 경계)
   - May Adapt → 도메인 맞춤 (추가 상태 필드, 액션 분리)

### 2단계: 코드 생성

참조 템플릿 (test-data):
- `front/src/modules/test-data/type/test-data.type.ts`
- `front/src/modules/test-data/store/test-data.store.ts`
- `front/src/modules/test-data/test/test-data.test.ts`

### 3단계: TDD 검증 (필수)

```bash
# 타입 체크
cd front && bunx vue-tsc --noEmit

# 테스트 실행 (있는 경우)
cd front && bun test src/modules/[모듈명]/test/
```

### 4단계: 티키타카

```
타입 에러 또는 테스트 실패 시:
1. 에러 원인 분석
2. 코드 수정
3. 다시 검증
4. 통과할 때까지 반복

⚠️ 타입 체크 통과 없이 완료 선언 금지!
```

---

## 생성 파일 구조

```
front/src/modules/[모듈명]/
├── type/[모듈명].type.ts    ← Entity, DTO 타입
├── store/[모듈명].store.ts  ← Pinia Store
└── test/[모듈명].test.ts    ← TDD 테스트 (선택적)
```

---

## 레이어별 체크리스트

### Type 레이어
- [ ] Entity Interface (백엔드와 동일)
- [ ] ListItem Interface (목록용, nIndex 추가)
- [ ] SearchDto Interface (검색 파라미터)
- [ ] PagingDto Interface (페이징, sortData 추가)
- [ ] InsertDto Interface (등록용)
- [ ] UpdateDto Interface (수정용)
- [ ] File Interface (file=Y인 경우)

### Store 레이어

#### State
- [ ] listData: ListItem[] (목록 데이터)
- [ ] listTotalRow: number (전체 개수)
- [ ] detailData: Entity | null (상세 데이터)

#### Actions ([상세](references/store-pattern.md))
- [ ] detailDataInit (상세 데이터 초기화)
- [ ] paging (페이징 목록) - `useApi().get('/[모듈명]', params)`
- [ ] list (전체 목록) - `useApi().get('/[모듈명]/list', params)`
- [ ] detail (상세 조회) - `useApi().get('/[모듈명]/' + seq)`
- [ ] cursorList (커서 페이징) - `useApi().get('/[모듈명]/cursor-list')`
- [ ] insert (등록) - `useApi().post('/[모듈명]', data)`
- [ ] update (수정) - `useApi().put('/[모듈명]/' + seq, data)`
- [ ] updateUse (활성화/비활성화) - `useApi().patch('/[모듈명]/use')`
- [ ] softDelete (삭제) - `useApi().patch('/[모듈명]/delete')`
- [ ] hardDelete (물리 삭제, 테스트용) - `useApi().delete('/[모듈명]/' + seq)`

#### TDD Operations (storeTdd=Y인 경우만)
→ 하단 "Store TDD" 섹션 참조

#### 파일 기능 (file=Y)
- [ ] uploadFileLocal (로컬 파일 업로드)
- [ ] uploadFileS3 (S3 파일 업로드)
- [ ] getDownloadUrl (다운로드 URL)

### TDD 테스트 (storeTdd=Y인 경우만)
→ 하단 "Store TDD" 섹션 참조

---

## 패턴 규칙

```typescript
// ✅ Pinia Option API 스타일 (권장)
export const use[모듈명]Store = defineStore('[모듈명]', {
  state: () => ({
    listData: [] as ListItem[],
    listTotalRow: 0,
    detailData: null as Entity | null,
  }),
  actions: {
    async paging(params: PagingDto) {
      const { $api } = useNuxtApp();
      const res = await $api.get('[모듈명]/paging', { params });
      if (res.value?.data) {
        this.listData = res.value.data.list;
        this.listTotalRow = res.value.data.totalRow;
      }
      return res;
    },
    // ...
  },
});

// ❌ Setup 스타일 (사용 금지)
export const use[모듈명]Store = defineStore('[모듈명]', () => {
  // ...
});
```

---

## file 옵션 처리

### file=N (기본)
- Store: 파일 관련 함수 제외
  - uploadFileLocal ❌
  - uploadFileS3 ❌
  - getDownloadUrl ❌

### file=Y
- Store: 파일 관련 함수 포함
  - `uploadFileLocal` ✅
  - `uploadFileS3` ✅
  - `getDownloadUrl` ✅
- Type: File 인터페이스 추가

---

## Bounded Autonomy (자율 적응 규칙)

### Must Follow (절대 준수)
- Pinia Option API (Setup 스타일 금지)
- 타입: 옵셔널(`?`), `null`, `undefined` 금지
- 모듈 경계: `_common`만 import
- Store 표준 상태: `listData`, `listTotalRow`, `detailData`

### May Adapt (분석 후 보완)
- 추가 상태 필드 (도메인 고유 필터, 다중 리스트)
- 액션 분리 방식 (복잡한 데이터 변환 로직)
- 에러 핸들링 세부 구현

### Adapt 조건
보완 시 반드시: (1) 이유 설명 (2) Must Follow 미침범 (3) vue-tsc 통과

---

## 완료 조건

```
┌─────────────────────────────────────────────────────────────────┐
│  ✅ 완료 체크리스트                                              │
│                                                                 │
│  □ bunx vue-tsc --noEmit 통과 (필수)                             │
│  □ TDD 테스트 통과 (storeTdd=Y인 경우만)                        │
│                                                                 │
│  위 조건 모두 통과해야 완료!                                     │
│  실패 시 AI와 티키타카로 수정                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 완료 후 안내

```
🎉 Frontend Store 생성 완료!

생성된 파일:
├── front/src/modules/[모듈명]/
│   ├── type/[모듈명].type.ts
│   └── store/[모듈명].store.ts

검증 결과:
✅ 타입 체크 통과

📌 확정된 Store 인터페이스:
- use[모듈명]Store()
  - state: listData, listTotalRow, detailData
  - actions: paging, list, detail, insert, update, updateUse, softDelete

다음 단계:
→ /peach-gen-ui [모듈명] 실행하여 Frontend UI 생성
```

---

## Store TDD (storeTdd=Y인 경우만)

→ [test-pattern.md](references/test-pattern.md) 상세 참조

> **전제조건**: Backend controllerTdd=Y 필요
> 대부분의 Store는 API Wrapper이므로 TDD 불필요. Backend TDD로 충분.

### TDD Actions
- initTdd (TDD 데이터 생성) - `useApi().post('/[모듈명]/tdd/init')`
- cleanupTdd (TDD 정리) - `useApi().delete('/[모듈명]/tdd/cleanup/' + seq)`

### 통합 워크플로우 테스트
- beforeAll: VitestSetup.initializeTestEnvironment(), sign()
- it('통합 워크플로우'): 실행기 스타일 단일 테스트
  1. TDD 데이터 생성 (initTdd)
  2. 상세 조회 (detail)
  3. 데이터 수정 (update)
  4. 사용여부 변경 (updateUse)
  5. 리스트/페이징 조회
  6. 커서 페이징 (cursorList)
  7. 파일 업로드/수정 (file=Y)
  8. 논리적 삭제 (softDelete)
  9. TDD 물리 삭제 (cleanupTdd)
- finally: 예외 시 cleanup

---

## 상세 가이드 참조

각 레이어별 상세 패턴은 references 폴더 참조:

- **[store-pattern.md](references/store-pattern.md)**: Pinia Option API Store 패턴
- **[type-pattern.md](references/type-pattern.md)**: Frontend Type 패턴 (Entity, DTO)
- **[test-pattern.md](references/test-pattern.md)**: Frontend TDD 테스트 패턴 (실행기 스타일)
- **[file-option.md](references/file-option.md)**: file 옵션 처리 가이드

---

## ⚠️ 조건부 참조 가이드 (토큰 절약)

> **중요**: 선택된 옵션의 참조 파일만 읽으세요!
> 모든 references를 한 번에 로드하지 마세요.

### 필수 참조 (항상)

| 파일 | 용도 |
|------|------|
| store-pattern.md | Pinia Store 구조 |
| type-pattern.md | Entity, DTO 타입 정의 |

### 옵션별 추가 참조

| 옵션 | 읽어야 할 파일 |
|------|---------------|
| file=Y | file-option.md |
| storeTdd=Y | test-pattern.md |

---

## 참조

- **가이드 코드 (필수)**: `front/src/modules/test-data/`
- **Backend Type**: `api/src/modules/[모듈명]/type/`

⚠️ **중요**: test-data 가이드 코드를 기준 골격으로 참조하되, 도메인 특성에 맞게 Bounded Autonomy 범위 내에서 적응
