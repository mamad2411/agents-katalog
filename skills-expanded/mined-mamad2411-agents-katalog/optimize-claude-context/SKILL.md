---
name: optimize-claude-context
description: >
  Manage a project's Claude Code context layer (CLAUDE.md, .claude/rules/,
  .claude/skills/) using the directive model. Three commands: handle-one-directive
  (add, update, or evaluate a single knowledge point — "I want Claude to know X",
  "add a rule", "这个要加进去", "帮 Claude 记住"), rebuild (reprocess all existing
  context from scratch — "rebuild", "重建", "start fresh"), audit (score the health
  of the current context layer — "audit", "health check", "评分", "what's wrong
  with my CLAUDE.md"). Also proactively suggest audit when noticing bloat or
  wrong-layer content — never modify files without explicit user confirmation.
---

# CRITICAL — Read first

- **Directive model.** Every piece of knowledge is a directive: one atomic, scoped
  knowledge point. Route each directive through the decision tree to exactly one layer.
- **Linter first.** If the toolchain can enforce it, graduate it — do not add it to
  any context file.
- **Multi-step procedure → Skill, always.** This overrides all other routing conditions.

# optimize-claude-context

## Scope

Three artifacts only:
- `./CLAUDE.md` — behavioral rules, every session
- `./.claude/rules/*.md` — path-scoped lookup/reference
- `./.claude/skills/*/SKILL.md` — semantically triggered workflows

Do not modify `~/.claude/` (global) files. Note existence of `AGENTS.md` or
`.cursorrules` but do not modify them.

## Dependencies

Check via filesystem before starting any workflow:

```bash
ls ~/.claude/skills/skill-creator/ 2>/dev/null || ls ~/.agents/skills/skill-creator/ 2>/dev/null
ls ~/.claude/skills/skill-surgeon/ 2>/dev/null || ls ~/.agents/skills/skill-surgeon/ 2>/dev/null
```

Fallback: check `available_skills` context if filesystem check finds nothing.

| Skill | When needed | Install |
|---|---|---|
| `skill-creator` | Writing a new skill body | `npx skills add anthropics/skills --skill skill-creator -g -y` |
| `skill-surgeon` | Updating an existing skill file | `npx skills add darian-deng/agent-skills --skill skill-surgeon -g -y` |
| `feature-dev` *(recommended)* | Code exploration during Step 4 enrichment and rebuild Phase 4 | Install as plugin |

If a required dependency is missing when you reach the point of needing it: stop,
explain why, give the install command, wait for confirmation.

## Intent routing

| Command | Signals | Reference |
|---|---|---|
| **handle-one-directive** | "add a directive", "I want Claude to know X", "update this rule", "change this skill", "evaluate this", "remove this rule", "delete this directive", "这个要加进去", "帮 Claude 记住", "这条删掉", "废弃这个", or called by any external workflow in pre-parsed mode | [references/handle-one-directive.md](references/handle-one-directive.md) |
| **assess-candidate** | called by Stage 4 implementer subagent after tests pass to assess a knowledge candidate; never called interactively by users | [references/assess-candidate.md](references/assess-candidate.md) |
| **rebuild** | "rebuild", "重建", "reprocess everything", "context layer 重写", "start fresh with directives" | [references/rebuild-workflow.md](references/rebuild-workflow.md) |
| **audit** | "audit", "health check", "评分", "score my context", "what's wrong with my CLAUDE.md", "how good is my context" | [references/audit-workflow.md](references/audit-workflow.md) |

**If ambiguous, ask one targeted question before acting.** Never guess intent.

**Proactive detection:** if you notice bloat, wrong-layer content, or
linter-enforceable rules while working on an unrelated task, briefly flag the issue
and ask whether to run audit. Never modify files without confirmation.

## Shared foundations

All three commands depend on:
- [references/directive.md](references/directive.md) — directive concept, scope, layers
- [references/decision-tree.md](references/decision-tree.md) — routing logic
- [references/linter-capabilities.md](references/linter-capabilities.md) — linter check methodology
- [references/writing-formats.md](references/writing-formats.md) — content specs per layer

`handle-one-directive.md` is also an internal dependency of rebuild (Phase 6
execution unit) — read it when executing rebuild Phase 6.

Read the relevant reference file before executing any command. Do not rely on
memory of the decision tree — always read from `decision-tree.md`.

## Output language

All output follows the user's language. Quoted content from existing files stays in
its original language; rationale and commentary use the user's language.
