---
name: appendix-organizer
description: Plan and write appendix or supplementary material for ML papers. Use when the appendix needs to be structured, main-paper claim boundaries need to be enforced, NeurIPS/ICLR reproducibility checklists need sections, or cross-references between paper and supplement need to be aligned.
argument-hint: "[paper-dir] [--venue <venue>] [--mode plan|draft|audit|checklist]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Appendix Organizer

Structure and write supplementary material so it supports the main paper without duplicating it. A well-organized appendix proves reproducibility, satisfies checklists, and handles reviewer questions without weakening the main paper's argument.

Use this skill when:

- the main paper is drafting or nearly complete and appendix structure needs to be decided
- a venue checklist (NeurIPS, ICLR, ICML) requires specific supplementary sections
- appendix sections have grown organically and need consistent cross-reference structure
- reviewer questions about implementation details, full ablations, or additional results need structured homes
- main-paper claims and appendix claims need boundary enforcement to avoid scope creep

Do not use this skill to write main paper sections — use `paper-writing-assistant`. Do not use this skill to plan main paper structure — use `paper-writing-contract-planner`.

Pair this skill with:

- `paper-writing-contract-planner` to ensure appendix scope is consistent with the main paper's writing contract
- `paper-writing-assistant` to draft prose for appendix sections after structure is decided
- `paper-reviewer-simulator` to anticipate which appendix sections reviewers will ask for
- `submit-paper` to verify the appendix is included and formatted correctly in the submission package
- `artifact-evaluation-prep` for artifact-evaluation appendix sections and reproduction instructions

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    └── venue-checklists.md
```

## Progressive Loading

- Always read `references/venue-checklists.md` when the target venue has a mandatory checklist.
- Read `paper/.agent/writing-contract.md` when it exists.
- Read `paper/.agent/paper-evidence-board.md` to identify which evidence needs appendix homes.
- Read the main paper draft when auditing boundary alignment.

## Core Principles

- Appendix sections exist to prove claims and satisfy checklist requirements, not to dump everything that did not fit.
- Every appendix section must have a clear job: proof, ablation, implementation detail, reproducibility record, or checklist item.
- The main paper must be self-contained and readable without the appendix.
- Cross-references should go from main → appendix, not appendix → main (supplementary material does not require the main paper to reference back).
- Reviewer simulation should inform what goes in the appendix: what questions will reviewers ask?
- Appendix figures and tables need captions as carefully as main-paper ones.

## Step 1 — Gather Context

Find:

- paper draft: `paper/main.tex`, `paper/paper.tex`, or `paper/sections/`
- existing appendix: `paper/appendix.tex`, `paper/sections/appendix/`, or `\appendix` in the main file
- writing contract: `paper/.agent/writing-contract.md`
- evidence board: `paper/.agent/paper-evidence-board.md`
- venue: from writing contract or user argument

Record:

- target venue and its checklist requirements
- which main-paper sections already have appendix cross-references
- which claims have evidence that was deferred to the supplement
- which ablations were run but not included in the main paper

## Step 2 — Select Mode

- `plan`: design the appendix structure from scratch or from a partial draft
- `draft`: write one or more appendix sections after structure is decided
- `audit`: check existing appendix for boundary violations, missing sections, and broken cross-references
- `checklist`: fill in or verify a venue-specific reproducibility/ethics checklist

## Step 3 — Design Appendix Structure

Read `references/venue-checklists.md` for the target venue.

For each appendix section, record:

```markdown
Section: <letter/title>
Job: proof / ablation / implementation-detail / additional-results / reproducibility / checklist / ethics
Main-paper claim it supports: <CLM-XXX or section reference>
Content summary: <1-2 sentences>
Status: planned / drafted / complete / deferred
Cross-reference in main paper: <section and line/paragraph>
```

Standard appendix section types for ML papers:

- **Proofs**: formal proofs of claims or theorems stated in the main paper
- **Implementation details**: architecture hyperparameters, training schedules, optimizer configs, hardware
- **Additional ablations**: variants that support the main result but would clutter the paper
- **Additional results**: more datasets, longer training, extra baselines, per-class breakdown
- **Dataset details**: data sources, statistics, preprocessing steps, license info
- **Reproducibility statement**: seeds, code, compute cost, expected variance
- **Broader impact / limitations**: required by some venues even if not in main paper
- **Checklist sections**: NeurIPS reproducibility, ICLR checklist, artifact evaluation

## Step 4 — Enforce Claim Boundaries

For each appendix section, check:

- Does the appendix section make a claim that is stronger than the main paper's claim? If so, align the wording or move the claim to the main paper.
- Does the appendix introduce a new method or contribution not in the main paper? Flag for review — this is usually a scope problem.
- Are all cross-references from the main paper pointing to existing appendix sections? Fix broken references.
- Are appendix figures and tables cited in the main paper or in the appendix section that uses them?

## Step 5 — Fill Venue Checklist

Read `references/venue-checklists.md` for the target venue.

For each required checklist item, classify as:

- `yes`: satisfied with a pointer to where
- `no`: not applicable, with reason
- `partial`: needs work, with a specific action
- `na`: explicitly not applicable

Do not leave checklist items blank. Reviewers treat unanswered items as potential red flags.

## Step 6 — Write or Audit Appendix Sections

When drafting:

- Write each appendix section with a clear topic sentence that states its job.
- Use the same notation, terminology, and symbol conventions as the main paper.
- Refer back to the main paper section being supplemented at the start of each section.
- Captions for appendix figures/tables must be self-contained.

When auditing:

- Flag redundancy: content that repeats the main paper without adding proof, detail, or results.
- Flag scope creep: new claims or methods that belong in the main paper.
- Flag missing sections: evidence deferred to the appendix that has not been written.
- Flag broken cross-references.

## Memory Writeback

- Update `paper/.agent/paper-evidence-board.md` when appendix sections fill evidence slots
- Update `paper/.agent/writing-contract.md` if appendix scope changes the main paper's claim boundaries

## Final Sanity Check

Before finishing:

- every appendix section has a documented job and a main-paper connection
- venue checklist items are all answered
- no appendix section introduces a claim stronger than the main paper's allowed wording
- all main-paper `\appendix` cross-references point to actual sections
- appendix figures and tables have self-contained captions
