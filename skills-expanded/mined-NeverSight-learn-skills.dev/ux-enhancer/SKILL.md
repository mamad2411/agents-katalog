---
name: ux-enhancer
description: 'Refactors React components for usability using Steve Krug''s "Don''t Make Me Think" principles — visual hierarchy, scanning-optimized layout, ruthless copy reduction, unambiguous CTAs, and proper loading/empty/error states. Use when a user shares a React component and asks to improve UX, reduce cognitive load, simplify copy, fix cluttered layouts, clarify navigation, or make an interface more intuitive. Triggers: "improve UX", "usability audit", "simplify this", "too much text", "make it cleaner", "users are confused", "apply Krug". Use proactively on settings pages, forms, modals, navigation, and any task-driven workflow. Skip for backend-only, perf-only, or pure styling/branding tasks (use frontend-design or impeccable instead).'
---

# UX Enhancer

A UX refactor specialist for React components. The job is to remove cognitive friction — not to redesign the feature, not to add abstractions, not to "improve" the architecture.

## North star

Steve Krug's first law: **Don't make me think.** A first-time user should navigate the screen correctly with zero training. If they have to pause, re-read, or hunt for the primary action, the design failed.

Three operating principles, in priority order:

1. **Users scan, they don't read.** Optimize for the 3-second glance.
2. **Users satisfice.** They pick the first plausible option, not the best one. Make the right choice the most prominent one.
3. **Users muddle through.** They don't understand your model. Conventions over cleverness.

## When to use this skill

**Use it when:**
- A React component shared with intent to improve usability, copy, hierarchy, navigation, forms, or states.
- A component has instruction paragraphs, ambiguous CTAs, dense walls of text, or missing empty/loading/error states.
- The user mentions cognitive load, scannability, "Don't Make Me Think," or asks "why is this confusing?"

**Skip it when:**
- Backend / API / DB / business logic only — no UI to refactor.
- Pure performance work (memoization, bundle size) — use `vercel-react-best-practices`.
- Visual branding, animation polish, or building a landing page from scratch — use `frontend-design` or `impeccable`.
- The user wants a fresh design from a brief — this skill *refactors existing* UI.

## Workflow

Run these steps in order. Don't skip steps.

### 1. Understand the user's task

Read the component. Answer in your head:
- What screen is this? (Settings? List? Form? Modal?)
- Who is the user? (Admin? Customer? Internal staff?)
- What is the user trying to do here?

If this isn't obvious from the code, ask one clarifying question before refactoring.

### 2. Identify the primary action

Every screen has one most-important thing the user came to do. Find it. The refactor must make that action the most prominent visual element on the screen.

If you can't identify a primary action, the screen is doing too much — flag it as a structural issue rather than refactoring noise.

### 3. Audit cognitive friction

Walk the **red flags checklist** (below) AND the smell catalog at `references/component-smell-catalog.md`. Note every hit. Don't fix yet — just inventory.

**Triage rules:**
- Sort hits by severity: Blocker → High → Medium → Low.
- Fix Blockers and High first. Do not refactor cosmetic / Low issues while a Blocker exists.
- Tie every major change in the output bullets to a specific smell name (e.g. "Vague button smell") or a Krug principle.

### 4. Refactor in this order

1. **Cut copy** — happy talk, instructions, verbose labels. Half the wins live here.
2. **Fix hierarchy** — promote primary, demote secondaries, group related, separate unrelated.
3. **Fix states** — loading, empty, error, success, disabled, pending all need explicit handling.
4. **Fix interactions** — clickability, current state indicators, hover-only behaviors.
5. **Tighten labels and microcopy** — verb of what happens, not the form mechanic.

### 5. Preserve the existing design system

Detect the project's DS (shadcn/ui, MUI, Chakra, Mantine, Ant Design, or custom) by scanning imports. **Use what exists. Do not invent new primitives.** If no fit, flag with `// New pattern — DS gap`.

### 6. Explain changes

Output the refactored code, then a 3–7 bullet list mapping each significant change to its cognitive-load reason or Krug principle. Specific. Tied to the code. No generic praise.

## Krug rules → React translations

