---
name: spec-discover
description: Create a lightweight project spec by identifying the decisions that must be made before implementation, without resolving them. Use as the first step in the spec-driven workflow to produce the initial spec for later exploration and fortification.
---

# Spec Discover

Use this skill for the discovery phase of the spec-driven workflow.

## Instructions

You are scoping a project spec. Your job is to identify the distinct decisions
that need to be made, not to make them.

The user will describe what they want to build after referencing this skill.
From their description, produce a spec file and save it to disk.

## File Convention

Save as: `specs.local/NNN_<topic-slug>.md` relative to the project root, where
NNN is the next available zero-padded index (`001`, `002`, `003`, etc.).

After saving the spec file, if the working directory is a Git repository,
configure local ignore rules for `specs.local` if not already configured:

- add `specs.local/` to `.git/info/exclude` so local specs are not committed
- add `!specs.local/` to `.ignore` so Codex can still reference those files with `@`
- add `.ignore` to `.git/info/exclude` if the file only contains the line above

## Spec File Format

```md
# Spec: <Short Title>

## Summary

<What we're building>

## Constraints

<Non-negotiable requirements extracted from user prompt and context>

## Decisions

| ID  | Decision | ✅  |
| --- | -------- | --- |
| D01 | <title>  |     |
| D02 | <title>  |     |

---

## Future Ideas

- <Explicitly deferred idea that is out of scope for the first implementation>

---

## D01: <Title>

<What needs answering before we can build this part>

## D02: <Title>

...
```

## Rules

- If there is no real tradeoff and the requirement is explicit and non-negotiable, it is a constraint.
- If a detail could plausibly be implemented in more than one valid way, it is a decision.
- If something is intentionally out of scope for the first implementation but worth remembering, put it in `Future Ideas`, not in `Constraints`.
- Suggested contracts, examples, and likely designs should be preserved as decision input when they inform an unresolved choice.
- Do not infer additional hard requirements from examples or suggested contracts beyond what is directly stated.
- Prefer narrower constraints plus broader decisions. Preserve ambiguity instead of resolving it, and preserve user-provided detail inside the relevant decision.
- Foundational decisions first. Call out dependencies in context paragraphs.
- Name likely options to frame the tradeoff, but do not recommend or commit to one.
- Keep `Future Ideas` lightweight. It is a parking lot for explicit deferments, not a second backlog of unresolved requirements.
- Before finalizing, audit each constraint: if it depends on interpretation rather than direct user intent, move it to `Decisions` and keep the motivating detail if it remains relevant.
