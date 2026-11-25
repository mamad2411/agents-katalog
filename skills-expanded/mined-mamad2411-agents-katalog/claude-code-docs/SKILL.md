---
name: claude-code-docs
description: "Knowledge base from the official Claude Code documentation (Anthropic, code.claude.com/docs) on the four extension mechanisms: memory (CLAUDE.md, .claude/rules, AGENTS.md, auto memory), skills (SKILL.md, frontmatter, invocation control, dynamic context, context: fork), subagents (scope, tools, models, forks, resume) and hooks (events, matchers, exit codes, JSON decisions, prompt/agent/HTTP hooks). Use when writing or debugging a CLAUDE.md, skill, subagent or hook, choosing between them, or studying/referencing the docs."
---

<!-- argument-hint: [topic, field/event name, or chapter number] -->

# Claude Code Docs — Memory, Skills, Subagents, Hooks
**Author**: Anthropic (official Claude Code docs: memory, skills, sub-agents, hooks-guide) | **Source**: 4 pages, ~45k words | **Chapters**: 16 | **Generated**: 2026-10-13

## How to Use This Skill

- **No arguments**: load the core rules below.
- **A topic, field or event** (`context: fork`, `PreToolUse`, `claudeMdExcludes`): find it in the Topic Index and read that chapter before answering.
- **A chapter** (`ch15`): load that file. **Browse**: "what chapters do you have?"

Chapters carry field tables, exact config/JSON snippets and a worked example. For an exact field name, default, limit or exit-code rule, read the chapter instead of answering from memory: these docs change often, and a misspelled frontmatter key fails silently. For the decision table "which mechanism?", start with [cheatsheet.md](cheatsheet.md).

---

## Core Frameworks & Mental Models

### 1. Pick the mechanism by cost and guarantee
- **CLAUDE.md** = always-loaded context. **Skill** = a procedure that loads on demand. **Subagent** = isolated context that returns a summary. **Hook** = deterministic code at a lifecycle event.
- Instructions (CLAUDE.md, skills, subagent prompts) are **advisory**. Anything that *must* hold goes in a hook or a permission rule (**Advice + Lock**). A hook `deny` holds even in `bypassPermissions`. Hooks only tighten permissions and never loosen past deny rules. (ch01, ch16)
- Move a CLAUDE.md section into a skill once it becomes a multi-step procedure, because a skill body costs context only when invoked. Move noisy work (tests, logs, wide searches) into a subagent. (ch05, ch12)

### 2. Memory: what loads, when (ch01–ch04)
- CLAUDE.md files **concatenate**, nothing overrides: managed policy first, then user (`~/.claude/CLAUDE.md`), then project files from the repo root down to cwd. In each directory `CLAUDE.local.md` comes after `CLAUDE.md`. Subdirectory CLAUDE.md files load **on demand** when Claude touches files there.
- `@path` imports load **at launch** (relative to the importing file, 4 hops max), so they don't save context. To save context, use `.claude/rules/*.md` with `paths:` globs, which load only when a matching file is read or edited.
- Keep each CLAUDE.md **under 200 lines** of concrete, verifiable instructions ("run `npm test` before committing", not "test well"). Check what actually loaded with `/context` → Memory files.
- **AGENTS.md** is read natively only when no CLAUDE.md, `.claude/CLAUDE.md` or `CLAUDE.local.md` is on the path (default `claude-md-or-agents-md`). Adding a CLAUDE.md silently drops it, so put `@AGENTS.md` inside your CLAUDE.md. (ch03)
- **Auto memory** lives in `~/.claude/projects/<project>/memory/`, one per repo, shared across worktrees and local to the machine. Only the first **200 lines / 25KB** of `MEMORY.md` load, so keep it as an index and put detail in topic files. Turn it off with `autoMemoryEnabled: false`. (ch04)
- After `/compact`, only the project-root CLAUDE.md is re-injected right away. Rules given only in chat are lost, so write durable ones down. (ch04)
- Org-wide: managed CLAUDE.md or `claudeMd` in managed settings loads first and cannot be excluded. Developers skip noisy files with `claudeMdExcludes`, which takes absolute-path globs. (ch03)

