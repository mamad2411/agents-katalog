# SAP-038: Internationalization - Claude Agent Guide

**SAP ID**: SAP-038
**Version**: 1.0.0
**Status**: pilot
**For**: Claude Code, Claude Desktop, Claude API
**Last Updated**: 2025-11-09

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

This CLAUDE.md provides: Claude Code-specific workflows for implementing internationalization.

---

### When to Use This SAP

**Use SAP-038 when user requests**:
- "Add internationalization to my app"
- "Support multiple languages (English, Spanish, Arabic)"
- "Add Arabic with right-to-left layout"
- "Setup locale routing (/en/, /es/)"
- "Add SEO for international markets"
- "Translate my React app"

**Don't use SAP-038 when**:
- User wants server-side translation only (use API-level i18n)
- User wants translation management only (use POEditor/Crowdin directly)
- User needs locale-specific content (beyond language translation)

---

## Progressive Context Loading Strategy

Claude should load context progressively to optimize token usage:

### Phase 1: Orientation (0-10k tokens)

**Goal**: Understand requirements and recommend library

**Read**:
1. This file (CLAUDE.md) for overview
2. AGENTS.md for library decision tree

**Ask user**:
- "Are you using Next.js 15 App Router?"
- "How many languages do you need?"
- "Do you need RTL support (Arabic, Hebrew)?"
- "What's your expected scale?"

**Output**: Library recommendation (next-intl or react-i18next)

**Time**: 2-3 minutes

---

### Phase 2: Implementation (10-50k tokens)

**Goal**: Setup chosen library and integrate with app

**Read**:
1. `adoption-blueprint.md` - Step-by-step setup for chosen library
2. `protocol-spec.md` (relevant sections) - Code examples and API reference

**Generate**:
- Middleware for locale routing
- Translation files (en.json, es.json, ar.json)
- Layout with locale provider
- Language switcher component
- RTL support (if needed)
- Basic SEO (hreflang tags)

**Time**: 20-25 minutes

---

### Phase 3: Advanced Patterns (50-100k tokens)

**Goal**: Add pluralization, SEO, translation management

**Read**:
1. `protocol-spec.md` (How-To Guides section) - Advanced patterns
2. `AGENTS.md` (Integration section) - Cross-SAP patterns

**Generate**:
- CLDR pluralization patterns
- Number/date formatting
- Complete SEO optimization (hreflang, sitemaps)
- Translation management integration (POEditor, Crowdin)
- Integration with SAP-041 (Forms), SAP-026 (Accessibility)

**Time**: 30-60 minutes (depending on complexity)

---

## Library Decision Framework for Claude

### Decision Tree Prompt

When user requests i18n features, use this prompt:

```
I'll help you add internationalization. First, let me ask a few questions:

1. **Framework**: Are you using Next.js 15 App Router? (YES/NO)
2. **Languages**: How many languages do you need? (2-5, 5-10, 10+)
3. **RTL support**: Do you need Arabic, Hebrew, or Farsi? (YES/NO)
4. **Scale**: What's your expected scale? (<1k users, 1k-10k, 10k+)

Based on your answers, I'll recommend the best library:
- **next-intl**: Next.js 15 native, Server Components, type-safe
- **react-i18next**: Framework-agnostic, mature ecosystem, flexible
```

---

### Recommendation Matrix

| User Requirements | Recommended Library | Rationale |
|-------------------|---------------------|-----------|
| Next.js 15 App Router | **next-intl** | Native integration, type-safe, Server Components |
| React Native / Vite / Remix | **react-i18next** | Framework-agnostic, mature |
| Need Server Component support | **next-intl** | Native SSR, no client-side flicker |
| Need framework flexibility | **react-i18next** | Works with any React framework |
| Need full type safety | **next-intl** | TypeScript inference from JSON |
| Legacy project migration | **react-i18next** | Easier incremental adoption |

---

## Code Generation Patterns for Claude

