---
name: jira-triage
description: Triage a Jira issue — fetch via MCP, classify type/priority/component, ask for missing repro, transition state, route owner. Jira only — not other trackers.
---

# jira-triage

> Triage one Jira issue via the jira MCP server.

> **MCP binding (read before any tool call):** resolve which server backs `issue_tracker` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.jira` — when `source` is `host`, the CURRENT host agent's own `jira` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- A Jira reference (PROJ-123 or a browse URL) is in the prompt.
- The user says "triage the backlog" or "look at this ticket".

## Procedure

1. **Fetch** the issue via `jira_get_issue` (or equivalent on the configured server). Pull the description, comments, current status, and existing labels.
2. **Classify**:
   - **Bug** — observed behavior differs. Severity per the project's scale, mapped to incident severities where possible.
   - **Story** — net-new capability. Defer estimation to `polymath-planning:estimate`.
   - **Task** — operational work; lower priority than story unless tied to a milestone.
   - **Question / support** — answer in a comment; resolve.
   - **Duplicate** — link the original; transition to `Closed/Duplicate`.
3. **Components / area labels** — set based on the code area implicated. Mirror the team's existing label vocabulary.
4. **Missing repro** — for bugs lacking version + steps + expected/actual, add a polite request and a `needs-info` label. Don't berate.
5. **Transition** — move to the right column (`To Do` / `In Progress` / `Blocked` / `Done`) via `jira_transition_issue` only when you're confident in the state.
6. **Assign** — team handle if your Jira uses team accounts, otherwise an explicit person from the rotation.

## Project localization

If the project-context snapshot has a `tracker` block
(`polymath-core:project-context`), use its `project`/`area_path`/`iteration`
as the destination vocabulary, and any NEW item you create during triage
(e.g. a split-out ticket) gets the 3-layer provenance marking —
`marking.title_prefix`, `marking.tag`, traceability footer — is created only
after explicit confirmation (HITL), and is read back to verify the marking
landed.

## Output

```text
Triage: PROJ-1234

Type: Bug | Priority: Medium | Component: payments-api.
Repro: complete (v0.4.7 + 5 steps + expected/actual).

Actions (jira MCP):
  - jira_update_issue: labels=["component/payments-api", "type/bug"]
  - jira_update_issue: priority="Medium"
  - jira_transition_issue: target="In Progress" (after assignment)
  - jira_add_comment: thank-you + acknowledged

Routing: payments-api team via @payments-eng.
```

## Anti-patterns to avoid

- Transitioning to "In Progress" before assigning an owner.
- Closing as "Duplicate" without linking the original key.
- Asking for repro that's already in the body — read first.
- Bulk-updating priority without per-ticket justification.

