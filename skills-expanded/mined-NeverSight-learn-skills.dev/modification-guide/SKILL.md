---
name: modification-guide
description: SaaS 수정 및 업데이트 가이드 - 코드 변경, 기능 추가, 유지보수
triggers:
  - modify
  - 수정
  - update
  - 업데이트
  - 유지보수
---

# SaaS 수정 및 업데이트 가이드

> 프로덕션 SaaS 코드 수정, 기능 추가, 유지보수 완벽 가이드

---

## 1. 코드 수정 워크플로우

### 1.1 기본 수정 프로세스

```
┌─────────────────────────────────────────────────────────────┐
│ 🔄 코드 수정 워크플로우                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 이슈 확인/생성                                           │
│     ↓                                                        │
│  2. 브랜치 생성 (feature/fix-xxx)                           │
│     ↓                                                        │
│  3. 코드 수정                                                │
│     ↓                                                        │
│  4. 로컬 테스트                                              │
│     ↓                                                        │
│  5. PR 생성                                                  │
│     ↓                                                        │
│  6. 코드 리뷰                                                │
│     ↓                                                        │
│  7. 스테이징 배포 & 테스트                                   │
│     ↓                                                        │
│  8. 프로덕션 배포                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Git 브랜치 전략

```bash
# 브랜치 명명 규칙
main              # 프로덕션
├── develop       # 개발 통합
├── feature/xxx   # 새 기능
├── fix/xxx       # 버그 수정
├── hotfix/xxx    # 긴급 수정
└── release/x.x.x # 릴리즈 준비

# 새 기능 브랜치 생성
git checkout develop
git pull origin develop
git checkout -b feature/add-dark-mode

# 작업 완료 후
git add .
git commit -m "feat: add dark mode toggle"
git push origin feature/add-dark-mode
```

### 1.3 커밋 메시지 컨벤션

```bash
# 형식: <type>(<scope>): <description>

# Types
feat:     새 기능
fix:      버그 수정
docs:     문서 수정
style:    코드 포맷팅 (기능 변경 없음)
refactor: 리팩토링
perf:     성능 개선
test:     테스트
chore:    빌드/도구 설정

# 예시
git commit -m "feat(auth): add Google OAuth login"
git commit -m "fix(payment): handle Stripe webhook timeout"
git commit -m "docs(readme): update installation steps"
git commit -m "refactor(api): simplify user validation logic"
```

---

## 2. UI 수정

### 2.1 색상 변경

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  theme: {
    extend: {
      colors: {
        // 브랜드 색상 정의
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',  // 메인 색상
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          // ...
        },
      },
    },
  },
};

// 색상 사용
<button className="bg-primary-500 hover:bg-primary-600">
  버튼
</button>
```

### 2.2 레이아웃 변경

```typescript
// src/components/Layout.tsx
export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex">
      {/* 사이드바 너비 조절 */}
      <aside className="w-64 lg:w-72 xl:w-80">
        <Sidebar />
      </aside>

      {/* 메인 콘텐츠 영역 */}
      <main className="flex-1 p-4 lg:p-6 xl:p-8">
        {children}
      </main>
    </div>
  );
}
```

### 2.3 컴포넌트 스타일 오버라이드

```typescript
// src/components/ui/Button.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // 기본 스타일
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary-500 text-white hover:bg-primary-600',
        destructive: 'bg-red-500 text-white hover:bg-red-600',
        outline: 'border border-gray-300 bg-transparent hover:bg-gray-100',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        ghost: 'hover:bg-gray-100',
        link: 'text-primary-500 underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-8 px-3',
        lg: 'h-12 px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

// 사용 예시
<Button variant="outline" size="lg">큰 아웃라인 버튼</Button>
```

### 2.4 다크모드 추가

```typescript
// src/components/ThemeProvider.tsx
'use client';

import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      {children}
    </NextThemesProvider>
  );
}

// src/components/ThemeToggle.tsx
'use client';

import { useTheme } from 'next-themes';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    </button>
  );
}
```

```css
/* src/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    /* ... */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    /* ... */
  }
}
```

---

## 3. 기능 추가

### 3.1 새 API 엔드포인트 추가

```typescript
// src/app/api/products/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { z } from 'zod';

// 스키마 정의
const createProductSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  price: z.number().positive(),
});

// GET: 상품 목록
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') || '1');
  const limit = parseInt(searchParams.get('limit') || '20');

  const products = await prisma.product.findMany({
    take: limit,
    skip: (page - 1) * limit,
    orderBy: { createdAt: 'desc' },
  });

  const total = await prisma.product.count();

  return NextResponse.json({
    data: products,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit),
    },
  });
}

// POST: 상품 생성
export async function POST(request: NextRequest) {
  // 인증 확인
  const session = await getServerSession(authOptions);
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // 요청 파싱 및 검증
  const body = await request.json();
  const result = createProductSchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: result.error.issues },
      { status: 400 }
    );
  }

  // 생성
  const product = await prisma.product.create({
    data: {
      ...result.data,
      userId: session.user.id,
    },
  });

  return NextResponse.json(product, { status: 201 });
}
```

