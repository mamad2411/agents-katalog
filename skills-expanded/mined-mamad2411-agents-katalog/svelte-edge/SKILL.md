---
name: svelte-edge
description: |
  Future-first guidance for writing modern Svelte 5 and SvelteKit 2 code.
  Use this skill whenever the user asks about Svelte, SvelteKit, or frontend code that is clearly Svelte.
  Default to modern Svelte 5 patterns, avoid legacy leakage, and keep SvelteKit architecture stable unless the user explicitly wants edge features or SvelteKit 3 preview work.
---

# Svelte Edge

## Purpose

Produce modern, coherent, production-safe Svelte 5 / SvelteKit 2 answers.

- **Stable-first.** Experimental features are opt-in only.
- **TypeScript-first** for new code unless the codebase clearly says otherwise.
- **Current non-legacy syntax first.** Inspect project versions, then target the newest documented stable pattern they support.
- **Never mix Svelte 4 and Svelte 5 syntax** in the same component.
- **Never recommend experimental flags as defaults.**

## Operating assumption

Assume the model already knows Svelte and web fundamentals. This skill is a correction and decision layer, not a beginner tutorial.

Read reference files to get the correct version gate, current API shape, and recommended pattern — not to learn what the concept is. Do not skip a reference file because the topic feels familiar; the file exists because this area changes and training knowledge drifts.

Read only the sections relevant to the task, not every file end-to-end.

- Spend context on current syntax, version gates, architecture boundaries, and failure modes.
- Prefer one production-shaped example over several introductory variants.
- Teach fundamentals only when the user's question shows they need them.

## Pre-answer gate

Before generating or changing Svelte code:

1. Inspect installed Svelte/SvelteKit/tooling versions and experimental flags when project files are available.
2. Classify the task as new code, legacy edit, explicit migration, edge feature, or audit.
3. Read every canonical reference required by the topic.
4. Choose one syntax generation and keep component, composition, events, state, and config coherent.
5. State version/flag blockers instead of silently substituting legacy syntax.
6. After material edits, run the project's checks — normally `npx sv check`, targeted tests, and relevant E2E coverage.

## Reference files — mandatory reading

**Do not rely on training knowledge for any topic below.**
Identify the relevant file from the table and read it with your file-reading tool before answering.
Reference files exist because APIs, version gates, and recommended patterns change — training knowledge drifts.

| Topic | File to read |
|---|---|
| `$state`, `$derived`, `$effect`, `$props`, `$props.id()`, `$bindable`, `$host`, callback props, `createEventDispatcher`, `bind:`, lifecycle, scheduling, stores interop, reactive classes, context, reactivity helpers | `references/runes.md` |
| `{#snippet}`, `{@render}`, `children`, snippet typing, dynamic components, `Component` typing | `references/snippets.md` |
| `{let ...}`, `{const ...}`, declaration-tag scope/reactivity, legacy `{@const}` | `references/declaration-tags.md` |
| `{@attach}`, `svelte/attachments`, `fromAction` | `references/attachments.md` |
| `svelte/motion`, `Spring`, `Tween`, `prefersReducedMotion`, `transition:`, `in:`, `out:`, `animate:`, easing, custom motion functions | `references/motion.md` |
| direct `await`, async `$derived`, `<svelte:boundary>`, `getAbortSignal()`, `fork(...)`, `hydratable(...)` | `references/async-svelte.md` |
| `untrack`, `flushSync`, typed HTML wrappers, `svelte/elements` | `references/runes.md` and `references/best-practices.md` |
| `mount`, `hydrate`, `unmount`, imperative roots, replacing `new Component(...)` | `references/imperative-api.md` |
| `load`, form actions, auth guards, server-only modules, env vars, `+server`, `$app/state`, routing, snapshots, shallow routing | `references/sveltekit.md` |
| testing strategy, Vitest, Playwright, Storybook | `references/testing.md` |
| pitfalls, anti-mixing, event modifiers, hydration caveats, raw HTML safety, `<svelte:element>` dynamic tags | `references/best-practices.md` |
| `sv create`, `sv add`, `sv migrate`, `sv check`, experimental add-on, `svelte-check` flags/toolchain gates | `references/cli.md` |

If two files overlap on a topic, the row above is authoritative.

## Reference files — on-demand only

Read these **only when the trigger condition is met**. Do not pull them for general Svelte questions.

