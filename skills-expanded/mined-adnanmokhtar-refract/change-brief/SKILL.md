---
name: change-brief
description: The comprehension gate — "if you can't explain the code, it isn't yours." For every non-trivial change (AI-generated or human), produce + validate a 5-field change brief (What / Why this shape / Edge cases / Blast radius / Verified by) before the change is committed or a PR opens. Mechanical, not advisory — the brief has a required shape, a hand-wave grep, and a citation requirement; a brief that paraphrases the diff without explaining it is rejected. Wired into /pre-commit and /review-changes; named by engineering-principles.md § AI-assisted development.
kind: skill
pack: code-quality
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: change-brief

## Purpose

Close the gap between **code that runs** and **code that's owned**. AI-generated code compiles, passes the happy-path test, and ships — and the developer who merged it cannot explain why it's shaped that way, what breaks it, or who it affects. The defect surfaces in production weeks later, and nobody on the team can navigate the code that caused it.

The existing rule ("Don't accept code you don't understand", `engineering-principles.md § AI-assisted development`) is advisory — nothing enforces it. This skill is the mechanical surface: a change cannot advance past `/pre-commit` / `/review-changes` until a brief exists that proves the change was understood, not just accepted.

**The brief is the explain-it-or-it-isn't-yours test in artifact form.** Writing it takes 2 minutes when you understand the change — and is impossible when you don't. That asymmetry is the gate.

## When to use

- Dispatched by `/pre-commit` (generate + validate before the commit lands) and `/review-changes` (validate that the PR body carries a passing brief).
- On demand: "write the change brief for this diff" / "does this PR have a valid brief?".
- **Self-applied by agents**: when an agent authors a non-trivial change, it generates the brief as part of the same turn — an agent that cannot fill all 5 fields from what it actually did has not finished the work.

### Trigger tiers (what counts as non-trivial)

A brief is REQUIRED when the change matches any of:
- diff > 20 lines (excluding lockfiles / generated files / snapshots),
- adds a dependency, a new public symbol, or a new abstraction,
- touches an I/O boundary (network / DB / queue / file), auth, payments, or tenant scoping,
- changes an error path, a default value, or a permission gate.

