---
name: session-retrospective
description: Audits a Claude Code session — deterministic jq analysis of token spend and tool usage, then a judged retrospective in .claude/retrospectives/. Use after a task or when a session felt expensive.
---

# session-retrospective

Use this skill to audit how a session spent its tokens and used its harness, and to turn that into a graded, severity-ordered retrospective with process improvements.

> **Note:** This audits the *process* (spend, tool usage, delegation), not the *artifact*. For reviewing the code a session produced, use the `code-review` skill.

## Triggers

- After finishing a large task, before closing the session
- When a session felt slow or expensive and you want to know why
- Periodically, to spot recurring harness anti-patterns on a project

## Protocol

### Step 1 — Locate the transcript

Transcripts live under `~/.claude/projects/`, in a directory named after the absolute project path with `/` and `.` flattened to `-`:

```bash
PROJECT_DIR=~/.claude/projects/$(pwd | tr '/.' '--')
TRANSCRIPT=$(ls -t "$PROJECT_DIR"/*.jsonl | head -1)   # most recent session
ls -lh "$TRANSCRIPT"                                    # sanity-check size and mtime
```

For a specific session, use `"$PROJECT_DIR/<session-id>.jsonl"`.

**Never read the raw JSONL into context** — transcripts reach tens of megabytes, and loading one costs more than the session being audited. All extraction goes through `jq`.

### Step 2 — Deterministic analysis (zero token cost)

Assistant lines carry `message.model` and per-request `message.usage`; tool calls are `tool_use` blocks on assistant lines; failures are `tool_result` blocks with `is_error: true` on user lines.

```bash
# Tool-call histogram — what did the session actually do?
jq -s '[.[] | select(.type=="assistant") | .message.content[]? | select(.type=="tool_use") | .name]
  | group_by(.) | map({tool: .[0], calls: length}) | sort_by(-.calls)' "$TRANSCRIPT"
```

```bash
# Token totals per model + cache-read ratio — where did the money go?
jq -s '[.[] | select(.type=="assistant") | {m: .message.model, u: .message.usage}]
  | group_by(.m) | map({model: .[0].m, requests: length,
      input: ([.[].u.input_tokens] | add),
      output: ([.[].u.output_tokens] | add),
      cache_read: ([.[].u.cache_read_input_tokens // 0] | add),
      cache_creation: ([.[].u.cache_creation_input_tokens // 0] | add)})
  | map(. + {cache_read_pct: (100 * .cache_read / ([.cache_read + .cache_creation + .input, 1] | max) | round)})' "$TRANSCRIPT"
```

```bash
# Repeated Reads of the same path — context that was paid for more than once
jq -s '[.[] | select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="Read") | .input.file_path]
  | group_by(.) | map(select(length > 1) | {path: .[0], reads: length}) | sort_by(-.reads)' "$TRANSCRIPT"
```

```bash
# Subagent and skill invocations — was work delegated?
jq -s '[.[] | select(.type=="assistant") | .message.content[]? | select(.type=="tool_use")]
  | {subagents: ([.[] | select(.name=="Task") | .input.subagent_type // "general"] | group_by(.) | map({type: .[0], n: length})),
     skills:    ([.[] | select(.name=="Skill") | .input.skill] | group_by(.) | map({skill: .[0], n: length}))}' "$TRANSCRIPT"
```

```bash
# Tool errors — failed calls that were paid for anyway
jq -s '[.[] | select(.type=="user") | .message.content[]? | select(.type=="tool_result" and .is_error==true)] | length' "$TRANSCRIPT"
```

### Step 3 — Judge and write the retrospective

Interpret the numbers into findings, severity-ordered:

1. **Wasted spend** — repeated `Read`s of one path, identical retries after errors, redundant searches. Cite the count and the metric.
2. **Harness misuse** — `Bash` doing a dedicated tool's job: `cat`/`head` instead of `Read`, `grep`/`find` instead of search tools, `sed -i` instead of `Edit`. A `Bash`-dominated histogram is the signature.
3. **Missed parallelism / delegation** — zero `Task` calls in a long exploratory session; independent workstreams run serially; fan-out searches done inline instead of via a subagent.
4. **Context bloat** — cache-read ratio below ~80%, whole-file reads where a range sufficed.

Write the report to `.claude/retrospectives/<session-id>.md` (create the directory if needed):