| Topic | Trigger | File to read |
|---|---|---|
| migration from legacy Svelte / Svelte 4 | user asks about migration or upgrading from Svelte 4 | `references/migration.md` |
| ecosystem libraries, community packages, third-party tools | user asks about a library, package, or third-party tool | `references/libraries.md` |
| maintaining or refreshing this skill | user asks about updating the skill itself | `references/maintenance.md` |
| remote functions | user asks about `query`, `command`, `form`, or `prerender`; project contains `.remote.ts` / `.remote.js`; or `kit.experimental.remoteFunctions` is enabled | `references/remote-functions.md` |
| SvelteKit 3 preview, Kit 2 → Kit 3 migration | project resolves `@sveltejs/kit@3.0.0-next.*`; or user explicitly asks about SvelteKit 3, "Kit 3 preview", or migrating from SvelteKit 2 to 3 | `references/sveltekit-3-preview.md` |

## Working modes

### New code mode (default)
Modern Svelte 5: runes, declaration tags over legacy `{@const}`, snippets over slots, event attributes (`onclick`), attachments over actions, SvelteKit primitives (`load`, form actions, `+server`, `$app/state`). No experimental flags unless they materially improve the requested solution.

### Legacy edit mode
User gave an existing file for fix or local refactor.
- **Tiny fix in a legacy file:** preserve the existing style.
- **Local refactor:** modernize only if the touched file stays coherent.
- **Explicit migration/rewrite:** rewrite coherently in modern Svelte 5.

Never half-migrate into a hybrid.

### Edge feature mode
Only when one of: user explicitly wants the newest patterns, the project has experimental flags enabled, or the solution clearly benefits from async-first / remote functions.

You may recommend `compilerOptions.experimental.async`, `kit.experimental.remoteFunctions`, `kit.experimental.explicitEnvironmentVariables`, or `kit.experimental.handleRenderingErrors`. State clearly that they are experimental opt-in. Do not treat missing flags as bugs. Prefer stable primitives when they solve the problem cleanly.

### Audit mode
Only when explicitly asked for an audit, review, modernization pass, or health check. Categorize findings (see audit contract). Do not treat disabled experimental flags as bugs by default. Inspect versions and flags before judging compatibility.

## Non-negotiable rules

**Security and architecture:**
- Never `{@html}` with unsanitized user-controlled content
- Never put per-user mutable state in shared server module scope
- Never use `load` for side effects, writes, or mutations

**Anti-mixing in new components:**
- Never mix `export let` with `$props()`
- Never mix `on:` directives with modern event attributes
- Never mix `<slot>` with snippets (unless explicit migration work)
- Never mix legacy Svelte 4 syntax with Svelte 5 runes
- Never generate legacy `{@const}` when Svelte 5.56+ declaration tags are available
- Never introduce `createEventDispatcher`, `<svelte:component>`, `SvelteComponent`, `ComponentType`, or `ComponentEvents` in new code; use callback props, dynamic component values, and `Component`

**Defaults:**
- Do not proactively recommend legacy fallbacks
- Do not recommend remote functions as the default SvelteKit answer
- Do not present experimental flags as mandatory defaults
- Do not silently downgrade syntax. State the minimum version, or preserve the file's existing generation in legacy edit mode.

## Multi-topic triage

When a question spans topics, route by risk to correctness:

1. Security / unsafe HTML / server-state leakage / side effects in `load`
2. SvelteKit architecture and request boundaries
3. Svelte semantics and reactivity
4. Async component semantics
5. Composition patterns
6. Testing strategy

For mixed async-Svelte + SvelteKit questions: `async-svelte.md` owns `<svelte:boundary>` and direct `await`; `sveltekit.md` owns stable server architecture; `remote-functions.md` owns remote function request boundaries.

## Edge-feature guardrails

When recommending an edge feature:
- Explain the benefit in *this* project
- State the required flag and minimum version
- Mark it clearly as experimental
- Skip the recommendation if stable primitives already solve the problem

## Version gates

State minimum versions instead of silently downgrading syntax. Always verify project dependencies (e.g. `package.json`) before writing code.

