---
name: literature-review-sprint
description: Guide a focused CS or AI literature review sprint that turns a topic, idea, claim, or project direction into a ranked paper map, closest-work risk assessment, method taxonomy, novelty implications, baseline implications, and next actions. Use this skill whenever the user needs to survey a topic, check novelty, map related work, prepare a project, find canonical or recent papers, decide read/skim/ignore priority, or turn papers into a research direction.
argument-hint: "[topic-or-project-dir] [--area <area>] [--mode quick|full|novelty|baseline|positioning]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Literature Review Sprint

Turn a broad topic, rough idea, or uncertain project direction into a ranked literature map and concrete research implications.

Use this skill when:

- a user needs to understand a new field quickly
- novelty depends on whether close prior work already exists
- a project needs canonical, closest, and recent/concurrent papers before algorithm or experiment design
- a paper draft has weak related-work positioning but the goal is still field understanding, not final citation cleanup
- an advisor meeting needs a crisp paper map, gap analysis, or next reading plan
- early experiments or writing reveal that the project may be in the wrong literature frame

Do not use this skill as a metadata or BibTeX checker. Use `citation-audit` for citation correctness and `citation-coverage-audit` for submission-time missing-reference review.

Pair this skill with:

- `research-project-memory` when literature findings should persist as risks, actions, claims, or positioning decisions
- `research-idea-validator` before or after the sprint when the result should become a pursue/revise/park/kill decision
- `algorithm-design-planner` when the map clarifies the closest baseline and the method now needs specification
- `experiment-design-planner` when the map implies required baselines, datasets, metrics, or diagnostics
- `paper-evidence-board` when literature risks should be linked to paper claims, sections, figures, and reviewer risks
- `citation-coverage-audit` later, after the paper is close to submission

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── memory-writeback.md
    ├── paper-taxonomy.md
    ├── reading-priority.md
    ├── search-protocol.md
    └── synthesis-template.md
```

## Progressive Loading

- Always read `references/search-protocol.md`, `references/paper-taxonomy.md`, and `references/reading-priority.md`.
- Read `references/synthesis-template.md` before writing the final sprint report.
- Read `references/memory-writeback.md` when a project has `memory/`, component `.agent/` folders, or the user asks for cross-session memory.
- If the user asks about recent, concurrent, accepted, or current work, verify with current sources through web search, OpenReview, proceedings pages, arXiv, DBLP, Semantic Scholar, ACL Anthology, PMLR, CVF, or user-provided papers.
- If web access is unavailable, state that the output is a provisional reading plan and mark unverified papers or gaps explicitly.

## Core Principles

- Optimize for project decisions, not an exhaustive bibliography.
- Separate canonical background, closest competitors, adjacent tools, and recent/concurrent threats.
- Treat unknown closest work as a major novelty risk.
- Rank papers by decision value: what changes the project if this paper is strong?
- Convert literature findings into baselines, ablations, claims to avoid, and writing positions.
- Preserve search provenance: where searched, when, which queries, and what was excluded.
- Do not overclaim novelty from absence of evidence.
- End with a next action that changes the project trajectory.

## Step 1 - Define the Sprint Question

Recover:

- topic, project idea, paper claim, or draft section
- target area and venues, if known
- intended contribution type
- known seed papers, baselines, datasets, or methods
- what decision the sprint must support
- time budget: quick scan, focused half-day, full sprint, novelty check, baseline check, or positioning check
- project memory IDs such as `CLM-###`, `RSK-###`, or `ACT-###`, if present

Rewrite the sprint question as:

```text
For [topic/claim], determine whether [proposed contribution] is novel and important relative to [closest families], and identify [papers/baselines/gaps] that change the next project decision.
```

If the user only asks for "papers about X", still produce a decision-oriented map.

## Step 2 - Build a Search Protocol

Read `references/search-protocol.md`.

Create:

- seed concepts and synonyms
- method names and older terminology
- venue filters and likely communities
- canonical-source search paths
- recent/concurrent search paths
- backward and forward citation plan
- OpenReview or proceedings search plan when venue style matters
- stopping criteria

For current literature, record source names and dates. Prefer primary sources over blog posts, slides, or secondhand summaries.

## Step 3 - Collect and Classify Candidate Papers

Read `references/paper-taxonomy.md`.

Classify each candidate into one or more roles:

- foundational or canonical
- closest prior work
- direct competitor
- baseline method
- benchmark, dataset, or metric source
- adjacent method family
- theory or analysis source
- empirical survey or taxonomy
- recent or concurrent threat
- negative result or limitation evidence
- writing or positioning exemplar

For each important paper, extract a compact card:

```text
Paper:
Role:
Core idea:
What it proves or demonstrates:
Relation to our project:
Decision impact:
Read priority:
Verification/source:
```

## Step 4 - Prioritize Reading

Read `references/reading-priority.md`.

Assign:

- `read-now`: can change novelty, baseline selection, method design, or project viability
- `skim`: useful for context or framing, unlikely to change the core decision
- `defer`: relevant but not needed for this sprint's decision
- `ignore-for-now`: out of scope, weakly related, or superseded for current purpose

Every `read-now` paper must have a reason tied to a project decision.

## Step 5 - Synthesize the Literature Map

Build:

- method-family map
- chronology of key ideas
- closest-work comparison table
- baseline implications
- dataset, metric, or protocol implications
- theory or assumption implications
- open gaps and saturated claims
- terminology map for search and writing

Flag:

- `novelty-risk`: close work may already cover the idea
- `baseline-risk`: a missing baseline would weaken experiments
- `positioning-risk`: the project is framed in the wrong community or contribution type
- `evidence-risk`: available experiments do not address the field's standard concern
- `scope-risk`: the literature is too broad for the current project shape

## Step 6 - Convert Findings into Project Decisions

Return concrete implications:

- should the idea be pursued, revised, parked, or killed?
- what is the closest prior work to beat or distinguish from?
- what claim is still defensible?
- what claim should be avoided?
- what baseline must be implemented or cited?
- what experiment, theorem, diagnostic, or analysis becomes mandatory?
- what writing frame is likely reviewer-friendly?
- what next skill should be used?

If the literature map changes the project direction, route to `research-idea-validator` or `algorithm-design-planner` before experiments.

## Step 7 - Write the Sprint Report

Read `references/synthesis-template.md`.

If saving to a project and no path is given, use:

```text
docs/literature/literature_sprint_YYYY-MM-DD_<short-name>.md
```

The report must include:

- sprint question
- search log and limitations
- ranked paper map
- closest-work risks
- method taxonomy
- baseline and evaluation implications
- project decision implications
- next reading or experiment actions
- memory update section

## Step 8 - Write Back to Project Memory

Read `references/memory-writeback.md` when memory exists.

Update the smallest useful set of entries:

- `memory/decision-log.md`: literature-driven project or positioning decisions
- `memory/risk-board.md`: closest-work, baseline, evidence, and positioning risks
- `memory/action-board.md`: read-now papers, baseline checks, implementation tasks, or writing tasks
- `memory/claim-board.md`: claims to keep, revise, narrow, park, or cut
- `memory/evidence-board.md`: planned baseline, dataset, metric, theorem, or diagnostic evidence
- `paper/.agent/` when related-work or positioning notes affect a draft

Use:

- `verified` for facts checked against primary sources
- `user-stated` for papers or constraints supplied by the user
- `inferred` for risk judgments and positioning implications
- `unverified` for search leads not yet checked

## Final Sanity Check

Before finalizing:

- search scope and limitations are explicit
- papers are ranked by decision impact, not merely listed
- closest-work risk is named even if unresolved
- recent/concurrent search status is stated
- baseline implications are concrete
- project claims are adjusted when needed
- next skill or next action is unambiguous
- memory writeback is performed when the project has memory
