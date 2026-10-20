---
description: List every extension point and route me to the right one (start here to extend the app)
allowed-tools: Bash, Read
---
Help me extend this workshop app. I will NOT hand-write code — you do it.

Steps:
1. Run `grep -rn "🪁" . --include=*.ts --include=*.tsx --include=*.md` to list every
   marked extension point.
2. Read `EXTENDING.md` and present the five axes as a short numbered menu:
   1) a UI component (L3) → `/add-component`
   2) an A2UI catalog primitive (L4) → `/add-catalog-item`
   3) a tool the agent can call → `/add-tool`
   4) a new skill / slash command → `/add-skill`
   5) a plan→approve→act action → edit the `extend` agent + `planCard`/`planResult`
3. Ask which one I want and what it should do.
4. Hand off by running the matching `/add-*` command with my answer, or (for #5)
   guide the edit to `src/lessons/ExtendDemo.tsx` + the `extend` agent in `server.ts`.

Keep it friendly and concrete — assume I've never written code.
