---
name: enhancement-guide
description: SaaS 수정 및 고도화 가이드 - 기능 추가, 성능 개선, 확장 방법
---

# SaaS 수정 및 고도화 가이드

처음 만든 SaaS를 더 좋게 만들고 싶으신가요? 이 가이드를 따라하세요!

---

## 목차

1. [코드 수정하기](#1-코드-수정하기)
2. [새 기능 추가하기](#2-새-기능-추가하기)
3. [디자인 변경하기](#3-디자인-변경하기)
4. [성능 개선하기](#4-성능-개선하기)
5. [확장하기 (스케일링)](#5-확장하기-스케일링)
6. [보안 강화하기](#6-보안-강화하기)
7. [유지보수 가이드](#7-유지보수-가이드)

---

## 1. 코드 수정하기

### 1.1 수정 전 준비사항

```
⚠️ 중요: 코드를 수정하기 전에 항상 백업하세요!

방법 1: Git으로 백업 (권장)
┌─────────────────────────────────────────┐
│ git add .                               │
│ git commit -m "수정 전 백업"              │
└─────────────────────────────────────────┘

방법 2: 새 브랜치 만들기 (더 안전)
┌─────────────────────────────────────────┐
│ git checkout -b feature/새기능이름        │
└─────────────────────────────────────────┘
```

### 1.2 파일 찾기

```
📁 어디를 수정해야 할까요?

┌─────────────────────────────────────────────────────────┐
│ 수정하고 싶은 것          │  찾아야 할 파일              │
├─────────────────────────────────────────────────────────┤
│ 홈페이지 내용             │  src/app/page.tsx           │
│ 로그인 페이지             │  src/app/(auth)/login/      │
│ 대시보드                  │  src/app/(dashboard)/       │
│ 가격 페이지               │  src/app/pricing/           │
│ 버튼, 카드 등 UI          │  src/components/ui/         │
│ 색상, 폰트                │  tailwind.config.js         │
│ API 로직                  │  src/app/api/               │
│ 데이터베이스 연결          │  src/lib/db.ts              │
│ 환경 변수                 │  .env.local                 │
└─────────────────────────────────────────────────────────┘
```

### 1.3 텍스트 수정하기

```tsx
// 예시: 홈페이지 제목 변경하기

// 📂 src/app/page.tsx 열기

// 변경 전:
<h1>Welcome to My SaaS</h1>

// 변경 후:
<h1>나만의 멋진 서비스</h1>

// 💾 저장 (Ctrl+S 또는 Cmd+S)
// 🔄 브라우저에서 자동으로 변경사항 확인!
```

### 1.4 색상 변경하기

```javascript
// 📂 tailwind.config.js

module.exports = {
  theme: {
    extend: {
      colors: {
        // 브랜드 색상 변경
        primary: {
          50: '#eff6ff',   // 가장 밝은 색
          500: '#3b82f6',  // 기본 색
          600: '#2563eb',  // 호버 색
          900: '#1e3a8a',  // 가장 어두운 색
        },
        // 새 색상 추가
        brand: '#FF6B6B',
      },
    },
  },
}

// 사용법:
// <button className="bg-primary-500 hover:bg-primary-600">
// <div className="text-brand">
```

### 1.5 수정 후 확인하기

```
수정 후 체크리스트:

□ 1. 개발 서버에서 확인
     npm run dev
     → http://localhost:3000 에서 확인

□ 2. 에러 확인
     터미널에 빨간 글씨가 있나요?
     브라우저 콘솔(F12)에 에러가 있나요?

□ 3. 빌드 테스트
     npm run build
     → 에러 없이 완료되어야 함

□ 4. 변경사항 저장
     git add .
     git commit -m "설명: 무엇을 변경했는지"
```

---

## 2. 새 기능 추가하기

### 2.1 새 페이지 추가하기

```
📁 새 페이지 만드는 법 (Next.js App Router)

예시: /about 페이지 추가

1단계: 폴더 만들기
┌─────────────────────────────────────────┐
│ src/app/about/                          │
│   └── page.tsx    ← 이 파일 생성        │
└─────────────────────────────────────────┘

2단계: 코드 작성
```

```tsx
// 📂 src/app/about/page.tsx

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold">회사 소개</h1>
      <p className="mt-4">
        우리는 최고의 서비스를 제공합니다.
      </p>
    </div>
  );
}
```

```
3단계: 확인
→ http://localhost:3000/about 접속
```

### 2.2 새 API 추가하기

```
📁 새 API 만드는 법

예시: /api/contact API 추가

1단계: 폴더 만들기
┌─────────────────────────────────────────┐
│ src/app/api/contact/                    │
│   └── route.ts    ← 이 파일 생성        │
└─────────────────────────────────────────┘
```

```typescript
// 📂 src/app/api/contact/route.ts

import { NextResponse } from 'next/server';

// POST /api/contact
export async function POST(request: Request) {
  try {
    // 1. 요청 데이터 받기
    const body = await request.json();
    const { name, email, message } = body;

    // 2. 유효성 검사
    if (!name || !email || !message) {
      return NextResponse.json(
        { error: '모든 필드를 입력해주세요' },
        { status: 400 }
      );
    }

    // 3. 데이터 처리 (예: DB 저장, 이메일 발송)
    console.log('문의 접수:', { name, email, message });

    // 4. 성공 응답
    return NextResponse.json({
      success: true,
      message: '문의가 접수되었습니다'
    });

  } catch (error) {
    return NextResponse.json(
      { error: '서버 오류가 발생했습니다' },
      { status: 500 }
    );
  }
}
```

### 2.3 새 컴포넌트 추가하기

```
📁 새 컴포넌트 만드는 법

예시: 알림 배너 컴포넌트

1단계: 파일 만들기
┌─────────────────────────────────────────┐
│ src/components/ui/Banner.tsx            │
└─────────────────────────────────────────┘
```

```tsx
// 📂 src/components/ui/Banner.tsx

interface BannerProps {
  message: string;
  type?: 'info' | 'success' | 'warning' | 'error';
  onClose?: () => void;
}

export function Banner({ message, type = 'info', onClose }: BannerProps) {
  const colors = {
    info: 'bg-blue-100 text-blue-800 border-blue-200',
    success: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    error: 'bg-red-100 text-red-800 border-red-200',
  };

  return (
    <div className={`p-4 rounded-lg border ${colors[type]} flex justify-between items-center`}>
      <span>{message}</span>
      {onClose && (
        <button onClick={onClose} className="ml-4 text-xl">
          ×
        </button>
      )}
    </div>
  );
}

// 사용법:
// import { Banner } from '@/components/ui/Banner';
// <Banner message="환영합니다!" type="success" />
```

### 2.4 새 기능 추가 체크리스트

```
새 기능 추가 시 확인사항:

□ 새 브랜치에서 작업하기
  git checkout -b feature/기능이름

□ 필요한 패키지 설치
  npm install 패키지이름

□ 환경 변수 필요하면 .env.local에 추가
  NEW_API_KEY=값

□ 타입 정의 (TypeScript)
  interface, type 추가

□ 에러 처리 추가
  try-catch, 에러 메시지

□ 테스트
  npm run dev로 확인

□ 빌드 확인
  npm run build

□ 커밋 & 푸시
  git add .
  git commit -m "feat: 새 기능 설명"
  git push origin feature/기능이름

□ PR(Pull Request) 생성
  GitHub에서 main 브랜치로 PR 생성
```

---

## 3. 디자인 변경하기

### 3.1 레이아웃 변경

```tsx
// 📂 src/app/(dashboard)/layout.tsx

// 사이드바 너비 변경
<aside className="w-64">  {/* 64 = 16rem = 256px */}
  {/* w-48 = 192px, w-72 = 288px, w-80 = 320px */}
</aside>

// 헤더 높이 변경
<header className="h-16">  {/* 16 = 4rem = 64px */}
  {/* h-14 = 56px, h-20 = 80px */}
</header>
```

### 3.2 반응형 디자인

```tsx
// Tailwind 반응형 접두사
// sm: 640px 이상
// md: 768px 이상
// lg: 1024px 이상
// xl: 1280px 이상

// 예시: 모바일에서 1열, 태블릿에서 2열, 데스크톱에서 3열
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>카드 1</div>
  <div>카드 2</div><div>카드 3</div>
</div>

// 예시: 모바일에서 숨기기
<div className="hidden md:block">
  데스크톱에서만 보임
</div>

// 예시: 모바일에서만 보이기
<div className="block md:hidden">
  모바일에서만 보임
</div>
```

### 3.3 다크 모드 추가

```tsx
// 1단계: tailwind.config.js 설정
module.exports = {
  darkMode: 'class', // 또는 'media' (시스템 설정 따름)
  // ...
}

// 2단계: 다크 모드 스타일 적용
<div className="bg-white dark:bg-gray-900 text-black dark:text-white">
  콘텐츠
</div>

// 3단계: 토글 버튼 만들기
'use client';
import { useState, useEffect } from 'react';

export function DarkModeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // 저장된 설정 불러오기
    const saved = localStorage.getItem('darde');
    if (saved === 'true') {
      setIsDark(true);
      document.documentElement.classList.add('dark');
    }
  }, []);

  const toggle = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', (!isDark).toString());
  };

  return (
    <button onClick={toggle}>
      {isDark ? '🌙' : '☀️'}
    </button>
  );
}
```

### 3.4 애니메이션 추가

```tsx
// Tailwind 기본 애니메이션
<div className="animate-spin">회전</div>
<div className="animate-ping">핑</div>
<div className="animate-pulse">깜빡</div>
<div className="animate-bounce">튕김</div>

// 호버 효과
<button className="transition-all duration-300 hover:scale-105 hover:shadow-lg">
  버튼
</button>

// 페이드 인 효과 (커스텀)
// tailwind.config.js에 추가:
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
}

// 사용: <div className="animate-fade-in">
```

---

## 4. 성능 개선하기

### 4.1 이미지 최적화

```tsx
// ❌ 느림
<img src="/large-image.png" alt="이미지" />

// ✅ 빠름 - Next.js Image 사용
import Image from 'next/image';

<Image
  src="/large-image.png"
  alt="이미지"
  width={800}
  height={600}
  priority        // 중요한 이미지는 먼저 로드
  placeholder="blur"  // 로딩 중 블러 효과
/>
```

### 4.2 코드 분할 (Code Splitting)

```tsx
// ❌ 모든 컴포넌트를 한번에 로드
import HeavyChart from '@/components/HeavyChart';

// ✅ 필요할 때만 로드 (동적 임포트)
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(
  () => import('@/components/HeavyChart'),
  {
    loading: () => <p>차트 로딩 중...</p>,
    ssr: false  // 서버에서는 렌더링 안 함
  }
);
```

### 4.3 캐싱 활용

```typescript
// API 응답 캐싱
// 📂 src/app/api/data/route.ts

export async function GET() {
  const data = await fetchData();

  return new Response(JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=30',
      // 60초 동안 캐시, 이후 30초 동안 stale 데이터 제공하며 재검증
    },
  });
}

// 클라이언트 캐싱 (React Query / SWR)
import useSWR from 'swr';

function Dashboard() {
  const { data, error, isLoading } = useSWR('/api/data', fetcher, {
    revalidateOnFocus: false,  // 탭 전환 시 재요청 안 함
    dedupingInterval: 60000,   // 1분 동안 중복 요청 방지
  });
}
```

### 4.4 데이터베이스 최적화

```typescript
// ❌ 느림 - N+1 문제
const users = await db.user.findMany();
for (const user of users) {
  const posts = await db.post.findMany({ where: { userId: user.id } });
}

// ✅ 빠름 - 한 번에 조회
const users = await db.user.findMany({
  include: {
    posts: true,  // 관계 데이터 함께 조회
  },
});

// ✅ 더 빠름 - 필요한 필드만 선택
const users = await db.user.findMany({
  select: {
    id: true,
    name: true,
    posts: {
      select: {
        title: true,
      },
      take: 5,  // 최근 5개만
    },
  },
});

// 인덱스 추가 (schema.prisma)
model Post {
  id        String   @id
  title     String
  userId    String
  createdAt DateTime @default(now())

  @@index([userId])           // 사용자별 조회 최적화
  @@index([createdAt(sort: Desc)])  // 최신순 조회 최적화
}
```

### 4.5 성능 측정하기

```
📊 성능 측정 도구

1. Lighthouse (브라우저 내장)
   → Chrome DevTools > Lighthouse 탭
   → "Analyze page load" 클릭

2. Vercel Analytics (배포 후)
   → npm install @vercel/analytics
   → 대시보드에서 실시간 성능 확인

3. Web Vitals
   → LCP (Largest Contentful Paint): 2.5초 이하
   → FID (First Input Delay): 100ms 이하
   → CLS (Cumulative Layout Shift): 0.1 이하

권장 점수:
┌─────────────────────────────────────────┐
│ 항목         │ 최소  │ 권장  │ 최고    │
├─────────────────────────────────────────┤
│ Performance  │  70   │  85   │  95+    │
│ Accessibility│  80   │  90   │  100    │
│ Best Practice│  80   │  90   │  100    │
│ SEO          │  80   │  90   │  100    │
└─────────────────────────────────────────┘
```

---

## 5. 확장하기 (스케일링)

### 5.1 사용자 증가 대응

```
📈 사용자 규모별 권장 구성

┌─────────────────────────────────────────────────────────────┐
│ 사용자 수    │ 권장 구성                                     │
├─────────────────────────────────────────────────────────────┤
│ ~100명       │ Vercel (무료) + Supabase (무료)              │
│ ~1,000명     │ Vercel Pro + Supabase Pro                    │
│ ~10,000명    │ + Redis 캐시 + CDN                           │
│ ~100,000명   │ + 로드밸런서 + DB 읽기 복제본                 │
│ 100,000명+   │ AWS/GCP + 마이크로서비스                      │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 캐시 레이어 추가 (Redis)

```typescript
// Redis 설치
// npm install ioredis

// 📂 src/lib/redis.ts
import Redis from 'ioredis';

export const redis = new Redis(process.env.REDIS_URL!);

// 캐시 유틸리티
export async function getOrSetCache<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 3600  // 1시간
): Promise<T> {
  // 캐시에서 찾기
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached);
  }

  // 없으면 데이터 가져와서 캐시에 저장
  const data = await fetcher();
  await redis.setex(key, ttl, JSON.stringify(data));
  return data;
}

// 사용 예시
const user = await getOrSetCache(
  `user:${userId}`,
  () => db.user.findUnique({ where: { id: userId } }),
  3600  // 1시간 캐시
);
```

### 5.3 CDN 활용

```
🌐 CDN (ontent Delivery Network) 설정

Vercel 사용 시:
→ 자동으로 CDN 적용됨 (추가 설정 불필요)

Cloudflare 추가 시:
1. Cloudflare 가입 (무료)
2. 도메인 DNS를 Cloudflare로 변경
3. SSL/TLS → Full (strict) 선택
4. 캐싱 규칙 설정:
   - 정적 파일: 1개월
   - API: 캐시 안 함
```

### 5.4 백그라운드 작업 처리

```typescript
// 무거운 작업은 큐로 처리
// npm install bullmq

// 📂 src/lib/queue.ts
import { Queue, Worker } from 'bullmq';

const connection = {
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT!),
};

// 큐 생성
export const emailQueue = new Queue('email', { connection });

// 워커 생성 (백그라운드에서 실행)
const worker = new Worker('email', async (job) => {
  const { to, subject, body } = job.data;
  await sendEmail(to, subject, body);
}, { connection });

// 사용 예시 (즉시 반환, 나중에 처리)
await emailQueue.add('welcome', {
  to: user.email,
  subject: '가입을 환영합니다',
  body: '...',
});
```

---

## 6. 보안 강화하기

### 6.1 보안 체크리스트

```
🔒 필수 보안 체크리스트

인증/인가:
□ 비밀번호 해싱 (bcrypt/argon2)
□ JWT 토큰 만료 설정
□ 리프레시 토큰 구현
□ API 권한 검증
□ 세션 타임아웃

입력 검증:
□ 모든 사용자 입력 검증
□ SQL 인젝션 방지 (ORM 사용)
□ XSS 방지 (React 자동 이스케이프)
□ CSRF 토큰

환경 변수:
□ 민감 정보 .env.local에 저장
□ .gitignore에 .env* 추가
□ 프로덕션 환경 변수 분리

HTTPS:
□ SSL 인증서 적용
□ HTTP → HTTPS 리다이렉트
□ Secure 쿠키 사용

기타:
□ 에러 메시지에 민감 정보 노출 금지
□ Rate limiting 적용
□ 로깅 및 모니터링
```

### 6.2 Rate Limiting 추가

```typescript
// npm install @upstash/ratelimit @upstash/redis

// 📂 src/lib/ratelimit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL!,
  token: process.env.UPSTASH_REDIS_TOKEN!,
});

export const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, '60 s'), // 60초에 10번
});

