---
name: compose-org
description: >-
  Run a task as an evolved multi-agent ORG using the installed liquid-org
  framework — where YOU (the running Claude) embody the org: you ask liquid-org
  which proven team topology + specialist personas to use (retrieved from its
  evolved pool, or assembled fresh), then dispatch ONE SUBAGENT PER TALENT to
  play each role independently, then grade and record the result so the pool
  learns. Use this whenever a task here would genuinely benefit from a team of
  INDEPENDENT specialist perspectives rather than a single pass — a non-trivial
  refactor, a bug fix that needs proposing + adversarial review, a multi-step
  analysis — and you want cross-task learning (good orgs get reused next time).
  Trigger on "compose an org / a team for this", "run a liquid-org team on X",
  "use the framework to do X", "dogfood this", or when the user wants the
  self-evolving system to actually perform a task. Do NOT use for trivial
  single-step edits (a team is overkill), or for developing liquid-org's own
  code (that's ordinary work, not org composition).
---

# Run a task as a liquid-org org (you ARE the runtime)

liquid-org treats a *team of agents* as first-class, evolving data: topologies
that scored well on past tasks are cached and retrieved for similar new ones.
The native way to use it from inside a Claude session is **not** to shell out to
another model — *you are already the model*. So: liquid-org tells you **which
team to run**, and **you run it** by playing each talent as an independent
subagent. No `claude -p`, no API key.

> There is also a batch launcher (`liquid-org compose`) for *unattended* runs that
> drive the model through an external backend — see "Unattended alternative" at
> the end. Prefer the native path below when you're in an interactive session.

## Why subagents (not you role-playing inline)

The entire value of an org is that the perspectives are **independent**. An
auditor auditing a proposer is only worth something if it didn't write the
proposal. If you play every role in one context, the "auditor" already knows
what the "proposer" was thinking — that's theater, not a team. So **dispatch a
real subagent per talent**: each gets a fresh context and only sees what the
topology says it should.

## Requirements & the CLI

- **Prerequisite — the `liquid-org` CLI on PATH.** Install the package once:
  `pip install "git+https://github.com/U0001F3A2/liquid-org.git"` (or, from a
  clone, `pip install .`). That puts the unified
  `liquid-org` command (subcommands `plan` / `compose` / `record`) on PATH — the
  primary surface this skill drives. Needs Python ≥3.12. Verify: `liquid-org -h`.
  The commands below show the **installed** form (no repo, no `uv`).
  - **Inside the liquid-org dev repo?** Prefix every command with `uv run`
    (e.g. `uv run liquid-org plan "..."`) so `uv` resolves the repo's env.
  - **Last-resort fallback** (the package is importable but `liquid-org` isn't on
    PATH): the bundled thin-shim scripts wrap the same code —
    `python "${CLAUDE_PLUGIN_ROOT}/skills/compose-org/scripts/plan_org.py" "..."`
    == `liquid-org plan "..."` (`record_outcome.py` == `record`,
    `compose_org.py` == `compose`).
- **EXECUTE-only** — run these, don't read them as reference. They are
  deterministic helpers (org retrieval/assembly, grading) so this skill never
  regenerates that logic: `plan` (model-free — no model call, no API key),
  `record` (records a real grade), and the unattended `compose`.
- **Exit codes** (so a subagent can branch on failure): `0` ok · `2` usage
  error · `1` runtime failure.
- **The evolving pool lives in ONE SQLite DB** — `liquid.db` in the **current
  directory** by default (override with `--db sqlite:///<path>`). This is the
  whole point of the skill: it's the cross-task memory good orgs are reused from.
  So `plan` (step 2) and `record` (step 6) **MUST hit the SAME DB**, or the org
  you planned can't be graded and the pool never learns. Pick ONE stable path at
  the start of a run and pass it to every command — e.g.
  `--db "sqlite:///$PWD/liquid.db"` (and don't `cd` between steps), or an explicit
  absolute `--db "sqlite:////abs/path/liquid.db"`. Keep that file; it's the state.

## The flow

### 1. Classify the task into a signature
You are the model, so you extract the task signature. Decide two axes:
- **decision_depth**: `one-shot` (a single transform → LINEAR pipeline) ·
  `multi-step` (needs a coordinator → HUB) · `debate` (needs adversarial
  back-and-forth).
- **output_modality**: `code-patch` · `prose` · `analysis` (what the org produces).

### 2. Get the team plan (model-free, no LLM call)
```bash
liquid-org plan "<the task>" \
    --decision-depth <one-shot|multi-step|debate> \
    --output-modality <code-patch|prose|analysis> \
    --db "sqlite:///$PWD/liquid.db"   # use this SAME --db in step 6 (record)
# in the dev repo: prefix `uv run`. fallback: python "${CLAUDE_PLUGIN_ROOT}/skills/compose-org/scripts/plan_org.py" "<the task>" ...
```
This retrieves a proven org (or assembles a fresh team from the talent pool),
persists an **ungraded** org graph, and prints a JSON plan:
```json
{
  "graph_id": "g-...",
  "topology": "linear" | "hub-and-spoke" | ...,
  "reused_from": "g-..." | null,        // non-null = a past org was reused (learning!)
  "steps": [ {"ordinal":0,"node_label":"reader","role_hint":"code-reader",
              "talent_id":"...","persona_prompt":"<full persona>", ...}, ... ],
  "edges": [ {"src":"reader","dst":"proposer","pattern":"handoff"}, ... ]
}
```
Lead your eventual report with **`reused_from`**: non-null means liquid-org
recognized this task and re-ran a team that worked before — that's the cross-task
learning the framework exists for.

### 3. Make a scratchpad (the org's blackboard)
Create a run-scoped dir, e.g. `.claude/org_runs/<graph_id>/`. Each talent writes
its **full** work product to a file there. This matters: subagents return only a
*summary* to you, but the next talent often needs the previous one's *exact*
output (e.g. a diff). So talents write artifacts to the scratchpad, and you hand
the next talent the file contents — not the summary.

### 4. Run the org — one subagent per talent, per the topology
Walk `steps` and dispatch a **subagent (Task tool)** for each, threading the
scratchpad. The `edges` give the structure; the common shapes:

- **LINEAR** (`handoff` edges): run steps in `ordinal` order, sequentially. Each
  subagent gets the task + the scratchpad's prior outputs; it writes its output
  to `.claude/org_runs/<graph_id>/<node_label>.md`; the next reads it.
- **HUB_AND_SPOKE** (a planner + spokes): run the planner step first (it briefs
  the work), then dispatch the spoke steps as **parallel** subagents (one Task
  message, multiple subagents), then run the planner's integrate step over all
  spoke outputs.
- For any shape: a subagent's prompt is
  `"You are the {role_hint}. {persona_prompt}\n\nTask: {task}\n\nPrior team
  outputs:\n{scratchpad contents}\n\nSCOPE: act ONLY on the concrete target
  named in the task / prior outputs — do not broaden to the whole repo. If no
  concrete target is given, say so in one line and stop; do NOT ask which file
  (this org runs unattended — nobody answers).\n\nWrite your complete output to
  {scratchpad path}."`

This SCOPE line matters once talents have real tools: a persona written for the
tool-less path ("run ruff", "given the code") will, with a live shell, act on
its standalone default (lint the whole repo, ask "which file?") instead of the
org's task. Anchoring scope in the dispatch prompt — not just the persona —
keeps each talent on the one artifact it was composed to handle. (The unattended
`liquid-org compose` path enforces the same intent via the `_SCOPE_ANCHOR`
constant in `liquid_org/runtime/compiler.py` — keep the two in sync.)

Keep each talent in-character (its `persona_prompt`); do not collapse them.

### 5. Grade what the org produced — for real
If the org produced a code change, **apply it and run the actual checks**
(`ruff check`, `pytest` on the affected files). Use real results, not an
impression. For prose/analysis, assess against the task honestly.

### 6. Record the outcome (close the loop so the pool evolves)
```bash
liquid-org record <graph_id> \
    --db "sqlite:///$PWD/liquid.db" \  # MUST match the --db from step 2's plan
    --ruff-ok --pytest-ok            # or --no-ruff-ok / --no-pytest-ok per the real checks
#   --ast-pass-rate 0.x   (optional)   |   --no-op  (org produced nothing usable)
# in the dev repo: prefix `uv run`. fallback: python "${CLAUDE_PLUGIN_ROOT}/skills/compose-org/scripts/record_outcome.py" <graph_id> ...
```
This scores the org graph; high scorers become retrieval candidates for future
similar tasks. **Pass the grade you actually measured** — a fabricated grade
poisons the evolution signal, which is the one thing this whole system is for.

### 7. Report
Lead with **reused vs freshly-assembled**, then the org's output, then the
recorded score. If reused, say which past org and that the pool is converging.

## Unattended alternative (batch launcher)

For CI / overnight corpus generation where no human is in the loop, the batch
launcher runs the whole org through an external model backend instead of you:
```bash
liquid-org compose "<task>" --transport auto
# in the dev repo: prefix `uv run`. fallback: python "${CLAUDE_PLUGIN_ROOT}/skills/compose-org/scripts/compose_org.py" "<task>" --transport auto
```
**Transport taxonomy** (`--transport`, see `liquid-org compose --help`):
- `api` — raw Messages API: clean completions, real temperature=0 determinism,
  metered cost. The **MEASUREMENT** path; needs `ANTHROPIC_API_KEY` (sk-ant-api...).
- `agent-sdk` — the **Claude Agent SDK**: OAuth auth (no API key), **tool-using
  talents** (each talent can Read/Grep/Glob the real context). The approved
  **PRODUCTION** transport; needs the optional dep (`uv sync --extra agent-sdk`).
- `claude-cli` — the `claude -p` bridge: **DEPRECATED**, superseded by `agent-sdk`;
  each talent is a tool-less Claude Code session (no temperature/cost control).
  Kept working as an explicit choice.

`--transport auto` (default) picks `api` when `ANTHROPIC_API_KEY` is set, else
`agent-sdk`. This is the *non-native* path; in an interactive session, prefer the
subagent flow above — you're the better runtime.

## Install & activation

This skill ships in the **`liquid-org` Claude Code plugin** (manifest at the repo's
`.claude-plugin/plugin.json`) and is auto-discovered once the plugin is installed:
```bash
/plugin marketplace add U0001F3A2/liquid-org    # then
/plugin install liquid-org@liquid-org
pip install "git+https://github.com/U0001F3A2/liquid-org.git"   # the CLI the skill drives (see Requirements)
```
> These commands require the `U0001F3A2/liquid-org` repo to be **accessible** —
> public, or (while private) an authenticated git source: `git+ssh://git@github.com/U0001F3A2/liquid-org.git`
> for the CLI, and a configured GitHub token for the marketplace source.
**Developing in the liquid-org repo** (not installing the plugin)? `.claude/` is
gitignored, so the skill lives in tracked `skills/`; symlink it for local discovery
and use `uv run` for the CLI:
```bash
mkdir -p .claude/skills && ln -s "$(pwd)/skills/compose-org" .claude/skills/compose-org
```
