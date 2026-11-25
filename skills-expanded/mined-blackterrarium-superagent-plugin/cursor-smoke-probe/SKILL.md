---
name: cursor-smoke-probe
description: Use when asked to run the cursor smoke probe (or "superagent cursor probe") — verifies the Cursor build of the superagent plugin is loaded and reports environment facts for the port smoke test.
---

# Cursor smoke probe

Perform these checks with your file/shell tools, then output ONLY the report block below —
no extra prose before or after it.

1. Determine this skill file's own location and derive `plugin_root` = the directory two levels
   above it (the directory containing `skills/` and `templates/`). If you cannot determine the
   file's location, report `unknown`.
2. Check whether `<plugin_root>/templates/superenv.default` is readable; capture its first line.
3. Check `<plugin_root>/skills/superloop/SKILL.md`: does it exist; does it contain the string
   "GENERATED FILE — Cursor build" (a correct Cursor build MUST); does it contain the string
   "cc-only" (a correct Cursor build must NOT — that would be marker leakage from the build).
4. Report the CLAUDE_PLUGIN_ROOT environment variable: `echo "${CLAUDE_PLUGIN_ROOT:-unset}"`.
5. Check whether `<plugin_root>/scripts/role-bridge.sh` exists and is executable.

Report block (fill every value):

    PROBE-BEGIN
    plugin_root: <absolute path, or unknown>
    superenv_default_readable: <yes|no>
    superenv_first_line: <the line, or n/a>
    superloop_skill_present: <yes|no>
    superloop_has_cursor_banner: <yes|no>
    superloop_marker_leakage: <yes|no>
    env_claude_plugin_root: <value, or unset>
    role_bridge_present: <yes|no>
    PROBE-END
