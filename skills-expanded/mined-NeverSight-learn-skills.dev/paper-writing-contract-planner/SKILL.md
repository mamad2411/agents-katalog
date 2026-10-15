---
name: paper-writing-contract-planner
description: Create a paper writing contract before drafting. Use to lock venue, positioning, archetype, section order, paragraph roles, evidence slots, figure/table jobs, and forbidden claims.
argument-hint: "[paper-dir-or-project-root] [--venue <venue>] [--archetype <type>] [--mode create|update|audit]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Paper Writing Contract Planner

Create the paper's writing contract: a durable agreement about what the paper is, what each section must do, which claims are allowed, what evidence each claim requires, and how later writing skills should execute the draft. This skill plans the "paper formula" before prose writing.

Use this skill for:

- locking the target venue, paper archetype, and positioning
- choosing the section order and paragraph roles
- mapping claims to required evidence slots
- assigning jobs to figures, tables, captions, and result paragraphs
- defining related-work boundaries and limitation policy
- selecting exemplar patterns and writing style rules
- forbidding unsupported claims, tone, or result language
- creating or updating `paper/.agent/writing-contract.md`

Do not use this skill to write full paper prose. Use `paper-writing-assistant` after the contract exists. Use `paper-writing-memory-manager` after creating or updating the contract so section status, dependencies, style rules, and open writing threads reflect the new agreement. Use `paper-positioning-planner` first if the primary contribution is still undecided. Use `paper-evidence-board` if the main task is a claim/evidence inventory. Use `experiment-design-planner` when missing evidence needs a runnable experiment plan.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── contract-schema.md
│   └── update-protocol.md
└── templates/
    └── writing-contract.md
```

## Progressive Loading

- Always read `references/contract-schema.md` and `templates/writing-contract.md`.
- Read `references/update-protocol.md` when updating an existing contract or when the draft/results changed.
- Read `paper-writing-assistant/references/evidence-recipes.md` when available and the contract needs archetype-specific evidence slots.
- Read `paper-writing-assistant/references/style-selection.md` and `paper-writing-assistant/references/exemplar-index.md` when venue/topic style or exemplar patterns matter.
- Read or update `paper/.agent/writing-memory/` through `paper-writing-memory-manager` when the contract changes section order, paragraph roles, claim strength, style rules, or forbidden claims.
- Read `paper-positioning-planner` outputs when present, such as positioning reports, claim decisions, or narrative architecture.

## Core Principles

- A writing contract is a constraint file, not a prose draft.
- Choose one primary archetype and at most one secondary archetype.
- Every main claim needs a section location, evidence slot, and allowed wording strength.
- Every section needs a job. Every important paragraph needs a role.
- Every main figure/table needs a paper job before captions are polished.
- Missing evidence should become an explicit placeholder, action, narrowed claim, or forbidden claim.
- The contract should be compact enough to stay useful while drafting.
- Later writing should follow the contract unless new evidence changes the contract first.

## Step 1 - Gather Inputs

Find:

- paper root: `paper/`, current directory, or user-provided path
- existing `paper/.agent/writing-contract.md`
- paper draft files: `main.tex`, `paper.tex`, `sections/*.tex`
- project memory: `memory/claim-board.md`, `memory/evidence-board.md`, `memory/action-board.md`
- paper-local state: `paper/.agent/paper-evidence-board.md`, `paper/.agent/paper-status.md`, `paper/.agent/provisional-results.md`
- positioning reports, result reports, figure/table maps, reviewer risks, and literature notes

If the user provides only an idea, produce a draft contract and mark uncertain fields as `TBD` or `needs-decision`.

## Step 2 - Decide Contract Mode

Use one of:

- `create`: no contract exists or the paper is being repositioned
- `update`: revise an existing contract after new results, new venue, new claims, or draft changes
- `audit`: check whether a contract matches the current draft and evidence

If no mode is specified, default to `create` when no contract exists and `update` when one exists.

## Step 3 - Select Archetype and Structure

Read `references/contract-schema.md`.

Choose:

- primary archetype: method, theory-guided method, empirical study, benchmark/dataset, systems/tooling, analysis/diagnostic, application, negative result/limitation, or hybrid
- target venue and audience
- section order
- per-section job
- paragraph roles for introduction, method/setup, experiments/results, related work, and limitations

If the archetype is uncertain, write the competing options and the evidence needed to choose, but still pick a provisional primary archetype for the contract.

## Step 4 - Map Claims to Evidence Slots

For every main and secondary claim, record:

```markdown
- Claim ID:
- Claim wording:
- Allowed strength:
- Paper locations:
- Required evidence slots:
- Current evidence status:
- Missing evidence action:
- Forbidden overclaim:
```

Use evidence slot statuses: `filled`, `user-stated`, `planned`, `running`, `provisional`, `missing`, `contradicted`, or `not-needed`.

If an evidence slot is a blocker for the selected archetype, mark the corresponding claim as blocked or narrowed.

## Step 5 - Define Writing Rules

Specify:

- title direction
- abstract moves
- intro paragraph recipe
- main figure/table roles
- result section order
- related-work boundary
- limitation policy
- provisional result policy
- allowed tone and forbidden tone
- terms, method names, dataset names, and baseline names to use consistently
- exemplar patterns to borrow, if any

Do not include long exemplar quotes.

## Step 6 - Write or Update Contract

Use `templates/writing-contract.md`.

Save to:

```text
paper/.agent/writing-contract.md
```

If there is no `paper/` directory and the current directory is the paper repo, save to:

```text
.agent/writing-contract.md
```

When updating, preserve useful stable decisions and add a compact change note instead of rewriting history.

## Step 7 - Route Follow-Ups

Route unresolved items:

- `paper-writing-assistant`: write or revise sections under the contract
- `paper-writing-memory-manager`: initialize or update writing memory after contract creation or revision
- `paper-evidence-board`: synchronize claim/evidence/action IDs
- `experiment-design-planner`: plan missing evidence slots
- `baseline-selection-audit`: defend required baselines
- `figure-results-review`: validate figure jobs and captions
- `table-results-review`: validate table jobs and provenance
- `paper-positioning-planner`: revisit primary archetype or claim scope
- `paper-reviewer-simulator`: stress-test the contract before full drafting

## Final Sanity Check

Before finalizing:

- one primary archetype is selected
- section order and paragraph roles are explicit
- main claims have evidence slots and allowed strength
- missing blocker evidence creates actions or narrowed claims
- figure/table jobs are defined before prose polishing
- related-work and limitation boundaries are explicit
- unsupported claims and forbidden tones are listed
- output path and next writing action are clear
