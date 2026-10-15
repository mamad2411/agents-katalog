---
name: short-form-eval
description: "Closes the feedback loop for short-form video — scores published posts against the original brief and platform-intelligence references inside an existing marketing eval loop. Reads `<loop-slug>` + `<post-url>` + `<brief-path>` + the matching short-form-research catalog, runs a 4-dimension provisional rubric (v0.1, mandatory revision after cycle 2-3), writes a cycle report to `skills-resources/loops/[slug]/evals/[date]-cycle-N.md`, and appends `results.tsv`. Not for pre-publish brief authoring (use short-form-brief in marketing-skills). Not for catalog discovery (use short-form-research). Cycle 1 weights observation 70 / scoring 30 to avoid overfitting on a single calibration pair."
argument-hint: "<loop-slug> <post-url> <brief-path>"
allowed-tools: Read Grep Glob Bash WebFetch Write
license: MIT
metadata:
  author: hungv47
  version: "0.1.0"
  budget: standard
  estimated-cost: "$0.50-1.50"
promptSignals:
  phrases:
    - "score this post"
    - "evaluate the post"
    - "post-publish review"
    - "did the brief work"
    - "short-form eval"
    - "eval cycle"
    - "feedback loop"
  allOf:
    - [eval, post]
    - [score, brief]
  anyOf:
    - "post vs brief"
    - "did it land"
    - "eval cycle"
    - "feedback loop"
    - "post-publish"
  noneOf:
    - "long-form"
    - "blog post"
    - "podcast"
  minScore: 5
routing:
  intent-tags:
    - eval
    - feedback
    - post-publish
    - short-form
  position: feedback-loop
  lifecycle: evaluation
  produces:
    - skills-resources/loops/[slug]/evals/[date]-cycle-N.md
    - skills-resources/loops/[slug]/results.tsv
    - skills-resources/loops/[slug]/learnings.md
  consumes:
    - skills-resources/loops/[slug]/program.md
    - skills-resources/loops/[slug]/context.md
    - skills-resources/loops/[slug]/results.tsv
    - short-form-brief output (the per-asset brief that produced the post)
    - .agents/skill-artifacts/research/short-form-research/[slug].md (platform-intelligence references)
    - published post URL or saved post data
  requires: []
  defers-to:
    - skill: short-form-research
      when: "no platform-intel catalog exists for the topic+market — eval against missing reference is meaningless"
    - skill: short-form-brief
      when: "user wants pre-publish brief authoring, not post-publish scoring"
    - skill: eval-loop
      when: "no existing marketing loop workspace exists for this short-form initiative"
  parallel-with: []
  interactive: false
  estimated-complexity: medium
---

# Short-Form Eval — Orchestrator

*Feedback-loop skill — closes the brief → publish → score → pattern-log loop. The gap-gate consumes its outputs to decide what the stack should learn next.*

**Core Question:** "Did the brief survive contact with the platform — and what's the signal-bearing pattern this cycle adds to the log?"

---

## Critical Gates — Read First

Non-negotiable constraints before dispatching any agent:

1. **Provisional rubric, not locked.** `references/rubric.md` ships at `version: 0.1, status: provisional`. Mandatory revision after cycle 2-3 against real variance. Per-cycle rubric drift is expected — encode the change in the artifact, don't smuggle it into the rubric file silently.
2. **Cycle 1 weighting is 70% observation / 30% scoring.** Single calibration pair would overfit a locked rubric. First cycle leans toward describing what you saw; later cycles harden scoring as variance accumulates.
3. **Both brief and reference catalog must exist.** No platform-intel reference → BLOCKED. No brief → BLOCKED. The eval scores a *fidelity claim* against *known patterns*; missing either side reduces the run to vibes.
4. **No fabricated metrics.** Every engagement number, completion rate, save/share count, and sample-size claim cites the URL or panel screenshot it came from. Critic rubric #1 fails the artifact otherwise.
5. **Pattern-log entries are atomic.** One cycle = one pattern-log entry block in the report. The block has a fixed shape (claim, evidence, refutability, expiry) so future cycles can diff. Free-form prose patterns are unusable downstream.

---

## Philosophy

The eval skill exists to **close** a loop, not to grade. Brief skills produce hypotheses ("this hook archetype will land"); the eval scores the hypothesis against what the platform did with it. The signal that matters is the *delta* between predicted and observed — not the absolute engagement number.

A v0.1 rubric is a hedge against premature lock-in. The panel that scoped this skill (`agents-panel` 2026-05-08) explicitly flagged premature-rubric-lock as the highest residual risk. The mitigation is procedural: revise the rubric after cycle 2-3 against real variance, and ship cycle 1 weighted toward observation. If observation contradicts the rubric, observation wins.

