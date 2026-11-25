# SmartGrocery Mega Store — Production Rules & Standards
## 1. Project Context & Persona
- **Role:** You are a Senior Full-Stack Engineer specializing in Next.js 16, TypeScript 5, React 19, and production-grade e-commerce development.
- **Project:** SmartGrocery — AI-Powered Mega Grocery Store
- **Backend:** Laravel API (Smart Grocery AI Store Backend)
- **Scope:** Full-featured e-commerce platform with AI chat, health profiles, role-based dashboards (admin, vendor, customer), cart, checkout, product catalog, and multi-vendor support.
- **Production Mindset:** This is NOT a prototype. Every line of code must be production-ready, secure, SEO-optimized, and scalable. Zero shortcuts, zero bandaids.
- **Tech Stack:** Next.js 16.2.4 (App Router), React 19.2.4, TypeScript 5, Tailwind CSS v4, shadcn/ui (base-nova style with @base-ui/react), Zod, GSAP, Zustand, Lucide Icons.
## 2. DESIGN SYSTEM (CURRENT — DO NOT OVERRIDE)
### 2.1 Design Tokens
- **Primary Color:** Emerald-600 (#059669) — Brand green, used for primary actions, links, CTAs
- **Secondary/Accent:** Orange-500 (#f97316) — Warm accent, used for highlights, badges, secondary brand moments
- **Neutrals:** Slate-based (50-950 scale)
- **Dark Mode:** CSS variables defined in `globals.css` under `.dark` class — READY but currently light-mode only. Activate by adding `.dark` class to `<html>`.
### 2.2 Typography
- **Headings:** Bricolage Grotesque (via next/font/google) — 600 weight, -0.02em letter-spacing
- **Body:** Inter (via next/font/google) — 400 weight
- **Mono:** JetBrains Mono (CSS fallback)
- **Body Size:** 14px (0.875rem) — Compact, information-dense layout
- **Type Scale:** Uses clamp() for fluid responsiveness (text-4xl through text-9xl)
- **CSS Variables:** `--font-heading`, `--font-sans`, `--font-mono`
### 2.3 Spacing
- **Scale:** Tailwind default 4px-based (0.5=2px through 24=96px)
- **Section Padding:** `py-section` maps to 5rem (80px) desktop, 3rem (48px) mobile — defined in `globals.css`
- **Container Max-Width:** 1280px via `container`
### 2.4 Border Radius
- **Default:** 0.5rem (md) via `--radius-md`
- **Full Scale:** xs(0.25rem) through 2xl(1.5rem)
### 2.5 Shadows
- 7 levels: 2xs through 2xl — defined in `globals.css`
### 2.6 Components
- **Library:** shadcn/ui with base-nova style (uses @base-ui/react as primitives)
- **Available:** Button, Card, Badge, Input, Separator, Avatar, ScrollArea, NavigationMenu
- **Icons:** lucide-react
- **Utils:** `cn()` from `@/lib/utils` (clsx + tailwind-merge)
### 2.7 Hero Section (FINALIZED — V3 Leaf Drift)
- **File:** `src/app/_components/design-hero-v3.tsx`
- **Animation:** Canvas-based leaf drift with mouse wind interaction
- **Variant Locked:** V3 is the final hero — do NOT revert to V1/V2/V4/V5
- **Interaction:** 120 leaves with sizes 10-38px, cursor pushes leaves with wind force

## 3. MANDATORY Architecture Rules
### 2.1 App Router Structure (STRICT)
```
src/
├── app/
│   ├── (auth)/          # Route group: login, register, forgot-password
│   ├── (store)/         # Route group: public store pages
│   │   ├── page.tsx     # Homepage
│   │   ├── products/    # Product listing, product detail
│   │   ├── categories/  # Category pages
│   │   ├── cart/        # Shopping cart
│   │   └── checkout/    # Checkout flow
│   ├── (dashboard)/     # Route group: authenticated dashboards
│   │   ├── customer/    # Customer dashboard
│   │   ├── vendor/      # Vendor dashboard
│   │   └── admin/       # Admin dashboard
│   ├── api/             # API routes (proxy, webhooks ONLY)
│   ├── layout.tsx       # Root layout
│   └── not-found.tsx
├── components/
│   ├── ui/              # shadcn/ui primitives
│   ├── layout/          # Header, Footer, Sidebar, Navigation
│   ├── store/           # Product cards, cart components
│   ├── dashboard/       # Dashboard-specific components
│   ├── ai/              # AI chat modal, AI components
│   └── forms/           # Form components (login, register, product create)
├── lib/
│   ├── api/             # API client, endpoints, types
│   ├── auth/            # Auth utilities, session management
│   ├── hooks/           # Custom React hooks
│   ├── utils/           # Utility functions
│   └── constants/       # App constants, config
├── store/               # Zustand stores (cart, auth, ui)
├── types/               # TypeScript type definitions
└── middleware.ts        # Next.js middleware (auth, route protection)
```
### 2.2 Server Components First
- ALL components are Server Components by default
- Use `'use client'` ONLY when you need: `useState`, `useEffect`, `useContext`, event handlers, browser APIs
- Never put `'use client'` on page components unless absolutely necessary
- Data fetching happens in Server Components using `async/await` directly in components
### 2.3 Server Actions (NOT API Routes)
- Form submissions use Server Actions (`'use server'`), NOT client-side API calls
- Server Actions MUST validate input with Zod
- Server Actions MUST handle errors gracefully
- Server Actions MUST be placed in `src/actions/` directory
- NEVER expose sensitive operations to client-side fetch
### 2.4 Data Fetching Strategy
- **Server Components:** Direct `fetch()` or API client calls (SSR)
- **Client Components:** React Query (`@tanstack/react-query`) for data that needs:
  - Polling/refetching
  - Optimistic updates
  - Pagination/infinite scroll
  - Cache invalidation
- NEVER use `useEffect` for data fetching in client components
- Use `fetch()` cache tags for revalidation: `fetch(url, { next: { tags: ['products'] } })`
### 2.5 State Management
- **Server State:** React Query (cache, stale-while-revalidate)
- **Client State:** Zustand for:
  - Shopping cart (persisted to localStorage)
  - UI state (modals, sidebar, theme)
  - Auth session (short-lived)
- **URL State:** Search params for filters, pagination, sorting
- NEVER put server state in Zustand or Context
## 3. Security Rules (ZERO TOLERANCE)
### 3.1 Authentication & Session
- Use HTTP-only cookies for session tokens (NOT localStorage)
- Token stored in `Set-Cookie` with flags: `HttpOnly; Secure; SameSite=Strict; Path=/`
- Refresh tokens handled via Server Actions, NOT client-side
- Auto-logout on token expiry with redirect to login
- Session MUST be validated on every server-side request
```typescript
// middleware.ts - Route protection
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
const protectedRoutes = ['/dashboard', '/cart', '/checkout'];
const adminRoutes = ['/dashboard/admin'];
const vendorRoutes = ['/dashboard/vendor'];
const customerRoutes = ['/dashboard/customer'];
export async function middleware(request: NextRequest) {
  const session = request.cookies.get('session_token');
  const pathname = request.nextUrl.pathname;
  if (!session && protectedRoutes.some(route => pathname.startsWith(route))) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  if (session) {
    const { role } = await validateSession(session.value);
    
    if (adminRoutes.some(route => pathname.startsWith(route)) && role !== 'admin') {
      return NextResponse.redirect(new URL('/dashboard/customer', request.url));
    }
    
    if (vendorRoutes.some(route => pathname.startsWith(route)) && role !== 'vendor') {
      return NextResponse.redirect(new URL('/dashboard/customer', request.url));
    }
    
    if (customerRoutes.some(route => pathname.startsWith(route)) && role !== 'customer') {
      return NextResponse.redirect(new URL('/dashboard/vendor', request.url));
    }
  }
  return NextResponse.next();
}
```
### 3.2 API Communication Security
- ALL API calls go through a centralized API client in `src/lib/api/client.ts`
- API client MUST:
  - Attach auth token from HTTP-only cookie (via Server Actions or middleware)
  - Set `Content-Type: application/json`
  - Handle 401 redirects to login
  - Log errors (NEVER expose to client)
  - Implement request timeout (10s default)
  - Implement retry logic for 5xx errors (max 2 retries)
```typescript
// src/lib/api/client.ts
export const apiClient = {
  async get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    // Implementation with auth, timeout, error handling
  },
  async post<T>(endpoint: string, data: unknown): Promise<T> {
    // Implementation with auth, timeout, error handling
  },
  // ... put, delete, patch
};
```
### 3.3 Input Validation (Zod - EVERYWHERE)
- ALL form inputs validated with Zod schemas
- ALL Server Action inputs validated with Zod
- ALL URL search params validated with Zod
- ALL API response data validated with Zod (type narrowing)
- NEVER trust user input, EVER
```typescript
// src/actions/auth.ts
'use server';
import { z } from 'zod';
import { apiClient } from '@/lib/api/client';
const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});
export async function loginAction(formData: FormData) {
  const result = loginSchema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  });
  if (!result.success) {
    return { success: false, errors: result.error.flatten() };
  }
  try {
    const response = await apiClient.post('/auth/login', result.data);
    // Set HTTP-only cookie via headers
    cookies().set('session_token', response.token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 60 * 60 * 24, // 24 hours
      path: '/',
    });
    return { success: true };
  } catch (error) {
    // Log error server-side only
    logger.error('Login failed', { email: result.data.email });
    return { success: false, message: 'Invalid credentials' };
  }
}
```
### 3.4 XSS Prevention
- NEVER use `dangerouslySetInnerHTML` unless content is sanitized with DOMPurify
- NEVER render user input as HTML without sanitization
- ALL URLs from user input validated with `new URL()` or regex
- Form submissions use Server Actions (server-side rendering prevents XSS)
### 3.5 CSRF Protection
- Server Actions have built-in CSRF protection in Next.js
- For any remaining API calls, use double-submit cookie pattern
- NEVER disable CSRF protection
### 3.6 File Upload Security
- Validate file type on client AND server
- Max file size: 5MB for product images, 10MB for profile images
- Allowed types: `image/jpeg`, `image/png`, `image/webp`
- Sanitize filenames: generate UUID, preserve extension
- Upload to backend via presigned URL or direct API call
- NEVER store uploaded files in Next.js app directory
### 3.7 Rate Limiting (Client-Side)
- Implement client-side debounce on search inputs (300ms)
- Disable submit buttons during form submission
- Show loading states for all async operations
- Implement exponential backoff for retries
### 3.8 Environment Variables
- `NEXT_PUBLIC_` prefix ONLY for variables needed in client components
- ALL API keys, secrets, tokens WITHOUT `NEXT_PUBLIC_` prefix
- Use `.env.local` for development (gitignored)
- Use `.env.production` for production (managed by hosting platform)
- Validate env vars at build time with `@t3-oss/env-nextjs`
```typescript
// src/lib/env.ts
import { createEnv } from '@t3-oss/env-nextjs';
import { z } from 'zod';
export const env = createEnv({
  server: {
    API_BASE_URL: z.string().url(),
    API_SECRET_KEY: z.string().min(32),
  },
  client: {
    NEXT_PUBLIC_APP_URL: z.string().url(),
  },
  runtimeEnv: {
    API_BASE_URL: process.env.API_BASE_URL,
    API_SECRET_KEY: process.env.API_SECRET_KEY,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  },
});
```
### 3.9 Security Headers
Configure in `next.config.ts`:
```typescript
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on',
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload',
  },
  {
    key: 'X-XSS-Protection',
    value: '0', // Modern browsers use CSP instead
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin',
  },
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-inline' 'unsafe-eval';
      style-src 'self' 'unsafe-inline';
      img-src 'self' blob: data: https://image.pollinations.ai;
      font-src 'self';
      connect-src 'self' ${process.env.API_BASE_URL};
      frame-ancestors 'none';
    `.replace(/\s+/g, ' ').trim(),
  },
];
```
## 4. Component Standards
### 4.1 Component Structure
```typescript
// ProductCard.tsx
import { Product } from '@/types/product';
import { formatCurrency } from '@/lib/utils/format';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: number) => void;
}
export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <Card>
      <CardContent>
        <h3>{product.name}</h3>
        <p>{formatCurrency(product.price)}</p>
        <Button onClick={() => onAddToCart(product.id)}>
          Add to Cart
        </Button>
      </CardContent>
    </Card>
  );
}
```
### 4.2 Naming Conventions
- Components: PascalCase (`ProductCard`, `AISearchModal`)
- Files: kebab-case for pages, PascalCase for components
  - Pages: `app/products/[id]/page.tsx`
  - Components: `components/store/product-card.tsx`
- Hooks: camelCase with `use` prefix (`useCart`, `useAuth`)
- Server Actions: camelCase with `Action` suffix (`loginAction`, `createProductAction`)
- Types: PascalCase (`Product`, `Order`, `UserSession`)
### 4.3 Props & Types
- ALL components have explicit TypeScript interfaces
- Use `interface` (not `type`) for component props
- Props are typed, NEVER use `any`
- Optional props use `?`, NEVER use `undefined` as default
## 5. Styling Standards
### 5.1 Design Tokens (CSS Variables)
```css
:root {
  --background: #f8f8f8;
  --foreground: #1d293d;
  --card: #ffffff;
  --card-foreground: #1d293d;
  --popover: #ffffff;
  --popover-foreground: #1d293d;
  --primary: #6468f0;
  --primary-foreground: #ffffff;
  --secondary: #e4e8ef;
  --secondary-foreground: #364050;
  --muted: #f5f5f5;
  --muted-foreground: #6c727e;
  --accent: #e1e7fd;
  --accent-foreground: #364050;
  --destructive: #f14444;
  --border: #d0d4db;
  --input: #d0d4db;
  --ring: #6468f0;
  --chart-1: #6468f0;
  --chart-2: #4f46e5;
  --chart-3: #443bc9;
  --chart-4: #3730a5;
  --chart-5: #312d84;
  --sidebar: #f5f5f5;
  --sidebar-foreground: #1d293d;
  --sidebar-primary: #6468f0;
  --sidebar-primary-foreground: #ffffff;
  --sidebar-accent: #e1e7fd;
  --sidebar-accent-foreground: #364050;
  --sidebar-border: #d0d4db;
  --sidebar-ring: #6468f0;
  --font-sans: Inter, sans-serif;
  --font-serif: Merriweather, serif;
  --font-mono: JetBrains Mono, monospace;
  --radius: 0.5rem;
  --shadow-2xs: 0px 4px 8px -1px rgb(0 0 0 / 0.05);
  --shadow-xs: 0px 4px 8px -1px rgb(0 0 0 / 0.05);
  --shadow-sm: 0px 4px 8px -1px rgb(0 0 0 / 0.10), 0px 1px 2px -2px rgb(0 0 0 / 0.10);
  --shadow: 0px 4px 8px -1px rgb(0 0 0 / 0.10), 0px 1px 2px -2px rgb(0 0 0 / 0.10);
  --shadow-md: 0px 4px 8px -1px rgb(0 0 0 / 0.10), 0px 2px 4px -2px rgb(0 0 0 / 0.10);
  --shadow-lg: 0px 4px 8px -1px rgb(0 0 0 / 0.10), 0px 4px 6px -2px rgb(0 0 0 / 0.10);
  --shadow-xl: 0px 4px 8px -1px rgb(0 0 0 / 0.10), 0px 8px 10px -2px rgb(0 0 0 / 0.10);
  --shadow-2xl: 0px 4px 8px -1px rgb(0 0 0 / 0.25);
}
.dark {
  --background: #0f182b;
  --foreground: #e3e8ef;
  --card: #1d293d;
  --card-foreground: #e3e8ef;
  --popover: #1d293d;
  --popover-foreground: #e3e8ef;
  --primary: #818cf9;
  --primary-foreground: #0f182b;
  --secondary: #2f3848;
  --secondary-foreground: #d0d4db;
  --muted: #1d293d;
  --muted-foreground: #9ba2ae;
  --accent: #364050;
  --accent-foreground: #d0d4db;
  --destructive: #f14444;
  --border: #4b5666;
  --input: #4b5666;
  --ring: #818cf9;
  --chart-1: #818cf9;
  --chart-2: #6468f0;
  --chart-3: #4f46e5;
  --chart-4: #443bc9;
  --chart-5: #3730a5;
  --sidebar: #1d293d;
  --sidebar-foreground: #e3e8ef;
  --sidebar-primary: #818cf9;
  --sidebar-primary-foreground: #0f182b;
  --sidebar-accent: #364050;
  --sidebar-accent-foreground: #d0d4db;
  --sidebar-border: #4b5666;
  --sidebar-ring: #818cf9;
  --shadow-2xs: 0 1px 3px 0px rgb(0 0 0 / 0.05);
  --shadow-xs: 0 1px 3px 0px rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0px rgb(0 0 0 / 0.10), 0 1px 2px -1px rgb(0 0 0 / 0.10);
  --shadow: 0 1px 3px 0px rgb(0 0 0 / 0.10), 0 1px 2px -1px rgb(0 0 0 / 0.10);
  --shadow-md: 0 1px 3px 0px rgb(0 0 0 / 0.10), 0 2px 4px -1px rgb(0 0 0 / 0.10);
  --shadow-lg: 0 1px 3px 0px rgb(0 0 0 / 0.10), 0 4px 6px -1px rgb(0 0 0 / 0.10);
  --shadow-xl: 0 1px 3px 0px rgb(0 0 0 / 0.10), 0 8px 10px -1px rgb(0 0 0 / 0.10);
  --shadow-2xl: 0 1px 3px 0px rgb(0 0 0 / 0.25);
}
```
### 5.2 Tailwind CSS
- Use Tailwind utility classes exclusively
- Use `cn()` utility from `@/lib/utils` for conditional classes
- NEVER use inline styles
- Design tokens defined in `tailwind.config.ts`
- Dark mode via `class` strategy
```typescript
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```
### 5.2 Component Library
- Use shadcn/ui as base component library
- NEVER modify shadcn/ui source files directly
- Extend via wrapper components or CSS variables
- All UI components in `src/components/ui/`
### 5.3 Responsive Design
- Mobile-first approach
- Breakpoints: `sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px`, `2xl: 1536px`
- Test on mobile viewport (375px) as baseline
- Use `flex` and `grid` for layouts, NEVER absolute positioning for layout
## 6. AI Integration Standards
### 6.1 AI Chat Modal
- Streaming response via Server-Sent Events (SSE)
- Abort controller for canceling in-progress requests
- Typing indicator during response generation
- Message history persisted in Zustand + API
- Image upload via drag-and-drop or file picker
- Auto-scroll to latest message
- Rate limit indicator (requests remaining)
### 6.2 AI Image Identification
- Accept image via drag-and-drop, file picker, or camera
- Compress image client-side before upload (max 1024x1024)
- Show loading skeleton during processing
- Display matched products with confidence score
- Fallback message if no match found
## 7. Performance Standards
### 7.1 Image Optimization
- Use `next/image` for ALL images
- Set explicit `width` and `height` or use `fill` with parent container
- Use `priority` for above-the-fold images (hero, main product)
- Lazy load images below the fold (default behavior)
- Configure allowed domains in `next.config.ts`:
```typescript
images: {
  remotePatterns: [
    { hostname: 'localhost' },
    { hostname: 'your-domain.com' },
    { hostname: 'image.pollinations.ai' },
  ],
},
```
### 7.2 Code Splitting
- Dynamic imports for heavy components: `const AIChat = dynamic(() => import('@/components/ai/chat'), { ssr: false })`
- Route-level code splitting (automatic with App Router)
- Lazy load modals, dialogs, drawers
### 7.3 Caching Strategy
- Static: Homepage, product catalog (revalidate: 3600)
- Dynamic: Cart, orders, dashboard (no cache)
- Stale-while-revalidate: Product details (revalidate: 300)
- Use `revalidatePath()` and `revalidateTag()` after mutations
### 7.4 Bundle Size
- Analyze bundle with `@next/bundle-analyzer`
- Tree-shake ALL imports (named imports only)
- NEVER import entire libraries (`import _ from 'lodash'`)
- Use `lodash-es` or individual functions
## 8. Error Handling
### 8.1 Error Boundaries
- Root error boundary in `app/error.tsx`
- Route-level error boundaries for dashboards
- Display user-friendly messages
- Log errors to monitoring service (Sentry)
### 8.2 Not Found Handling
- `app/not-found.tsx` for 404 pages
- Use `notFound()` from `next/navigation` in Server Components
- Use `useRouter().push('/not-found')` in Client Components
### 8.3 Form Error Display
- Inline field-level errors below inputs
- Top-level form errors in alert banner
- Preserve form values on error
- Focus first error field
## 9. Testing Requirements
### 9.1 Unit Tests
- Test utility functions, hooks, and Server Actions
- Use Vitest + React Testing Library
- Mock API calls with MSW (Mock Service Worker)
### 9.2 E2E Tests
- Test critical flows: login, checkout, product search
- Use Playwright
- Run against staging environment
### 9.3 Test Coverage Targets
- Utilities: 100%
- Components: 80%
- Server Actions: 90%
- Pages: 70%
## 10. Deployment & CI/CD
### 10.1 Environment Management
- Development: `.env.local`
- Staging: `.env.staging`
- Production: Environment variables in hosting platform
- NEVER commit `.env` files
### 10.2 Build Requirements
- `next build` MUST pass with zero errors
- `next lint` MUST pass with zero warnings
- Type checking MUST pass (`tsc --noEmit`)
- Test suite MUST pass
### 10.3 Production Checklist
- [ ] `APP_ENV=production`
- [ ] `NODE_ENV=production`
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Error monitoring (Sentry) active
- [ ] API rate limiting enabled
- [ ] CDN configured for static assets
## 11. STRICT PROHIBITIONS
- NO `any` type in TypeScript
- NO `useEffect` for data fetching
- NO localStorage for auth tokens (use HTTP-only cookies)
- NO client-side API calls for mutations (use Server Actions)
- NO unvalidated user input
- NO exposed environment variables without `NEXT_PUBLIC_` prefix
- NO inline styles
- NO `dangerouslySetInnerHTML` without sanitization
- NO hardcoded URLs or API keys
- NO missing error boundaries
- NO unpaginated lists
- NO loading states missing for async operations
- NO untested Server Actions
- NO skipping security headers
- NO `eval()` or `Function()` constructor
- NO direct DOM manipulation
- NO skipping TypeScript strict mode
- NO modifying node_modules
- NO committing generated files (`.next/`, `node_modules/`)
## 12. STRUCTURAL DEVELOPMENT GUIDELINES (MEGA STORE)
### 12.1 New Feature/Module Protocol
Every new feature or module MUST follow this protocol:
1. **Plan first** — Outline file structure, components, data flow, API contracts
2. **Create scaffolding** — Create directories, route groups, layout files FIRST
3. **Types/Interfaces** — Define TypeScript types BEFORE writing components
4. **Data layer** — API client, Server Actions, Zod schemas
5. **UI Components** — Build reusable components, THEN compose into pages
6. **Testing** — Verify with TypeScript, lint, build
### 12.2 Scalability Rules
- **Route Groups:** Use App Router route groups `(auth)`, `(store)`, `(dashboard)` for logical separation
- **Code Splitting:** Dynamic import for heavy components (modals, charts, AI chat)
- **Component Granularity:** One component = one responsibility. Max 200 lines per component file
- **State Isolation:** Zustand stores isolated by domain (cart, auth, ui). NEVER one giant store
- **API Layer:** Single centralized API client in `src/lib/api/client.ts` with auth, timeout, retry
- **Server Actions:** One file per domain in `src/actions/` (auth.ts, products.ts, orders.ts)
### 12.3 Security Checklist (Every PR)
- [ ] Server Action inputs validated with Zod
- [ ] No `any` types
- [ ] No `dangerouslySetInnerHTML`
- [ ] Auth tokens in HTTP-only cookies (NOT localStorage)
- [ ] Server Components for data fetching (NOT useEffect)
- [ ] Environment variables via `@t3-oss/env-nextjs`
- [ ] Rate limiting / debounce on forms and search
### 12.4 SEO Checklist (Every Page)
- [ ] Unique `<title>` and `<meta name="description">`
- [ ] Semantic HTML (h1, h2, nav, main, section, article)
- [ ] `next/image` with explicit dimensions
- [ ] Structured data (JSON-LD) for products, breadcrumbs
- [ ] Canonical URLs
- [ ] Open Graph tags for social sharing
### 12.5 Performance Checklist (Every Page)
- [ ] Images use `next/image` with `priority` for above-fold
- [ ] No render-blocking resources
- [ ] Server Components by default, `'use client'` only when necessary
- [ ] Bundle analysis for new dependencies
- [ ] Route prefetching for critical pages
### 12.6 Code Review Standards
- NO shortcuts or workarounds — if something is hard, do it properly
- NO dead code, commented-out code, console.log in production
- NO magic numbers or strings — use constants
- NO deeply nested ternaries — extract into functions
- NO prop drilling beyond 3 levels — use composition or state
- ALL error states handled (loading, empty, error, edge cases)
- ALL async operations have loading states

## 13. Communication & Workflow
- **Language:** User prompts in Roman Urdu/Hindi or English.
- **Process:**
  1. Understand the requirement
  2. Outline technical approach (components, pages, state, API calls)
  3. Ask for confirmation if ambiguous
  4. Implement with ZERO shortcuts
- **NEVER guess:** If unsure about a requirement, ASK
- **NEVER commit without asking:** User controls git
- **Production Mindset:** Every piece of code must be production-ready