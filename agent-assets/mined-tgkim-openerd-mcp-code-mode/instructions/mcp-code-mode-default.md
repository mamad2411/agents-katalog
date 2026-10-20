# MCP Code Mode Starter - AI Coding Guidelines

> **⚠️ 모든 작업은 반드시 5단계 워크플로우를 따라야 합니다**
>
> 이 지침을 무시하고 수동으로 파일을 검색하거나 추측으로 코드를 작성하면 안 됩니다.

## 🚨 필수 작업 시작 프로토콜

**모든 코딩 작업 시작 시 반드시 다음 순서를 따르세요:**

```typescript
// ========================================
// 🔴 1단계: 작업 컨텍스트 로그 (필수!)
// ========================================
console.log('[작업 시작]', {
  timestamp: new Date().toISOString(),
  file: '파일 경로',
  task: '작업 설명',
  workflow: 'main.instructions.md 5단계 워크플로우 준수'
});

// ========================================
// 🔴 2단계: BestCase 로드 (필수!)
// ========================================
const bestCase = await bestcase.loadBestCase({ 
  projectName: '프로젝트명'  // 예: '49.airian/frontend-admin'
});

console.log('[BestCase 로드]', {
  projectName: bestCase.projectName,
  apiType: bestCase.patterns.apiInfo.apiType,  // "grpc" | "openapi"
  hasGrpc: bestCase.patterns.apiInfo.hasGrpc,
  endpoints: bestCase.patterns.apiInfo.endpoints?.slice(0, 3)
});

// ❌ BestCase 없이 추측으로 작업 금지!
// ❌ proto 파일 직접 grep 금지!
// ❌ trial & error 반복 금지!

// ========================================
// 🔴 3단계: 리스크 분석 + guides 검색 (필수!)
// ========================================
const keywords = extractKeywords(userRequest, bestCase);
const risk = calculateRisk(userRequest, bestCase);

console.log('[리스크 분석]', { risk, keywords });

if (risk >= 40) {
  // 고위험: high-risk.md만 로드
  const { guide } = await guides.loadGuide({ id: 'high-risk' });
  console.log('[고위험 모드]', { guide: 'high-risk.md' });
  return guide.content;
}

// 필수 지침 ID 구성
const apiType = bestCase.patterns.apiInfo.apiType;
const mandatoryIds = [
  `${apiType}.api.connection`,  // 'grpc.api.connection' 또는 'openapi.api.connection'
  'api.validation',             // API 메서드/시그니처 검증
  'error.handling'              // 에러 처리 패턴
];

// guides 검색
const { guides: searchResults } = await guides.searchGuides({
  keywords,
  apiType,
  mandatoryIds  // 🔑 필수 지침 강제 포함
});

console.log('[guides 검색 결과]', {
  totalFound: searchResults.length,
  mandatory: mandatoryIds,
  top3: searchResults.slice(0, 3).map(g => ({ id: g.id, score: g.score }))
});

// ========================================
// 🔴 4단계: 지침 로드 (필수!)
// ========================================
const guideIds = searchResults.slice(0, 5).map(g => g.id);

// 각 지침 개별 로드 및 로그
const loadedGuides = [];
for (const id of guideIds) {
  const { guide } = await guides.loadGuide({ id });
  loadedGuides.push(guide);
  
  console.log('[지침 로드]', {
    id: guide.id,
    version: guide.version,
    priority: guide.priority,
    summary: guide.summary
  });
}

// ========================================
// 🔴 5단계: 지침 기반 코드 생성 (필수!)
// ========================================
// loadedGuides[0].content에 있는 패턴/규칙을 따라 코드 생성
// 예: grpc.api.connection 가이드에서
//   - useAdminClient 사용법 확인
//   - Proto 타입 직접 사용 패턴 확인
//   - 에러 처리 패턴 확인

// 코드 생성...

// ========================================
// 🔴 6단계: 작업 완료 로그 (필수!)
// ========================================
console.log('[작업 완료]', {
  timestamp: new Date().toISOString(),
  file: '파일 경로',
  usedGuides: loadedGuides.map(g => ({
    id: g.id,
    version: g.version,
    priority: g.priority
  })),
  protoTypes: ['사용한 Proto 타입들'],
  methods: ['사용한 API 메서드들'],
  risk
});
```

