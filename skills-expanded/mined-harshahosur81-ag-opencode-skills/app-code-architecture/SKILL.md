---
name: app-code-architecture
description: Expert code reviewer for app development. Audits code quality, performance,
  scalability, security, and architectural patterns with measurable standards.
category: architecture
tags:
- architecture
- app
- code
---
# Skill: App Code & Architecture Expert

**You are the architectural perfectionist.** You can mentally compile code, predict race conditions, and spot bottlenecks before the profiler does.

---

## ⚡ Code Audit Checklist

- [ ] **Async Patterns:** Debouncing (300ms) on search/filter inputs?
- [ ] **Request Cancellation:** AbortController on component unmount?
- [ ] **State Management:** No direct mutations (immutable updates)?
- [ ] **Magic Strings:** Constants/enums for repeated values?
- [ ] **Type Safety:** No `any` in TypeScript (use proper types)?
- [ ] **Error Handling:** Try/catch with user-friendly messages?
- [ ] **Security:** Server-side validation (not just client)?
- [ ] **Performance:** Core Web Vitals met (LCP <2.5s, CLS <0.1)?
- [ ] **Bundle Size:** Initial JS <200KB gzipped?
- [ ] **Code Reuse:** Logic extracted, not copy-pasted?

---

## 🎯 When to Use This Skill

**Use when:**
- Reviewing code/PRs for quality or performance
- User mentions: "optimize", "refactor", "architecture", "scale"
- Before production deployment
- Debugging performance issues

**Don't use for:**
- Pure UI/UX design (use UX audit skill)
- DevOps/infrastructure only

---

## 🚨 Code Issue Priority

### P0 (Blocking)
- Security vulnerabilities (XSS, injection, exposed secrets)
- App crashes or data loss
- Memory leaks in production

### P1 (Critical)
- Core Web Vitals failures (LCP >2.5s, CLS >0.1)
- Race conditions in critical flows (checkout, save)
- No error handling on network requests

### P2 (Important)
- Non-optimal patterns (prop drilling, God components)
- Missing loading states
- Hardcoded values (magic strings)

### P3 (Polish)
- Code organization, minor refactors

---

## 🧠 Core Philosophy

1. **Code is Liability:** Best code is no code. Solve with architecture/config first.
2. **Physics over Frameworks:** Frameworks change. Network latency (100ms perception) doesn't.
3. **Measure Everything:** "Feels slow" ≠ actionable. "LCP is 4.2s" = actionable.
4. **Security by Design:** Trust nothing from client. Validate server-side.

---

## 💻 Domain 1: Code Quality & Patterns

### Race Conditions
**Problem:** Search triggers on every keystroke without debouncing.

```typescript
// ❌ Bad: 10 requests for "javascript"
const handleSearch = (query: string) => {
  fetch(`/api/search?q=${query}`).then(setResults);
}
```

**Why it fails:**
- Request 1 (for "j") may return AFTER request 10 (for "javascript")
- Wrong results displayed

```typescript
// ✅ Good: Debounce + cancellation
import { useDebouncedValue } from '@/hooks/useDebouncedValue';

const [query, setQuery] = useState('');
const debouncedQuery = useDebouncedValue(query, 300);
const abortRef = useRef<AbortController>();

useEffect(() => {
  if (!debouncedQuery) return;
  
  abortRef.current?.abort();
  abortRef.current = new AbortController();

  fetch(`/api/search?q=${debouncedQuery}`, {
    signal: abortRef.current.signal
  })
    .then(res => res.json())
    .then(setResults)
    .catch(err => {
      if (err.name !== 'AbortError') console.error(err);
    });

  return () => abortRef.current?.abort();
}, [debouncedQuery]);
```

### State Mutation
**Problem:** Direct object mutation in React/Vue state.

```typescript
// ❌ Bad: Silent bugs, missed re-renders
const addItem = (item) => {
  state.items.push(item); // Mutation!
  setState(state);
}
```

```typescript
// ✅ Good: Immutable update
const addItem = (item) => {
  setState({
    ...state,
    items: [...state.items, item]
  });
}
```

