---
name: shutdown
description: Graceful Willow 2.0 session close — resolve flags, write handoff, audit KB, run full pipeline
---
@markdownai

# /shutdown — Willow 2.0 Graceful Close

Stack position: this skill is the **end-of-session persistence** layer — it absorbed the former `/handoff` skill, so the handoff write is step 2 of this sequence, not a separate skill. See the Persistent memory section in `willow.md` for the full 4-layer stack.

## Sequence

1. **Close scan (mechanized)** — run the deterministic pre-handoff scan:
   ```
   willow_run(app_id, allow_net=True, task="python3 -m willow.fylgja.close_scan {AGENT} --apply")
   ```
   One pass does what used to be three model loops: closes provably-finished `process-*` flags
   (pid gone), reconciles every PR-shaped open thread against live `gh pr view`, and lints
   MEMORY.md for entries missing KB atom IDs. Read its JSON:
   - `flags.still_running` → update each flag with current progress (`soil_put`) so the next
     session reads accurate state. `flags.ambiguous` (no pid; log tail attached) → judge from
     the log tail; close or annotate manually. A handoff over a stale flag is a lie.
   - `threads.drop` → these PRs are MERGED/CLOSED and must **not** appear in the handoff. If one
     left genuine follow-up work, write *that follow-up* as the thread — never the merge.
   - `threads.keep` → carry forward with the refreshed `pr_status`. `threads.no_pr_ref` → carry
     or close on judgment.
   - `memory.missing_atom_id` → fix in step 3.

2. **Write the handoff** — this runs early by design: it is the one artifact that must survive
   even if the session dies partway through the steps below.

   a. **Load + reconcile current state** — the step-1 scan already loaded the prior handoff's
      threads and reconciled them against live PR state; write the draft from its
      `threads.keep` + `threads.no_pr_ref` lists plus this session's new threads. Any *new*
      thread you add that references a PR must also be checked (`gh pr view` via Kart) before
      it reaches the draft. Never carry anything from `threads.drop` — a merged PR forwarded
      as "needs merge" is the zombie-thread bug (#402, #444, #446, #481 each lingered across
      sessions this way). The flag state from step 1 must appear in the handoff.

   b. **Draft** — copy [`docs/templates/HANDOFF.template.md`](../../docs/templates/HANDOFF.template.md)
      as the canonical v2 structure:

```
# HANDOFF: <title>
From: {AGENT} (Claude Code, Sonnet 5)
Session: {YYYY-MM-DDx} | Resume: claude --resume {UUID}

## What I Now Understand
<2-3 sentences of architectural truth, not task summary>

## What We Agreed On
<decisions USER ratified this session — include what was ruled out and why>
<format: "Decision: X. Ruled out: Y because Z.">
<omit if session was pure execution with no design conversation>

## Capabilities (persistent — carry forward, update don't rewrite)
| Capability | Location | Status |
|------------|----------|--------|
<what has been built and is available>

## What Was Done
<bullet list — high level, no code details>

## Open Threads
<anything unfinished, blocked, or requiring a decision next session>
<do NOT include things already captured in "What We Agreed On">

## 17 Questions
Q1–Q16: sequential, specific, bite-sized
Q17: "What is the next single bite?"

## Risks / Open Gates
<anything that could break the next session>

## Agent Notes for Human
<the agent's reflections to the operator — reminders, to-dos, unfinished tasks, patterns
 surfaced this session. Max 17 lines.>

## Human Notes to Agent
<leave EMPTY at close. The operator writes here after the session; handoff_latest reads it
 live from the file at next boot.>

## Machine block for handoff_rebuild / kb_ingest
<the content JSONB from step 2c, fenced as ```json — required for handoff_rebuild to parse>
```

   c. **Write to KB** — call `kb_ingest` with `category="handoff"`, `source_type="session"`,
      `title="Session handoff {YYYY-MM-DD} — {one-line summary}"`, `summary` = the prose
      narrative (~500 chars), and `content` JSONB:
      ```json
      {
        "summary": "<prose narrative>",
        "open_threads": ["<thread 1>", "..."],
        "agreements": ["<decision + ruling>", "..."],
        "key_actions": ["<action 1>", "..."],
        "next_steps": ["<Q17>", "<Q16>", "..."],
        "tools_used": ["kb_ingest", "fleet_status", "..."],
        "signals": {"health": "ok|degraded", "grove": "up|down"},
        "compact_receipt": null
      }
      ```
      Set `compact_receipt` to `{"tokens_before": N, "tokens_after": M, "turns_dropped": K}` if
      context was compacted this session, otherwise `null`.

   d. **Write markdown file** — submit a Kart task using `script_body` to call
      `willow.fylgja.handoff_write.write_session_handoff(agent, body)`. This writes the
      canonical v2 YAML frontmatter and body to
      `$WILLOW_HOME/handoffs/{agent}/session_handoff-{date}{letter}_{agent}.md`
      (`~/github/.willow`; `~/.willow` alias OK). Do NOT write manually to `docs/handoffs/` —
      deprecated, not indexed. Example script_body:
      ```python
      from willow.fylgja.handoff_write import write_session_handoff
      path = write_session_handoff("willow", """# HANDOFF: ...\n...""")
      print(path)
      ```

   e. **Write FRANK ledger entry** — call `ledger_write` with `event_type="check_in"`,
      `summary`, `shipped` (list), `open_decisions` (list), `atoms_written` (every `kb_ingest`
      ID this session — required if any), `gaps_flagged`, `next_bite` (Q17 verbatim).

   f. **Rebuild DB** — call `handoff_rebuild` so the next session's `handoff_latest` returns
      current state.

   g. **Confirm** — report the KB atom ID, markdown file path, and Q17.

3. **KB close audit** — for every task completed or closed this session, verify its KB atom
   reflects the resolution. Search with `kb_search` for each task name. If the atom says the
   task is open or unsolved, update it with `kb_ingest` (new atom) marking it resolved and
   citing the commit or output. This step exists because atoms written at task-open never get
   updated on close — that's what causes rediscovery loops in future sessions.

   Also check: did this session discover new patterns, governance gaps, conflicts of interest,
   or durable lessons? Each one requires **all three** of the following — not a subset:
   1. A memory file written to `~/.claude/projects/.../memory/<type>_<slug>.md`
   2. A one-line entry added to `MEMORY.md` with the KB atom ID
   3. A KB atom ingested via `kb_ingest`

   A Grove post is communication, not memory. Scan MEMORY.md entries added this session — any
   entry missing a KB atom ID is incomplete. Fix before closing. If patterns were extracted but
   edges are missing, add them now with `soil_add_edge`.

   If this audit changes open threads or agreements materially, amend the handoff (re-run 2c–2f
   for the delta) — cheap compared to a wrong handoff.

3b. **Handoff gate** — verify the file written in step 2 passes the v2 completeness check:
   ```
   python3 scripts/session_close.py --check-handoff ${WILLOW_AGENT_NAME}
   ```
   On REJECT, fix the handoff (missing sections, empty Open Threads, no Q17) before continuing.
   A handoff that fails the gate will not surface via `handoff_latest`.

4. **Memory audit** — run `/health memory` to check for STALE/DEAD/REDUNDANT/DARK records. Archive or fix before closing.

5. **Run the close pipeline** — the Stop hook is now cleanup-only. Run the full pipeline explicitly:
   ```
   Bash: "${WILLOW_ROOT:-$(pwd)}/willow.sh" exec-python -m willow.fylgja.events.shutdown
   ```
   **Pipeline stages:**
   - `mark_session_clean` — track successful session close
   - `run_grove_ingest` — pull new Grove channel messages
   - `run_compost` — ingest session activity summary
   - `run_atom_synthesis` — Phase 3: extract atoms missed by hooks
   - `run_edge_linking` — Phase 4: connect atoms into knowledge graph
   - `run_feedback_pipeline` — process any pending feedback
   - `run_handoff_rebuild` — rebuild handoffs DB
   - `close_session` — mark session complete in SAFE
   - `run_ingot` — cat observation from local model

5b. **Norn pass (the pump)** — promote pending intake records so nothing buffers unpumped:
   `intake_schedule(app_id=<agent>, days=1)` then `kart_task_run(app_id=<agent>)`.
   Weekly or after heavy sessions, run the fleet variant: `intake_schedule_fleet(app_id=<agent>)`.

6. **State the next bite** from Q17. One sentence.

7. **Session Close Report** — the final user-facing output. Render the session's data as
   compact visual **tables** (not prose) so the close is legible at a glance. Pull values from
   the steps above; do not recompute. Omit any table whose data is empty. Keep ~5 rows max per
   table; make IDs/paths/PRs clickable. This is the user's receipt — the last thing they see.

   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     SESSION CLOSE — {agent} · {session}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

   **Shipped** — PRs, commits, releases
   | What | Where | State |
   |------|-------|-------|

   **Memory written** — the session's durable trace
   | Kind | ID / path | Title |
   |------|-----------|-------|
   (KB atoms via `kb_ingest`, the handoff file, the FRANK ledger `check_in`)

   **Flags resolved** — from step 1
   | Flag | Resolution |
   |------|-----------|

   **Open threads** ({N}) — carried to next session
   | Thread | Next action |
   |--------|-------------|

   **Pipeline** — step 5, one line: stages passed / failed.

   **Next bite (Q17):** {one sentence}

## Context-critical mode

When invoked by `/context-sentinel` (HANDOFF_NOW) or when remaining context is plainly too small
for the full sequence: run **steps 1–2 only**, then attempt step 5, then stop. Skip steps 3–4 —
a finished handoff beats a half-finished audit. Never start step 3 or 4 if doing so risks dying
before the pipeline runs.

## Rules

- Never exit without writing the handoff. The next session reads from it.
- The handoff write (step 2) comes before the audits by design — it is the artifact that must
  survive a dying session. Amend it after the audits if they change the picture.
- Never skip the KB close audit (step 3) in a normal close. An unclosed atom is a future rediscovery loop.
- Never skip `handoff_rebuild` or `ledger_write` — the next session boots from both; a missing
  ledger entry means the next session starts blind.
- "What I Now Understand" = architectural truth, not a task list.
- "What We Agreed On" = ratified decisions only — include ruled-out options to prevent
  re-litigation. This section is what makes CC CLI sessions legible to the next agent.
- `open_threads` in the content JSONB is what `handoff_latest` returns. Keep them precise.
- PR-shaped open threads are reconciled by the step-1 `close_scan` *before* the handoff is
  written; new threads added at draft time get the same `gh pr view` check. Never carry a MERGED
  or CLOSED PR forward as an open thread — drop it, or rewrite it as the remaining follow-up.
  This is the step that stops zombie threads.
- Q17 must be a single concrete next bite, not a project description.
- Phases 3+4 (atom synthesis + edge linking) only run if `WILLOW_ATOM_EXTRACTION=1`.
- Stop hook is cleanup-only (depth stack + thread file). Pipeline only runs on explicit /shutdown.
- Step 1 (close scan) is not optional. A handoff written over a stale running flag is incorrect state — the next session will surface it as an open problem that is already solved.
- The draft template must keep **## Agent Notes for Human** and **## Human Notes to Agent** (matching `docs/templates/HANDOFF.template.md` and the v2 parser). Agent Notes = the agent's reflections to the operator; Human Notes = left empty at close for the operator to fill after, read live at next boot. Dropping either breaks parity with `handoff_latest`.
- Step 7 (Session Close Report) is the final user-facing output — always render it. The user should never have to open the handoff file to see what the session did. In context-critical mode the floor is a minimal version: **Shipped** + **Next bite**.
- Do NOT write to `docs/handoffs/` (deprecated, unindexed) or `~/Ashokoa/` (does not exist).
