---
name: handoff
description: Relay session state across /clear. At the end of a session, /handoff
  writes a briefing note to the brain; at the start of a fresh session, /handoff
  reads the latest note and picks the work back up. Use when asked to "hand off",
  "write a handoff", or "handoff resume".
---

# handoff

Session-state relay across /clear, for keeping sessions fresh without losing
the thread. Notes live in the hosted brain as `handoff` documents
(`handoffs/<UTC timestamp>-<slug>.md`), written and read through the brain
MCP tools `handoff_write` and `handoff_latest`. The nightly git export
copies them to the repo, so write nothing you would not commit.

If the brain tools are deferred, load them with ToolSearch
`select:mcp__brain__handoff_write,mcp__brain__handoff_latest,mcp__brain__recall`.

## Mode selection

- Fresh session: this invocation is the first substantive message (right
  after /clear), so use **resume mode**.
- Real work exists above in the conversation: **write mode**.
- Explicit args always win: `/handoff write`, `/handoff resume`, or
  `/handoff resume <topic or date>`.

## Write mode

1. Distill THIS session into a briefing a context-free session can act on.
   A briefing, not a transcript:
   - **Task**: what we were working on and why.
   - **State**: done, in progress, blocked, with evidence (verdicts, test
     results, commits).
   - **Decisions**: calls the user made this session. The next session must
     not re-litigate these.
   - **Next steps**: the single concrete first action, then the ordered queue.
   - **Pointers**: exact file paths, commands, branches, doc locations.
   - **Open questions**: only the unresolved ones.
2. Call `handoff_write(slug, body, description, project)`: `slug` is a short
   task slug, `description` one line, `project` the repo or directory the
   work lives in. Start the body with a `# Title` line. The server picks the
   UTC timestamp, so names sort chronologically and "latest" just works.
3. Tell the user the note is written and they can /clear. Then END the reply
   with the exact kickoff for the next session in a fenced code block, so the
   user can paste it without thinking:
   - default: `/handoff`
   - if this note might not be the newest by then: `/handoff resume <slug>`
   - if the next session should skip straight to a specific action, put that
     full prompt in the block instead (`/handoff` on one line, then the
     one-line instruction).
   A handoff that does not tell the user what to paste next is incomplete.

## Resume mode

1. Call `handoff_latest()` for the newest note, or `handoff_latest(topic)`
   when args name a topic or date.
2. Brief the user: task, state, decisions already made, and lead with the
   first concrete next action. Flag the note's age if it is more than about
   two days old; the world may have moved.
3. If the note references specs, plans, or files, verify the key ones still
   exist before acting on them. `recall` can fill gaps the note does not
   cover.
4. If the first next step is unambiguous, propose it and get to work;
   otherwise present the queue and let the user pick.