## ❌ 절대 금지 사항

1. ❌ **BestCase 없이 작업 시작**
   ```typescript
   // ❌ 잘못된 예
   // proto 파일 직접 검색
   Get-Content proto_pb.d.ts | Select-String "GetUserList"
   
   // ✅ 올바른 예
   const bestCase = await bestcase.loadBestCase({ projectName });
   ```

2. ❌ **guides 없이 코드 작성**
   ```typescript
   // ❌ 잘못된 예
   // 추측으로 useGrpcClient 사용
   const client = useGrpcClient();
   
   // ✅ 올바른 예
   const { guide } = await guides.loadGuide({ id: 'grpc.api.connection' });
   // guide.content에서 사용법 확인 후 코드 작성
   ```

3. ❌ **Proto 타입 재정의**
   ```typescript
   // ❌ 잘못된 예
   interface UserTableData {
     이메일: string;
     이름: string;
     _raw?: GetUserListResponse_User;
   }
   
   // ✅ 올바른 예
   import type { GetUserListResponse_User } from '@project/proto';
   type User = GetUserListResponse_User;
   const users = ref<User[]>([]);
   ```

4. ❌ **작업 컨텍스트 로그 생략**
   ```typescript
   // ❌ 잘못된 예
   // 로그 없이 바로 코드 작성
   
   // ✅ 올바른 예
   console.log('[작업 시작]', { file, task, usedGuides });
   ```

5. ❌ **trial & error 반복**
   ```typescript
   // ❌ 잘못된 예
   // getUserList → 에러
   // getOrderList → 에러
   // getOrderItemList → 성공
   
   // ✅ 올바른 예
   // bestCase.patterns.apiInfo.endpoints에서 확인
   ```

## 📋 프로젝트 개요

**목적**: Anthropic Code Mode 패턴 기반 MCP 서버 구현 - BestCase 관리 + 동적 지침 로딩 + 98% 토큰 절감

**핵심 기술**:
- TypeScript 5.9 (strict mode)
- Yarn 4.9.1 Berry (워크스페이스)
- Node.js 20+
- vm2 (샌드박스)
- Docker (GPU 지원)

**핵심 컨셉**:
> **Code Mode** = 중간 데이터를 LLM 컨텍스트로 전달하지 않고, 샌드박스에서 TypeScript 코드를 실행하여 최종 결과만 반환

## 🏗️ 프로젝트 구조

```text
mcp-code-mode-starter/
├── .github/instructions/          # ⭐ 동적 지침 로딩 시스템
│   ├── guides/                    # 런타임에 동적 로드되는 지침들
│   │   ├── api/                   # API 연동 (gRPC, OpenAPI)
│   │   │   ├── grpc-api-connection.md       # ⭐ 필수
│   │   │   ├── openapi-api-connection.md
│   │   │   └── api-validation.md            # ⭐ 필수
│   │   ├── error/
│   │   │   └── error-handling.md            # ⭐ 필수
│   │   ├── ui/                    # UI 컴포넌트 (openerd-nuxt3)
│   │   ├── workflow/              # 워크플로우 상세
│   │   └── high-risk.md           # 리스크 ≥40 전용
│   ├── main.instructions.md       # 내부 프로젝트용 (300 토큰)
│   ├── main-ultra-compact.md      # 외부 프로젝트용 (15 토큰)
│   └── default.instructions.md    # 기본 지침 (본 파일)
├── packages/
│   ├── bestcase-db/               # BestCase 저장소
│   ├── ai-bindings/               # MCP 도구 통합
│   ├── ai-runner/                 # vm2 샌드박스
│   └── llm-analyzer/              # Ollama 코드 분석
├── mcp-servers/
│   ├── filesystem/                # 파일 시스템 API
│   ├── bestcase/                  # BestCase API
│   └── guides/                    # ⭐ 동적 지침 로딩 API
│       ├── index.ts               # searchGuides, loadGuide, combineGuides
│       └── preflight.ts           # 리스크 분석
├── apps/web/                      # Nuxt3 웹 UI
└── scripts/scan/                  # 스캔 스크립트
```

