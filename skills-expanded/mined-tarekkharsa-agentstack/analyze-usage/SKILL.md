---
name: analyze-usage
description: Report on your own agent usage — parse Claude Code session transcripts for token burn, and cross-check installed agentstack skills/servers against what was actually used to flag dead weight. Local and read-only.
---

# Analyze usage

Use when you want to understand your own footprint: how many tokens you're
burning, and which installed capabilities are actually pulling their weight.

## Where the data is

Claude Code writes a JSON-lines transcript per session at:

```
~/.claude/projects/<project-hash>/<session-id>.jsonl
```

Each line is one event; assistant turns carry token usage, and tool-use events
name the tool or skill invoked. It's local and safe to read.

## Token burn

Sum token usage across a session or a day. The fields are nested
(`message.usage.input_tokens` / `output_tokens`), so use python for anything
beyond a trivial count — don't hand-roll it in a shell one-liner.

## Dead-weight detection (the useful one)

1. List what's installed: `agentstack more lib list` (library skills + servers) and
   the project's active profile.
2. Extract which skills/servers were actually invoked, from the transcripts'
   tool-use / skill-load events.
3. The set difference — **installed but never invoked** — is dead weight: it
   taxes every session's context window for nothing. Propose pruning it.

## Rules

- **Read-only and local.** Never send transcript content anywhere; report only
  aggregates — counts, totals, names.
- **Best-effort.** The transcript format is undocumented and can change —
  tolerate unknown lines, don't assume a fixed schema.
- **Coverage is uneven.** This is rich for Claude Code; other CLIs expose less
  (or nothing). Say which agents you could actually see.

## Note

agentstack records some of this natively (activation counts, per-server context
cost). If `agentstack more report calls` exists in your version, prefer it — it joins
usage to the library for you. This skill is the portable, no-code version.
