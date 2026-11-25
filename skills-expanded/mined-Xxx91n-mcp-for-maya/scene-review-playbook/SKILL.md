---
name: scene-review-playbook
description: "Run and act on the mcp-for-maya scene_review check: pick the right checks, interpret the 0-100 score and per-check results, add your own checks to the run, and map common findings (orphans, naming problems, overlaps, weak aesthetics, lighting gaps) to concrete fixes. Use after structural scene changes, before reporting a scene as done, or when a scene feels disorganized."
compatibility: "Tested on Claude Code only; requires mcp-for-maya MCP server"
---

# scene_review Playbook

> **Experimental.** Evaluated on Claude Code only; untested on Codex/Gemini CLI/Cursor. Tracked in issue #3.

`scene_review()` runs up to 11 fixed checks and returns `{checks, issues, score, total_issues, errors, warnings, standards}` — score is 0-100 (weighted per-check, normalized). Checks you add for this session show up in a separate `custom` section with its own score.

## Checks

| check | what it looks at |
|---|---|
| spatial | object/camera/light presence vs expectations |
| overlaps | bbox collisions (parent-child excluded) |
| conflicts | penetration between unrelated objects |
| zones | zone coverage against the names the zone map knows |
| naming | GRP_/GEO_/MAT_/CAM_/LGT_/LOC_ prefix discipline |
| components | GRP_ grouping, nesting depth ≤ 4 |
| orphans | empty groups, default Maya names |
| aesthetics | 5-dimension aesthetic score (color/composition/scale/lighting/flow) |
| lighting | three-point setup, fill ratio, decay |
| organization | overall hierarchy health |
| constraints | the built-in 500-object budget (not the `custom` section below) |

Per-check weights are defined in the review engine — see the score table in README.md for exact max points; this card intentionally does not duplicate them.

## How to run

- Full run: `scene_review()` — after structural changes.
- Subset: `scene_review(checks="overlaps,conflicts")` — one comma-separated string; cheaper re-verify after a targeted fix. The tool splits it itself, so a Python list is not the shape it accepts.
- Maya-side, for the same subset: `_mcp_scene.scene_review_with_validators(["overlaps","conflicts"])` — a Python list, reached through `execute_code` once `_mcp_scene` is in the session (see Your own checks below). That is the Maya-side entry point the MCP tool itself calls, not the MCP argument; the bare `_mcp_scene.scene_review(...)` takes the same list but drops the `custom` section.
- Interpret: each entry in `issues[]` carries `severity` (error > warning > info), `check`, and a `msg` summary (counts + advice). An `info` row lands in neither the `errors` nor the `warnings` count. Per-object detail lives under `checks[]` — e.g. `checks.overlaps.details` names the colliding pairs (sampled list). Fix errors first; warnings are judgment calls.

## Findings → actions

- `orphans`: root-level meshes or empty groups → reparent under a `GRP_*` group; delete empty groups.
- `naming`: rename the object to use the agreed prefixes; never ship `pCube1`-style names.
- `overlaps` / `conflicts`: `scene_measure(obj_a, obj_b, mode="clearance")`, then move or resize; re-run those checks.
- `zones` low coverage: `scene_plan` for zone mapping and auto-grouping suggestions.
- `aesthetics` / `lighting` weak: `scene_aesthetics()` for the 5-dimension breakdown; lighting fixes follow three-point discipline (key/fill/rim).
- `constraints` violations: read the rule type in the issue, then satisfy it or re-validate via `scene_validate`.

## Your own checks

Register rules in the Maya session via `execute_code` and `scene_review()` reports them in a separate `custom` section — `validators` (each with `name`, `family`, `severity`, `weight`, `passed`, `status` — `passed` | `failed` | `check_error` — and `message`), `score`/`max_score` in weight points from one denominator, and `issues` (each with `severity`, `check: "custom"`, `name`, `family`, `msg`) for whatever did not pass. The built-in 0-100 never moves and the section is absent when nothing is registered. Nothing in `custom` reaches the top-level `errors`/`warnings`/`total_issues` counts — those belong to the built-in checks, so the `custom` section has to be read on its own.

