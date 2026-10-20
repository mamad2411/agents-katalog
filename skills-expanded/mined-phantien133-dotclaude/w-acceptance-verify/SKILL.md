---
description: Phase 5b helper for w-task — proves the finished task actually delivers what the ticket asked for. Builds a requirement-to-evidence matrix from intake/questions/plan, fans out independent verifier agents, and (for UI work) compares the implementation against the Figma design export so wrong or invented assets are caught before the PR. Writes acceptance.md, and open-issues.md when the fix loop is exhausted.
argument-hint: <task-slug> [--iteration N] [--visual-only|--acceptance-only]
allowed-tools: Bash, Read, Write, Edit, Skill, Agent
---

# w-acceptance-verify

The last question before a PR is not "do the tests pass" — it is **"did we build the
thing that was asked for, with the assets that were given"**. Phases 4 and 4c answer
the first. This skill answers the second.

It runs after docs are persisted, so what it verifies is the complete shipped unit:
code, tests, docs, and UI.

Reads `.claude/workflow.yaml`:
- `verify.acceptance` — `true` (default) | `false`
- `verify.visual` — `auto` (default) | `true` | `false`
- `verify.max_loops` — default `3`
- `workflow.state_root`, `project.dev_server_command`, `project.dev_server_port`

Reads from `<state_root>/<task-slug>/`: `intake.md`, `questions.md`, `plan.md`,
`impact.md`, `tests.md`, `verify.md`, and — when UI is in scope — `figma-spec.md`
or `figma-snapshot.md`, `figma-assets.md`, `figma-mapping.md`, `figma-screens/`.

---

## Step 0 — Preconditions

| Condition | Action |
|---|---|
| `verify.acceptance: false` AND `verify.visual: false` | print "Acceptance verification disabled." exit 0 |
| `<state_root>/<task-slug>/` missing | error, exit 1 |
| `plan.md` missing | error — nothing to verify against, exit 1 |

Resolve `ITERATION` from `--iteration` (default: `state.yaml.gates.5b_iteration` or 1)
and `MAX_LOOPS` from `verify.max_loops`.

---

## Step 1 — Build the requirement inventory

Every requirement gets a stable ID so iteration 2 can be compared against iteration 1.

Extract, in this order — earlier sources win on conflict, because they are closer to
the person who asked:

| ID prefix | Source | What counts as a requirement |
|---|---|---|
| `T-` | `intake.md § Description` | each explicit ask in the ticket body, including non-functional ones ("must be idempotent", "no new dependency") |
| `Q-` | `questions.md` | each answered clarifying question — the answer is a requirement |
| `A-` | `plan.md § Acceptance criteria` | each criterion |
| `S-` | `plan.md § Feature scope` | each scoped item not already covered above |
| `U-` | `figma-spec.md` / `figma-snapshot.md` | each screen, state and interactive element in scope |

Explicit **out of scope** items from `plan.md § Out of scope` are recorded as
`X-` rows and verified in the opposite direction: they must NOT be implemented.

If a requirement is ambiguous, keep it and mark it `NEEDS-HUMAN` — never drop it
and never soften it into something that happens to be satisfied.

---

## Step 2 — Collect evidence

For each requirement, gather the artefacts that would prove it:

- **code** — files from `impact.md § Affected Files` plus `git diff --name-only <base>..HEAD`
- **tests** — assertions in the files listed in `tests.md`
- **checks** — `verify.md` table (typecheck / lint / tests / review)
- **browser** — `verify.md § Browser Verify` rows and `browser-*.png`
- **docs** — files committed by Phase 5
- **design** — `figma-spec.md`, exported files listed in `figma-assets.md`

Use `w-codegraph query`/`affected` when available to locate the implementing symbol
for a requirement instead of grepping the tree.

Evidence is a **file:line reference or a check result**, never a claim. "Implemented
in the service" is not evidence; `src/auth/sign-up.service.ts:41` is.

---

## Step 3 — Fan out the verifiers (parallel, independent)

Spawn one agent per lens, each given the requirement inventory + the evidence set
and told to work **adversarially** — its job is to find the requirement that is not
actually met, not to confirm the happy path. Run them concurrently.

| Lens | Agent | Brief |
|---|---|---|
| Ticket coverage | `code-reviewer` (or `planner` when installed) | For every `T-`/`Q-` row: is it implemented, and does the implementation match what was asked — not a near neighbour? Flag scope drift in both directions. |
| Test adequacy | `tdd-guide` (fallback `code-reviewer`) | For every `A-` row: does a test actually assert it, including the abnormal flow? A row covered only by a happy-path test is a FAIL. |
| Language review | the Phase 4 language-routed reviewer for each changed language | Re-check that CRITICAL/HIGH items from Phase 4 were truly resolved and no fix introduced a regression. |
| Doc accuracy | `code-reviewer` | Do the Phase 5 docs describe what the code does? A doc that describes the plan rather than the implementation is a FAIL. |
| Out-of-scope | `code-reviewer` | For every `X-` row: confirm it was NOT built. Unasked-for work is a finding. |

Each agent returns rows of `{id, verdict, severity, evidence, what_is_missing}`.
`verdict` is `PASS` / `FAIL` / `NEEDS-HUMAN` only — no "probably" and no partials.

---

## Step 4 — Visual verification (UI tasks)

*Skipped when `verify.visual: false`, when `state.yaml.has_ui` is not `true`, or when
there is no design reference at all. Record the skip with its reason — a skip must
never read as a pass.*

The failure this step exists to catch: **the UI looks fine but is not the design** —
an icon redrawn instead of exported, a colour eyeballed, a spacing rounded, an asset
swapped for a lookalike from an icon pack.

