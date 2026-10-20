# Pre-built custom subagents

Drop these markdown files into your project's `.claude/agents/` directory and Claude Code will recognize them as project-scoped custom subagents. They appear in the `/agents` menu and via `@agent-<name>` mentions.

## Why this directory exists (correction to v5 messaging)

v5 emphasized "subagents do not inherit skills" — and that's true for ad-hoc subagents spawned via the `Agent` tool. But Claude Code's **file-based custom subagents** in `.claude/agents/<name>.md` support a `skills:` frontmatter field that **explicitly preloads named skills into the subagent's context at startup**.

Quoting the Claude Code docs:
> `skills` — Comma-separated list of skills to preload. Injects full skill content into the subagent's context at startup.

This is the structural fix for the v4/v5 briefing-discipline burden. Instead of pasting concern bundles inline in a worker briefing every time, define a custom subagent that preloads `production-readiness` and the relevant concern bundle. Then `@security-verifier` just works.

The agents in this directory are paste-ready examples for the four concern verifiers from `verify-rigorously` §Parallel-by-concern verification.

## Installation

```bash
# In your project root
mkdir -p .claude/agents
cp -r path/to/engineering-excellence-v6/engineering-excellence/agents/*.md .claude/agents/
```

These files are committed (team-shared knowledge). They will appear in `/agents` and via `@security-verifier`, `@performance-verifier`, etc.

## Usage

```
# In Claude Code:
@security-verifier review the diff in src/auth/
@performance-verifier audit the changes in src/api/orders/
@reliability-verifier check the new payment retry logic
@tests-verifier review the test coverage for the new endpoint
```

Or invoke automatically by description matching:
```
review this auth change for security issues
```
Claude Code will see `@security-verifier`'s description and route to it.

## What's in each frontmatter (and why)

```yaml
---
name: security-verifier               # @security-verifier and /agents listing
description: ...                      # Claude uses this to decide when to delegate
tools: Read, Grep, Glob              # READ-ONLY — verifiers don't edit
disallowedTools: Edit, Write, Bash   # belt-and-suspenders: even if Claude tries, blocked
model: sonnet                         # Sonnet for verification (cheaper than Opus)
skills: production-readiness          # PRELOADS the skill — this is the fix
maxTurns: 20                          # cost cap; verifiers don't need long sessions
permissionMode: default               # ask before any tool that requires permission
isolation: worktree                   # optional; isolated git worktree for safety
background: false                     # foreground; we want results before continuing
effort: medium                        # reasoning effort; medium for verification
color: red                            # UI hint; red = security/danger
memory: project                       # accumulate findings across sessions
---
```

**`tools` is critical.** Every verifier here is read-only (`Read`, `Grep`, `Glob`). They cannot edit code, run shell commands, or write files outside the mission artifacts directory. This is the structural enforcement of "audit workers report; they don't fix" from `verify-rigorously`.

**`skills` is the v6 unlock.** By naming the skills to preload, the verifier subagent has the discipline content in context without you pasting it inline. The custom subagent definitions below preload `production-readiness`, plus optionally `unbiased-development` for honest reporting.

**`maxTurns: 20` matters.** Verifiers should not loop indefinitely. A capped budget forces them to produce findings or report "no findings" promptly.

## Per-agent purpose

| Agent file | Specialty | Tools | Skills preloaded |
|---|---|---|---|
| `security-verifier.md` | OWASP-lens audit of diffs | `Read, Grep, Glob` | `production-readiness, unbiased-development` |
| `performance-verifier.md` | N+1, hot path, allocation review | `Read, Grep, Glob, Bash` | `production-readiness, unbiased-development` |
| `reliability-verifier.md` | Error/retry/idempotency review | `Read, Grep, Glob` | `production-readiness, unbiased-development` |
| `tests-verifier.md` | Test coverage and quality review | `Read, Grep, Glob, Bash` | `testing-discipline, verify-rigorously, unbiased-development` |

Bash is allowed for `performance-verifier` and `tests-verifier` to permit running EXPLAIN-equivalent / running the test suite in dry-run / checking for regressions. The `permissionMode: default` ensures any actual command execution still asks first.

## When to use these vs. spawning generic Agents

- **Use these custom subagents** when the work matches their specialty exactly (a focused security review, a performance audit). They preload the right skills, have the right tool restrictions, and produce consistent output.
- **Spawn a generic `Agent` worker** when the work is one-off (research a specific library, summarize a debugging session) and doesn't fit a recurring pattern.
- **Use the built-in `Explore` subagent** for fast, read-only codebase navigation. It's optimized for that and runs cheaper than a general-purpose subagent.

The mental model: custom subagents in this directory = recurring specialist roles. Ad-hoc `Agent` spawn = one-time worker. Built-in `Explore` / `Plan` = navigational scaffolding.

## See also

- `engineering-excellence/SKILL.md` §Multi-agent coordination — how this fits into the orchestration pattern.
- `engineering-excellence/briefings/worker-template.md` — for ad-hoc workers where you can't pre-define a custom subagent.
- `engineering-excellence/briefings/concern-bundles/` — the same checklist content these custom subagents preload via the `skills:` field (kept for ad-hoc fan-outs).
