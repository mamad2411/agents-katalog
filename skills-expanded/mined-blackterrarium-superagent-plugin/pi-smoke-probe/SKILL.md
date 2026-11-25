---
name: pi-smoke-probe
description: Use when asked to run the pi smoke probe (or "superagent pi probe") — verifies the Pi build of the superagent plugin is loaded and reports environment facts for the port smoke test.
---

# Pi smoke probe

Perform these checks with your file/shell tools, then output ONLY the report block below —
no extra prose before or after it.

1. Determine this skill file's own location and derive `plugin_root` = the directory two levels
   above it (the directory containing `skills/`, `templates/`, `scripts/`). If you cannot
   determine the file's location, report `unknown`.
2. Check whether `<plugin_root>/templates/superenv.default` is readable; capture its first line.
3. Check `<plugin_root>/skills/superloop/SKILL.md`: does it exist; does it contain the string
   "GENERATED FILE — Pi build" (a correct Pi build MUST); does it contain "cc-only", "cursor-only",
   or "codex-only" (a correct Pi build must NOT — marker leakage).
4. Do you have a tool named `subagent`? Report `yes` or `no`.
5. Check whether `<plugin_root>/scripts/role-bridge.sh` and `<plugin_root>/scripts/bridge-fanout.sh`
   exist and are executable.

Report block (fill every value):

    PROBE-BEGIN
    plugin_root: <absolute path, or unknown>
    superenv_default_readable: <yes|no>
    superenv_first_line: <the line, or n/a>
    superloop_skill_present: <yes|no>
    superloop_has_pi_banner: <yes|no>
    superloop_marker_leakage: <yes|no>
    subagent_tool: <yes|no>
    role_bridge_present: <yes|no>
    bridge_fanout_present: <yes|no>
    PROBE-END