**With the official Figma engine** (`figma_engine: official`):

1. Invoke skill `figma-verify-parity` for each implemented route, passing
   `figma-spec.md`. It diffs computed styles against the spec and writes
   `figma-parity-report.md`.
2. Spawn the `figma-visual-verifier` agent with the rendered screenshots
   (`browser-*.png` from Phase 4c, or freshly captured) **and** the design export
   images in `figma-screens/`, asking for a side-by-side verdict per screen.

**With the legacy engine, or no engine but exported design images present:**

Capture the implemented screens (start the dev server, `localhost` only, same safety
rules as Phase 4c), then compare each against its design export and report on:

| Check | FAIL when |
|---|---|
| Asset identity | a rendered icon/image is not one of the files listed in `figma-assets.md` |
| Placeholders | any `TODO(figma-asset)` / `ASSET_PLACEHOLDER` survives in shipped code |
| Layout | element order, grouping or responsive behaviour differs from the design |
| Colour / type / spacing | values differ from the spec beyond the spec's own tolerance |
| States | a state present in the design (empty, loading, error, disabled) has no implementation |

**No design reference at all:** record `visual: NOT RUN (no design reference)` and
verify only that no placeholder markers remain.

Kill any dev server started here, pass or fail.

**Browser/MCP contention:** this step drives the same `chrome-devtools` MCP as
Phase 4c. When those tools are busy or held by another session, follow the
**MCP contention protocol** defined in `w-task` Phase 4c — retry for up to
`verify.browser_wait_seconds` (default 180s), then open a confirm gate. Never
record `NOT RUN` for contention on your own.

---

## Step 5 — Write `acceptance.md`

```markdown
# Acceptance — <title>

Iteration <N> of <MAX_LOOPS> · <YYYY-MM-DD HH:MM>

## Verdict
<PASS | FAIL (<B> blocker, <M> major, <m> minor) | NEEDS-HUMAN>

## Requirement matrix

| ID | Requirement | Source | Evidence | Verdict |
|----|-------------|--------|----------|---------|
| T-1 | ... | intake | src/...:41 · test:12 | ✅ |
| A-3 | ... | plan | — | ❌ blocker |
| X-1 | (out of scope) ... | plan | not present | ✅ |

## Visual verification
<PASS / FAIL / NOT RUN (reason)>

| Screen | Design ref | Check | Result |
|--------|-----------|-------|--------|

## Findings
### <ID> — <severity> — <one-line title>
- **Expected:** <from the requirement>
- **Actual:** <what the evidence shows>
- **Fix:** <smallest change that closes it>

## Carried over
<findings from iteration N-1 that are still open — with their original IDs>
```

Severity: **blocker** = a ticket requirement is not delivered, or the UI ships a
wrong/invented asset. **major** = delivered but untested, or docs contradict code.
**minor** = cosmetic within tolerance, naming, comment.

Exit code: `0` when there is no blocker and no major; non-zero otherwise. Minors
never block — they are listed and carried into the PR description.

---

## Step 6 — The fix loop (contract with w-task Phase 5b)

This skill does not decide when to stop; it reports. `w-task` runs the loop:

```
iteration = 1
repeat:
    run w-acceptance-verify --iteration <n>
    exit 0            → gate passes, continue to Phase 6
    exit non-zero:
        fix every blocker + major        (smallest change that closes the finding)
        re-run tests → must be GREEN     (a fix that breaks a test is not a fix)
        commit           fix(<scope>): <finding title>  [<ID>]
        re-persist docs  → Phase 5 helpers for anything the fix changed
        w-codegraph sync
        iteration++
    until iteration > MAX_LOOPS
```

**Every fix is committed** — the loop never leaves an uncommitted working tree, and
docs are re-persisted in the same iteration as the code they describe, so the
docs-with-code invariant that `w-doc-gate` enforces at Phase 6 still holds.

---

## Step 7 — Loop exhausted → hand over to a human

When `iteration > MAX_LOOPS` and findings remain, stop trying. Write
`<state_root>/<task-slug>/open-issues.md` — written for the person who has to decide
what happens next, not for the model:

```markdown
# Open issues — <title>

<N> issue(s) survived <MAX_LOOPS> fix attempts. The task is otherwise complete:
code committed, tests GREEN, docs persisted.

## What is still wrong

### 1. <plain-language title>  ·  <blocker|major>
**What was asked:** <the requirement, in the ticket's own words>
**What happens instead:** <observable behaviour or visible difference>
**What I tried:** <attempt 1> · <attempt 2> · <attempt 3>
**Why it did not close:** <the actual obstacle — missing asset, ambiguous spec,
conflicting requirement, needs a decision>
**What would unblock it:** <the decision or artefact needed, and from whom>

## What is verified and fine
<one line per area that passed — so the reader knows the blast radius is bounded>

## Suggested next step
<continue to PR with these known gaps · get decision X first · re-scope>
```

Rules for this file: one screen of text, no stack traces, no model reasoning, no
apology. Each issue must be understandable by someone who has not read the diff.

Then set `state.yaml`: `status: blocked`, `gates.5b: open_issues`, and surface the
file path. The operator decides whether to continue to Phase 6 with known gaps or
re-plan.

---

## Notes

- Never mark a requirement PASS on the strength of your own earlier claim in this
  task. Evidence is a file reference or a command result, re-read this iteration.
- A finding fixed in iteration N keeps its ID and appears in iteration N+1 under
  **Carried over** only if it re-opens — never silently disappears.
- The skill is read-mostly; the only files it writes are `acceptance.md`,
  `open-issues.md`, and `figma-parity-report.md` via the parity skill.
