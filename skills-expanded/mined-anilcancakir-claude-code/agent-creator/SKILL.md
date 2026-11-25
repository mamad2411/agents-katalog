---
name: agent-creator
description: "Create or audit a Claude Code subagent: tools, model and effort, permissions, memory, isolation, and the system-prompt body."
when_to_use: "Use when writing, editing or debugging a subagent definition."
---

# Agent Creator

An agent is a markdown file: the frontmatter sets its tools, model and runtime; the body becomes its whole system prompt. The parent calls the Agent tool with `subagent_type`, a `prompt` and optional `description`, `model`, `effort`, `run_in_background` or `isolation`; the agent runs in a fresh context and only its final message returns to the parent.

Route the body's wording through `ac:prompt-writer` and its shape through the five-section pattern below.

## Rules that hold for every agent

1. **The body is the whole system prompt.** The main thread's persona, tone and Claude Code's built-in rules do not reach a subagent; every rule it follows lives in its body. CLAUDE.md does reach it unless `omitClaudeMd: true`.
2. **Context isolation is the value.** The parent sees only the final message, so the Output Format is a locked contract it can act on without follow-up.
3. **Minimal frontmatter.** `name` and `description` are required; add any other field only when you can name the condition.
4. **Decide nesting on purpose.** A denylist inherits the Agent tool and, on current Opus models, the agent will spawn children; an allowlist without `Agent` cannot.
5. **Plugin agents are restricted.** They ignore `permissionMode`, `hooks`, `mcpServers` and `initialPrompt`; an agent that needs them ships as a user or project agent.
6. **Plain wording, scope in both directions.** No caps; name what the agent does and where it stops.

## Decision flow

```
Is a custom subagent the right tool?
├── A built-in agent already fits → use it (on an `/ac:install` setup Explore and Plan are disabled; use `ac:explore` or `general-purpose`).
├── A repeatable procedure with no need for isolation → a skill, via `ac:skill-creator`.
├── A user-typed `/name [args]` workflow → a skill, via `ac:skill-creator`; a `context: fork` skill can run it in an agent.
├── Must happen deterministically → a hook, via `update-config`.
├── A standing fact → CLAUDE.md or a rule, via `ac:claude-md-rules-creator`.
└── Recurring work that benefits from its own context, tools or model → an agent. Continue.

Where does it live?
├── Project → `.claude/agents/<name>.md` (commit to share)
├── Personal → `~/.claude/agents/<name>.md`
├── Plugin → `<plugin>/agents/<name>.md`, addressed as `<plugin>:<name>`
├── Org-wide → managed directory
└── One run → the `--agents` JSON flag

Auditing an existing agent? → `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` first.
```

Same-name definitions resolve managed > `--agents` > project > user > plugin > built-in. `--add-dir` directories are not scanned for agents.

## Frontmatter

> **Escape convention.** This SKILL.md is preprocessed, so named tokens show `&#36;` for the dollar sign. In a plugin agent body, write a plain `$`.

| Field | Default | Semantics, and when to set it |
|-------|---------|-------------------------------|
| `name` | required | Lowercase and hyphens, at most 256 characters, no `:` |
| `description` | required | The delegation trigger the parent reads |
| `tools` | every parent tool | Allowlist; comma string or YAML list |
| `disallowedTools` | none | Denylist; applied to the inherited pool before `tools` filters it |
| `model` | `inherit` | `sonnet`, `opus`, `haiku`, `fable`, a full model id, or `inherit` |
| `effort` | session effort | `low`, `medium`, `high`, `xhigh`, `max`; the Agent tool's `effort` parameter overrides it |
| `permissionMode` | parent's | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | none | Positive integer cap on agentic turns |
| `autoCompactWindow` | inherited | Compaction threshold, 100000 to 1000000; only lowers the inherited window |
| `skills` | none | Full skill bodies injected at start; subagents do not inherit the parent's skills, and an unresolvable one is skipped with only a debug line; limits in the checklist |
| `mcpServers` | none | Servers scoped to the agent, inline or by name |
| `hooks` | none | Hooks active while the agent runs |
| `memory` | none | `user`, `project` or `local`: a persistent directory the agent reads and updates |
| `background` | `false` | `true` spawns it in the background by default |
| `omitClaudeMd` | `false` | `true` drops the CLAUDE.md hierarchy from its context |
| `isolation` | none | `worktree` runs it in a temporary git worktree |
| `color` | none | Display color in the task list |
| `initialPrompt` | none | First user turn when the agent runs as the main session (`--agent`) |
| `experimental.cacheTtl` | `5m` | `5m` or `1h` prompt-cache lifetime; `1h` for an agent that idles over five minutes between turns |

