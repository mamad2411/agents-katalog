---
name: lane-frontend
description: Frontend build lane of a delivery run — sibling/wrapper-mirror premise, intent, prior-art and data-sensitivity gates, the UI design slice, generate rules, lens set by tier, nav-speed/SEO/a11y/i18n validation, spec conformance. Read by @architect, @implementer and /add-feature; not run on its own.
kind: skill
pack: delivery
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# lane-frontend — the frontend build procedure of a delivery run

The stack-specific half of `/add-feature`, cut from the frontend pack's former `add-feature` body —
the orchestrator (`/add-feature`, delivery pack) owns the run, the tiers, the acceptance contract,
the human gates and the verdict; this skill owns how THIS stack builds a change. Read by
`@architect` (constraints and design slices), `@implementer` (one task at a time) and the
orchestrator (which lenses to dispatch, what to validate). Tier words below are run tiers
(`.claude/templates/governance/tiers.json`): T1 ≈ the former trivial, T2 ≈ standard, T3 ≈ heavy.

| Section | Run phase | Reader |
|---|---|---|
| Premise · Invariants · Phase 1 gates (intent, prior-art, data-sensitivity) · Standard inputs | P0–P2 | orchestrator, @product-analyst |
| Phase 2 — the frontend design slice | P4 | @architect |
| Phase 3 Retrieve · Phase 4 Generate · New-dependency gate · Sibling-shape halt · Standards gate | P6 | @implementer |
| Phase 5 Update | P6b | doc-writer / orchestrator |
| Phase 6 Validate · Spec conformance · Traceability | P7–P12 | orchestrator |
| Phase 7 Improve | P15 | orchestrator |

> **STACK ASSUMPTION**: see the frontend pack's `STACK.md`. Inline syntax in this file uses Vue 3 + PrimeVue + TypeScript for illustration; substitute your stack's primitives from `_extracted-idioms.md`.

## The Premise (read this first, internalize, do not deviate)

**Existing pages and components are the truth.** Real users ship against the project's existing surface every day. Every sibling page in the same module — every wrapper, composable, service, permission gate, lifecycle hook, locale-key shape — is the intentional pattern, unless explicitly deprecated.

**The agent's job is exactly this:**
1. Find a sibling page / component in the same module that does roughly the same thing (CRUD list, detail view, dialog, form).
2. Mirror its structure: shared wrappers (`<BaseModal>`, `<BaseForm>`, `<FormField>`, `<CrudActions>`, `<CrudPaginator>`), composables (`useCrud`, `useForm`), service layer (`BaseCrudService`), permission gates, lifecycle hooks (`onActivated` for KeepAlive caching), locale-key paths.
3. Add only the delta the new feature actually needs. Everything else: copy the sibling's shape silently.

**Why.** Most of any page in this project is scaffolding its siblings already settled — routing entry, layout import, fetch call site, loading/error/empty states, permission gate, locale-key path. A page that re-decides them produces one micro-divergence, and micro-divergences compound: nothing is shared, so nothing can be fixed once. The cost surfaces months later as a refactor budget nobody can fund. Measure the claim on THIS repo rather than quoting a ratio — diff two sibling pages and count what differs; that count is the real delta this lane is allowed to add.

**The agent ONLY asks the user when:**
- **No sibling page exists** (truly new shape — first list page, first wizard, first chart panel).
- **Requirements need a new shared wrapper** that doesn't exist yet (e.g., `<BaseDateRangePicker>` when only `<BaseDatePicker>` exists).
- **Framework-level decision** (new state library, new router pattern, switch from CSR to SSR).

That's it. Three escalation triggers. Everything else — style, error handling, loading state shape, i18n key naming, focus management, empty-state copy — is silent sibling-mirror. No "do you want option A or B" prompts mid-run. Pick the sibling, mirror it.

## Invariants

