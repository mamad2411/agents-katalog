---
name: citation-coverage-audit
description: Audit whether an academic paper cites the necessary classic, closest, and recent concurrent work before submission. Use this skill whenever the user worries that references are incomplete, wants missing citations found, needs related work coverage checked, asks whether a paper cites classic work or recent arXiv/OpenReview work, or wants a citation coverage report for ML/AI venues such as NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, or similar conferences.
argument-hint: "[paper-dir] [--venue <venue>] [--topic <topic>] [--since YYYY-MM] [--add-bibtex]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Citation Coverage Audit

Audit whether a draft paper cites the works it should cite. This skill is about reference completeness: classic foundations, closest prior work, current concurrent work, benchmark/dataset/method attributions, and reviewer-sensitive omissions.

Use this skill when:

- the user has a draft paper but suspects the reference list is incomplete
- a related work section may miss classic or recent work
- the paper needs to cite concurrent arXiv/OpenReview papers before submission
- the paper makes novelty claims that require stronger citation support
- the user wants to reduce reviewer complaints like "missing important related work"

Do not use this as a replacement for `citation-audit`. Use `citation-audit` after this skill to verify that added BibTeX entries and citation keys are correct.

Pair this skill with `research-project-memory` when missing citations affect novelty, baseline, related-work, or reviewer-risk tracking.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── coverage-taxonomy.md
    ├── discovery-protocol.md
    ├── memory-model.md
    └── report-template.md
