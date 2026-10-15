---
name: conference-writing-adapter
description: Adapt an ML paper's writing, structure, positioning, and paragraph-level narrative to a target conference such as NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, or similar venues. Use this skill whenever the user wants to submit, rewrite, polish, restructure, or tailor a paper for a specific conference; asks what good accepted/oral papers at a venue look like; wants reviewer-friendly writing; or wants section-by-section or paragraph-by-paragraph paper guidance. This is a writing and presentation skill, not an experiment-design skill.
allowed-tools: Read, Write, Edit, Bash, Glob, WebFetch, WebSearch
---

# Conference Writing Adapter

Adapt an existing research paper to the writing conventions, reviewer expectations, and paper archetypes of a target ML/AI conference. The goal is to make the paper easier for the right reviewers to understand, trust, and champion without inventing unsupported claims or new experimental results.

Use this skill for:

- paper structure diagnosis before submission
- conference-specific rewrite plans
- abstract, introduction, method, experiment, limitation, and related-work rewrites
- venue-aware figure/table story, visual style, and result presentation decisions
- paragraph-level outlines for an existing draft
- learning from accepted, oral, spotlight, best-paper, or highly discussed papers at the target venue
- accumulating reusable knowledge about venue taste and successful paper patterns

Do not use this skill as a substitute for running experiments, proving claims, or checking final submission compliance. Pair it with `submit-paper` for final readiness checks and with experiment skills when the paper has evidence gaps. Use `figure-results-review` when the main issue is whether a figure/table's claim support, style, caption, or visual encoding is paper-ready.

Pair this skill with `research-project-memory` when rewriting changes paper claims, section structure, figure/table roles, writing risks, or experiment actions.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── conference-profiles.md
    ├── exemplar-analysis.md
    ├── memory-model.md
    ├── paper-archetypes.md
    ├── quality-gates.md
    └── paragraph-protocol.md
