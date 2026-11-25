---
name: scribe-query
description: >
  Query and analyze AI agent behavior traces using scribe's CLI query primitives
  (scribe q). Use this skill whenever you need to: inspect what an AI agent
  (Claude Code, Codex, Cursor) sent or received in its API calls; search through
  system prompts, tool definitions, or conversation history; understand the
  parent-child hierarchy of agent and subagent requests; compare how prompts
  evolve across turns; or debug why an agent behaved a certain way. Trigger this
  skill when the user mentions scribe, trace analysis, agent behavior inspection,
  prompt archaeology, request trees, or wants to understand what happened in a
  coding agent session. Also trigger when the user says things like "what did
  Claude send", "show me the system prompt", "how many subagents spawned",
  "what tools were available", or "what changed between turns".
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Scribe Query — Agent Behavior Analysis via CLI

Scribe records every API request and response flowing through AI coding agents
(Claude Code, Codex, Cursor). The `scribe q` command group exposes 6 query
primitives for searching, inspecting, and diffing this data from the terminal.

Arguments passed: `$ARGUMENTS`

## Quick start

```bash
# List recent sessions
scribe q sessions --source claude-code --table

# See the request tree for the latest session
scribe q tree --latest --source claude-code --table

# Search for a pattern across payloads
scribe q search "MEMORY.md" --latest --role system

# Inspect a specific request (use ID from tree or search)
scribe q show 019578a1b2c3 --full

# See what changed since the previous turn
scribe q diff 019578a1b2c3 --fields system,tools
```

## Commands by domain

### Navigation — find your target

```bash
# List sessions (newest first)
scribe q sessions
scribe q sessions --source claude-code --limit 10
scribe q sessions --source codex --table
scribe q sessions --fields all              # includes models, ended_at, metadata
scribe q sessions --full                    # show full 32-char IDs

# Search across payloads (regex, case-insensitive)
scribe q search "<pattern>"
scribe q search "system-reminder" --latest --source claude-code
scribe q search "CLAUDE.md" --role system --direction request
scribe q search "error" --role assistant --direction response --limit 5
scribe q search "memory/" --context-chars 200 --full
```

### Inspection — read the content

```bash
# Structured decoded view (messages + tools + usage + config)
scribe q show <trace_request_id>
scribe q show <id> --full                   # no truncation
scribe q show <id> --fields messages        # only messages
scribe q show <id> --fields tools           # tool definitions + calls + count
scribe q show <id> --fields usage           # token counts
scribe q show <id> --fields config          # model, max_tokens, temperature, thinking

# Raw payload (escape hatch)
scribe q raw <trace_request_id>
scribe q raw <id> --pretty                  # force pretty-print
scribe q raw <id> --no-pretty               # force compact
scribe q raw <id> --decode-cursor           # decode Cursor protobuf
```

### Analysis — understand the structure

```bash
# Hierarchical request tree
scribe q tree --latest --source claude-code
scribe q tree --latest --source claude-code --table    # human-readable
scribe q tree --session 019d2463d141 --turn 3          # specific turn
scribe q tree --latest --source codex
scribe q tree --latest --role subagent                 # only subagent requests
scribe q tree --latest --fine-role task_subagent_explore  # specific fine role

# Incremental diff from previous same-role request
scribe q diff <trace_request_id>
scribe q diff <id> --fields system          # system prompt changes
scribe q diff <id> --fields tools           # added/removed tools
scribe q diff <id> --fields memory          # memory file path changes
scribe q diff <id> --fields config          # model/temperature changes
scribe q diff <id> --fields messages        # new messages this turn
scribe q diff <id> --fields usage           # token delta
scribe q diff <id> --full                   # no truncation on diffs
```

### Output filtering — jq integration

Every command supports `--jq` for client-side filtering:

```bash
# Count subagent requests (or use --role subagent)
scribe q tree --latest --source claude-code \
  --jq '[.turns[].requests[] | select(.execution_role=="subagent")] | length'

# Extract system prompt text
scribe q show <id> --fields messages --full \
  --jq '.messages[] | select(.role=="system") | .content'

# Get trace_request_id from search
scribe q search "MEMORY.md" --role system --latest \
  --jq '.matches[0].trace_request_id_full'

# List tool names
scribe q show <id> --fields tools \
  --jq '.tool_definitions[].name'
```

## Shared flags

