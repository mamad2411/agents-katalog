---
name: skills-registry
description: Discover what capabilities exist in this org's skills registry — and the MCP bindings needed to call them.
license: MIT
metadata:
  owner: ITSpecialist111
  source: https://github.com/ITSpecialist111/AgenticSkillstoAgents
  readOnly: true
---

# Skills Registry skill

## What this skill does

This skill gives the agent **read-only discovery** over the organisation's
skills registry. The registry is the missing-middle layer between
GitHub-tracked capability manifests and the live MCP servers that execute
each skill. Use it before invoking any business workflow — it answers:

- *"Who in this org can do X?"* (e.g. extract fields from an invoice)
- *"What categories of work are available?"*
- *"Is this skill safe to use for the task in front of me?"*

The skill does **not** execute business logic. Each result includes an
`mcp` binding (server name, tool name, transport) that the agent uses to
call the underlying skill server directly.

## When to use it

Use this skill **first** whenever a user request maps to a likely
capability (invoice processing, PO matching, AP intake, etc.) but you
don't already know which concrete tool to call. Typical signals:

- The user names a business document, process, or system.
- The user asks "can you …?" about something outside the agent's built-in
  toolkit.
- A previous tool call returned a result that needs further enrichment
  ("now reconcile this against the PO").

## Tools

| Tool | When to call |
|---|---|
| `find_skill_by_capability(tag)` | You know roughly what capability you need. Pass a dotted lowercase tag (e.g. `invoice.extract`). |
| `describe_skill(skill_id)` | You have a candidate skill id and need the full manifest (governance, scoring, preconditions, effects) before deciding to call it. The response includes a `payloadFiles` list of `skill://` resource URIs for the narrative SKILL.md and any asset schemas. |
| `list_capabilities()` | You want the full inventory before forming a plan, or to confirm a tag exists. |
| `submit_skill_draft(manifest, payload?)` | An agent or human authored a new skill and wants it registered. Opens a PR; a human reviewer must merge before the skill becomes discoverable. |

## Resources

Each skill's narrative and assets are exposed as **MCP resources** rather
than tool output, so reading them costs no tool slots and no system-prompt
context:

- `skill://<slug>/SKILL.md` — human-readable description and composition notes.
- `skill://<slug>/assets/<file>` — JSON schemas, examples, scripts.

The `<slug>` is the skill id with `/` replaced by `-` (so
`finance/invoice-extract` → `finance-invoice-extract`). The URIs are
returned in `describe_skill().payloadFiles`.

## Typical workflow

1. User: *"Pull the invoice fields out of this PDF and reconcile against the PO."*
2. Agent → `list_capabilities()` to see what tags exist.
3. Agent → `find_skill_by_capability(tag="invoice.extract")`
   - returns `finance/invoice-extract` + its `mcp` binding.
4. Agent → `describe_skill("finance/invoice-extract")` to confirm the
   skill's data classification is acceptable for the user's document,
   then optionally reads `skill://finance-invoice-extract/SKILL.md` for
   composition guidance.
5. Agent calls the underlying skill server via the returned `mcp` binding.
6. Agent → `find_skill_by_capability(tag="po.match")` and repeats for
   the matching step.
7. Agent composes the final answer.

## What this skill is not

- **Not an executor.** It returns bindings, not results.
- **Not a write-free zone.** `submit_skill_draft` opens a PR, but the PR
  review is the actual Register gate — nothing lands on `main` without
  human approval.
- **Not authoritative for credentials.** Auth lives on each underlying
  skill server.
