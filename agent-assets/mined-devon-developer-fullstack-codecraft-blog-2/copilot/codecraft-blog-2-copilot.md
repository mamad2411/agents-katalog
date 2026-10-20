# GitHub Copilot Instructions — SvelteKit (Svelte 5, Runes-first)

> **Scope & placement**  
> Place this file at `.github/copilot-instructions.md`. These rules are **mandatory** for Copilot’s code suggestions, Copilot Chat, Copilot Code Review, and the Copilot Coding Agent.

---

## 1) Project framing Copilot must assume

- **Framework & mode:** SvelteKit (latest), Svelte 5 **runes** mode, **TypeScript** everywhere (`strict` recommended).
- **Directory conventions:**
  - Reusable **components, UI primitives, and utilities** live under `src/lib/**` (e.g., `src/lib/components`, `src/lib/ui`, `src/lib/utils`). Import via `$lib` and `$lib/server`.
  - Routes and pages live under `src/routes/**` using filesystem routing.
- **Testing:** Unit (Vitest), component (Testing Library for Svelte), E2E (Playwright).
- **Lints/format:** ESLint (TypeScript/Svelte plugins) + Prettier (repo configs are source of truth).
- **Accessibility:** WCAG 2.2 AA; use ARIA only when native semantics are insufficient.
- **Security:** Follow OWASP Top 10 basics; never commit secrets; validate env at startup.

> ✅ When Copilot scaffolds a component or utility, it **must place it in `src/lib/…`** (unless it’s route-local UI inside `src/routes`).

---

## 2) Runes-first state management (no Svelte stores)

- Do **not** suggest or generate `svelte/store` code (`writable`, `readable`, `derived`, `$app/stores`, etc.).
- Use **Svelte runes**—`$state`, `$derived`, `$effect`, etc.—for reactivity.
- **Share reactive logic** via **`.svelte.ts` modules**, which allow runes in regular TypeScript files and can be imported by components or other modules.
- **Encapsulate state** in a **class with `$state` fields** + methods, or keep module-private `$state` with exported getter/setter **functions**.  
  Do **not** export a bare `$state` variable directly.

> Project policy: standardize on **runes + `.svelte.ts` + class/accessor encapsulation** for all shared state.

### Required patterns Copilot must follow

**A. Class-based state module (`.svelte.ts`)**

```ts
// file: src/lib/state/counter.svelte.ts
export class Counter {
  value = $state(0)          // reactive class field
  inc = () => { this.value += 1 }
  reset = () => { this.value = 0 }
}

// Export a singleton by default (or export a factory if you need multiple counters)
export const counter = new Counter()

```
**B. Consuming in components**

```svelte
<!-- file: src/routes/+page.svelte -->
<script lang="ts">
  import { counter } from '$lib/state/counter.svelte'
</script>

<button onclick={counter.inc}>
  Count: {counter.value}
</button>
```
**C. Alternative: module-private state with accessors**

```ts
// file: src/lib/state/theme.svelte.ts
let mode = $state<'light' | 'dark'>('light')

export function getTheme() { return mode }
export function setTheme(next: 'light' | 'dark') { mode = next }
```

## 3) Routing, pages, and colocated code
- Pages are `+page.svelte`; layours are `+layout.svelte`; server endpoints are `+server.ts`.
- Use `load` functions in `+page.ts` or `+layout.ts` for data loading. Prefer server data loaded over client `onMount` fetches.
- Use `actions` in `+page.server.ts` for form handling.
- Route-specific helpers may live in that route's folder; **reusable** pieces belong in `src/lib/**`.
- **Server-only** code (e.g., DB clients, secrete usage) belongs under `src/lib/server/**` and must ot be imported into browser/client code.

## 4) File placement reules Copilot must enforce
- **Components/UI**: `src/lib/components/**` (or `src/lib/components/ui`). Name files with `.svelte` extension (import via `$lib` alias).
- **State & Services**: `src/lib/state/**` or `src/lib/services/**` (use `.svelte.ts` for runes support).
- **Server Utilities**: `src/lib/server/**` (e.g., DB clients, auth helpers). These must never be imported into client code.
- **Routes**: `src/routes/**` (use filesystem routing). Use `+page.svelte`, `+layout.svelte`, `+server.ts`, etc. as per SvelteKit conventions.