### 3.2 새 페이지 추가

```typescript
// src/app/products/page.tsx
import { Suspense } from 'react';
import { ProductList } from '@/components/ProductList';
import { ProductFilters } from '@/components/ProductFilters';
import { Skeleton } from '@/components/ui/Skeleton';

export const metadata = {
  title: '상품 목록',
  description: '모든 상품을 둘러보세요',
};

export default function ProductsPage({
  searchParams,
}: {
  searchParams: { category?: string; sort?: string };
}) {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-8">상품 목록</h1>

      <div className="flex gap-8">
        <aside className="w-64">
          <ProductFilters />
        </aside>

        <main className="flex-1">
          <Suspense fallback={<ProductListSkeleton />}>
            <ProductList
              category={searchParams.category}
              sort={searchParams.sort}
            />
          </Suspense>
        </main>
      </div>
    </div>
  );
}

function ProductListSkeleton() {
  return (
    <div className="grid grid-cols-3 gap-4">
      {Array.from({ length: 9 }).map((_, i) => (
        <Skeleton key={i} className="h-64 rounded-lg" />
      ))}
    </div>
  );
}
```

### 3.3 데이터베이스 마이그레이션

```bash
# 1. 스키마 수정
# prisma/schema.prisma

# 2. 마이그레이션 생성
npx prisma migrate dev --name add_products_table

# 3. 타입 생성
npx prisma generate

# 4. 프로덕션 적용
npx prisma migrate deploy
```

```prisma
// prisma/schema.prisma 예시
model Product {
  id          String   @id @default(cuid())
  name        String
  description String?
  price       Float
  images      String[]
  status      ProductStatus @default(DRAFT)
  userId      String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  user        User     @relation(fields: [userId], references: [id])
  categories  Category[]

  @@index([userId])
  @@index([status])
}

enum ProductStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}
```

---

## 4. 버그 수정

### 4.1 버그 분석 프로세스

```
┌─────────────────────────────────────────────────────────────┐
│ 🐛 버그 수정 프로세스                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 버그 재현                                                │
│     • 정확한 재현 스텝 확인                                  │
│     • 환경 정보 수집 (브라우저, OS 등)                       │
│                                                              │
│  2. 원인 분석                                                │
│     • 에러 로그 확인                                         │
│     • 관련 코드 추적                                         │
│     • 최근 변경사항 확인                                     │
│                                                              │
│  3. 수정                                                     │
│     • 최소한의 변경으로 수정                                 │
│     • 테스트 케이스 추가                                     │
│                                                              │
│  4. 검증                                                     │
│     • 원래 버그 해결 확인                                    │
│     • 사이드 이펙트 확인                                     │
│     • 회귀 테스트                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 에러 로그 확인

```typescript
// 프로덕션 에러 로깅
import * as Sentry from '@sentry/nextjs';

// 에러 캡처
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    tags: { component: 'PaymentForm' },
    extra: { userId, orderId },
  });
  throw error;
}

// Breadcrumb 추가
Sentry.addBreadcrumb({
  category: 'user-action',
  message: 'Clicked checkout button',
  level: 'info',
});
```

### 4.3 핫픽스 배포

```bash
# 1. 핫픽스 브랜치 생성 (main에서)
git checkout main
git pull origin main
git checkout -b hotfix/fix-payment-error

# 2. 수정 및 커밋
git add .
git commit -m "fix: resolve payment timeout issue"

# 3. main에 머지
git checkout main
git merge hotfix/fix-payment-error
git push origin main

# 4. develop에도 머지
git checkout develop
git merge hotfix/fix-payment-error
git push origin develop

# 5. 즉시 배포
vercel --prod
```

---

## 5. 의존성 업데이트

### 5.1 정기 업데이트

```bash
# 업데이트 가능한 패키지 확인
npm outdated

# 마이너/패치 업데이트 (안전)
npm update

# 특정 패키지 업데이트
npm update next@latest

# 메이저 버전 업데이트 (주의)
npm install next@15 react@19 react-dom@19

# 취약점 확인 및 수정
npm audit
npm audit fix
```

### 5.2 업데이트 후 테스트

```bash
# 전체 테스트 실행
npm run test

# 타입 체크
npm run type-check

# 빌드 테스트
npm run build

# E2E 테스트
npm run test:e2e
```

### 5.3 Breaking Changes 대응

```typescript
// 예: Next.js 14 → 15 마이그레이션

// Before (Next.js 14)
export async function getServerSideProps() {
  const data = await fetchData();
  return { props: { data } };
}

// After (Next.js 15 App Router)
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 },
  });
  return res.json();
}

export default async function Page() {
  const data = await getData();
  return <div>{/* ... */}</div>;
}
```

---

## 6. 성능 최적화

### 6.1 번들 분석

```bash
# 번들 분석기 설치
npm install @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // ...
});