| Flag | Available on | Effect |
|------|-------------|--------|
| `--source claude-code\|codex\|cursor` | sessions, search, tree | Filter by source tool |
| `--latest` | search, tree | Target the most recent session |
| `--session <id>` | search, tree | Target a specific session |
| `--full` | sessions, search, show, diff | Disable content truncation |
| `--table` | sessions, tree | Human-readable table output |
| `--jq <expr>` | all 6 commands | Client-side jq filter |
| `--fields <list>` | sessions, show, diff | Select output sections |
| `--role <role>` | tree | Filter by execution_role (primary/subagent/assistive/probe) |
| `--fine-role <role>` | tree | Filter by fine_role (e.g. task_subagent_explore) |
| `--limit <n>` | sessions, search | Cap number of results |

ID prefix matching: any 8+ character prefix of a session or trace_request ID
works. If the prefix is ambiguous, you get a list of candidates.

Default truncation: strings at 300 chars, tool_call_json at 500 chars. Truncated
values are marked with `...[+N chars]` and the containing object gets
`_truncated: true`.

## Examples

### Inspect a Claude Code session structure

```bash
# 1. Find the session
scribe q sessions --source claude-code --limit 3 --table

# 2. See the full tree
scribe q tree --latest --source claude-code --table
# Output:
# Session: 019d2463d141  Source: claude-code
#
# Turn 1
#   019d2463d4cd  claude-haiku-4-5-20251001  -> end_turn
#   019d2463d146  claude-opus-4-6  (main_primary) -> tool_use
#
# Turn 2
#   019d2463d607  claude-opus-4-6  (main_primary) -> end_turn
#   019d2463f347  claude-haiku-4-5-20251001 [assistive] (hook_assistive) -> tool_use

# 3. Inspect the primary request's messages
scribe q show 019d2463d146 --fields messages --full
```

### Track system prompt evolution across turns

```bash
# 1. Get trace IDs for primary requests
scribe q tree --latest --source claude-code \
  --jq '.turns[].requests[] | select(.execution_role=="primary") | .trace_request_id'

# 2. Diff each against its predecessor
scribe q diff 019d2463d607 --fields system
# Output:
# {"trace_request_id": "...", "status": "delta",
#  "system_prompt": {"changed": false, "chars": 27823}}

scribe q diff 019d24661c1f --fields system,memory
# Shows what changed: system prompt diff + memory path additions/removals
```

### Debug a subagent interaction

```bash
# 1. Find the subagent in the tree
scribe q tree --latest --source claude-code --role subagent --table
# Shows only subagent nodes — note the trace_request_id

# 2. See what the subagent was asked to do
scribe q show 019d24663909 --fields messages --full

# 3. See what it responded
scribe q show 019d24663909
# Note the paired_trace_request_id, then:
scribe q raw <paired_id> --pretty
```

## Known limitations and workarounds

### `show --fields tools` may return empty

Tool definitions are not always extracted by `show`. Use direct DB query:

```bash
sqlite3 ~/.scribe/traces.db \
  "SELECT body FROM raw_payloads WHERE trace_request_id = '<full_32char_id>'" \
  | python3 -c "import json,sys; [print(t['name']) for t in json.loads(sys.stdin.read()).get('tools',[])]"
```

### `raw` command may crash

If `raw` errors out, query the database directly:

```bash
sqlite3 ~/.scribe/traces.db \
  "SELECT body FROM raw_payloads WHERE trace_request_id = '<id>'" \
  | python3 -m json.tool
```

See [references/raw-payloads.md](references/raw-payloads.md) § "Direct database
fallback" for more patterns (tool extraction, config extraction, tool list diffs).

## Specific tasks

For deeper guidance on specific analysis patterns, read the relevant reference:

* **Searching payloads** — [references/search-patterns.md](references/search-patterns.md)
  Regex tips, role/direction filtering, multi-session search, snippet interpretation.

* **Understanding the request tree** — [references/trace-tree.md](references/trace-tree.md)
  Execution roles, parent-child hierarchy, subagent families, probe detection.

* **Tracking prompt evolution** — [references/diff-analysis.md](references/diff-analysis.md)
  System prompt diffs, tool mutations, memory file tracking, config drift.

* **Working with raw payloads** — [references/raw-payloads.md](references/raw-payloads.md)
  SSE response parsing, Cursor protobuf decoding, provider-specific payload formats.

* **Multi-command recipes** — [references/workflow-recipes.md](references/workflow-recipes.md)
  Common analysis scenarios combining multiple commands.

* **Data model** — [references/data-model.md](references/data-model.md)
  Session/Turn/TraceRequest/RawPayload schema, execution roles, fine roles, provider detection.
