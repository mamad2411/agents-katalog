---
name: qraspi-research
audience: team
description: >
  QRASPI Research phase -- map the solution LANDSCAPE for a new system, factual only, no
  recommendations. Use for "/qraspi-research <project>", "research the solution landscape for new
  X", "what libraries / prior art exist for X", "survey the options before architecting X". Mode
  switch: external-domain (no codebase) or inherited-repo. Do NOT use for QRSPI (an EXISTING
  codebase / adding a feature) -- that routes to qrspi-research. Do NOT use for the deprecated RPI
  workflow.
---

# QRASPI Research

> "The map is not the territory."
> -- Alfred Korzybski

## Core Philosophy

The Research phase produces a **factual landscape map of the solution space** -- never a
recommendation. Greenfield has no ticket to hide and (in the default mode) no codebase to map;
the failure mode shifts from QRSPI's "biased map" to **premature solution** -- the agent quietly
picking FastAPI + Postgres before the Architecture phase has weighed a single trade-off.
Recommendations are Architecture's job, gated behind ADRs. This phase catalogs what EXISTS in the
solution space -- libraries, prior art, patterns, constraints -- and converts every comparative
judgment into an open question for Architecture to decide.

The phase runs in one of two modes, detected at pre-flight (`references/landscape-vs-codebase.md`):
**external-domain** (default; pure greenfield) maps the problem domain and solution landscape via
`research-synthesis` and the web; **inherited-repo** (greenfield component inside an existing repo)
maps the host repo's conventions via the read-only `research-*` subagents.

**Non-Negotiable Constraints:**
1. LANDSCAPE, not evaluation -- catalog what EXISTS in the solution space; convert every
   comparative judgment into an open question for Architecture. Recommendations are A's job.
2. NO premature solution -- the state flag `recommendations_made` MUST stay false; do not pick a
   stack, framework, or library here
3. CITE every claim -- external-domain: source + credibility (via `research-synthesis`);
   inherited-repo: `file:line`. An uncited claim is dropped.
4. MODE-AWARE firewall -- external-domain uses source-credibility discipline; inherited-repo
   passes ONLY a neutral topic string to the read-only subagents (never the project goal)
5. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `research.md` with progress and
   tell the user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the project folder thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
    [ ] Read the ANSWERED questions.md to scope the landscape (areas/constraints only)
        -> If no questions.md exists, scope from the argument and note the gap
    [ ] DETECT research_mode (see references/landscape-vs-codebase.md):
        populated source tree at the target?  no -> external-domain (default)   yes -> inherited-repo

GATHER
    external-domain:  invoke research-synthesis; survey libraries, prior art, patterns, and
                      constraints via WebSearch/WebFetch; score source credibility; facts + citations
    inherited-repo:   derive a NEUTRAL topic string; spawn in PARALLEL via the Task tool, passing
                      ONLY that string:
                        @research-file-locator   "Find all files related to: {neutral topic}"
                        @research-code-analyzer  "Analyze the implementation of: {neutral topic}"
                        @research-pattern-finder "Find patterns and conventions related to: {neutral topic}"
                      wait for ALL THREE before synthesizing
                      NO subagent support (Pi): run the same three passes SEQUENTIALLY in this
                      session -- locate, then analyze, then patterns -- writing each pass to
                      research-{locate,analyze,pattern}.md before the next, and synthesizing from
                      those files. The ticket/goal must still never enter the session.

SYNTHESIZE
    Organize into overview, landscape findings, options-on-the-table, constraints, open questions.
    Convert EVERY comparative judgment ("X is faster than Y") into an open question for Architecture.
    Compact to <= ~200 lines.

WRITE
    thoughts/shared/qraspi/YYYY-MM-DD-{slug}/research.md   (references/research-template.md)
    Set status: complete

REPORT
    Artifact path · 3-5 landscape facts · the options surfaced (NOT a pick) · open questions ·
    "Review, then start a NEW session and run /qraspi-architecture"
```

**Exit criteria:** `research.md` written as a factual landscape map; mode recorded; every claim
cited; every comparative judgment converted to an open question; `recommendations_made: false`;
user told to review before `/qraspi-architecture`.

## State Block

```
<qraspi-research-state>
phase: PRE-FLIGHT | GATHER | SYNTHESIZE | WRITE | REPORT | COMPLETE
project_folder: thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
research_mode: external-domain | inherited-repo
recommendations_made: false   # MUST remain false -- the no-premature-solution firewall
neutral_topic: [ticket-free topic string | n/a for external-domain]
subagents_spawned: 0 | 1 | 2 | 3   # inherited-repo only
subagents_complete: 0 | 1 | 2 | 3  # inherited-repo only
open_questions: [count]
context_budget: under-40 | approaching-60 | checkpoint-now
status: in_progress | complete
</qraspi-research-state>
```

## Output Template

See `references/research-template.md` for the full `research.md` structure and frontmatter, and
`references/landscape-vs-codebase.md` for mode detection and the per-mode evidence rules.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qraspi-questions` | Prior phase. Its answered `questions.md` scopes the landscape. |
| `qraspi-architecture` | Next phase. Consumes `research.md`; it -- not this phase -- makes the picks via ADRs. |
| `research-synthesis` | The external-domain engine: source-credibility scoring and cross-referencing for the landscape map. |
| `qrspi-research` | Brownfield sibling. Use it instead when the system EXISTS and you are mapping it to add a feature. |
