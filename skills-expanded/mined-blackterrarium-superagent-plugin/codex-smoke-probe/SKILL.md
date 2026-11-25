---
name: codex-smoke-probe
description: Use when asked to run the codex smoke probe (or "superagent codex probe") — verifies the Codex build of the superagent plugin is loaded and reports environment facts for the port smoke test.
---

# Codex smoke probe

Perform these checks with your file/shell tools, then output ONLY the report block below —
no extra prose before or after it.

1. Determine this skill file's own location and derive `plugin_root` = the directory two levels
   above it (the directory containing `skills/` and `templates/`). If you cannot determine the
   file's location, report `unknown`.
2. Check whether `<plugin_root>/templates/superenv.default` is readable; capture its first line.
3. Check `<plugin_root>/skills/superloop/SKILL.md`: does it exist; does it
   contain the string "GENERATED FILE — Codex build" (a correct Codex build MUST); does it
   contain the string "cc-only" OR the string "cursor-only" (a correct Codex build must NOT —
   either would be marker leakage from the build).
4. Report the CODEX_HOME environment variable: `echo "${CODEX_HOME:-unset}"`.
5. Check whether `<plugin_root>/scripts/role-bridge.sh` exists and is executable.

Report block (fill every value):

    PROBE-BEGIN
    plugin_root: <absolute path, or unknown>
    superenv_default_readable: <yes|no>
    superenv_first_line: <the line, or n/a>
    superloop_skill_present: <yes|no>
    superloop_has_codex_banner: <yes|no>
    superloop_marker_leakage: <yes|no>
    env_codex_home: <value, or unset>
    role_bridge_present: <yes|no>
    PROBE-END
