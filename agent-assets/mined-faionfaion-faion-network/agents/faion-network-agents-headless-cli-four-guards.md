# Headless CLI — Four Guards Against Mystery Hangs

## Summary

**One-sentence:** Requires every non-interactive agent-CLI invocation (Claude Code, Codex, Aider, opencode) to set four guards — headless flag, explicit allowedTools, --max-turns cap, and `< /dev/null` stdin — eliminating the four documented production failure modes (TUI hang, permission stall, runaway loop, garbage stdin).

**One-paragraph:** Every non-interactive run of an agent CLI MUST set four guards: (1) print/headless flag to disable the TUI, (2) explicit `--allowedTools` allowlist (NEVER `--dangerously-skip-permissions` in prod), (3) `--max-turns` cap tied to a real workflow length, (4) closed stdin via `< /dev/null` so the agent cannot block waiting on user input. Missing any one turns into a mystery hang or runaway-loop incident.

**Ефективно для:** будь-якого cron / CI / черги / scheduled-agent виклику CLI-агента — там, де немає TTY і немає людини, щоб натиснути "Ctrl-C".

## Applies If (ALL must hold)

- ANY cron/CI/GitHub Actions/queue/scheduled-agent invocation of claude, codex, aider, or opencode.
- Multi-agent pipelines where one agent shells out to another.
- Background pool subagents.
- Self-healing scripts running unattended on a server.

## Skip If (ANY kills it)

- Interactive developer sessions — TUI is the point.
- One-shot smoke tests where the operator watches the terminal.
- Local prototyping where the agent should pause to ask.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task prompt | String passed as positional arg | Caller |
| Allowlist | Comma-separated `Tool` or `Bash(prog:*)` patterns | Engineering review |
| Turn cap | Integer tied to workflow length | Workflow author |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `idempotent-write-tools` | Headless agents that mutate state need idempotency keys for safe retry. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: all-four-required, no-dangerously-skip, cap-tied-to-workflow, per-CLI mapping, lint-in-CI | ~1000 |
| `content/02-output-contract.xml` | essential | The four-guard invocation pattern and per-CLI flag table | ~900 |
| `content/03-failure-modes.xml` | essential | Each missing guard → its documented failure mode | ~900 |
| `content/06-decision-tree.xml` | essential | Per-CLI mapping for the four guards | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate guarded invocation for a new script | haiku | Mechanical template fill |
| Audit existing cron scripts | sonnet | Pattern detection across many files |
| Design narrow allowlist for new workflow | sonnet | Requires understanding of needed tools |

## Templates

| File | Purpose |
|------|---------|
| `templates/headless-guards.sh` | Reusable guarded invocation wrapper for Claude Code, Codex, Aider, opencode |
| `templates/_smoke-test.sh` | Minimum invocation for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-headless-cli-four-guards.py` | Lints a shell script for missing guards | Pre-commit on any cron/CI script that calls an agent CLI |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[idempotent-write-tools]]
- [[generator-critic-bounded-loop]]

## Decision tree

See `content/06-decision-tree.xml`. The root question is whether the invocation runs in an interactive TTY. If not, the tree enforces all four guards and maps them to the correct flag per CLI (Claude Code uses `-p`, Codex uses `codex exec`, etc.).