### Pattern 1: next-intl Setup

**User request**: "Setup next-intl for my Next.js 15 app"

**Claude generates**:

1. **Install dependencies**:
```bash
npm install next-intl
```

2. **Create middleware**:
```typescript
// middleware.ts
import createMiddleware from 'next-intl/middleware';

export default createMiddleware({
  locales: ['en', 'es', 'ar'],
  defaultLocale: 'en',
});

export const config = {
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)'],
};
```

3. **Create translation files**:
```json
// messages/en.json
{
  "HomePage": {
    "title": "Welcome to {appName}",
    "subtitle": "Build amazing apps"
  }
}

// messages/es.json
{
  "HomePage": {
    "title": "Bienvenido a {appName}",
    "subtitle": "Crea aplicaciones increíbles"
  }
}
```

4. **Update layout**:
```typescript
// app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export default async function LocaleLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const messages = await getMessages();
  const isRTL = locale === 'ar' || locale === 'he' || locale === 'fa';

  return (
    <html lang={locale} dir={isRTL ? 'rtl' : 'ltr'}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

5. **Use in component**:
```typescript
'use client';

import { useTranslations } from 'next-intl';

export default function HomePage() {
  const t = useTranslations('HomePage');

  return (
    <div>
      <h1>{t('title', { appName: 'MyApp' })}</h1>
      <p>{t('subtitle')}</p>
    </div>
  );
}
```

**Explain to user**:
- "I've set up next-intl with locale routing (/en/, /es/, /ar/)"
- "Type-safe translations with IDE autocomplete"
- "RTL support automatically enabled for Arabic"
- "Next steps: Add translated content to messages/*.json files"

---

### Pattern 2: react-i18next Setup

**User request**: "Setup react-i18next for my Vite app"

**Claude generates**:

1. **Install dependencies**:
```bash
npm install react-i18next i18next i18next-browser-languagedetector
```

2. **Initialize i18n**:
```typescript
// lib/i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import en from '@/locales/en.json';
import es from '@/locales/es.json';

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      es: { translation: es },
    },
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
```

3. **Setup provider**:
```typescript
// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './lib/i18n';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

4. **Use in component**:
```typescript
import { useTranslation } from 'react-i18next';

export default function HomePage() {
  const { t, i18n } = useTranslation();

  return (
    <div>
      <h1>{t('home.title', { appName: 'MyApp' })}</h1>
      <button onClick={() => i18n.changeLanguage('es')}>
        Español
      </button>
    </div>
  );
}
```

**Explain to user**:
- "I've set up react-i18next with automatic language detection"
- "Languages persist in cookies/localStorage"
- "Easy to switch languages with i18n.changeLanguage()"
- "Next steps: Add translations to locales/*.json files"

---

### Pattern 3: RTL Support with Tailwind

**User request**: "Add RTL support for Arabic"

**Claude generates**:

1. **Install Tailwind RTL plugin**:
```bash
npm install tailwindcss-rtl
```

2. **Configure Tailwind**:
```typescript
// tailwind.config.ts
import rtlPlugin from 'tailwindcss-rtl';

export default {
  plugins: [rtlPlugin],
};
```

3. **Use logical properties**:
```typescript
export default function Sidebar() {
  return (
    <aside className="
      ms-4           {/* margin-start: 16px (left in LTR, right in RTL) */}
      me-8           {/* margin-end: 32px */}
      ps-2           {/* padding-start: 8px */}
      border-s-2     {/* border-start: 2px */}
      text-start     {/* text-align: start */}
      rtl:flex-row-reverse  {/* Reverse flex in RTL */}
    ">
      Sidebar content
    </aside>
  );
}
```

4. **Flip directional icons**:
```typescript
import { useLocale } from 'next-intl';

export function Icon({ name, flip = false }) {
  const locale = useLocale();
  const isRTL = locale === 'ar' || locale === 'he' || locale === 'fa';

  return (
    <svg className={isRTL && flip ? 'scale-x-[-1]' : ''}>
      {/* Arrow/chevron icons */}
    </svg>
  );
}
```