**Refutability > Correctness > Completeness.** A pattern claim that can't be wrong in any future cycle isn't a pattern — it's a tautology. Every pattern-log entry includes an expiry condition (what would refute it).

## Inputs / Output

**Inputs:**
- `<loop-slug>` (required) — existing marketing loop under `skills-resources/loops/[slug]/`
- `<post-url>` (required) — public URL of the published short-form post
- `<brief-path>` (required) — path to the brief artifact that produced the post (typically a short-form-brief output under `.agents/skill-artifacts/mkt/short-form-brief/...`)
- Implicit: matching `short-form-research` catalog entry for the post's topic+market — auto-resolved from brief frontmatter or asked once during Pre-Dispatch
- Optional: prior cycle reports and `results.tsv` rows in `skills-resources/loops/[slug]/` — for trend context

**Output:** `skills-resources/loops/[slug]/evals/[YYYY-MM-DD]-cycle-N.md` — one file per cycle, single platform, single brief — plus a validated `results.tsv` row appended with `scripts/append-loop-result.ts`.

## Quality Gate

Critic agent verifies before delivery (all four binary PASS required, max 2 rewrite cycles):

- [ ] Every metric and observation has a source URL or panel/screenshot citation
- [ ] All four rubric dimensions scored against the v0.1 rubric in `references/rubric.md`; each score has a one-sentence falsifiable justification
- [ ] At least one pattern-log entry exists in the canonical block shape (claim / evidence / refutability / expiry)
- [ ] Cycle 1 weighting note (70 obs / 30 score) is honored — the report's prose-to-score ratio is observation-heavy on cycle 1

## Chain Position

Previous: `short-form-brief` (marketing-skills, the brief whose post is being scored) and `short-form-research` (the catalog whose patterns are the reference)
Next: pattern-log entries are read by future `short-form-research` re-runs and (eventually) by gap-gate analysis.

**Re-run triggers:**
- New post published from the same brief tier — run a fresh cycle
- Cycle 2-3 boundary — operator runs the rubric revision pass (v0.1 → v0.2)
- Catalog refresh in `short-form-research` — re-score prior cycles against the new reference (optional)

### Skill Deference
- No platform-intel catalog exists → `short-form-research` first (BLOCKED if missing)
- Pre-publish brief authoring → `short-form-brief` (different job, marketing-skills)
- Multi-post campaign rollup → out of scope for v0.1; one post per cycle

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Hook Strength Agent | 1 (parallel) | `agents/hook-strength-agent.md` | Compares observed opening 1-3s of the post against the platform-intel hook archetypes for the matching topic+market — surfaces match, mismatch, or novel archetype |
| Eval Runner Agent | 1 (parallel) | `agents/eval-runner-agent.md` | Per-rubric-dimension scorer — applies the v0.1 rubric in `references/rubric.md`, produces per-dimension scores 0-3 with falsifiable justifications and the cycle-1 70/30 weighting |
| Pattern Extractor Agent | 2 (sequential) | `agents/pattern-extractor-agent.md` | Drafts the canonical pattern-log entry — claim, evidence, refutability condition, expiry — from the upstream agent outputs |
| Critic Agent | 2 (final) | `agents/critic-agent.md` | Four-rubric quality gate — citation discipline, score justification falsifiability, pattern-block shape, cycle-1 weighting honored. Routes rewrites; max 2 cycles |

---

## Routing Logic

Single route. The skill always runs the full Layer 1 + Layer 2 sequence — there is no "Quick" route because skipping the hook check or the rubric pass produces a hollow report.

```
1. Pre-dispatch (warm-start scan + cold-start probe if reference catalog isn't resolvable)
2. LAYER 1 IN PARALLEL: hook-strength-agent, eval-runner-agent
3. LAYER 2 SEQUENTIAL:
   - pattern-extractor-agent (consumes both Layer 1 outputs)
   - critic-agent (4-rubric gate; FAIL → re-dispatch named agent with feedback)
4. Critic FAIL → re-dispatch named agent(s) (max 2 cycles); after cycle 2, ship done_with_concerns
5. Write artifact to `skills-resources/loops/[slug]/evals/[date]-cycle-N.md`, append `results.tsv` with `append-loop-result.ts`, then call manifest-sync
```

---

## Pre-Dispatch

Run the canonical Pre-Dispatch protocol (`references/_shared/pre-dispatch-protocol.md`).

**Needed dimensions:** loop slug (positional arg), post URL (positional arg), brief path (positional arg), platform-intel catalog (auto-resolve from brief frontmatter), cycle index (auto-increment from loop `results.tsv`).

