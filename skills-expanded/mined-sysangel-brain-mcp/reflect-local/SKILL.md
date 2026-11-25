---
name: reflect-local
description: Local-mode consolidation (git + SQLite store, no hosted server). Refresh the index, review sessions since the
  last reflection, distill durable facts into memory files, compact the store,
  propose skills, commit. Use when asked to "reflect" or "consolidate memory";
  also invoked headless by brain-autoreflect when
  BRAIN_REFLECT_SKILL=/reflect-local.
---

# reflect-local

You are running the brain's consolidation pass. The brain lives at
`~/src/brain`: `memories/` is the declarative store (markdown, git = source of
truth), `cache/brain.db` is a disposable derived index. Work directly; be
economical — in headless mode nobody is watching, so never ask questions and
never wait.

## Steps

1. **Sync, then refresh the index.** First, best-effort pull:
   `uv --directory ~/src/brain run brain-sync pull` — on failure (offline, no
   remote, or a `cache/sync-conflict` flag) note it in the report and continue;
   it never blocks the pass. Then `uv --directory ~/src/brain run brain-ingest`
   (incremental; near-instant when nothing changed).

2. **Find the review window.** Read `~/src/brain/cache/last-reflect` (ISO
   timestamp). Missing file → default to the last 48 hours.

3. **Pull the time slice.** Query the index directly for episodes since then:
   `sqlite3 ~/src/brain/cache/brain.db "SELECT ts, session_id, cwd, substr(text,1,600) FROM episodes WHERE ts > '<last>' AND is_sidechain = 0 ORDER BY ts"`.
   Read full exchanges only where the slice looks consequential
   (decisions, corrections, new facts) — not routine tool chatter.

4. **Write session digests.** Find digest-worthy sessions from the index
   with exactly this query — the `strftime` format string is load-bearing
   (episode `ts` is ISO-8601 with a `T` separator, so a bare `datetime('now')`,
   which uses a space, would break the lexical `-1h` comparison and let live
   sessions through). Do not improvise it:

   ```sql
   SELECT session_id, count(*) AS n, sum(length(text)) AS chars,
          substr(min(ts),1,7) AS ym, substr(min(ts),1,10) AS day, cwd
   FROM episodes
   WHERE is_sidechain = 0
   GROUP BY session_id
   HAVING (n >= 3 OR chars >= 15000)
      AND max(ts) < strftime('%Y-%m-%dT%H:%M:%S', 'now', '-1 hour')
   ORDER BY max(ts) DESC;
   ```

   **Privacy denylist:** drop any candidate whose `cwd` contains a substring
   listed in `BRAIN_DIGEST_EXCLUDE` (config env var; e.g. personal-finance projects)
   — those are never digested and never written to `summaries/`. For each
   remaining session, skip it if `~/src/brain/summaries/*/<session_id>.md`
   already exists — unless its current episode count (`n`) is at least double
   the `episodes:` value in that file's frontmatter (a resumed session), in
   which case **rewrite the digest in place at that exact glob-matched path** —
   never recompute the `YYYY-MM` directory on a rewrite, or an old-month copy
   would survive and double-index the session. Take at most **5** per night,
   newest first; leftovers wait for the next night. For each selected session,
   read its episodes from the index (`SELECT ts, substr(text,1,2500) FROM
   episodes WHERE session_id = '<id>' AND is_sidechain = 0 ORDER BY ts`; pull
   more of an episode only when the slice is clearly consequential) and write
   `summaries/YYYY-MM/<session_id>.md` (new digests only — `YYYY-MM` from the
   first episode's ts); frontmatter `session_id, date, project` (basename of
   cwd), `cwd, host` (`hostname -s`), `episodes` (count), `description` (one
   line, **≤150 chars**); body ≤ **~1,800 chars**: what happened, decisions,
   facts learned, files touched, outcome. Same bar as memories: never
   secrets/credentials, no transcript quotes longer than a sentence.

5. **Review usage.** Run
   `uv --directory ~/src/brain run brain-usage-report --days 30`.
   One command, compact output; if it fails or reports no usage DB, note
   that in the final summary and continue — usage telemetry is optional,
   lossy signal. Treat its three lists as leads, not orders:
   - *never-recalled*: memories with zero recall hits and zero opens in the
     window → merge/demotion candidates for the Compact step. Delete only
     if the content is also judged dead — low traffic alone is not a death
     sentence for rarely-needed reference facts.
   - *gap queries*: recalls whose best hit was weak or empty → while
     distilling, check whether the reviewed sessions contain a durable fact
     that would have answered them; if so, that's a NEW memory candidate
     (cluster near-duplicate queries yourself before deciding).
   - *most-opened*: items whose full text was fetched most often (explicit
     opens count double) → promotion candidates: ensure each has a crisp,
     current memory; an episode opened repeatedly deserves distillation.

