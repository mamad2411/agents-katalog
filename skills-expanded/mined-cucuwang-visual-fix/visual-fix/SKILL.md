---
name: visual-fix
description: Locate and repair a specific frontend UI defect from a screenshot, pointed region, visible text, route, selector, or plain-language symptom. Use for targeted visual fixes in an existing codebase that require source localization, an explicit change plan, approval before edits, and honest visual or static verification. Do not use for broad redesigns, new feature development, or bitmap editing.
---

# Visual Fix

Turn one visible UI problem into one localized, approved, verified code change.

## Supported evidence

Accept any useful combination of:

- A screenshot of the current UI
- An annotated or described region in a screenshot
- A current and target screenshot with their roles identified
- A route, viewport, component name, visible string, selector, or test id
- A plain-language symptom such as "this card is clipped" or "these controls do not line up"

Ask only for evidence that blocks reliable localization. A route plus a unique visible string may be enough without a screenshot. A screenshot with repeated components may still need a route, label, or state.

Handle one visual issue at a time. Split unrelated symptoms into separate fixes.

## Workflow

### 1. Establish the target

Restate the bounded outcome in concrete terms:

- What looks wrong now
- What the user expects to see
- Which route, component, state, and viewport are relevant when known
- Which visible anchor identifies the target

If the requested result is subjective or could affect different elements, ask the smallest question that distinguishes them.

### 2. Establish a read-only baseline

Before editing:

- Find the repository instructions and source of truth.
- Inspect worktree status and preserve existing user changes.
- Identify the framework, route entry, component tree, styling system, and available run or test commands.
- Reproduce the target route and viewport when the environment permits.
- Capture or record the current state before changing it.

Do not edit generated output when a maintained source file exists. Do not clean or overwrite unrelated worktree changes.

Report the baseline briefly:

```text
Context
- Route/state: /catalog, filters open
- Viewport: 390 x 844
- Source of truth: src/routes/catalog.tsx + src/styles/catalog.css
- Existing user changes: none
- Reproduction: available
```

### 3. Locate the rendered source

Trace evidence from the rendered element back to maintained code. Use the route, accessible name, visible text, DOM selector, component name, test id, class, style token, or screenshot geometry. Read [references/locating.md](references/locating.md) when multiple files or style layers are involved.

Identify one primary source location and at most two required related locations. File and line evidence must come from the current worktree.

```text
Located
- Primary: src/components/ProductGrid.tsx:42, ProductGrid
- Related: src/styles/products.css:18
- Evidence: `.grid` controls the repeated horizontal spacing visible between the cards
- Confidence: high
```

If two similar elements remain plausible, explain the distinguishing evidence and stop for clarification.

### 4. Diagnose from evidence

Connect the visible symptom to actual code. Prefer one supported cause. Offer two or three hypotheses only when the evidence remains ambiguous.

For each hypothesis include:

- The property, selector, token, or component involved
- The code or rendered evidence supporting it
- The intended fix direction
- An observation that would disprove it

Do not invent CSS values from the screenshot. Inspect the current value and the surrounding design system first.

### 5. Present the exact change plan

Show the proposed patch before editing:

```text
Change plan
- Files: src/components/ProductGrid.tsx:42
- Current: gap: 8px
- Proposed: use the existing space-4 token (16px)
- Scope: ProductGrid on /catalog and /search
- Preserving: card padding, mobile column count, unrelated routes
- Verification: targeted test, lint, screenshots at 390 x 844 and 1280 x 800
- Risk: medium; the component is shared by two routes
```

Wait for explicit approval of this plan. Choosing a diagnosis does not approve a code change. If the plan later expands to another file, dependency, lockfile, generated artifact, or route, present the revised plan and obtain approval again.

### 6. Apply the approved patch

Make the smallest change that implements the plan. Keep edits inside the approved files and scope. Then inspect the diff immediately:

- Run `git diff --check` when the project uses Git.
- Confirm the diff contains only the planned change.
- Preserve pre-existing changes and avoid unrelated formatting churn.
- Do not commit, push, install dependencies, or modify external services unless separately authorized.

### 7. Verify the result

Read [references/verification.md](references/verification.md) before claiming success.

Use the strongest available evidence:

1. Run targeted tests, formatting, type checks, or a build relevant to the changed code.
2. Render the same route, state, and viewport used for the baseline.
3. Compare before and after visually.
4. Check one nearby viewport or shared route when the changed source has wider scope.

Report exactly one verification state:

- `Verified visually` when comparable before and after render evidence exists
- `Verified statically` when code checks pass but the UI could not be rendered
- `Unable to verify visually` when the environment lacks the route, browser, fixture, or startup path
- `Verification failed` with the failing command or observed regression

If verification fails, return to diagnosis. Do not stack an unapproved second fix on top of the first.

## Completion report

Keep the handoff compact and evidence-based:

```text
Fixed
- Target: catalog card spacing at mobile width
- Source: src/components/ProductGrid.tsx:42
- Change: gap now uses space-4
- Verification: Verified visually at 390 x 844; unit test and lint passed
- Wider checks: /search at 390 x 844 and /catalog at 1280 x 800
```

Mention any remaining visual uncertainty. Never describe a code diff as visual proof.