`requiredMcpServers` also parses. Every field's values and pitfalls: `${CLAUDE_SKILL_DIR}/references/frontmatter.md`. `claude --debug` names unknown fields with a typo hint.

## Tools and nesting

| Shape | Frontmatter | Use for |
|-------|-------------|---------|
| Allowlist | `tools: Read, Grep, Glob, Bash` | Focused agents; the default for read-only researchers |
| Denylist | `disallowedTools: Write, Edit, NotebookEdit` | "Anything except touching files" |

`tools: Agent(worker, researcher)` limits spawning to those types. Nesting reaches 3 levels by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) and at most 20 agents run concurrently. Where cost and order matter, keep chains orchestrator-driven: the agent returns a report naming the next agent and the parent spawns it.

An allowlist without `ToolSearch` ships deferred tools such as `LSP` inline instead of behind a search round-trip, so an agent whose body requires LSP belongs on an allowlist that names it. Detail and templates: `${CLAUDE_SKILL_DIR}/references/tool-restrictions.md`.

## Model and effort

- **haiku**: fast and cheap; search, lookup, classification. On Bedrock, Vertex, Foundry and Claude Platform on AWS it is Haiku 4.5, which takes no `effort`; omit the field there.
- **sonnet**: balanced; review, analysis, standard implementation.
- **opus**: deep reasoning; architecture, cross-file refactors, adversarial review.
- **fable**: the tier above Opus, for the hardest single-shot work.
- **inherit**: quality tracks the session.

Effort precedence, highest first: the `CLAUDE_CODE_EFFORT_LEVEL` environment variable, the Agent tool's `effort` parameter, the agent's `effort` field, the session effort. Set the field only when the agent needs a different level from the session; per-model calibration is in `ac:prompt-writer`.

## Permissions, memory, isolation

`permissionMode` works on user and project agents only; a parent running `bypassPermissions` or `acceptEdits` takes precedence, and a parent in `auto` makes it irrelevant. Most agents leave it unset and constrain capability through tools.

`memory: project` (or `user`, `local`) gives the agent a persistent directory; Read, Write and Edit are added to its tools, the start of its `MEMORY.md` is added to its system prompt, and the body must say when to update it.

`isolation: worktree` gives the agent its own checkout; use it for agents that must not touch the main checkout or that run in parallel. Detail on memory and skills: `${CLAUDE_SKILL_DIR}/references/memory-and-skills.md`.

## Body: the five-section pattern

- `## Identity`: one or two sentences, who the agent is and what it returns.
- `## Execution`: numbered steps; read first, then act; sub-numbers for parallel steps.
- `## Output Format`: the exact shape the parent parses (headers, citation format, length cap).
- `## Failure Conditions`: "FAILED if:" the quality-gate violations the agent checks itself against.
- `## Constraints`: scope limits, tool restrictions restated, evidence requirements.

Each section has a success criterion the agent can check. Plugin agent bodies get one substitution pass, `&#36;{CLAUDE_PLUGIN_ROOT}` and `&#36;{user_config.X}`; other agents get none. No agent gets argument substitution, the skill-directory token or shell injection. Depth and three worked structures: `${CLAUDE_SKILL_DIR}/references/system-prompt-structure.md`.

## Workflow

### 1. Capture intent

Ask what it does in one sentence, whether it reads or writes, which model fits, and the scope; ask about tool limits, memory, preloaded skills, permission mode or a worktree only when the answers imply them.

**Success criterion**: each optional field you will set has a named reason.

### 2. Write the frontmatter

Required: `name` (kebab-case) and `description`. Write `description` the way Claude Code writes its built-in agents: a role noun, one "Use this when" sentence, then what it returns, about 200 characters. Name a knob the caller sets in the brief, as the built-in Explore names its breadth levels. An agent only one caller spawns ends with "Spawned only by <caller>; not for general tasks." Skip "use proactively".

### 3. Write the body

