---
name: heroui-frameworks
description: >
  Integrate HeroUI v3 with Next.js (App Router, Pages Router) and Vite. Covers
  heroui-cli init, first Button usage, no-provider rule, Next.js locale/RTL via
  I18nProvider and isRTL, Accept-Language in root layout, and CSP nonce meta for
  React Aria. Use when scaffolding a HeroUI app, wiring Next.js layout providers,
  setting html lang/dir, Vite App.tsx setup, or framework-specific HeroUI install.
  Keywords: HeroUI frameworks, Next.js HeroUI, Vite HeroUI, I18nProvider, isRTL,
  heroui-cli init, App Router, Pages Router, csp-nonce. Use when the user runs
  /heroui-frameworks.
---

# HeroUI Frameworks (v3)

Integrate HeroUI v3 with Next.js and Vite. Components work after install + style import — **no `HeroUIProvider`**.

**Source:** https://heroui.com/en/docs/react/getting-started/frameworks

## Apply the Skill

- Read `references/frameworks.md` for full layout/provider code samples.
- Use this skill when scaffolding or wiring HeroUI into a framework app (Next.js App/Pages, Vite).
- For package install, Tailwind v4 CSS order, and per-component APIs, also use `heroui-react`.
- For semantic variants / composition policy, use `heroui-design-principles`.
- For v2 → v3 migrations, use `heroui-migration`.

## Non-Negotiables

| Do | Don't |
|----|--------|
| `npx heroui-cli@latest init` for framework templates | Assume v2 CLI / `HeroUIProvider` scaffolding |
| Import components from `@heroui/react` after styles are set up | Skip style import / Tailwind v4 setup |
| No provider required for basic UI | Wrap the app in `HeroUIProvider` (v2) |
| Next.js i18n: server `lang`/`dir` on `<html>` + client `I18nProvider` | Mismatch server locale vs React Aria locale |
| Use `isRTL(lang)` from `@heroui/react` for `dir` | Hardcode `dir` without locale awareness |
| CSP: `<meta property="csp-nonce" content="…">` for React Aria | Ignore nonce when CSP blocks styles/scripts React Aria injects |

## Work in This Order

1. **Scaffold** — `npx heroui-cli@latest init` → pick **App**, **Pages**, or **Vite** → install deps (`pnpm install`, etc.).
2. **First component** — Render a `Button` from `@heroui/react` in the framework entry page.
3. **Confirm no provider** — Only add client providers when needed (locale, theme toggles you own).
4. **Next.js locale (optional)** — Server layout reads preferred language → `lang` + `dir` on `<html>` → client `I18nProvider locale={lang}`.
5. **CSP (if used)** — Emit `csp-nonce` meta so React Aria can read the nonce.
6. **Next steps** — Themes, component catalog, or design principles as needed.

## Decision Rules

### Which template?

| Goal | Template |
|------|----------|
| Next.js App Router | **App** |
| Next.js Pages Router | **Pages** |
| SPA / Vite | **Vite** |

### Provider policy

- **Default:** no HeroUI root provider.
- **Optional Next.js:** client `I18nProvider` only for React Aria locale alignment — not a full design-system provider.

### Locale alignment (Next.js)

1. Resolve language on the server (`Accept-Language`, DB, URL, …).
2. Set `<html lang={lang} dir={isRTL(lang) ? 'rtl' : 'ltr'}>`.
3. Pass `lang` into a `"use client"` wrapper that renders `<I18nProvider locale={lang}>`.

### CSP

If Content-Security-Policy uses nonces, put the generated nonce in:

```html
<meta property="csp-nonce" content="{nonce}" />
```

React Aria reads this automatically.

## Quick patterns

### First component (App Router)

```tsx
// app/page.tsx
import { Button } from "@heroui/react";

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <Button variant="tertiary">Hello HeroUI</Button>
    </main>
  );
}
```

### First component (Vite)

```tsx
// src/App.tsx
import { Button } from "@heroui/react";

function App() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <Button variant="tertiary">Hello HeroUI</Button>
    </main>
  );
}

export default App;
```

### Next.js locale skeleton

```tsx
// app/layout.tsx (server)
import { headers } from "next/headers";
import { isRTL } from "@heroui/react";
import { ClientProviders } from "./provider";

export default async function RootLayout({ children }) {
  const acceptLanguage = (await headers()).get("accept-language");
  const lang = acceptLanguage?.split(/[,;]/)[0] || "en-US";

  return (
    <html lang={lang} dir={isRTL(lang) ? "rtl" : "ltr"}>
      <body>
        <ClientProviders lang={lang}>{children}</ClientProviders>
      </body>
    </html>
  );
}
```

```tsx
// app/provider.tsx
"use client";

import { I18nProvider } from "@heroui/react";

export function ClientProviders({ lang, children }) {
  return <I18nProvider locale={lang}>{children}</I18nProvider>;
}
```

## Anti-Patterns

- Requiring `HeroUIProvider` for any framework integration
- Setting `lang` on `<html>` but not wrapping with `I18nProvider` (or the reverse) when localization matters
- Using Pages Router examples under `app/` or App Router under `pages/` without adapting paths
- Forgetting install after `heroui-cli init`
- Treating Vite and Next the same for locale/SSR — Vite has no Next `headers()` layout pattern

## Reference Map

- Full framework steps and samples: `references/frameworks.md`
- Official docs: https://heroui.com/en/docs/react/getting-started/frameworks
- Raw MDX: https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(overview)/frameworks.mdx
- Related: Quick Start, Themes, Components on heroui.com
- Sibling skills: `heroui-react`, `heroui-design-principles`, `heroui-migration`
