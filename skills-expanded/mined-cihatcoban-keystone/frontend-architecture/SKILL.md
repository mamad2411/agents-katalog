---
name: frontend-architecture
description: Structures UI for correctness, accessibility and performance - state ownership, data fetching, components, accessible widgets, rendering budgets. Triggers - build the settings page, where should this component state live, page feels slow or jumps while loading, make this modal accessible, WCAG, form handling.
---

# Frontend Architecture

Most frontend complexity is misplaced state. A UI is a projection of state onto
pixels; when the state model is wrong, no amount of component refactoring
rescues it — you get synchronization bugs, spinners that never end, and
interfaces that are subtly wrong in ways tests do not catch.

## State: own it in one place

Classify every piece of state before choosing a tool.

| Kind | Example | Where it belongs |
|---|---|---|
| **Server state** | Records fetched from an API | A data-fetching layer with caching, staleness and revalidation — *not* hand-rolled into global state |
| **URL state** | Filters, tab, page, selected id | The URL. It is shareable, back-button correct and survives reload |
| **Local UI state** | Open/closed, hover, input draft | The component that owns the interaction |
| **Global client state** | Theme, auth session, feature flags | A small global store. Should be genuinely small |
| **Derived state** | Totals, filtered lists, validity | Computed at render. **Never stored** |

Two rules prevent most bugs: **server state is a cache, not your data**
(copying it into a global store creates two sources of truth that drift), and
**derived state is never stored** (a stored total is a total that can be wrong).

## Async state has four states, not two

Every remote interaction must render: **idle · loading · success · error** —
plus *empty* as a distinct success case, and *stale-while-revalidating* when
refetching. The universal failure is shipping loading and success, then
discovering in production that errors render a blank page and empty lists look
like a bug.

Also handle: out-of-order responses (a slow first request resolving after a
fast second — use the request's own key/abort), optimistic updates with a
rollback path, and retries that do not duplicate a write.

## Component boundaries

- Split by **responsibility**, not by size. A 300-line component doing one
  thing is fine; three 40-line components sharing hidden state are not.
- Keep data-fetching and presentation separable enough to render the visual
  states in isolation.
- Props are a contract: required means required, and a component that takes 15
  props is describing a missing abstraction.
- Colocate. A component, its styles, its tests and its local types live
  together; splitting by file *type* (`components/`, `styles/`, `hooks/`)
  scatters every change across the tree.

## Accessibility is a correctness requirement

Not a polish phase. Non-negotiable baseline:

- Semantic elements first: a `button` is a button. A clickable `div` loses
  keyboard access, focus, and assistive-technology semantics, then needs four
  attributes to imitate what the native element does for free.
- Every interactive element is reachable and operable by keyboard, with a
  visible focus indicator. Test by unplugging the mouse.
- Labels are programmatically associated with inputs; errors are announced and
  linked to the field.
- Contrast ≥ 4.5:1 for body text; never encode meaning in color alone.
- Focus is managed on route change, dialog open and dialog close.
- Respect `prefers-reduced-motion`.
- Automated checks (axe) catch roughly a third of issues. A keyboard-only pass
  catches most of the rest.

Widgets fail in predictable ways. Before building one, look it up:

| Widget | Start from | Must hold |
|---|---|---|
| Modal | Native `dialog`, opened modally | Named by its heading; focus in on open, back to the trigger on close; Escape closes |
| Show/hide | `details`, or a button with `aria-expanded` | State announced; content follows the button |
| Tabs | `tablist` / `tab` / `tabpanel` | Arrow keys between tabs, one tab stop, panel labelled by its tab |
| Autocomplete | Native `select` / `datalist` first | Focus stays in the input; result count announced |
| Form errors | Field + linked message | `aria-invalid`, message via `aria-describedby`, summary focused on failed submit |
| Toast / status | A live region present before the message | Polite by default; no action that exists only in an auto-dismissing toast |
| Route change | — | Title updated; focus to the new page's heading |

Each row's structure and keyboard script: `references/frontend-a11y-patterns.md`.
Run the keyboard script for every widget you build or change.

## In a specific framework

The rules above are framework-independent; where they live is not. After stack
discovery, read the project's framework section in
`references/frontend-framework-map.md` — it maps each rule here (state
kinds, cancellation, error states, focus, forms, code splitting, rendering
cost, component tests) to that framework's idiom and the trap that breaks it
there. Check the versions it was written against; if the project's framework
is not listed, apply this skill as written and say the lookup was missing.

## Performance budgets

Set them, put them in CI, and measure on a mid-range device on a throttled
network — not on the developer machine.

| Metric | Target |
|---|---|
| LCP | ≤ 2.5 s |
| INP | ≤ 200 ms |
| CLS | ≤ 0.1 |
| Initial JS (compressed) | ≤ 200 KB, budget enforced in CI |

Highest-leverage moves, in order: ship less JavaScript (code-split by route);
size and lazy-load images correctly; reserve space for async content (CLS);
avoid rendering large lists without virtualization; keep the main thread free
during interaction. Micro-optimizing re-renders is far down this list —
profile before touching it.

## Verifying UI

- **Query the way people do.** Component tests find elements by role, label
  and text — the way users and assistive technology do. A test that cannot find
  the button by its role has found an accessibility defect, not a test problem.
- **End-to-end tests for the few journeys that matter** — sign-up, checkout,
  the flow that would page someone — against a real build. Everything else
  lives in the faster tiers (`testing-strategy`).
- **Visual snapshots narrowly,** reviewed like code; a snapshot nobody reads
  approves every regression.
- **Profile before optimizing rendering.** The framework's profiler names the
  component and the cause; guessing adds memoization that can cost more than
  it saves.

## Forms

The most bug-dense area of most UIs. Decide explicitly: validation timing (on
blur, not on every keystroke, for errors), server-error mapping back to fields,
what happens on double submit, whether the draft survives navigation, and
whether the submit is idempotent. Native validation and semantics first.

## Design system adherence

Use the system's tokens for spacing, color, typography and radius. A one-off
hex value is a future inconsistency. If the system lacks something, extend the
system — do not fork it locally.

## Exit checklist

- [ ] Every state item classified; server state is not duplicated into a store
- [ ] No derived value is stored
- [ ] Loading, empty, error and stale states are all implemented and reviewable
- [ ] Out-of-order responses and double submits are handled
- [ ] Keyboard-only pass completed; focus visible and managed
- [ ] Every widget built or changed matches its pattern and passed its keyboard
      script; native elements used where they exist
- [ ] Framework idioms checked against the map for this project's framework
      and version, or the missing lookup reported
- [ ] Component tests query by role and label; end-to-end tests cover the
      critical journeys against a real build
- [ ] Labels associated; errors announced; contrast checked
- [ ] Performance budget defined and enforced in CI, measured throttled
- [ ] Design tokens used; no one-off values
