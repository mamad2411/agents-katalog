---
name: deep-review
description: Multi-angle code review that adapts to what is being reviewed — a mid-flight worktree increment, a full PR before production, a merge-window integration sweep, or a security-only pass. Findings are scored, adversarially refuted, widened to the same defect elsewhere in the codebase, and reported to the native review UI. Use when the user asks to review changes, review a PR, sweep the codebase for integration drift, or run a security review.
argument-hint: "[--pr [N]] [--sweep [--since <ref|date>]] [--security] [--fix] [--amplify|--no-amplify] [--min-impact critical|high|medium|medium-low|low]"
---

# Deep Review

One review command, four modes. Absorbs the strongest parts of six prior review skills; see
`DESIGN.md` for what came from where and why.

<HARD-RULES>

1. **Never spawn Fable.** Not at any tier, not under any flag. When a finding warrants a stronger
   independent read, STOP and print the escalation block (§10). The operator invokes Fable
   themselves, in a fresh context.
2. **Never block a merge.** This command is advisory. It may emit a verdict; it may not act on one.
3. **Never auto-fix without re-reviewing the fix.** A fix for a review finding is not pre-vetted.
4. **Agents are read-only.** Parallel agents share one worktree — a writing agent corrupts the
   others' view.

</HARD-RULES>

## 1. Resolve mode and base ref

| Invocation | Mode | Base |
|---|---|---|
| `/deep-review` | **A** — increment | `git merge-base origin/main HEAD`, includes uncommitted |
| `/deep-review --pr [N]` | **B** — pre-prod gate | `origin/main` (three-dot) |
| `/deep-review --sweep [--since X]` | **C** — integration sweep | union diff of merges since marker |
| `/deep-review --security` | **D** — security-only | any of the above scopes |

**Always resolve `origin/main`, never local `main`** — a stale local main silently corrupts the
diff base. Run `git fetch origin` first. For Mode B, cross-check the computed base against
`gh pr view <N> --json baseRefName,baseRefOid`; if they disagree, trust `gh` and say so.

For Mode C, read the marker from `<REVIEWS>/state.json` (see §11). If absent, default `--since`
to the last merge commit on `origin/main` and say which ref you chose.

**Amplification (§8) runs by default in Mode B only.** `--amplify` enables it in Modes A, C, and D.
`--no-amplify` disables it **in every mode**, including the Mode A `--fix` path. Absent
`--no-amplify`, `--fix` in Mode A amplifies the findings it fixed (§12) without needing
`--amplify`.

**Fail fast, before spawning anything:** confirm the ref resolves (`git rev-parse`), confirm the
diff is non-empty, confirm the working tree state matches the mode. A bad ref must fail here, not
inside fourteen sub-agents.

**Commit or stash first.** If Mode A has uncommitted changes, note that agents will read the
working tree and must not write to it. If the tree is dirty in Modes B/C, stop and ask.

## 2. Gather context

Read, and pass to every angle agent:

- `CLAUDE.md`, `docs/CLAUDE.md`, `CONTEXT.md`, `docs/adr/`, any `CODING_STANDARDS.md` / `CONTRIBUTING.md`
- The project memory dir, if one exists for this project — as **suppressors** and **detectors** (§9)
- `<REVIEWS>/dismissals.json` — findings already rejected (§11)
- The spec (§3)

**Context isolation:** each agent receives crafted context only — the diff, the standards, its own
brief. Never your session history. You are the coordinator; do not review the diff inline, or you
burn the context needed to drive the pipeline.

## 3. Find the spec — three-way, and ASK if not found

Discovery order:

1. **Issue tracker** — check every connected issue-tracker MCP server (Jira, Linear, ClickUp,
   Asana, GitHub Issues, etc.) for a ticket referenced in the branch name or commit messages. If
   exactly one produces a match, use it silently. If more than one matches, or none clearly does,
   ask which to use. If a repo-specific tracker doc exists (e.g. `docs/agents/issue-tracker.md`),
   follow it.
2. **`docs/specs/`** — match the branch or ticket series
3. **PR body** (`gh pr view --json body`)

**If none is found, STOP and ask the operator where the spec is.** Do not silently skip the axis
and do not infer requirements from a stale document.

The spec drives three distinct questions. Keep them distinct:

| Question | Angle |
|---|---|
| Does the code do what the ticket asked? | `spec-conformance` |
| Did the ticket ask for **enough to be usable**? | `slice-completeness` |
| Does every hunk trace to the task at all? | `collateral` |

## 4. Select angles (applicability gating)

Run every applicable angle. Skip what cannot apply — do not run the contracts angle when no types
changed.

