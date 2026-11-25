---
name: evolve-skill
description: "Evolve Skill: measurement-first skill optimizer. Evaluates SKILL.md files against an anchored 9-dimension rubric, validates that the rubric itself is stable (test-retest), optimizes with a hill-climbing loop that only accepts improvements larger than measurement noise, protects against overfitting with train/holdout prompt splits, and preserves original function via semantic diff checks. Use when user mentions: optimize skill, skill review, skill audit, improve SKILL.md, skill score, skill rubric, skill quality, make my skill better, rate my skills, evolve skills, skill hill climbing, automated skill improvement."
category: agent-evaluation
domain: agent-evaluation
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "taneltaluri/evolve-skill"
  commit: "8d24739a45"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# Evolve Skill

> A measurement-first skill optimizer. Inspired by Karpathy's `autoresearch` and the `darwin-skill` project, but rebuilt around one conviction: **if you cannot trust your measurement, you cannot trust your optimization.**
>
> Every decision this skill makes is gated by whether the measurement is reliable enough to justify it.

---

## What This Skill Is Not

This is not a formatting linter. This is not a prompt rewriter. This is not an autonomous agent that will rewrite your skills in the background.

This is a **disciplined experiment loop** with strict gates around scoring noise, overfitting, and function drift — the three failure modes that make most "auto-optimize" tools produce worse skills over time.

If you want a quick skill tidy-up, use a simpler tool. If you have 20+ skills and need to know which ones are actually improving, this is for you.

---

## Core Philosophy — The Three Gates

Every optimization cycle passes through three gates. If any gate fails, the cycle stops or rolls back.

### Gate 1 — Measurement Stability (can we trust the score?)

Before any optimization runs, score the baseline skill **three independent times** using three separate sub-agents. Compute the standard deviation. If `SD > 2.0 points`, the rubric is too loose and no optimization may proceed until the rubric is tightened.

A ratchet mechanism with unreliable measurement is not a ratchet — it is a random walk pretending to be progress.

### Gate 2 — Effect Size (is this improvement real?)

A keep decision requires `Δscore ≥ max(3, 2×SD)` where SD is the measurement noise from Gate 1. A skill that "improved" by 1.5 points when noise is ±2 points did not improve.

### Gate 3 — Function Preservation (is it still the same skill?)

Before and after every change, extract the skill's core functions as a bullet list (via a sub-agent). If function overlap drops below 80%, the change is rejected regardless of score. A higher-scoring skill that silently lost a capability is worse, not better.

---

## The 9-Dimension Anchored Rubric (100 points)

Each dimension is scored 1–10. Every dimension has three anchor points (1, 5, 10) defined in `rubric/anchored-rubric.md`. Scorers must reference the anchors and cite which anchor their score lies closest to. This is what stabilizes inter-rater agreement.

**Structure (50 points)**

| # | Dimension | Weight | What it measures |
|---|-----------|--------|------------------|
| 1 | Frontmatter quality | 8 | name format, description ≤1024 chars, triggers |
| 2 | Workflow clarity | 12 | numbered steps, I/O per step |
| 3 | Edge-case coverage | 8 | fallbacks, error recovery |
| 4 | Checkpoint design | 6 | human-in-loop gates before destructive actions |
| 5 | Instruction specificity | 12 | concrete params, formats, examples |
| 6 | Resource integration | 4 | references/scripts/assets resolve |

**Effectiveness (40 points)**

| # | Dimension | Weight | What it measures |
|---|-----------|--------|------------------|
| 7 | Architectural fit | 10 | non-redundant, matches ecosystem conventions |
| 8 | Live test performance | 30 | output quality on held-out test prompts |

**Localization (10 points)**

| # | Dimension | Weight | What it measures |
|---|-----------|--------|------------------|
| 9 | Localization quality | 10 | triggers + examples in all declared languages, cross-platform paths |

**Total:** `Σ(dimension_score × weight) / 10`, capped at 100.

**The effectiveness dimension (30 points) is the largest single weight** by design. A beautifully written skill that produces bad output is still a bad skill.

---