// 📂 src/middleware.ts
import { ratelimit } from './lib/ratelimit';

export async function middleware(request: NextRequest) {
  const ip = request.ip ?? '127.0.0.1';
  const { success, limit, reset, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return new Response('Too Many Requests', {
      status: 429,
      headers: {
        'X-RateLimit-Limit': limit.toString(),
        'X-RateLimit-Remaining': remaining.toString(),
        'X-RateLimit-Reset': reset.toString(),
      },
    });
  }
}
```

### 6.3 입력 검증

```typescript
// npm install zod

// 📂 src/lib/validations.ts
import { z } from 'zod';

export const userSchema = z.object({
  email: z.string().email('유효한 이메일을 입력하세요'),
  password: z.string()
    .min(8, '비밀번호는 8자 이상이어야 합니다')
    .regex(/[A-Z]/, '대문자를 포함해야 합니다')
    .regex(/[0-9]/, '숫자를 포함해야 합니다'),
  name: z.string().min(2, '이름은 2자 이상이어야 합니다'),
});

// API에서 사용
export async function POST(request: Request) {
  const body = await request.json();

  const result = userSchema.safeParse(body);
  if (!result.success) {
    return NextResponse.json(
      { errors: result.error.flatten().fieldErrors },
      { status: 400 }
    );
  }

  // 검증된 데이터 사용
  const { email, password, name } = result.data;
}
```

---

## 7. 유지보수 가이드

### 7.1 정기 업데이트

```
📅 주기별 체크리스트