- **Zero placeholders** in output. Every file has real content. No `<TODO>` comments.
- **New npm dependency is gated** — a package no sibling already imports halts for a dependency review (maintenance / license / bundle-size / supply-chain) before it lands. No silent `npm install`, any tier. See Phase 4 § New-dependency gate.
- **All relevant patterns consulted** — not just principles, specific pattern docs (`ai/patterns/forms.md`, `rendering-strategy.md`, `i18n.md`, etc.).
- **All applicable agents dispatched** — `ui-architect` designs; `ui-reviewer` reviews (carrying the framework-specific lens — Vue/React/Svelte/etc.); `@ux-reviewer` *(ui-ux pack)* judges WCAG and UI states, with `@accessibility-auditor` as the fallback when ui-ux is not installed; `i18n-auditor` if i18n in scope.
- **Signal-aware** — RTL locale detected → RTL audit fires. SSR detected → ssr-safety pattern consulted. Multi-theme detected → `@design-system-guardian` *(ui-ux pack)* audits, or — when that pack is absent — the theme lane is reported `UNREVIEWED(theme) — design-system-guardian not installed (ui-ux pack)` and the run is INCOMPLETE; it is never self-graded.
- **Zero unverified UI ships.** Real Playwright/Cypress test or, at minimum, manual checklist with screenshots.
- **Accessibility from the start, not retrofitted.** WCAG 2.2 AA is the floor.
- **i18n from the start, not retrofitted.** No hardcoded user-facing strings.

## Phase 1 — Understand (run P0–P2 — what this lane adds)

### Spec-driven branch (when given a spec path / Spec-ID)

If the argument is a path under `specs/` (or a `Spec-ID`), READ that spec **in full** and treat it as the requirements **CONTRACT**. Ingest every section, not just stories + AC:

- **User stories + acceptance criteria** — each AC carries an AC-ID; these drive the traceability rebuild (Phase 6).
- **Traceability table** — AC-ID → component/screen/test mapping; this is the seed for the Phase 6 AC→test map.
- **Affected modules, components/screens/state, API consumed, Test plan, Out-of-scope.**
- **a11y requirements** — each becomes a Phase 6 axe/keyboard conformance check.
- **i18n requirements** — each becomes a Phase 6 both-locale check.
- **NFR / perf-budget** — bundle-size ceilings, LCP/INP/CLS targets, route-timing budgets, **navigation budgets** (route prefetch on primary nav links, instant-loading route-change→paint target, streaming targets for SSR routes); each becomes a Phase 6 bundle-size/LCP/nav-speed gate.
- **Authorization & data-sensitivity** — per-role access rules + sensitive-field handling; each rule becomes a Phase 6 unauthorized-access test.
- **Observability** — required error/analytics/RUM signals; each must be matched by a wired signal in Phase 6.
- **Rollout** — flag strategy, staged exposure, rollback path; carried into the Phase 6 release note.
- **Success metrics** — each must be instrumented (event wired) or explicitly deferred in Phase 6.
- **Sizing signal** — the spec's own complexity estimate; seeds the run tier (see § Sizing-signal seeding below).

Do NOT re-derive requirements the spec already contains; proceed to design/generate from the spec (skip the Standard-inputs re-interview below). Still run the prior-art gate, the sibling-shape halt (Phase 4), and the new-dependency gate (Phase 4).

**Sizing-signal seeding.** The spec's **Sizing signal** seeds the run tier (`risk-tier.py --request-file=<spec>`); the seed is **promotion-only** — a stronger local signal (accessibility-critical surface, framework-level decision, a T3 trigger) promotes, nothing demotes. The divergence lands in `run.json.tier_reasons`.

**Open-questions HALT invariant.** If the spec carries unresolved **Open questions**, HALT before Phase 4 (Generate). Surface them and require resolution (answer recorded back to the spec, or an explicit accept-with-assumption from the user) before any code is generated. Unresolved open questions are a hard stop, not a warning.

Otherwise (bare description) proceed with the existing flow below.

### Intent gate (mandatory pre-step)

Before anything else, parse the user's description for **enhancement / fix / bug** keywords that indicate a different command is the right choice. Halt with a redirect message rather than start an add-feature flow on a request that's not actually adding a feature:

| User description contains | Right command | Action |
|---|---|---|
| "enhance" / "improve" / "polish" / "cleaner" / "better look" / "refine the design" / "redesign" / "match colors" / "fix padding" | `/enhance-ui` *(ui-ux pack)* | Halt; suggest `/enhance-ui <description>` — or `/polish` (core) if ui-ux is not installed |
| "align" / "convention" / "drift" / "cleanup" / "remove duplication" | `/align-recheck` *(align pack)* | Halt; suggest `/align-recheck <description>` — or `/align` (core) if that pack is not installed |
| "fix" + ("bug" / "broken" / "wrong" / "crash" / "error") — when the issue is incorrect behavior, NOT visual polish | `/fix-bug` | Halt; suggest `/fix-bug <description>` |
| "audit" / "review" / "inspect" — without intent to change code | `/frontend-audit` (this pack; `/a11y-audit` and `/i18n-audit` are its presets), then `/frontend-fix` to close what it finds; `/design-review` *(ui-ux pack)* | Halt; suggest the right read-only audit |
| "iterate" / "try variants" / "few options" — visual exploration | `design-iterate` skill *(ui-ux pack)* | Halt; suggest "use design-iterate skill on <path>" — absent that pack, `/polish` (core) |
| "add" / "new" / "create" / "build" / "implement" — actually adding new feature work | `/add-feature` (the delivery run) | Proceed |