`_mcp_scene` is not in a fresh session until a tool that uses it injects it, and `execute_code` never injects anything — it only forwards code to Maya. Run `scene_review()` (or `scene_snapshot()`) once first; the checks before you register are the built-in ones.

Pre-import the module in its own `execute_code` call, then send each validator call as one expression with `result_type="JSON"` — `execute_code` defaults to `result_type="NONE"`, which runs statements and hands back `None`, so with the default there is no return to read. `import _mcp_scene; _mcp_scene.register_validator(...)` in one payload is the shape that fails under result capture. JSON capture may hand you the decoded dict or its JSON text; handle both.

```python
# 0) scene_review() or scene_snapshot() first: that is what puts _mcp_scene in the session
# execute_code 1: import _mcp_scene
# execute_code 2+, one expression per call, result_type="JSON":
_mcp_scene.register_validator(
    "roots_named",
    lambda: (False, "3 root objects are unnamed"),  # or just True/False
    severity="warning",  # "error" | "warning" | "info" — the built-in vocabulary
    weight=2,
    family="studio",  # free label on the result — you group by it, the report does not
)
_mcp_scene.list_validators()
_mcp_scene.unregister_validator("roots_named")
```

What each call hands back:

- `register_validator(name, predicate, severity="error", weight=1, family="custom", message=None)` → `{"registered": name, "overwritten": bool, "count": int}`. Same name overwrites, so `overwritten: true` is the expected answer on a re-register, not a second copy of the rule. `message=` is the rule's own report text, used when the predicate hands back no text of its own — a bare `True`/`False` or a `(passed, None)` — on a pass as on a failure; a `(bool, message)` return wins over it, and a `check_error` row carries the failure's own text rather than this. With neither source of text, the row reads `<name> passed` / `<name> failed`.
- `list_validators()` → `{"count": int, "validators": [{"name": ..., "family": ..., "severity": ..., "weight": ..., "message": ...}]}`, in run order. It is how you read the active names, and it never echoes the predicate — that is a live callable and would not survive the JSON trip back to the host.
- `unregister_validator(name)` → `{"unregistered": name, "count": int}`. A name that is not registered comes back as the error envelope with `validator_not_found`; it is not a silent no-op.

A bad argument is refused with an envelope rather than an exception: `{"error": {"code": ..., "message": ...}}`, plus a `suggestion` where there is one. The checks are `invalid_validator_name` (both calls refuse a bad name), `invalid_predicate`, `invalid_severity`, `invalid_weight`, `invalid_family`, `invalid_message`; sizing the registry is the `weight_overflow` refusal below. Nothing runs at registration time, so a bad predicate is only discovered when the review runs — and is then isolated the same way as one that raises. The checks read caller-defined hooks — `strip()` on `name` or `family`, the truthiness test on a stripped `name`, the `__eq__` the severity test asks for, `__float__` on `weight` — and a hook that raises an ordinary exception is answered with this envelope like any other bad argument. What still escapes is a BaseException, which propagates on purpose — same stance as the isolation below (a human stopping Maya is not a rule misbehaving).

A predicate returns `bool` or `(bool, message)` — the pair accepted as a tuple or as the same two items in a list; anything else is recorded as `check_error` rather than guessed at. A predicate that raises is isolated the same way — and `check_error` counts as failed, so it costs its weight and lands in `issues` like any other violation while the rest of the review runs. One limit, stated plainly: the isolation catches `Exception`, so a `BaseException` such as `KeyboardInterrupt` still stops the run — that is a human stopping Maya, not a rule misbehaving. Weights must be finite positive numbers of the same order of magnitude (1-100 is the design range, not an enforced cap): a string, a bool, `nan`, `inf`, zero or a negative comes back `invalid_weight`, while a registration that would push the registry total past the float range is refused with `weight_overflow` rather than landing an unparsable score. Re-registering after a reconnect is safe, and it is required: replacing the module or restarting Maya clears the registry, so a `custom` section that vanished means re-register, not "passed". Pre-1.0 API: it may break before 1.0, with a changelog note.

## Done means

- errors: 0; warnings reviewed (not necessarily zero — judgment).
- with checks registered, `custom` is part of done too: a failing row or a `check_error` there is not covered by `errors: 0`.
- after fixes, re-run the affected checks; never re-report a stale score.