| Angle | Model | Runs when |
|---|---|---|
| `correctness` — logic errors, silent failures | Opus | any code change |
| `concurrency` — races, TOCTOU, check-then-act, missing locks | Opus | shared state, async, transactions, caches |
| `security` — OWASP Top 10 | Opus | any code or config change |
| `contracts` — types, invariants, API shape, data modeling | Opus | types/API/schema touched |
| `test-coverage` + **hollow-test detector** | Opus | code or test files touched |
| `spec-conformance` | Opus | always |
| `slice-completeness` | Opus | always |
| `collateral` | Opus | always |
| `quality` — maintainability + Fowler smell baseline | Sonnet | any code change |
| `error-handling` — swallowed exceptions, async errors, broad catch | Sonnet | any code change |
| `boundaries` — null/empty, off-by-one, numeric limits | Sonnet | any code change |
| `performance` — N+1, hot paths, unbounded memory | Sonnet | queries, loops, hot paths |
| `removal` — dead code, stale flags, feature-flagged-off branches | Sonnet | any change |
| `historical-context` — `git blame` on changed lines | Sonnet | high complexity, or churn-heavy files |

**Mode C swaps:** drop `historical-context` (everything is recent, so blame is noise). Add
`cross-pr-drift` (Opus), `duplicate-arrival` (Opus), `seam-consistency` (Opus),
`flag-accumulation` (Sonnet). See `references/mode-c-angles.md`.

**Mode D:** run only `security`, `concurrency`, and `contracts`, at maximum depth. See
`references/security-owasp.md`.

Angle briefs, including the Fowler baseline and the hollow-test procedure, are in
`references/angles.md`. Every angle brief ends with the same requirement:

> Every finding MUST include a concrete failure scenario: specific inputs or state → the wrong
> output, crash, or corruption that results. A finding you cannot make concrete is not a finding.

## 5. Fan out

Spawn all applicable angle agents **in parallel, in a single message**, using the models in the
table above. Each gets: the diff command, the commit list, the standards sources, the suppressor
and detector lists, the spec, and its own brief. Each returns a structured finding list.

Agents are **read-only**. State this in every brief.

## 6. Score — confidence × impact

For each raw finding, spawn a **Sonnet** scorer. It returns two integers.

**Confidence (0–100)** — is this real, or a false positive?
`0` refuted on light scrutiny, or pre-existing and unrelated to this change · `25` unverified,
might be real · `50` verified real but possibly a nitpick · `75` double-checked, will be hit in
practice · `100` certain and frequent.

**Never score a `sibling:` finding down for being pre-existing.** Out-of-diff is what a `sibling:`
finding (§8) *is*, not evidence against it. Score it on whether the rule actually holds at the
location it names. The `0` anchor above is for pre-existing issues **unrelated to this change**,
which a sibling — tied to a confirmed finding by a shared rule — is not.

**Impact (0–100)** — what happens if it ships?
`0–20` style · `21–40` maintainability, no functional effect · `41–60` edge-case errors or
degradation · `61–80` breaks core features or corrupts data under normal use · `81–100` runtime
failure, data loss, crash, or security breach.

Apply two filters, in order:

**(a) Mode floor** — drop anything below the mode's minimum impact:

| Mode | Floor |
|---|---|
| A increment | medium (41) |
| B pre-prod | medium-low (21) |
| C sweep | high (61) |
| D security | low (0) |

`--min-impact` overrides the floor. Its five values map to the impact bands below:
`critical` 81 · `high` 61 · `medium` 41 · `medium-low` 21 · `low` 0.

**(b) Progressive confidence** — higher impact needs less confidence:

| Impact | Min confidence |
|---|---|
| 81–100 | 50 |
| 61–80 | 65 |
| 41–60 | 75 |
| 21–40 | 85 |
| 0–20 | 95 |

**Floor exemptions** — these bypass filter (a) entirely, though not (b):
- `collateral` findings that are **deletions or value-reverts**
- `slice-completeness` findings — a missing layer
- findings whose category is prefixed `sibling:` (§8) — the parent finding is the evidence

All three are findings whose real cost is invisible in the diff.

The exemption is against the mode's **default** floor only. An explicit `--min-impact` overrides
the exemptions too: an operator who asks for blockers only means all categories, and a flag that
silently fails to bind on three of them is worse than no flag.

**Never report** (the false-positive catalogue):
- pre-existing issues in unchanged code — **except** a sibling of a CONFIRMED finding, under the
  same restated rule (§8)