| Krug rule | React translation |
|---|---|
| Pages should be self-evident | Title, primary action, and content type readable in 3 seconds without scrolling |
| Users scan, they don't read | Headings + lists > paragraphs. Equal-weight labels are a smell. |
| Conventions over cleverness | Top-left logo links home. Hamburger = nav. Magnifier = search. Don't reinvent. |
| Visual hierarchy beats decoration | Size, weight, spacing communicate importance — not gradients or icons |
| Clickable looks clickable | Buttons are buttons. Not text with `cursor: pointer` and a hover. |
| Cut needless words ruthlessly | Get rid of half. Then half again. |
| Kill happy talk | "Welcome to your dashboard!" → delete entirely |
| Navigation answers Where am I / What can I do / Where can I go | Active page indicator, breadcrumb when ≥2 levels deep, persistent main nav |
| Page titles match clicked links | If the user clicked "Patients," the page H1 says `Patients`, not `Patient management` |
| Forms are forgiving and obvious | Labels above fields, inline validation, retain user input on error |
| Empty/loading/error guide next action | Never blank, never silent, never dead-end |
| Mobile: no hover-only, big tap targets | 44×44px min, all hover affordances also tappable |
| Accessibility is part of usability | Semantic HTML, labeled controls, focus visible, color not the only signal |
| Don't waste user time | One click better than two. One word better than two. |

## Red flags checklist

Inventory all hits before refactoring.

**Copy smells**
- [ ] "Welcome to..." or other happy talk paragraphs
- [ ] Instruction paragraph above a form
- [ ] Field labels longer than 3 words
- [ ] Buttons labeled `Submit`, `OK`, `Confirm`, `Click here`
- [ ] Sentence-form labels: "Please enter your..."
- [ ] Duplicate copy: tab label = page heading = card title
- [ ] Marketing voice in product UI ("amazing," "powerful," "simply")

**Hierarchy smells**
- [ ] Multiple H1s, or no H1
- [ ] Primary CTA visually equal to secondaries
- [ ] All buttons same color/weight
- [ ] Decorative emphasis (gradients, glows) competing with real CTAs
- [ ] Sidebar with 15+ flat items, no grouping

**Interaction smells**
- [ ] Text styled to look like a link, but isn't (or vice versa)
- [ ] `cursor: pointer` on a non-button div
- [ ] Hover-only menus, tooltips with critical info, hover-only edit buttons
- [ ] Modal with X-only dismiss (no Cancel + primary)
- [ ] Destructive action (Delete, Remove) styled identically to safe ones
- [ ] No focus ring / focus invisible

**State smells**
- [ ] Inline `<Spinner />` with no context label
- [ ] Empty state shows blank or `No results`
- [ ] Errors render as raw strings or `Error: undefined`
- [ ] Disabled buttons with no explanation
- [ ] Async actions with no pending state

**Navigation smells**
- [ ] No active state on current nav item
- [ ] Breadcrumb missing on deep page
- [ ] Page H1 doesn't match the nav label that led here
- [ ] Back button mystery — unclear what it goes back to

## What NOT to do

The refactor stays in scope. Hard rules:

- **Don't redesign the feature.** If the spec says "patient profile form," output a patient profile form. Not a wizard, not a stepper, not a tabs view.
- **Don't add abstractions.** No new hooks, no `useFormReducer`, no extracting "for reuse" unless the original was already duplicated.
- **Don't rewrite business logic.** `handleSubmit` stays as-is unless it's the cause of the UX problem.
- **Don't add dependencies.** No new packages. Use what's imported.
- **Don't introduce a design system.** If none exists, suggest primitives in comments — don't ship a `Button.tsx` file.
- **Don't add features the user didn't ask for.** No extra validation rules, no autosave, no keyboard shortcuts.
- **Don't moralize.** No paragraphs about why the original was bad. The diff speaks.

## Forms checklist

- [ ] Labels above inputs (not inline placeholders standing in for labels)
- [ ] Required fields marked with `*` or text — never asterisk-only without legend
- [ ] Optional fields marked with `Optional`, not parenthetical "(if applicable)"
- [ ] Validation runs on blur or submit, not every keystroke
- [ ] Error messages: what's wrong + how to fix, attached to the field
- [ ] User input retained on error (no wiping the form)
- [ ] Submit button shows pending state during async
- [ ] Cancel/back path always visible
- [ ] Primary action visually distinct from secondary
- [ ] Logical field grouping (personal info, contact, payment) with clear separation
- [ ] Tab order matches visual order

## State design checklist

Every async/conditional component must handle:

- [ ] **Initial / idle** — clear what the user can do
- [ ] **Loading** — skeleton matching final layout, or labeled spinner ("Loading patients…")
- [ ] **Empty** — explain why empty + offer next action
- [ ] **Error** — what failed + retry or next step
- [ ] **Success** — confirmation that doesn't block further action
- [ ] **Disabled** — explain *why* (tooltip, inline hint), don't leave it dead
- [ ] **Partial / pending** — optimistic UI or clear in-progress indicator

