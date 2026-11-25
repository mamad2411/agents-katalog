---
name: creating-agents-and-skills
description: Use when the user wants to create, add, extend, or modify an agent, skill, or workflow in this kit (e.g. "create a skill for our dbt naming standard", "add an agent for X", "new workflow"). Decides whether to build an agent, a skill, or nothing, enforces lean quality standards, and keeps every installed AI-tool folder (.agent, .claude, .github, .opencode, .cursor, AGENTS.md) identical in each tool's native format.
---

# Skill: creating-agents-and-skills

The governance gate for extending this kit. Goal: people add capabilities **only when they
help**, build them **with quality**, and every installed tool folder stays **in sync**.

Follow three phases in order: **Decide → Author → Propagate.**

---

## Phase 1 — Decide what (if anything) to build

Run these gates before creating anything. If a gate says stop, explain why and stop.

- **LLM-native? → don't create.** If a capable model already does this well ("write clean
  code", "use CTEs", "explain this function"), no artifact is needed. Just do the task.
- **Narrow knowledge / a tool / a format / a checklist / a script? → make a SKILL.** This is
  the default for almost everything: a team naming standard, a framework's rules, a validation
  procedure. Skills auto-activate by description and cost almost nothing until used.
- **A repeatable multi-step procedure the user invokes? → make a WORKFLOW** (slash command).
- **Overlaps an existing skill/agent? → extend it,** don't add a near-duplicate.

### The agent-survival rule

An **agent** is allowed only if it imposes something the model cannot impose on itself:

1. **Restricted tools** — a frontmatter `tools` list that removes capabilities (e.g. read-only).
2. **Independent review** — fresh context, without the author's reasoning.
3. **A different model** than the main session.
4. **An automatic trigger** that fires without the user asking.

If none applies, it is a skill: "a persona with a domain" is not a reason. Domain knowledge
belongs in a skill, or is dropped if the model already knows it. Agents must not hand off to
other agents.

> Default to a skill. Recommend an agent only if you can name which of the four criteria it
> satisfies, and say so in the agent's description or body.

---

## Phase 2 — Author it lean

Write only domain/org-specific signal. No filler, no restating what the model knows. English.

**Agent** — `.agent/agents/<name>.md` (example: `pbi-visual-reviewer`, a read-only reviewer):
```yaml
---
name: pbi-visual-reviewer
description: Independently reviews Power BI report screenshots against the request and the PBIR folder; PASS/FAIL per page and visual. Use after a report change has been reloaded and screenshotted.
tools: Read, Grep, Glob        # the restriction that justifies the agent: no Bash/Edit/Write
model: inherit
---
# PBI Visual Reviewer
<1–2 line identity> → fixed checklist → output format (PASS/FAIL). No handoffs.
```
`tools` is the field that matters: list only what the agent needs.

**Skill** — `.agent/skills/<name>/SKILL.md` (gerund-style name, e.g. `validating-dbt-models`):
```yaml
---
name: <name>
description: What it does AND when to use it, in the third person, with trigger words so it
  auto-activates (e.g. "Use when the user asks to ... "). This is the most important field.
---
# Skill: <name>
<when/why> → concrete rules or steps. Keep the body under ~500 lines; move long reference
material to sibling files (e.g. references/, scripts/) and link them.
```
Write descriptions in the **third person** ("Generates...", "Use when...") — never "I can help".
The description is what makes the skill fire without the user naming it.

**Workflow** — `.agent/workflows/<name>.md`: `description` frontmatter + concise numbered steps.

---

## Phase 3 — Propagate to every installed tool folder

A capability must exist, identically, in each AI tool the project uses — each in its native
format. Pick the path that matches the project:

### Path A — Source of truth present (`.agent/` + `scripts/sync_agents.py` exist)
This is the kit repo or an Antigravity install. **Author in `.agent/` only, then sync:**
```bash
python3 scripts/sync_agents.py          # regenerate
python3 scripts/sync_agents.py --check  # exits 1 if generated folders are stale (CI runs this)
```
The script regenerates `.claude/`, `.github/`, `.opencode/`, `.cursor/`, and root `AGENTS.md`
(which also covers OpenAI Codex). Never hand-edit those — they're overwritten. Done.

### Path B — No source of truth (user installed one or more tool flavors)
Detect which folders exist and write the artifact into **each present folder** in its native
format (the body content stays identical; only frontmatter changes). Format mapping:

| Concept | `.agent` (Antigravity) | `.claude` (Claude Code) | `.github` (Copilot) | `.opencode` (OpenCode) | `.cursor` (Cursor) |
|---|---|---|---|---|---|
| Agent | `agents/<n>.md` | `agents/<n>.md` (identical) | `agents/<n>.agent.md` — frontmatter `name`, `description`, `tools` mapped from Claude names (Read→`read`, Grep/Glob→`search`, Edit/Write→`edit`, Bash→`execute`) | `agents/<n>.md` — frontmatter `description`, `mode: subagent`, `permission` (deny edit/bash when the agent is read-only; drop `tools`/`model`/`name`/`skills`) | — (none; run the task in a fresh chat) |
| Skill | `skills/<n>/SKILL.md` | `skills/<n>/SKILL.md` (identical) | `skills/<n>/SKILL.md` (identical) | `skills/<n>/SKILL.md` (identical) | `skills/<n>/SKILL.md` (identical) |
| Workflow | `workflows/<n>.md` | `commands/<n>.md` (native slash command) + `workflows/<n>.md` | `prompts/<n>.prompt.md` — frontmatter `name`, `description`; body starts `**Context:** ${selection}` | `commands/<n>.md` (identical) | `commands/<n>.md` (identical) |
| Global rule | `rules/rules.md` (with `trigger: always_on`) | `CLAUDE.md` (rules + commands section) | `copilot-instructions.md` (rules) | root `AGENTS.md` (rules) | `rules/<n>.mdc` — frontmatter `description`, `globs`, `alwaysApply: true` |

Rules:
- **Strip the `trigger: always_on` frontmatter** from `rules.md` when writing it anywhere
  outside `.agent/` — it's Antigravity-only and is noise everywhere else.
- **OpenCode reads the root `AGENTS.md`**, not `.opencode/AGENTS.md` — don't create the latter.
  The same root `AGENTS.md` is what **OpenAI Codex** reads, so Codex needs no dedicated folder.
- Frontmatter differs per tool (Copilot agent/prompt, OpenCode agent, Cursor rule/mdc); the
  **body is a verbatim copy** everywhere.
- Create the same `<name>` in all present folders — do not leave a tool behind.
- If the user installed only one folder but wants multi-tool support, offer to add the others.

### Verify parity
After either path, confirm the artifact exists in every present tool folder and that no folder
references something that no longer exists. In Path A, `python3 scripts/sync_agents.py --check`
does this. State which folders you wrote.

---

## Anti-patterns
- Creating an agent for a persona, a single tool, or a single task (e.g. "GitAgent") — it fails
  the survival rule; write a skill.
- Chaining agents through handoffs.
- Putting episodic guidance in the always-on rules — it belongs in a skill like this one.
- Editing generated folders (`.claude`/`.github`/`.opencode`/`.cursor`/`AGENTS.md`) when `.agent/` exists.
