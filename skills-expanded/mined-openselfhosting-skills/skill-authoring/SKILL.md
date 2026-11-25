---
name: skill-authoring
description: "Creates, improves, and evaluates portable Agent Skills that follow the open SKILL.md format and work across compatible coding agents. Use when drafting a new skill, reviewing skill quality, adding tests/evals, or preparing a skill for contribution."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Agent Skill Authoring

## Goal
Create a focused, portable skill that improves an agent's performance on a repeatable class of tasks. A skill is a workflow package, not a broad persona prompt or a substitute for unavailable tools.

## Design workflow
1. **Choose a real job.** Define the user problem, intended audience, trigger situations, expected output, and non-goals. Prefer one coherent task over an omnibus “do everything” skill.
2. **Check the repository and current standard.** Follow local authoring guidance and the current Agent Skills specification. Do not assume optional frontmatter fields work identically in every client.
3. **Write a useful description.** State what the skill does and when to use it; include natural task terms a user would say. Avoid vague claims like “improves productivity.”
4. **Write a deterministic workflow.** Include steps, decision points, evidence requirements, expected output, and finish criteria. Prefer concrete actions to motivational wording. Separate mandatory steps from recommendations.
5. **Add guardrails.** Identify destructive operations, external side effects, sensitive data, permission boundaries, and ways to avoid false claims. Do not instruct a client to bypass its safety or authorization requirements.
6. **Use progressive disclosure.** Keep core instructions focused. Put longer references, templates, and scripts in separate directories and link them with relative paths. Keep references shallow and easy to find.
7. **Keep it portable.** Use standard Markdown, generic shell/Python only when justified, and explain dependencies. Do not assume a vendor-specific tool exists. State fallback behavior if a tool or environment is unavailable.
8. **Create evaluations.** Add realistic prompts, expected behaviors, unacceptable behaviors, and relevant edge cases. Include at least one ambiguous or failure condition where appropriate. Evals are a review aid, not a guarantee of model behavior.
9. **Validate mechanically.** Check frontmatter, directory/name agreement, file paths, line length/size guidance, and evaluation schema. Execute bundled scripts only after reviewing their behavior.
10. **Review behavior manually.** Test the skill against representative tasks in at least one compatible agent; test more than one client before claiming broad interoperability. Compare outputs against the rubric and revise ambiguous instructions.
11. **Document limitations.** Explain prerequisites, side effects, privacy considerations, and what the skill cannot verify.

## Quality rubric (0–2 each)
- Focus and trigger precision.
- Clear sequence and decision points.
- Grounding in observable evidence.
- Safe behavior and permission boundaries.
- Useful output format and completion criteria.
- Portability and honest dependency handling.
- Evaluation quality and edge-case coverage.

A high score does not replace execution testing. Do not claim compatibility or effectiveness from a rubric score alone.

## Required handoff
Provide the skill's purpose, install command, prerequisites, test/evaluation results, known limits, and the exact files added or changed.

## Anti-patterns
Avoid vague all-purpose instructions, duplicated policies, hardcoded environment assumptions, unnecessary scripts, hidden network calls, broad filesystem edits, unverifiable success claims, and descriptions that trigger on nearly every task.