## Workflow

### Phase 0 — Scope and Setup

1. Determine scope:
   - `optimize all skills` → scan `.claude/skills/*/SKILL.md` and skill directories
   - `optimize <name>` → single skill
   - `evaluate only` → Phases 0–2 only, no edits
2. Create a dated branch: `evolve/YYYYMMDD-HHMM`
3. Initialize `results.tsv` and `playbook.md` if they do not exist
4. Read existing `playbook.md` — known patterns will be tried first in Phase 3

### Phase 1 — Test Prompt Design (Train / Holdout Split)

For each skill, the user — not the agent — writes prompts. The agent may suggest, but suggestions must be confirmed.

1. **Training prompts (3)** — seen during optimization, used to drive keep/revert decisions
   - One happy-path prompt
   - One complex or ambiguous prompt
   - One edge-case prompt
2. **Holdout prompts (2)** — never seen during optimization, used only for final validation
   - Cover different scenarios than the training prompts
3. Save to `<skill_dir>/test-prompts.json` using the template in `templates/test-prompts.template.json`
4. Show both sets to the user. Confirm before proceeding.

**Why both sets exist:** without holdouts, the optimization overfits to the training prompts and appears to improve while quietly getting worse on unseen inputs.

### Phase 2 — Baseline Evaluation with Stability Check

For each skill:

1. **Score three times independently** using three separate sub-agents with no shared context
2. Compute mean and SD across the three runs
3. If `SD > 2.0 points`:
   - Flag the skill as `calibration_required`
   - Skip optimization for this skill
   - Report to user: "Rubric is too loose for this skill. Tighten anchors before proceeding."
4. If `SD ≤ 2.0`:
   - Store `baseline_score = mean`, `baseline_sd = sd`
   - Proceed to Phase 3

For the live-test dimension (30 points): run each training prompt through two sub-agents — one with the skill loaded, one without (baseline). Compare output quality against the anchors in the rubric.

If sub-agents are unavailable, set `confidence=low` and **do not** use the score for keep/revert decisions. A low-confidence score is diagnostic only.

### Phase 3 — Optimization Loop

Budget allocation follows a multi-armed bandit pattern, not round-robin:

```
initial_budget_per_skill = 3 rounds
total_budget = 30 rounds across 10 skills (configurable)

round allocation:
  if last round Δ ≥ 5 points:      +2 bonus rounds
  if last round Δ between 0 and 3:  continue at baseline allocation
  if last round Δ ≤ 0 (reverted):   forfeit remaining budget, move on
  hot skills (3+ consecutive keeps) can use up to 10 rounds total
```

Each round:

```
1. Consult playbook.md:
   "Has a known pattern worked for a skill like this before?"
   If yes, try the known pattern first.

2. If no known pattern, diagnose:
   Find the lowest-scoring dimension.

3. Generate exactly one targeted change:
   - Which lines change
   - Which rubric dimension this targets
   - Predicted Δ score

4. Execute on an experiment branch:
   git checkout -b evolve/YYYYMMDD-HHMM/<skill>/exp-<N>
   edit SKILL.md
   git commit -m "exp: <skill> <dimension> <summary>"

5. Re-score with an INDEPENDENT sub-agent (never the editing agent):
   - Run training prompts only (holdout stays sealed)
   - Compute new_score and run Gate 3 (function preservation)

6. Apply gates:
   Gate 2: if new_score > old_score + max(3, 2×SD) → candidate keep
   Gate 3: if function_overlap ≥ 80% → candidate keep
   Otherwise → branch stays for history, move on

7. On candidate keep:
   git checkout main_branch
   git merge --no-ff evolve/.../exp-<N>
   update results.tsv with status=keep

8. On reject:
   leave the experiment branch in place (do not delete — it is training data)
   update results.tsv with status=reject and reason code

9. Log to results.tsv with every column filled
```

After a skill's budget is exhausted, insert a **human checkpoint**:
- Show diff across all kept experiments
- Show training-prompt output comparison
- Show delta summary
- Wait for explicit user approval

### Phase 4 — Holdout Validation (Overfitting Check)

