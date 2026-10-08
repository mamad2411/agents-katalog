---
description: service bacis guide that you should follow every time
alwaysApply: false
---

# 몬스터 협동조합 프로젝트 가이드

## 프로젝트 개요
**몬스터 협동조합**은 "팀프러너를 양성하는 No.1 교육 기관"으로, Next.js 15 기반의 현대적인 웹 플랫폼을 구축하는 프로젝트입니다.

### 핵심 목표
- 1차: 몬스터 협동조합 소개 및 브랜딩 플랫폼
- 2차: 오프라인 교육 프로그램 예약/결제 시스템
- 3차: SQUEEZE LMS 온라인 구독 서비스

## 기술 스택

### 프론트엔드
- **프레임워크**: Next.js 15 (App Router)
- **UI**: Shadcn/ui + Tailwind CSS
- **애니메이션**: Framer Motion
- **상태관리**: TanStack Query + React State
- **폼 관리**: React Hook Form + Zod

### 백엔드 & 데이터베이스
- **Database**: Supabase PostgreSQL (이미 스키마 적용 완료)
- **인증**: Supabase Auth
- **스토리지**: Supabase Storage
- **실시간**: Supabase Realtime
- **결제**: TossPayments
- **MCP**: Supabase MCP를 통한 데이터베이스 관리

### 데이터베이스 구조 (DB Schema 적용 완료)
- **사용자**: profiles, program_participants, wishlists
- **프로그램**: programs, program_categories
- **구독**: subscription_plans, user_subscriptions
- **결제**: payments, refunds
- **시스템**: inquiries, notifications, site_settings

### CMS (하이브리드)
- **Supabase**: 상품 메타데이터 (가격, 재고, 기본 정보)
- **Notion**: 상세 컨텐츠 (커리큘럼, 강사 소개, 리치 미디어)

## 코딩 표준

### 파일 구조
```
app/
├── (auth)/
├── (main)/
├── admin/
├── api/
├── components/
├── lib/
│   ├── supabase/
│   │   ├── client.ts
│   │   └── server.ts
│   ├── database/
│   ├── auth/
│   ├── payments/
│   ├── utils/
│   └── types/
└── types/
```

### Supabase Client 사용법
```typescript
// 클라이언트 컴포넌트에서
import { createClient } from '@/lib/supabase/client'

// 서버 컴포넌트/API에서
import { createClient } from '@/lib/supabase/server'
```

### 네이밍 컨벤션
- 컴포넌트: PascalCase (UserProfile.tsx)
- 파일명: kebab-case (user-profile.tsx)
- 함수: camelCase (getUserProfile)
- 상수: UPPER_SNAKE_CASE (MAX_FILE_SIZE)

### 타입 정의
- 모든 컴포넌트에 props 타입 정의
- Zod 스키마를 통한 런타임 검증
- `/types` 디렉토리에서 중앙 집중 관리
- Database 타입은 Supabase CLI로 자동 생성

### 라이브러리 함수 구조 (/lib)
```
lib/
├── supabase/          # Supabase 클라이언트
├── database/          # DB 쿼리 함수들
│   ├── programs.ts    # 프로그램 관련 쿼리
│   ├── users.ts       # 사용자 관련 쿼리
│   ├── payments.ts    # 결제 관련 쿼리
│   └── subscriptions.ts # 구독 관련 쿼리
├── auth/              # 인증 관련 함수
├── payments/          # TossPayments 통합
├── utils/             # 유틸리티 함수
└── types/             # 공통 타입 정의
```

### 컴포넌트 작성 규칙
1. 기본 import 순서: React → Third-party → Internal → Types
2. Shadcn/ui 컴포넌트 우선 사용
3. 접근성(a11y) 고려사항 포함
4. 반응형 디자인 필수
5. Supabase 클라이언트는 서버/클라이언트 구분하여 사용

### 브랜드 가이드라인
- **메인 컬러**: #56007C (어두운 보라색)
- **보조 컬러**: White, Light Gray, Dark Gray
- **디자인 철학**: Modern & Clean, Professional, Approachable

## MCP (Model Context Protocol) 사용

### 🔧 활용 가능한 MCP 도구 목록

#### 1. **Supabase MCP** ⭐ 핵심
```bash
# 데이터베이스 관리
/mcp:supabase list-tables
/mcp:supabase execute-sql "SELECT * FROM programs WHERE status = 'active'"
/mcp:supabase generate-typescript-types
/mcp:supabase apply-migration "migration_name"

# 프로젝트 관리
/mcp:supabase list-projects
/mcp:supabase get-project [project_id]
/mcp:supabase create-branch [name]
/mcp:supabase get-advisors [project_id] security
```

#### 2. **TossPayments Integration Guide MCP** 🚀 NEW!
```bash
# V2 결제 위젯 (권장)
/mcp:tosspayments-integration-guide get-v2-documents {"keywords": ["결제위젯", "연동"]}

# V1 레거시 (필요시만)
/mcp:tosspayments-integration-guide get-v1-documents {"keywords": ["카드", "결제", "flow"]}

# 실제 사용 예시
/mcp:tosspayments-integration-guide get-v2-documents {"keywords": ["카드", "간편결제", "웹훅"]}
```

