---
name: compute-anchor-density
description: Score the anchor-density of a generated artifact (rule / agent / skill / command / ai-file) on four axes (name density, path density, signal density, specificity) for a total 0-100. Used by /setup-project Phase 5.5 in REFINE mode to identify which artifacts are shallow (< 70) and need round-two re-anchoring, AND to detect plateau (Δ ≤ 2 between runs = "no further refinement available").
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: compute-anchor-density

## Purpose

REFINE rewrites only artifacts whose round-one anchor is shallow. To decide which is "shallow," we need a rubric score applied the same way every run, not a vibe check. This skill is the rubric. **It ships no scorer script:** the model applies the four axes below, so the score is reproducible only as far as each axis cites its evidence (the counted lines, the cited `file:line`s). Label every score `model-scored`, print the per-axis evidence beside it, and treat a Δ under the plateau threshold between two runs on an unchanged tree as noise, never as a signal. It's also the plateau detector — when 2nd / 3rd `--refine` runs produce Δ ≤ 2 points across the artifact set, REFINE exits with "plateau reached."

## Premise

- Real source is the truth. Read the artifact + the extraction substrate before scoring — the score is computed from observed citations, not from impressions of "looks anchored."
- Every counted identifier resolves in `_extracted-codebase.md` or `_refine-extract.md`; every counted path exists on disk.
- Miscitations (identifier off-by-one, ghost path) are deductions, not silent passes.
- Empty signal is honest — a 0 on an axis with a recorded reason is a valid score.
- Fabrication — crediting a citation that doesn't resolve, or a signal category the substrate doesn't carry — is the failure mode the deduction rules exist to penalize.

## Mechanical halt

- Hand-wave verdicts — `PLATEAU` without `-DEEP`/`-WEAK`, `verdict_message` without enumerating weak phases, "looks anchored" with no axis breakdown — REFUSE to emit.
- The scorer regenerates the JSON with all four axes populated AND the verdict tagged with one of `PLATEAU-DEEP` / `PLATEAU-WEAK` / `NOT-PLATEAU`.
- If extraction is genuinely missing for a signal category, the axis scores 0 and the JSON records `<NOT-DETECTED: <category>>` in the sibling reason field.
- Never synthesize a phantom signal, identifier, or path to inflate an axis — every axis is auditable against the substrate.

## When to use