- anything a linter, type checker, or compiler catches — assume CI runs
- pedantry a senior engineer would not raise
- issues explicitly silenced in code (lint-ignore comments)
- changes that are plainly intentional and part of the broader task
- anything in `dismissals.json` (§11), dismissed either way

## 7. Refute

For each survivor, spawn an **Opus** refuter. Give it the **claim only** — never the finder's
reasoning — plus the code the claim concerns and the repo standards. For a finding inside the diff
that is the diff hunk; for a `sibling:` finding (§8), which has no hunk, it is the cited file and
line range. Brief:

> Try to refute this finding. Default to refuted if uncertain. Report `refuted: true|false` with
> reasoning, and whether the stated failure scenario actually reproduces.

`refuted: false` → **CONFIRMED**. Uncertain or split → **PLAUSIBLE**. `refuted: true` → dropped.

Finder and refuter share a model, so their errors correlate; independence here comes from
isolation, not diversity. Treat PLAUSIBLE as genuinely uncertain.

## 8. Amplify — widen the blast radius

Default-on in **Mode B**. `--amplify` enables it in Modes A, C, and D. `--no-amplify` disables it
in **every** mode and beats `--amplify` if both are passed. It also runs, narrowly, after an
accepted fix in a run that had no earlier amplification pass (§12).

A CONFIRMED finding is **one instance of a rule**, and the rule usually has other instances. For
each CONFIRMED finding, spawn one **Opus** amplifier. It restates the defect as an abstract rule,
then searches for other instances along six axes — peer **fields**, **branches**, **callers**,
**layers**, **claims**, **exclusions** — plus precedent from repo history. Full brief in
`references/amplification.md`.

Three properties carry the stage, and the brief enforces all three:

- **It never searches the literal text of the parent finding.** Searching the phrasing you already
  hold matches only what you already found; the method quietly confirms where you started.
- **It inspects every candidate before proposing it.** A speculative list of locations
  over-generates, and each false candidate costs a full refutation below.
- **Depth 1.** A sibling never spawns its own amplifier, not even after being fixed. Cap 5
  candidates per parent finding; disclose any truncation under "Areas not covered" (§10).

Siblings are **not** trusted for being siblings. Each re-enters the pipeline at §6 and §7 —
independently scored, independently refuted. They bypass filter (a), the mode floor, for the same
reason `collateral` deletions do; they must still clear (b).

**Classify each returned sibling by location — the amplifier does not only find out-of-diff code.**
Three of the six axes (peer fields, peer branches, peer callers) routinely land in the parent's own
file, and the other arm of a conditional this very diff added is a sibling like any other. The
coordinator holds the diff, so the coordinator makes this call, not the amplifier:

| Location | Category | Treatment |
|---|---|---|
| **inside the diff** | its plain category, no prefix | an ordinary finding in every respect — counts toward the verdict, can escalate, is eligible for `--fix`. Amplification found it; that does not make it less a part of this change. |
| **outside the diff** | `sibling:<original-category>` | the containment rules in §10 and §12 apply |

**"Inside the diff" means changed lines, not changed files.** A result sitting in an untouched hunk
of a file this change happens to edit is **outside** — the operator put those lines up for review,
not the rest of the file. Precisely: a result is inside when its cited location touches at least
one line the diff **adds, modifies, or deletes** — for a deletion, the position the removed lines
occupied. Otherwise it is outside. All three classes count: a defect introduced by removing code is
introduced by this change as surely as one introduced by adding it, and `collateral` runs on every
change specifically to catch it. "The diff" is whatever §1 resolved for this run, which in Mode A
includes uncommitted working-tree changes.

Getting this wrong in the file-level direction is the expensive error: it lets `--fix` edit
untouched code and lets an old defect elsewhere in a large file block a clean PR.

**Deduplicate across amplifiers.** Two parents can surface the same location under different rules.
Score and refute it once; report it once, naming both parents.

The `sibling:` prefix is therefore load-bearing: §6's floor exemption, §6's never-score-down rule,
§10's axis assignment, and §12's fix exclusion all key on it, and all of them mean *out-of-diff*.
A sibling keeps the category describing the defect (`sibling:concurrency`, `sibling:contracts`)
rather than losing it to a bare axis name.

Before searching, read every `not-real` entry in `dismissals.json` (§11) that carries a stored
`rule`. If your restated rule matches one, stop — return the rule, no siblings, and say you stopped
on a dismissed rule. `wont-fix` entries never invalidate a rule; ignore them here.

