---
description: Make a skill or skill system production-grade — its quality rules become enforced gates, reviewers, and evals instead of prose it can ignore.
argument-hint: "[skill or system to harden] (optional; inferred from context)"
---

# Harden a skill

1. Fetch the hardening workflow: call the `aieb` MCP `get_skill` tool (match ANY tool ending in `get_skill` — names vary by surface; on Cowork run a tool search for "get_skill" first) with `skill_id: meta-create-skill`, `path: workflows/build-harness.md`. Follow exactly what it returns, applied to the skill/system in `$ARGUMENTS` (or the one just discussed).
2. This only hardens skills the user OWNS (`.claude/skills/`). For a skill this plugin serves, standing adjustments belong in `digital-assets/overrides/<skill-id>.md` instead — say so and offer that.
3. Any other path the workflow references (e.g. `references/mechanism-selection.md`, gate templates) → fetch it the same way with that exact path. Gate scripts you scaffold are written into the USER's workspace and run there.
4. If no `get_skill` tool exists after searching, the connector is missing — run the `check-setup` skill and stop.
5. A 🔒 or license message from `get_skill` is a normal answer, not an error: relay it warmly with the link it contains, then stop. Never reconstruct the workflow yourself.