If the description is ambiguous, ASK the user one clarifying question: "are you adding new functionality, or improving existing UI/UX?" Then route based on the answer.

If the user explicitly insists on `/add-feature` for an enhancement task (e.g., "no, run add-feature anyway"), proceed but flag in the run summary that a redirect was suggested but overridden.

### Prior-art gate (mandatory, all tiers)

The intent gate above routes the *request*. This gate checks the *capability*: **does the page / flow / component already exist** under another name? Sibling search finds a shape to copy — it does not tell you the feature is already shipped on another route.

1. Search by **behavior, not name** — existing routes, page components, composables, or services that already cover the user-facing capability (a "saved filters" feature may already live inside an existing list page's `useCrud` state).
2. **Near-duplicate found → HALT.** Surface the existing surface (route + what it does) and ask: extend it, replace it, or ship a deliberate parallel (rare — record the rationale inline).
3. Nothing matches → continue.

### Data-sensitivity gate (mandatory, both branches, before the tier is final)

The spec-driven branch above ingests **Authorization & data-sensitivity** as one of its spec sections. That lens is not a property of having a spec — it is a property of the data, so it runs here too, on every run, before the tier is chosen.

**Does this feature touch a credential, a payment instrument, a government or tax identifier, a health / biometric record, or a third-party access token?**

- **No** → continue; nothing below changes.
- **Yes** → three consequences, none of them optional:
  1. **The run promotes to T3** (`risk-tier.py --run=<id> --write`; signal `pii` or `money-movement`), regardless of how sibling-shaped the surface looks. This is the promotion that makes the security lens reachable at all.
  2. **The value is held by reference, never by value.** The capture surface is the provider's hosted / tokenised primitive (payment element, identity widget, signed upload); the repo stores a token. A repo-owned input bound to the repo's validation schema is a **HALT**, not a design choice, and the fact that a sibling already does it makes it a defect to report rather than a shape to mirror.
  3. **Every derived surface inherits the restriction** — the field is not a table column, not a filter, not a fixture value, not a log line, not an analytics property. `/add-crud-page` § Phase 1 carries the full surface-by-surface branch; this lane follows it rather than restating it.

Record the outcome in the run summary either way: `data-sensitivity: none` or `data-sensitivity: <class> — captured via <provider primitive>; run promoted to T3`.

### Standard inputs

Ask (one consolidated question if any of these unknown):

- **What is the user-facing feature?** Describe in plain language: what does the user see / do / accomplish?
- **What user roles use it?** (admin, customer, tenant member, anonymous, etc.)
- **What entry points?** New route? Existing route + new section? Modal/drawer over existing page?
- **What state lives where?** (component-local / store / URL / server)
- **What backend endpoints does it consume?** (existing or to-be-built)
- **Locales supported?** (en only, en+ar+RTL, ...)
- **Theme variants?** (light/dark/per-tenant brand)
- **Browser/device targets?** (mobile-first? desktop-first? PWA?)

If user provides a design (Figma link, screenshot) or written spec, treat it as authoritative.

Otherwise default to the project's prior conventions (read `ai/business-domain.md`, `ai/users-and-personas.md`, and the sibling components themselves — the component-shape contract lives in the sibling-shape halt below and in `@ui-architect` § Component API, not in a pattern file).

## Phase 2 — Organize: the frontend design slice (run P4 — @architect writes it into design.md)

`@architect` writes this slice into `design.md` (dispatching `ui-architect` for it when the frontend pack is installed). When the ui-ux pack is installed, `@ux-designer` has already written the flows and the state matrix into `ux.md` at P3: the architect reads them and leaves `## State matrix` out of this slice. Without ui-ux, the slice carries it, written in the `state-matrix` format (a row per surface × `THR-UI-STATES` state, `n-a` with a reason or the story or test that will force it). Shape:

```
## Feature: <name>

### Routes
| Path | Component | Layout | Auth | Roles |
|---|---|---|---|---|
| /orders/new | NewOrderPage | DefaultLayout | required | tenant_member |

### Components (new)
| Name | Path | Type | Props | Used by |
|---|---|---|---|---|
| OrderForm | components/orders/OrderForm.* | client | initialValues, onSubmit | NewOrderPage |
| OrderSummary | components/orders/OrderSummary.* | server (where applicable) | order | NewOrderPage |
| ProductPicker | components/orders/ProductPicker.* | client | onPick | OrderForm |

### State
| Concern | Where |
|---|---|
| Form values | useForm in OrderForm (component-local) |
| Selected products | OrderForm parent state |
| Submitted order | server response → routed to /orders/<id> |

### Server interactions
| Action | Endpoint | Mode | Cache strategy |
|---|---|---|---|
| List products | GET /api/products | server-component fetch | next.revalidate=60 |
| Submit order | POST /api/orders | server action / client mutation | invalidate /orders list on success |

### i18n keys (new)
| Key | en | ar |
|---|---|---|
| orders.new.title | New order | طلب جديد |
| orders.new.submit | Place order | إرسال الطلب |
| orders.new.error.product_required | Select at least one product | اختر منتجًا واحدًا على الأقل |

### A11y notes
- Form fields: associated `<label>`, `aria-describedby` for errors, `aria-invalid` on validation fail.
- Submit button: disable + aria-busy during submit; restore + announce result via live region.
- Modal/drawer (if used): focus trap; restore focus on close.
- Keyboard: every interactive element reachable via Tab; visible focus indicator.

### Tests
| Layer | File | Cases |
|---|---|---|
| unit | OrderForm.test.tsx | empty submit, valid submit, validation errors, currency formatting |
| component | OrderForm.spec.ts (Vitest+Testing Library) | render, interaction, submit handler invoked |
| e2e | orders/new.e2e.ts (Playwright) | full flow: arrive → fill → submit → land on /orders/<id> |
| visual | <if visual-regression in scope> | snapshot pre/post-fill, error state |

### Open questions
<anything you had to assume — flag for the user>

## State matrix
Surfaces:
- `new-order` — app/orders/new/page.tsx, components/orders/OrderForm.tsx

| Surface | State | Source | Expected (message · action · focus) | Proof |
|---|---|---|---|---|
| new-order | loading | AC-001 | product picker skeleton, aria-busy · — · — | components/orders/OrderForm.stories.tsx#Loading |
| new-order | error | AC-003 | "Couldn't load products" · Retry · focus on Retry | e2e/orders/new.e2e.ts::products error shows retry |
| new-order | pending-submit | AC-004 | "Placing order…" · submit disabled · inputs kept on 500 | components/orders/OrderForm.test.tsx::one order per double click |
| new-order | offline | n-a | n-a — <why this state cannot occur on this surface> | — |
<one row per required state; the conditional states the surface has>
```

The `## State matrix` heading is an h2 on purpose: `state-matrix-lint.py` reads the first `## State matrix` section of `ux.md`, else `design.md`. Lint it before P4 closes (`--phase=design`: a named, not-yet-written test passes) — and gate G12 lints it again at P12, when every proof must exist.

## Phase 3 — Retrieve (run P6 — read before each task)

**MUST read** [`templates/governance/core-discipline.md`](../../../../governance/core-discipline.md) before generating code.

Read, in this order:

1. `CLAUDE.md` — declared stack, conventions, anti-patterns.
2. `ai/business-domain.md` + `ai/business-flows.md` — what the feature is doing in business terms.
3. `ai/users-and-personas.md` — who uses it.
4. `ai/conventions.md` — naming, structure, imports.
5. `ai/patterns/forms.md`, `ai/patterns/i18n.md`, `ai/patterns/rendering-strategy.md`, `ai/patterns/ssr-safety.md` — applicable patterns.
6. `.claude/rules/frontend-principles.md` (a11y + styling MUSTs live inside it) and `.claude/rules/i18n.md`; plus `ui-principles.md` *(ui-ux pack, when co-installed)*.
7. Sibling component folder (`components/<similar-feature>/`) — mirror its shape.
8. Framework reference: `references/<framework>.md` (next/nuxt/vue/svelte/angular).
9. Existing endpoints used: read controller signatures + DTOs to align types.

If `ai/_extracted-codebase.md` exists, read it for project-specific anchors (base components, design system primitives, store conventions).

## Phase 4 — Generate (run P6 — @implementer, one plan.md task at a time)

For each component / page / route in the design:

1. **Pre-flight injection.** Every generated file gets the standard pre-flight comment:
   ```
   <!-- Pre-flight: read ai/conventions.md, the design system primitives, sibling components in this folder. -->
   ```
2. **Anchor to the project's actual primitives.** If the project uses a UI library (PrimeVue / shadcn / Material / Chakra / Radix Themes / etc.), use ITS components. Don't hand-roll.
3. **Use ONE styling system.** If Tailwind is in use, don't introduce CSS modules. If CSS modules, don't sneak in Tailwind classes.
4. **Locale strings via i18n key, never hardcoded user-facing text.**
5. **State at the right layer.** Component-local for ephemeral (open/closed); store (Pinia/Zustand/Redux) for cross-component; URL for deep-linkable; server for source-of-truth.
6. **Server data via the project's pattern** — TanStack Query / SWR / native `fetch` in Server Components / `useFetch`. Don't introduce a new pattern.
7. **Form validation at the schema level** (Zod/Yup/class-validator), not inline.
8. **Server action / client mutation discipline** — Next.js Server Action with `"use server"` and Zod validation; or client mutation with optimistic update + rollback on error.

Lens set for this lane at P10 (gated by run tier; the orchestrator dispatches them in its one parallel fan-out):

- **T1:** `@ui-reviewer` only — convention adherence, prop types, no business logic in templates. The sibling-shape halt below is the primary gate.
- **T2:** add `@i18n-auditor` (if i18n in scope) and `@ux-reviewer` *(ui-ux pack)* for WCAG and UI states — `@accessibility-auditor` when ui-ux is not installed.
- **T3:** the full cascade — `@ui-reviewer`, `@ux-reviewer` (fallback `@accessibility-auditor`), `@i18n-auditor`, `@design-system-guardian`, `@security-auditor` (if auth/payment in scope — which the Phase 1 data-sensitivity gate guarantees is reachable: a sensitive surface promotes to T3 on data grounds, so it can no longer be T1 by virtue of mirroring a sibling). Run in parallel. `@ui-reviewer` carries the framework-specific lens (Vue/React/Svelte/etc.) — there is no separate per-framework reviewer agent.

If a named **agent, command, or skill** is not installed in this project, that lane is **not reviewed** — do not grade it yourself; the builder judging its own change is not a review. Label it `UNREVIEWED(<axis>) — <name> not installed (<pack> pack)` and end the run **INCOMPLETE**, naming the install that closes it (`/setup-project --include=<pack>`) — never silently skip the axis, never claim a reviewer that did not run, and never halt into a redirect target the project does not have.

### New-dependency gate (all tiers)

If implementing the feature pulls in an npm package **no sibling already imports**, it never lands silently — the cost on frontend is paid by every user on every page load.

- **Confirm it's actually new** — check `package.json` + lockfile; a sibling may already ship an equivalent (date lib, form lib, icon set). Reuse it.
- **Run a dependency review** (dispatch `security-auditor`): maintenance health, license, **bundle-size delta** (gzipped, and whether it tree-shakes), and whether a platform API or an already-installed primitive covers the need. Not installed → record those facts with the command that produced each (`npm view <pkg> time.modified license`, `npm audit`, the measured gzip delta) and report `UNREVIEWED(dependency) — security-auditor not installed (security pack)`; the run is INCOMPLETE.
- **Record the decision** — one PR line (T1 / T2) or an ADR (T3, or any auth / payment / crypto dep).

HALT on an unreviewed new dependency. Prefer the design-system / already-present primitive over a new package by default.

### Sibling-shape mechanical halt (mandatory, all tiers)

Before declaring success, the auditor compares the new page/component against ≥2 sibling files in the same module. Per gap, track `closed` (matches sibling shape) / `still-open` (divergent) / `regressed` (introduced a new break on an unrelated axis). The **per-file verdict** uses the shared vocabulary in [`templates/snippets/sibling-shape-halt.md`](../../../../snippets/sibling-shape-halt.md): all gaps `closed` → `aligned`; any `still-open` or `regressed` → `drifted` (HALT); no sibling to compare → `no-siblings` (escalate).

**Halt if any of:**

- Uses raw framework components where Base*-wrappers exist — raw `<Dialog>` instead of `<BaseModal>`, raw `<Paginator>` instead of `<CrudPaginator>`, raw `<Dropdown>` instead of `<BaseDropdown>`, raw `<form>` instead of `<BaseForm>`.
- Uses `onMounted` instead of `onActivated` on a route page (KeepAlive cache divergence — the sibling page caches across navigation; the new page silently re-mounts).
- Has i18n keys missing from one locale (`en.ts` ✓, `ar.ts` ✗ — silent break in the alt locale).
- Doesn't use the project's gold-standard composable (e.g., `useCrud` for list pages, `useForm` for forms).
- Default-true wrapper props left implicit when affordances should be hidden — removing a `@delete-selected` handler does NOT hide the underlying button; pass `:show-delete="false"` / `:can-delete="false"` explicitly.
- New file placed outside the module's existing path convention (e.g., `pages/orders/NewOrder.vue` when sibling lives at `views/orders/Form.vue`).

**Hard rule:** `gap_count_in != gap_count_closed` → HALT. Do not advance to Phase 5. Surface the open list: refix, or return `NEEDS_INPUT` (escalate the tier, or accept with an ADR). Any `regressed` → HALT. Any NEW gap surfaced by the audit → HALT.

This is the same `regressed` mechanism from `parity-auditor.md` § V2-structure conformance. No silent advance.

### Standards gate (mandatory, all tiers)

Run [`templates/snippets/standards-gate.md`](../../../../snippets/standards-gate.md) with the `web` baseline (plus `data` if the change adds a query, a schema or a local store). Select the fired rows before generating (they go into `plan.md § Constraints`) — for a feature that is usually WEB-1..WEB-12, QG-1, QG-3 on role-gated surfaces — and close each with evidence after Phase 6, before the Output block. The sibling governs shape; the baseline governs guarantees: a sibling page with no empty state, a raw `fetch` or a hardcoded colour is a defect to report and fix, not a shape to mirror. Any `UNMET` or `SKIPPED` row → INCOMPLETE.

## Phase 5 — Update (run P6b)

Gated by run tier. T1 writes only the bare minimum; ADR drafts are T3 opt-in (avoiding the "ADR-as-closure" anti-pattern):

- **T1:** `ai/status.md` § Recent Changes — one-line entry. Nothing else.
- **T2:** add `ai/modules.md` module entry + 1-paragraph sibling-shape note inline.
- **T3:** add `ai/patterns/<new-pattern>.md` (only if new pattern has ≥3 callsites) + `ai/decisions/<NNNN>-<slug>.md` (only if a framework-level decision was made — new state library, new router pattern, CSR↔SSR switch). `ai/dynamic/changelog.md` entry.

**When built from a spec — `Spec: <Spec-ID>` on ALL tiers.** The backreference is not gated by tier. Wherever this tier writes, the `Spec: <Spec-ID>` line goes with it:

- **T1:** on the `ai/status.md` § Recent Changes one-line entry (and in the run's output block).
- **T2:** the above + on the `ai/modules.md` module entry.
- **T3:** the above + on the `ai/dynamic/changelog.md` entry (and any ADR header it drafts).

The same `Spec: <Spec-ID>` line belongs in the PR description on every tier, so the shipped feature traces back to its source spec regardless of ceremony.

## Phase 6 — Validate (run P7–P11 — what this lane checks)

- Lint + type-check pass on all touched files.
- Unit tests pass; e2e test passes against running dev server.
- Bundle-size delta acceptable — measured with the `bundle-analyze` skill (in-pack; it is a skill, not an agent). No analyzer available → report the delta as `bundle: unmeasured`, never as `acceptable`.
- **Navigation-speed / streaming / instant-loading MUSTs verified** on every new route (frontend-principles, not optional) — via the `navigation-speed` (prefetch / Speculation Rules / bfcache / View Transitions), `streaming-ssr` (stream-the-shell boundary scan), and `lcp-audit` (LCP-resource priority hints) skills; field INP via `web-vitals-field` (authoritative; lab INP is a proxy) with per-interaction budget from the `inp-responsiveness` pattern. Framework specifics come from `references/<framework>.md` + these skills — keep this stack-agnostic. A missing MUST HALTs (see Spec-conformance gate).
- **SEO + asset MUSTs verified** on every new PUBLIC route (frontend-principles, not optional) — unique metadata + self-referencing canonical + OG/Twitter + page-appropriate JSON-LD via the project's own primitive, reciprocal `hreflang` for localized routes, and SSR/SSG/prerender (never CSR-only) — via `seo-audit` + `@technical-seo`; content images via `image-optimization` (format / responsive / dimensions-CLS / lazy-below-fold); web fonts via `font-optimization` (font-display / self-host / size-adjust fallback). A missing MUST on a public route HALTs. Admin/authenticated-only routes report `seo: n/a` explicitly.
- A11y automated check passes: `a11y-scan` §1 on every touched route-state, diffed against the baseline — no new serious or critical violation (`THR-A11Y.axe_gate`, gate G9). A Lighthouse accessibility score is not axe and not conformance; it is never the gate.
- **State matrix (G12):** `python3 .claude/skills/state-matrix/scripts/state-matrix-lint.py --run=ai/runs/<run_id> --base=<merge-base>` — every touched surface has every required state, and every cited story or test exists (ui-ux pack; `gate-check.py` runs the same lint as `G12 state-matrix`). Without ui-ux: `UNREVIEWED(states) — state-matrix not installed (ui-ux pack)`.
- Locale completeness — no missing keys for declared locales.
- **Live browser verification (default for any user-visible feature):**
  1. `dev-server-start` skill — boot the running app (idempotent; reuses already-running server).
  2. `verify-with-playwright` skill — drive the new feature through the Playwright MCP server: navigate → assert visible → fill form → assert success → screenshot. Multi-locale + multi-viewport when `i18n`/breakpoints declared.
  3. Console-error pass — zero errors on load; warnings logged to report.
  - Skipping live verification is allowed only for backend-shaped changes (API contracts, types, store internals) where no rendered surface changed. Use `--no-verify-browser` to opt out explicitly with rationale.
- **Observability sign-off** (gated on what the project ships — check `.claude/codebase-profile.md` / `CLAUDE.md` for an error-tracker / analytics / RUM layer):
  - Error tracking (Sentry / Bugsnag / equivalent) captures errors from the new routes/components — error boundary or handler wired the same way siblings wire it.
  - Route-level performance signal exists if the project records one (web-vitals / RUM route timing) — new route reports like siblings do. **Nav-speed parity:** the new route prefetches its primary inbound links AND ships an instant loading state (skeleton / streamed shell) the same way its siblings do — a sibling that prefetches + has a loading boundary while the new route does neither is drift (HALT, per the Sibling-shape mechanical halt). Verify via the `navigation-speed` / `streaming-ssr` skills.
  - Product analytics events added if siblings of this surface emit them (same naming convention).
  - No console.* left as the only failure signal on any error path.
  - If the project ships NO observability layer: note `observability: none configured` in the report — explicit, never silent.
- **Release note (T3 → `ai/runs/<run_id>/release.md`)**: one PR-description paragraph — feature flag or flagless-with-rationale, rollback path (flag off / revert), and what gets checked on staging/preview before production.

### Spec-conformance gate (spec-path only — HALT per unmet section)

When the run was built from a spec, every spec section ingested at P1 gets a frontend-specialized conformance check. Walk the sections one by one; **HALT on the first unmet requirement** — do not aggregate-and-ship. Per requirement:

- **Each a11y requirement → axe + keyboard test.** The requirement is met only when an automated axe assertion AND a keyboard-reachability/focus test cover it. Missing either → HALT.
- **Each i18n requirement → both-locale check.** Every required string resolves in BOTH declared locales (en + ar) at the same key path, verified rendered. Any locale gap → HALT.
- **Each perf-budget / NFR → bundle-size / LCP check.** Measure the actual bundle-size delta against the spec's ceiling and the rendered LCP (and INP/CLS if the spec sets them) against the spec's target. Over budget → HALT. **ALSO enforce the frontend-principles navigation-speed / streaming / instant-loading MUSTs on every new route the feature adds — regardless of whether the spec names them (they are mandatory MUSTs):** primary inbound nav links prefetch the route (`navigation-speed` skill — Speculation Rules / prefetch / bfcache safety, no `unload`/`beforeunload`); SSR routes whose above-the-fold doesn't depend on a slow query stream the shell (`streaming-ssr` skill); data-dependent routes paint an instant layout-stable skeleton with no CLS (`lcp-audit` skill for LCP-resource priority hints). AUTHORITATIVE field INP via the `web-vitals-field` skill (lab/Lighthouse INP is a synthetic proxy only); per-interaction budget via the `inp-responsiveness` pattern. Missing any MUST → HALT, same as over-budget.
- **Each Authorization rule → unauthorized-access test.** For every per-role rule the spec states, there is a test asserting the surface is denied/hidden for a role that should NOT have access (not just allowed for the role that should). Missing the negative test → HALT.
- **Observability → matched signal.** Each required signal (error capture, analytics event, RUM/route timing) is wired the way siblings wire it and verified emitted. Unmatched signal → HALT.
- **Each Success metric → instrumented OR deferred.** The metric's event is wired and firing, OR it is explicitly deferred with a recorded reason. Silently-absent metric → HALT.

If a named agent, command, or skill (`@accessibility-auditor`, `@i18n-auditor`, `@security-auditor`, `/enhance-ui`, `web-vitals-field`, ...) is not installed, that check is **not run** — do not grade it yourself; report `UNREVIEWED(<axis>) — <name> not installed (<pack> pack)` and the run is INCOMPLETE — never skip the section, never fabricate the output the missing artifact would have produced.

### Build-time traceability rebuild (spec-path only — HALT on any untested AC-ID)

`python3 .claude/scripts/trace-matrix.py <run_id> --phase=build` rebuilds the AC→test map from the live tests — do not trust the spec's traceability table as-written; it predates the code. For every **acceptance-criterion AC-ID**:

1. Resolve it to a **named test** (file + test name) that actually asserts it.
2. **HALT if any AC-ID has no test** — an untested AC-ID is an unmet contract, not a follow-up.
3. **Emit the AC→test map in the run output**, so the shipped feature's coverage is auditable line-by-line.

## Phase 7 — Improve (run P15)

- If a new pattern emerged → `/learn-from-task` to promote.
- If a stale convention was caught → propose update to `ai/conventions.md`.
- If an a11y/i18n drift was found → log to `ai/dynamic/drift-log.md`.
- If the feature involved a new external dependency → it was already gated in Phase 4; promote to ADR here if it's load-bearing or touches auth/payment/crypto.
- **If the implementation diverged from the spec** (a requirement was changed, dropped, or satisfied differently than written) → close the loop three ways, do NOT invent a new file:
  1. **Annotate the spec in place** — append a `Deviation: <what changed and why>` line to the affected spec section; if the divergence was reconciled (spec updated to match reality), use `Resolved: <how>` instead.
  2. **Queue the learning** — append the divergence to `ai/dynamic/feedback-learned.md` so the next spec authored avoids the same gap.
  3. **Surface in the PR** — list each `Deviation:` / `Resolved:` in the PR description so the reviewer sees spec-vs-code drift explicitly.

## Failure modes

- **Untyped server response leaking into UI.** Always type the boundary; align with backend DTO.
- **Hardcoded strings in templates.** Caught by `@i18n-auditor`. Pre-empt by writing keys first.
- **Hand-rolled component when system primitive exists.** Caught by `@design-system-guardian` *(ui-ux pack)*; absent that pack, caught by the sibling-shape halt's raw-primitive row in this lane.
- **State scattered.** State should have ONE home per concern; if it's drifting between component / store / URL, that's an architecture flag.
- **A11y added at the end.** Should be in Phase 1 invariants; if it's a Phase 6 patch, the design wasn't a11y-aware.
- **Server vs client boundary leak.** `"use client"` files importing server-only deps. Audit imports across the boundary.

## Hard rules (lane)

- **Sibling-mirror is the default closure.** New pages copy the shape of an existing sibling in the same module. Asking the user about cosmetic / wrapper-shape / lifecycle / i18n-key choices when a sibling answers them is a token-waste anti-pattern.
- **Default-true wrapper props are explicit.** Removing handlers without setting `:show-*="false"` / `:can-*="false"` is a default-true bug.
- **i18n keys land in BOTH locales** (typically `en.ts` + `ar.ts`) at the same path. Missing-locale = silent break.
- **Match shared wrappers, not raw components.** No raw `<Dialog>` / `<Paginator>` / `<Dropdown>` / `<form>` where `<BaseModal>` / `<CrudPaginator>` / `<BaseDropdown>` / `<BaseForm>` exist. This gate is **creation-time only** — sweeping drift that already shipped is `ui-design-sweep`'s `unify-component` verb *(ui-ux pack)* or the core `/unify-surfaces`, not this lane.
- **One styling system.** Pick at Phase 1; never mix.
- **Every user-facing string is a locale key.** No exceptions, even for "internal" tools.
- **Every form has schema validation at the boundary** (server action OR API endpoint), not just client-side.
- **Every Server Component fetch is explicit about cache.** `cache:` and `next.revalidate` set on every `fetch`.
- **Every Server Action validates input.** Zod or equivalent. Action is a public RPC surface.
- **Every interactive element keyboard-reachable + has visible focus.** A11y is a must.

## Related

- `/add-page` · `/add-component` · `/add-crud-page` (frontend pack) — the leaf commands; a task may call them with the dispatch contract of `lane-backend` § Dispatch contract.
- `/frontend-audit` (frontend pack; `/a11y-audit` and `/i18n-audit` are its presets) — the standalone read-only audit of what this lane validates; `/frontend-fix` closes its findings failing-first.
- `lane-backend` — the counterpart for the API a UI task consumes; cross-stack runs carry both lanes.