This runs once per skill, after Phase 3 completes and the user has approved.

1. Run the **holdout prompts** (which have never been seen during optimization) against both the original and optimized versions
2. Score only the live-test dimension (30 points)
3. If `holdout_delta < 0`:
   - The optimization overfit to the training prompts
   - Roll back the entire optimization for this skill
   - Log as `overfit_detected` in results.tsv
4. If `holdout_delta ≥ 0`:
   - Optimization is validated
   - Write any discovered patterns into `playbook.md`

### Phase 5 — Playbook Update and Reporting

For every keep that produced `Δ ≥ 5 points`, add an entry to `playbook.md`:

```markdown
## Pattern: <short name>
- **Problem signature:** <what triggers this pattern's applicability>
- **Intervention:** <the specific edit>
- **Measured impact:** <skill, Δ, n observations>
- **Where it worked:** <skill names>
- **Where it failed:** <skill names, if any>
```

Phase 3 of future runs will check this playbook before diagnosing fresh.

Final report includes:
- Per-skill before/after with confidence intervals
- Holdout validation results
- Playbook additions
- Branches with failed experiments (for later review)

---

## Constraints

1. **Core function is immutable.** Gate 3 enforces this. If a change removes a capability, it is rejected even if the score went up.
2. **No new dependencies.** Do not add scripts, references, or external tools the original skill did not declare.
3. **One dimension per experiment.** Multi-dimension changes make keep/revert decisions unattributable.
4. **Size ceiling.** Optimized SKILL.md must be ≤150% of original size.
5. **Git-first, rollback-safe.** Every change is on a branch. `git revert` is for merge commits only; failed branches are preserved.
6. **Score independence.** The sub-agent that edits is never the sub-agent that scores. Enforced by session separation.
7. **Confidence gating.** A `confidence=low` score cannot drive a keep decision under any circumstances.
8. **Localization is a dimension, not an afterthought.** If a skill declares bilingual support, both languages are tested.

---

## File Layout

```
.claude/skills/evolve-skill/
├── SKILL.md                           # This file
├── rubric/
│   ├── anchored-rubric.md             # Human-readable anchors
│   └── rubric-v1.json                 # Machine-readable rubric
├── scripts/
│   ├── calibrate.py                   # Test-retest variance
│   ├── score.py                       # Apply rubric with anchors
│   ├── semantic_diff.py               # Function preservation
│   ├── ratchet.py                     # Keep/revert with CI
│   └── allocate.py                    # Bandit budget allocation
├── templates/
│   ├── test-prompts.template.json     # Train/holdout structure
│   ├── result-card.html               # Optional visual card
│   └── playbook.template.md           # Starter playbook
├── examples/
│   ├── example-walkthrough.md         # Full optimization run
│   └── example-results.tsv            # Real log format
└── results.tsv                        # Created on first run
```

Per-skill files created during optimization:

```
<target_skill>/
├── SKILL.md
├── test-prompts.json                  # Train + holdout split
├── baseline-scores.json               # Three-run variance record
└── optimization-log.md                # Per-skill narrative
```

---

## results.tsv Schema

Tab-separated, append-only. Every row is an event.

```
timestamp  branch  skill  old_score  new_score  delta  sd  status  dimension  intervention  function_overlap  holdout_delta  confidence  eval_mode  notes
```

Column definitions:

- `status` ∈ {`baseline`, `keep`, `reject_effect_size`, `reject_function_drift`, `reject_noisy`, `overfit_detected`}
- `confidence` ∈ {`high`, `medium`, `low`} — derived from `eval_mode`
- `eval_mode` ∈ {`full_test` (sub-agents with live prompts), `partial` (structure only), `simulation` (no sub-agent available)}
- `function_overlap` — semantic-diff overlap percentage from Gate 3
- `holdout_delta` — only populated on Phase 4 rows

---

## Intervention Playbook (Priority Order)

When diagnosing the lowest-scoring dimension, consult this ranked list of proven interventions.

### P0 — Effectiveness Problems (Live-Test Signals)

