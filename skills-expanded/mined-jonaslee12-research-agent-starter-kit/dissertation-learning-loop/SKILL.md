---
name: dissertation-learning-loop
description: Use when dissertation work should convert new reading, source searches, LMS/module materials, supervisor resources, or discussion outcomes into durable project knowledge, literature-map updates, proposal implications, and next-reading questions without enabling unsupervised background automation.
---

# Dissertation Learning Loop

Use this skill when the agent needs to learn from newly read sources, websites, LMS content, supervisor or public resource material, supervisor feedback, proposal discussions, or user-confirmed decisions and carry that learning into later dissertation work.

## Purpose

Make the agent's learning task-triggered, source-grounded, and reusable. This is a local learning workflow, not autonomous background browsing.

## Core Rule

Every learned item must keep its evidence boundary:

- `CONFIRMED`: directly supported by a local file, LMS/module source, user-confirmed fact, or verified source.
- `LITERATURE-SUPPORTED`: supported by a screened academic source.
- `CONTEXTUAL`: useful for thinking, but not formal dissertation evidence.
- `INFERENCE`: the agent's synthesis or implication.
- `TO CONFIRM`: needs user, supervisor, LMS, or source verification.

## When To Use

Use for:

- literature search follow-up
- reading-list or source-note ingestion
- proposal/gap/methodology discussion where new decisions emerge
- supervisor feedback digestion
- updating Obsidian, source registers, or research-wiki after new evidence
- preparing the next research-search questions

Do not use for:

- raw participant data storage
- inventing citation details from memory
- automatic weekly searches unless a separate automation is explicitly created
- writing formal text before source-first and document-quality gates are applied

## Workflow

1. Identify the learning input:
   - source file, URL, LMS page, user-confirmed statement, supervisor note, or discussion result.
2. Classify the learning type:
   - literature concept
   - project decision
   - methodology implication
   - ethics/design boundary
   - writing-style preference
   - next-reading need
3. Extract only reusable knowledge:
   - key concept or claim
   - why it matters for this dissertation
   - what it can support
   - what it cannot support
   - next question it raises
4. Update the right layer:
   - `knowledge-base/SOURCE_REGISTER.md` for source status
   - `knowledge-base/sources/` for source notes
   - `research-wiki/LITERATURE_MAP.md` for clusters and gap logic
   - `research-wiki/METHOD_DECISIONS.md` for methodology decisions
   - `research-wiki/OPEN_QUESTIONS.md` for unresolved questions
   - Obsidian for navigation and thinking links
5. Record major learning events in `research-wiki/TASK_STATE.md` when they affect future work.

## Output Shape

```text
Learning captured:
- Source/input:
- Evidence status:
- Reusable point:
- Dissertation implication:
- Boundary:
- Files updated:
- Next reading/question:
```

## Guardrails

- Do not treat a skimmed or metadata-only source as full evidence.
- Do not store full copyrighted text or raw participant material in project knowledge layers.
- Do not let a useful idea become a formal claim without citation readiness.
- If the learning changes the dissertation route, mark the affected proposal/methodology decision clearly.