**Explain to user**:
- "I've set up full RTL support with Tailwind"
- "Layout automatically mirrors for Arabic, Hebrew, Farsi"
- "Use ms-, me-, ps-, pe- instead of ml-, mr-, pl-, pr-"
- "Directional icons flip automatically"

---

### Pattern 4: SEO Optimization

**User request**: "Add SEO for international markets"

**Claude generates**:

```typescript
// app/[locale]/layout.tsx
export async function generateMetadata({ params: { locale } }) {
  const t = await getTranslations({ locale, namespace: 'Metadata' });

  return {
    title: t('title'),
    description: t('description'),
    alternates: {
      canonical: `/${locale}`,
      languages: {
        'en': '/en',
        'es': '/es',
        'ar': '/ar',
        'x-default': '/en',
      },
    },
    openGraph: {
      locale: locale,
      alternateLocale: ['en', 'es', 'ar'].filter(l => l !== locale),
    },
  };
}
```

**Generate sitemap**:
```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next';

const locales = ['en', 'es', 'ar'];
const routes = ['', '/about', '/contact'];

export default function sitemap(): MetadataRoute.Sitemap {
  return routes.flatMap(route =>
    locales.map(locale => ({
      url: `https://example.com/${locale}${route}`,
      lastModified: new Date(),
      alternates: {
        languages: Object.fromEntries(
          locales.map(l => [l, `https://example.com/${l}${route}`])
        ),
      },
    }))
  );
}
```

**Explain to user**:
- "I've added hreflang tags for all locales"
- "Generated locale sitemap for search engines"
- "Added Open Graph locale tags for social sharing"
- "Verify in Google Search Console"

---

## Workflow Templates for Claude

### Workflow 1: New i18n Project (35 min)

**User**: "Add internationalization to my Next.js app (English, Spanish, Arabic)"

**Claude**:

1. **Clarify requirements** (5 min):
   ```
   I'll help add i18n with 3 languages. A few questions:

   1. Do you need Server Component support? (YES/NO)
   2. Do you need SEO optimization (hreflang tags)? (YES/NO)
   3. Expected scale? (<1k, 1k-10k, 10k+)
   ```

2. **Recommend library** (2 min):
   - Next.js 15 + Server Components → next-intl

3. **Setup library** (20 min):
   - Install next-intl
   - Create middleware for locale routing
   - Create translation files (en, es, ar)
   - Update layout with locale provider
   - Add language switcher

4. **Add RTL support** (5 min):
   - Install Tailwind RTL plugin
   - Configure logical properties
   - Add dir attribute to HTML

5. **Add SEO** (3 min):
   - Generate hreflang tags
   - Create locale sitemap

6. **Test** (5 min):
   - Visit /en, /es, /ar
   - Verify translations load
   - Check RTL layout (Arabic)
   - Verify hreflang tags

**Expected time**: 35 minutes
**Output**: Fully functional i18n with 3 languages, RTL, and SEO

---

### Workflow 2: Add RTL Support (10 min)

**User**: "Add RTL support for Arabic"

**Claude**:

1. **Check current i18n setup** (2 min):
   - Verify next-intl or react-i18next installed
   - Check if Arabic locale exists

2. **Install Tailwind RTL** (2 min):
   ```bash
   npm install tailwindcss-rtl
   ```

3. **Configure Tailwind** (2 min):
   ```typescript
   // tailwind.config.ts
   import rtlPlugin from 'tailwindcss-rtl';
   export default { plugins: [rtlPlugin] };
   ```

4. **Update layout** (2 min):
   ```typescript
   const isRTL = locale === 'ar';
   return <html dir={isRTL ? 'rtl' : 'ltr'}>{children}</html>;
   ```

5. **Test** (2 min):
   - Switch to Arabic
   - Verify layout mirrors

**Expected time**: 10 minutes
**Output**: Full RTL support with automatic layout mirroring

---

### Workflow 3: Add Pluralization (15 min)

**User**: "Handle plural forms for different languages"

**Claude**:

1. **Explain CLDR** (3 min):
   - Unicode CLDR standard
   - 6 plural categories (zero, one, two, few, many, other)
   - Arabic has all 6, English has 2

2. **Update translation files** (8 min):
   ```json
   // en.json
   {
     "items": "{count, plural, =0 {no items} =1 {one item} other {# items}}"
   }

   // ar.json (6 forms)
   {
     "items": "{count, plural, =0 {لا عناصر} =1 {عنصر واحد} =2 {عنصران} few {# عناصر} many {# عنصرا} other {# عنصر}}"
   }
   ```

3. **Use in component** (2 min):
   ```typescript
   t('items', { count: 5 }); // Automatic plural selection
   ```

4. **Test** (2 min):
   - Test counts: 0, 1, 2, 5, 11, 100
   - Verify correct plural form

**Expected time**: 15 minutes
**Output**: CLDR-compliant pluralization for all languages

---

### Workflow 4: Debug i18n Issues (15-30 min)

**User**: "My translations aren't loading"

**Claude**:

1. **Check translation files** (5 min):
   ```bash
   # Verify files exist
   ls messages/en.json

   # Verify JSON syntax
   cat messages/en.json | jq

   # Check namespace matches
   # Component: useTranslations('HomePage')
   # File: { "HomePage": { ... } }
   ```

2. **Check middleware** (5 min):
   ```typescript
   // Verify matcher excludes API routes
   matcher: ['/((?!api|_next|.*\\..*).*)']

   // Verify locales array
   locales: ['en', 'es', 'ar']
   ```

3. **Check layout** (5 min):
   ```typescript
   // Verify provider wraps children
   <NextIntlClientProvider messages={messages}>
     {children}
   </NextIntlClientProvider>
   ```

4. **Add logging** (5 min):
   ```typescript
   console.log('Locale:', locale);
   console.log('Messages:', Object.keys(messages));
   ```

5. **Test fixes** (5-10 min):
   - Clear browser cache
   - Hard refresh
   - Check Network tab

**Expected time**: 15-30 minutes
**Output**: Debugged and working i18n

---

## Integration Guidance for Claude

### SAP-020: API Integration

**When user has REST API**, add locale-aware headers:

```typescript
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

