---
name: resume-claude-here
description: Recover a prior Claude Code session from natural-language hints, search Claude history by topic/date/project, and import the useful context into the current conversation. Use this for Claude session handoff, transcript recovery, context transfer into Codex or another agent, and continuing after Claude hit a usage or rate limit.
---

# Continue Claude Here

Use this skill when the user wants to pull forward prior Claude work into the current conversation.

Primary outcome:

- import the relevant prior session context into the current conversation without switching runtimes

Keep the workflow deterministic. Do not guess a session from vibes alone when there are several plausible candidates.

Default bias:

- Always prefer importing the prior Claude session into the current conversation.
- Treat true Claude reopen or CLI resume as an edge path only if the user explicitly insists on that.

## Tools

- Use `scripts/claude_session_tool.py search` to discover and rank candidate sessions.
- Use `scripts/claude_session_tool.py export` to preview or stage transcript content.
- Use the local `claude` CLI only if the user explicitly asks to reopen Claude itself.

Read [research-notes.md](./references/research-notes.md) only if you need the exact CLI/session behavior that motivated this workflow.

## Workflow

### 1. Classify the user's intent

Pick the primary mode first:

- `import-into-current`: The user wants the current conversation to absorb the prior context.
- `unclear`: Search first, then ask one concise question only if the top candidates are ambiguous.

Unless the user explicitly asks to reopen Claude itself, treat all of these as `import-into-current`:

- "continue"
- "resume"
- "pick up where we left off"
- "bring that chat here"
- "import the transcript"
- "Claude hit the limit"

### 2. Search sessions from the user's language

Run the search helper with the user's wording, not your paraphrase:

```bash
python scripts/claude_session_tool.py search \
  --query "that pdfwiki desktop research from sunday" \
  --cwd "$PWD" \
  --limit 8
```

The helper already ranks by:

- session title or slug
- current and historical working directory
- branch metadata when available
- first prompt and recent user prompts
- recency
- fuzzy similarity and token overlap

Treat the top result as auto-selectable only when it is clearly stronger than the next result. Otherwise present a short ranked shortlist with why each candidate matched.

When the user says they hit a limit, search for the prior Claude session first and transfer context into the current agent. Do not make Claude CLI resume the default.

### 3. Handle match confidence

Use this policy:

- One strong candidate: proceed without asking.
- Several close candidates: show 2-4 candidates with timestamps, project/cwd, and match reasons.
- No strong candidate: widen scope, try a shorter query, or search without cwd bias.

When asking the user to disambiguate, ask one short question and include the concrete candidates.

### 4. Import transcript context into the current conversation

If the user wants the current conversation to inherit prior context, choose between direct import and staged import.

This is the default path when the user was forced to stop because Claude hit a usage or rate limit and now wants to continue in Codex or another agent.

#### Direct import

Use this when the relevant slice is short enough to fit comfortably:

```bash
python scripts/claude_session_tool.py export \
  --session <session-id> \
  --tail 12 \
  --format markdown
```

Then bring in only the useful slice:

- the task framing
- the latest accepted plan
- key decisions, constraints, and unresolved items
- any exact user instructions that still matter
- the stopping point, including any rate-limit or failure message if it explains why the handoff happened

Do not dump a huge raw transcript into the conversation if a targeted slice will do.

#### Staged import through a file

Use this when the transcript is long, the session contains many tool calls, or the user wants a durable artifact:

```bash
mkdir -p .claude-resume
python scripts/claude_session_tool.py export \
  --session <session-id> \
  --format markdown \
  --output .claude-resume/<slug>.md
```

Then read or reference the exported file in chunks. Prefer this path for long sessions because it preserves context without overwhelming the active thread.

### 5. Multiple candidate sessions

When more than one session plausibly matches:

- show session name or fallback summary
- show exact last activity time
- show cwd or project hint
- show one-line reason for the match

Example shortlist format:

```text
1. auth-refactor | 2026-03-18 21:14 | repo=payments-api | matched "oauth" and current branch
2. Fix login tests | 2026-03-17 09:42 | repo=payments-api | matched "auth" but older and no branch match
3. cheerful-launching-stardust | 2026-03-16 14:34 | repo=pdfwiki | matched "research" only
```

If the user does not answer and one candidate is materially better, proceed with the best candidate and say that you inferred it from the stronger match.

### 6. Output discipline

When importing a session, preserve signal and drop noise:

- Prefer user messages, assistant text responses, session titles, and key timestamps.
- Omit repetitive progress lines unless the user explicitly wants the raw transcript.
- Omit tool payloads by default.
- Include tool payloads only when they are the important artifact.
- If the session hit a rate limit or failed, say so explicitly.

### 7. Failure handling

If searching or exporting fails:

- verify the session ID exists in the search results
- retry with a shorter query or without cwd bias
- export by explicit session ID once identified

If the transcript is too large, export to a file and import selectively instead of forcing the whole thing into the live context.

## Decision rule for limit handoff

When the user says some version of "Claude hit the limit":

- assume the target runtime is the current agent unless the user says otherwise
- search for the matching Claude session
- export only the relevant recent portion plus the original task framing
- summarize the state transfer clearly: goal, completed work, pending work, blockers, and last meaningful assistant output
- continue the task here

Do not bounce the user back into Claude unless they explicitly ask for that.

## Explicit reopen edge case

Only if the user explicitly insists on reopening Claude itself, use the local `claude` CLI:

```bash
claude --continue
claude --resume <session-id-or-name>
claude --fork-session --resume <session-id-or-name>
```

Do not present this as the normal path.
