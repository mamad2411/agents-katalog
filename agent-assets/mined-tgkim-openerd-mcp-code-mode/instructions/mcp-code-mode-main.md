# AI 코딩 에이전트 메인 지침 (2025.11.11)

> **MCP Code Mode Starter** - 동적 지침 로딩 시스템 (평균 83.5% 토큰 절감)

## 🎯 워크플로우 (5단계)

### 1. BestCase 로드 + 메타데이터

```typescript
const meta = await buildMetadata(userRequest);
const bestCase = await bestcase.loadBestCase({ projectName: meta.projectName });

// BestCase에서 API 타입 확정
const apiType = bestCase.patterns.apiInfo.apiType;  // "grpc" | "openapi"
```

### 2. TODO + 프리플라이트 (risk ≥40 → high-risk만)

```typescript
const todos = await synthesizeTodo(meta, bestCase);
const { ok, risk, keywords } = await preflight(meta, todos, bestCase);

if (!ok) {
  // risk ≥ 40: 스캐폴딩만 (97% 토큰 절감)
  return await guides.loadGuide({ id: 'high-risk' });
}
```

### 3. 필수 지침 + 동적 검색 (⚠️ API 검증 필수)

```typescript
// 🔑 필수 지침 3개 (API 타입 기반)
const mandatory = [
  `${apiType}.api.connection`,  // grpc.api.connection 또는 openapi.api.connection
  'api.validation',             // API 메서드/시그니처 검증
  'error.handling'              // 에러 처리 패턴
];

// 키워드 기반 동적 검색
const searched = await guides.searchGuides({ 
  keywords, 
  apiType,
  mandatoryIds: mandatory  // 필수 지침 강제 포함
});

// 상위 3개 + 필수 3개 병합
const combined = await guides.combineGuides({
  ids: [...mandatory, ...searched.slice(0, 3).map(g => g.id)]
});
```

### 4. 우수 사례 (≥85점) + 환경 폴백

```typescript
// BestCase에서 우수 사례 검색
const pattern = bestCase.patterns.aiAnalysis.excellentSnippets
  .find(s => s.score >= 85 && keywords.some(k => s.file.includes(k)));

// 환경 체크: openerd/tailwind 없으면 로컬 유틸
const envAware = applyFallback(pattern, meta.uiDeps);
```

### 5. 적용 + 근거 로그

```typescript
await apply({ combined, pattern: envAware });

// 근거 로그 (필수)
console.log({
  usedGuides: combined.usedGuides,  // [{ id, priority, version, scope }, ...]
  pattern: {
    file: pattern.file,
    score: pattern.score,
    reason: pattern.reason
  },
  risk
});
```

## 🚨 필수 규칙

### 1. BestCase 우선

```typescript
// ✅ 올바른 순서
const bestCase = await bestcase.loadBestCase({ projectName });
const apiType = bestCase.patterns.apiInfo.apiType;

// ❌ 잘못된 순서: BestCase 없이 추측
const apiType = 'grpc';  // 위험!
```

### 2. 필수 지침 강제 (⚠️ mandatoryIds)

```typescript
// ✅ 올바른 검색
const searched = await guides.searchGuides({
  keywords,
  apiType,
  mandatoryIds: [
    `${apiType}.api.connection`,
    'api.validation',
    'error.handling'
  ]
});

// ❌ 잘못된 검색: 필수 지침 누락 가능
const searched = await guides.searchGuides({ keywords, apiType });
```

### 3. 리스크 ≥40 처리

```typescript
// ✅ 올바른 처리
if (risk >= 40) {
  const guide = await guides.loadGuide({ id: 'high-risk' });
  return { mode: 'scaffold-only', guide };
}

// ❌ 잘못된 처리: 위험 코드 실행
if (risk >= 40) {
  console.log('Warning: high risk');
  // 계속 진행...
}
```

### 4. 환경 폴백 (openerd/tailwind)

