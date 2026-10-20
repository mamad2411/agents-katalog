# SAP-038: Internationalization - Agent Awareness Guide

**SAP ID**: SAP-038
**Name**: react-internationalization
**Version**: 1.0.0
**Status**: pilot
**For**: All AI agents (Claude, GitHub Copilot, etc.)

---

## 📖 Quick Reference

**New to SAP-038?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 4-step setup (35 minutes) with library decision tree for next-intl or react-i18next
- 📚 **Time Savings** - 88.3% reduction (35 min vs 4-6 hours manual), type-safe translations with TypeScript inference
- 🎯 **2 Library Options** - next-intl (Next.js 15 native, 14KB) or react-i18next (framework-agnostic, 22KB)
- 🔧 **Locale Routing** - Middleware-based routing (/en/, /es/, /ar/) with automatic locale detection
- 📊 **RTL Support** - CSS logical properties, Tailwind RTL, Arabic/Hebrew/Farsi support with auto-direction switching
- 🔗 **Integration** - Works with SAP-020 (Foundation), SAP-041 (Forms), SAP-026 (Accessibility), SAP-031 (Routing)

This AGENTS.md provides: Agent-specific patterns for implementing internationalization workflows.

---

## Library Decision Tree

Use this **3-question decision tree** to choose the right library:

```
Question 1: Are you using Next.js 15 App Router?
├─ YES → next-intl (20 min setup, native integration)
└─ NO  → react-i18next (20 min setup, framework-agnostic)

Question 2: Do you need Server Component support?
├─ YES → next-intl (native SSR, no client-side flicker)
└─ NO  → react-i18next (more flexible, mature ecosystem)

Question 3: Are you using React Native or Vite?
├─ YES → react-i18next (framework-agnostic)
└─ NO  → next-intl (if Next.js) or react-i18next
```

---

### Library Comparison

| Criteria | next-intl | react-i18next | Winner |
|----------|-----------|---------------|--------|
| **TypeScript** | ✅ Full type inference | ⚠️ Partial | next-intl |
| **Bundle Size** | 14KB gzipped | 22KB gzipped | next-intl |
| **Server Components** | ✅ Native | ⚠️ Manual | next-intl |
| **Framework Support** | Next.js only | ✅ Any | react-i18next |
| **Ecosystem** | Growing | ✅ Mature (8k stars) | react-i18next |
| **Setup Time** | 20 min | 20 min | Tie |
| **Best for** | Next.js 15+ | React Native, Vite, legacy | Context-dependent |

---

## Key Workflows for Agents

### Workflow 1: New i18n Project (35 min)

**User request**: "Add internationalization to my React app"

**Agent steps**:

1. **Ask clarifying questions** (5 min):
   ```
   To recommend the best i18n library, I need to know:

   1. Are you using Next.js 15 App Router? (YES/NO)
   2. How many languages do you need? (2-5, 5-10, 10+)
   3. Do you need RTL support (Arabic, Hebrew)? (YES/NO)
   4. What's your expected scale? (<1k, 1k-10k, 10k+)
   ```

2. **Recommend library** (based on decision tree):
   - Next.js 15 → next-intl
   - React Native / Vite → react-i18next
   - Need Server Components → next-intl
   - Need framework flexibility → react-i18next

3. **Follow adoption-blueprint.md** for step-by-step setup (15-20 min):
   - Install library
   - Setup middleware (locale routing)
   - Create translation files
   - Configure layout with locale provider
   - Add language switcher

4. **Add RTL support** (if needed, 5-10 min):
   - Install Tailwind RTL plugin
   - Add dir attribute to HTML
   - Use CSS logical properties (ms-, me-, start, end)
   - Flip directional icons

5. **SEO optimization** (5 min):
   - Generate hreflang tags
   - Create locale sitemap
   - Add lang attribute to HTML
   - Add Open Graph locale tags

**Expected time**: 35 minutes (library setup + RTL + SEO)

---

### Workflow 2: Add Locale Routing (15 min)

**User request**: "Add URL-based locale routing (/en/, /es/)"

**Agent steps**:

1. **Check current framework** (2 min):
   - Next.js → Use next-intl middleware
   - Other → Use custom middleware or react-i18next

2. **Setup middleware** (next-intl, 10 min):
   ```typescript
   // middleware.ts
   import createMiddleware from 'next-intl/middleware';

   export default createMiddleware({
     locales: ['en', 'es', 'ar', 'zh'],
     defaultLocale: 'en',
   });

   export const config = {
     matcher: ['/((?!api|_next|.*\\..*).*)'],
   };
   ```

3. **Update app structure** (3 min):
   ```
   app/
   ├─ [locale]/
   │  ├─ layout.tsx
   │  ├─ page.tsx
   │  └─ about/
   │     └─ page.tsx
   ```

