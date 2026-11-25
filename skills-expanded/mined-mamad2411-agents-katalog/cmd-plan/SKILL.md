---
name: cmd-plan
description: Command — Write a comprehensive implementation plan from an approved spec.
---

# /plan

Invokes `Skill(devkit:planning)` against an approved spec to produce a bite-sized implementation plan with file paths, code, tests, and commits.

Argument `[spec-path]` (optional): path to the spec doc to plan from. If omitted, looks for the most recent spec in `docs/specs/`.

After the plan is written and self-reviewed, run a calibrated review before the execution handoff: load `devkit_load_skill({ slug: "review-code" })` and run it with scope `plan <saved-plan-path>`, disposition their findings per `references/review-finding-disposition.md`, and apply every valid revision to the plan document. **Then** present the execution options. (The planning skill drives this step; on bb, native plan mode reaches the same review automatically through auto-review's plan gate.)

Output: a reviewed plan saved to `docs/plans/YYYY-MM-DD-<feature-name>.md` and a prompt to execute via `Skill(subagent-driven-development)` (recommended) or inline.

## Arguments

`[spec-path]`
