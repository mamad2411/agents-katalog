---
name: cost-audit
description: Analyzes the current session's token usage, pinpoints where tokens were wasted, and produces concrete optimization actions
user-invocable: true
allowed-tools: Bash(claude*), Read, Grep
effort: low
---

## Goal

Make it visible where the tokens in this session actually went. Not guesses — evidence. Output: "do these 3 things next time and you save ~X%."

## Step 1 — Capture current cost

```bash
/cost
```

Note the output: total tokens, input/output split, cache hit rate, total $.

## Step 2 — Find the leaks

Scan the transcript for these signals:

| Signal | How to detect it | Why it wastes tokens |
|---|---|---|
| Unnecessary file reads | `Read` calls touching `node_modules/`, `dist/`, `*.lock`, `coverage/` | Missing `.claudeignore` |
| Re-reading the same file | Same path appears in multiple `Read` calls | Context lost — `/compact` should have happened earlier |
| Reading entire large files | `Read` without `limit` on files >500 lines | Should have used `offset`/`limit` or `Grep` |
| Bash + grep/cat/find | `Bash` calls to `grep`, `cat`, `find`, `ls -R` | Dedicated tools (`Grep`/`Glob`/`Read`) are cheaper and more precise |
| Vague prompt → many tool calls | Single-word asks ("improve", "fix", "look") followed by 5+ tool calls | Prompt wasn't specific |
| Repeated onboarding research | Same concept re-discovered across sessions | Belongs in `CLAUDE.md` |

## Step 3 — Report

Give the user a report in this shape:

```
## Session summary
- Total: <tokens> (<$>)
- Cache hit: <%>

## Top 3 leaks
1. [Evidence]: X files under src/components/ were read in full; ~Y tokens combined
   Fix: add to .claudeignore → <lines>
   Estimated savings: ~Z%

2. ...

3. ...

## Action list
- [ ] Create .claudeignore with <lines>
- [ ] Add a "<topic>" section to CLAUDE.md
- [ ] Use `/compact <hint>` earlier in long sessions
```

## Step 4 — Optional auto-fixes

If the user approves:
- Create `.claudeignore` if missing, add the detected paths
- Create a `CLAUDE.md` scaffold if missing, seed it with the repeated-research topics
- Suggest a specific `/compact` hint phrase for this project

## Rules

- **No guessing** — only report what's in the transcript
- **Always a number** — not "a lot", but "12,400 tokens"
- **Action-oriented** — every finding ends with a concrete command or edit
- **Keep it short** — 3 top leaks is plenty; skip the long tail
