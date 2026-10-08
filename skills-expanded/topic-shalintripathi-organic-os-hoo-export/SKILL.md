---
name: hoo-export
description: Use to flatten the brain to CSV for BI tools - "export the data", "CSV for Sheets or Looker Studio", /organic-os:export. Read-only over the brain; writes only the dated export folder.
---

# CSV export (your data, no tier gate)

Resolve the brain: use registry.get_active() when running interactively;
scheduled runs receive the brain path from the routine configuration.

0. Run `core.contracts.check_schema(brain_path)` first. If not compatible,
   relay the action string and stop.
1. Run the export via the canonical invocation:
   `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -c` snippet calling
   `core.export.export_all(brain_path)`. It writes
   `runs/<UTCdate>-export/` inside the brain (see
   docs/site-repo-contract.md) and returns the dir, the file list, and a
   skipped-line count.
2. Present the result: each file with its path, plus the skipped-line
   count when it is non-zero ("N signal lines carried a metric token
   that did not parse and were skipped, never guessed at"). A source the
   brain does not have yet (no keyword history, no outcome records) is
   simply absent from the list - say so in one line, no error.
3. One line on usage: import the CSVs into Sheets or Looker Studio
   directly - your data is files in your own repo, so there is no
   locked tier and no gate (ROADMAP, v0.4: commercial tools gate export
   behind top tiers; export here is a right, not an upsell).
4. If the configured approval channel supports documents, offer to send
   the CSVs there (telegram: `core.telegram.send_document` per file;
   in-session: the paths from step 2 are already the delivery; a channel
   that cannot carry a file reports the paths instead - ADR-0009).
5. Commit "export: YYYY-MM-DD" if the brain mode is git.

This skill never mutates signals, items, the skillbook, or the site -
the CSV files under `runs/` are its only writes.