### 3. Skills: description, invocation, lifecycle (ch05–ch09)
- A skill is `<dir>/SKILL.md` in `~/.claude/skills/` (personal), `.claude/skills/` (project) or a plugin. Name clashes resolve enterprise > personal > project, and a skill beats a `.claude/commands/` file. Personal skills don't load in cloud sessions or routines. (ch05)
- **`description` is the only thing Claude matches against.** Put the trigger use case first, because `description` + `when_to_use` is truncated at **1,536 chars**. All descriptions share a listing budget of **1%** of the context window (`skillListingBudgetFraction`), and the least-invoked are dropped first. (ch06, ch09)
- Invocation control: `disable-model-invocation: true` = **user-only** (use it for deploy, commit or send). `user-invocable: false` = **Claude-only** background knowledge. `allowed-tools` **pre-approves for one turn** and restricts nothing. (ch07)
- Lifecycle: the rendered body **stays in the conversation and is never re-read**. After compaction each skill keeps its first **5,000 tokens** (25,000 total), so put standing rules at the top. (ch07)
- Arguments: `$ARGUMENTS`, `$ARGUMENTS[N]` / `$N`, or named `$name` declared in `arguments`. Use `${CLAUDE_SKILL_DIR}` to reference bundled scripts. Keep `SKILL.md` under 500 lines and link supporting files (progressive disclosure). (ch06, ch07)
- **Dynamic context** with `` !`cmd` `` runs *before* Claude sees the skill. A failure or an unapproved command **aborts the invocation**, so pair it with `allowed-tools` and append `|| true` to checks that exit 1. (ch08)
- `context: fork` (+ `agent:`) runs the body as a fresh subagent with **no chat history**, in the background by default. Restrict access with `Skill(name *)` permission rules and `skillOverrides` (`on`/`name-only`/`user-invocable-only`/`off`). Find unused skills with `/skill-doctor`. (ch08)
- Misspelled frontmatter keys are ignored silently. Validate with `claude plugin validate`, debug with `--debug`, and evaluate against a **skill-off baseline** in fresh sessions. (ch06, ch09)

### 4. Subagents: isolation and its price (ch10–ch13)
- A subagent is Markdown + YAML (`name` and `description` are required, keys are camelCase) in `.claude/agents/` or `~/.claude/agents/`. Name clashes resolve **Managed > `--agents` > project > user > plugin**. Plugin subagents ignore `hooks`, `mcpServers` and `permissionMode`. (ch10)
- **`description` drives automatic delegation.** Say *when* to use the subagent ("use proactively after code changes"). Combined custom descriptions above **15,000 tokens** trigger a warning. (ch10)
- A non-fork subagent starts **cold**: its own system prompt + the delegation message + CLAUDE.md (Explore and Plan skip it) + git status + preloaded `skills`. Restate every rule it needs in the brief. (ch12)
- Tools: the `tools` allowlist after the `disallowedTools` denylist. A `disallowedTools` entry with a specifier removes the **whole** tool, so block single commands with `permissions.deny: Bash(git push *)`. Define single-agent MCP servers inline in `mcpServers` to keep their tool descriptions out of the main context. (ch11)
- Model order: **per-call > frontmatter `model` > `CLAUDE_CODE_SUBAGENT_MODEL` > main model** (`_FORCE=1` makes the env var win). A parent in `bypassPermissions`/`acceptEdits`/`auto` overrides the subagent's `permissionMode`. (ch11)
- Execution: in interactive fork mode subagents run in the background. Limits are depth **3** and **20** concurrent. **Resume** with `SendMessage` to keep history (Explore and Plan cannot be resumed). Agent messages never count as user approval. (ch12)
- **Fork** (`/subtask`) inherits history, tools, model and the **prompt cache**, and returns only its result. Choose a defined subagent when you need different tools, a different model or a clean context. (ch13)

