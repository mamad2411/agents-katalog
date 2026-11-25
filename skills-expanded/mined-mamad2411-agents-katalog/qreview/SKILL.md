---
name: qreview
description: "This skill should be used when the user asks to \"review an artifact\", \"get multiple perspectives on\", \"multi-agent review\", \"qreview\", or wants N independent reviewers to evaluate any output (code, content, strategy, design) against requirements. Spawns 2-5 clean-context agents in parallel with max-severity deduplication."
version: 0.3.0
---

# /qreview -- Multi-Agent Artifact Review

Single-pass, multi-perspective review: N clean-context reviewers evaluate an
artifact against its requirements, in parallel, each blind to the others.
Findings are validated, deduplicated by max-severity, and sorted P0-first.
Diagnose-only — `/qreview` never edits the artifact (use `/qloop` to converge).

> **Hard rule: NEVER hand-write a review/pipeline workflow script.** The ONLY
> sanctioned path for this skill is `scriptPath=review-loop.workflow.js`. If
> that script file is missing, STOP and report — do not improvise a workflow.
> A hand-rolled script has no `model:` tiering, so every agent it spawns
> silently inherits the invoking session's model (including expensive
> long-context variants) — this is the single largest source of runaway spend
> observed across past runs. There is no acceptable workaround; a missing
> script is a bug to report, not a gap to paper over.

**This skill runs via the ai-review-toolkit ultracode Workflow**
(`review-loop.workflow.js` with `rounds: 1`). The Workflow owns the deterministic
loop — parallel reviewer fan-out with resolved models, JS synthesis/dedup, and
convergence checking. Invoking `/qreview` **is** the explicit opt-in to run that
Workflow. The deterministic adjudication is the Python library's JS port, drift-
locked against it in CI, so verdicts match the Python oracle exactly.

## Protocol

Follow in order.

### 0. Version check (best-effort, non-blocking)

Run `python3 <tools>/version-check.py check` once at the start. It is rate-limited
(~once/day) and fails silent-and-open. If it prints an upgrade notice, relay that
single line to the user, then continue — never block, retry, or wait on it.

### 1. Identify artifact + requirements

Accept a file path or inline content for each. Write inline content to a temp
file so agents can `Read` it. If no requirements exist, ask the user what the
artifact must accomplish and record that as the requirements file.

### 2. Resolve the review team (deterministic, Python)

Run the team selector and capture the resolved team (each reviewer carries its
tiered `model`). From the plugin, tools are under `tools/`; in the local fork
they are at `~/.claude/ai-review-tools/`.

```
python3 <tools>/team-selector.py "<short artifact description>" \
  --artifact <artifact_path> --json \
  --files <N> --context-window 200000 [--max 5] [--high-stakes]
```

- Default team is **3** reviewers, seated by domain relevance (use `--max 5`
  for genuinely high-stakes reviews; docs default to 2 — pass `--max 2`).
- `--files N` — files the change spans (escalates only the top-2 domain lenses
  to Opus if `> 3`). The artifact's byte size drives the ">40% of context"
  rule automatically. Opus seats are hard-capped at 2 per team.
- `--high-stakes` — force the security lens to Opus (it otherwise earns Opus
  only when the security/compliance domain actually scores).

Parse the JSON `team` array — objects of `{name, model, review_lens, ...}`. This
is passed straight into the Workflow; **do not re-tier or override models by
hand** — the escalation policy already ran.

### 3. Run the review Workflow

Resolve the workflow script path (it sits in `js/` beside `tools/`):
- plugin: `<plugin>/js/review-loop.workflow.js`
- fork: `~/.claude/ai-review-tools/js/review-loop.workflow.js`

Invoke the **Workflow** tool with that `scriptPath` and:

```json
{
  "artifact": "<artifact_path>",
  "requirements": "<requirements_path>",
  "team": <team array from step 2>,
  "rounds": 1,
  "threshold": 0
}
```

`rounds: 1` means single-pass, diagnose-only — the workflow reviews and
synthesizes but runs no fixer (it returns an `escalated` outcome listing any
unresolved P0/P1, which for `/qreview` is simply "here is what to fix"). Capture
the **Run ID** and the `workflows/<runId>.json` path from the tool result.

### 4. Present findings

The Workflow returns `{ outcome, rounds, final_findings, final_counts, history }`.
Present `final_findings` sorted by severity (P0 first). For each: id + severity,
title, requirement, finding, recommendation, evidence (file:line), sources
(which reviewers flagged it). Then the convergence line: **converged (safe to
ship)** = zero P0, zero P1, low-severity within threshold; otherwise state how
many P0/P1 remain.

**Never present a clean result from a panel that did not run.** The verdict carries
`reviewers <returned>/<requested> returned`, and a review whose panel fell below
quorum comes back `escalated` with `valid: false` on that `history` entry and a
reason per missing reviewer (`reviewers_missing`). Report that as an ENVIRONMENT
failure and re-run it: zero findings there means nobody looked, not that the
artifact is clean.

### 5. Scorecard (mandatory)