**Read order:**
1. `skills-resources/loops/[loop-slug]/program.md`, `context.md`, and `results.tsv` — confirm the loop exists and find the next cycle.
2. `<brief-path>` — confirm it exists, parse frontmatter for topic, market, target platform, hook archetype claim.
3. `.agents/skill-artifacts/research/short-form-research/[slug].md` — locate the matching catalog by topic+market; if multiple match, ask user once.
4. `.agents/manifest.json` — confirm catalog freshness (warn if stale).
5. `.agents/experience/content.md` — most recent entries for market and audience register.

**Warm Start** (brief, post URL, and matching catalog all resolvable):

```
Found:
- brief: [path] (topic="[topic]", market="[market]", platform=[platform])
- loop: skills-resources/loops/[slug]/
- catalog: .agents/skill-artifacts/research/short-form-research/[slug].md (last refreshed [date])
- prior cycles in results.tsv: N → this is cycle N+1
- post URL: [url]

Cycle 1 reminder: 70% observation / 30% scoring. Rubric is provisional v0.1.

Proceed with eval, or override?
```

**Cold Start** (catalog cannot be auto-resolved):

```
Short-form eval needs three things to score a post against a known reference. Two are in the args; one is missing.

1. Existing marketing loop slug for this short-form initiative:
   [free text — create one first with eval-loop if none exists]

2. Topic of this post (one phrase — to match a short-form-research catalog):
   [free text]

3. Target market the post was aimed at:
   (a) Vietnam   (b) US/global English   (c) SEA   (d) Other: ___

4. Platform of this post:
   (a) TikTok   (b) Reels   (c) Shorts   (d) X video   (e) LinkedIn video

Answer 1-4 in one response. I'll resolve the loop, catalog, and dispatch.
```

**Write-back to `.agents/experience/content.md`:**

| Q | Key |
|---|---|
| 1. Topic | `Content — short-form eval topic` (most recent) |
| 2. Market | `Content — primary market` (only if not already present) |
| 3. Platform | `Content — short-form eval platform` |

If no catalog matches after the cold-start answer, return **BLOCKED** with the recommendation: "Run `short-form-research` for `[topic]` / `[market]` first; eval against missing reference is meaningless."

---

## Dispatch Protocol

### How to spawn a sub-agent

For each agent dispatched, use the **Agent tool** with a prompt built as follows:

1. **Read** the agent instruction file — include FULL content in the Agent prompt
2. **Append** brief, post-URL fetched content, and the matched catalog excerpt as context
3. **Resolve paths to absolute**: replace relative reference paths with absolute paths rooted at this skill's directory
4. **Pass references by excerpt**: orchestrator reads `references/rubric.md` once and includes the relevant dimension's body in eval-runner-agent's context — sub-agents do not re-read
5. If **feedback** exists (critic FAIL cycle), append at end with header "## Critic Feedback — Address Every Point"

### Single-agent fallback

If multi-agent dispatch is unavailable, execute each agent's instructions sequentially in-context. Output quality is equivalent — multi-agent pattern optimizes parallelism, not capability.

---

## Layer 1: Parallel Hook Check + Rubric Run

Spawn **IN PARALLEL** (multiple Agent tool calls in one message).

| Agent | Instruction File | Pass These Inputs | Reference Files to Resolve |
|-------|-----------------|-------------------|---------------------------|
| Hook Strength Agent | `agents/hook-strength-agent.md` | `{ post_url, brief_excerpt, catalog_hook_archetypes }` | `references/rubric.md` (dimension: hook-strength-vs-platform-intel) |
| Eval Runner Agent | `agents/eval-runner-agent.md` | `{ post_url, brief, catalog_excerpt, cycle_index }` | `references/rubric.md` (full) |

---

## Layer 2: Sequential Pattern + Critic

Run sequentially. Each agent receives all upstream outputs.

| Agent | Instruction File | Inputs | Reference Files |
|-------|-----------------|--------|-----------------|
| Pattern Extractor | `agents/pattern-extractor-agent.md` | All Layer 1 outputs | `references/rubric.md` (dimension: pattern-log-entry-shape) |
| Critic Agent | `agents/critic-agent.md` | Pattern Extractor output + raw Layer 1 outputs | `references/rubric.md` |

---

## Critic Routing

Critic returns one of:

- **PASS** → write artifact as `done`
- **FAIL with named sections** → re-dispatch the source agent(s) with feedback. Common routes:
  - Citation FAIL → back to eval-runner or hook-strength (capture missing URL/screenshot reference)
  - Score-justification FAIL → eval-runner (rewrite justification to be falsifiable)
  - Pattern-block-shape FAIL → pattern-extractor (re-author with claim/evidence/refutability/expiry shape)
  - Cycle-1-weighting FAIL → eval-runner + pattern-extractor (rebalance prose vs score)

**Loop cap:** 2 cycles. After cycle 2, ship `done_with_concerns` with failed rubrics pinned at top of artifact.

---

## Output Artifact Structure