**The matching bar is strict, and the suppression is disclosed.** Two rules match only if they
describe the same defect shape at the same level of generality. **When in doubt, do not match** —
this is an exclusion, and over-matching an exclusion is a hole rather than a false positive. A
wrong non-match costs one amplifier run; a wrong match costs every sibling of a confirmed defect,
silently. Whenever an amplifier stops this way, list it under "Areas not covered" (§10) with the
rule it matched. A suppression nobody is told about is indistinguishable from a search that found
nothing.

## 9. Suppressors and detectors

From the project memory dir:

**Suppressors** — known non-issues. Do not report. The one that generalises to any repo: a test
failure that was already failing on `main` before the change under review.

> **Verify before silencing.** Memory records what was true when written. Confirm the observed
> failure is actually the known one — same test, same cause — before suppressing. A new failure in
> a known-flaky file must not be waved through.

**Detectors** — repo-specific checks derived from past failures. Generic:

- **hollow tests** — green tests that prove nothing; procedure in `references/angles.md`

**Examples from my stack — replace these with your own.** Real quirks from Laravel/Blade/Alpine
work. They will not fire on your codebase, and this list is meant to be edited: Blade `@if` needing
a non-word boundary, Blade comments inside `@php`, `x-data` comment double-quotes, Alpine duplicate
`:key`.

## 10. Report

Emit findings with `ReportFindings` to the native review UI.

**Preserve axis separation.** Three axes, never merged or re-ranked against one another:

| Axis | Categories |
|---|---|
| spec-side | `spec-conformance`, `slice-completeness`, `collateral` |
| standards-side | every other angle in §4 |
| sibling | any category prefixed `sibling:` (§8) |

`ReportFindings` has no field for axis, parent, rule, or the axis a sibling was found on. Encode
them: the report axis rides in `category` as the `sibling:` prefix; open each sibling's `summary`
with its parent finding, the restated rule, and the search axis that surfaced it. Keep
`short_summary` (60 chars) to the defect claim alone — it is the compact label, so parent and rule
do not belong in it. Per-axis counts go in the surrounding message, not the tool call.

Rank within each axis. Report counts per axis in the summary, so a clean standards pass cannot
visually bury a wrong-feature fail, and a long sibling list cannot bury either of the others.

Every `sibling:` finding states the restated rule, the parent finding it came from, and —
explicitly — that it lies **outside the diff**. An amplifier result inside the diff states its
parent and rule too, but is otherwise reported as the ordinary finding it is.

Alongside the findings, state:

- **Areas not covered** — angles skipped by gating, files too large to review, sibling candidates
  truncated at the cap, **amplifiers that stopped on a dismissed rule** (name the rule), anything
  you could not verify. A clean review that does not say what it skipped is not a clean review.
- **Mode B only:** an advisory verdict. `NOT RECOMMENDED FOR MERGE` if any CONFIRMED finding
  **inside the diff** scores impact ≥ 81 — which includes an amplifier result that landed inside
  the diff, since that carries no prefix and is an ordinary finding (§8). Advisory — take no action
  on it. A `sibling:` finding never drives the verdict: it is a defect in code this change did not
  touch, and blocking a good PR on a problem elsewhere is exactly the burying that axis separation
  exists to prevent. Report a `sibling:` finding at impact ≥ 81 prominently, at the top of its own
  axis, and say plainly that it is not a reason to hold the merge.

### Escalation — never auto-invoked

If any of these hold, append the escalation block and **stop**:

- a contested finding (PLAUSIBLE) with impact ≥ 61
- any impact ≥ 81 CONFIRMED finding **inside the diff** at the Mode B gate
- a Mode C `cross-pr-drift` or `seam-consistency` finding

A `sibling:` finding never triggers escalation, for the same reason it never drives the verdict. Escalation
**stops the review**, and halting on a defect outside the change under review turns a widened
search into a blocker.

```
## Escalate — recommend a fresh Fable session

N findings warrant a deeper independent read. Nothing has been invoked.
To run it yourself:

  claude --model fable
  > Review this contested finding in a fresh context:
    [file:line · claim · both verdicts · diff hunk]
```

## 11. Persist

`<REVIEWS>` = `~/.claude/projects/<project-slug>/reviews/` — **outside the repo, never committed.**
A findings history inside the codebase travels to GitHub and is a roadmap for anyone with read
access.

```
<REVIEWS>/
  YYYY-MM-DD-<mode>-<ref>.md   full findings, scores, verdicts
  dismissals.json               fingerprint → { decision, reason, rule }
  state.json                    last sweep ref + timestamp
```