#### 3. **GitHub MCP** (코드 관리)
```bash
# 이슈 및 PR 관리
/mcp:github list-issues
/mcp:github create-issue
/mcp:github get-pull-request [pr_number]
/mcp:github create-branch [branch_name]

# 파일 관리
/mcp:github get-file-contents [owner] [repo] [path]
/mcp:github create-or-update-file [path] [content]
/mcp:github push-files [files]
```

### 🎯 추천 MCP 워크플로우

#### 개발 시작 시
```bash
# 1. DB 스키마 확인
/mcp:supabase list-tables

# 2. 타입 자동 생성
/mcp:supabase generate-typescript-types

# 3. TossPayments 가이드 확인
/mcp:tosspayments-integration-guide get-v2-documents {"keywords": ["결제위젯"]}
```

#### 디버깅 시
```bash
# 1. 보안 정책 확인
/mcp:supabase get-advisors [project_id] security

# 2. 로그 확인
/mcp:supabase get-logs [project_id] api

# 3. 성능 분석
/mcp:supabase execute-sql "EXPLAIN ANALYZE SELECT * FROM programs"
```

## ⚠️ **DB Schema 필수 참조** ⚠️

**모든 개발 과정에서 반드시 `specs/db-schema.md`를 참고하세요!**

### 🎯 핵심 참고사항

#### 1. **테이블 구조** (397줄 완전 스키마)
- **사용자**: `profiles`, `program_participants`, `wishlists`
- **프로그램**: `programs`, `program_categories`  
- **구독**: `subscription_plans`, `user_subscriptions`
- **결제**: `payments`, `refunds`
- **시스템**: `inquiries`, `notifications`, `site_settings`

#### 2. **RLS 정책** (보안 핵심)
```sql
-- 프로필 접근 정책
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);

-- 결제 접근 정책  
CREATE POLICY "Users can view own payments" ON payments FOR SELECT USING (auth.uid() = user_id);
```

#### 3. **인덱스 구조** (성능 최적화)
```sql
CREATE INDEX idx_programs_category ON programs(category_id);
CREATE INDEX idx_participants_user ON program_participants(user_id);
CREATE INDEX idx_payments_user ON payments(user_id);
```

#### 4. **트리거 함수** (자동 업데이트)
```sql
-- 프로그램 참가자 수 자동 업데이트
CREATE TRIGGER trigger_update_participant_count
    AFTER INSERT OR UPDATE OR DELETE ON program_participants
    FOR EACH ROW EXECUTE FUNCTION update_program_participant_count();
```

#### 5. **제약 조건** (데이터 무결성)
```sql
-- 프로그램 상태 체크
CHECK (status IN ('open', 'full', 'cancelled', 'completed'))

-- 결제 상태 체크
CHECK (status IN ('pending', 'completed', 'failed', 'cancelled', 'refunded'))
```

### 📋 **개발 시 필수 체크리스트**

#### ✅ 코드 작성 전
- [ ] `specs/db-schema.md` 해당 테이블 구조 확인
- [ ] RLS 정책 권한 범위 확인  
- [ ] 인덱스 활용 가능한 쿼리 설계
- [ ] 트리거 함수 동작 이해

#### ✅ 함수 구현 시
- [ ] Database 타입 활용 (`Database['public']['Tables']`)
- [ ] 에러 처리 한국어 메시지
- [ ] RLS 정책 준수하는 쿼리 작성
- [ ] 트랜잭션 필요 시 적절히 적용

#### ✅ 테스트 전
- [ ] MCP로 실제 데이터 확인
- [ ] RLS 정책 테스트
- [ ] 성능 영향 분석

### Supabase MCP 활용
- **데이터베이스 관리**: Supabase MCP를 통한 스키마 관리
- **쿼리 실행**: 복잡한 데이터베이스 쿼리 자동 생성
- **마이그레이션**: 스키마 변경사항 자동 적용
- **RLS 정책**: Row Level Security 자동 관리

### MCP 명령어 예시
```bash
# 테이블 생성
/mcp:supabase create-table programs

# 데이터 조회
/mcp:supabase query "SELECT * FROM programs WHERE status = 'active'"

# RLS 정책 적용
/mcp:supabase enable-rls profiles
```

## 성능 최적화
- 이미지: WebP format, lazy loading
- 코드 분할: dynamic imports
- 캐싱: Supabase built-in caching + TanStack Query
- **데이터베이스**: 인덱스 최적화 (이미 적용)

## 보안 요구사항
- Row Level Security (RLS) 적용 (이미 스키마에 포함)
- 입력값 검증 (Zod)
- 환경변수 보안 관리
- HTTPS 필수
- **Supabase Auth**: JWT 기반 안전한 인증

## 테스트 전략
- 단위 테스트: Jest + Testing Library
- E2E 테스트: Playwright
- 컴포넌트 테스트: Storybook
- **DB 테스트**: Supabase 로컬 개발 환경

## 배포 및 CI/CD
- 개발: Vercel Preview + Supabase Preview
- 프로덕션: Vercel + Supabase Production
- 자동 배포: GitHub Actions

## Infinite Agent Loop 활용
- 페이지 자동 생성: `/project:create-page`
- 컴포넌트 생성: `/project:create-component`
- Supabase 함수 생성: `/project:create-supabase`
- 타입 정의 생성: `/project:create-types`

### 참고 레포지토리
- **Infinite Agentic Loop**: https://github.com/rungchan2/infinite-agentic-loop
- 검증된 패턴 및 구조 참고

@~/.claude/monster-coop-personal.md