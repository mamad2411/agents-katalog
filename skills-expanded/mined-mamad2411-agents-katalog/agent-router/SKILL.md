---
name: agent-router
description: Decides which Codex subagent, OpenAI model and reasoning effort should handle a task before any work starts, so the coordinator spends the fewest tokens that still hold quality. Use this every time the user asks to implement, fix, refactor, test, review, investigate, document or plan anything, even when the task looks small (the router may answer "inline" for trivial work). Also use it when unsure whether to delegate at all or how many subagents to spawn.
---

# Agent router (OpenAI Codex edition)

The main thread is the scarce resource: everything it reads is re-billed on every
turn, and quality drops as it fills. Delegating to a subagent moves the verbose part
(file reads, test output, exploration) into a disposable context and returns a
summary. The two cost levers are the **model tier** and the **reasoning effort**
(`none` < `low` < `medium` < `high` < `xhigh` < `max`; Codex exposes
`minimal`..`xhigh` in config).

| Tier | Model id | Input $/1M | Output $/1M | Relative input cost |
| --- | --- | --- | --- | --- |
| GPT-5.6 Luna | `gpt-5.6-luna` | 0.20 | 1.20 | 1x |
| GPT-5.6 Terra | `gpt-5.6-terra` | 2.00 | 12.00 | 10x |
| GPT-5.6 Sol | `gpt-5.6-sol` | 4.00 (promo until at least 2026-11-21; list 5.00) | 20.00 (list 30.00) | 20x |
| GPT-6 Astra | `gpt-6-astra` | 10.00 | 50.00 | 50x |

Cached input is 10% of the input price on every tier, and all GPT-5.6 tiers default to
`medium` effort. OpenAI's guidance: `low` for tool use, planning and search; `high`
for hard debugging and deep planning in agentic loops; `xhigh` for long asynchronous
runs; `max` only when correctness beats cost. Details and URLs in
[references/sources.md](references/sources.md).

Effort and model are pinned per agent in `.codex/agents/<name>.toml`
(`model`, `model_reasoning_effort`), with fallbacks in the `[agents]` table of
`config.toml`. Pick from the project's agents. If the project does not have them yet,
copy the templates in [assets/agents/](assets/agents/) into `.codex/agents/` and fill
in the project-specific placeholders (`<...>`).

## Step 1: classify the task

| Tier | Signals |
| --- | --- |
| **inline** | Answerable from what is already in context; one-line edit; a git or shell command whose output is short. A subagent costs more than doing it. |
| **lookup** | "Where is X", "how does Y work", "which files use Z". Read-only, no judgement about design. |
| **routine change** | Scope is clear, 1 to 3 files, an existing pattern to copy (new endpoint like an existing one, a new test for a known case, a config field). |
| **complex change** | Multi-file, new abstraction, unclear approach, or touches security-sensitive code (authentication, authorization, secrets, connection pooling, the startup/composition root, configuration schema). Also: a bug nobody has localised yet. |
| **review / security** | Judge an existing diff or design against the project rules (AGENTS.md). No edits. |
| **verify** | Run the build or a test filter and report only failures. |
| **plan** | The user wants a plan or an architecture decision, not code yet. |

When two tiers fit, take the cheaper one and rely on the escalation ladder below.

## Step 2: select agent, model and effort

| Tier | Agent | Model | Effort | Sandbox | Parallelism |
| --- | --- | --- | --- | --- | --- |
| inline | none (coordinator does it) | current | current | current | 1 |
| lookup | `scout` | `gpt-5.6-luna` | low | read-only | 1, or 2 to 3 only for independent questions |
| routine change | `builder` | `gpt-5.6-terra` | high | workspace-write | 1 |
| complex change | `architect` | `gpt-5.6-sol` | xhigh | workspace-write | 1 (split into independent `builder` sub-tasks only if the architect's plan says so) |
| review / security | `reviewer` | `gpt-5.6-terra` (override `model = "gpt-5.6-sol"` for security-sensitive paths: auth, secrets, rate limiting) | high | read-only | 1 |
| verify | `test-runner` | `gpt-5.6-luna` | low | workspace-write (needs to run the build) | 1 |
| plan | coordinator in plan mode, or `architect` with the instruction "plan only, no edits" | inherits | inherits | read-only | 1 |

Why these defaults: OpenAI documents `low` as the right level for tool-driven search
and lookups, `high` for complex debugging and deep planning, and `xhigh` for long
agentic runs; independent benchmarks on the GPT-5 line show up to 23x token spread
between the lowest and highest effort with flat quality on classification-style work.
So if `builder` bills look high on mechanical work, `medium` (the tier default) is the
first step-down to try (edit `.codex/agents/builder.toml`), not a cheaper model.

Use `gpt-6-astra` only when the user asks for it by name or an `architect` run at
`xhigh` failed on a problem that is genuinely frontier (novel algorithm, deep
concurrency bug), not just large. It costs 2.5x Sol and does not accept `none`.

Never spawn more subagents than there are independent questions: simple fact 1 agent,
comparison 2 to 4, and 10+ only for broad research. Dependent steps run in one agent
sequentially, not in several. Keep `agents.max_concurrent_threads_per_session` at 3
to 5.

## Step 3: write the delegation brief

Vague briefs make subagents redo each other's work or misread the goal. Every brief
has:

1. **Objective**: one sentence of what "done" means.
2. **Boundaries**: files or directories in scope, what not to touch, AGENTS.md rules that apply (auth conventions, endpoint catalogues, routing, no secrets in repo).
3. **Verification target**: the exact command that must pass, taken from the project's build and test section (for security-sensitive changes, always include the project's authentication or security test filter).
4. **Output contract**: what to return and how long. Default: a summary under 30 lines with file paths and line numbers, then the verification output trimmed to failures. Never "paste the whole file".

Name the agent explicitly in the request ("use the `builder` agent to ...") so Codex
does not fall back to the built-in `default`/`worker`/`explorer` roles. Preface the
delegation with the routing decision so it is visible in the transcript:

```
router: tier=<tier> agent=<agent> model=<model> effort=<effort> agents=<n> verify=<command>
```

## Step 4: verify, then escalate one rung at a time

Read the agent's evidence (test output, build exit code). If it fails or the answer is
shallow, do not retry at the same level: climb one rung.

```
scout (luna low) -> builder (terra high) -> architect (sol xhigh) -> architect with model = "gpt-6-astra"
```

Escalate with the failure attached to the brief, so the next agent does not rediscover
it. Two failures at the top rung means the task, not the agent, needs re-scoping: stop
and ask the user.

## Coordinator habits that keep this cheap

- Do not read large files or run the full test suite without a filter in the main thread when a subagent can return the summary instead.
- Ask for evidence, not assurances: the failing test names, the command and its exit code.
- Prefer one well-briefed subagent over several thin ones; every subagent re-loads AGENTS.md, the skills list and the tool list.
- Independent subagents are requested together so they run concurrently; dependent ones wait.
- Lock every agent that does not need to write files to `sandbox_mode = "read-only"`; subagents inherit the parent's approval policy, so an approval-gated edit in a subagent may be denied silently. Keep edits in `builder`/`architect` and check their reported diff with `git diff`.
- If the router says `inline`, just do it. Explaining why you did not delegate wastes more than the delegation would have saved.
