---
name: checkpoint
description: Fast pre-/clear state save. Rewrite the current project's state
  note in the hosted brain from the live session. Use before /clear, when asked
  to "checkpoint", or to save resume state without waiting for a full reflect.
---

# checkpoint

The cheap half of /reflect: one project, one note, about a minute. You are
saving the thread so a fresh session can pick it up, not consolidating the
brain. The full pass (digests, distillation, compaction) still happens later
through /reflect. Do not duplicate its work here.

The brain is the hosted MCP server `brain` (Supabase is the store). Every
step below is an MCP tool call. There is no local checkout, no git, and no
index to touch. If the brain tools are deferred, load them first with
ToolSearch `select:mcp__brain__state_get,mcp__brain__state_write`.

Runs INLINE in the main conversation, never as a background fork. A
checkpoint is invoked moments before /clear or quitting, and a background
agent spawned at that moment dies with the session before it writes. When
the report line appears, the note is stored and leaving is safe.

## Steps

1. **Identify the project.** Take it from the session: the repo basename,
   the cwd basename, or what the session was about. Call
   `state_get(project)`. `found: false` means a new project; that is fine,
   the write creates the note.

2. **Rewrite the note wholesale, never append.** Call
   `state_write(project, body, description)`:
   - `description`: the current one-line status, 150 characters or less.
   - `body` (about 25 lines at most): open with one plain-language line
     saying what the project is, then **Task**, **State (with evidence)**
     where every claim carries a sha, verdict, or `file:line`, **Decisions**
     (with the why), **Next actions** (most important first), **Pointers**
     (paths and commands verified this session). Absolute dates only. Same
     redaction bar as memories: no secrets, no credentials, no long
     transcript quotes, no client data beyond what the next session needs.
   The server stamps `written` itself; the SessionStart brief trusts that
   stamp for freshness.

3. **Touch nothing else.** No `reflect_claim`, no `reflect_complete`, no
   summaries, no other memory. A checkpoint is not a reflection and must not
   advance the reflect watermark.

4. **Report in five lines or fewer:** the project, the gist of what the note
   now says, and the next action it records. If `state_write` returned an
   error (an auth error means the sign-in expired: run `/mcp` and sign in
   again), say so plainly instead.