매주:
□ npm audit으로 보안 취약점 확인
  npm audit
  npm audit fix

매월:
□ 의존성 업데이트
  npm outdated          # 업데이트 가능한 패키지 확인
  npm update            # 마이너 버전 업데이트
  npx npm-check-updates # 메이저 버전 확인

분기별:
□ Next.js 버전 업그레이드
□ 사용하지 않는 패키지 제거
□ 코드 정리 및 리팩토링
□ 성능 측정 및 개선

연간:
□ 기술 스택 검토
□ 아키텍처 재평가
□ 보안 감사
```

### 7.2 의존성 업데이트

```bash
# 1. 현재 상태 확인
npm outdated

# 2. 마이너 버전 안전하게 업데이트
npm update

# 3. 메이저 버전 확인 (주의 필요)
npx npm-check-updates

# 4. 특정 패키지만 업데이트
npm install next@latest

# 5. 모든 패키지 최신 버전으로 (위험할 수 있음)
npx npm-check-updates -u
npm install

# 6. 업데이트 후 테스트
npm run build
npm run test
```

### 7.3 모니터링 설정

```typescript
// Sentry 에러 모니터링
// npm install @sentry/nextjs

// 📂 sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
});

// 📂 src/app/error.tsx
'use client';
import * as Sentry from '@sentry/nextjs';
import { useEffect } from 'react';