```

## Progressive Loading

- Always read `references/paper-archetypes.md` and `references/paragraph-protocol.md`.
- Read `references/conference-profiles.md` when the user names a target conference or asks to compare venues.
- Read `references/exemplar-analysis.md` when the task involves learning from accepted, oral, spotlight, best-paper, or otherwise strong target-venue papers.
- Read `references/quality-gates.md` before finalizing a rewrite plan or rewritten section.
- Read `references/memory-model.md` whenever learning from accepted papers, saving venue knowledge, or reusing prior knowledge.
- When target venue rules may affect writing or formatting, verify current official instructions from the venue website. Do not rely only on memory for page limits, checklist requirements, anonymity, supplementary rules, or ethics/impact requirements.

## Core Principles

- Optimize for reviewer cognition, not ornamental prose. A good paper makes the contribution, evidence, and limitations easy to evaluate.
- Match the paper to an archetype before rewriting. A method paper, benchmark paper, theory paper, dataset paper, system paper, and empirical study need different narrative skeletons.
- Learn from venue exemplars. For a target conference, inspect accepted/oral/spotlight/best-paper examples when available, then extract reusable writing patterns rather than copying text.
- Keep every paragraph accountable. Each paragraph should have one reviewer-facing job: motivate, identify a gap, state an insight, define a method component, support a claim, preempt a concern, interpret evidence, or delimit scope.
- Do not fabricate evidence. If the paper needs an experiment, ablation, theorem, user study, or analysis that does not exist, mark it as a writing blocker and suggest how to phrase the current limitation.
- Preserve the user's scientific intent. Improve positioning, structure, and clarity without changing the underlying claim beyond available evidence.

## Step 1 - Define the Adaptation Task

Identify:

- target conference and year, if known
- submission track, if relevant
- current paper format: LaTeX source, PDF, Markdown draft, outline, or notes
- desired output: diagnosis, rewrite plan, paragraph blueprint, rewritten section, full-paper pass, or venue knowledge note
- paper stage: idea, early draft, full draft, rebuttal revision, camera-ready
- whether internet access or user-provided exemplar papers are available

If the user only says a venue name and provides a draft, default to:

1. diagnose the paper archetype
2. compare it with target venue expectations
3. produce a section-level and paragraph-level rewrite plan
4. rewrite the abstract and introduction if the draft contains enough evidence

## Step 2 - Gather Paper Evidence

Prefer primary draft files and notes over memory.

Look for:

- `main.tex`, `paper.tex`, `sections/*.tex`, `*.bib`, `README.md`, `docs/`, `notes/`
- title, abstract, introduction, contribution list
- figures and tables, especially the main result figure
- existing visual style choices: palette, markers, symbols, font sizes, line widths, figure sizing, and table conventions
- method claim, assumptions, theorem statements, or system design
- experiment setup, baselines, ablations, datasets, metrics, qualitative examples
- limitations, broader impact, ethics, checklist, and appendix

Extract the paper into this working summary:

```markdown
## Paper Snapshot
- Current title:
- Target venue:
- Claimed contribution:
- Core technical idea:
- Primary evidence:
- Strongest result:
- Most likely reviewer concern:
- Missing or weak evidence:
- Current structure:
```

If the draft is too incomplete to rewrite, produce a structural plan and a list of missing evidence instead of pretending the paper is ready.

## Step 3 - Learn the Target Venue Taste

Read `references/conference-profiles.md`, then refine it with current evidence.
When learning from multiple exemplar papers, read `references/exemplar-analysis.md` and produce a compact style matrix before recommending a rewrite strategy.

Sources to prefer:

- official venue call for papers and author instructions
- accepted/oral/spotlight/best-paper lists
- OpenReview pages, using API/exported data/user-provided PDFs when the visible page is client-rendered
- proceedings pages and official PDFs
- reviewer guidelines, checklist requirements, and area descriptions

When using OpenReview:

- The group page may load notes client-side and expose only "Loading" in static HTML.
- If direct page content is unavailable, use OpenReview API endpoints, the venue's official accepted-paper export, search results, or user-provided links/PDFs.
- Prioritize papers with status such as oral, spotlight, notable, award, or high-review visibility, but include archetype diversity rather than only the most famous papers.

Extract patterns from exemplars:

- paper archetype
- title style
- abstract shape
- introduction move sequence
- where the core claim appears
- how contributions are enumerated
- method exposition density
- experiment narrative order
- figure/table role
- visual style: palette, typography, symbol conventions, figure density, caption style, and table compactness
- limitation handling
- reviewer concern preemption

Do not copy phrasing from exemplar papers. Distill patterns.

## Step 4 - Diagnose the Paper Archetype

Read `references/paper-archetypes.md` and classify the user's draft.

Use one primary archetype and optional secondary archetypes:

- `method`: new algorithm, architecture, objective, training recipe, inference procedure, or theoretical method
- `empirical-study`: systematic finding about models, data, scaling, evaluation, or failure modes
- `benchmark-dataset`: new dataset, task, benchmark, protocol, or evaluation suite
- `theory`: theorem-led paper with formal assumptions, guarantees, or impossibility results
- `systems`: infrastructure, serving, training, tool, compiler, data pipeline, or large-scale engineering contribution
- `analysis`: interpretability, diagnostic, causal, or mechanistic analysis
- `application`: strong domain result where novelty comes from ML adaptation plus evidence in a demanding setting

Then decide whether the current venue favors this archetype and what style variant fits best.

## Step 5 - Build the Reviewer-Facing Narrative

Write a narrative diagnosis before rewriting:

```markdown
## Venue Fit Diagnosis
- Target venue:
- Paper archetype:
- Best-fit style:
- Reviewer promise:
- Main tension:
- What must be obvious by the end of page 1:
- What must be proven by experiments/theory:
- Main figure/table role and visual style:
- What should move to appendix:
- Writing risks:
```

The "reviewer promise" is the sentence a reviewer should be able to say after reading the introduction:

> This paper matters because [problem], and it deserves acceptance because [specific contribution] is supported by [specific evidence].

## Step 6 - Produce a Section-Level Rewrite Plan

For a standard ML conference paper, plan:

- Title
- Abstract
- Introduction
- Background or Problem Setup
- Method / Approach / Theory / Benchmark Design
- Experiments / Evaluation
- Analysis / Ablations / Discussion
- Related Work
- Limitations / Ethics / Broader Impact
- Appendix / Supplementary

For each section, specify:

- section job
- target length or page budget
- required claims
- required evidence
- paragraphs to include
- material to cut or move
- venue-specific cautions
- figure/table role and visual style constraints when the section depends on visual evidence

If official page limits are relevant, verify current rules and state the source.

## Step 7 - Produce a Paragraph-Level Blueprint

Read `references/paragraph-protocol.md`.

For every important paragraph, output:

```markdown
### [Section] P[N]
- Function:
- Reader question answered:
- Claim:
- Evidence or support:
- Opening move:
- Closing move:
- Keep:
- Cut or move:
- Risk if weak:
```

Use this level of detail especially for the abstract, introduction, method overview, main experiment setup, and result interpretation.

## Step 8 - Rewrite Text

When rewriting, preserve traceability:

- Rewrite only sections that have enough evidence.
- Keep claims no stronger than the paper's evidence.
- Use explicit placeholders for missing facts, such as `[INSERT MAIN RESULT: metric, baseline, dataset]`.
- Prefer concrete nouns and verbs over hype.
- State contributions as claim plus evidence, not as vague novelty.
- Add reviewer-facing transitions that explain why the next section exists.

For LaTeX projects, edit the smallest relevant file. Do not reorganize the entire source tree unless the user asks.

## Step 9 - Run Quality Gates

Read `references/quality-gates.md` before finalizing a plan or rewritten section.

At minimum, check:

- venue fit: the structure and tone match the target venue rather than generic ML writing
- archetype fit: the chosen paper shape matches the actual contribution
- claim-evidence alignment: every major claim has evidence or is marked as missing
- paragraph function: each important paragraph has one reviewer-facing job
- rebuttal readiness: obvious objections are preempted in the main text or flagged
- reproducibility and assumptions: rules, assumptions, and appendix promises are explicit

If a gate fails, revise once before returning the result. If it still fails because evidence is missing, report the blocker instead of smoothing it over.

## Step 10 - Update Writing Memory

Read `references/memory-model.md`.

When the task involved studying target-venue exemplars or the user explicitly wants knowledge to persist:

1. create or update project-local memory under `.agent/conference-writing/`
2. add venue observations to `.agent/conference-writing/venues/<venue>.md`
3. add exemplar notes to `.agent/conference-writing/exemplars/<venue>-<year>.md`
4. add reusable decisions to `.agent/conference-writing/project-style.md`

Memory entries must separate:

- observed patterns from specific papers
- inferences about venue taste
- decisions for the current paper
- unresolved questions

Do not store copyrighted paper text beyond short titles, bibliographic metadata, and brief paraphrased notes.

If the project uses `research-project-memory`, also update:

- `memory/claim-board.md`: revised claim wording, paper locations, and unsupported claims to cut or weaken
- `memory/evidence-board.md`: figure/table roles and evidence items cited by rewritten sections
- `memory/risk-board.md`: writing, positioning, venue-fit, and evidence-gap risks
- `memory/action-board.md`: missing experiments, citation checks, section rewrites, or figure updates exposed by writing
- `paper/.agent/paper-status.md`: section map, paragraph-level decisions, and stale figures/tables
- `paper/.agent/visual-style.md` or `.agent/conference-writing/project-style.md`: venue-facing figure style decisions, including palette, symbol, typography, and table conventions

Do not strengthen claims in memory beyond the evidence available in the paper.

## Output Formats

### Diagnosis Only

```markdown
# Conference Writing Diagnosis
## Paper Snapshot
## Venue Fit Diagnosis
## Archetype Classification
## Main Reviewer Risks
## Recommended Rewrite Strategy
```

### Rewrite Plan

```markdown
# [Venue] Rewrite Plan
## Paper Snapshot
## Venue Pattern Summary
## Narrative Strategy
## Section-Level Plan
## Paragraph-Level Blueprint
## Evidence Gaps
## Appendix / Page-Budget Plan
## Memory Updates
```

### Rewritten Section

```markdown
# Rewritten [Section Name]
## Before/After Intent
## Draft Text
## Remaining Placeholders
## Why This Fits [Venue]
```

## Final Sanity Check

Before finalizing:

- the target conference and year are explicit
- current venue rules were verified if page limits or mandatory sections matter
- exemplar-derived observations are paraphrased and attributed at a high level
- the user's paper archetype is stated
- every paragraph in the blueprint has a clear reviewer-facing function
- the quality gates have been run and any failing gate is reported
- unsupported claims are marked as gaps
- memory updates, if any, are written to project-local files