```typescript
// ✅ 올바른 폴백
const hasOpenerd = meta.uiDeps.includes('openerd-nuxt3');
const pattern = hasOpenerd 
  ? excellentSnippet 
  : localUtilPattern;

// ❌ 잘못된 처리: openerd 없는데 사용
import { CommonTable } from '#components';  // 에러!
```

### 5. 근거 로그 필수

```typescript
// ✅ 올바른 로그
console.log({
  usedGuides: [
    { id: 'grpc.api.connection', priority: 100, version: '2025.11.10' },
    { id: 'api.validation', priority: 90, version: '2025.11.11' }
  ],
  pattern: { file: 'pages/users/list.vue', score: 92, reason: 'Pagination + gRPC' },
  risk: 25
});

// ❌ 잘못된 로그
console.log('Applied guides');
```

## 📂 지침 구조

```text
.github/instructions/
  ├─ main.instructions.md           # 본 파일 (내부 프로젝트용)
  ├─ main-ultra-compact.md          # 외부 프로젝트용 (메타 지침)
  ├─ default.instructions.md        # 기본 지침
  └─ guides/                        # 동적 로드 지침들
      ├─ api/
      │   ├─ grpc-api-connection.md
      │   ├─ openapi-api-connection.md
      │   ├─ api-validation.md       # ⭐ 필수 (API 검증)
      │   └─ ...
      ├─ error/
      │   └─ error-handling.md       # ⭐ 필수 (에러 처리)
      ├─ ui/
      │   ├─ openerd-nuxt3-components.md
      │   ├─ pagination-pattern.md
      │   └─ ...
      ├─ workflow/
      │   ├─ core-workflow.md
      │   └─ main-workflow.md
      └─ high-risk.md                # ⭐ risk ≥40 전용
```

## 🔧 리스크 계산 공식

```typescript
risk = 
  10 * apiMismatch +        // API 타입 불일치
  8 * missingDeps +         // 의존성 누락 (openerd 등)
  6 * writeRangeOver +      // 수정 범위 초과 (>5 files)
  4 * guideConflict +       // 지침 충돌
  2 * typeWarn;             // 타입 경고

// risk < 40: 자동 적용 (필수 지침 + 동적 검색)
// risk ≥ 40: high-risk.md만 로드 (스캐폴딩 제공)
```

## 📊 토큰 절감 효과

| 케이스 | 기존 (정적) | 변경 후 (동적) | 절감률 |
|--------|------------|---------------|--------|
| **외부 프로젝트** | 500 토큰 | 100 토큰 | **80%** |
| **내부 프로젝트** | 1500 토큰 | 300 토큰 | **80%** |
| **일반 케이스** | 모든 지침 | 상위 3개 | **77%** |
| **고위험 케이스** | 전체 지침 | high-risk만 | **97%** |

**평균 절감률**: **83.5%**

## 🛠️ MCP 서버 구성

### Filesystem MCP

```typescript
import * as filesystem from 'ai-bindings/filesystem';

await filesystem.readFile({ path: '/projects/my-app/src/index.ts' });
await filesystem.writeFile({ path, content });
await filesystem.searchFiles({ pattern: '*.vue', directory });
```

### BestCase MCP

```typescript
import * as bestcase from 'ai-bindings/bestcase';

const { bestCase } = await bestcase.loadBestCase({ projectName: '50.dktechin/frontend' });
await bestcase.saveBestCase({ projectName, category: 'auto-scan-ai', ... });
const { bestCases } = await bestcase.listBestCases();
```

### Guides MCP (⭐ 동적 로딩)

```typescript
import * as guides from 'ai-bindings/guides';

// 1. 검색 (필수 지침 강제 포함)
const { guides: results } = await guides.searchGuides({
  keywords: ['pagination', 'grpc'],
  apiType: 'grpc',
  mandatoryIds: ['grpc.api.connection', 'api.validation', 'error.handling']
});

// 2. 개별 로드
const { guide } = await guides.loadGuide({ id: 'api.validation' });

// 3. 병합
const { combined, usedGuides } = await guides.combineGuides({
  ids: ['grpc.api.connection', 'api.validation', 'error.handling'],
  context: { project: 'my-app', apiType: 'grpc' }
});
```