4. **Test** (2 min):
   - Visit /en/about → English content
   - Visit /es/about → Spanish content
   - Visit /about → Redirects to /en/about

**Expected time**: 15 minutes

---

### Workflow 3: Add RTL Support (10 min)

**User request**: "Support Arabic with right-to-left layout"

**Agent steps**:

1. **Install Tailwind RTL plugin** (2 min):
   ```bash
   npm install tailwindcss-rtl
   ```

2. **Configure Tailwind** (2 min):
   ```typescript
   // tailwind.config.ts
   import rtlPlugin from 'tailwindcss-rtl';

   export default {
     plugins: [rtlPlugin],
   };
   ```

3. **Add dir attribute** (2 min):
   ```typescript
   // app/[locale]/layout.tsx
   const isRTL = locale === 'ar' || locale === 'he' || locale === 'fa';

   return (
     <html lang={locale} dir={isRTL ? 'rtl' : 'ltr'}>
       <body>{children}</body>
     </html>
   );
   ```

4. **Use logical properties** (2 min):
   ```typescript
   // Replace left/right with start/end
   <div className="ms-4 me-8 text-start">
     {/* margin-start: 16px, margin-end: 32px, text-align: start */}
   </div>
   ```

5. **Test** (2 min):
   - Switch to Arabic (ar)
   - Verify layout mirrors
   - Check text aligns right

**Expected time**: 10 minutes

---

### Workflow 4: Debug i18n Issues (15-30 min)

**User request**: "My translations aren't loading / RTL layout is broken"

**Agent steps**:

1. **Check common issues** (5-10 min):

   **Missing translations**:
   ```typescript
   // Check translation file exists
   ls messages/en.json

   // Verify JSON syntax
   cat messages/en.json | jq

   // Check namespace matches
   // In component: useTranslations('HomePage')
   // In messages/en.json: { "HomePage": { ... } }
   ```

   **RTL layout broken**:
   ```typescript
   // Check dir attribute
   // <html dir="rtl"> (should be present for Arabic)

   // Check CSS logical properties
   // Use ms-, me- instead of ml-, mr-

   // Check Tailwind RTL plugin
   grep -r "tailwindcss-rtl" tailwind.config.ts
   ```

   **Locale routing not working**:
   ```typescript
   // Check middleware matcher
   // Should exclude API routes: /((?!api|_next|.*\\..*).*)

   // Check locale parameter
   // app/[locale]/page.tsx (not app/page.tsx)

   // Verify locales array
   // middleware.ts: locales: ['en', 'es', 'ar']
   ```

2. **Add logging** (5 min):
   ```typescript
   // middleware.ts
   console.log('Incoming request:', request.url);
   console.log('Detected locale:', locale);

   // app/[locale]/layout.tsx
   console.log('Current locale:', locale);
   console.log('Messages loaded:', Object.keys(messages));
   ```

3. **Test fixes** (5-10 min):
   - Clear browser cache
   - Hard refresh (Ctrl+Shift+R)
   - Check Network tab for translation file loads
   - Verify middleware runs on every request

**Expected time**: 15-30 minutes

---

## Integration Guidance for Agents

### SAP-020: API Integration

**When user has REST API**, integrate locale-aware headers:

```typescript
// lib/api.ts
import { getLocale } from 'next-intl/server';

export async function fetchData(endpoint: string) {
  const locale = await getLocale();

  const response = await fetch(`/api${endpoint}`, {
    headers: {
      'Accept-Language': locale,
    },
  });

  return response.json();
}
```

**Explain**: "API receives user's locale, returns translated content from database"

---

### SAP-041: Forms and Validation

**When user has Zod validation**, translate error messages:

```typescript
// lib/validation.ts
import { z } from 'zod';
import { useTranslations } from 'next-intl';

export function useValidationSchema() {
  const t = useTranslations('Validation');

  return z.object({
    email: z.string().email(t('emailInvalid')),
    password: z.string().min(8, t('passwordTooShort', { min: 8 })),
  });
}
```

**Explain**: "Validation errors now appear in user's language—better UX for non-English users"

---

### SAP-026: Accessibility

**When user needs accessibility**, add translated ARIA labels:

```typescript
import { useTranslations } from 'next-intl';

export function Button({ label }: Props) {
  const t = useTranslations('Common');

  return (
    <button aria-label={t(`${label}AriaLabel`)}>
      {t(label)}
    </button>
  );
}
```

**Explain**: "Screen readers announce buttons in user's language—crucial for blind users"

---

### SAP-031: Routing

**When user has Next.js routing**, use locale-aware Link:

```typescript
// navigation.ts (next-intl)
import { createSharedPathnamesNavigation } from 'next-intl/navigation';

export const { Link, redirect, usePathname } =
  createSharedPathnamesNavigation({ locales: ['en', 'es', 'ar'] });

// Usage
<Link href="/about"> {/* Automatically becomes /en/about, /es/about */}
  About
</Link>
```