`skills-resources/loops/[slug]/evals/[YYYY-MM-DD]-cycle-N.md`:

```yaml
---
type: short-form-eval
status: done | done_with_concerns | blocked | needs_context
date: [YYYY-MM-DD]
cycle: [N]
loop: [slug]
post_url: [url]
brief_path: [path]
catalog_path: [path]
catalog_freshness: fresh | warn | stale
topic: [from brief]
market: [from brief]
platform: [tiktok | reels | shorts | x | linkedin]
rubric_version: "0.1"
rubric_status: provisional
weighting: cycle-1-70-obs-30-score | cycle-2-plus-balanced
scores:
  brief-fidelity: [0-3]
  hook-strength-vs-platform-intel: [0-3]
  pattern-log-entry-shape: [0-3]
  platform-signal-freshness-flag: [0-3]
  author-discretion: [0-3]
---
```

**Body sections (in order):**

1. TL;DR — one paragraph: did the brief land, what shifted, what's the pattern-log entry
2. Observation — what the post actually did on the platform (engagement mix, opening 1-3s, caption, CTA placement, audio choice). Cycle 1: this section is the longest.
3. Brief vs Observed — side-by-side: what the brief claimed, what the platform did. Each row cites both sides.
4. Rubric Scores (v0.1, provisional) — per dimension, score + falsifiable justification. Author-discretion at lower weight.
5. Pattern-Log Entry — exactly one block in the canonical shape:
   ```
   ### Pattern: [name]
   **Claim:** [what this cycle suggests is true]
   **Evidence:** [URLs, metrics, citations]
   **Refutability:** [what would prove this wrong]
   **Expiry:** [conditions or timeframe after which this claim should be re-tested]
   ```
6. Open Risks & Caveats — including premature-rubric-lock risk if applicable
7. Recommendations for next cycle / catalog — does the catalog need a refresh, does the rubric need a revision now (mandatory at cycle 2-3), did a new archetype emerge

---

## Completion Status

Skill returns one of:

- **DONE** — all 4 critic rubrics PASS within ≤2 cycles. Pattern-log entry exists in canonical shape. Cycle-1 weighting honored where applicable.
- **DONE_WITH_CONCERNS** — critic loop cap reached; remaining failures are surfaceable as warnings (e.g., rubric dimension borderline, partial citation gap). Concerns pinned at top of artifact. Also returned when this is cycle 2 or 3 and the rubric has not been revised yet — flag the mandatory revision in the report.
- **BLOCKED** — post URL unfetchable, brief path doesn't exist, catalog cannot be resolved. State what's needed.
- **NEEDS_CONTEXT** — cold-start abandoned, or matching catalog truly missing for the post's topic+market. Defer to `short-form-research`.

---

## Format Conventions

- All dates ISO 8601 (`YYYY-MM-DD`).
- All URLs preserve query parameters (don't strip `?si=` or platform tracking).
- All numerical claims inline-cite source: `"saves/likes ratio 0.34 ([post panel screenshot 2026-05-09 09:14, archived at <path>](path))"`.
- Rubric scores always declared as `[score]/3 — [one-sentence falsifiable justification]`.
- Pattern-log entries always in the canonical 4-line shape; no free-form prose patterns.
- Cycle index always declared in frontmatter and filename.

---

## Anti-Patterns

- **Locking the rubric.** v0.1 stays provisional. Mandatory revision after cycle 2-3. Don't pre-emptively edit `references/rubric.md` to fix what looks wrong on cycle 1 — record the friction in the cycle artifact, revise deliberately at the cycle 2-3 boundary.
- **Treating cycle 1 like a graded test.** 70/30 weighting exists because a single calibration pair overfits. Long observation, short scoring. The score is provisional context, not a verdict.
- **Fabricated metrics.** No "approximately 12% completion" without a panel/screenshot citation. Critic rubric #1 fails the artifact.
- **Free-form pattern claims.** Pattern-log entries must use the claim / evidence / refutability / expiry shape. Anything else is unusable downstream by gap-gate or by future short-form-research re-runs.
- **Multi-post in one cycle.** v0.1 scope is one post per cycle. Multi-post rollup is parked for a later version.
- **Skipping refutability.** A pattern that can't be falsified in any future cycle is a tautology. Force the refutability line.
- **Auto-running cycles back-to-back.** Each cycle is operator-gated. The skill scaffolds and reports; it does not loop.

## Output

- **Artifact:** `skills-resources/loops/[slug]/evals/[YYYY-MM-DD]-cycle-N.md` (single file per cycle).
- **Side effects:** append `skills-resources/loops/[slug]/results.tsv` with `append-loop-result.ts`, then call `bun scripts/manifest-sync.ts` after artifact write so `.agents/manifest.json` indexes the new cycle.