## 🎓 핵심 원칙

1. ✅ **BestCase 우선**: API 타입/우수 사례 확인 필수
2. ✅ **필수 지침 강제**: `mandatoryIds` 파라미터 사용
3. ✅ **리스크 임계값**: ≥40이면 high-risk.md만
4. ✅ **환경 폴백**: openerd/tailwind 없으면 로컬 유틸
5. ✅ **근거 로그**: 지침 id/버전 + 우수 사례 파일/점수
6. ✅ **런타임 로딩**: 필요한 지침만 동적 로드
7. ✅ **scope 우선순위**: project > repo > org > global
8. ✅ **타입 안전성**: TypeScript strict mode
9. ✅ **모듈 해석**: 상대 경로 import (../../packages/...)
10. ✅ **ID Sanitization**: 슬래시 → 하이픈 (BestCase ID)
11. ✅ **Proto/OpenAPI 타입 직접 사용**: interface 재정의 금지
12. ✅ **작업 컨텍스트 로깅**: 파일/작업/타입 명시

### 11. Proto/OpenAPI 타입 직접 사용 (⭐ 데이터 원본성)

```typescript
// ❌ 잘못된 방법: interface 재정의
interface UserTableData {
  이메일: string;
  이름: string;
  가입일: string;  // Timestamp → string 변환
  _raw?: GetUserListResponse_User;  // 원본 중복 저장
}

const users = ref<UserTableData[]>([]);

// ✅ 올바른 방법: Proto 타입 직접 사용
import type { GetUserListResponse_User, Timestamp } from '@project/proto';

type User = GetUserListResponse_User;
const users = ref<User[]>([]);

// 테이블 컬럼에서 format 함수 활용
const columns = [
  { key: 'email', label: '이메일' },
  { key: 'name', label: '이름' },
  { 
    key: 'createdAt', 
    label: '가입일',
    format: (val: Timestamp) => formatDate(val)  // 표시만 변환
  }
];
```

**이유:**
- Proto 타입이 **정답** (백엔드 계약서)
- interface 재정의는 데이터 원본성 훼손
- `_raw` 필드 중복 저장은 메모리 낭비
- Proto 업데이트 시 자동 동기화

### 12. 작업 컨텍스트 로깅 (⭐ 투명성)

```typescript
// ✅ 모든 작업 시작 시 로깅
console.log('[작업 시작]', {
  file: 'pages/memberManagement.vue',
  task: '회원관리 페이지 - 회원 목록/주문 내역 조회',
  protoTypes: [
    'GetUserListRequest',
    'GetUserListResponse_User',
    'GetOrderItemProductGroupListResponse_OrderItem'
  ],
  methods: [
    'client.getUserList({ page, limit })',
    'client.getOrderItemProductGroupList({ userId })'
  ],
  usedGuides: [
    { id: 'grpc.api.connection', version: '2025.11.11' },
    { id: 'api.validation', version: '2025.11.11' }
  ],
  protoFile: 'node_modules/@airian/proto/dist/types/proto_pb.d.ts'
});

// API 호출 시
console.log('[API 호출]', { method: 'getUserList', request: { page: 1 } });
console.log('[API 응답]', { method: 'getUserList', count: response.users.length });
```

**이유:**
- 어떤 파일을 읽고 무슨 작업을 하는지 명확히
- main.instructions.md 워크플로우 준수 여부 검증
- 디버깅/에러 추적 용이

## 📚 참고 문서

- `.github/instructions/default.instructions.md` - 기본 지침 (프로젝트 구조, 빌드 규칙)
- `docs/PROJECT_STRUCTURE.md` - 프로젝트 구조 상세
- `docs/USAGE_GUIDE.md` - 사용법 + 토큰 절감 효과
- `docs/MCP_SETUP_GUIDE.md` - Guides MCP 서버 설정
- `CHANGELOG_DYNAMIC_GUIDES.md` - 2025.11.10 변경 이력

---

**이 지침을 따르면 평균 83.5% 토큰 절감 + production-ready MCP 서버 구축 가능**

