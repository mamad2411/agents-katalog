---
name: skt-mcp
description: |
  Use when asked to equip/enable/disable a skill or bundle, create or edit a skill, mcp, or inspect the Skill Hub registry.
  Trigger: "equip", "skill tree", "enable skill", "snippet", "update skill"
---

# Skill Hub over MCP

The `skill-tree` MCP server is the control plane for the Skill Hub registry: skills,
bundles (ordered skill groups), snippets (reusable agent-doc blocks), and their
assignment to projects. Every write auto-syncs symlinks and harness configs — you
never need to follow up with `sync` after a normal mutation.

## Discover before you write

Names must be exact. Discover them first:

- `project_list` — the only source of valid `project` values (+ each project's active skills).
- `skill_list` — all skills; pass `project` to see what's active there.
- `bundle_list` — bundles, their ordered skills, and where they're applied.
- `snippet_list` — snippets; `name` for detail, `project`/`scan` for placement status.
- `inspect` — harness inventory, permissions (read-only), risk scan, agent-doc root status.
- `skill_candidates` — hand-authored project-local skills the hub doesn't manage yet.

## Core operations

- Equip/unequip: `equip {target: skill|bundle, name, project, state: on|off}`.
  Optional `invocation` (skill + on only) sets a per-project invocation override.
- Create a skill: `skill_create`, then edit its files on disk, then `equip` it.
- Edit metadata: `skill_set_meta` (scope, description, harness affinity as an array,
  invocation mode; `new_name` renames — alone, not combined with other fields).
- Adopt a hand-authored skill: `skill_candidates` → `skill_import`.
- Bundles: `bundle_save` upserts (the `skills` array order is preserved).
- Snippets: `snippet_save` upserts the library copy; `snippet_place {op: apply|remove|refresh}`
  manages placements in project agent docs.

## Safety rules

- `skill_archive` and `bundle_delete` are destructive: they preview by default and only
  act with `confirm: true`. Preview first; ask the user before confirming unless they
  already told you to.
- `snippet_delete` deletes the library definition immediately — no preview. It refuses
  while the snippet is still applied anywhere unless `force: true`, which orphans the
  in-file blocks.
- Permissions and harnesses are READ-ONLY over MCP (`inspect`) — by design there is
  no MCP tool to change them; direct the user to the `hub` CLI or the Skill Tree app.
- Every result is `{ok, result, output, error}`. On `ok: false` read `error` — it often
  names the fix (e.g. "use project_list to discover project names").
