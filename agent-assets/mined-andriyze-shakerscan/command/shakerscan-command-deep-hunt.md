# Hunt compatibility command

Run an authorized, AI-driven Hunt against the supplied target.

**Usage:** `/deep-hunt <target-url-or-id> [objective]`

Use the `research-agent` skill. Deep Hunt is a compatibility name for the canonical `/hunts/*`
workflow: adaptive exploration, bounded capabilities, evidence-backed candidates, and deterministic
promotion where supported. It is not a DAST scan and must not use either legacy planner engine.

Confirm target authorization, create the required target-scoped credential approval when active
testing is requested, start one `/hunts` run, and plan through its returned capability manifest.
