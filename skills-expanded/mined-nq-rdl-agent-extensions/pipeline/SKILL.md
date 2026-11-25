---
license: CC-BY-4.0
description: >-
  Design reproducible multi-step flows in Claude Code — decide between a single
  ordered skill, multiple step commands, hook-gated state, and when to escalate
  a step to subagents, an agent team, or a dynamic workflow. Use when the user
  wants a repeatable procedure (step 1 → 2 → 3), a "pipeline", enforced step
  ordering, a gated process where a later step must check an earlier one, or asks
  how to package a multi-step process as a plugin. Also triggers on "make this
  reproducible", "marker file", "state machine", "step 2 needs step 1", "fan
  out", or "skill vs command vs workflow". Picks the lightest structure that
  fits and shows the marker-file + hook gating pattern.
argument-hint: "Describe the multi-step process to make reproducible (e.g. 'lint, then test, then release')"
compatibility: >-
  Requires Claude Code v2.1.x with skills and commands unified. The hook `if`
  field requires v2.1.85+. Agent-team task dependencies require the
  experimental CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS flag. Dynamic workflows
  require v2.1.154+; plugin workflow distribution verified on v2.1.274. Hook
  output fields checked against the hooks docs with Claude Code 2.1.284 on
  2026-09-29.
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

## User Input

```text
$ARGUMENTS
```

When the user invokes `/claude-code:pipeline`, help them structure a repeatable
multi-step process for the task in `$ARGUMENTS`. If empty, ask what procedure
they want to make reproducible and whether step order must be *enforced* or just
*documented*.

Pick the **lightest** structure that fits — most pipelines are one skill, not a
plugin full of gated commands.

---

## Step 1 — Choose the structure

The core question: do steps just need to run **in order**, or must order be
**enforced** (a later step refuses until an earlier one is done)?

| Your need | Build | Notes |
|-----------|-------|-------|
| Steps are instructions Claude follows in sequence | **One skill** with an ordered procedure | The default. Simplest, reproducible, marketplace-shippable. |
| Each step is heavy (own context, own entry point) | **Multiple step commands** in one plugin (`thing:step-1`, `thing:step-2`) | Split *only* when a single skill would be too large or each step is invoked separately. |
| Order must be **enforced** | **Skill/commands + hooks + a marker file** | Claude Code has **no native step ordering** — you build it (Step 3). |
| Native ordered tasks, one session | **Agent team** (task list has dependencies) | A pending task can't be claimed until its deps complete. Experimental, in-session, not a package. |

> **Custom commands are skills now.** `.claude/commands/x.md` and
> `.claude/skills/x/SKILL.md` both create `/x`. So "a step" = a skill; a plugin
> just bundles several of them (plus MCP and hooks) under one namespace.

**Default recommendation:** one skill containing the ordered steps + a marker
file for state. Escalate to multiple commands only when each step is genuinely
complex. Escalate to hooks only when order must be *guaranteed*, not just
followed.

## Step 2 — Package as one plugin

A single plugin holds everything the pipeline needs:

```
plugins/thing/
  skills/run/SKILL.md     # the ordered procedure (steps 1→3)
  scripts/*.sh            # write/read .thing/ state markers
  skills/run/references/subagent.rst  # optional worker outline
  hooks/hooks.json        # the gate (Step 3)
  .mcp.json               # any MCP servers a step calls
```

The skill body drives the flow: it runs the bundled scripts to record progress
(`.thing/step-1.done`) and reads them to decide what's next. Link optional worker instructions under the skill’s `references/`. Read them
when delegation helps or the user requests a subagent; pass them to the host’s
available worker mechanism. This catalog does not register named agent types.

## Step 3 — Enforce order with a marker file + hook

There is **no built-in prerequisite graph** — hooks give you the *mechanism*
(block, read state, inject context); you supply the *state*. The pattern:

1. **Step 1 writes a marker** when it completes:
   ```bash
   mkdir -p .thing && touch .thing/step-1.done
   ```
2. **A hook reads it** before step 2's work runs. `PreToolUse` is the earliest
   tool-level block point; `UserPromptSubmit` gates the whole prompt earlier; `Stop` keeps the turn
   going until done. The hook inspects the filesystem and decides:
   ```bash
   #!/usr/bin/env bash
   # PreToolUse gate: block step-2 work until step-1 is done
   if [ ! -f .thing/step-1.done ]; then
     echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse",
       "permissionDecision":"deny",
       "permissionDecisionReason":"Run /thing:step-1 first."}}'
     exit 0
   fi
   exit 0
   ```
3. **Or just nudge** instead of hard-block: return `additionalContext`
   (`"step 1 is not done yet"`) so Claude self-corrects. Use `exit 2` + stderr,
   or `{"decision":"block","reason":...}` on events that support it
   (`UserPromptSubmit`, `PostToolUse`, `Stop`, …).

> For the full hook I/O contract (exit codes, per-event JSON shapes, the
> prompt-injection trap), use **`/claude-code:hook`** — don't re-derive it here.

## Step 4 — Decide how each step fans out

A skill *advises*; it does not *guarantee*. Bake the fan-out **strategy** into the
skill body, and choose the primitive by how much determinism you need:

| Per-step need | Use | Bake into the skill? |
|---------------|-----|----------------------|
| Offload one noisy side-task; only the summary matters | **Subagent** | ✅ Fully — link a `references/subagent.rst` outline from the skill; read it when delegating and pass it to a host-supported worker |
| A few workers that must talk/challenge each other | **Agent team** | ✅ Guidance only — the skill designs the team + spawn prompt (see `/claude-code:agent-teams`) |
| **Deterministic, large-scale** fan-out (same orchestration every run) | **Workflow** | Ship the JavaScript through the plugin manifest's `workflows` field; use `/claude-code:create-workflow` for authoring guidance |

The determinism ladder, in one line:

> **Skill** by default (steps + fan-out strategy) → add **hooks + markers** when
> order must be enforced → escalate a step to a **workflow** only when it needs
> *guaranteed* heavy fan-out. The skill holds the plan; hooks hold the gate;
> a workflow holds a step that must run the same way every time.

## Anti-patterns

- **A plugin of gated commands for a simple 3-step checklist.** Use one skill.
- **Expecting hooks to "know" step order.** They don't — without a marker file a
  hook has no idea what ran before.
- **Relying on a skill for *guaranteed* orchestration.** Skills are followed
  probabilistically; if a step *must* fan out identically every time, that step
  is a workflow.
- **Shipping an unregistered workflow script.** Claude Code 2.1.274 supports
  plugin `workflows/` discovery or explicit manifest `workflows` paths, alongside
  project/personal `.claude/workflows/`. In this catalog, keep JavaScript in the
  canonical skill's `scripts/` directory and register its installed path in
  `targets.claude.workflows`. Exclude Claude-only entrypoints from Codex.

---

## Verify against canonical source

Skill/command/hook/orchestration behavior shifts across versions. When being
wrong would mislead, verify against the canonical docs:
[skills & commands](https://code.claude.com/docs/en/skills),
[hooks](https://code.claude.com/docs/en/hooks),
[subagents](https://code.claude.com/docs/en/sub-agents),
[agent teams](https://code.claude.com/docs/en/agent-teams),
[workflows](https://code.claude.com/docs/en/workflows).