EXEMPT (no brief; don't manufacture ceremony): typo/comment fixes, pure renames with mechanical consumer updates, formatting, lockfile-only bumps, generated-file regeneration. Same anti-bloat contract as the tiered migration/align floors — the gate scales with risk.

### Size tiers (what the fields cost as the diff grows)

The tiers above decide **whether** a brief is owed. They do not decide **how much work each field is** — and `Blast radius` says "grep every public symbol the diff touches". On a 25-line change that is two greps. On a 15-file feature branch it is thirty, most of them uninteresting, and the field gets skipped or invented. A contract that cannot be honoured at scale trains the reader to stop believing it, so scope the field by size rather than letting it silently degrade:

| Diff size | `Blast radius` obligation | `Edge cases` obligation |
|---|---|---|
| **≤ ~50 lines** | Every touched public symbol, each consumer at `<path:line>`. | Every I/O call and conditional in the diff. |
| **~50–300 lines / ≤ ~5 files** | Every touched **exported** symbol (skip file-local ones — they have no external consumers by construction), each consumer at `<path:line>`. | Every I/O call and every conditional **on a non-happy path**; pure-logic branches roll up per function. |
| **> ~300 lines or > ~5 files** | **Module-level.** Name the modules this change is now depended-upon-by and the modules it newly depends on — one line each, cited by the import that establishes it. Then `<path:line>` consumers for the **exported surface that actually changed shape** (new / removed / signature-changed symbols) — not for every symbol the diff happens to touch. A diff this size that changed no exported signature says so, and that is a complete answer. | Group by the diff's carrier files; each carrier gets its non-happy paths at `<path:line>`, consequence files roll up to one line. |

The other three fields do not scale — `What`, `Why this shape` and `Verified by` are the same size on a 30-line diff and a 30-file one. If `What` is getting longer as the diff grows, the change is doing more than one thing and wants splitting; that is a finding, not a formatting problem.

## The brief contract (5 required fields)

Lives in the commit body (multi-commit work: the PR description). Field names are literal — the validator greps for them.

```text
What:           <1–2 lines — the observable change, not the file list>
Why this shape: <why THIS implementation given the project's conventions — cite the
                 convention/idiom/ADR it follows (<path:line> or ADR-NNN), or name the
                 alternative considered and why it lost>
Edge cases:     <which non-happy paths this change handles or touches — error / empty /
                 null / concurrent / timeout — each with <path:line>; or the literal
                 "none touched — <reason>">
Blast radius:   <who consumes this — callers / endpoints / screens affected, each
                 <path:line>; or "module-local — no external consumers (grepped <symbol>)">
Verified by:    <the command(s) run + observed result — "pnpm test orders → 47 passed",
                 "booted dev server, exercised error path manually"; never "should work">
```

## Procedure

### Mode A — generate (at authoring time)

1. Read the full diff (`git diff --staged` or the branch diff). Not the summary — the diff.
2. For **Why this shape**: name the convention the change follows (grep `ai/conventions.md` / `_extracted-idioms.md` / `ai/decisions/`). If the shape follows no existing convention, STOP — that's either a missing idiom (`/setup-project --refine`) or a new pattern needing an ADR (`engineering-principles.md § Consistency`) — the brief just surfaced it before merge.
3. For **Edge cases**: walk every I/O call and conditional in the diff; list the non-happy paths each one handles. A fetch with no error path discovered here = fix it now (route to the unhandled-io detector's closure), don't document it as absent.
4. For **Blast radius**: apply the size tier above. Under ~50 lines, grep every public symbol the diff touches and list consumers with `<path:line>`. Above ~300 lines or 5 files, go module-level first and then cite consumers only for the exported symbols whose **shape** changed. `git diff --stat` picks the tier before you start; deciding it afterwards is how the field gets padded to look thorough.
5. For **Verified by**: run the verification; paste the real command + real result.
6. Write the brief into the commit body / PR description.

### Mode B — validate (at gate time)

1. Locate the brief (commit body, else PR description). Missing on a triggered change → **FAIL**.
2. **All 5 fields present and non-empty.** Missing field → FAIL naming it.
3. **Hand-wave grep** — FAIL on: `should work`, `looks good`, `standard approach`, `as requested`, `straightforward`, `simple change`, `minor tweak`, `various`, `etc.`, `and so on`, `n/a` (except the two sanctioned literals above).
4. **Citation check** — `Why this shape`, `Edge cases`, and `Blast radius` each contain ≥ 1 `<path:line>` / ADR reference OR one of the sanctioned literals. A brief with zero resolving citations is a paraphrase, not an explanation.
5. **Echo check** — `What` must not merely restate the diff stat ("updated OrderService", "changed 3 files"). It names the observable behaviour delta.
5b. **Tier check** — on a diff over ~300 lines or ~5 files, `Blast radius` must be module-level (see Size tiers), not a symbol list. A per-symbol list on a large diff is either incomplete or padded; both read the same and neither is checkable. Conversely, a module-level answer on a 30-line diff is under-specified — FAIL it and ask for the consumers.
6. **Verification check** — `Verified by` names a command/action + an observed result. Future tense ("will test") or modal ("should pass") → FAIL.
7. Emit verdict: PASS, or FAIL with the specific field + specific fix. The change does not advance until PASS.

## Verify (the check on the check)

- The validated brief belongs to THIS diff — spot-check one `Edge cases` citation and one `Blast radius` citation against the actual tree.
- `Verified by` claims were executed — for agent-authored changes, confirm the named command appears in the session's actual tool calls (the Trusted-Summary rule applied to self-reports).

## Anti-patterns this prevents

- **The Unowned Merge** — AI code accepted because it ran. The brief's `Why this shape` field is unanswerable without reading the code, which is the point.
- **The Paraphrase Brief** — "Updated the service to improve handling" restates the diff without explaining it. Caught by the echo check + citation check.
- **The Optimistic Verification** — "should work" / "tests should pass". Caught by check 6; same discipline as smoke-verify's Optimistic Boot Claim.
- **The Deferred Comprehension** — "I'll understand it when it breaks." The brief moves the 2 minutes of understanding to before the merge, where it's cheap — the post-production version of the same comprehension costs hours and a customer.
- **The Convention Bypass in Disguise** — a generic AI solution that fits no project convention can't fill `Why this shape` honestly; the gate converts silent drift into an explicit ADR-or-align decision.

## See also

- `engineering-principles.md § AI-assisted development` — the principle this skill mechanizes.
- `quality-principles.md` — WHY-not-WHAT comment discipline (the in-code sibling of the brief).
- `commands/pre-commit.md` / `commands/review-changes.md` — the gates that dispatch this skill.
- `align` pack `unhandled-io` detector — where an edge-case gap found in step A3 routes.