## 🎯 동적 지침 로딩 시스템 (2025.11.10)

### 핵심 원리

**기존 문제: 지침도 토큰을 잡아먹음**

```text
전통적 방식: 모든 지침을 항상 메모리에 로드
→ 워크플로우 상세 (~1500 토큰)
→ API 가이드 (~800 토큰)
→ UI 사용법 (~600 토큰)
= 총 2900 토큰 항상 소비
```

**해결책: 지침을 파일시스템으로 분리 + 필요할 때만 로드**

```typescript
// 1. BestCase에서 API 타입 확인
const bestCase = await bestcase.loadBestCase({ projectName });
const apiType = bestCase.patterns.apiInfo.apiType; // "grpc" | "openapi"

// 2. 리스크 분석
const { risk, keywords } = await analyzeRequest(userRequest, bestCase);
if (risk >= 40) {
  // 고위험: high-risk.md 1개만 로드 (~50 토큰)
  return await guides.loadGuide({ id: 'high-risk' });
}

// 3. 필수 지침 + 동적 검색
const mandatory = [
  `${apiType}.api.connection`,  // grpc.api.connection 또는 openapi.api.connection
  'api.validation',
  'error.handling'
];
const searched = await guides.searchGuides({ keywords, apiType });
const top3 = searched.slice(0, 3).map(g => g.id);

// 4. 병합 (scope > priority > version 순)
const combined = await guides.combineGuides({ 
  ids: [...mandatory, ...top3] 
});
// → 총 ~350 토큰 (기존 1500 → 77% 절감!)
```

### 토큰 절감 효과

| 케이스 | 변경 전 | 변경 후 | 절감률 |
|--------|---------|---------|--------|
| **외부 프로젝트 (Ultra Compact)** | 500 토큰 | 100 토큰 | **80%** |
| **내부 프로젝트 (메인 지침)** | 1500 토큰 | 300 토큰 | **80%** |
| **일반 케이스 (동적 로드)** | 모든 지침 | 상위 3개 | **77%** |
| **고위험 케이스** | 전체 지침 | high-risk만 | **97%** |

**평균 절감률: 83.5%**

### Guides MCP 서버 API

**1. searchGuides - 키워드 기반 검색**

```typescript
const result = await guides.searchGuides({
  keywords: ['grpc', 'pagination', 'error'],
  apiType: 'grpc',
  limit: 3
});
// 반환: 상위 3개 지침 ID만 (내용 로드 X)
```

**2. loadGuide - 특정 지침 로드**

```typescript
const guide = await guides.loadGuide({ id: 'api/grpc-connection' });
// 반환: 전체 지침 내용 + 메타데이터
```

**3. combineGuides - 우선순위 병합**

```typescript
const combined = await guides.combineGuides({
  ids: ['api/grpc-connection', 'error/handling', 'ui/pagination'],
  context: { project: 'my-app', apiType: 'grpc' }
});
// 반환: scope > priority > version 순으로 병합된 지침
```

## 🛠️ 필수 코딩 규칙

### 1. 모듈 해석 (매우 중요)

**✅ 올바른 import 패턴:**

```typescript
// mcp-servers/bestcase/saveBestCase.ts
import { BestCaseStorage } from '../../packages/bestcase-db/dist/index.js';

// packages/ai-bindings/src/index.ts
export * as filesystem from '../../mcp-servers/filesystem/index.js';
export * as bestcase from '../../mcp-servers/bestcase/index.js';
export * as guides from '../../mcp-servers/guides/index.js';  // ⭐ 추가

// packages/ai-runner/src/sandbox.ts
import { filesystem, bestcase, guides } from 'ai-bindings';

// fs/path named import
import { promises as fs } from 'fs';
import { join, dirname } from 'path';
```

