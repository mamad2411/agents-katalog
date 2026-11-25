---
name: skill-authoring
description: Creates, reviews and improves Claude skills (SKILL.md folders). Use whenever the user wants to write a new skill, turn a workflow or prompt into a reusable skill, fix a skill that does not trigger or behaves inconsistently, rewrite a skill description, add scripts or references to a skill, or check a skill against best practices, even if they only say "make this reusable". Scaffolds from a template and lints the result.
---

# skill-authoring

Turn a repeatable way of working into a skill that triggers at the right time, loads lean and produces consistent output.

```
skill-authoring/
├── SKILL.md
├── scripts/
│   ├── new_skill.sh          scaffold a skill and link it in the category README
│   └── lint_skill.py         check frontmatter, description, links, support files, template markers
├── references/
│   └── principles.md         loading levels, description craft, body and script rules, evaluation
└── templates/
    └── SKILL.template.md     skeleton with the standard sections
```

## When to use

- Creating a skill from scratch or from a conversation that worked well
- A skill never triggers, or triggers when it should not
- A skill gives different results each run
- A SKILL.md has grown too long or messy
- Reviewing a skill before publishing it

## Workflow

1. **Capture intent**: what should the skill do, which phrases should trigger it, what is the expected output, what is out of scope. If the conversation already contains a good workflow, extract it: tools used, order of steps, corrections the user made.
2. **Scaffold**: `bash scripts/new_skill.sh <category> <skill-name> "<one line summary>"` from the repository root. Names are lowercase with hyphens.
3. **Write the description first** (see `references/principles.md`): third person, what it does, when to use it, indirect triggers, boundaries with neighbouring skills.
4. **Write the body**: when to use, a numbered workflow with a verification step, rules with reasons, a "What to report back" table, related skills. Keep it under 500 lines.
5. **Bundle only what earns its place**: a script for exact or repeated work, a reference for detail needed sometimes, a template for output that must be consistent. Mention each file in the body and say when to use it.
6. **Lint**: `python3 scripts/lint_skill.py <category>/<skill-name>`. Fix errors, then warnings.
7. **Test on realistic prompts**: three that should trigger it and one that should not. Adjust the description if triggering fails, the body if behavior fails.
8. **Register**: add to the category README and, for a new category, the root README. Run `python3 scripts/validate_skills.py`.

## Rules

- The description decides triggering, so spend the most effort there
- Explain the reason behind a rule; shouting rules brittle and untestable
- Move detail out of the body into `references/`, and point to it with a clear condition
- Test scripts on a fixture, including a failure case, before shipping them
- Never ship a skill that sends data somewhere unexpected or hides side effects
- Keep one purpose per skill; split when the description needs "and also"
- Leave no unfilled template markers in a finished skill

## What to report back

| Field | Content |
|-------|---------|
| Skill | path and one line purpose |
| Trigger design | the description and the phrases it targets |
| Files | what is bundled and why |
| Lint result | clean, or what remains |
| Test prompts | the ones used, including a negative |

## Related skills

- `prompt-regression-testing`: keep the test prompts as a regression suite
- `multi-agent-orchestration`: when a skill coordinates several agents
- `commitsmith`: commit the new skill with a scoped message
