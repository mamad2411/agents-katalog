---
name: mcp-server-craft
description: "Design and build an MCP server whose tools are narrow, typed, idempotent, and documented. Use when exposing any system to AI agents via the Model Context Protocol."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [mcp, tools, agents, api-design, build]
    related_skills: [agent-loop-safety, spec-first-ai-feature]
    program_weeks: [16]
---

# MCP Server Craft

## 1 · Purpose

Make the tools an agent calls as well-designed as any public API, because to the
agent, the tool description *is* the documentation, and the schema *is* the contract.

## 2 · When to use

- Building an MCP server (or any tool layer) for agents.
- When an agent misuses a tool repeatedly, usually a tool-design bug, not a model
  bug.

## 3 · Inputs

- The system being exposed and its real operations.
- The agent task list: what the agent must accomplish, in verbs.
- An MCP client to test with (inspector, Claude Desktop, your Week-16 harness).

## 4 · Procedure

1. **One tool, one verb.** Name tools `verb_noun`: `track_shipment`,
   `search_policy`, `request_refund`. If a tool name needs "and", it is two tools.
2. **Type every argument.** Schemas with types, enums, ranges, and examples. The
   model fills what the schema describes; a vague schema invites a creative argument.
3. **Write the description as a picker hint.** First line: what it does. Then: when
   to use it, when *not* to use it, and what it returns. The agent chooses tools by
   this text alone.
4. **Make reads idempotent and writes explicit.** Reads never mutate. Writes take
   dry-run or confirmation parameters where the underlying operation is irreversible.
5. **Return structured results, not prose.** JSON the next step can consume:
   IDs, statuses, counts, plus a one-line human summary field.
6. **Fail informatively.** Errors return a code, a cause, and a next action
   ("lane not found, call `list_lanes` to enumerate valid lanes"). An agent that
   can read its errors can recover from them.
7. **Paginate and bound.** Any list operation takes `limit` and returns
   `truncated: true` when capped. An unbounded `list_all` is a context-window bomb.
8. **Test from a real client**, not just unit tests: connect an agent, give it the
   ten task list, and watch which tools it picks. Mispicks mean the descriptions
   failed, fix the text, not the model.
9. **Version the server.** Tool signatures are a contract; changing one is a
   version bump with a changelog entry.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "The model is smart enough to figure the tool out." | The model reads the description you wrote, not the code you meant. |
| "One flexible `query` tool covers everything." | A do-everything tool is chosen for everything and validated for nothing. |
| "Errors can be plain strings." | The agent's next action is decided by the error text. Give it a next action. |
| "We'll document the tools later." | The description field IS the documentation the agent reads. Later never comes. |

## 6 · Red flags

- Tools named `handle_`, `process_`, `do_`, verbs without meaning.
- Arguments typed as free strings where an enum or integer exists.
- A list tool with no limit parameter.
- Agents in testing call the wrong tool for a documented task.

## 7 · Verify

- Every tool has: typed schema, picker-hint description with a when-NOT line,
  structured output, informative errors.
- An end-to-end agent run against the ten-task list shows correct tool selection.
- The server version and changelog exist.

## 8 · ZoroLogistics example

Week 16's server ships four tools: `track_shipment(id)`,
`list_lanes(origin?, destination?, limit=50)`, `search_policy(query, limit=5)`,
`request_refund(shipment_id, reason, confirm=false)`. The refund tool with
`confirm=false` returns the computed refund and `requires_confirmation: true`,
the agent must re-call with `confirm=true`, which the harness routes to a human gate
(`agent-loop-safety`). During testing the agent kept calling `track_shipment` with
lane names; the fix was one line in `list_lanes`' description: "Use this to resolve
lane names to IDs before tracking." Tool design is prompt design with types.

---
© 2026 Zorost Intelligence LLC · zorost.com