The five sections, worded through `ac:prompt-writer`. Restate every rule the agent needs, including any CLAUDE.md rule it loses to `omitClaudeMd`.

### 4. Verify

Run the Pre-flight checklist below, and confirm the frontmatter parses with `claude --debug` reporting no unknown field, and that the description would make the parent delegate on a relevant request and not on a neighbouring one. Worked agents: `${CLAUDE_SKILL_DIR}/references/examples.md`.

### 5. Iterate

| Symptom | Fix |
|---------|-----|
| Never delegated to | Name the situation more exactly in "Use this when", or name the agent in CLAUDE.md for the work it owns |
| Delegated too eagerly | Remove broad words; say when not to use it |
| Does the wrong thing | Clearer Identity, explicit steps, locked Output Format |
| Writes files it should not | `disallowedTools: Write, Edit, NotebookEdit`, or an allowlist |
| Runs forever | `maxTurns` |
| Forgets across runs | `memory` plus an update instruction in the body |
| Re-discovers known patterns | Preload the domain skills through `skills:` |
| Spawns children unasked | An allowlist without `Agent`, or `Agent` in `disallowedTools` |
| A field seems ignored | `claude --debug`; on a plugin agent, rule 5 |

Deeper mapping: `${CLAUDE_SKILL_DIR}/references/anti-patterns.md`.

## Sibling skills

File scope, naming and listing budget go through `ac:skill-creator`; system-prompt wording through `ac:prompt-writer`; CLAUDE.md or `.claude/rules/<topic>.md` through `ac:claude-md-rules-creator`; PROJECT.md, ARCHITECTURE.md or DESIGN.md through `ac:project-md-writer`, `ac:architecture-md-writer` or `ac:design-md-writer`; a `/name` workflow that delegates to an agent through `ac:skill-creator` (user-typed skills); hook configuration through `update-config`.

## Built-in agents

Explore (read-only search), Plan (read-only architect), general-purpose (the fork default), claude-code-guide, statusline-setup. Case studies: `${CLAUDE_SKILL_DIR}/references/builtin-catalog.md`.

## Pre-flight checklist

- [ ] Right scope; filename equals `name` (at most 256 characters, no `:`).
- [ ] `description`: role noun, one "Use this when" sentence, what it returns, about 200 characters.
- [ ] Every optional field has a named reason.
- [ ] (`tools`) lists every tool the body calls; a read-only agent has no Write or Edit; `Agent` present only if nesting is wanted.
- [ ] (`skills`) each exists, none has `disable-model-invocation: true`, at most 32, plugin skills qualified.
- [ ] (`memory`) the body says when to update it.
- [ ] (Plugin agent) no `permissionMode`, `hooks`, `mcpServers` or `initialPrompt`.
- [ ] Body follows the five sections, restates every rule it needs, and its Output Format is locked and parseable.
- [ ] A fresh-session delegation returns the right shape.

## References

| File | Load when... |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/frontmatter.md` | Designing or auditing frontmatter: every field, precedence, plugin-agent restrictions, parsing pitfalls. |
| `${CLAUDE_SKILL_DIR}/references/system-prompt-structure.md` | Writing the body: the five sections in depth, three worked structures. |
| `${CLAUDE_SKILL_DIR}/references/tool-restrictions.md` | Allowlist or denylist, `Agent(x, y)`, conditional Bash through hooks. |
| `${CLAUDE_SKILL_DIR}/references/memory-and-skills.md` | Persistent memory or preloaded skills. |
| `${CLAUDE_SKILL_DIR}/references/builtin-catalog.md` | Case studies from the built-in agents. |
| `${CLAUDE_SKILL_DIR}/references/examples.md` | Worked agents to copy and adapt. |
| `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` | Diagnosing or auditing an agent. |
| `${CLAUDE_SKILL_DIR}/assets/AGENT.template.md` | Starting from a blank annotated template. |

Sibling skills are reached by invocation, not by path. Docs (append `.md` for raw markdown): subagents `https://code.claude.com/docs/en/sub-agents.md`, skills `https://code.claude.com/docs/en/skills.md`, plugins `https://code.claude.com/docs/en/plugins-reference.md`, permission modes `https://code.claude.com/docs/en/permission-modes.md`, hooks `https://code.claude.com/docs/en/hooks.md`. When the docs and the live binary disagree, trust the binary.
