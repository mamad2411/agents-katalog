---
name: aiops-ping
description: Use when verifying Hermes plugin discovery, AIOps plugin entry-point loading, or the aiops_ping boundary probe tool during Task 0 integration checks.
version: 1.0.0
author: AIOps Team
license: MIT
metadata:
  hermes:
    tags: [aiops, hermes, plugin, discovery, validation, ping]
    requires_toolsets: [terminal]
---

# AIOps Ping

## When to Use
Use this skill when you need to confirm the AIOps Hermes plugin is packaged and exposed correctly.

Typical triggers:
- You just installed or updated the AIOps plugin package.
- You need to verify Hermes can discover the `hermes_agent.plugins` plugin entry point and load the `aiops` plugin.
- You want a low-risk boundary probe before implementing real hooks, tools, or bot workflows.
- You need to separate packaging/discovery failures from runtime business-logic failures.

Do not use this skill for real incident handling, bot command routing, or write-action execution.

## Preconditions
- The AIOps package is installed in the Python environment used by Hermes.
- Hermes is running in the target environment where plugin discovery will be checked.
- The `aiops_ping` tool is registered by the plugin package.
- If you are validating through the Hermes runtime, the `hermes` CLI is available in that environment.

## Quick Reference
Expected entry-point group:

```text
hermes_agent.plugins
```

Expected plugin name:

```text
aiops
```

Primary manual verification command:

```bash
hermes plugins list
```

Verbose discovery debug:

```bash
HERMES_PLUGINS_DEBUG=1 hermes plugins list
```

## Procedure
1. Confirm the AIOps package is installed in the same environment Hermes uses.
2. Check that Hermes can discover the `aiops` plugin.
3. Verify the expected plugin name appears: `aiops`.
4. Trigger the `aiops_ping` tool as the lowest-risk runtime probe.
5. Confirm the returned payload is valid JSON and contains `success: true` and a `pong` message.
6. If discovery succeeds but the ping probe fails, classify the issue as handler/runtime wiring rather than packaging.

## Decision Points
- If `hermes plugins list` does not show the expected `aiops` plugin, stop and debug packaging/discovery first.
- If the `aiops` plugin is visible but `aiops_ping` fails, inspect tool registration and handler wiring.
- If the ping probe succeeds, proceed to the next integration task instead of expanding this skill further.

## Pitfalls
- Do not assume bot workflow routing is already implemented just because the plugin is discoverable.
- Do not treat this skill as proof that real webhook hooks or approval flows are working.
- Do not debug production logic here; this skill exists only to validate the integration boundary.
- If you are outside the Hermes runtime environment, repository-side tests can validate entry-point metadata but not runtime loading.

## Verification
Success means all of the following are true:
- Hermes can discover the AIOps plugin entry point.
- The plugin name `aiops` is visible.
- The `aiops_ping` probe returns a JSON payload with `success: true`.
- No additional runtime-only assumptions are made beyond packaging and boundary wiring.