### 5. Hooks: exit codes, JSON, precedence (ch14–ch16)
- Config shape: `hooks.<Event>[] → { matcher, hooks: [{ type, command, if, timeout }] }` in user, project, local or managed settings, plugins, or skill/agent frontmatter. Confirm it with `/hooks`. (ch14, ch15)
- **Exit 0 = no objection, not approval. Exit 2 = block**, with the reason on stderr. Any other code is a non-blocking error. Use **either** exit codes **or** JSON in a hook, never both. JSON event fields must sit inside `hookSpecificOutput`, because top-level placement is ignored silently. (ch15)
- All matching hooks run **in parallel to completion**, and for `PreToolUse` the most restrictive wins: **`deny` > `defer` > `ask` > `allow`**. `additionalContext` concatenates. For `updatedInput`, the last hook to finish wins. (ch15)
- The matcher tests something different per event (tool name, `SessionStart` source such as `compact`, notification type, filename). The `if` field (`Bash(git *)`) works only on tool events and **fails open**, so use permission rules for hard limits. (ch15)
- Types: `command` (default, 10 min timeout) for deterministic logic, `prompt` (30 s, `{ok, reason}`) for judgment from the input alone, `agent` (60 s, 50 turns, experimental) when the hook must inspect the repo, `http` for external policy. (ch16)
- Every blocking Stop hook needs a **`stop_hook_active`** guard (cap: 8 consecutive blocks). Valid JSON with no effect usually means a shell-profile `echo` printed before the `{`. (ch16)

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-claude-md-fundamentals.md) | CLAUDE.md Fundamentals | CLAUDE.md vs auto memory, locations, verifiable-instruction rule, 200-line target |
| [ch02](chapters/ch02-claude-md-loading-imports-rules.md) | CLAUDE.md Loading, Imports, `.claude/rules/` | Concatenation load order, `@path` imports, path-scoped rules |
| [ch03](chapters/ch03-large-teams-and-agents-md.md) | Large Teams, Managed CLAUDE.md, AGENTS.md | Settings enforce / CLAUDE.md guides, `claudeMdExcludes`, `@AGENTS.md` |
| [ch04](chapters/ch04-auto-memory-and-troubleshooting.md) | Auto Memory, `/memory`, Troubleshooting | Memory types, `MEMORY.md` index + topic files, debug ladder, `/compact` survival |
| [ch05](chapters/ch05-skills-bundled-and-first-skill.md) | Skills: Bundled, First Skill, Locations | Skill vs CLAUDE.md, location ladder, name-collision resolution |
| [ch06](chapters/ch06-skill-content-and-frontmatter.md) | Skill Content & Frontmatter Reference | Reference vs task content, full frontmatter table, progressive disclosure |
| [ch07](chapters/ch07-skill-invocation-lifecycle-arguments.md) | Skill Invocation, Lifecycle, Arguments | Invocation matrix, standing instructions, turn-scoped `allowed-tools`, `$ARGUMENTS` |
| [ch08](chapters/ch08-skills-advanced-patterns.md) | Advanced Skill Patterns | `` !`cmd` `` injection, `context: fork`, `Skill()` rules, `skillOverrides` |
| [ch09](chapters/ch09-skills-evaluate-share-troubleshoot.md) | Evaluate, Share, Troubleshoot Skills | Baseline eval, `claude plugin eval`, listing budget, drift triage |
| [ch10](chapters/ch10-subagents-builtin-and-scope.md) | Subagents: Built-ins, Scope, Files | Description-driven delegation, scope precedence, full frontmatter table |
| [ch11](chapters/ch11-subagent-models-capabilities-hooks.md) | Subagent Models, Capabilities, Hooks | Model resolution order, tool filters, `permissionMode`, `memory`, frontmatter hooks |
| [ch12](chapters/ch12-working-with-subagents.md) | Working with Subagents | Invocation ladder, fg/bg, depth & concurrency limits, `SendMessage` resume |
| [ch13](chapters/ch13-forks-and-example-subagents.md) | Forks and Example Subagents | Fork vs fresh subagent, `/subtask`, prompt rule + hook backstop |
| [ch14](chapters/ch14-hooks-first-hook-and-recipes.md) | Hooks: First Hook and Recipes | Deterministic automation, config shape, notify/format/protect/re-inject recipes |
| [ch15](chapters/ch15-how-hooks-work.md) | How Hooks Work | Exit codes vs JSON, `deny>defer>ask>allow`, matchers + `if`, locations |
| [ch16](chapters/ch16-hook-types-and-troubleshooting.md) | Hook Types, Limitations, Troubleshooting | prompt/agent/HTTP hooks, permission modes, `stop_hook_active`, triage |

