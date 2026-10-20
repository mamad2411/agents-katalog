---
name: "vendor-sourcing"
description: "Use when choosing, comparing, or integrating a third-party Godot addon, template, example, or vendor library from godot-lib-pazzle into this workspace."
applyTo: ".github/agents/**, .github/skills/**"
---

# Vendor Sourcing Rules

Use this file when an agent or skill needs to choose, evaluate, compare, or integrate a third-party Godot addon, template, example, or vendor library in this workspace.

- Start with `/home/projects/gamedev/godot-lib-pazzle/README.md` as the routing map for the local vendor set.
- If the user names a specific library already, still read that library's nearest `README.md`, `docs/`, `examples/`, `addons/`, demo scenes, and tests before recommending or integrating it.
- Treat `/home/projects/gamedev/godot-lib-pazzle/alternatives/` as first-class local replacements, not second-tier fallbacks.
- Prefer minimal integration into `/home/projects/gamedev/my-game/`; do not mass-edit vendored libraries unless the task genuinely requires modifying the vendored copy itself.
- If the task is mainly library selection or ownership routing, consult `/home/projects/gamedev/agents-faq.md` for the current library-to-agent map.
- If two vendor libraries overlap, prefer the one with the simpler entry point and cleaner integration path for the current `my-game` scope.
