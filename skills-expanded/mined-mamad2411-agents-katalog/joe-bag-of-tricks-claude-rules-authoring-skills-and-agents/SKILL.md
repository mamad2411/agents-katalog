# Authoring Skills and Agents

Editing any `SKILL.md` or any file under a plugin's `agents/`? YOU MUST invoke
`/joe-bag-of-tricks:writing-skills` (for skills) or `/joe-bag-of-tricks:writing-agents` (for
agents) via the Skill tool BEFORE the first edit. This applies to a bead whose work touches those
files, not only to creating a new one.

The discipline has two halves. They cost very different amounts, and conflating them is how both
get skipped together.

**The authoring half** — frontmatter, descriptions written as capabilities and triggers rather
than workflow summaries, progressive disclosure, token discipline. Required for EVERY edit.

Within the authoring half, one review question applies to every line that tells an agent HOW to
work: is this a step the model will perform, or a cost it can route around? A step is a defect —
procedural phrasing measured worse than shipping no guidance at all. Protocol constraints (scope,
prohibitions, status vocabulary, report format) are exempt. See
`docs/decisions/goal-shaped-not-procedural-agent-instruction.md`.

**The testing half** — the Iron Law: establish a failing baseline BEFORE writing the fix, verify
the fix closes it, then close whatever new rationalization the fix opens. Required only where
behavior changes.

| Edit | Authoring half | Testing half |
|---|---|---|
| Typo, link, rewording, manifest row, cross-reference | required | no |
| New skill or agent | required | baseline first |
| Description rewrite aimed at triggering | required | not a subagent test; `skill-creator`'s eval loop is the instrument, and it gates nothing |
| **Behavior change — a new rule, bucket, gate, or escalation trigger, or a relaxation of one** | required | **required** |

`docs/adr/006-defer-behavioral-evals.md` defers a **plugin-wide eval harness**. It does not defer
testing the change in front of you, and "no TDD here" covers code test suites, not this
discipline. Neither is a reason to skip the testing half.

Full design: `docs/designs/authoring-workflow.md`.