**Major Baseline Floors:**
- Svelte 5: **Svelte 5.56.0+** (Template declaration tags baseline; legacy `{@const}` is banned)
- SvelteKit: **SvelteKit 2.70.0+** (`defineEnvVars` moved to dedicated `@sveltejs/kit/env` subpath)
- SvelteKit 3: **SvelteKit 3.0.0-next.0..13** (Treat as separate generation; read `references/sveltekit-3-preview.md` for specific floors)

**Critical Security Patch Floors:**
- `hydratable(...)` with user-controlled data: require **Svelte 5.55.7+** (escaped inline scripts)
- `transformError(...)` in boundaries: require **Svelte 5.53.5+** (CVE-2026-27902 unescaped comments XSS)
- Form action and remote function origin checks: require **SvelteKit 2.70.0+** (in non-production `NODE_ENV` builds)
- Remote form file input deletion: require **SvelteKit 2.69.1+** (prototype pollution fix)

For all minor feature version gates (e.g., specific runes, snippets, attachments, or remote functions), refer directly to the canonical topic files in `references/`.

## Audit output contract

For each finding in audit mode:

- `id`, `file`, `category`, `severity`, `confidence`
- `evidence` (specific quote or pattern)
- `why_it_matters`
- `recommended_change`
- `version_or_flag_blocker`
- `patch_scope`
- `canonical_owner` (which reference file the rule comes from)

**Categories:** `bug` | `modernization` | `experimental-opt-in` | `freshness` | `ecosystem-risk` | `documentation-gap`

**Severity:**
- `critical`: security, user-data leak, invalid server-state pattern, unsafe HTML, production-breaking guidance
- `high`: incorrect default, wrong version/flag, mixed-generation guidance in new code, incorrect async/server boundary
- `medium`: modernization gap, stale example, incomplete explanation that could mislead
- `low`: wording, clarity, minor consistency

## Component selection policy

Before writing a complex UI primitive from scratch (modal, popover, dropdown, combobox, datepicker, calendar, table, drag-drop, command palette, toast, sheet, carousel, rich-text editor, virtualized list):

1. Propose 1-2 existing libraries from `references/libraries.md` (load on demand) or discover via https://madewithsvelte.com
2. State Svelte 5 / SvelteKit support, maturity, fit, and measured or sourced bundle impact; say unknown when it has not been measured
3. Only build bespoke if no library fits the design intent, or if the need is simple enough that a library would be over-engineering

For pure layout, buttons, cards, hero sections, marketing blocks, and other static visual structure — write directly. Reach for libraries when behavior is complex or accessibility is non-trivial.

## Ecosystem recommendation policy

Before recommending a package from `references/libraries.md`, verify:
- Svelte 5 / current SvelteKit support is clear
- maintenance is active enough for the use case
- docs are alive and readable
- release history is recent enough for production
- source/repo is credible

If live verification is unavailable, name the checks that were not performed and frame the entry as a candidate to investigate, not as a verified recommendation. Never reuse a stale successful observation as if it were current.

Separate observations from judgments:
- A 404 or DNS failure describes that exact reference at that audit time; it does not prove the project is unavailable elsewhere.
- An old commit, low adoption, missing peer dependency, or unpublished package is a review signal, not an automatic viability verdict.
- If a package is absent from the shortlist, rediscover it from canonical package sources, recent official monthly posts, or Made with Svelte; absence is not a viability claim.
- Never use `dead`, `abandoned`, `unmaintained`, or `production-ready` without direct, dated evidence that supports that exact claim.

Frame ecosystem choices on separate axes: maturity (`established` | `current` | `experimental` | `unverified`), fit (`broad` | `exact` | `unverified`), and provenance (`official-svelte` | `official-other` | `vendor` | `community` | `unverified`). Treat the bundled file as a shortlist/watchlist, evaluate other discoveries live, and never present community packages as official Svelte defaults.

## Freshness policy

Validated baseline: **August 1, 2026** — Svelte **5.56.8**, SvelteKit **2.70.1**, `sv` **0.16.6**, `svelte-check` **4.7.4**. SvelteKit 3 preview coverage validated separately: `references/sveltekit-3-preview.md` tracks `3.0.0-next.0` through `next.13`.

Update version gates when official releases change minimums or feature status. Treat official docs and changelogs as authoritative; use monthly blog posts as discovery indexes. Review ecosystem entries more often than framework semantics — packages decay faster. When uncertain, state the version requirement rather than guess. For the refresh workflow, read `references/maintenance.md`.
