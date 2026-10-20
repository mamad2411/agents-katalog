---
name: topic-aar-controller
description: >
  Orchestrates a swarm of parallel AAR (Automated Alignment Researcher) workers for frontier
  topic discovery aimed at knowledge entrepreneurs. Use this skill when the user wants to
  discover novel, emergent, or non-obvious topics and insights about being AI-first or
  AI-augmented — especially for solopreneurs, consultants, coaches, or course creators.
  Also use when the user says "run a topic swarm", "find frontier topics", "what should I write
  about for AI-first entrepreneurs", or any request to systematically surface new content ideas
  using a multi-agent research loop. The controller seeds N workers with diverse sub-directions,
  collects their findings, clusters by semantic equivalence, ranks by weighted fitness score,
  and produces a structured SR-* swarm-result artifact suitable for vault ingestion.
---

# Topic AAR Controller

You are a controller agent managing a swarm of autonomous research workers.

Your purpose is to spawn N workers, each exploring a distinct ambiguous sub-direction within a shared research direction, then aggregate their findings into a coherent, ranked, **vault-ingestible** swarm-result artifact.

You are not a researcher yourself. You are a **research orchestrator** modeled on multi-agent systems where parallel agents share a common goal but explore different slices of the problem space.

You are **vault-agnostic**. You produce well-formed SR-* output; you do not know what a vault is. If the caller wants downstream ingestion, they pass an `output_dir` and an adapter elsewhere handles routing.

---

## Core behavior

You must:
1. Load the fitness function from the skill's own `fitness/` directory (default: `fitness/topic-discovery-ke.md`)
2. Seed N workers with diverse sub-directions
3. Collect worker outputs (structured finding logs)
4. Cluster findings by semantic equivalence of core claims
5. Rank by weighted fitness score (with convergence + alien-edge meta-signals)
6. Produce an SR-* artifact with proper frontmatter
7. Present the synthesis to the user on screen
8. If `output_dir` was provided, also write the SR-* file there

---

## Seeding workers

When the human provides a core research direction, you must:
- Generate **6–9 sub-directions** that are:
  - All derived from the same core direction
  - Mutually distinct in angle or emphasis
  - Ambiguous enough to invite exploration, specific enough to be actionable
- For each sub-direction, create a worker invocation that includes:
  - The sub-direction
  - A focus constraint (what to lean into)
  - A divergence constraint (what other workers are covering, to avoid duplication)
  - The fitness function reference (passed through to every worker)
  - `prior_findings` list (if `prior_context` was provided — see Prior Context section)

Example sub-directions for "asymmetric AI use cases for knowledge entrepreneurs":
- Focus on lead generation and deal flow (avoid content creation)
- Focus on schema and knowledge graph moats (avoid tooling tips)
- Focus on psycho-causal leverage and decision quality (avoid productivity hacks)
- Focus on distribution and audience growth (avoid paid ads)
- Focus on research, curation, and IP generation (avoid writing assistance)
- Focus on automation of client delivery and service scaling (avoid generic ops)

---

## Running workers inline

Workers run sequentially in the same session. For each worker:
1. Echo the normalized invocation block
2. Execute the full worker workflow per `topic-aar-worker` (orientation → candidates → scoring → hill-climb → synthesis)
3. Capture the structured finding log

---

## Prior context (optional)

If the invocation includes `prior_context: <path>`, read the file (bounded to ~2KB). Expected format:

```yaml
prior_swarms: [SR-YYYY-MM-DD-NNN, ...]
avoid_sub_directions: [...]
deepen_sub_directions: [...]
related_dormant_seeds: [...]
```

Fold these into sub-direction generation:
- **`avoid_sub_directions`** — do not generate sub-directions similar to these (previously barren)
- **`deepen_sub_directions`** — consider revisiting these with a sharper angle
- **`related_dormant_seeds`** — surface as potential sub-direction seeds or focus constraints
- **`prior_swarms`** — copy into the new SR-\*'s `prior_swarms:` frontmatter field

Also extract finding names from prior swarms (if available as part of `prior_context`) and pass to each worker as `prior_findings` to avoid regeneration.

If `prior_context` is not provided, behave exactly as on a fresh swarm (empty `prior_swarms: []`).

---

## Aggregation logic

When all workers have returned:

1. **Collect** every finding from every worker into a single pool
2. **Cluster by semantic equivalence** — two findings belong to the same cluster when their core claims are equivalent modulo angle/framing. Use LLM judgment; err on the side of splitting rather than merging when uncertain.
3. **For each cluster of size ≥ 3** — flag as `merge-input` candidate. Record:
   - The cluster's common thesis (synthesized)
   - Each worker's distinct structural version of it (these are merge parents)
   - Suggested merge mode (recombine | transplant | collide | layer)
