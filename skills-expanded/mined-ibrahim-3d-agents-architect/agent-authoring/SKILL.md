---
name: agent-authoring
description: Write or refactor Claude Code sub-agent definitions (files in agents/*.md). Use when the user asks to "create a subagent", "add an agent for X", "build a specialist agent", "make a research agent", "write an agent file", "agent YAML", "delegate to a subagent", "design a multi-agent workflow", or when a task needs a fresh context window, restricted tools, or isolation. Covers frontmatter (tools/model/effort/maxTurns/isolation), delegation patterns, read-only constraints, and orchestrator↔specialist contracts.
---

# Sub-Agent Authoring

Sub-agents run in a fresh context window with a restricted tool allowlist. Use them when:

- The task benefits from isolation (heavy file reading, research).
- You want deterministic tool scoping (read-only codebase analysis, no network).
- You need parallelism (spawn N agents concurrently).
- Context pressure in the orchestrator is high and you need to keep it lean.

**Do not** create a sub-agent for trivial work — the spawn cost (~1-3s, fresh context reload) exceeds benefit for tasks under ~5 tool calls.

## Frontmatter schema (Claude Code plugin agents)

```yaml
---
name: <kebab-case, matches filename>
description: What it does and when to invoke. Trigger-optimized like a skill description.
model: sonnet | opus | haiku    # optional, defaults to parent
effort: low | medium | high     # optional
maxTurns: 20                    # cap tool loops
tools: Read, Grep, Glob, Bash   # ALLOWLIST — omitting = inherit all
disallowedTools: Write, Edit    # alternative: blocklist
skills: [skill-a, skill-b]      # preload specific skills
memory: preserve | fresh        # context handling
background: true | false        # long-running background agent
isolation: worktree             # only valid value; copies repo to temp worktree
---
```

**Security**: `hooks`, `mcpServers`, and `permissionMode` are NOT allowed in plugin-shipped agents. Do not include them.

## Body structure (XML-tagged, like GSD convention)

```markdown
<role>
You are <specialist>. Spawned by <parent command/orchestrator>. You answer <single question> and produce <single artifact>.
</role>

<required_reading>
Files the orchestrator MUST pass via Read. List them.
</required_reading>

<responsibilities>
Bullet list, 3-7 items.
</responsibilities>

<constraints>
- Read-only / write-only / deterministic
- Never do X
- Always do Y
</constraints>

<output_contract>
Produce exactly: `<path>/<file>.md` with sections: ...
Exit with a 5-line summary for the orchestrator.
</output_contract>
```

## Design principles

1. **Single artifact**: each agent produces one canonical file (PATTERNS.md, RESEARCH.md, PLAN.md). Never have an agent update multiple cross-cutting files.
2. **Read-only by default**: specialists read and analyze; only `executor`-class agents write code. Enforce via `tools` allowlist.
3. **Tight tool allowlists**: research agent → `Read, Grep, Glob, WebFetch, WebSearch`. Code reviewer → `Read, Grep, Glob, Bash`. Never include `Write` unless the agent's job is to write.
4. **Explicit upstream contract**: agents list exactly which files/variables they need; orchestrators pass them. No implicit shared state.
5. **Exit summary**: 3-7 lines summarizing what was produced + key findings. Keeps orchestrator context lean.

## Orchestrator ↔ specialist pattern

The orchestrator (usually a slash command) routes. It:
1. Initializes state (reads configs, creates directories).
2. Spawns specialists via Task tool with `subagent_type` + prompt containing `<required_reading>` paths.
3. Aggregates their output files (reads frontmatter only, not full body — see context-management skill).
4. Makes the next routing decision.

The orchestrator NEVER does the specialist's work inline.

## References

- @../../agents-architect/references/agent-tool-allowlists.md — canonical tool sets per agent archetype
- @../../agents-architect/templates/agent.template.md
- @../../agents-architect/references/context-budget.md — how orchestrators read agent output without blowing context

## Output

Produce `agents/<name>.md` with correct frontmatter + structured body. Include a tool-allowlist justification comment for future auditors. Finish with a 3-line summary of the agent's niche.
