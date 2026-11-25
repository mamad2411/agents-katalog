---
name: full-power
description: "Maximize agent capability: spawn well-briefed sub-agents, use every resource, verify before accepting. For complex, high-stakes tasks."
---

# Full Power Mode

**What this mode is NOT:** a license to skip rigor. The mandatory gates in global
CLAUDE.md still run first: the Root Cause `<diagnosis>` pass (it carries the
patch-vs-root cost lines) and Outside Voice review for plans in its scope (locked
contracts, migrations, new architecture, or a review ask). Full power accelerates
execution AFTER those gates, never around them.

## Sub-Agents: Brief Well, Check What Gates

**Spawn liberally**, brief every sub-agent well, and check its output where that output gates your next step.

Model routing still binds: set `model` on every spawn, `opus` for judgement work (reviews, planning, debugging, synthesis) and `sonnet` for mechanical work, per `~/.claude/CLAUDE.md`. "Spawn liberally" widens scope, never tier.

### Briefing (prevents drift)

Before calling any `Agent` tool, write a prompt that includes ALL of the following:

1. **Goal + why**: what the user is trying to accomplish and why it matters. One sentence.
2. **Exact scope**: what the agent MUST do, and explicitly what it MUST NOT do (no refactors, no unrelated fixes, no new files unless asked).
3. **Concrete anchors**: file paths with line numbers, function/symbol names, exact commands to run. No vague "find the relevant code."
4. **Context already gathered**: what you've ruled out, what you've tried, what's been confirmed. Prevents re-investigation.
5. **Non-negotiables**: read the PROJECT CLAUDE.md and quote its mandates verbatim in the brief (e.g. Quantamental's no-vol-clip / futures_pnl.py / safe_sync.py rules when working there; each project has its own).
6. **Deliverable shape**: exactly what to return: a diff, a ≤200-word report, a file path, a pass/fail verdict. Cap the response length.
7. **Stop conditions**: when to stop and report vs. when to keep going. Prevents runaway work.

Terse prompts produce shallow work. If your prompt is under 5 sentences for a non-trivial
task, it's probably under-briefed.

**Never delegate understanding.** Do not write "based on your findings, fix it" or
"do what's needed." Synthesis stays with you. The agent executes specifics.

### Review (catches drift)

Take a sub-agent's findings as done (CLAUDE.md, Sub-agents) and check only what gates your next step:

1. **Scope**: did it stay in the brief? `git status` and the diff show files it shouldn't have touched, or abstractions, refactors and helpers nobody asked for.
2. **Gating claims**: when its "tests pass" or a number decides what you do next, read the log or the output of the one command it cites.
3. **Slop** (checklist: de-sloppify Pass 2).
4. **Project non-negotiables**: did it violate the project CLAUDE.md? (e.g. in Quantamental: an added vol cap or raw sync; anywhere: mocked data it shouldn't have).
5. **If drift is detected**: send a corrective `SendMessage` to the same agent with the specific violations and what to fix. Do NOT silently clean up its mess yourself, that trains the behavior to continue.

If the agent's output is trustworthy and in-scope, proceed. If not, reject and re-run
with tighter constraints.

### Parallelism & orchestration

- Run truly independent agents concurrently in a single message.
- Do NOT parallelize when one agent's output is needed to brief another: that's sequential.
- Pick the right agent type for each subtask (see `~/.claude/docs/agent-routing.md`).

## Resources

- Use every tool at your disposal: connected MCP servers, web search, browser, LSP,
  skills.
- Prefer the most authoritative source for each question: official docs for library
  APIs, `git log`/`git blame` for history, the live DB/read-model for data state, the
  code itself over memory.
- Before recommending a file/function/flag from memory, verify it still exists.

## Rigor

- Check edge cases, failure modes, and second-order effects before acting.
- **Test after changing**, and source every number (Sourcing in CLAUDE.md).
- Double-check critical operations: SQL, production scripts, data syncs, destructive
  commands, anything touching prod or master.
- If uncertain, investigate first. Do not guess.

## Execution

- Break complex tasks into discrete tracked steps (the session's task/todo list). Mark each done as soon as it finishes, don't batch.
- Validate outputs at each stage before moving to the next.
- Before claiming completion: run the verification command (tests, the project's output-validation script if it has one, build, type-check) and confirm output. Evidence before assertions.
