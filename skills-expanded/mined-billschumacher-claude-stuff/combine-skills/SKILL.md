---
name: combine-skills
description: This skill is always used to determine which skills need to be combined to handle any task.
---

# Combine Skills

Before starting work on any non-trivial task, follow this procedure:

1. **List your available skills.** Look at every skill currently available in your environment, not just the ones you'd reach for by default.

2. **Match each skill against the task.** For every skill, ask: "Does this skill's description apply to anything I am about to do?" Be generous — if there's any meaningful overlap, the answer is yes.

3. **Invoke every matching skill.** Use the Skill tool to invoke each one. Do not stop after the first match. A task that involves writing Python code AND following a development workflow needs BOTH skills, not just one.

4. **Apply all guidance together.** When the skills have been invoked, treat their guidance as additive. If one skill says "write tests first" and another says "use type annotations", do both. Neither overrides the other.

## Why this matters

The default behavior is to invoke a single skill that seems most relevant and ignore the rest. This loses value: skills are designed to be composed. A coding task often needs guidance from multiple skills simultaneously — one for the language conventions, one for the workflow discipline, one for the domain.

## Example

Task: "Implement a Queue data structure with tests"

- `python-style` matches (writing Python)
- `dev-workflow` matches (implementing a feature with tests)

Wrong: invoke only `python-style` because Python is more salient.
Right: invoke BOTH `python-style` and `dev-workflow`, then apply guidance from each.

## When this skill does NOT apply

- Trivial single-line edits
- Pure questions where no work will be done
- Tasks where only one skill is even remotely relevant
