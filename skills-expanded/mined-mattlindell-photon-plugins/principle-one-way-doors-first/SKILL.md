---
name: principle-one-way-doors-first
description: "Apply when sequencing decisions or ordering a plan. Surface and settle irreversible decisions early, while changing your mind is still cheap."
user-invocable: false
---

# One-Way Doors First

Sort decisions by how expensive they are to undo, and take the expensive ones while a human is still in the room.

**Why:** A one-way door found during planning costs a conversation. The same door found during implementation costs a rollback - and on an unattended agent it costs an escalation, which is exactly the expensive path the whole system is built to avoid. `ph-build` gates its costly machinery on this same test, so a door you fail to surface here is one it must discover the hard way.

**Pattern:**

- **Classify before sequencing.** Schema and data migrations, public API surface, anything that deletes or rewrites data, anything external parties will depend on - one-way. Most code is two-way.
- **Pull one-way doors forward**, even when they are not the natural starting point.
- **Two-way doors get decided fast**, and reversed later if wrong. Do not spend a grilling round on something you can undo in an afternoon.
- **Mark them in the artifact**, so execution knows which parts it must not improvise through.

**Boundaries:**

- Reversibility is about cost, not possibility. Almost everything is technically reversible; the question is what it costs.

**The test:** For each decision, ask what undoing it looks like a month from now. If the answer involves a migration, a deprecation, or an apology to someone outside the team, it was a one-way door and belonged earlier.