**Explain**: "Validation errors now appear in user's language"

---

### SAP-026: Accessibility

**Add translated ARIA labels**:

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

**Explain**: "Screen readers announce buttons in user's language"

---

## Common Pitfalls for Claude

### Pitfall 1: Not Using CSS Logical Properties

**Problem**:
```typescript
// ❌ Breaks in RTL
<div className="ml-4 text-left">
```

**Fix**:
```typescript
// ✅ RTL-safe
<div className="ms-4 text-start">
```

**Claude should always use logical properties** when RTL support is needed.

---

### Pitfall 2: Missing hreflang Tags

**Problem**: No hreflang tags → SEO issues

**Fix**:
```typescript
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

**Claude should always generate hreflang** for multilingual sites.

---

### Pitfall 3: Hardcoded Pluralization

**Problem**:
```typescript
// ❌ Fails in Arabic (6 forms)
const msg = count === 1 ? '1 item' : `${count} items`;
```

**Fix**:
```typescript
// ✅ Uses CLDR rules
t('items', { count });
```

**Claude should never use ternary** for pluralization.

---

### Pitfall 4: Not Testing RTL

**Problem**: RTL layout looks broken in Arabic

**Fix**: Always include RTL testing checklist:
- [ ] Switch to Arabic locale
- [ ] Verify text aligns right
- [ ] Check sidebar moves to right
- [ ] Verify arrows flip direction

**Claude should provide testing instructions** after RTL setup.

---

### Pitfall 5: Recommending Wrong Library

**Problem**: User has Next.js 15 → Claude recommends react-i18next (misses next-intl benefits)

**Fix**: Always use decision tree:
- Next.js 15 App Router → next-intl (better integration)
- React Native → react-i18next (framework-agnostic)
- Need Server Components → next-intl (native support)

**Claude should ask clarifying questions** before recommending library.

---

## Performance Optimization Tips for Claude

### 1. Use Server Components for Translations

**When user has Next.js 15**:

```typescript
// ✅ Server Component (no client JS)
import { getTranslations } from 'next-intl/server';