## Topic Index

- **`@path` imports** → ch02
- **`additionalContext` / `updatedInput`** → ch15
- **AGENTS.md / Project instructions setting** → ch03, ch04
- **`agent` hooks / `prompt` hooks / `http` hooks** → ch16
- **`allowed-tools` (skills)** → ch07, ch08
- **`$ARGUMENTS` / `arguments` / `argument-hint`** → ch06, ch07
- **Auto memory / `MEMORY.md` / `autoMemoryEnabled`** → ch04
- **Built-in subagents (Explore, Plan, general-purpose)** → ch10
- **Bundled skills (`/doctor`, `/verify`, `/claude-api`)** → ch05
- **`CLAUDE_ENV_FILE` / `CwdChanged` / `FileChanged`** → ch14
- **CLAUDE.md locations & load order** → ch01, ch02
- **`claudeMd` / `claudeMdExcludes` / managed CLAUDE.md** → ch03
- **`/compact` survival** → ch04, ch07, ch14
- **`context: fork` / `agent:` (skills)** → ch08
- **Concurrent / depth limits** → ch12
- **`description` (skills)** → ch06, ch09
- **`description` (subagents) / automatic delegation** → ch10, ch12
- **`disable-model-invocation` / `user-invocable`** → ch07
- **`disallowedTools` / `tools` (subagents)** → ch11
- **Dynamic context injection (`` !`cmd` ``)** → ch08
- **Evals / skill-creator / `claude plugin eval`** → ch09
- **Exit codes (0 / 2 / other)** → ch15
- **Fork / `/subtask` / fork mode** → ch13
- **Frontmatter reference (skills)** → ch06
- **Frontmatter reference (subagents)** → ch10, ch11
- **`hookSpecificOutput` / `permissionDecision`** → ch15
- **Hook locations / `disableAllHooks` / `allowManagedHooksOnly`** → ch15, ch16
- **Hooks in skill/agent frontmatter** → ch11, ch06
- **`if` field / matchers** → ch15
- **`mcpServers` inline** → ch11
- **`memory` (subagent persistent memory)** → ch11
- **Model selection (`CLAUDE_CODE_SUBAGENT_MODEL`)** → ch11
- **`Notification` / `PermissionRequest` hooks** → ch14
- **`paths` (rules and skills)** → ch02, ch06
- **`permissionMode` / permission modes vs hooks** → ch11, ch16
- **`PreToolUse` / `PostToolUse` recipes** → ch14
- **`SendMessage` / resume subagents** → ch12
- **`SessionStart` matcher `compact`** → ch14
- **Skill content lifecycle / compaction budget** → ch07
- **Skill listing budget (`skillListingBudgetFraction`)** → ch09
- **Skill locations / name collisions** → ch05
- **`Skill()` permission rules / `skillOverrides` / `/skill-doctor`** → ch08
- **`Stop` hooks / `stop_hook_active` / block cap** → ch16
- **Subagent scope precedence / `--agents`** → ch10
- **Supporting files / `${CLAUDE_SKILL_DIR}`** → ch06
- **Troubleshooting: CLAUDE.md not followed** → ch04
- **Troubleshooting: hooks** → ch16
- **Troubleshooting: skills** → ch09

## Supporting Files

- [glossary.md](glossary.md): every key field, event and term, with chapter refs
- [patterns.md](patterns.md): Advice + Lock, path-scoped rules, forked tasks, guardrail hooks and more
- [cheatsheet.md](cheatsheet.md): "which mechanism?" table, precedence orders, thresholds, tells

---

## Scope & Limits

This skill covers four Claude Code doc pages: memory, skills, sub-agents and hooks-guide. It does not cover the hooks *reference* (full event schema), settings, MCP, plugins, permissions or the Agent SDK pages, so for those check the live docs index at https://code.claude.com/docs/llms.txt. Claude Code ships often, and version-gated behavior (noted as v2.1.x in chapters) may have moved since 2026-10-13.
