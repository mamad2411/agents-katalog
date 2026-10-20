# Claude Agent 지침 (AGENTS.md)

## ⚠️ Next.js 16 Breaking Changes

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. **ALWAYS** read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

### 주요 변경사항

#### 1. React 19 및 컴포넌트 구조
- **기본값**: Server Components (더 빠르고 안전)
- **명시 필요**: `'use client'` 디렉티브 (클라이언트 전용 코드)
- **React.FC 제거**: 함수 컴포넌트의 반환 타입은 `React.ReactNode` 사용

#### 2. Next.js 16 App Router 특징
- `app/` 디렉토리 기반 파일 라우팅
- Layout 컴포넌트로 UI 계층 구조 관리
- Route Groups: `(auth)`, `(dashboard)` 등으로 라우트 분류

#### 3. Server Actions 및 보안
- **Server Actions**: 'use server' 디렉티브로 서버 함수 표시
- **직접 DB 접근**: 클라이언트에서 DB 직접 접근 불가 (RLS 필수)
- **권한 검증**: 항상 Server Actions에서 user 검증

#### 4. 데이터 페칭 패턴
- **비추천**: getServerSideProps, getStaticProps (구형)
- **권장**: Server Components에서 async/await
- **클라이언트 데이터**: TanStack Query (React Query) 사용

---

## 코딩 규칙

### Server Components vs Client Components

#### Server Components (권장)
```typescript
// ✅ 기본값, DB 접근 가능
export default async function Page() {
  const data = await fetchData() // Direct DB or API
  return <div>{data}</div>
}
```

#### Client Components (필요할 때만)
```typescript
// ❌ 필요한 경우만 사용
'use client'

import { useEffect, useState } from 'react'
export function MyComponent() {
  const [data, setData] = useState(null)
  // useEffect, useState, hooks 사용
  return <div>{data}</div>
}
```

### 타입 정의

```typescript
// ✅ interface 우선 (Supabase 타입)
interface Album {
  id: string
  family_id: string
  name: string
  created_at: string
}

// 🔄 type도 가능 (스키마, union types)
type Role = 'owner' | 'member'
```

### Error Handling

```typescript
// ✅ Server Actions에서
export async function createAlbum(input: AlbumCreateInput) {
  try {
    const { data, error } = await supabase.from('albums').insert([input])
    if (error) {
      console.error('앨범 생성 실패:', error)
      throw new Error('앨범을 생성할 수 없습니다')
    }
    return data
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : '알 수 없는 오류'
    console.error('오류:', message)
    throw new Error(message)
  }
}
```

---

## 파일 구조 및 경로

### Path Alias 사용
```typescript
// ✅ 권장
import { createFamily } from '@/lib/actions/family.actions'
import type { Album } from '@/types/album'

// ❌ 상대 경로
import { createFamily } from '../../../lib/actions/family.actions'
```

### 디렉토리 네이밍
- `app/` - 라우트 및 레이아웃
- `components/` - UI 컴포넌트 (폴더로 분류)
- `lib/` - 로직 함수
  - `actions/` - Server Actions
  - `queries/` - 데이터 조회 (서버)
  - `supabase/` - DB 클라이언트
- `hooks/` - 커스텀 React 훅
- `types/` - TypeScript 타입 정의
- `schemas/` - Zod 스키마

---

## 의존성 및 라이브러리

### TanStack Query (React Query) 패턴

```typescript
// ✅ 쿼리 (조회)
export function useAlbums(familyId: string) {
  return useQuery({
    queryKey: ['albums', familyId],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('albums')
        .select('*')
        .eq('family_id', familyId)
      if (error) throw error
      return data as Album[]
    },
    enabled: !!familyId,
  })
}

// ✅ 뮤테이션 (변조)
export function useCreateAlbum() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (input: AlbumCreateInput) => {
      const { data, error } = await supabase
        .from('albums')
        .insert([input])
      if (error) throw error
      return data[0] as Album
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['albums'] })
    },
  })
}
```

### Zod 스키마 패턴

```typescript
// ✅ 스키마 정의
export const albumSchema = z.object({
  name: z.string().min(1, '앨범명은 필수입니다'),
  description: z.string().optional(),
})

export type AlbumCreateInput = z.infer<typeof albumSchema>

// ✅ React Hook Form 연결
const form = useForm<AlbumCreateInput>({
  resolver: zodResolver(albumSchema),
})
```

---

## 권한 및 보안

### Supabase 권한 검증 패턴

```typescript
// ✅ Server Actions에서 항상 검증
export async function updateFamily(input: { familyId: string; name: string }) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user) throw new Error('인증 필요')
  
  // 권한 검증 (owner 확인)
  const { data: member } = await supabase
    .from('family_members')
    .select('role')
    .eq('family_id', input.familyId)
    .eq('user_id', user.id)
    .single()
  
  if (member?.role !== 'owner') {
    throw new Error('권한이 없습니다')
  }
  
  // 실제 업데이트
  const { error } = await supabase
    .from('families')
    .update({ name: input.name })
    .eq('id', input.familyId)
  
  if (error) throw new Error('업데이트 실패')
}
```

### Magic Link 인증 (Supabase)

```typescript
// ✅ 로그인
const { error } = await supabase.auth.signInWithOtp({
  email: userEmail,
  options: {
    emailRedirectTo: `${baseUrl}/auth/callback?next=/dashboard`,
    shouldCreateUser: true,
  },
})

// ✅ 로그아웃
const { error } = await supabase.auth.signOut()
```

---

## 성능 최적화

### 이미지 최적화 (Next.js Image)
```typescript
// ✅ 권장
import Image from 'next/image'
<Image
  src={photoUrl}
  alt="사진"
  width={300}
  height={300}
  priority={false}
/>

// ❌ HTML img 태그
<img src={photoUrl} alt="사진" />
```

### 동적 import (Code Splitting)
```typescript
// ✅ 대용량 컴포넌트
const HeavyModal = dynamic(() => import('@/components/HeavyModal'), {
  loading: () => <div>로딩 중...</div>,
})
```

---

## 테스트 및 디버깅

### Console 로깅
```typescript
// ✅ 에러만 로깅
console.error('데이터베이스 오류:', error)
console.error('서버 액션 실패:', errorMessage)

// ⚠️ 개발 중에만 (프로덕션에서 제거)
console.log('디버그:', data)
```

---

## 일반적인 실수 & 해결법

| 실수 | 원인 | 해결 |
|------|------|------|
| "Cannot access DB from Client" | 클라이언트에서 DB 직접 접근 | Server Actions 사용 |
| RLS 오류 (401/403) | 권한 정책 누락 | Supabase RLS 정책 확인 |
| 쿼리 캐시 안 업데이트됨 | invalidateQueries 빼먹음 | onSuccess에서 캐시 무효화 |
| 타입 불일치 | Supabase 스키마와 차이 | types/ 동기화 |

---

## Commit Message Convention

**한국어로 작성**, 명확한 제목:

```
feat: [기능명] 설명
fix: [파일명] 버그 설명
refactor: [영역] 리팩토링 목표
docs: 문서 업데이트
```

예:
```
feat: 가족 멤버 관리 권한 체크 완화
fix: 새로고침할 때마다 가족이 자동으로 생성되는 문제 해결
refactor: Server Actions 에러 처리 통일
```

---

## 유용한 Next.js 16 문서

- [App Router 마이그레이션](https://nextjs.org/docs/app)
- [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions)
- [Dynamic Routes](https://nextjs.org/docs/app/building-your-application/routing/dynamic-routes)
- [Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)