Fingerprint a finding as `sha1(category + file + normalized-claim)` so it survives line drift, and
**strip any `sibling:` prefix from the category first**. The same defect at the same location must
hash the same however it surfaced — otherwise a finding you dismissed when an angle raised it comes
back the moment an amplifier rediscovers it, and the promise that a rejected finding stays rejected
quietly fails at exactly the boundary this change introduced.

Siblings still fingerprint independently of their parents — different file, different claim.

Each `dismissals.json` entry carries three fields:

| Field | Value |
|---|---|
| `decision` | `not-real` or `wont-fix` — never omit it |
| `reason` | free text |
| `rule` | the restated rule (§8) when this finding is a **parent** that went through amplification; `null` otherwise — including for every sibling |

- Check `dismissals.json` **before** scoring — a dismissed finding never reaches the refuter,
  whichever way it was dismissed.
- After reporting, offer to record dismissals for anything the operator rejects.
- **Type every dismissal, and store the rule with it.** `not-real` means the claim was wrong: its
  `rule` is thereafter invalid, and §8 refuses to amplify any restated rule matching it — including
  when a *different* finding raises the same rule later. `wont-fix` means the claim was right and
  you chose not to act: it suppresses that fingerprint only, and leaves the rule available, so a
  different finding under the same rule still amplifies normally. A `wont-fix` recorded as
  `not-real` silently hides the same defect everywhere else it occurs.
- **Do not invent a `rule`.** If no amplifier ran — any mode where §8 was off, or any run with
  `--no-amplify` — write `rule: null`. A fabricated rule recorded as invalid will suppress
  legitimate amplification later. The amplifier returns its restated rule on every run, including
  runs that found no siblings, so a rule exists to store wherever amplification happened at all.
- **Only a parent's dismissal can invalidate a rule.** A dismissed sibling always stores
  `rule: null`, however it was typed. One false-positive location must not disable a rule that
  produced three real findings elsewhere.
- Dismissing a parent does **not** dismiss its siblings, and dismissing a sibling does not dismiss
  its parent. Each was scored and refuted on its own and each is rejected on its own.
- A finding dismissed 3+ times may be proposed as a standing suppressor — subject to §9's
  verify-before-silencing rule.
- Mode C writes `state.json` on completion.

## 12. Fix — Modes A and B only

`--fix` is rejected in Modes C and D. Mass-fixing without a bounded diff has too large a blast
radius, and a plausible-looking security fix can still be exploitable.

```
CONFIRMED findings INSIDE THE DIFF only
   — PLAUSIBLE is never auto-fixed, and neither is a sibling
   ↓ apply (Opus)
   ↓ re-review the FIX DIFF ONLY, through `correctness` + the angle that raised it (Opus)
   ↓ fix introduced a new CONFIRMED finding? → revert that fix, report why
   ↓ if §8 did not already run this pass: amplify the fixed finding (§8) — depth 1
```

**`sibling:` findings are never auto-fixed.** They sit outside the diff — that is what the prefix
means (§8) — and this section's whole bound is the diff: editing code the operator did not put up
for review is the blast radius the first paragraph rules out. It is also unexecutable as
written, since the re-review step runs "the angle that raised it" and no §4 angle raised a sibling.
Report them; let the operator decide whether they become their own change. An amplifier result that
landed **inside** the diff carries no prefix, is an ordinary finding, and is fixed like one.

Any amplification triggered by this section runs after §10 and §11 have already executed. Append
its results to the re-report, and persist them alongside the fix outcomes.

**Amplify each finding at most once per run**, whichever stage reaches it first. Wherever §8 ran
before reporting — Mode B by default, and Mode A, C, or D under `--amplify` — the fixed findings
were already amplified in that pass, so the fix loop must not repeat it.

The fix-path amplification exists for the one case §8 does not cover: **a `--fix` run in which
nothing was amplified pre-report** — in practice Mode A without `--amplify`. A fix is the moment
the same defect one field over is most likely to be missed, because the re-review step above asks
whether the fix broke something *here* and never whether the thing it fixed exists somewhere else
too. `--no-amplify` suppresses this path like any other.

Report an outcome per finding: `fixed` · `reverted` · `skipped` · `no_change_needed`. Re-report
through `ReportFindings` with the `outcome` field set.

This loop exists because a fix for a review finding has shipped a new defect before. The fix is
not pre-vetted merely because it fixes something real.

## Model table

Change models here and nowhere else.

| Stage | Model |
|---|---|
| Reasoning angles | `opus` |
| Mechanical angles | `sonnet` |
| Scorer | `sonnet` — flip to `haiku` to cut cost at volume |
| Refuter | `opus` |
| Amplifier | `opus` |
| Fix applier / fix re-reviewer | `opus` |
| **Fable** | **never** |