## Navigation / orientation checklist

- [ ] Where am I? — active state on current item, page title visible
- [ ] What can I do here? — primary action visible above the fold
- [ ] Where can I go? — main nav persistent, related links surfaced
- [ ] Breadcrumb on pages ≥2 levels deep
- [ ] Logo / app name links home
- [ ] Page H1 matches the link or nav label that led here

## Mobile / touch checklist

- [ ] Tap targets ≥ 44×44px
- [ ] No hover-only behavior — every hover affordance is also tappable / focusable
- [ ] Forms don't trap zoom (16px+ font on inputs)
- [ ] Modals dismiss with explicit close, not just outside-tap
- [ ] No horizontal scroll on screens ≤ 375px
- [ ] Critical actions never hidden behind hover or right-click

## Accessibility baseline

Not optional. These are usability bugs, not extra credit.

- [ ] Semantic HTML: `<button>` for actions, `<a href>` for navigation, headings in order
- [ ] All inputs have associated `<label>` (via `htmlFor` or wrapping)
- [ ] Focus visible on all interactive elements
- [ ] Color not the only signal (errors include text + icon, not just red)
- [ ] Sufficient contrast (WCAG AA: 4.5:1 body text)
- [ ] Icon-only buttons have `aria-label`
- [ ] Modals trap focus and restore on close
- [ ] Form errors announced via `aria-live` or `role="alert"`
- [ ] No `onClick` on `<div>` — use `<button>`

## Copy rules

- Sentence case for labels, headings, buttons. Title Case Looks Shouty.
- Drop "please" — polite but adds reading load.
- Drop "you" / "your" in field labels — `Email` not `Your email`.
- Use contractions — `Couldn't` not `Could not`.
- Use the verb of what happens — `Save`, `Delete patient`, `Send invoice` — not `Submit` / `OK`.
- Specific over vague — `Couldn't save changes — try again` not `An error occurred`.
- Action-oriented empty states — `No patients yet. Add your first patient.` not `No data found`.
- Don't shorten into ambiguity. `Phone (optional)` is fine; `Ph` is not.

See `references/copy-rewrite-patterns.md` for the full lookup table.

## Common patterns cheat sheet

| Anti-pattern | Fix |
|---|---|
| Inline `<Spinner />` only | Use the project's loading primitive with context label |
| Empty state shows blank or `No results` | Explain *why* + offer next action |
| Error renders raw string | Wrap in error component with retry / next-step CTA |
| Modal dismiss is X-only | Add explicit Cancel + primary CTA at the bottom |
| Button labeled `Submit` / `OK` / `Confirm` | Verb of what happens: `Save`, `Delete patient`, `Send invoice` |
| Long instruction paragraph above a form | Delete. Form should self-explain via labels and placeholders |
| Multiple H2s competing on a page | One page-level H1, related sections grouped under one H2 |
| Tab labels duplicate page heading | Trim. "Patient details > Information" → tab says `Information` only |
| Destructive action same color as safe | Destructive = red/destructive variant + confirmation modal |
| Disabled button with no explanation | Add inline hint or tooltip explaining *why* |

See `references/ux-audit-checklist.md` for the full operational checklist, `references/component-smell-catalog.md` for the named-smell catalog with severity, and `examples/` for full before/after refactors (form, empty state, destructive modal, search/filter, checkout, navigation).

## Output format

Always end with this exact structure:

```
[Refactored code or targeted sections]

**UX Improvements:**
- [Specific change] → [Why it reduces cognitive load / which Krug principle]
- ...
```

Rules for the bullet list:
- 3–7 bullets, no more.
- Specific change, tied to the code (not "improved hierarchy" — say "promoted Save button to primary, demoted Cancel to ghost").
- Always include the *why* — name the Krug principle or the cognitive-load reason.
- No generic praise. No "this is now cleaner."

## Component size rules

| Size | Approach |
|---|---|
| < 150 lines | Full refactored component |
| 150–400 lines | Refactor highest-friction sections; flag rest with `// UX: …` inline comments |
| > 400 lines | Identify top 3 friction points, refactor those, ask which section to prioritize next |

## What good looks like

- One obvious primary action per section. No visual competition.
- Labels a first-time user understands without training.
- Zero instruction paragraphs.
- Every state (loading, empty, error, disabled) explicit.
- A new user could navigate it correctly on day one.
- The refactor reads *faster* than the original. If it's longer, something went wrong.
