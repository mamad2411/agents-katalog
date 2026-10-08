# Anbeeld's PROMPTING.md — AI Instruction Designer

A ruleset for writing text that an AI model is expected to act on: system and developer prompts, task prompts, repository instruction files, skills, agent profiles, tool descriptions, plans, memory and state documents, and more.

It treats prompting as configuration engineering. A clear sentence is not enough when the wrong source can override it, two routes match the same task, or a prohibition has no safe fallback. The ruleset was developed from external research on instruction design and model behavior, together with practical examples from multiple projects.

[![Support my work](https://anbeeld.com/images/support.jpg)](https://anbeeld.com/support)

## What it does

- Define the target configuration and observable behavior before drafting instructions.
- Separate authority, trust, requirements, defaults, guidelines, runtime facts, and explanatory text.
- Route neighboring tasks and modes with explicit overlap handling, no silent substitution, and a fallback for uncovered cases.
- Represent durable state, decisions, unknowns, lifecycle transitions, and handoffs explicitly.
- Match the control mechanism to the cost of failure, from natural-language guidance to schemas, permissions, validators, and human approval.
- Write decidable rules with clear actors, triggers, actions, scope, prerequisites, exceptions, and stopping conditions.
- Manage context, instruction density, representation, and compression without assuming that shorter or more formatted text is automatically better.
- Design tools, security boundaries, evaluation, revision, and pre-delivery audit as parts of the same prompt system.

## How to use it

### 1. Manually as direct instructions

Give [the ruleset](PROMPTING.md) to an AI and tell it to apply the rules while writing or reviewing your instruction artifact. You do not need to select sections manually; give it the complete file and let the relevant surface overlay govern the task.

One simple workflow that works well is to request the first complete draft, then ask the AI to run the required audit and revise any material findings.

### 2. As a skill in an agent harness

Use the packaged skill in [/skills/prompting](skills/prompting/) with tools that support skills: Claude Code, Codex, Cursor, OpenCode, and others. The skill is loaded on demand when the agent is doing AI-facing instruction work.

**Installation:** copy the complete [/skills/prompting](skills/prompting/) directory to your global skills folder:

- **Claude Code:** `~/.claude/skills/`
- **Codex:** `~/.codex/skills/`
- **Cursor:** `~/.cursor/skills/`
- **OpenCode:** `~/.config/opencode/skills/`

Keep the complete directory together so `prompting/SKILL.md` retains its `references/` directory.

## See also

- [Anbeeld's Global AGENTS.md / CLAUDE.md](https://github.com/Anbeeld/AGENTS.md)
- [Anbeeld's WRITING.md: AI Writing Rules](https://github.com/Anbeeld/WRITING.md)
- [Anbeeld's RESUME.md: AI Resume/CV Rules](https://github.com/Anbeeld/RESUME.md)

[![Support my work](https://anbeeld.com/images/support.jpg)](https://anbeeld.com/support)
