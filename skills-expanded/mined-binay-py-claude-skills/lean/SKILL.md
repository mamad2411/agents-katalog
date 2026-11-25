---
name: lean
description: Token-lean mode. Use when the user says lean, save tokens, cheap mode, low token, hitting limits, or asks to get max result for min tokens. Also audits setup overhead.
---

# Lean mode

Goal: same quality result, fewest tokens. Context is re-sent every turn, so every byte you pull in is paid for again and again. Follow these rules for the rest of the session.

## Reading
- Grep/Glob first, then Read only the file you need, with `offset`/`limit` around the hit. Never Read a whole large file to find one function.
- Never re-read a file you already read or just edited. Edit fails loudly if it didn't apply.
- Use `output_mode: "files_with_matches"` or `head_limit` on Grep before asking for content.
- Don't open lockfiles, build output, minified, generated or vendored files.

## Commands
- Cap output: `| tail -n 40`, `| head -n 40`, `grep -m 20`, `--quiet`, `-q`, `--silent`. Tests: show failures only (`pytest -q --tb=short`, `npm test 2>&1 | tail -n 40`).
- Never dump logs, JSON blobs or `ls -R`. Filter with grep/jq/python first, print only what matters.
- Chain related shell steps into one call; run independent tool calls in parallel in one message.

## Delegation
- Broad search over many files: one `Explore` agent with `model: "haiku"`, ask for a conclusion of under 150 words. Don't also search yourself.
- Don't spawn agents for things doable in 1–3 tool calls. Never fan out multiple agents unless the work is truly parallel.

## Writing
- Edit with small, exact `old_string` hunks. Never rewrite a whole file to change a few lines.
- No narration between tool calls. No restating the plan or the user's request.
- Final answer: result first, short. Bullets over paragraphs. Show code only when it's new for the user. No summary of what you just did unless asked.

## Thinking
- Act as soon as there's enough info. Don't re-derive facts already in the conversation.
- Pick one approach and go; don't survey options.
- If the task is ambiguous in a way that would waste a lot of work, ask one short question instead of guessing.

## Tell the user (once, briefly) when it helps
- Switching to unrelated work → `/clear` (free) beats `/compact` (costs a full read).
- Simple task on Opus → `/model sonnet` or `/effort low`.
- Session idle a long time → cache is cold; a fresh `/clear` + short brief is cheaper than continuing.

## Setup audit
When asked to check the setup, or the user keeps hitting limits, run:

```
python scripts/lean_check.py [project_dir]
```

(Run from this skill's folder; needs Python 3.8+, no packages.) It prints the fixed per-session overhead (model, CLAUDE.md, MEMORY.md, MCP servers, plugins, skill descriptions, prompt hooks) with fixes. Show the user its output and offer to apply the fixes. Never edit settings without approval. For a deep log analysis, use the `claude-token-audit` skill if installed.
