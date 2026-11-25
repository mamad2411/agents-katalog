---
name: introspect
description: Capture corrections and lessons from this testing session into introspection.md at the feature demo path.
argument-hint: '<optional: feature-name>'
model: opus
---

User's request: $ARGUMENTS

# Introspect

## Project Discovery

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/project-discovery.md`.

Store the resolved base directory as `$DEMO_BASE`.

## Run Introspection

Use the Agent tool with `subagent_type: "showboat-introspect"` and pass the demo base path and feature name so the agent knows where to write:

```
Agent({
  subagent_type: "showboat-introspect",
  description: "Write introspection.md for this demo session",
  prompt: "Feature: <feature-name>. Write the introspection document to: <$DEMO_BASE>/introspection.md"
})
```

## Done

Report the path written by the agent.
