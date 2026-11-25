---
name: doctor
description: Diagnose Codex plugin, policy, app configuration, agents, skills, and managed-install state without changing it.
---

# Diagnose Codex setup safely

Resolve `POLYTROPOS_ROOT` from this skill's location. In a managed copy use `POLYTROPOS_ROOT="{{POLYTROPOS_ROOT}}"`; reject the literal placeholder. Confirm pricing data, `bin/harness_select.py`, `bin/codex_policy.py`, and `bin/codex_app_policy.py` exist. If they do not, stop rather than guessing a path.

Run the read-only doctor and application diagnostics against explicit roots only:

```bash
python3 "$POLYTROPOS_ROOT/bin/harness_select.py" doctor --harness codex --repo-root "$POLYTROPOS_ROOT" --codex-home <codex-home> --json
python3 "$POLYTROPOS_ROOT/bin/codex_app_policy.py" status --repo-root "$POLYTROPOS_ROOT" --codex-home <codex-home> --backup-root <new-empty-dir> --json
```

Report package readiness, runtime activation as observed or `unknown`, policy availability, role-file ownership, planned application changes, and any unavailable required worker. Do not claim an arbitrary host-selected model or direct host tool is sandboxed by this policy boundary.

`codex_app_policy.py apply` writes configuration and needs an explicit runtime availability snapshot, explicit repository, Codex-home, and new empty backup roots. Preview with `plan` first, then obtain explicit user authority. It preserves unrelated TOML and refuses to overwrite unmanaged or edited agent roles. Legacy refresh remains an explicit `--refresh-managed` install action. Restart or start a new task after an authorized app change.
