---
name: reference-corpus-analyzer
description: Produce a multi-paper comparison matrix across a literature corpus with tiered read depth. Use when multiple papers need to be compared side-by-side for method differences, performance gaps, closest-work ranking, or trend identification — distinct from per-paper source cards (reference-reading-summarizer) and single-paper project linking (reference-project-synthesizer).
argument-hint: "[project-dir] [--corpus <path>] [--top-n <N>] [--mode compare|rank|trend|gap]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Reference Corpus Analyzer

Synthesize a literature corpus into a structured comparison matrix. This skill answers: *across these N papers, who does what, how do they differ, and where is the open space?*

Use this skill when:

- related-work writing requires a side-by-side method comparison across multiple papers
- you want to identify the closest 3–5 papers and understand exactly how they differ from each other
- a literature survey needs trend identification across publication years or venues
- you want to map open gaps across a set of existing approaches before writing the related-work section
- you have 5+ source cards and want a comparison table rather than individual summaries

Do not use this skill to create per-paper source cards — use `reference-reading-summarizer` for that. Do not use this skill to link a paper to your project's claims — use `reference-project-synthesizer` for that. Use this skill after source cards exist; avoid re-reading raw PDFs unless a card is insufficient.

Pair this skill with:

- `reference-reading-summarizer` upstream: produce source cards before running corpus analysis
- `reference-project-synthesizer` upstream or downstream: link individual papers to project memory before or after comparison
- `related-work-positioning-writer` downstream: use the comparison matrix to write novelty-boundary paragraphs
- `baseline-selection-audit` downstream: use the ranking to identify must-have baselines
- `literature-review-sprint` when the corpus is not yet assembled and a broader topic survey is needed first

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── templates/
    └── comparison-matrix.md
```

## Progressive Loading

- Read `reference/cards/` to find available source cards before reading raw sources.
- Read `reference/.agent/source-index.md` or `reference/.agent/reference-index.md` to get the corpus inventory.
- Read `memory/claim-board.md` when the comparison should be anchored to specific project claims.
- Read `templates/comparison-matrix.md` before writing the output matrix.

## Core Principles

- Tiered depth: read deeply only the top-N closest papers; skim the rest for placement.
- The comparison matrix is a project artifact, not a free-text essay — it should be queryable.
- Ranking closest work requires a clear criterion: task overlap, method overlap, or claim overlap.
- Gaps should be stated specifically: "no paper does X under constraint Y" beats "X is underexplored".
- Do not invent paper properties not stated in the source card or the paper itself.

## Step 1 — Assemble the Corpus

Read `reference/.agent/source-index.md` (or `reference-index.md`) to list available sources.

For each source, record:
- source ID and title
- card availability: `has-card`, `no-card`, `partial-card`
- initial relevance estimate: `core`, `related`, `background`, `tangential`

If cards are missing for sources that appear highly relevant, route to `reference-reading-summarizer` first.

## Step 2 — Select Tiered Read Depth

Assign read depth to each source:

| Tier | Sources | Read depth |
|---|---|---|
| Deep | Top 3–5 closest by task + method overlap | Full source card; re-read raw source if card is insufficient |
| Standard | Next 5–10 related works | Source card only |
| Survey | Remaining background papers | Title + abstract + card summary |

Criterion for "closest": same task, same claim type, overlapping method family, or shared benchmark.

## Step 3 — Build the Comparison Matrix

Read `templates/comparison-matrix.md`.

Dimensions to compare (select those relevant to the project):

- **Task / problem**: what problem does the paper address?
- **Method family**: what is the core mechanism (attention, diffusion, RL, prompting, etc.)?
- **Key innovation**: what is the single thing this paper claims to contribute?
- **Benchmark / dataset**: what is it evaluated on?
- **Primary metric**: what metric is reported?
- **Best reported result**: the headline number (with venue and year for context)
- **Limitations acknowledged**: what does the paper say it cannot do?
- **Relationship to our work**: closer / complementary / orthogonal / superseded by ours

For each tier-1 (deep) paper, also add:
- **Closest claim to ours**: the specific claim that most overlaps with our paper's contribution
- **Key differentiator**: in one sentence, how our work differs from this paper

Save to `reference/corpus-analysis-<date>.md`.

## Step 4 — Rank Closest Work

Produce a ranked list of the top-5 closest papers with:

```markdown
Rank: 1
Paper: [title] ([venue year])
Overlap: task=high / method=medium / claim=high
Closest claim: [their specific claim that overlaps ours]
Differentiator: [one sentence: how we differ]
Novelty risk: high / medium / low
Reviewer action: cite as closest work / cite as baseline / cite as background
```

A paper with `novelty risk: high` and `method=high` overlap is the paper whose related-work paragraph needs the clearest boundary statement.

## Step 5 — Identify Gaps and Trends

Gaps: what combinations of (task, method, constraint, benchmark) are not yet addressed by any paper in the corpus?

```
Gap: no paper addresses [X] under [constraint Y] with [method family Z]
Evidence: papers A, B, C address X but not under Y; papers D, E address Y but not X
Opportunity: our work fills this gap by [brief description]
```

Trends (optional, for survey mode):
- Which method families are gaining / losing papers over the last 3 years?
- Which benchmarks are becoming standard vs. falling out of use?
- What claims were controversial 2 years ago and are now accepted?

## Step 6 — Write Memory Writeback

- Update `reference/.agent/source-index.md` with read-depth assignments
- Update `memory/risk-board.md` for any high-novelty-risk closest-work findings
- Update `memory/claim-board.md` if the comparison changes the novelty framing of a claim
- The comparison matrix itself is saved in `reference/` — do not copy it into `memory/`

## Final Sanity Check

Before finishing:

- tier-1 papers have been read at full card depth
- the comparison matrix has consistent dimensions across all papers
- top-5 closest-work ranking has differentiators in one sentence each
- gaps are stated specifically (not as vague "future work" language)
- novelty-risk papers are flagged for `related-work-positioning-writer`