- Output misses user intent → search SKILL.md for misleading instructions, prune
- `with_skill` output worse than `baseline` → skill is over-constraining, simplify
- Output format inconsistent → add explicit output schema with example

### P1 — Structural Problems

- Frontmatter trigger list too narrow → expand with synonyms and natural phrasings in all declared languages
- Workflow lacks Phase/Step structure → impose linear numbered flow
- No human checkpoint before destructive actions → insert confirmation gate

### P2 — Specificity Problems

- Vague steps ("process the image") → replace with specific operation + parameters
- Missing I/O specs → add format, path, and example for each step
- No error handling → add "if X fails, then Y" branches

### P3 — Readability Problems

- Paragraphs too long → break into tables or shorter blocks
- Repeated descriptions → deduplicate
- No quick reference → add TL;DR or decision tree

Every P0 or P1 intervention that produces `Δ ≥ 5 points` must be added to `playbook.md` with a pattern signature.

---

## Usage Patterns

### Full audit + optimization (first run)
```
User: "optimize all my skills"
→ Phases 0–5
→ Agent suggests starting with 5 lowest baseline scores
```

### Single skill
```
User: "optimize my blog-writer skill"
→ Phases 0–5 limited to one skill
```

### Evaluation only (no edits)
```
User: "rate all my skills"
→ Phases 0–2 only
→ Report includes confidence level per skill
```

### Calibration check
```
User: "is my rubric reliable?"
→ Phase 2 three-run variance only
→ Reports SD per skill
→ Flags which skills cannot be optimized under current rubric
```

### Playbook review
```
User: "what patterns work for my skills?"
→ Display playbook.md with frequency and average Δ per pattern
```

### Rollback
```
User: "revert optimization for <skill>"
→ git checkout main_branch
→ git revert <merge_commit>
→ Restore from pre-evolution tag
```

---

## What Makes This Different from Darwin / autoresearch

| Concern | autoresearch | darwin-skill | evolve-skill |
|---------|-------------|--------------|--------------|
| Measurement noise | Tolerable (loss is tight) | Unmeasured | **Gate 1 requires SD ≤ 2.0** |
| Overfitting | Natural (val set) | Unprotected | **Train/holdout split, Phase 4 validation** |
| Function drift | Not a concern (code) | Addressed by rule, not measurement | **Gate 3 semantic diff, 80% overlap minimum** |
| Rubric stability | N/A | "Score 1–10" | **Anchored 1/5/10 points per dimension** |
| Keep threshold | `new_loss < old_loss` | `new > old` | `Δ ≥ max(3, 2×SD)` |
| Budget allocation | Compute-bound | Fixed 3 rounds | Multi-armed bandit |
| Failed experiments | Discarded | `git revert` creates noise | **Preserved on branches** |
| Learning across skills | N/A | None | **Playbook crosstalk** |
| Human oversight | None | Per-skill pause | Per-skill pause + holdout gate |

---

## Success Criteria for This Skill Itself

This skill is working correctly if, over a full optimization run:

- Fewer than 20% of candidate changes are rejected by Gate 2 (effect-size too small) → anchors are useful
- Fewer than 5% of candidate changes are rejected by Gate 3 (function drift) → the editor is disciplined
- Holdout delta agrees with training delta direction ≥ 90% of the time → no significant overfitting
- Playbook patterns reused in later runs have positive expected delta → crosstalk works

These are meta-metrics — tracked in `results.tsv` over time — that tell you whether the optimizer itself is healthy.

---

## Design Inspiration

- **Karpathy, autoresearch** — autonomous experiment loops driven by a measurable objective
- **darwin-skill (alchaincyf)** — applying the autoresearch pattern to SKILL.md optimization
- **Inter-rater agreement research** — why anchored rubrics reduce scorer variance
- **Train/validation/test discipline from ML** — why holdouts matter

The contribution of this skill is not novelty. It is **measurement discipline**: the loss function (rubric) is treated as a first-class object that itself must be validated, not assumed.

---

## License

MIT. Use, fork, modify, ship. Attribution appreciated but not required.