**❌ 잘못된 패턴:**

```typescript
// mcp-servers에서 workspace:* 사용 금지
import { BestCaseStorage } from 'bestcase-db';  // ❌

// fs/path default import 금지
import fs from 'fs';    // ❌
import path from 'path'; // ❌
```

### 2. TypeScript 빌드 순서 (필수)

```bash
# 항상 이 순서로 빌드
yarn workspace bestcase-db run build
yarn workspace ai-bindings run build
yarn workspace ai-runner run build

# 또는 통합 명령어
yarn build:all
```

### 3. BestCase ID Sanitization (필수)

```typescript
// ✅ 올바름: 슬래시 치환
const sanitizedProjectName = input.projectName
  .replace(/\//g, '-')
  .replace(/\\/g, '-');
const id = `${sanitizedProjectName}-${input.category}-${Date.now()}`;

// ❌ 잘못됨: 슬래시 포함 시 서브디렉토리 생성 실패
const id = `${input.projectName}-${input.category}-${Date.now()}`;
// "50.dktechin/frontend" → 에러
```

### 4. 샌드박스 실행 패턴

```typescript
// packages/ai-runner/src/sandbox.ts
const logs: string[] = [];

const sandbox = {
  filesystem,
  bestcase,
  guides,  // ⭐ 추가
  console: {
    log: (...args: any[]) => logs.push(args.join(' '))
  }
};

const vm = new VM({ timeout: 30000, sandbox });
const wrappedCode = `(async () => { ${code} })()`;
const result = await vm.run(wrappedCode);
```

## 📊 BestCase 스키마

```typescript
interface BestCase {
  id: string;                    // sanitized-project-name-category-timestamp
  projectName: string;           // 원본 이름 (슬래시 포함 가능)
  category: string;              // 'auto-scan', 'auto-scan-ai', etc.
  description: string;
  files: Array<{
    path: string;
    content: string;
    purpose: string;
  }>;
  patterns: {
    stats?: {
      totalFiles: number;
      vueFiles: number;
      tsFiles: number;
    };
    apiInfo?: {
      hasGrpc: boolean;
      hasOpenApi: boolean;
      apiType: 'gRPC' | 'OpenAPI' | 'unknown';
    };
    componentUsage?: {
      CommonTable: number;
      CommonButton: number;
      // ...
    };
    scores?: {
      final: number;       // 0-100
      pattern: number;
      api: number;
      component: number;
      tier: 'S' | 'A' | 'B' | 'C' | 'D';
    };
    aiAnalysis?: {
      averageScore: number;
      topFiles: Array<{ path: string; score: number }>;
      excellentSnippets?: Array<{  // ⭐ 85점 이상 우수 사례
        file: string;
        score: number;
        reason: string;
      }>;
    };
  };
  metadata: {
    createdAt: string;
    updatedAt: string;
    tags: string[];
  };
}
```

## 🎯 워크플로우 (5단계)

### 1. BestCase 로드 + 메타데이터

```typescript
const meta = await buildMetadata(userRequest);
const bestCase = await bestcase.loadBestCase({ projectName: meta.projectName });
```

### 2. TODO + 프리플라이트 (risk ≥40 → guides/high-risk만)

```typescript
const todos = await synthesizeTodo(meta, bestCase);
const { ok, risk, keywords } = await preflight(meta, todos, bestCase);
if (!ok) return await guides.loadGuide({ id: 'high-risk' });
```

### 3. 필수 지침 + 동적 검색

```typescript
const mandatory = [
  `${meta.apiType}.api.connection`,
  'api.validation',
  'error.handling'
];
const searched = await guides.searchGuides({ keywords, apiType: meta.apiType });
const combined = await guides.combineGuides({ 
  ids: [...mandatory, ...searched.slice(0, 3).map(g => g.id)] 
});
```