export default function Error({ error, reset }) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <div>
      <h2>문제가 발생했습니다</h2>
      <button onClick={reset}>다시 시도</button>
    </div>
  );
}
```

### 7.4 백업 전략

```
💾 백업 체크리스트

코드:
✓ GitHub에 자동 백업됨
✓ 브랜치 보호 규칙 설정
✓ 태그로 릴리스 관리

데이터베이스:
□ Supabase: 자동 일일 백업 (Pro 플랜)
□ 수동 백업: pg_dump 사용
□ 다른 리전에 복제본 유지

환경 변수:
□ 안전한 곳에 .env 백업
□ 1Password / Bitwarden 사용 권장
□ 팀원과 안전하게 공유

미디어 파일:
□ 클라우드 스토리지 백업
□ CDN 원본 보관
```

### 7.5 문서화

```
📝 문서화 권장 사항

README.md:
- 프로젝트 소개
- 설치 방법
- 환경 변수 목록
- 실행 방법

CHANGELOG.md:
- 버전별 변경사항
- 날짜와 함께 기록

docs/:
- API 문서
- 아키텍처 설명
- 배포 가이드

코드 주석:
- 복잡한 로직에만 주석
- WHY를 설명 (WHAT 아님)
- JSDoc으로 함수 설명
```

---

## 자주 묻는 질문 (FAQ)

### Q: 수정했는데 변경이 안 보여요
```
해결 방법:
1. 파일을 저장했는지 확인 (Ctrl+S / Cmd+S)
2. 개발 서버 재시작: Ctrl+C → npm run dev
3. 브라우저 캐시 삭제: Ctrl+Shift+R
4. .next 폴더 삭제 후 재시작:
   rm -rf .next
   npm run dev
