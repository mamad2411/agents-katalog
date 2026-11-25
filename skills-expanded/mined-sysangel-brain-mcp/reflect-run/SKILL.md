---
name: reflect-run
description: The brain's full consolidation pass. Review sessions since the last
  reflection, write session digests, distill durable facts into memories,
  refresh per-project state notes, compact, propose skills, and advance the
  reflect watermark, all in the hosted brain. Normally started headless by
  /reflect; run it directly only when a foreground full pass is wanted.
context: fork
model: opus
---

# reflect-run

You are running the brain's consolidation pass in an isolated subagent. The
invoking session's context is not available and is not needed: everything
you review comes from the hosted brain (MCP server `brain`, Supabase
underneath). Sessions reach it through each device's `brain-push` hook, so
the in-flight session is usually there already. Work directly; be
economical. Nobody is watching, so never ask questions and never wait.

Every step is a brain MCP tool call. There is no local checkout, no git, and
no SQLite index. If the tools are deferred, load only the ones this pass
calls with ToolSearch
`select:mcp__brain__reflect_claim,mcp__brain__reflect_complete,mcp__brain__reflect_window,mcp__brain__reflect_sessions,mcp__brain__session_episodes,mcp__brain__summary_write,mcp__brain__get_episode,mcp__brain__recall,mcp__brain__remember,mcp__brain__memory_update,mcp__brain__memory_set_status,mcp__brain__state_get,mcp__brain__state_write,mcp__brain__proposal_write`.
Do not load `device_token_create`, `device_token_list`, `device_token_revoke`,
or `device_token_revoke_hash`. If any call fails with an auth error, stop
and report "brain sign-in expired: run /mcp and sign in again".

## Steps

1. **Claim the review window.** `reflect_claim()`. `ok: true` returns the
   claim `id` (keep it for step 9) and `window_start`, which is `<last>` for
   step 2. `ok: false` means another pass holds the lease: **abort the whole
   pass** and report who holds it and since when. Never fall back to a
   default window on a failed claim.

2. **Pull the time slice.** `reflect_window(since=<last>)`, paging with
   `offset` while `total` says there is more. Each episode carries `ts`,
   `session_id`, `cwd`, `scope`, and the first 600 characters. Keep each
   session's `scope` in view; step 5's stamping rule needs it. Read more of
   an exchange (`get_episode(id)`) only where the slice looks consequential:
   decisions, corrections, new facts. Skip routine tool chatter.

3. **Write session digests.** Loop `reflect_sessions(limit=5)` until it
   returns an empty list or **15 digests have been written in this pass**.
   Each call returns sessions that need one: at least 3 episodes or 15,000
   characters, idle for an hour, and either undigested or grown to double
   the episodes their digest covered (`rewrite_of` is set then).
   Privacy-excluded projects (`BRAIN_DIGEST_EXCLUDE` on the server) are
   already dropped. For each, read it with `session_episodes(session_id)`
   and call
   `summary_write(session_id, body, description, project, cwd, episodes)`:
   `project` is the basename of cwd, `episodes` the count you digested,
   `description` one line of 150 characters or less, body about 1,800
   characters at most: what happened, decisions, facts learned, files
   touched, outcome. A rewrite keeps the existing path on its own. Never
   secrets or credentials, no transcript quotes longer than a sentence, and
   no client data beyond what a future session needs to act. Later nightly
   passes drain any remainder.

4. **Usage review is not available on the hosted store yet.** Say so in the
   report and continue.

5. **Distill.** For each durable fact, `recall` first (scope `memories`) to
   find an existing memory; update rather than duplicate with
   `memory_update(id, fact)`; retire memories the new sessions contradict
   with `memory_set_status(id, "forgotten")`. A new memory goes through
   `remember(fact, type, name, project=...)`. The bar for a NEW memory:
   *would knowing this change behavior in a future session?* Types: `user`
   (identity, preferences), `feedback` (corrections on how to work; include
   **Why** and **How to apply**), `project` (goals, decisions, constraints
   not derivable from code or git), `reference` (URLs, dashboards, tickets).
   Never store secrets or credentials, anything derivable from a repo's code
   or history, one-off task details, or transcript excerpts longer than a
   sentence; reference session ids instead.

   **Scope stamping:** a NEW general-knowledge memory (`user`, `feedback`,
   `reference`) distilled solely from episodes carrying `scope: work` gets
   `scope="work"` on `remember`. A fact drawn from mixed or unscoped sessions
   stays shared (omit `scope`). `project` memories and state notes are NEVER
   scoped, and reflect never stamps `personal`.

6. **Refresh per-project state notes.** For each project with at least one
   episode in the window and enough substance to have produced a digest
   (excluded projects stay out), `state_get(project)` then
   `state_write(project, body, description)`. **Overwrite wholesale; never
   append.** `description` is the current one-line status (150 characters
   or less). Body (about 25 lines): one plain-language line on what the
   project is, then **Task**, **State (with evidence)** where every claim
   carries a commit sha, verdict, `file:line`, or digest session id,
   **Decisions** (with the why), **Next actions** (most important first),
   **Pointers**. The server stamps `written`; the SessionStart brief trusts
   it. For a project with **no** activity this pass whose newest episode is
   older than 30 days (`BRAIN_STATE_STALE_DAYS`), retire its note with
   `memory_set_status(<note id from state_get>, "archived")`.

7. **Compact.** Keep the memory set lean. Use `recall` (scope `memories`)
   around the topics this window touched to find near-duplicates and
   verbose entries; merge with `memory_update` on the keeper and
   `memory_set_status(id, "forgotten")` on the rest. State notes are exempt
   from merging; step 6 rewrites them.

8. **Mine for skills.** If the window shows the same multi-step workflow
   performed twice or more, or a repeated correction to how a task is done,
   write `proposal_write(slug, body, description)` (what repeated, proposed
   skill name, rough steps). Propose only; the user promotes proposals.

9. **Complete.** `reflect_complete(id)` with the claim id from step 1. It
   advances the watermark to the claim time and drops the lease. Run it even
   on an empty pass.

10. **Report.** End with a summary of 10 lines or fewer: window reviewed,
    memories added, updated, retired (by name), digests written (by session
    id), state notes refreshed, proposals written. One item per line. This
    final message is the skill's return value; headless, it lands in the
    log.

## Guardrails

- Nothing in the window worth keeping is a fine outcome: still call
  `reflect_complete`, then report "no durable facts".
- If a tool call is denied or errors, say so explicitly in the report (which
  tool, which error) and continue with what you can reach. A silently
  skipped step looks like a clean pass.
- Never write files on disk and never run git; the hosted store and its
  nightly export own persistence.
- Do not improvise schema or data fixes during a reflection pass. Report the
  error and stop.
