---
name: paper-writing-assistant
description: Draft and revise ML/AI paper prose as a claim-aware writing assistant. Use for section writing, result interpretation, venue-aware style, and provisional metrics.
argument-hint: "[paper-dir] [--venue <venue>] [--section <section>] [--mode draft|rewrite|revise|fill-placeholders]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Paper Writing Assistant

Write the paper with the author. This skill is for producing and editing paper prose, not for simulating reviewers. It keeps the paper's claims, venue style, evidence, and provisional placeholders aligned while writing sections such as the abstract, introduction, method, experiments, results, limitations, and conclusion.

Use this skill for:

- drafting or rewriting paper sections
- turning experiment results into claim-supporting result prose
- adapting tone, structure, and paragraph flow to a target venue and paper positioning
- writing figure captions, table captions, paragraph openings, paragraph closings, contribution bullets, transitions, and limitation language
- keeping claims visible while editing individual sections
- inserting clearly marked provisional results when experiments are not finished
- replacing provisional placeholders with verified results later
- maintaining a writing ledger of open placeholders, stale result prose, and claim wording decisions

Do not use this skill to review like a hostile reviewer. Use `paper-reviewer-simulator` for acceptance-risk critique. Use `conference-writing-adapter` for venue-level restructuring and paragraph blueprints. Use `paper-writing-memory-manager` before and after nontrivial edits so local prose changes update the global writing state. Use `paper-evidence-board` when the main task is claim/evidence inventory rather than prose. Use `paper-evidence-gap-miner` when writing reveals a missing result and existing CSVs may already contain the needed evidence. Use `paper-result-asset-builder` when raw CSV results need to become paper-facing tables or figures. Use `experiment-design-planner` only when the gap miner concludes that new compute is required.

## Core Principles

- Write as the author, not as a reviewer. The output should be usable paper prose or a concrete edit plan.
- Preserve the paper's scientific claim. Improve clarity, emphasis, and interpretation without silently changing what the paper asserts.
- Interpret results toward claims. Result prose should explain why the evidence supports, narrows, or complicates the claim.
- Keep evidence status explicit. Verified results, user-stated results, inferred interpretation, and provisional placeholders must not be mixed.
- Temporary results are allowed only as marked writing scaffolds. They must be searchable in the source and tracked in a ledger before final submission.
- If a needed experiment is missing, write the best current section while creating a placeholder and an action, instead of stopping all writing.
- Prefer local draft files, project memory, and evidence artifacts over memory. Do not invent final numbers.
- Use reference-backed writing patterns for concrete prose moves. Do not imitate or store long passages from exemplar papers.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── style-selection.md
    ├── evidence-recipes.md
    ├── exemplar-index.md
    ├── exemplars/
    │   └── *.md
    ├── section-patterns/
    │   ├── abstract.md
    │   ├── introduction.md
    │   ├── method.md
    │   ├── experiments-results.md
    │   ├── related-work.md
    │   └── limitations-conclusion.md
    └── micro-patterns/
        ├── paragraph-openings-closings.md
        ├── result-interpretation.md
        ├── figure-captions.md
        ├── table-captions.md
        └── transitions-and-positioning.md
