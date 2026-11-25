---
name: x-ray
metadata:
  internal: true
description: >
  Review a diff for correctness, project conventions and architecture alignment.
  Route component checks to installed specialists, preserve independent review
  evidence, and optionally verify browser behavior or create a local HTML review.
---

The developer wants a full-strength, project-aware review of a diff. Here is their input:

---

## $ARGUMENTS

A diff range, PR number, branch name or file path identifies the review target.
Optional effort preferences apply only if supported by the selected review mechanism.

Apply `.claude/skills/x-ray/runtime/delegation.md` for dispatch and
`runtime/review.md` for the independent correctness pass. Keep correctness, component
conventions and architecture as independent passes over the same resolved scope.

## Step 1 — Resolve scope and touched layers

Resolve the diff range: `git diff @{upstream}...HEAD`,
falling back to `git diff main...HEAD` / `git diff HEAD~1` / working-tree changes if
there's no upstream or the range is empty, or the explicit target from `$ARGUMENTS` if one was
given. This repo's default branch is `main` — never fall back to a different default
branch name. Keep this resolved range/target as a single string — every sub-review in Step 2
reviews the _same_ scope, so pass it through unchanged.

Run `git diff <range> --name-only`. Match changed paths to the Agents table in
`CLAUDE.md` and the installed role scopes. These specialists
are instances of the canonical `layer` template for the project's actual components.
Do not assume particular component names or a frontend/backend/data split. Resolve
ambiguous ownership and identify unmatched paths explicitly.

## Step 2 — Independent review passes

Each pass receives the whole resolved diff for context and applies its own review
responsibility. Convention and architecture passes must not filter the correctness
pass's input. Dispatch concurrently when supported and authorized; sequential
independent reviews preserve the same contract when concurrency is unavailable.

**2a. Correctness pass.** Apply `runtime/review.md`. Record the mechanism, coverage,
actual findings and any unavailable capability. Never equate an unavailable review
with a clean result. If no independent review can run, present the limitation and
wait for a human review or explicit skip; label a skipped pass **NOT RUN**.

**2b. Convention pass — one per touched layer.**
For each touched component, invoke its installed specialist through runtime/delegation.md with a prompt like:

> "Review `<resolved diff range>` strictly against your own conventions (folder structure,
> naming, layer boundaries, exception handling, whatever your system prompt
> defines as non-negotiable) — do NOT write, edit, or fix anything, and do not evaluate general
> correctness bugs (that's covered separately). Return each violation as
> `{file, line, summary, failure_scenario}` where `failure_scenario` states which of your own
> rules is broken and quotes it. If nothing violates your conventions, return an empty list."

**2c. Architecture pass — conditional.**
Apply the exact trigger criteria from `.claude/skills/dev/patterns/satellite-review.md`'s "When
to trigger" section (read it now) to the Step 1 diff. If met, spawn `@architect` with the same
review-mode prompt shape that section already defines (HLD container boundaries, data-flow
direction, NFRs, layer best practices) scoped to `<resolved diff range>`. Skip this call entirely
if the trigger criteria aren't met — do not invent a lighter version of the check instead.

## Step 3 — Verify the new findings only

Preserve Step 2a’s findings and verification labels; report their actual evidence and limitations.

For every candidate returned by Step 2b/2c (conventions + architecture), run one verifier per
candidate: give it the diff, the relevant file(s), and the candidate; it returns one of
**CONFIRMED / PLAUSIBLE / REFUTED**. Use evidence-based judgment —
default to PLAUSIBLE unless the candidate is factually wrong, provably impossible, or already
handled in this diff. Keep CONFIRMED and PLAUSIBLE, drop REFUTED, dedup near-duplicates first.

## Step 4 — Present as two native-vocabulary groups

Keep correctness, conventions and architecture findings distinct, identifying
the actual reviewer/mechanism and verification evidence for each.

```
## /x-ray — <scope> — <date>

### Correctness & cleanup (<actual review mechanism>)
<ranked findings with file/line, failure scenario and verification evidence>
If completed with no findings: "No correctness findings in the reviewed scope."
If skipped: "**NOT RUN** — <reason and explicit skip attribution>."

### Project conventions (@auth / @web)
| Code | Finding | File | Severity | Layer |
|------|---------|------|----------|-------|
| BUG-XXX / DESIGN-XXX / IMPROVE-XXX | ... | `path:line` | Must fix / Advisory / Optional | Auth/Web |
If none: "No convention violations found."

### Architecture (@architect)
<only if Step 2c ran — the doc-to-code alignment table + gaps, as @architect's own output format>
If Step 2c was skipped: "Skipped — satellite-review trigger criteria weren't met."
```

## Step 4b — Browser verification (optional, web changes only)

Skip when the changed components have no browser-observable behavior, determined
from their actual scope and project evidence.

Unlike `/dev test`'s equivalent step, this one is opt-in — `/x-ray` is often run by a reviewer who
may not have a dev server running or want the extra round-trip. Ask:

> "Want me to verify this diff's behavior live in a browser — network requests, console, and any
> keyboard/ARIA wiring for accessibility-related findings? I'll need the dev server running.
> (yes / no)"

**Stop and wait.** If no (or no response), skip straight to Step 5 — this is a bonus check, never
a blocker on the rest of the review.

If yes, apply `.claude/skills/x-ray/runtime/browser.md`. Verify each required
browser capability is exposed and authorized; record unavailable checks rather
than assuming a particular integration exists.

**Scope restriction (always):** only navigate/interact with `http://localhost:5173` — never any
other URL or origin. Reading network requests the loaded page itself fires to its configured
services via available network inspection is fine — that's the page's own traffic, not the browser
navigating elsewhere. In this project there is no local backend to observe — the Auth container
(Lambda@Edge) only runs deployed at the CloudFront edge, so the only relevant requests are the
VitePress site's own.

Ask the developer to start the dev server the diff needs (never run the serve command yourself):

> "Please start the dev server(s) this diff needs (e.g. `yarn nx run site:serve`) and let me know when they're up."

**Stop and wait.** Once confirmed, use the selected browser tools to exercise the changed
behavior directly, rather than taking Step 4's findings on faith:

1. Navigate to the affected page(s) and exercise the change the diff introduces.
2. Inspect the resulting network requests through available network inspection to confirm wire-level behavior
   actually matches what the diff claims.
3. Check available console inspection for new errors/warnings.
4. For any Step 4 finding about keyboard focus, ARIA wiring, or screen-reader behavior, verify it
   directly using supported DOM inspection (focus the element, assert the resulting DOM state) instead of
   relying on a screenshot or the finding's own description.
5. Fold the result back into the Step 4 findings already presented — e.g. "confirmed live: X" /
   "could not reproduce: Y" — rather than presenting it as a separate, untethered report.

Follow the existing browser-automation guardrails: stop and ask the developer after 2-3 failed
attempts at any single check rather than retrying in a loop, and never trigger a blocking
dialog/alert. If the dev server isn't reachable, or the tools fail repeatedly, say so and move on
to Step 5 — do not block the rest of the review on this step. This step does not itself write to
`2-report.md`, matching this skill's own "read-only, presentation-only" scope (see Output below).

## Step 5 — Always offer the interactive demo (never build without a yes)

Regardless of what Steps 2-4 found — critical issues, only minor cleanup items, or nothing at
all — always ask at the end:

> "Want an interactive HTML version of this review via `@interactive-demo`? (yes / no)"

**Stop and wait.** If yes, use the installed `interactive-demo` role when available and permitted; otherwise create the local HTML review inline, preserving the same findings and scope. When delegating, invoke the role, passing it: the resolved diff scope, the
full findings list from Step 4 (with severities and source group intact, even if empty), whether
the 2a correctness pass ran or was explicitly skipped, and ticket context if one is
identifiable (`docs/Stories/*{TICKET}*/`). A clean/near-empty findings
list is a valid input, not a reason to skip the offer — `@interactive-demo` degrades gracefully
to an Overview-only-of-substance page in that case (see its own "Critical issues" tab rule for
the empty case). For inline generation, save under the identified ticket’s `interactive-review/` folder; otherwise use a project-local review folder and report its path. If no, stop here — do not build anything.

> **Not yet deployed in this project:** `@interactive-demo` has no canonical template in
> `.claude/skills/implementation-harness/` — it is expected to arrive via a separate harvest from a
> project that already has it (see `x-ray/INTENT.md`'s Conditionals). Until then, answering
> "yes" here will fail to find the agent; say so plainly rather than trying to improvise its
> behavior yourself.

**Do not tell `@interactive-demo` where to save the file** — it defaults to the ticket's
`docs/Stories/*{TICKET}*/interactive-review/` folder on its own, which is where the report
belongs. Never pass it a scratchpad or temp path; only pass an explicit save path if the
developer named one.

**When `@interactive-demo` returns, report the local file path and STOP — do not publish it.**
The report is a local HTML file for the developer to open; it stays on disk. Do NOT call the
`Artifact` tool (or otherwise upload/host the page) on your own initiative, and do not offer or
promise to — publishing sends review content to an external hosting service, which is only ever done
when the developer explicitly asks for a hosted/shareable link in a later turn. Silence or a
"yes" to the demo offer is not consent to publish.

## Output

If a ticket folder was identified, this skill does not itself write into `2-report.md` — that
file's `## PR Review` section belongs to `/dev test`'s own review-gate flow (verify → classify →
write → stop-for-confirmation → per-fix loop), which `/x-ray` does not replicate. `/x-ray` is a
read-only, presentation-only pass: report the findings to the developer as shown in Step 4, and
let them decide what to do with them.
