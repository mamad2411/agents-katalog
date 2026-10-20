# Composition Module

Orchestration tools that let agents compose other tools: batch (parallel
sub-agents), pipe (sequential tool chaining), map (fan-out over items), and
workspace (shared blackboard for multi-agent coordination).

These are opt-in conveniences. Map and pipe call the guarded tool executor;
each child inherits the caller’s permissions, scope and session context.
