---
description: Graduate a proven skill to run on a schedule, unattended — the capstone of the build ladder (an AI Employee that shows up on its own).
argument-hint: "[skill] [cadence, e.g. every weekday 8am] (optional; asked if omitted)"
---

# Schedule a skill

1. Fetch the scheduling workflow: call the `aieb` MCP `get_skill` tool (match ANY tool ending in `get_skill` — names vary by surface; on Cowork run a tool search for "get_skill" first) with `skill_id: meta-create-skill`, `path: workflows/graduate-to-schedule.md`. Follow exactly what it returns for the skill/cadence in `$ARGUMENTS` (ask if omitted).
2. Honor the workflow's gates — proven + recurring + safe-unattended — before creating any routine. An unproven skill routes back to testing first; an event-triggered job is a hook, not a schedule.
3. Any other path the workflow references → fetch it the same way with that exact path. The user's own skills are local files — read those from disk normally.
4. If no `get_skill` tool exists after searching, the connector is missing — run the `check-setup` skill and stop.
5. A 🔒 or license message from `get_skill` is a normal answer, not an error: relay it warmly with the link it contains, then stop. Never reconstruct the workflow yourself.