export default async function Page() {
  const t = await getTranslations('HomePage');
  return <h1>{t('title')}</h1>;
}
```

**Explain**: "Server Components eliminate 14KB client bundle"

---

### 2. Lazy Load Namespaces

**When user has 100+ translation keys**:

```typescript
// Split by route
messages/
├─ en/
│  ├─ common.json      # Nav, footer (10 keys)
│  ├─ home.json        # HomePage (20 keys)
│  └─ products.json    # ProductsPage (70 keys)

// Load only active namespace
const t = useTranslations('HomePage'); // Only loads home.json
```

**Explain**: "Namespace splitting reduces initial bundle by 60%"

---

### 3. Static Generation for Locales

**When user has static content**:

```typescript
export function generateStaticParams() {
  return [
    { locale: 'en' },
    { locale: 'es' },
    { locale: 'ar' },
  ];
}
```

**Explain**: "Pre-renders all locales at build time—zero runtime cost"

---

## Documentation Navigation for Claude

### When to Read Each Artifact

| User Request | Artifact to Read | Why |
|--------------|------------------|-----|
| "What is SAP-038?" | CLAUDE.md (this file) | Overview, decision tree |
| "Setup next-intl" | adoption-blueprint.md (Option A) | Step-by-step setup, 20 min |
| "Setup react-i18next" | adoption-blueprint.md (Option B) | Step-by-step setup, 20 min |
| "How to add RTL?" | protocol-spec.md (How-To 2) | Complete RTL guide |
| "Show pluralization example" | protocol-spec.md (How-To 4) | CLDR patterns |
| "Why next-intl vs react-i18next?" | capability-charter.md (Solution Design) | Library comparison |
| "How much time savings?" | ledger.md (Evidence) | Quantified metrics |

---

### Progressive Reading Strategy

**Small request** (e.g., "Setup locale routing"):
- Read: adoption-blueprint.md (relevant section only)
- Don't read: protocol-spec.md (too large)

**Medium request** (e.g., "Add i18n + RTL"):
- Read: adoption-blueprint.md + protocol-spec.md (How-To sections)
- Don't read: capability-charter.md, ledger.md

**Large request** (e.g., "Design i18n architecture"):
- Read: capability-charter.md (Solution Design) + protocol-spec.md (full)
- Skim: ledger.md (case studies)

---

## Quick Command Reference

### Installation

```bash
# next-intl
npm install next-intl

# react-i18next
npm install react-i18next i18next i18next-browser-languagedetector

# Tailwind RTL
npm install tailwindcss-rtl
```

### Testing

```bash
# Run dev server
npm run dev

# Test locales
open http://localhost:3000/en
open http://localhost:3000/es
open http://localhost:3000/ar
```

---

## Version History

- **1.0.0** (2025-11-09): Initial release
  - Two-library architecture (next-intl, react-i18next)
  - Progressive context loading strategy
  - Code generation patterns for both libraries
  - 4 workflow templates
  - Integration guidance (SAP-020, SAP-041, SAP-026)
  - Common pitfalls and fixes

---

**Status**: Pilot
**For**: Claude Code, Claude Desktop, Claude API
**Estimated Setup Time**: 35 minutes
**Time Savings**: 88.3% (4-6h → 35min)
**Next Review**: After 3 validation projects