```markdown
# Session retrospective — <session-id>

**Date:** … **Models:** … **Tokens:** in/out/cache … **Tool calls:** … **Errors:** …
**Grade:** B — solid delegation, but 4 re-reads of the same config file and a 62% cache ratio.

## Findings (by severity)
1. …metric-backed finding…

## Process improvements
- …concrete, checkable action…

## What went well
- …at least one pattern to keep…
```

Every finding must cite a number from Step 2. Improvements must be actionable next session ("delegate `src/` fan-out searches to an Explore subagent"), not generic ("use fewer tokens").

## Automating with a SessionEnd hook

To run this on every session automatically, copy the canonical reference implementation from [prototypdigital/bluetemberg](https://github.com/prototypdigital/bluetemberg) on `main` rather than reinventing it: `.claude/hooks/spawn-session-audit.sh` (the hook entry — gates and detaches) and `.claude/hooks/run-session-audit.sh` (the worker — runs the Step 2 analysis and the judged pass). Shipped in [#231](https://github.com/prototypdigital/bluetemberg/pull/231).

`SessionEnd` hooks share a **1.5 s budget** — never run the analysis synchronously. The entry script performs cheap, deterministic checks before detaching:

- Skip `reason == "clear"` — a deliberately discarded session has nothing worth auditing.
- Skip if the transcript path, session id, or cwd is missing from the hook input.
- Skip if `.claude/retrospectives/<session-id>.md` already exists — one retrospective per session.

then hands off and exits 0 immediately:

```bash
nohup "$hook_dir/run-session-audit.sh" "$transcript" "$session_id" "$cwd" >/dev/null 2>&1 &
disown
```

The triviality gate — skipping sessions under ~5 assistant turns, since there's nothing to grade yet — lives in the worker, not the entry script: counting turns means reading the transcript, and that's too slow for the entry script's 1.5 s budget. The worker runs the Step 2 jq analysis, then a cheap headless judge (`claude -p --model haiku`) fed the stats and truncated user prompts — **never the raw JSONL** (cost, size, and the fact that the transcript format is officially internal and version-unstable all argue against it). Sandbox the judge call itself: `--tools ""` and `--strict-mcp-config` (the transcript's own prompt text reaches the judge's input, so a prompt-injected session shouldn't be able to make it call anything), `--max-turns 1`, and a `--max-budget-usd` ceiling. As with the pr-reviewer's cost comment, gate on the JSON result's `.is_error == false` rather than exit status or non-empty stdout — `claude -p` reports `subtype: "success"` even on an auth failure, with the error text sitting in `.result`.

Merge this `SessionEnd` entry into the project's `llm/hooks.claude.json` as a sibling of whatever's already there (only create the file fresh if it doesn't exist yet — see [prototypdigital/bluetemberg#225](https://github.com/prototypdigital/bluetemberg/issues/225), shipped in engine 0.9.0). Copying the block below over an existing file instead of merging it will silently drop other event keys — e.g. a `PostToolUse` entry from the `pr-review-loop` skill:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/spawn-session-audit.sh",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

Run `bluetemberg sync` (or `npm run sync:llm-config`) afterward — it writes this into `.claude/settings.json` and preserves any other hooks already wired there (e.g. a `PostToolUse` entry from the `pr-review-loop` skill lives under the same file, as a sibling top-level event key). The pack itself still cannot ship this manifest — packs are content, not executable config, and command hooks are only ever honored from the project's own `llm/` — so authoring `llm/hooks.claude.json` once is still a manual, one-time step; everything after that (regenerating `settings.json` on every sync) is automatic.

For a continuous dashboard instead of per-session reports, Claude Code's OpenTelemetry export is the better fit: the `claude_code.token.usage` metric is attributed per agent, skill, and MCP tool, and feeds any OTLP backend without touching transcripts.

## Completion checklist

- [ ] Transcript located by flattened project path; size sanity-checked; raw JSONL never read into context
- [ ] All five jq analyses run; numbers captured
- [ ] Findings severity-ordered, each citing a metric
- [ ] Retrospective written to `.claude/retrospectives/<session-id>.md` with a grade and at least one "went well"
- [ ] If asked for automation: hook entry gates clear/missing-input/dedup and detaches to a worker (`nohup … &`), never synchronous; the worker gates trivial sessions (<5 assistant turns) and the judge's JSON result on `.is_error == false`

## When NOT to use

- Mid-task, when the session is still short — there is nothing meaningful to grade yet
- To review the code a session produced (use `code-review`)
- As a substitute for continuous monitoring across a team — that is the OpenTelemetry export's job