```

### Q: 빌드 에러가 나요
```
해결 방법:
1. 에러 메시지 자세히 읽기
2. 에러가 발생한 파일과 줄 번호 확인
3. 최근 변경사항 되돌리기:
   git checkout -- 파일명
4. node_modules 재설치:
   rm -rf node_modules
   npm install
5. TypeScript 에러면 타입 확인
```

### Q: 배포 후 에러가 나요
```
해결 방법:
1. Vercel 대시보드에서 로그 확인
2. 환경 변수가 설정되었는지 확인
3. 로컬에서 빌드 테스트:
   npm run build
4. 빌드 로그에서 경고 메시지 확인
5. 이전 배포로 롤백:
   Vercel 대시보드 → Deployments → ... → Rollback
```

### Q: 데이터가 안 보여요
```
해결 방법:
1. 브라우저 개발자 도구 (F12) → Network 탭
2. API 요청이 성공했는지 확인 (200 OK)
3. Console 탭에서 에러 확인
4. 환경 변수 (API 키 등) 확인
5. 데이터베이스 연결 확인
```

---

## 도움 받기

```
🆘 막히면 이렇게 해보세요!

1. 에러 메시지 구글링
   → "Next.js [에러 메시지]" 검색

2. 공식 문서 확인
   → Next.js: https://nextjs.org/docs
   → Supabase: https://supabase.com/docs
   → Tailwind: https://tailwindcss.com/docs

3. Claude에게 물어보기
   → 에러 메시지와 코드를 함께 보여주세요
   → "이 에러가 왜 나는지 설명해줘"

4. 커뮤니티
   → GitHub Issues
   → Stack Overflow
   → Discord 채널
```

---

축하합니다! 이제 SaaS를 수정하고 발전시킬 수 있습니다! 🎉
