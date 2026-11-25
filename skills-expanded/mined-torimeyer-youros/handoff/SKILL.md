---
name: handoff
description: Write a handoff doc capturing current work state — uncommitted changes, recent commits, in-flight agents, open needles, and what to pick up next. Use when the user types `/handoff` or asks for a handoff to another session/machine.
---

# Handoff skill

Write a self-contained handoff document so another session (different machine, tomorrow's session, a teammate) can pick up exactly where this one stopped.

## When to invoke

The user typed `/handoff`, said "write a handoff", or asked for "context for tomorrow / for my work machine / for Scott". If they gave a topic argument (e.g. `/handoff onboarding e2e`), scope the handoff to that thread of work. No argument = capture everything currently in flight.

## What to capture

Run all of these in parallel as one batch (each is a separate Bash/ostk call). Do not skip any. The handoff is only useful if it has receipts.

1. **Branch + uncommitted state**
   - `git status --short` (never `-uall`)
   - `git diff --stat` (staged + unstaged together)
   - `git log --oneline -10` (recent commits for context)

2. **Test status**
   - If unit/e2e tests were run this turn, quote the verbatim summary line (`X passed`, `Y failed`).
   - If not run, say so explicitly. Do not guess.

3. **In-flight agents**
   - `curl -sf --connect-timeout 3 -m 5 -k https://127.0.0.1:8000/api/agents 2>/dev/null | python3 -c "import json,sys; [print(f\"  {a['name']}: {a.get('status','?')} ({a.get('current_step','-')})\") for a in json.load(sys.stdin) if a.get('status') in ('running','queued')]"`
   - If none, say "no agents in flight".

4. **Open needles** (only if relevant to the work)
   - `ostk work list --open --limit 10` for top needles.
   - Skip this section entirely if the handoff is scoped to one specific thread.

5. **Recent decisions / context**
   - From this conversation: what the user explicitly said to do or not do. Quote it.
   - Any deferred follow-ups ("we'll release v3.8.2 after testing onboarding").

## Output format

Write to `~/.claude/handoffs/<YYYY-MM-DD>-<slug>.md`. Slug is 2-4 words from the topic (e.g. `onboarding-e2e-test`, `release-v3.8.2`). If the file exists, append a new dated section instead of overwriting.

Use this structure exactly:

```markdown
# Handoff — <topic>
*Written <ISO date> from <branch> at <short commit hash>*

## Goal
<One sentence: what was this session trying to accomplish?>

## State right now
- Branch: <name>
- Uncommitted: <N files, list paths>
- Last commit: <hash> <subject>
- Tests: <pass/fail summary with counts, or "not run">
- Agents in flight: <list or "none">

## What landed this session
<Bullet list. Each item: what changed + commit hash if committed, or "uncommitted in <path>" if not.>

## What's next
<Numbered list. Each item is a concrete action with a path or command. Lead with the highest-value item.>

## Watch out for
<Gotchas, half-finished work, things that look done but aren't, decisions that could be revisited.>

## Sources to re-read
<Paths to the original spec, plan, and task detail files this work came from. The next session verifies from these, not from the retelling above.>

## Verbatim from this session
<Quote any user instructions that shape the next steps. Path: line format if they came from a file.>
```

## Rules

- **Receipts only.** Every "done" or "fixed" claim must carry a commit hash from `git log` run this turn, or verbatim test output, or a quoted file line. No relayed claims.
- **No em-dashes.** Periods or commas. (User rule, see CLAUDE.md.)
- **Plain language.** No jargon in the prose. Code paths and commands are fine.
- **Don't commit the handoff file.** It lives outside the repo on purpose. Mention the path in your reply so the user can open it.
- **Open the file after writing it** if the user wants to review (`open ~/.claude/handoffs/<file>.md`). Reports get auto-opened per CLAUDE.md.

## After writing

Reply to the user with:
1. The full path to the handoff file (clickable markdown link).
2. A 1-2 sentence summary of what's in it.
3. Nothing else. The file IS the response.