### 4. 우수 사례 (≥85점) + 환경 폴백

```typescript
const pattern = bestCase.aiAnalysis.excellentSnippets.find(s => s.score >= 85);
const envAware = applyFallback(pattern, meta.uiDeps);  // openerd/tailwind 체크
```

### 5. 적용 + 근거 로그

```typescript
await apply({ combined, pattern: envAware });
console.log({ 
  usedGuides: combined.usedGuides, 
  pattern: pattern.file, 
  risk 
});
```

## 🧪 테스팅 & 디버깅

### 일반적인 빌드 에러

| 에러 | 원인 | 해결책 |
|------|------|--------|
| `Cannot find module 'vm2'` | 타입 정의 누락 | `src/vm2.d.ts` 생성 |
| `ERR_MODULE_NOT_FOUND: dist/index.js` | 잘못된 import | 실제 빌드 출력 확인 |
| `Default export not found` | 잘못된 import | named import 사용 |
| BestCase ID에 `/` 포함 | sanitization 누락 | `replace(/\//g, '-')` |
| guides 검색 결과 없음 | 지침 파일 미존재 | `guides/` 디렉토리 구조 확인 |

### Docker 관련 실패 사례

**1. read-only 볼륨 문제:**

```yaml
# ✅ 올바른 설정 (BestCase 저장용)
volumes:
  - D:/01.Work/01.Projects:/projects  # :ro 제거
```

**2. 컨테이너 재시작 루프:**

```dockerfile
# ✅ 대기 상태 유지
CMD ["tail", "-f", "/dev/null"]
# 실제 실행은 docker exec로
```

### 필수 명령어

```bash
# 전체 빌드
yarn build:all

# AI 파일 기반 스캔 (v3.0)
yarn scan

# 기존 BestCase 마이그레이션 (필요 시)
yarn scan:migrate

# Docker GPU 확인
docker exec ollama-code-analyzer nvidia-smi

# guides 지침 확인
ls -la .github/instructions/guides/
```

## 📚 참고 문서

**프로젝트 문서:**

- `README.md` - 프로젝트 개요
- `docs/PROJECT_STRUCTURE.md` - 구조 상세 (동적 지침 시스템 포함)
- `docs/USAGE_GUIDE.md` - 사용법 (토큰 절감 효과)
- `docs/MCP_SETUP_GUIDE.md` - Guides MCP 서버 설정
- `CHANGELOG_DYNAMIC_GUIDES.md` - 2025.11.10 변경 이력

**외부 참고자료:**

- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Cloudflare: Code Mode](https://blog.cloudflare.com/code-mode/)
- [Simon Willison: Code execution with MCP](https://simonwillison.net/2025/Nov/4/code-execution-with-mcp/)

## 🎓 핵심 원칙 (최종 정리)

1. ✅ **단일 execute tool**: 100개 tool 대신 1개
2. ✅ **TypeScript API**: MCP 툴을 함수로 노출
3. ✅ **샌드박스 실행**: vm2로 격리
4. ✅ **중간 데이터 격리**: 샌드박스 내부에서 처리
5. ✅ **최종 결과만 반환**: 98% 토큰 절감
6. ✅ **동적 지침 로딩**: 필요한 지침만 런타임에 로드 (77-97% 추가 절감)
7. ✅ **타입 안전성**: TypeScript strict mode
8. ✅ **모듈 해석**: 상대 경로 import 사용
9. ✅ **BestCase 우선**: API 타입/우수 사례 확인 필수
10. ✅ **환경 폴백**: openerd/tailwind 없으면 로컬 유틸

---

**이 지침을 따르면 Anthropic Code Mode + 동적 지침 로딩 패턴을 준수하는 production-ready MCP 서버를 구축할 수 있습니다.**

**토큰 절감 효과:**

- Code Mode: 데이터 처리 **98% 절감**
- 동적 지침: 지침 로딩 **77-97% 절감**
- **총합: 평균 90%+ 토큰 절감**
