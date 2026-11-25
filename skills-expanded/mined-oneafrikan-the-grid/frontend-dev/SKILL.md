<!--
  SKILL.md — Frontend Dev operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific framework unless injected via a stack overlay.
  Stack-specific commands are NOT here — they live in stacks/<stack>/ overlays.
  Injection points are marked: `STACK: ...`
-->

# Skill: Frontend Dev

## Invocation

```
/frontend_dev <task reference — PRD path + task list>
```

Or picked up from a Signal Protocol entry / PR assigned to frontend-dev. Either
way: **no PRD and no API contract, no work.** If there's no PRD to reference,
ask for one; if the contract from backend-dev is missing, confirm it first.

---

## Step 1 — Read the PRD and confirm the API contract

Before writing code, confirm from the PRD and backend-dev's handoff:

| Question | Why |
|---|---|
| What are the exact UI tasks assigned to frontend? | Bounds the work; anything outside is not yours to build |
| What is the API contract? (method, path, request, exact response shape, status codes, error format) | You render what the backend promises — assume nothing it didn't agree |
| What are the screens/components and their states? | Empty, loading, error, success are all in scope, not just the happy path |
| What interactions and validation rules apply? | Forms, client validation, and feedback are designed, not improvised |
| What is the accessibility target? | Keyboard, ARIA, contrast, focus are acceptance criteria |
| What are the acceptance criteria + verification command? | This is your definition of done |

**Rule:** If the PRD is silent or the contract is missing/mismatched, ask once.
If still unclear, escalate — do not guess the contract or fabricate a response shape.

---

## Step 2 — Plan components and state

Before tests, sketch the shape (in the PR notes or a scratch file):

- **Component tree** — what components exist, which are reused, which own data vs. presentation.
- **State placement** — keep state at the lowest level that works; lift only when shared. Distinguish server state (from the API) from local UI state.
- **Data flow** — which component fetches against the contract, how the response maps to props.
- **States to cover** — list empty / loading / error / success for each data-driven view.

<!-- STACK: stack-specific component + state-management idioms injected here -->

---

## Step 3 — Write failing tests first

For each acceptance criterion, write a test that fails for the right reason:

- Component render — renders the success state from a contract-shaped fixture.
- Interaction — click/submit/keyboard flows do what the PRD says.
- States — empty, loading, and error each render correctly.
- Accessibility — key elements are reachable and labelled (role/name queries, focus order).

<!-- STACK: stack-specific test framework + how to run a single test injected here -->

Run them. Confirm they fail. Now you have a target.

---

## Step 4 — Implement to the contract

Build the smallest code that turns the tests green:

**Markup / components**
- Build components against the agreed response shape — never read a field the contract didn't promise.
- Keep components small and composable; one responsibility each.
- <!-- STACK: stack-specific component / template syntax injected here -->

**Client state + data**
- Fetch against the agreed endpoint, method, and request shape.
- Keep state at the lowest level that works; isolate server state from local UI state.
- Handle the response per the contract's status codes and error format.

**Forms + interaction**
- Validate input at the boundary with clear, accessible feedback.
- Map every form field and control to its label and error message.

---

## Step 5 — Handle every state

Every data-driven view implements all four — none assumed:

- **Empty** — no data yet: a clear, non-broken empty view, not a blank screen.
- **Loading** — a visible, accessible loading indication; no layout jump on resolve.
- **Error** — the contract's error format surfaced as human-readable feedback; a retry path where it makes sense.
- **Success** — the happy path, rendered from the contract shape.

---

## Step 6 — Accessibility pass

Run the accessibility checklist (below) before verifying. Treat each failing
item as a failing test, not a nice-to-have.

<!-- STACK: stack-specific a11y tooling (linter / axe / testing-library queries) injected here -->

---

## Step 7 — Verify

- All tests green, including state and accessibility tests.
- Run the PRD's verification command — it must pass.
- Lint / type-check clean.
- Accessibility checklist clear; component checklist clear.
- Re-read the diff as a reviewer would: does every line trace to a task?

---

## Step 8 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

Open a PR (or append to `signals/→<agent>.md`) with:

```markdown
## Frontend — <Feature Name>

### PRD
PRD: <path> (Section: <frontend tasks>)

### API contract consumed (from backend-dev)
- `<METHOD> <path>` → request: <shape> | response: <shape> | errors: <codes/format>

### What changed
- <component / view / form> — <one line why>

### States covered
- [ ] Empty  [ ] Loading  [ ] Error  [ ] Success

### Accessibility
- [ ] Keyboard reachable  [ ] ARIA roles/names  [ ] Contrast  [ ] Focus order

### Verification
- Command: `<verification command>`
- Tests: <count> added, all passing

### Definition of done
- [ ] All assigned PRD acceptance criteria met
- [ ] Verification command passes
- [ ] All four states implemented and tested
- [ ] Accessibility checklist clear
```

Then flag QA (qa-engineer) to verify, and the Tech Lead to review. Do not merge
your own work to production — QA gates, the human approves the deploy.

---

## Accessibility checklist

Every interactive view you ship answers all of these:

- [ ] **Keyboard** — every control is reachable and operable without a mouse; no keyboard traps.
- [ ] **Focus** — focus order is logical; focus is visible; focus moves sensibly on route/modal changes.
- [ ] **ARIA / semantics** — native elements first; roles and accessible names present where semantics aren't implicit.
- [ ] **Labels** — every form control has an associated label; errors are programmatically linked to their field.
- [ ] **Contrast** — text and meaningful UI meet the project's contrast target.
- [ ] **Feedback** — loading/error/success states are announced to assistive tech, not just shown visually.
- [ ] **Images/icons** — meaningful images have alt text; decorative ones are hidden from assistive tech.

<!-- STACK: stack-specific a11y target (WCAG level) + tooling injected here -->

---

## Component checklist

Every component you ship answers all of these:

- [ ] One responsibility; presentation and data concerns separated where it helps.
- [ ] Props match the contract shape; no field read that the API didn't promise.
- [ ] State lives at the lowest level that works; no needless lifting or global state.
- [ ] Empty / loading / error / success all handled for data-driven views.
- [ ] Reuses existing components and patterns rather than re-inventing them.
- [ ] No layout shift between loading and resolved states on the common path.
- [ ] Styles follow the project's conventions (tokens/utilities/classes already in use).