6. **Distill.** For each durable fact, check for an existing memory first
   (grep `memories/` descriptions); update rather than duplicate; delete
   memories the new sessions contradict. The bar for a NEW memory:
   *would knowing this change behavior in a future session?* Types:
   `user` (identity, preferences), `feedback` (corrections on how to work —
   include **Why** and **How to apply**), `project` (goals, decisions,
   constraints not derivable from code or git), `reference` (URLs, dashboards,
   tickets). Never store: secrets or credentials, anything derivable from a
   repo's code/history, one-off task details, transcript excerpts longer than
   a sentence — reference session ids instead.

7. **Refresh per-project state notes.** For each project with ≥1 non-sidechain
   episode since the review window opened — excluding any whose cwd/project
   matches `BRAIN_DIGEST_EXCLUDE`, and only for projects substantive enough to
   have produced a digest — (re)write a single living note at
   `memories/<project>-state.md` (`<project>` = basename of cwd). **Overwrite it
   wholesale; never append.** Frontmatter: `name: <project>-state`, `description`
   (≤150 chars, the current one-line status), `metadata.type: project`, `date:`
   = today (UTC), `written:` = the current full UTC ISO timestamp (e.g.
   `2026-07-04T18:22:03Z`) — the SessionStart hook's freshness math trusts this
   stamp over git/mtime, so never omit or backdate it. Body (≤~25 lines): **Task** (current objective), **State (with
   evidence)** — every claim carries a commit sha / verdict / `file:line` /
   digest session id, **Decisions** (with the why; not to be re-litigated on
   resume), **Next actions** (single most important first), **Pointers**
   (paths/commands/URLs verified this pass). Same redaction bar as memories. For
   a project with **no** activity this pass: leave its note untouched if its
   newest episode is < `BRAIN_STATE_STALE_DAYS` (default 30) old; otherwise
   `git mv` the note to `memories/archive/<project>-state.md` (archived: still in
   git, no longer indexed). If a reactivated project has a stale
   `memories/archive/` copy, `git rm` it after writing the fresh top-level note.
   These notes are injected automatically at session start by the
   `brain-session-start` hook and are the deep-resume target read by `/catchup`
   — both at exactly `memories/<project>-state.md`.

8. **Compact.** This is what keeps the brain from rotting. If `memories/` has
   more than ~50 files, or any file exceeds ~20 lines of body, merge
   near-duplicates and rewrite verbose entries denser. Delete dead facts
   outright — git history is the archive. Also repair duplicate
   frontmatter/body lines left by union merges (the sync driver concatenates
   both sides of a same-file edit; this pass is the semantic deduplicator).
   `*-state.md` files are living per-project state — exempt from the ~50-file /
   ~20-line-body caps and never merged into another memory; they are rewritten
   wholesale by step 7.

9. **Mine for skills.** If the window shows the same multi-step workflow
   performed twice or more, or a repeated correction to how a task is done,
   write a short proposal to `~/src/brain/proposals/YYYY-MM-DD-<slug>.md`
   (what repeated, proposed skill name, rough steps). Propose only — the user
   promotes proposals to `~/src/skills` themselves.

10. **Re-index and commit.** Run `brain-ingest` again to pick up memory and
   digest edits. Write the current UTC ISO timestamp to `cache/last-reflect`.
   Then one commit of `memories/` + `proposals/` + `summaries/`:
   run git as plain `git add` / `git commit` from the repo root — the session
   already runs with cwd `~/src/brain`, and the headless allowlist matches the
   plain shapes (`-C`/`cd &&` variants may be permission-gated). Message
   `reflect: YYYY-MM-DD — N added, N updated, N pruned, N digests` with trailers
   `Host: <hostname -s>` and, when the env var exists,
   `Session: $CLAUDE_CODE_SESSION_ID`. Then push:
   `uv --directory ~/src/brain run brain-sync push` — best-effort and
   non-fatal; on failure note it in the report and continue (the commit rides
   the next successful sync).

11. **Report.** End with a ≤10-line summary: window reviewed, memories
   added/updated/pruned (by name), digests written (by session id), proposals
   written, index counts. In headless mode this lands in the log — keep it
   grep-able, one item per line.

## Guardrails

- Nothing in the window worth keeping is a fine outcome: write
  `cache/last-reflect`, commit nothing, report "no durable facts".
- Never edit files outside `~/src/brain`.
- Never write to `local/usage.db`; read it only via `brain-usage-report`.
- If ingest or the DB errors, report the error and stop — do not improvise
  schema changes during a reflection pass.
- Sync failures never abort a reflection: a failed pull or push is noted in the
  report and the pass continues. If `cache/sync-conflict` exists, report it —
  do not resolve it headless; a human clears it with ordinary git.
