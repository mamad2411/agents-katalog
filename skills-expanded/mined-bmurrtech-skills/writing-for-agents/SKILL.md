---
name: writing-for-agents
description: >
  Writing for agents: context pointers, hierarchy, completion criteria,
  leading words, guardrails, pruning. Use when authoring or editing skills, or
  any instructions meant to make agent behavior repeatable across LLMs.
disable-model-invocation: true
---

# writing-for-agents

Standalone guidance for writing what agents consume — especially skills — so
behaviour is repeatable across models. Packaging differs; writing does not:
same levers, same *process* every run (not the same output).

Owns the prose and structure bar. Does **not** create or maintain ops manuals.

When the document is a **skill**, also read [references/mechanics.md](references/mechanics.md)
(frontmatter, invocation, routers, must-pass checklist). Workflow shape options:
[references/patterns.md](references/patterns.md). Packaging/runtime failures:
[references/troubleshooting.md](references/troubleshooting.md). Behavioral
suites (triggering / functional / baseline): **`tdd`**
`references/skill-testing.md`.

## Workflow

### 1. Lock intent

One-sentence purpose; 2–3 user asks → expected agent behavior. Name the document
type (skill / instruction doc / pointer-reached doc).

**Done when:** purpose + examples + type are written.

### 2. Load the levers

Read [references/levers.md](references/levers.md). Apply every named lever to the
draft (or blank): context pointer, two loads, information hierarchy, completion
criteria, when-to-split, leading words, negative-imperative guardrails, pruning.

If writing a skill: also score [references/mechanics.md](references/mechanics.md).

**Done when:** every lever checked; fails fixed or waived with reason.

### 3. Place on the ladder

Inline what every branch needs. Disclose branch-only / long reference under
`references/` (or a sibling pointer) with **when-to-read** links. Co-locate each
concept. Cut sprawl via the ladder, not by deleting live levers.

**Done when:** body has no always-irrelevant branches; every hop is named from a
step or always-needed rule.

### 4. Validate (skills only)

If this repo has a skill validator (e.g. `scripts/quick_validate.py`), run it on
the skill folder. Soft-skip when no validator is present — this skill must work
standalone in any consumer.

```bash
python3 scripts/quick_validate.py skills/<name>   # when present
```

Then run skill TDD under **`tdd`** for the examples from step 1: triggering
(should / should-not), at least one functional slice, and baseline comparison
when you claim improvement. Soft-skip programmatic evals when no harness
exists — manual or scripted probes still count.

Skip structural + behavioral skill checks for plain instruction docs outside a
skill folder.

**Done when:** exit 0 (or soft-skip); description/pointer alone would route the
examples from step 1; agreed skill scenarios pass at the chosen rigor.
