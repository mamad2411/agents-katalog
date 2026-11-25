---
name: evidence-recorder
description: "Append one JSONL record to ~/.claude/evolution/records/ when a correction, a non-obvious win, or a repeated rework pattern occurs. Use sparingly — only when the event is load-bearing for future behavior. Do not log routine tool calls; the PreToolUse usage-logger already does that."
---

# evidence-recorder

## When to auto-use
Record an event when **any** of these are true:
- The user explicitly corrects an approach ("no, do X instead", "stop doing Y", "actually we prefer Z").
- A non-obvious technique produced a clear win (it worked when a naive approach would have failed).
- You notice a repeated rework pattern in the same session (doing X, being told to redo as Y, 2+ times).
- An adaptation was proposed or applied.

## When NOT to use
- Routine file edits, tool calls, or test runs — those are already captured by the PreToolUse usage-logger.
- Ambiguous events. If you're not sure it's a pattern, it's noise.
- To journal your reasoning — this is an evidence store, not a diary.

## How to record
Append one JSON line to the correct file:

```bash
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SESSION="${CLAUDE_SESSION_ID:-unknown}"   # populate from SessionStart hook if available
PROJECT=$(basename "$(pwd)")

python3 -c "
import json
rec = {
  'ts': '$TS',
  'session': '$SESSION',
  'project': '$PROJECT',
  'type': 'correction',              # one of: correction | win | friction | adaptation
  'scope': 'global',                 # global | project-specific | language:<x> | stack:<x>
  'summary': 'User corrected: prefer rsync --delete over rm before copy for setup sync.',
  'context': 'During sync of ~/.claude from repo; this prevented orphan files.',
  'id': 'evid-$TS-correction'
}
with open('$HOME/.claude/evolution/records/corrections.jsonl','a') as f:
  f.write(json.dumps(rec)+'\n')
"
```

Type → file mapping:
- `correction` → `records/corrections.jsonl`
- `win` → `records/outcomes.jsonl`
- `friction` → `records/outcomes.jsonl` (with `success: false`)
- `adaptation` → `records/adaptations.jsonl`

## Schema (all fields required unless marked optional)
- `ts` — ISO-8601 UTC
- `session` — session id if available
- `project` — basename of CWD
- `type` — correction / win / friction / adaptation
- `scope` — global / project-specific / language:<x> / stack:<x>
- `summary` — one sentence, ≤ 200 chars
- `context` — optional short context, ≤ 500 chars
- `id` — unique identifier

## Quality bar
A good record is terse, falsifiable, and future-useful. Bad example: "user was frustrated." Good example: "user prefers rsync --delete for setup sync (prevents orphan files)."