Run the deterministic scorecard against the run and show it verbatim (pure,
reproducible, no LLM); it is the final OUTPUT to the user, but step 6 below still
runs after it:

```
python3 <tools>/scorecard.py --workflow <session>/workflows/<runId>.json
```

Its first line is the VERDICT: status, rounds used against the budget (and their
kinds), total tokens, USD, and wall-clock, followed by the escalation reason when
there is one. Then Process, Issues Found, Token Cost (per-model USD), and Model
Execution Time (per-agent wall-clock rolled per model + the workflow wall-clock
total).

### 6. Record QAC inputs (fail-open telemetry)

Persist the run's findings so `fleet metrics --qac` prices the rework (companion
to fleet REQ-COST-153..157; spec: `qreview/requirements.md` REQ-QAC-201/203). The
fleet contract assigns the findings keys to the session that PRODUCED the
findings, so the orchestrating session writes to its own key, with no `--session`
(that flag exists for the build-supervisor's ask-size case only):

```
fleet qac-inputs --p0p1 <N> --p2p3 <N> --review-rounds <R>
```

- Derive the numbers mechanically from the workflow result (`{final_counts,
  history}`), never by judgment. `--p0p1` = count of P0/P1 entries in
  `final_findings`. `--p2p3` = the round-level significant-P2/P3 count, matching
  qloop: `history[0].significant - (history[0].counts.P0 +
  history[0].counts.P1)` (the returned `significant` is a per-round count that
  always includes P0/P1, so subtracting them leaves the reviewer-flagged
  significant P2/P3; single pass, so round 0 is the only round). Do NOT count raw
  P2/P3 in `final_findings`: the fleet key is `p2p3_significant_findings`, and the
  trivial cosmetic nits the engine spot-fixes are not significant. `--review-rounds`
  = review rounds EXECUTED, for single-pass `/qreview`: 1. (The fleet key's gloss
  is "rounds until no P0/P1"; an unconverged pass records the rounds it ran, and
  its unresolved P0/P1 are already in `--p0p1`, so the pair reads together.)
- The counts are per-SESSION cumulative, not per-run: the artifact key is this
  session, and the findings keys keep the MAX across writes (monotonic floor; a
  smaller later write does not take). If this session already recorded a review
  (`fleet qac-inputs` with no value flags is read mode; the stored values are the
  `qac_inputs` object, absent keys null), write the running total: stored value
  plus this run's counts. Write once per run, after the run ends, never per round.
- `--reset` deletes the WHOLE artifact for the key, including any `ask_*` a
  supervisor wrote there and the `_writers` trail. It is for a typo'd count
  only: read first, then re-supply every key it held in the same command.
- Own key is right ONLY when this session is part of the build under review (a
  spawned `pr<N>-reviewer` child, or a builder reviewing its own work). Rows
  group by parent, so if this is a cockpit-class session reviewing another
  build's work, SKIP the write entirely; do not record at your own key (recording
  the reviewer child at spawn time, per the build-supervisor charter, is the way
  a supervisor gets these numbers onto the right build).
- Fail open, exactly this shape: run the command; any non-zero exit or missing
  CLI is one printed line ("QAC inputs: skipped") and you move on. Never retry,
  never hunt for the CLI, never ask the user; recording telemetry never blocks
  or fails a review. Surface the outcome in the run's final output as one line
  ("QAC inputs: wrote p0p1=N p2p3=N rounds=R at <key>", or "QAC inputs: skipped")
  so a close-out reader can tell a write from a skip. There is no CI flag to
  pass; the CI-red signal is read-time-computed on the fleet side.

## Severity taxonomy

| Severity | Meaning | Action |
|----------|---------|--------|
| P0 | Blocks shipping (correctness, security, data loss, requirement violation). | Fix before any release. |
| P1 | Must fix before v1 (quality, error handling, incomplete coverage). | Fix before feature-complete. |
| P2 | Should fix (code smell, suboptimal pattern, minor UX, doc gap). | Next iteration. |
| P3 | Nice to have (style, optional optimization, cosmetic). | If time permits. |

## Key rules (enforced in code, not prose)

- **Dissent is default / max-severity wins.** One reviewer's P0 is never
  downgraded by majority — `deduplicateFindings` merges by normalized title and
  keeps the max severity.
- **Clean context per reviewer.** Each runs in a fresh agent, blind to the others
  and to the team composition.
- **Pre-existing issues are in-scope.** Reviewers do not self-censor as "out of
  scope."
- **Reviewer quorum.** Every requested reviewer is attested as returned or missing
  with its failure reason; a review below quorum (a majority of the panel, floor 2)
  is INVALID, never clean. A dead reviewer and a reviewer who found nothing are not
  the same thing.

## Tools

- **`js/review-loop.workflow.js`** — the ultracode Workflow (the loop engine).
  Generated from `js/adjudication.mjs` + `js/prompts.mjs`; do not hand-edit.
- **`tools/team-selector.py`** — deterministic domain classification + team
  selection + model tiering (Python oracle).
- **`tools/scorecard.py`** — deterministic end-of-run scorecard.
