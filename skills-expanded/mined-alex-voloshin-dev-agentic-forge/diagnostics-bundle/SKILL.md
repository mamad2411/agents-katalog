---
name: diagnostics-bundle
description: Package this repo's agentic-forge diagnostics (the audit + diagnostics logs, environment, and plugin/config metadata) into ONE redacted, consistently-named zip in ~/Downloads, covering the last 7 days (or a user-given window), to share with a maintainer. Manual utility — run it when asked to collect / package / export the plugin diagnostics or "bundle up what the plugin did".
disable-model-invocation: true
allowed-tools: Bash
---

# Diagnostics bundle

Package the plugin's own diagnostics for the current repo into a single redacted zip that a
maintainer can analyze — the audit trail, the diagnostics log, an environment snapshot, and the
plugin/config metadata, plus a generated `README.md` and `log-summary.txt`. A thin wrapper over the
tested `agentic_forge.diag_bundle` lib (ADR 0052/0053).

## When to use

When asked to collect, package, export, or share the agentic-forge diagnostics for debugging the
plugin. Not for reading a single log in place (use `dev/audit_digest.py` / `dev/diagnostics_digest.py`)
and not for the plugin's own SDLC work.

## Steps

1. Pick the window: default **7 days**; use the number the user gave (e.g. "last 30 days" → 30).
   Full history is `--days 0`.
2. Run the shipped packager from the repo you want to bundle (default: current directory):

   ```bash
   python3 -E "${CLAUDE_PLUGIN_ROOT}/skills/diagnostics-bundle/scripts/build_bundle.py" --days 7
   ```

   Add `--repo /path/to/repo` to bundle a different repo. It writes strictly to
   `~/Downloads/agentic-forge-diagnostics-<YYYYMMDD-HHMMSS>.zip` (UTC stamp) and prints the path.
   `--home /path` (or `AGENTIC_FORGE_HOME`) points it at another home — the eval stand uses a
   seeded `./fake-home` so a run never reads the operator's `~/.claude` or writes their Downloads.
3. Report the output path, the covered window, and the audit/diagnostics record counts by
   **quoting the command's three lines verbatim** — `Diagnostics bundle written to:` (an
   absolute path: the operator may be in another directory when they go looking for the file),
   `Window:` and `Records:`. Do not shorten the path to a relative one for readability: a live
   session did, and the report stopped saying where the file is (ADR 0098). The counts were never
   printed before ADR 0096, so the answer used to require opening the zip.
   The bundle is already redacted — logs are hook-redacted at write time and the
   config/settings slices are re-redacted (the settings slice keeps only enablement + hooks, never
   tokens), so it is safe to share.

## Notes

- Consistent by contract: same filename shape and same internal layout every run, so bundles sort
  by time and are easy to find in `~/Downloads`.
- The window filters records by timestamp; records that predate audit timestamps (legacy) are
  retained rather than silently dropped.
- Details of the manifest, redaction, and windowing live in the lib and its tests
  (`tests/test_diag_bundle.py`); see `docs/architecture/scheduling-observability.md`.