```

## Progressive Loading

- Always read `references/coverage-taxonomy.md` and `references/discovery-protocol.md`.
- Read `references/report-template.md` when writing the audit output.
- Read `references/memory-model.md` when saving or reusing topic-specific citation coverage knowledge.
- Use current web search for recent and concurrent work. Do not rely on static memory for "latest" or "recent" citations.

## Core Principles

- Missing close citations are submission risks. Treat them as reviewer-facing problems, not bibliography trivia.
- Separate classic foundations, closest prior work, and recent concurrent work. They serve different rhetorical and reviewer functions.
- Search from the paper's claims, not just keywords. A method paper, benchmark paper, theory paper, and empirical study need different citation coverage.
- Prefer primary sources: official papers, proceedings pages, arXiv, OpenReview, ACL Anthology, PMLR, CVF, ACM, IEEE, Springer, Semantic Scholar, DBLP, and authors' project pages.
- Do not pad the bibliography. Recommend citations only when they support a specific sentence, section, baseline, dataset, method component, theorem, or novelty boundary.
- Mark uncertainty. If a candidate looks relevant but cannot be verified, list it as `needs-author-review`.

## Step 1 - Define Scope

Identify:

- target venue and year
- topic and subtopic
- paper archetype: method, theory, empirical study, benchmark/dataset, systems, analysis, application, or hybrid
- paper stage: outline, full draft, final submission, rebuttal, camera-ready
- current source format: LaTeX, PDF, Markdown, notes
- search horizon for recent work, such as last 6 months, last 12 months, or since the previous conference deadline
- whether the user wants a report only or also BibTeX/prose patch suggestions

Default search horizon:

- for active ML/AI topics: last 12 months
- for fast-moving topics such as foundation models, diffusion, reasoning, agents, alignment, or multimodal learning: last 6-9 months plus current OpenReview submissions if accessible
- for theory or mature topics: include classics and last 24 months

## Step 2 - Extract Paper Claims and Existing Coverage

Read the draft and extract:

- title and abstract
- contribution bullets
- introduction novelty claims
- related work categories
- method components
- theorem assumptions or proof techniques
- datasets, benchmarks, metrics, and baselines
- experiment comparison points
- limitation and scope claims
- current citation keys and BibTeX entries

Build a paper citation map:

```markdown
## Paper Citation Map
- Main claim:
- Core method/theory:
- Closest related work currently cited:
- Classic foundations currently cited:
- Recent/concurrent work currently cited:
- Datasets/benchmarks currently cited:
- Baselines currently cited:
- Novelty claims requiring citation support:
- Sections with thin citation coverage:
```

If the draft is incomplete, audit the available claims and mark missing context.

## Step 3 - Classify Required Citation Categories

Read `references/coverage-taxonomy.md`.

For the paper, define required buckets:

- foundational classics
- closest prior work
- direct competitors
- concurrent work
- benchmark/dataset/metric sources
- method/tooling components
- theory/proof technique sources
- negative or limitation-related citations
- surveys or taxonomy papers
- venue-specific or community-standard citations

For each bucket, state why it matters for reviewer perception.

## Step 4 - Discover Missing Work

Read `references/discovery-protocol.md`.

Search iteratively:

1. use the paper's own title/claim keywords
2. search each method component and baseline
3. search closest cited papers forward and backward when possible
4. search recent arXiv/OpenReview/proceedings for the topic
5. search venue-specific accepted/oral/spotlight papers if the target venue matters
6. inspect surveys or benchmark leaderboards for canonical citations

For recent/concurrent work, include access dates and search queries. Search results change over time.

Do not recommend a paper only because it shares keywords. Each candidate must map to a citation role.

## Step 5 - Evaluate Candidate Relevance

For each candidate missing paper, classify:

- `must-cite`: close prior work, direct competitor, foundational citation, dataset/metric/source attribution, or work required to support/qualify a novelty claim
- `should-cite`: relevant recent work, adjacent strong baseline, useful survey, or important related line reviewers may expect
- `optional`: context or breadth citation that improves related work but is unlikely to affect review
- `do-not-cite`: keyword match but not scientifically relevant
- `needs-author-review`: relevance plausible but not enough evidence to decide

For every `must-cite` or `should-cite`, specify:

- where to cite it
- what claim it supports or qualifies
- how it changes novelty framing
- whether it needs BibTeX
- whether it suggests new experiments or baselines

## Step 6 - Check Novelty and Reviewer Risk

For each novelty claim, ask:

- Is the closest prior work cited?
- Is the difference stated correctly?
- Would a reviewer expect this missing paper?
- Does the missing paper weaken the novelty claim?
- Does it require a new baseline, ablation, theorem comparison, or discussion?

Risk levels:

- `blocking`: missing citation could make a novelty claim look false or unethical
- `high`: reviewer likely complains about missing related work
- `medium`: omission weakens positioning but probably not fatal
- `low`: useful completeness citation

## Step 7 - Produce Coverage Report

Use `references/report-template.md`.

The report should include:

- paper citation map
- search strategy and search date
- candidate missing citations
- must-cite and should-cite recommendations
- exact insertion points
- novelty-framing updates
- baseline/experiment implications
- unresolved author decisions

If the user wants a saved report and gives no path, use:

```text
docs/reports/citation_coverage_audit_YYYY-MM-DD.md
```

## Step 8 - Optional BibTeX and Text Patches

If the user asks for edits:

- add BibTeX only from verified metadata
- insert citations at the smallest safe location
- do not make broad related-work rewrites unless asked
- do not cite papers you have not verified enough to identify
- after edits, run or recommend `citation-audit` to verify keys and metadata

When exact prose is uncertain, write a suggested sentence in the report instead of editing the paper.

## Step 9 - Update Citation Coverage Memory

Read `references/memory-model.md`.

When a topic scan was performed:

1. update `.agent/citation-coverage/topics/<topic-slug>.md`
2. update `.agent/citation-coverage/project-coverage.md`
3. record search queries, access dates, candidate papers, and decisions

Memory must separate:

- canonical papers for the topic
- recent/concurrent papers with access dates
- papers already cited
- papers intentionally not cited
- unresolved author decisions

If the project uses `research-project-memory`, also update:

- `memory/risk-board.md`: missing closest-work, classic, benchmark, baseline, or concurrent-work risks
- `memory/action-board.md`: add-citation, check-bibtex, add-baseline, revise-novelty, or author-review actions
- `memory/claim-board.md`: novelty claims that must be weakened or qualified
- `memory/evidence-board.md`: citation evidence for claims when a paper directly supports or limits a claim
- `paper/.agent/paper-status.md`: related-work sections or insertion points that need edits

Use `needs-verification` for candidate papers not yet read deeply enough.

## Final Sanity Check

Before finalizing:

- classic, closest, and recent/concurrent work were considered separately
- search queries and dates are recorded
- every recommended paper has a citation role
- must-cite recommendations include insertion points
- novelty risks are explicit
- uncertain candidates are not presented as verified
- any edits are followed by a recommendation to run `citation-audit`