# 분석 실행
ANALYZE=true npm run build
```

### 6.2 코드 스플리팅

```typescript
// 동적 임포트
import dynamic from 'next/dynamic';

// 무거운 컴포넌트 lazy loading
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});

// 조건부 로딩
const AdminPanel = dynamic(() => import('@/components/AdminPanel'), {
  loading: () => <p>Loading...</p>,
});

export default function Dashboard({ isAdmin }: { isAdmin: boolean }) {
  return (
    <div>
      <HeavyChart />
      {isAdmin && <AdminPanel />}
    </div>
  );
}
```

### 6.3 이미지 최적화

```typescript
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
    imageSizes: [16, 32, 48, 64, 96, 128, 256],
    minimumCacheTTL: 60 * 60 * 24, // 24시간
  },
};

// 컴포넌트에서
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // LCP 이미지
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

### 6.4 캐싱 전략

```typescript
// API 라우트 캐싱
export async function GET() {
  const data = await fetchData();

  return NextResponse.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
}

// 페이지 revalidation
export const revalidate = 3600; // 1시간마다 재생성

// On-demand revalidation
// src/app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';

export async function POST(request: Request) {
  const { path, tag, secret } = await request.json();

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  if (path) revalidatePath(path);
  if (tag) revalidateTag(tag);

  return NextResponse.json({ revalidated: true });
}
```

---

## 7. 테스트

### 7.1 유닛 테스트

```typescript
// __tests__/utils.test.ts
import { formatPrice, validateEmail } from '@/lib/utils';

describe('formatPrice', () => {
  it('formats Korean won correctly', () => {
    expect(formatPrice(10000)).toBe('₩10,000');
    expect(formatPrice(1000000)).toBe('₩1,000,000');
  });

  it('handles zero', () => {
    expect(formatPrice(0)).toBe('₩0');
  });
});

describe('validateEmail', () => {
  it('validates correct emails', () => {
    expect(validateEmail('test@example.com')).toBe(true);
    expect(validateEmail('user.name@domain.co.kr')).toBe(true);
  });

  it('rejects invalid emails', () => {
    expect(validateEmail('invalid')).toBe(false);
    expect(validateEmail('test@')).toBe(false);
  });
});
```

### 7.2 컴포넌트 테스트

```typescript
// __tests__/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onClick when clicked', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click me</Button>);

    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### 7.3 API 테스트

```typescript
// __tests__/api/products.test.ts
import { createMocks } from 'node-mocks-http';
import { GET, POST } from '@/app/api/products/route';

describe('/api/products', () => {
  describe('GET', () => {
    it('returns products list', async () => {
      const { req } = createMocks({ method: 'GET' });
      const response = await GET(req as any);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data).toHaveProperty('data');
      expect(data).toHaveProperty('pagination');
    });
  });

  describe('POST', () => {
    it('creates a new product', async () => {
      const { req } = createMocks({
        method: 'POST',
        body: { name: 'Test Product', price: 10000 },
      });

      // Mock session
      jest.mock('next-auth', () => ({
        getServerSession: () => ({ user: { id: 'user-1' } }),
      }));

      const response = await POST(req as any);
      expect(response.status).toBe(201);
    });
  });
});
```

---

## 8. 롤백

### 8.1 Vercel 롤백

```bash
# 이전 배포 목록 확인
vercel list

# 특정 배포로 롤백
vercel rollback [deployment-url]

# 또는 대시보드에서:
# Deployments → 이전 배포 선택 → ... → Promote to Production
```

### 8.2 데이터베이스 롤백

```bash
# 마이그레이션 상태 확인
npx prisma migrate status

# 마지막 마이그레이션 롤백 (개발용)
npx prisma migrate reset

# 프로덕션 롤백 (수동)
# 1. 백업에서 복원
# 2. 또는 역방향 마이그레이션 SQL 실행
```

### 8.3 Git 롤백

```bash
# 커밋 되돌리기 (새 커밋 생성)
git revert HEAD
git push origin main

# 강제 롤백 (주의!)
git reset --hard HEAD~1
git push origin main --force
```

---

## 9. 수정 체크리스트

```
┌─────────────────────────────────────────────────────────────┐
│ ✅ 코드 수정 체크리스트                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 📝 수정 전                                                    │
│ □ 이슈/티켓 확인                                             │
│ □ 관련 코드 파악                                             │
│ □ 영향 범위 분석                                             │
│ □ 브랜치 생성                                                │
│                                                              │
│ 💻 수정 중                                                    │
│ □ 최소한의 변경만                                            │
│ □ 코드 스타일 준수                                           │
│ □ 주석/문서 업데이트                                         │
│ □ 테스트 추가/수정                                           │
│                                                              │
│ ✅ 수정 후                                                    │
│ □ 로컬 테스트 통과                                           │
│ □ 린트/타입 체크 통과                                        │
│ □ PR 생성 및 리뷰 요청                                       │
│ □ 스테이징 테스트                                            │
│ □ 프로덕션 배포                                              │
│ □ 배포 후 모니터링                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```