```

## Progressive Loading

Always read `references/style-selection.md` before substantial drafting or revision.

Read `references/evidence-recipes.md` when selecting paper structure, interpreting results, deciding whether a claim is supported, or handling missing experiments. Use it to map claims to must-have, should-have, optional, and blocker evidence slots.

Read `references/exemplar-index.md` when the user asks for writing based on example papers, when venue/topic positioning is important, or when the section needs concrete precedent from successful papers. Then load only one to three relevant files from `references/exemplars/`.

Then load only the relevant section pattern:

- `references/section-patterns/abstract.md` for abstracts
- `references/section-patterns/introduction.md` for introductions and contribution lists
- `references/section-patterns/method.md` for method, theory setup, benchmark design, or system design
- `references/section-patterns/experiments-results.md` for experiments, results, analysis, and ablations
- `references/section-patterns/related-work.md` for related work and novelty boundaries
- `references/section-patterns/limitations-conclusion.md` for limitations, broader impact, ethics, scope, and conclusion

Load micro-patterns by writing action:

- `references/micro-patterns/paragraph-openings-closings.md` for paragraph starts, paragraph endings, and local flow
- `references/micro-patterns/result-interpretation.md` for result prose, ablation interpretation, claim-evidence bridges, and provisional result language
- `references/micro-patterns/figure-captions.md` for figure captions
- `references/micro-patterns/table-captions.md` for table captions
- `references/micro-patterns/transitions-and-positioning.md` for section transitions, contribution bullets, related-work positioning, and limitation language

Read local project artifacts as needed:

- `memory/claim-board.md`, `memory/evidence-board.md`, `memory/action-board.md`, and `paper/.agent/paper-evidence-board.md` for project truth
- `paper/.agent/writing-memory/` for current writing state, section status, dependencies, style decisions, open threads, and edit-impact history
- `paper/.agent/evidence-completion-plan.md`, `paper/.agent/result-inventory.md`, and `paper/.agent/result-asset-provenance.md` when writing depends on CSV-derived result assets
- `paper/.agent/provisional-results.md` for temporary result placeholders
- `paper/.agent/paper-status.md` for active writing status
- `paper/.agent/visual-style.md` and figure/table maps when result prose depends on figures or tables
- target paper files such as `main.tex`, `paper.tex`, `sections/*.tex`, `figures/`, `tables/`, and appendix files

Pair with `conference-writing-adapter` when target venue style or section structure is uncertain. Pair with `paper-writing-memory-manager` whenever a prose edit changes a claim, result interpretation, section status, caption, terminology, or open writing thread. Pair with `paper-evidence-board` when writing exposes claim/evidence drift. Pair with `paper-evidence-gap-miner` before asking for new experiments, because existing CSV results may already support the claim. Pair with `paper-result-asset-builder` when result prose needs a paper-facing table or figure generated from CSVs.

## Step 1 - Define the Writing Task

Identify:

- target venue and year, if known
- paper positioning or archetype: method, benchmark, empirical study, theory, systems, analysis, application, or hybrid
- topic area and closest exemplar family, if known
- target section and desired mode: draft, rewrite, revise, compress, expand, polish, or fill placeholders
- available source: outline, notes, TeX files, result tables, figures, logs, or memory boards
- whether temporary placeholders are allowed in this pass
- micro-writing target, if any: paragraph opening, paragraph closing, caption, transition, result interpretation, contribution bullet, limitation, or related-work positioning

If the user asks to "help write" without more detail, default to:

1. read the current abstract, introduction, and claim/evidence memory if present
2. produce a paper snapshot
3. propose the next section to write or revise
4. write a concrete section draft when enough context exists

## Step 2 - Build the Writing Snapshot

Before writing substantial prose, extract:

```markdown
## Writing Snapshot
- Target venue:
- Paper positioning:
- Active section:
- Main claim:
- Secondary claims:
- Required evidence:
- Available evidence:
- Missing evidence:
- Evidence recipe loaded:
- Evidence slot status:
- Tone/style target:
- Exemplars loaded:
- Section pattern loaded:
- Micro-patterns loaded:
- Provisional placeholders allowed: yes/no
```

Use claim IDs such as `CLM-001` when available. If the project lacks IDs, assign local `CLM-TMP-001` IDs and recommend syncing them to `paper-evidence-board` or project memory.

## Step 3 - Select Writing Patterns

Read `references/style-selection.md`, then choose:

- one venue/topic/positioning style profile
- one evidence recipe for the primary paper archetype
- zero to three exemplar cards when concrete precedent is useful
- one section pattern file for the active section
- one to three micro-pattern files for the exact prose action

Use this routing:

```text
venue + topic + positioning + section + paragraph job + evidence type
-> section pattern + micro-patterns
```

Examples:

- `NeurIPS + method + introduction + gap paragraph + claim framing` -> `section-patterns/introduction.md` + `micro-patterns/paragraph-openings-closings.md`
- `CVPR + benchmark + figure caption + visual evidence` -> `micro-patterns/figure-captions.md`
- `ACL + empirical study + result paragraph + table evidence` -> `section-patterns/experiments-results.md` + `micro-patterns/table-captions.md` + `micro-patterns/result-interpretation.md`
- `ICLR + method + ablation interpretation + mechanism claim` -> `section-patterns/experiments-results.md` + `micro-patterns/result-interpretation.md`

If writing a broad section, load the section pattern first and add micro-patterns only for paragraphs, captions, transitions, or bullets that need concrete guidance. If writing only a caption, transition, or paragraph opening, load the relevant micro-pattern without loading a whole section file.

When exemplars are loaded, use them only for:

- section move order
- paragraph job sequence
- caption and result-prose strategy
- evidence placement
- tone and scope discipline

Do not copy exemplar wording. Do not let a famous exemplar override the user's actual claim or evidence.

## Step 4 - Map Evidence Slots

Use `references/evidence-recipes.md` to map the active claim to evidence slots before writing final-sounding prose.

For each major claim, classify:

```markdown
- Claim:
- Archetype:
- Required evidence slot:
- Current status: filled / user-stated / planned / running / provisional / missing / contradicted / not-needed
- Paper location:
- Writing consequence:
```

Rules:

- `filled` evidence can be written as observed evidence.
- `user-stated` evidence can be drafted, but mark source verification if the artifact has not been checked.
- `planned`, `running`, or `missing` evidence requires provisional language, an action, or a narrowed claim.
- `contradicted` evidence requires result diagnosis, claim narrowing, or a different paper positioning.
- Missing blocker slots from the evidence recipe should prevent strong final claims.

## Step 5 - Write Claim-Aware Prose

Apply the selected patterns to the user's paper rather than copying template wording. For each paragraph, caption, or bullet, keep a hidden working contract:

For paragraphs:

```markdown
- Paragraph job:
- Claim supported:
- Evidence used:
- Reader question answered:
- Risk if overclaimed:
```

The final prose should not include this contract unless the user asks for an outline. Use it to keep writing disciplined.

For figure captions:

```markdown
- Figure job:
- Claim supported:
- Setup/protocol:
- Visual encoding:
- Takeaway:
- Caveat:
```

For table captions:

```markdown
- Table job:
- Claim supported:
- Comparison question:
- Protocol/metrics:
- Formatting rule:
- Main takeaway:
- Scope caveat:
```

Result interpretation should follow this pattern:

1. state the comparison or observation
2. name the measured setting
3. state what changed relative to the relevant baseline or control
4. explain how this supports the claim
5. state the boundary condition or limitation if needed

Avoid empty claims such as "significantly improves performance" without saying where, against what, and why it matters.

## Step 6 - Handle Missing Experiments While Writing

When writing exposes a missing result:

1. decide whether the prose can be drafted with a provisional placeholder
2. insert a searchable marker in the paper source
3. create or update `paper/.agent/provisional-results.md`
4. create a follow-up action in project memory when present
5. mention the placeholder in the response summary
6. link the placeholder to the evidence recipe slot it is meant to fill

Use this marker format in paper text:

```tex
\textbf{[PROVISIONAL-RESULT PR-001: replace with verified result for CLM-001]}
```

If the venue or project style dislikes visible bold placeholders, use a LaTeX comment plus bracketed prose:

```tex
% PROVISIONAL-RESULT PR-001: replace with verified result for CLM-001
[PR-001: pending main result on DATASET against BASELINE]
```

Never insert an unmarked provisional number into final-looking prose. If the user explicitly asks for a temporary numeric target, mark it as a target or placeholder, not observed evidence. If the missing evidence is a blocker slot for the paper archetype, either narrow the claim or record an action that must be resolved before submission.

## Step 7 - Maintain the Provisional Result Ledger

If provisional placeholders exist, create or update:

```text
paper/.agent/provisional-results.md
```

Use this format:

```markdown
# Provisional Results

## Open Placeholders

### PR-001
- Status: open
- Claim: CLM-001
- Paper location:
- Draft text:
- Placeholder value:
- Evidence recipe slot:
- Why this value supports the claim:
- Required real experiment:
- Expected source artifact:
- Owner:
- Created:
- Replacement rule:

## Resolved Placeholders

### PR-000
- Status: resolved
- Claim:
- Paper location:
- Final value:
- Source artifact:
- Resolved:
- Notes:
```

Replacement rule examples:

- replace placeholder with verified metric from `code/docs/results/...`
- weaken claim if improvement is below baseline on any primary dataset
- remove paragraph if the ablation does not isolate the mechanism

## Step 8 - Replace Provisional Results

When real results arrive:

- find every `PROVISIONAL-RESULT` and `PR-###` marker
- update the prose, tables, captions, and abstract/intro claims if the result changes the story
- move the ledger entry from open to resolved
- mark stale prose or figures in `paper-evidence-board` when present
- if the real result contradicts the claim, route to `result-diagnosis` or narrow the claim rather than forcing supportive language

Before submission, there must be no open `PROVISIONAL-RESULT` markers in paper source.

## Step 9 - Edit Files

For LaTeX projects:

- edit the smallest relevant `sections/*.tex` file
- preserve labels, citations, macros, and line endings
- do not reorganize the source tree unless asked
- use LaTeX comments for traceability when temporary placeholders are present
- keep prose changes local to the requested section unless claim consistency requires synchronized edits

When giving prose in chat instead of editing files, still list any provisional placeholders and the ledger entries that should be created.

## Final Sanity Check

Before finalizing:

- the written prose matches the target venue and paper positioning
- every major assertion supports or preserves a named claim
- major claims satisfy the must-have evidence slots for the selected paper archetype, or are explicitly narrowed
- result interpretation says how the evidence supports the claim
- captions state the claim, setup, visual/table encoding, and takeaway when applicable
- paragraph openings and closings serve the section's argument rather than generic flow
- unverified facts are marked as provisional, user-stated, or needs-verification
- every provisional result has a `PR-###` marker and a ledger entry
- no provisional text is disguised as final observed evidence
- missing experiments have follow-up actions when project memory exists
