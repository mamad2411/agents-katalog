---
name: startup
description: Willow 2.0 boot — anchor, inbox, ledger, KB continuity (config-driven), flags, report
---

@markdownai v1.0

# /startup

> **Recovery path — not the default boot.** Use this skill when boot is degraded, the session anchor is missing/stale, or you need deeper continuity recovery than the normal `willow.md` path.

Default boot with MCP available is the compact 7-step loop: (1) `markdownai-read_file("willow.md")`; (2) establish local operating context with agent, namespace, repo root, branch, and a compact repo diff summary; (3) `fleet_status`; (4) `handoff_latest(app_id=<agent>, workspace=<repo root>)`; (5) `grove_get_history` on the agent channel/inbox; (6) `kb_search` on the current task/topic; (7) stop on degraded base or proceed to act. Keep step 2 compact: branch, clean/dirty, staged/unstaged/untracked counts, ahead/behind if known, and a short diff note, not a full patch. SessionStart already ran status/handoff/flags and wrote `$WILLOW_HOME/session_anchor_{agent}_{project}.json` (or `session_anchor_{agent}.json` when project is unknown; `~/github/.willow` / `~/.willow` alias OK). Re-run the deeper recovery steps below only if the anchor is missing, stale (`written_at` > **2h**), or live MCP boot is degraded.

Stack position: this skill belongs to the **boot persistence** layer. See the Persistent memory section in `willow.md` for the full 4-layer stack.

## Steps

1. Read anchor JSON (path above).
2. **Postgres — live probe, not anchor copy.** The anchor field `postgres` can be `unknown` when SessionStart could not reach MCP. Do **not** report that as the truth. Prefer `fleet_status`: `postgres` is a **dict** ⇒ up. If MCP is missing, times out, or returns non-dict: from the **willow-2.0 repo root** run `pg_isready` (honor `WILLOW_PG_HOST` / `WILLOW_PG_PORT` if set) and one connect + `SELECT 1` against `WILLOW_PG_DB` (default `willow_20`) — e.g. `python3 -c "from core.pg_bridge import try_connect; c=try_connect(); assert c; c.close()"` or `psql`. **Probe success** ⇒ treat as up for the boot paragraph. **Probe failure** ⇒ post `#general`, stop.
3. `grove_get_history(channel={AGENT}, limit=20)` — inbox only; scan since `anchor.written_at` for directed / urgent / Loki.
4. If `/tmp/willow-dispatch-inbox-{AGENT}.json` non-empty → read, surface, delete.
5. Grove LISTEN monitor — `willow/fylgja/skills/grove-persistent-monitor.md` (all msgs on own channel; `@mentions` elsewhere); never `last_id=0`.
6. Flat handoff `$WILLOW_HOME/handoffs/{AGENT}-{today}.md`: if `## JSONL` path present, tail 200 lines; on clean exit signals, close matching `{AGENT}/flags` in `running` / `awaiting authorization`. Else skip.
6b. **Open initiatives** — `soil_list({AGENT}/overseer)` → filter `status != "closed"`. One line per hit: `[<branch>] <goal>`. Empty → skip. Surface count in boot report. (`run_overseer.py` writes this record on worktree creation; KB atom is the fallback via `kb_search("overseer open initiative")` if store is empty.)
7. `ledger_read(project=<agent>, limit=3)` — **mandatory.** Use fleet agent id, not OS username. Newest entry `content.atoms_written` → priority IDs to skim.
7a. **KB continuity** — `kb_startup_continuity(app_id=<boot agent>)` **once** (runs `startup_continuity.json` with curated pool). Skim `results[].top` titles/summaries; `kb_get` only if a hit ties to step 6 gate, step 7 gap, or step 7b open flag. All empty → skip. (Edit `willow/fylgja/config/startup_continuity.json` to tune recall.)
8. `soil_list({AGENT}/flags)` — empty → skip. **>75 records:** B+D only. **Else** A+B+C+D: **close** A dup open vs closed same `subject`; B open+`resolution`; D open+orphan `assigned_to` (fleet from `soil_get({AGENT}/agents,inactive)` else `{Heimdallr}`). **Prompt:** C — open + single-line `fix_path` ≤150c, max 5, wait for USER. Closes: `resolution=auto-closed at boot — …`
9. Report: one paragraph, **≤6 sentences**, no headers — postgres, flags (count + top), latest ledger line, `next_bite`; if 7a reprioritizes work, one extra clause (titles/IDs only).

## Rules

- **Postgres:** Never answer "postgres is unknown" from the anchor alone; always run step 2 probe first when state is not already confirmed up via `fleet_status`.
- No `#general` / `#architecture` / `#handoffs` pulls at boot (on-demand).
- Do not read full handoff `.md` — anchor is enough.
- **Tune KB recall vs tokens** by editing `willow/fylgja/config/startup_continuity.json`, not this file.
- **Path discipline:** `/startup` Cursor/Claude command stubs resolve **FYLGJA** via `WILLOW_FYLGJA_ROOT` or relative `willow/fylgja` / `willow-2.0/willow/fylgja` — never embed machine-local absolute paths in those stubs.