### Async/Await in Loops
**Problem:** Serializing parallel operations.

```typescript
// ❌ Bad: Takes 5 seconds for 5 items
for (const item of items) {
  await processItem(item); // Waits for each
}
```

```typescript
// ✅ Good: Parallel execution
await Promise.all(items.map(item => processItem(item)));
```

---

## ⛔ Anti-Patterns Table

| Bad Pattern | Why | Good Alternative |
|-------------|-----|------------------|
| `setTimeout` for async flow | Non-deterministic | `async/await` with proper error handling |
| `any` in TypeScript | Defeats type safety | Proper types or `unknown` with guards |
| Fetching in `useEffect` without cleanup | Race conditions, leaks | React Query, SWR, or Server Components |
| `&&` for conditional render with numbers | `0` renders as text | Ternary: `count > 0 ? <Comp /> : null` |
| Global CSS in components | Namespace pollution | CSS Modules or scoped styles |
| Hardcoded API URLs | Breaks across environments | Environment variables |

---

## 🛡️ Security Patterns

### Server-Side Validation
```typescript
// ❌ Bad: Client-only validation
const handleSubmit = (data) => {
  if (data.email.includes('@')) { // Easily bypassed
    api.createUser(data);
  }
}
```

```typescript
// ✅ Good: Server validates
// server.ts
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18).max(120)
});

app.post('/users', (req, res) => {
  const result = UserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json(result.error);
  }
  // Proceed with validated data
});
```

### Environment Variables
```typescript
// ❌ Bad: API key in frontend
const API_KEY = 'sk-abc123...'; // Leaked to client!

// ✅ Good: Server-side proxy
// Frontend calls your backend, backend uses key
fetch('/api/ai-proxy', { ... });
```

---

## 📊 Performance Budget

### Core Web Vitals

| Metric | Good | Poor |
|--------|------|------|
| **LCP** (Largest Contentful Paint) | <2.5s | >4.0s |
| **FID** (First Input Delay) | <100ms | >300ms |
| **CLS** (Cumulative Layout Shift) | <0.1 | >0.25 |
| **TTI** (Time to Interactive) | <3.8s | >7.3s |

### Bundle Size
- **Initial JS:** <200KB gzipped
- **Total JS:** <500KB gzipped
- **Images:** Use WebP/AVIF, lazy load below fold

### Optimization Checklist
- [ ] Code splitting (dynamic imports)
- [ ] Tree shaking (remove unused code)
- [ ] Image optimization (responsive, lazy load)
- [ ] Font subsetting (only needed glyphs)
- [ ] CDN for static assets

---

## 🏗️ Architecture Patterns

### Feature Flags
**Never deploy without a kill switch.**

```typescript
// config/flags.ts
export const flags = {
  newCheckout: process.env.ENABLE_NEW_CHECKOUT === 'true',
  aiSuggestions: process.env.ENABLE_AI === 'true'
};

// components/Checkout.tsx
import { flags } from '@/config/flags';

export function Checkout() {
  if (flags.newCheckout) {
    return <NewCheckout />;
  }
  return <LegacyCheckout />;
}
```

**Benefit:** Turn off broken feature in 1 second without redeploying.

### Plugin Architecture
**Make components swappable.**

```typescript
// ❌ Bad: Hardcoded payment
function Checkout() {
  return <StripePayment />; // Locked to Stripe
}
```

```typescript
// ✅ Good: Interface-based
interface PaymentProvider {
  processPayment(amount: number): Promise<Result>;
}

class StripePayment implements PaymentProvider { ... }
class PayPalPayment implements PaymentProvider { ... }

function Checkout({ provider }: { provider: PaymentProvider }) {
  return <PaymentForm provider={provider} />;
}
```

**Test:** Can you add a new provider without editing Checkout?

### Design Tokens
**Never hardcode colors.**

```css
/* ❌ Bad: Hardcoded */
.button {
  background: #3B82F6;
  color: #1F2937;
}
```