- `/setup-project --refine` Phase 5.5 — score every Phase-4-generated artifact (`.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, `.claude/rules/*.md`, `.claude/commands/*.md`, `ai/*.md`).
- Internally by Phase 4.6-DEEP — to identify which artifacts to re-anchor (skip ≥ 70).
- On-demand via `/health` when the user wants to know "how anchored is my setup, really?"

## Inputs

- `artifact_path` — absolute path to the file to score.
- `extracted_codebase_path` — `.claude/_extracted-codebase.md` (round-one extraction substrate).
- `refine_extract_path` (optional) — `.claude/_refine-extract.md` (round-two extraction substrate; required for high signal-density scores).
- `sampled_sections` — the list of `## <Section>` headings in `_extracted-codebase.md` that carry a `[SAMPLED: <seen>/<present> <unit>]` marker, as written by `extract-codebase-overview § Step 2.5`. Empty list = round-one read everything it declared. Read directly from the substrate rather than being passed in when the caller omits it — it is a `grep` over a file this skill already opens. **This is a verdict input, not a scoring input**: it never touches any of the four axes (see Step 7's coverage precondition, and § Anti-patterns on why coverage may only demote).
- `plateau_consumed_prior` / prior `.claude/_setup-quality.md` — the baseline the plateau delta is computed against, plus any `coverage-accepted:` line a human recorded there (Step 7).

## Procedure

### Step 1 — Locate the `## Project-specific` block

Every Phase-4-generated artifact ships with markers:

```
<!-- project-specific:start -->
## Project-specific (auto-generated, regenerate with `/setup-project --refine`)

...content...

<!-- project-specific:end -->
```

> **The example above is FENCED on purpose — leave it fenced.** A `<!-- project-specific:start -->` line only counts as a live anchor when it sits at column 0 **outside** a ``` fence. That rule is what lets this file — and `apply-pack-adaptation`, the other file that teaches the convention — document the markers without claiming to carry one. Both `scripts/apply-anchors.sh § has_live_anchor` and `scripts/audit-anchoring.sh § has_live_anchor / extract_anchor_block` implement exactly that test, and they must keep agreeing.
>
> **Why this note exists**: when the injector matched a bare `^<!-- project-specific:start -->$` while the auditor skipped fenced regions, these two skills deadlocked on a real 8,151-file repo — `apply-anchors.sh` skipped them as "already anchored" (Injected 0 / Already 234) and `audit-anchoring.sh --strict` failed them as `anchor-too-thin(0-lines)`, C2d at 99%, with a printed remediation ("re-run apply-anchors.sh") that was a no-op on precisely those files. Unfencing this example, or hand-writing a marker at column 0 anywhere below, restores that deadlock. Scoring this file: its own live anchor is the injected block near the top, **not** the example above.

If markers are absent → the artifact has zero project-specific anchor. Score = 0/100. Record reason: `markers-missing` (this is a round-one bug; flag for re-run of standard Phase 4.6, not REFINE).

If markers present → extract the block content (between the markers). All scoring below applies to this block.

For `ai/*.md` files, the markers are `<!-- refine-enriched:start -->` ... `<!-- refine-enriched:end -->`. If absent in REFINE mode, score the whole file body but cap "name density" at 12/25 (since the round-one auto-population did include detected facts, just not deeply).

### Step 2 — Score Name density (0-25)

Count concrete project identifiers in the block. An identifier is:

- A class / function / module name appearing anywhere in `_extracted-codebase.md` (most often `## Modules`, `## Base classes`, `## Data model`, `## API surface`) or in `_refine-extract.md` (any section). There is no `## Identifiers` section — `extract-codebase-overview § Step 14` enumerates the 13 sections that file has and that is not one of them. Scoring against a section that never existed silently scored every round-one identifier as uncountable.
- A table column / model field / migration name.
- An endpoint path (e.g. `POST /api/invoices`).
- A package/module name from this project (NOT external libs).

Rules:
- Each unique identifier counts ONCE (repetition doesn't multiply).
- Identifiers must appear verbatim in extraction. Cross-check. If the artifact cites `BillingService.create_invoice` but extraction shows `BillingService.create_invoice_with_line_items`, that's a MISCITATION — DEDUCT 5 (capped at 0).

Scoring:
- 0 unique identifiers → 0
- 1-2 → 8
- 3 → 13
- 4 → 18
- 5 → 22
- ≥ 6 → 25

### Step 3 — Score Path density (0-25)

Count concrete file path or `file:line` citations in the block.

Rules:
- A bare `file.py` is a path. A `file.py:42` is a path-with-line (counts as 1, but verified-existence carries more weight).
- For each citation, verify the file exists in the project (use the codebase profile's file inventory). If the cited file does NOT exist → MISCITATION, deduct 5 per ghost path.
- For `file:line` citations, the verification is harder (we can't always confirm the line). Heuristic: if the file exists AND total lines ≥ cited line, accept. Otherwise flag as ghost.

Scoring (after deductions):
- 0 → 0
- 1 → 8
- 2 → 13
- 3 → 18
- 4 → 22
- ≥ 5 → 25

### Step 4 — Score Signal density (0-25)

Signal density measures how many of the deep-extraction inputs the block actually consumes. Sources:

| Signal | Where to find it in `_refine-extract.md` |
|---|---|
| domain-entity | `## Domain entities` — entity names with field lists |
| invariant | `## Domain entities` → `cross_entity_invariants` or per-entity `invariants:` |
| lifecycle-event | `## Domain entities` → per-entity `lifecycle_events:` |
| flow | `## Flows` — flow names |
| hot-path | `## Hot paths` — path names |
| n+1-citation | `## Hot paths` → per-path `n_plus_1_sites:` |
| missing-index | `## Hot paths` → per-path `missing_indexes:` |
| layer-or-boundary | `## Architecture` — layer or boundary names |
| emergent-convention | `## Conventions (emergent)` — pattern names |
| contested-convention | `## Conventions (emergent)` → `contested_conventions:` (round two), or a `[CONTESTED: <A> n/N, <B> m/N]` row in `_extracted-codebase.md § Conventions` (round one) |
| failure-theme | `## Failure history` → `recurring_themes:` |

Count distinct signal categories the block consumes. A block can cite a `domain-entity` AND a `flow` AND an `emergent-convention` — that's 3 distinct signals.

**`contested-convention` scores like any other signal, deliberately.** A block that says "this codebase is split 6/4 between two error-handling shapes, both live, here are the counts and a citation for each" is MORE useful to an agent than one asserting a winner that is true of 60% of the files — it stops the agent from "fixing" the other 40%. Contested entries carry no `pattern:` key, so a scorer that only looks for pattern names credits them zero and the honest extraction scores below the averaged one. That inversion is what this row removes: recording a contest is rewarded, not penalised.

Rules:
- Count a signal when its upstream extraction gate is **STRONG or MEDIUM**; never when it is **WEAK**.
  WEAK means the extractor found nothing usable, so a block citing it is citing a gap. MEDIUM means
  it found real, cited signal and less of it — `extract-failures-from-history` is the one skill that
  declares the tier (`**MEDIUM**: 1 recurring theme found`), and one theme whose diffs were read and
  whose SHAs are cited is exactly as consumable per-citation as three. Excluding it scored the
  honest thin extraction at **0** on `failure-theme` while a WEAK one also scored 0 — a tier that
  changes no consumer's behaviour is not a tier, and this row is what makes it one. The other five
  round-two skills are binary STRONG/WEAK, so for them this rule reads exactly as before.
- A block is said to "consume" a signal if it uses the signal's NAME and at least 1 of the signal's FIELDS (citation, count, etc.).

Scoring:
- 0 distinct signals consumed → 0
- 1 → 8
- 2 → 13
- 3 → 18
- 4 → 22
- ≥ 5 → 25

### Step 5 — Score Specificity (0-25)

**This axis is a positive test, not a blocklist.** It used to start at 25 and deduct 5 per phrase
from a nine-string list — which meant any prose avoiding those nine exact strings scored a perfect
25. "Follow the team's established patterns for this layer" hits none of them and is precisely the
sentence the axis exists to catch. Worse, it made this the one axis a generator could max out by
writing *more confident* prose, and confident prose with no referent is the failure the whole rubric
is built against. It is now scored the other way round: earn it by pointing at something.

**Unit of scoring: the directive.** A directive is a sentence or bullet that tells a reader to do,
prefer, avoid or check something — imperative mood, or containing `MUST`, `MUST NOT`, `SHOULD`,
`always`, `never`, `use`, `prefer`, `avoid`, `call`, `extend`, `wrap`, `validate`. Non-directive
prose (framing, rationale) is not counted either way; a block may explain itself freely.

A directive is **grounded** when it names, in the same directive, at least one of:

- a project identifier that Step 2 already verified against extraction, or
- a project path / `file:line` that Step 3 already verified exists, or
- a number, threshold or version taken from extraction (`≥3 extenders`, `timeout 30s`, `v0.14`).

Otherwise it is **floating**. Score:

```
grounded_ratio = grounded_directives / total_directives
```

| `grounded_ratio` | Score | Reading |
|---|---|---|
| ≥ 0.80 | 25 | nearly every instruction points at this repo |
| 0.60 – 0.79 | 18 | mostly grounded, some filler |
| 0.40 – 0.59 | 13 | half the advice would fit any project |
| 0.20 – 0.39 | 8 | mostly generic with decoration |
| < 0.20 | 0 | generic prose wearing project clothes |
| `total_directives == 0` | 0 | a block that instructs nobody anchors nothing |

**Deductions still apply, on top**: −5 per angle-bracket placeholder left in the block (`<TODO>`,
`<FIXME>`, `<base>`, `<entity>`, `<service>`, `<module>`, `the project's <X>`) or per auto-comment
announcing un-filled content. Capped at 0. These are unambiguous un-filled-in output, not a judgement
about prose quality, which is why they survive as deductions.

**Why the change matters to the run, not just to the number.** Specificity was the axis that let a
block reach `6 identifiers + 5 paths + 0 signals + 25 = 75 = ANCHORED` — permanently skipped by
Phase 4.6-DEEP — while consuming **zero** deep-extraction signal and instructing the reader to
"follow established patterns". Under the positive test that block's directives are floating, so it
scores SHALLOW and gets re-anchored, which is what a run with unconsumed signal should do.

### Step 6 — Compute total + classify

Total = sum of the 4 axes (range: 0-100).

Classification:
- **DEEP** ≥ 85 — the block is concrete enough that an agent reading it gets project-specific guidance. Phase 4.6-DEEP skips this artifact (further re-anchoring won't help much).
- **ANCHORED** 70-84 — sufficient. Phase 4.6-DEEP skips by default but rewrites if `--refine --aggressive` is passed.
- **SHALLOW** < 70 — Phase 4.6-DEEP rewrites this artifact's `## Project-specific` block.
- **MISSING** = 0 (markers absent OR block empty) — flag separately; not a REFINE concern (it's a Phase 4.6 / round-one bug).

### Step 7 — Compute plateau verdict (when scoring multiple artifacts for the run)

After scoring all artifacts, compare to the prior `.claude/_setup-quality.md` (if present):

```
plateau_delta     = avg(this_run_scores) - avg(prior_run_scores)
plateau_consumed  = signals_consumed_this_run / signals_available_in_refine_extract
weak_phase_count  = count(phases in 2.7..2.12 with [REFINE-WEAK: ...] flag)
avg_score         = avg(this_run_scores)
coverage_blocked  = (sampled_sections is non-empty) AND (no `coverage-accepted:` line in the prior
                     `.claude/_setup-quality.md` naming the CURRENT seen/present figures)
```

The plateau verdict is THREE-WAY — never a single binary. The two plateau classes carry very different user actions:

| Verdict | Conditions | Per-artifact tag | Run-level message |
|---|---|---|---|
| **PLATEAU-DEEP** | `plateau_delta ≤ 2` AND `plateau_consumed ≥ 0.85` AND `avg_score ≥ 80` AND **NOT `coverage_blocked`** | `LEAVE-DEEP-IDEMPOTENT` | "Plateau reached (DEEP) — setup is anchored; further `--refine` adds nothing meaningful." |
| **PLATEAU-WEAK** | `plateau_delta ≤ 2` AND (`plateau_consumed < 0.85` OR `avg_score < 80` OR `coverage_blocked`) — i.e. we converged, but not to a DEEP state | `LEAVE-DEEP-IDEMPOTENT` (with `weak_phases:<list>` in the row) | "Plateau reached (WEAK) — setup is NOT yet anchored deeply. <reason-specific message; see below>." |
| **NOT-PLATEAU** | `plateau_delta > 2` OR no prior baseline | (none) | (no plateau message — REFINE may climb on next run) |

**Critical**: NEVER emit "Plateau reached" without one of `(DEEP)` or `(WEAK)`. A bare "plateau reached" + score 58 is the misleading-message bug this classifier exists to prevent.

#### Every `PLATEAU-WEAK` carries a `reason` — and the three call for opposite actions

`PLATEAU-WEAK` is not one state. `phase-5.5-quality.md § Exit codes` (and the three worked `## Plateau verdict` reports beside it) wires each reason to a different remediation, and the run-level JSON below carries the field it reads. First match wins, in this order:

| `reason` | Fires when | What the user must do |
|---|---|---|
| `coverage` | `coverage_blocked` — `_extracted-codebase.md` still carries `[SAMPLED]` markers and no human has accepted them | **Raise coverage first**: re-run extraction without `--lightweight`, or raise the per-category sample in `extract-codebase-overview § Step 8`. NOT "go write more code". |
| `signal` | `plateau_consumed < 0.85` — the upstream extraction phases hit their `[REFINE-WEAK]` gates | Grow the codebase / git history, then re-run `--refine`. Enumerate the weak phases (below). |
| `score` | `avg_score < 80` while `plateau_consumed ≥ 0.85` — the substrate WAS consumed and the artifacts still did not anchor | The generators are the problem, not the extraction. Report it as such; do not tell the user to write more code. |

**Why `coverage` is checked first and why it may only demote.** `plateau_consumed = 0.92` measures the fraction of the *extracted signals* that were consumed — never the fraction of the *codebase* they were extracted from. If `## Conventions` rested on 10 of 412 files, 92% of an 8% sample is not exhaustion of the substrate; it is exhaustion of the part that was read, and `PLATEAU-DEEP`'s claim ("the substrate is exhausted, stop refining") is then simply false. So coverage can BLOCK `PLATEAU-DEEP`; it can never raise a score, promote a verdict, or touch an axis. A metric that can only cost you is not worth gaming — once a coverage percentage could promote, the cheapest way to move it is to cite files gratuitously, and the citation-path check catches ghost citations, not padding.

**The demotion is driven by the `[SAMPLED]` markers, not by the raw percentage.** `files_cited` under-counts by construction (a file can be read and cite nothing), so a healthy run can legitimately show 15%; gating on that number produces noisy exit-2 runs and the feature gets switched off. Markers drive behaviour; the percentage informs the human.

**Escape hatch.** Step-8-class sampling fires on almost every non-trivial repo, so an un-escapable rule makes `PLATEAU-DEEP` unreachable and trains users to ignore exit 2. A maintainer who has read `## Coverage` and judged the sample sufficient records `coverage-accepted: <name>@<iso> — <seen>/<present> <unit> reviewed` in `.claude/_setup-quality.md`; `coverage_blocked` then evaluates false and the report prints the acceptance beside the verdict. It is a human statement on the record, never a flag this skill may set for itself, and it is **scoped to the figures it names** — new `seen`/`present` numbers need a new acceptance.

**The full set of plateau-WEAK reasons** the run-level message must enumerate (so the user knows what to grow):

- Phase 2.7 (entities) WEAK → "add more domain models / migrations / Pydantic-or-Zod schemas"
- Phase 2.8 (architecture) WEAK → "add more clearly-bounded modules / cross-cutting middleware"
- Phase 2.9 (flows) WEAK → "trace more endpoints (need ≥5 total)"
- Phase 2.10 (conventions) WEAK → "let conventions emerge across more files (need patterns recurring 5+ times)"
- Phase 2.11 (hot paths) WEAK → "add monitoring config / Datadog dashboard / git churn signal"
- Phase 2.12 (failures) WEAK → "accumulate more git history (need ≥30 commits) OR opt into `--include-incidents=<path>`"

The skill MUST emit ALL relevant reasons — silence on a WEAK axis is the same misleading-message bug.

## Output

Per-artifact JSON (in-memory; aggregated by Phase 5.5 into `_setup-quality.md`):

```json
{
  "artifact": ".claude/rules/database.md",
  "name_density": 22,
  "path_density": 18,
  "signal_density": 25,
  "specificity": 23,
  "total": 88,
  "classification": "DEEP",
  "signals_consumed": ["domain-entity", "hot-path", "n+1-citation", "missing-index"],
  "deductions": [],
  "miscitations": [],
  "delta_from_prior": 46,
  "plateau_idempotent": false
}
```

Run-level JSON (one per `--refine` invocation):

```json
{
  "run_timestamp": "2026-04-28T09:14:00Z",
  "artifact_count": 18,
  "avg_score": 81,
  "avg_score_prior": 47,
  "plateau_delta": 34,
  "plateau_consumed": 0.92,
  "sampled_sections": [],
  "coverage_accepted": null,
  "weak_phases": [],
  "verdict": "NOT-PLATEAU",
  "reason": null,
  "verdict_message": "REFINE climbed +34 points; no plateau yet."
}
```

**`reason` is mandatory whenever `verdict` is `PLATEAU-WEAK`, and `null` otherwise.** Its three values are exactly the three in Step 7's table — `coverage` / `signal` / `score` — and `phase-5.5-quality.md § Exit codes` reads it to choose which remediation to print behind the same exit `2`. Without the field, that phase's three-way branch has nothing to branch on and every WEAK run gets the `signal` message ("grow the codebase"), which is actively wrong advice for the other two: `score` means the generators failed on a substrate that was fine, and `coverage` means read more of the code you already have. A `PLATEAU-WEAK` with `reason: null` is the same defect class as a bare `## Plateau reached` — refuse to emit it (§ Mechanical halt).

Or, on a converged DEEP run:

```json
{
  "verdict": "PLATEAU-DEEP",
  "verdict_message": "Plateau reached (DEEP) — setup is anchored at avg 81/100 with 92% of signal consumed. Further --refine adds nothing meaningful. Stop running --refine until significant new code lands.",
  "weak_phases": []
}
```

Or, on a converged DEEP-scoring run that coverage blocks — note the average is 81, the same as the DEEP example above, and the verdict is still WEAK:

```json
{
  "verdict": "PLATEAU-WEAK",
  "reason": "coverage",
  "avg_score": 81,
  "plateau_consumed": 0.92,
  "sampled_sections": ["## Conventions [SAMPLED: 10/412 files]", "## Architecture [SAMPLED: 8/1204 files]"],
  "coverage_accepted": null,
  "weak_phases": [],
  "verdict_message": "Plateau reached (WEAK, reason: coverage) — scores plateaued at avg 81/100 with signals_consumed = 92%, but round-one extraction cited 214 of 1,204 source files (18%) and 2 sections are still marked [SAMPLED]. signals_consumed measures the extracted signals, not the source they came from, so this is NOT a DEEP plateau. Raise coverage first: re-run extraction without --lightweight, or raise the per-category sample in extract-codebase-overview Step 8. If 10/412 is genuinely enough here, record `coverage-accepted:` in .claude/_setup-quality.md and PLATEAU-DEEP becomes available again."
}
```

`weak_phases` is empty here and that is correct — no deep-extraction phase was weak. This is the case that proves `reason` cannot be derived from `weak_phases`: a consumer inferring the reason from that list would read "no weak phases" and print the DEEP message under a WEAK verdict.

Or, on a converged WEAK run whose upstream extraction was thin:

```json
{
  "verdict": "PLATEAU-WEAK",
  "reason": "signal",
  "verdict_message": "Plateau reached (WEAK, reason: signal) — setup is NOT yet anchored deeply (avg 58/100), but no further refinement is possible. 4 of 6 deep-extraction phases produced WEAK output. Grow upstream signal before re-running --refine.",
  "sampled_sections": [],
  "coverage_accepted": null,
  "weak_phases": ["entities", "flows", "hotpaths", "failures"],
  "weak_phase_actions": {
    "entities": "add more domain models / migrations / schemas",
    "flows": "trace more endpoints (need >=5 total)",
    "hotpaths": "add monitoring config / git churn signal",
    "failures": "accumulate more git history OR --include-incidents=<path>"
  }
}
```

Aggregate goes into `.claude/_setup-quality.md` per the format defined in setup-project.md Phase 5.5.

## Anti-patterns

- **Counting an identifier that's only in the artifact's body, not in the `## Project-specific` block** — only the block counts. Body is generic teaching prose; the block is the project anchor.
- **Counting external lib names as identifiers** — only THIS project's identifiers count. `pandas.DataFrame` is not an anchor; `app/services/billing.py:BillingService` is.
- **Crediting a citation that's a ghost** — if the file doesn't exist, the citation is worse than missing. Deduct.
- **Adding bonus points for length** — verbose blocks are not deeper. Keep the scoring axes pure.
- **Self-fulfilling plateau** — if extraction is WEAK across the board, scores will be capped (signal density 0); reporting "plateau reached" without classifying as PLATEAU-WEAK is misleading. The verdict MUST be one of `PLATEAU-DEEP` / `PLATEAU-WEAK` / `NOT-PLATEAU` — never a bare "plateau reached" string.
- **Single-line plateau verdict in the JSON** — the run-level JSON's `verdict_message` MUST enumerate weak phases when verdict is `PLATEAU-WEAK` for reason `signal`. Silence on a WEAK axis defeats the diagnostic purpose of the verdict.
- **`PLATEAU-WEAK` with no `reason`** — the consumer then has to guess, and every guess defaults to "grow the codebase," which is the wrong instruction for two of the three reasons. Emit the field or do not emit the verdict.
- **Letting coverage raise a score or promote a verdict** — it may only ever demote (Step 7). The moment a coverage figure can help, padding citations becomes the cheapest way to move it, and the path check catches ghosts, not padding.
- **Setting `coverage_accepted` from inside this skill** — the acceptance is a human's statement that they read `## Coverage` and judged the sample sufficient. A tool that can grant itself the exemption has not implemented the rule; it has implemented a warning.