**Explain**: "Links automatically prefix locale—no manual URL construction needed"

---

## Common Pitfalls for Agents

### Pitfall 1: Not Using CSS Logical Properties

**Problem**:
```typescript
// ❌ Hardcoded left/right (breaks in RTL)
<div className="ml-4 text-left">
  Content
</div>
```

**Fix**:
```typescript
// ✅ Logical properties (RTL-safe)
<div className="ms-4 text-start">
  Content
</div>
```

**Agent should always use logical properties** when RTL support is needed.

---

### Pitfall 2: Missing hreflang Tags

**Problem**: No hreflang tags → Google indexes duplicate content

**Fix**:
```typescript
// app/[locale]/layout.tsx
export async function generateMetadata({ params: { locale } }) {
  return {
    alternates: {
      languages: {
        'en': '/en',
        'es': '/es',
        'ar': '/ar',
        'x-default': '/en',
      },
    },
  };
}
```

**Agent should always generate hreflang** for multilingual sites.

---

### Pitfall 3: Not Testing RTL Layouts

**Problem**: RTL layout looks broken in Arabic

**Fix**: Always include RTL testing checklist:
- [ ] Switch to Arabic locale
- [ ] Verify text aligns right
- [ ] Check sidebar moves to right
- [ ] Verify arrows flip direction
- [ ] Test forms (labels on right)

**Agent should provide testing instructions** after RTL setup.

---

### Pitfall 4: Hardcoded Pluralization

**Problem**:
```typescript
// ❌ Fails in Arabic (6 plural forms)
const message = count === 1 ? '1 item' : `${count} items`;
```

**Fix**:
```typescript
// ✅ Uses CLDR rules (all languages)
t('items', { count });
// Translation: "{count, plural, =0 {no items} =1 {one item} other {# items}}"
```

**Agent should never use ternary** for pluralization—always use CLDR.

---

### Pitfall 5: Recommending Wrong Library

**Problem**: User asks for "i18n in Next.js" → Agent recommends react-i18next (misses next-intl benefits)

**Fix**: Always use decision tree:
- Next.js 15 App Router → next-intl (better integration)
- React Native → react-i18next (framework-agnostic)
- Need Server Components → next-intl (native support)

**Agent should ask clarifying questions** before recommending library.

---

## Performance Optimization Tips for Agents

### 1. Lazy Load Translation Namespaces

**When user has 100+ translation keys**:

```typescript
// Split by route
messages/
├─ en/
│  ├─ common.json      # Nav, footer (10 keys)
│  ├─ home.json        # HomePage (20 keys)
│  ├─ about.json       # AboutPage (15 keys)
│  └─ products.json    # ProductsPage (50 keys)

// Load only active namespace
const t = useTranslations('HomePage'); // Only loads home.json
```

**Explain**: "Splitting namespaces reduces initial bundle by 60%—only load what's needed"

---

### 2. Use Server Components for Translations

**When user has Next.js 15**:

```typescript
// ✅ Server Component (no client JS)
import { getTranslations } from 'next-intl/server';

export default async function Page() {
  const t = await getTranslations('HomePage');

  return <h1>{t('title')}</h1>;
}

// ❌ Client Component (requires client bundle)
'use client';
import { useTranslations } from 'next-intl';

export default function Page() {
  const t = useTranslations('HomePage');
  return <h1>{t('title')}</h1>;
}
```

**Explain**: "Server Components eliminate client-side JS—14KB bundle saved"

---

### 3. Static Generation for Locales

**When user has static content**:

```typescript
// app/[locale]/page.tsx
export function generateStaticParams() {
  return [
    { locale: 'en' },
    { locale: 'es' },
    { locale: 'ar' },
  ];
}

export default async function Page({ params: { locale } }) {
  // Pre-rendered at build time for all locales
  const t = await getTranslations({ locale });
  return <div>{t('content')}</div>;
}
```

**Explain**: "Static generation pre-renders all locales—zero runtime translation cost"

---

## Security Checklist for Agents

When implementing i18n, agent should ensure:

- [ ] **XSS prevention**: next-intl auto-escapes, react-i18next requires `interpolation: { escapeValue: false }` in React
- [ ] **Injection attacks**: Never use `dangerouslySetInnerHTML` with translations
- [ ] **Path traversal**: Validate locale parameter (`if (!locales.includes(locale)) notFound()`)
- [ ] **Open redirects**: Don't redirect to user-supplied locale URLs without validation
- [ ] **Translation file access**: Serve translation files from public CDN (not database) to prevent SQL injection

**Example**: Always validate locale parameter:

```typescript
// middleware.ts
const locales = ['en', 'es', 'ar'];

export function middleware(request: NextRequest) {
  const locale = request.nextUrl.pathname.split('/')[1];

  // ✅ Validate locale
  if (!locales.includes(locale)) {
    return NextResponse.redirect(new URL('/en', request.url));
  }

  return NextResponse.next();
}
```

---

## Documentation Navigation for Agents

### When to Read Each Artifact

| User Request | Artifact to Read | Why |
|--------------|------------------|-----|
| "What is SAP-038?" | AGENTS.md (this file) | High-level overview, decision tree |
| "Setup next-intl" | adoption-blueprint.md (Option A) | Step-by-step setup, 20 min |
| "Setup react-i18next" | adoption-blueprint.md (Option B) | Step-by-step setup, 20 min |
| "How to add RTL?" | protocol-spec.md (How-To 2) | Complete RTL guide |
| "Show me pluralization example" | protocol-spec.md (How-To 4) | CLDR pluralization patterns |
| "Why use next-intl vs react-i18next?" | capability-charter.md (Solution Design) | Library comparison |
| "How much time does this save?" | ledger.md (Time Savings Evidence) | Quantified metrics |

---

### Progressive Reading Strategy

**Small request** (e.g., "Setup locale routing"):
- Read: adoption-blueprint.md (relevant section only)
- Don't read: protocol-spec.md (too large), capability-charter.md (not needed)

**Medium request** (e.g., "Add i18n + RTL"):
- Read: adoption-blueprint.md + protocol-spec.md (How-To sections)
- Don't read: capability-charter.md, ledger.md

**Large request** (e.g., "Design i18n architecture for 20+ languages"):
- Read: capability-charter.md (Solution Design) + protocol-spec.md (full)
- Skim: ledger.md (production case studies)

---

## Quick Command Reference

### Installation

```bash
# next-intl
npm install next-intl

# react-i18next
npm install react-i18next i18next

# Tailwind RTL plugin (optional)
npm install tailwindcss-rtl
```

---

### Testing

```bash
# Run dev server
npm run dev

# Test locales
open http://localhost:3000/en
open http://localhost:3000/es
open http://localhost:3000/ar

# Test RTL
# Switch to Arabic, verify layout mirrors
```

---

### Translation Management

```bash
# POEditor
poeditor export --project-id 12345 --language en --output messages/en.json

# Crowdin
crowdin upload sources
crowdin download
```

---

## Example Agent Conversation

```markdown
User: "Add internationalization to my Next.js 15 app with Arabic support"

Agent (thinking):
- Task = i18n for Next.js 15
- Needs Arabic = RTL support required
- Next.js 15 App Router → recommend next-intl

Agent (Phase 1: Clarification - 2 min):
I'll help add i18n with Arabic support. A few questions:

1. How many languages total? (e.g., English + Arabic + ?)
2. Do you need SEO optimization (hreflang tags)?
3. Do you have existing translations or need to create them?

User: "English, Spanish, Arabic. Yes to SEO. Need to create translations."

Agent (Phase 2: Implementation - 20 min):
Perfect! I'll use next-intl (best for Next.js 15) with full RTL and SEO support.

1. Installing next-intl...
   [runs: npm install next-intl tailwindcss-rtl]

2. Setting up middleware for locale routing...
   [creates: middleware.ts with en/es/ar locales]

3. Creating translation files...
   [creates: messages/en.json, messages/es.json, messages/ar.json]

4. Configuring layout with RTL support...
   [updates: app/[locale]/layout.tsx with dir="rtl" for Arabic]

5. Adding SEO optimization...
   [generates: hreflang tags, locale sitemap]

6. Testing...
   ✅ /en/about → English content
   ✅ /es/about → Spanish content
   ✅ /ar/about → Arabic content (RTL layout)

Result: i18n setup complete! 3 languages with full RTL and SEO support.

Time: 20 minutes
Next steps: Add your translated content to messages/*.json files
```

---

## Integration Summary

| SAP | Integration | Command |
|-----|-------------|---------|
| **SAP-020** | Locale-aware API | Add `Accept-Language` header |
| **SAP-041** | Translated forms | `t('validation.emailInvalid')` |
| **SAP-026** | ARIA labels | `aria-label={t('button.close')}` |
| **SAP-031** | Locale routing | Use next-intl `<Link>` component |

---

## Version History

- **1.0.0** (2025-11-09): Initial release
  - Two-library architecture (next-intl, react-i18next)
  - Decision tree (3 questions)
  - 4 workflows (new project, locale routing, RTL, debugging)
  - Integration guidance (SAP-020, SAP-041, SAP-026, SAP-031)
  - Common pitfalls and fixes

---

**Status**: Pilot
**For**: All AI agents
**Estimated Setup Time**: 35 minutes
**Time Savings**: 88.3% (4-6h → 35min)
**Next Review**: After 3 validation projects
