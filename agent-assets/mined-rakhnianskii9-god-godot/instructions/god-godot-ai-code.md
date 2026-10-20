---
name: "ai-code"
description: "Use when editing gameplay AI in Godot scripts or scenes: NPC behavior, behavior trees, steering, perception, squad logic, decision-making, or combat AI."
applyTo: "my-game/scripts/**, my-game/scenes/**"
---

# AI Code Rules

- AI update budget: 2ms per frame maximum — profile to verify
- All AI parameters must be tunable from data files (behavior tree weights, perception ranges, timers)
- AI must be debuggable: implement visualization hooks for all AI state (paths, perception cones, decision trees)
- AI should telegraph intentions — players need time to read and react
- Prefer utility-based or behavior tree approaches over hard-coded if/else chains
- Group AI must support formation, flanking, and role assignment from data
- All AI state machines must log transitions for debugging
- Never trust AI input from the network without validation
