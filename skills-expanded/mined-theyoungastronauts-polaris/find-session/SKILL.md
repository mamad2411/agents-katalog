---
name: find-session
description: "Use when the user refers to an earlier Claude Code conversation you can't see: \"does this ring a bell\", \"find our session about X\", \"get up to speed on the X work\", \"what session had this link\", \"resume the session where we...\", \"we talked about this before\", or names past work with no doc or commit to point at."
---

# Find Session

Past sessions are on disk as transcripts. Search what the **user typed** (not tool output), rank by recency, then read the best match and brief the user on it.

Transcripts: `~/.claude/projects/<cwd with every non-alphanumeric char replaced by ->/<session-id>.jsonl`, one JSON record per line. User-typed messages have `type == "user"` and `message.content` as a string or a list of `text` parts. Skip `isMeta` records, tool results, and injected text (`<command-...>`, `<system-reminder>`, `<task-notification>`). Subagent transcripts sit one level deeper and are skipped.

## 1. Search

Turn the user's words into a case-insensitive regex: 2-4 distinctive keywords, `|` between them, `\b` in front so `trip` doesn't hit `strip`. Requires `jq`.

```bash
P=~/.claude/projects/$(pwd | sed 's/[^A-Za-z0-9]/-/g')   # all projects: P=~/.claude/projects/
RE='\b(stripe|webhook|retry)'
grep -lisE "$RE" "$P"*/*.jsonl | while read -r f; do
  jq -r --arg re "$RE" --arg f "$f" '
    select(.type == "user" and (.isMeta | not))
    | (.message.content | if type == "string" then . else ([.[]? | select(.type == "text") | .text] | join(" ")) end) as $m
    | select(($m | test("^\\s*(<|Caveat:|Another Claude session)") | not) and ($m | test($re; "i")))
    | ($m | gsub("\\s+"; " ")) as $flat
    | ([($flat | match($re; "i").offset) - 50, 0] | max) as $at
    | [.timestamp[0:16], $f, $flat[$at:$at + 160]] | @tsv' "$f" 2>/dev/null
done | sort -r | awk -F'\t' '
  !($2 in hits) { order[++n] = $2; last[$2] = $1 }
  { if (++hits[$2] <= 3) snips[$2] = snips[$2] "\n    " substr($1, 1, 10) "  " $3 }
  END { for (i = 1; i <= n && i <= 8; i++) { s = order[i]; printf "\n%s  %d hits  %s%s\n", last[s], hits[s], s, snips[s] } }'
```

Prints up to 8 sessions, newest last-hit first, each with its hit count, path, and three snippets. `"$P"*` also covers nested dirs and worktrees of this project. The current project takes about a second; all projects can take ~30s.

- **The newest hit is often this session** (the user's own question). Skip it.
- **Nothing found:** try synonyms, drop to one keyword, then offer to widen to all projects.
- **A link or exact string** may only appear in Claude's replies or tool output. Search the raw files: `grep -lF 'https://example.com/x' "$P"*/*.jsonl | xargs ls -t`.

## 2. Read the best match

```bash
F=<path from step 1>; O=$(mktemp)
jq -r 'select(.type == "custom-title" or .type == "ai-title") | .customTitle // .aiTitle' "$F" | tail -1
jq -r '
  select((.type == "user" and (.isMeta | not)) or .type == "assistant")
  | (.message.content | if type == "string" then . else ([.[]? | select(.type == "text") | .text] | join(" ")) end) as $m
  | select(($m | length) > 0 and ($m | test("^\\s*(<|Caveat:)") | not))
  | "\n## \(if .type == "user" then "USER" else "CLAUDE" end) \(.timestamp[0:16])\n\($m[0:1500])"' "$F" > "$O"
wc -c "$O"; head -c 6000 "$O"; tail -c 25000 "$O"
```

The head shows what the session set out to do; the tail shows where it ended. Read the middle around the step-1 hits if the decision you need is there. If two sessions both look right, read both before answering.

## 3. Brief the user

```
<title or first ask>, <date>, <session id>
Goal:       one line
Decided:    rulings and the reasons given
Open:       what was queued or left unanswered
Last state: where the conversation stopped (as of that date)
```

It is a transcript, not current state. Check the repo before you rely on any "done" it reports. To keep working from it, `claude --resume <session-id>` reopens it, or continue here from the brief.

## Common mistakes

- **Searching tool output by default.** Old file dumps match every keyword. Search what the user typed; go raw only for links and exact strings.
- **Summarizing from snippets.** Snippets choose the session; read the transcript before you brief.
- **Treating the transcript as truth.** Decisions hold; status has drifted. Say what it showed and when.