```css
/* ✅ Good: Tokens */
:root {
  --color-primary: #3B82F6;
  --color-text: #1F2937;
}

[data-theme="dark"] {
  --color-primary: #60A5FA;
  --color-text: #F9FAFB;
}

.button {
  background: var(--color-primary);
  color: var(--color-text);
}
```

**Benefit:** CEO wants dark mode? Change 5 lines, not 500.

---

## 🆕 Modern Patterns (2026)

### AI Integration
- **Streaming:** Use Server-Sent Events for progressive responses
- **Caching:** Cache AI responses (expensive API calls)
- **Fallbacks:** Handle API downtime gracefully

### Edge Computing
- **Edge Functions:** Move auth checks to edge (Cloudflare, Vercel)
- **Reduces latency:** 50ms vs. 200ms to origin server

### State Management
- **Signals:** Fine-grained reactivity (Solid.js, Vue refs) vs. component re-renders
- **Server Components:** Ship less JS (React Server Components)
- **Local-First:** Offline sync (RxDB, Electric SQL)

---

## 🔧 Verification Tools

**Code Analysis:**
- `grep_search` for magic strings: `grep_search('#[0-9a-fA-F]{6}')` (hardcoded colors)
- `grep_search('useEffect')` - check for cleanup functions

**Performance:**
- Lighthouse in Chrome DevTools
- `npx vite-bundle-visualizer` or `webpack-bundle-analyzer`
- Test on throttled network (Fast 3G in DevTools)

**Security:**
- `npm audit` for dependencies
- Check for exposed secrets: `git secrets --scan`

**Type Safety:**
- `grep_search(': any')` - find TypeScript escape hatches

---

## 🚩 Code Red Flags

- **"Just copy-paste that logic"** - DRY principle. Extract to function.
- **50+ warnings in console** - Fix them. They hide real errors.
- **No error handling** - Every network request needs try/catch.
- **Magic numbers** - `setTimeout(fn, 3000)` → `DEBOUNCE_MS = 3000`
- **God components** - 800+ line files doing everything.
- **No loading states** - User thinks app froze.

---

## 🚀 Code Review Template

**❌ Issue Found:**
- **File:** `ProductList.tsx:67`
- **Severity:** P1 (Critical)

```typescript
const ProductList = () => {
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    fetch('/api/products').then(res => res.json()).then(setProducts);
  }, []);
  // ...
}
```

**🔍 Diagnosis:**
- No error handling (network failure crashes app)
- No loading state (appears frozen while fetching)
- No cleanup (if component unmounts mid-fetch, setState on unmounted component)

**⚠️ Impact:**
- **User:** Sees blank screen, no feedback
- **Production:** Unhandled promise rejections

**✅ Fix:**
```typescript
const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const controller = new AbortController();
    
    setLoading(true);
    fetch('/api/products', { signal: controller.signal })
      .then(res => res.json())
      .then(data => {
        setProducts(data);
        setLoading(false);
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          setError('Failed to load products. Please try again.');
          setLoading(false);
        }
      });
    
    return () => controller.abort();
  }, []);
  
  if (loading) return <ProductSkeleton />;
  if (error) return <ErrorMessage message={error} retry={() => window.location.reload()} />;
  return <ProductGrid products={products} />;
}
```

**💡 Guru Tip:**
Consider using React Query or SWR for automatic caching, retries, and refetching.

---

## 📚 Glossary

- **Debouncing:** Delay execution until user stops action (300ms after last keystroke)
- **Throttling:** Limit execution to once per period (max once per 100ms)
- **Race Condition:** Two async ops where order matters, but completion is non-deterministic
- **Immutable Update:** Create new object instead of mutating existing
- **Design Tokens:** Abstract values (colors, spacing) into variables

---

## 🎓 Final Wisdom

**The Architect's Mantra:**
> "Build it so it scales to 100x users, survives API outages, and a junior dev can understand it in 30 minutes."

**Remember:**
1. Every millisecond counts (100ms = perception threshold)
2. Failure is inevitable - design for it
3. Security is architecture, not an afterthought
4. The best optimization is eliminating code
