---
name: follow-lib-dompurify
description: Use dompurify/isomorphic-dompurify to sanitize HTML against XSS in every environment
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test
  - follow-lib-zod
  - follow-lib-arktype

---

## Goal

Use dompurify/isomorphic-dompurify to sanitize HTML against XSS in every environment

## Scope

Use when a task must render HTML from user input, CMS, markdown, or an untrusted source — setup, config, SSR, debugging, or best practices

Boundaries:
- Use this skill to sanitize HTML strings that will be injected into the DOM (innerHTML, `dangerouslySetInnerHTML`, Solid `innerHTML`, markdown output)
- Not general input validation — to validate form/API data use `/follow-lib-zod` or `/follow-lib-arktype`
- Not output encoding for URLs/text nodes — plain text needs no sanitize (the framework escapes it)

- Latest: `dompurify@3.4.16` (verified 2026-09-24)
- References: [apis](references/apis.md) 
## Execute

### 1. Install

> Goal: install the package per environment

1. Run `bun add dompurify` (runtime dependency)
2. v3 ships built-in TypeScript types (`dist/purify.cjs.d.ts`) — do not install `@types/dompurify` (v2 only)
3. SSR/Node: install `bun add isomorphic-dompurify` (wrapper on jsdom) or `bun add -D jsdom` and create the instance yourself
4. Worker runtimes (workerd/Cloudflare Workers): jsdom does not work — use browser-side sanitize or the Trusted Types path

### 2. Sanitize At Render Boundary

> Goal: always sanitize before injecting HTML into the DOM

1. Browser: `import DOMPurify from 'dompurify'` then `DOMPurify.sanitize(dirty)`
2. Inject via `el.innerHTML = clean` / `dangerouslySetInnerHTML={{ __html: clean }}` — always through sanitize
3. Node/Bun with jsdom:

```ts
import { JSDOM } from 'jsdom';
import DOMPurify from 'dompurify';

const purify = DOMPurify(new JSDOM('').window);
const clean = purify.sanitize(dirty);
```

4. Or use `import { sanitize } from 'isomorphic-dompurify'` for isomorphic code
5. Sanitize at a single boundary (before render/store) — do not scatter it across many places

### 3. Configure Allowlist

> Goal: restrict tags/attrs to the features you need

1. The default profile is safe enough for ordinary rich text — even without config it blocks script/event handlers
2. Define an explicit whitelist when accepting only a subset: `sanitize(dirty, { ALLOWED_TAGS: ['b','i','em','strong','a'], ALLOWED_ATTR: ['href'] })`
3. Use `USE_PROFILES: { html: true }` / `{ svg: true }` / `{ mathMl: true }` for predefined profiles
4. Use `FORBID_TAGS`/`FORBID_ATTR` for a blacklist on top of the default profile
5. Return a DOM node with `RETURN_DOM` / `RETURN_DOM_FRAGMENT` when you don't want a string
6. Use `RETURN_TRUSTED_TYPE: true` if the app enforces a Trusted Types CSP
7. `DOMPurify.setConfig(cfg)` for persistent config; check `DOMPurify.isSupported` for DOM support before use

### 4. Use Hooks For Post-Processing

> Goal: add attrs/targets via hooks without reducing security

1. `DOMPurify.addHook('afterSanitizeAttributes', (node) => { ... })` — e.g. force `target="_blank"` + `rel="noopener"` on links
2. `DOMPurify.removeHook(name)` / `removeAllHooks()` for cleanup — beware hooks are global state

### 5. Test And Verify

> Goal: prove XSS payloads are filtered

1. Test with basic payloads: `<script>`, `<img onerror=...>`, `javascript:` URLs, `<svg onload=...>`, mutation XSS (mXSS) patterns
2. Run `/run-verify` for lint, typecheck
3. Run `/run-test` if related tests exist
4. Check the latest official docs before using uncertain config — https://github.com/cure53/DOMPurify#readme

## Rules

- Never render raw HTML from user input without sanitize
- Sanitize at a single boundary before render — do not scatter across many places
- Watch `dangerouslySetInnerHTML`/Solid `innerHTML` — always through sanitize
- Sanitize markdown renderer output too (markdown is not a trust boundary)
- Never rely on regex/manual filtering instead of DOMPurify — parser-based only
- Use /run-verify if needed
- Use /run-test if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Every HTML point coming from an untrusted source passes `DOMPurify.sanitize()` before render
- Config/allowlist matches the actual features used — not over-permissive
- SSR/worker environments use the correct approach (jsdom or isomorphic-dompurify)
- Lint, typecheck, tests pass
