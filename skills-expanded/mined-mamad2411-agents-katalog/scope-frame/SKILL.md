---
name: scope-frame
description: Declares session boundaries (in scope, out, assumptions) before spec work. Use after intake, before specify, or /scope. Not for detecting the domain (intake) or writing criteria (specify).
---

# Scope-frame

You establish the fence before anyone starts digging. Your job is explicit agreement on what this
session covers, what it excludes, and what is being assumed — before specify writes a single
requirement. The boundary is domain-neutral: in / out / assumptions apply to a game feature, a finance
model, or a curriculum identically.

## What this does / does not do

Does: read the resolved domain + opening context, load any discovered project standards, draft and
confirm `scope.md` (in-scope, out-of-scope, assumptions), write a receipt. Does **not**: detect the
domain (intake), write the task card or acceptance criteria (specify), or proceed without explicit
user confirmation of the boundary.

## When NOT to use

- Intake has not run (no `intake.json`) — the domain is unknown (I3); there is nothing to scope against.
- `scope.md` is already locked and no expansion has been detected — re-framing a locked scope mid-task
  without a trigger is churn; only re-run on a detected expansion.

## Reference Routing

| Situation | Reference |
|---|---|
| scope.md / receipt write delegation | `engine/shared/references/script-delegation-contract.md` |

## Inputs

- `<workspace>/intake.json` (domain, sub_target, complexity)
- The opening user message and any attached documents
- Discovered project standards from memory (`category: project-standard`), if any

## How to do it

### Step 1 — Read the domain and context

Load `intake.json`; take the domain, sub_target, and complexity. Read the user's request in full.

### Step 1b — Load discovered standards

Query memory for `category: project-standard` drawers. Load all `critical` drawers; load `high` ones
if the domain or task overlaps their category. For each: spot-check that its evidence still exists and
the pattern holds. Confirmed → cite the drawer ID in Assumptions. Evidence gone → mark the drawer
NEEDS_REVERIFICATION; do not cite it. If no standards exist, note "no project standards discovered"
and proceed.

### Step 2 — Draft the boundaries (specific — vague scope is a defect, I12)

- **In Scope** — what this session must produce, in action language ("implement X", "define Y",
  "model Z"). 3–7 items for Low; more for Medium/High.
- **Out of Scope** — what is explicitly excluded. Adjacent topics the user mentioned go here.
  Exclusions prevent scope creep — as important as the inclusions.
- **Assumptions** — what is taken as given (dependencies, environment facts, prior decisions). A false
  assumption later triggers a re-frame.

### Step 3 — Present for confirmation

Show the drafted scope. Ask "Does this match what you intended?" Accept additions/removals. Do not
proceed until the user explicitly confirms — an unconfirmed scope is not a locked scope.

### Step 4 — Write `scope.md`, then the receipt

Delegate the scope write (do not hand-author it). Then write the receipt with `user_confirmed: true`
(never write the receipt with `user_confirmed: false`).

## Output Contract

**scope.md** (`<workspace>/scope.md` — persistence: **Spec-First**, discard after archive):

```markdown
# Session Scope
**domain:** <from intake.json>   **sub_target:** <or none>   **complexity:** Low|Medium|High
**locked_at:** <ISO-8601>

## In Scope
- <item>
## Out of Scope
- <item>
## Assumptions
- <item>
- **Standard [std-<id>]:** <name> — <one-line rule> (criticality: critical|high) [evidence: <path>]

## Scope Change Log
| timestamp | change | triggered_by |
|---|---|---|
```

**receipt** (`<workspace>/receipts/scopeframe-receipt.json`): base + `in_scope_count`,
`out_of_scope_count`, `assumptions_count`, `user_confirmed` (must be true for a written receipt).

## Proactive Triggers

- **Out of Scope is empty**: the scope is not specific enough — ask "what should we NOT tackle here?"
  before locking.
- **Assumptions is empty**: every task has at least one (environment, dependency, prior work) — you
  missed one.
- **About to write the receipt with `user_confirmed: false`**: stop — an unconfirmed scope is not
  locked; get explicit confirmation first.
- **A loaded standard's evidence path no longer exists**: mark it NEEDS_REVERIFICATION; do not cite a
  stale standard as active (I9).
- **The user's request implies work beyond the resolved domain**: that may be a domain change — route
  back to intake rather than silently widening scope.

## Completion Criteria

**Done when:** `<workspace>/scope.md` exists with at least one in-scope item, at least one out-of-scope
item, and at least one assumption; a receipt with `user_confirmed: true`.

**Not done if:** Out of Scope or Assumptions is empty; the receipt was written without user
confirmation; scope was widened past the resolved domain without re-intake.

**Next step:** `specify` (write the task card against the locked scope).

## Related Skills

- **intake**: Resolves the domain before scope-frame. NOT for boundaries — that is scope-frame.
- **specify**: Consumes the locked scope to write the task card. NOT for declaring boundaries — scope-frame.
- **decompose**: May re-trigger scope-frame on a detected mid-execution expansion. NOT a scope owner itself.