## 5) Coding style & best practices
- Use `async/await` for async code; avoid raw Promises.
- Prefer `fetch` API for HTTP requests; avoid external HTTP libraries unless necessary.
- Use `try/catch` for error handling; avoid unhandled rejections.
- Write clear, concise comments and JSDoc for complex logic. 
- Functions and variables should have descriptive names.
- Follow established linting and formatting rules (ESLint + Prettier).

**Specifics:**
- **TypeScript:** Use strict types; avoid `any`. Prefer interfaces and type aliases. Use generics for reusable functions.
- **Imports:** Prefer `$lib` alias over long relative paths.
- **Components:** Small and focused. Extract reusable parts to `src/lib/components/**`.
- **Events & Bindings:** Use **runes-mode idioms** (e.g., `onclick={...}`), not legacy Svelte directive sugar from older versions when runs mode provides clearer equivalents.
- **Accessibility:** Use semantic HTML elements first. Add ARIA attributes only when necessary. Ensure keyboard/focus flows and visible focus states.
- **Performance:** Keep inital payloads small; lazy-load heavy components; batch updates; use `$derived` runes to avoid unnecessary recomputations; streams where beneficial.
- **Security:** Validate inputs; never leak secrets; map errors to safe messages at boundaries.


## 6) What copilot must never do
- Never suggest or generate `svelte/store` code or patterns.
- Never place reusable components or utilities inside `src/routes/**`.
- Never import server-only code into client/browser code.
- Never export a bare `$state` variable directly from a module; always wrap in a class or use accessor functions.
- Never introduce React, Vue, Angular, or other framework code or idioms. All non-Svelte code must be framework-agnostic TypeScript/JavaScript.

## 7) Example scaffolds Copilot may emit
**Reusable UI Component (correct placement)**

```svelte
<!-- file: src/lib/components/Button.svelte -->
<script lang="ts">
  export let kind: 'primary' | 'secondary' = 'primary'
  let { children } = $props()
</script>

<button data-kind={kind} class="btn">
  {@render children()}
</button>
```
**Route using a lib component**

```svelte
<!-- file: src/routes/settings/+page.svelte -->
<script lang="ts">
  import Button from '$lib/components/Button.svelte'
</script>

<h1>Settings</h1>
<Button kind="primary">Save</Button>
```

**Server-only helper**

```ts
// file: src/lib/server/db.ts
import { DATABASE_URL } from '$env/static/private'

export function connect() {
  // server-only client init here
}
```

## 8) PR & Code Review Expectations (for Copilot Agents/Review) 
- Open **minimal, focused** PRs.
- Include in PR description: problem, solution, before/after behavior, tests added/updated, and manual verification steps (commands).
- Respond to review comments with concrete code updates and a short rationale. 
- Fix lints/CI before re-requesting review.

## 9) Maintainability Checklist (Copilot must self-check before proposing code)
- [ ] New reuable UI lives under `src/lib/components/**`. and uses `$lib` imports.
- [ ] No `svelte/store` usage; uses runes and `.svelte.ts` modules for shared state.
- [ ] No server-only code imported into client/browser code.
- [ ] Types are strict; no `any`.
- [ ] Async code uses `async/await` with `try/catch`.
- [ ] Accessibility best practices followed.
- [ ] Code is well-commented and clear.
- [ ] Shared state exported via class instance or accessor functions from a `.svelte.ts` module.
- [ ] Routes follow SvelteKit conventions with `+page.svelte`, `+layout.svelte`, `+server.ts`, etc.
- [ ] Tests are included for new functionality.

## Appendix -- How Copilot should interpret these rules
- Treat this document as **authorative** for all SvelteKit + Svelte 5 + runes-mode coding in this repo. If the repository code conflicts with these rules, prefer the rules and propose incremental refactors to align the codebase.
- Keep suggestions **concise, focused, scoped, and reversible**. Avoid large scaffolds unless explicitly requested.
- When in doubt, prefer **clarity, maintainability, and correctness** over brevity or cleverness.
- Ask for clarifications if the user request is ambiguous or conflicts with these rules.