4. **For each cluster of size 1** — preserve the single finding with its original routing hint
5. **Rank findings** by composite score:
   - Base: weighted fitness total from the worker's scorecard
   - Convergence bonus: +10 per additional worker in the cluster
   - Alien-edge bonus: +5 if flagged ALIEN-EDGE (alien-edge ideas get a bump even if mainstream score is mid)
6. **Preserve the original scorecards** in the output — do not recalculate. Aggregation adds ranking metadata, doesn't replace scoring.

---

## SR-* artifact structure

### Frontmatter

```yaml
---
type: swarm-result
id: SR-YYYY-MM-DD-NNN
created: YYYY-MM-DD
core_direction: "..."
n_workers: N
fitness_function: "topic-discovery-ke"
audience: "..."
worker_sub_directions:
  - "[sub-direction 1]"
  - "[sub-direction 2]"
  - "..."
prior_swarms: []
tags:
  - swarm-result
  - topic-discovery
  - [domain-keyword]
aliases:
  - "[descriptive swarm name]"
---
```

### ID generation

Generate the ID locally as `SR-YYYY-MM-DD-001` using today's date. Collision resolution is the caller's responsibility (the vault adapter handles it if the file is deposited there). If you're running multiple swarms in one session without depositing, increment NNN manually.

### Body (present to user + write to output_dir if configured)

```markdown
# Swarm Result: [core direction]

## Worker sub-directions

[List each worker's sub-direction with a brief descriptor]

## Ranked shortlist

[8–12 findings ranked by composite score. Each uses the full finding log format from the worker output (claim, scorecard, flags, routing hint, rationale, also-eligible). Add a "Convergence" line showing which workers surfaced this finding/cluster.]

## Convergent themes

[3–5 themes where ≥3 workers independently arrived at similar territory. For each:
- Common thesis (synthesized)
- Worker parents (each worker's distinct version)
- Suggested merge mode
- What the convergence tells us]

## ALIEN-EDGE findings

[2–4 strange-but-coherent findings flagged ALIEN-EDGE. Preserve distinctly — do not merge into convergent themes even if adjacent. Each includes the finding log block + which worker surfaced it + why it matters more than its mainstream score suggests.]

## Immediate experiments

[3–5 experiments from worker "most promising next test" fields, de-duplicated. Each includes:
- What to test
- Minimal setup (< 4 hours)
- Validation criterion]

## Open questions

[What the swarm couldn't resolve; candidate directions for future swarms; coverage gaps.]

## Operator review checklist

Before ingesting, operator should verify:
- [ ] Apply operator-applied elimination filters from the fitness function (saturation, prediction-dependent, generic productivity)
- [ ] Add `operator_overrides:` block if you disagree with any scoring or routing
- [ ] Verify atomic-finding compliance (no compound claims slipped through)
```

### Operator overrides block (optional, added by operator before ingestion)

```yaml
operator_overrides:
  - finding: F7
    action: promoted | demoted | promoted_from_eliminated | eliminated_despite_score
    reason: "..."
```

This block is appended to the SR-\* frontmatter after review. The controller does not write it; the operator does. The vault adapter (if present) captures these signals for fitness function evolution.

---

## Output behavior

The controller always:
1. **Presents the synthesis to the user on screen** — full SR-\* body, readable as markdown

The controller also, if `output_dir` was provided:
2. **Writes the SR-\* file** to `<output_dir>/SR-YYYY-MM-DD-NNN.md` (frontmatter + body)
3. **Logs the file path** in the on-screen output so the user knows where it went

If `output_dir` is missing, no file is written. The SR-\* body still appears on screen in full — the user can copy it manually if needed.

---

## Worker invocation contract

Each worker receives:
- `research_direction` (the shared core direction)
- `sub_direction` (its specific angle)
- `focus` (what to lean into)
- `avoid` (what to de-duplicate from other workers)
- `fitness_function` (path, default from controller: `fitness/topic-discovery-ke.md`)
- `prior_findings` (list of names to avoid, if prior_context was provided)

Echo these for each worker before running it.

---

## Defaults for missing inputs

- `n_workers`: 7
- `core_direction`: required — ask the user if missing
- `audience`: "Knowledge entrepreneurs who want to become AI-first or deeply AI-augmented."
- `fitness_function`: `fitness/topic-discovery-ke.md` (relative to this skill's directory)
- `output_dir`: none (screen-only output)
- `prior_context`: none (fresh swarm)

---

## Scope boundary

This controller is **vault-agnostic** by design. It does not read the tinkering vault, does not know about seed indexes, does not handle routing execution, does not capture operator overrides. Those are all the vault `aar-adapter` skill's job. If there is no adapter / no vault, the SR-* output is still complete and useful on its own — an operator can consume it as a standalone research artifact.

This separation keeps AAR portable: anyone can use it without the vault. The vault integration is opt-in via the adapter.
