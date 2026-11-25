---
name: skill-creator
audience: team
description: >
  Create, modify, and audit AI agent skills in this toolkit. Use when scaffolding a new SKILL.md
  from the 5-section lean layout, revising an existing skill to fix structural defects, or
  scoring a skill against the 10-dimension rubric. Not for running a skill (invoke it directly)
  or creating an agent definition (use AGENTS.md conventions).
---

# Skill Creator

> "Precision in instructions is not pedantry — it is the difference between a tool that does what
> you intend and one that does what you said."
> -- adapted from Fred Brooks, "The Mythical Man-Month"

## Core Philosophy

A skill is a reusable, invocable instruction set for an AI agent. Its quality is measured by one
criterion: does it cause the agent to behave correctly, reliably, and without ambiguity? Beautiful
prose is worthless if the skill triggers on the wrong prompts, fails to stop when it should, or
produces inconsistent outputs. Full-template skills use the **5-section lean layout** — Core
Philosophy, Workflow, State Block, Output Template, Integration — and push all depth (principle
tables, discipline rules, anti-patterns, error recovery, code/report templates) to `references/`,
loaded just-in-time. Every always-loaded section is a per-invocation token tax.

**Non-Negotiable Constraints:**
1. TRIGGER-FIRST — a skill that does not trigger reliably is worthless; the description is the most important line in the file.
2. REFERENCES MANDATORY — every skill has a `references/` directory with ≥ 2 supporting files before it is complete.
3. NEVER RENAME STATE TAGS — changing a state block XML tag during revision is a silent breaking change for in-flight sessions.
4. 5-SECTION LEAN LAYOUT — SKILL.md keeps only the five sections (≤ 200 lines); depth goes to `references/`, never more inline sections.
5. AI-FIRST PHRASING — imperatives and explicit branches, never hedging or open-ended judgment calls.

Full principle table, discipline rules, anti-patterns, and error recovery live in
`references/conventions.md`.

## Workflow

```
Mode: CREATE — scaffold a new skill
  LOAD       Read a lean gold standard: skills/cargo-package-scaffold/SKILL.md (domain
             scaffolder) or skills/qraspi-skeleton/SKILL.md (phase driver). Note the 5-section
             structure, description format, and reference-pointer pattern.
  INTAKE     Ask: one-sentence purpose? trigger phrases? negative triggers (Do NOT use when)?
             how many workflow modes (1 simple, 2-3 multi-mode)?
  DRAFT      Write the 5 sections from references/skill-template.md. Fold Critical/High principles
             into Non-Negotiable Constraints. Create references/conventions.md (full principle
             table, WRONG/RIGHT discipline rules, anti-patterns, error recovery) + a templates
             reference. Leave stubs where content is unknown.
  DESCRIBE   Write the description LAST: ≤ 1024 chars, third person, sentence 1 = what it does,
             sentence 2 = "Use when…", plus a "Do NOT use when…" negative trigger.
  VERIFY     [ ] 5 sections present  [ ] description has a "Do NOT use when…" clause
             [ ] state block XML tag unique (grep skills/)  [ ] SKILL.md ≤ 200 lines
             [ ] references/ has ≥ 2 files, each named by a pointer in Output Template
             [ ] conventions.md has the 10-row principle table, ≥ 3 WRONG/RIGHT rules,
                 ≥ 8-row anti-patterns table, ≥ 3 error-recovery scenarios
  REPORT     Skill path, sections complete, line count, references count, issues found.

Mode: REVISE — fix an existing skill
  LOAD/PATCH Read the target + a gold standard; identify defects via the rubric. Patch minimally;
             never change the state block tag; move inline depth to references rather than deleting.
             Migrating a legacy 10-section skill: see the recovery steps in conventions.md.
  VERIFY     Run the CREATE checklist; confirm no regressions and the state tag is unchanged.
  REPORT     Revision diff summary (references/templates.md).

Mode: SCORE — audit against the rubric
  Load references/scoring-rubric.md; score each of 10 dimensions 1–5 with evidence; classify
  (≥45 EXEMPLARY · 35–44 PASS · 25–34 REVISE · <25 DEPRECATE); emit the scorecard (templates.md).
```

**Exit criteria:** CREATE — all 5 sections present, ≤ 200 lines, unique state tag, ≥ 2 references
with the depth offloaded, description with a negative trigger. REVISE — defects patched, no
regressions, state tag unchanged. SCORE — full scorecard with a verdict and severity-ranked issues.

## State Block

```
<skill-creator-state>
mode: create | revise | score
target_skill: [skills/<name>/SKILL.md or "new"]
sections_complete: [N]/5
line_count: [N]
references_count: [N]
state_tag_unique: true | false
last_action: [what was just done]
next_action: [what should happen next]
</skill-creator-state>
```

## Output Template

- **Blank 5-section skill scaffold + what goes in references/** — `references/skill-template.md`.
- **Revision diff summary, quality scorecard** — `references/templates.md`.
- **SCORE rubric (10 dimensions, 1–5 criteria, thresholds)** — `references/scoring-rubric.md`.
- **Principle table, discipline rules, anti-patterns, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `spec-coach` | For creating agent definitions, PRDs, or Spec Kit files, or any interactive spec design session — use it instead of this skill, which targets SKILL.md files. |
| `cargo-package-scaffold` / `qraspi-skeleton` | The lean gold standards. Read one before scaffolding or revising. |
| `automated-code-review` | Run after creating or revising a skill to quality-check the new content against project conventions. |
| `session-context` | Use at the start of a revision session to understand what changed in the skills suite since last time. |
