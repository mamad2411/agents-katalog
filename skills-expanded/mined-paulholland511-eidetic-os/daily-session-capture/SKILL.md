---
name: daily-session-capture
description: Nightly capture of the day's Cowork chat transcripts into the vault as session-log notes.
---

Capture every Cowork session from the last 24 hours into the vault as a clean,
self-describing markdown note, so your work is searchable alongside the rest of
your knowledge base.

> **Recommended default is twice daily.** Most users are better served by the
> `morning-session-capture` + `afternoon-session-capture` pair (each with a
> 12-hour window), so the day's work lands in the vault closer to when it
> happened and a long-running machine never loses a full day to a single missed
> run. Use this once-a-day skill if you prefer a single nightly capture; set
> `SESSION_CAPTURE_FREQUENCY=daily` to document that choice.

> Placeholders: replace `{{VAULT_PATH}}` with your vault path (the `VAULT_PATH`
> env var). Scripts live in the Eidetic OS `scripts/` directory referenced as
> `{{EIDETIC_OS}}/scripts`.

**Objective:** Save the day's Cowork chat transcripts to
`{{VAULT_PATH}}/sessions/` as `session-log-YYYY-MM-DD-<title>.md` notes — one per
session — and confirm what was captured.

**Steps:**

1. Request access to `{{VAULT_PATH}}`
2. Run the capture, scoped to the last 24 hours and routed through the audit
   trail as an unattended run:
   ```bash
   EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} eidetic session save --since 24h --json
   ```
3. The command will:
   - Read Cowork session metadata + transcripts from the local session store
     (`~/Library/Application Support/Claude/local-agent-mode-sessions/` on macOS)
   - For each new or changed session in the window, extract the title, date,
     duration, message counts, tools used, and files modified
   - Write one markdown note per session under `{{VAULT_PATH}}/sessions/`, with
     `[session-log, cowork]` frontmatter and a `session_id`
   - Advance the watermark in `{{VAULT_PATH}}/.eidetic/last_session_save.txt` so the
     next run only picks up newer sessions (re-running is safe — notes are keyed
     by session id and overwritten in place)
4. Parse the JSON summary (`new`, `discovered`, `saved`, `out_dir`) and report:
   - How many sessions were captured and where they landed
   - If `new` is 0, just say "No new sessions since the last capture"
5. Optionally enrich: for any notably long or important session, open its note
   and tighten the **Summary** into a one-paragraph narrative of what was
   accomplished. Leave the **Key Actions** and **Files Modified** sections as the
   script generated them.

**If the session store is missing or empty:** the command exits cleanly with
`new: 0` — note that there was nothing to capture and stop. Do not invent
sessions.

**Constraints:**
- Typically scheduled nightly (e.g. ~23:30, after the day's work).
- Do NOT modify any vault notes other than those under `sessions/` and the
  `.eidetic/last_session_save.txt` watermark.
- Session notes contain your own conversation summaries — keep them in the
  private vault; never copy them elsewhere without asking.
