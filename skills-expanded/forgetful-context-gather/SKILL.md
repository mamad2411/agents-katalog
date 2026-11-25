---
name: forgetful-context-gather
description: >-
  Gather deep context before planning or implementing — one pass that turns a task
  description into a cited context pack: relevant decisions, patterns, constraints, code
  pointers, procedures, and explicit gaps. Runs recall from several angles, explores the
  graph around the strongest hits, and opens the linked material.
license: MIT
disable-model-invocation: true
tags: [context, retrieval, workflow, pre-work]
allowed-tools:
  - mcp__forgetful__discover_forgetful_tools
  - mcp__forgetful__how_to_use_forgetful_tool
  - mcp__forgetful__execute_forgetful_tool
  - Bash(forgetful:*)
---

# Gathering context before work

A single query answers a question; a context gather prepares a task. The output is a pack
the work can lean on, with every claim cited by memory ID and every dry angle stated —
silence is never ambiguous.

## Invoking operations

Operations are named by registry name (`query_memory`, `get_document`, ...). Invoke via
whichever surface this agent has:

- **MCP**: `execute_forgetful_tool(tool_name="query_memory", arguments={...})`
- **CLI**: `forgetful call query_memory --args '{"query": "..."}' --json`

Get any operation's schema at runtime: `how_to_use_forgetful_tool` (MCP) or
`forgetful tools info <operation>` (CLI) — schemas are deliberately not repeated here.

Delegating this workflow to a subagent: hand it the CLI flavor — `Bash` travels into
subagents, MCP tool access does not. Run MCP-flavored gathers in the main conversation.

## Step 1 — Derive the query angles

From the task description, write 3–5 distinct angles: the feature area, the technology or
library, exact error text or identifiers, the architectural layer, adjacent domains that
share patterns. One angle is a spot-check; several are coverage.

Done when: the angles are listed before any query runs.

## Step 2 — Recall per angle

`query_memory` per angle — `query` and `query_context` are both required, and
`query_context` should carry the task's intent (per `forgetful-recall`: reads cross-project
by default, identifiers verbatim, `truncated` handled). Skills referenced by name in this
skill resolve via `search_skills` → `export_skill` when not already available. Track which
angles hit and which came up dry.

Done when: every angle has run and its outcome is recorded.

## Step 3 — Explore around the strongest hits

Where hits reference entities or cluster into a topic, walk the graph (per
`forgetful-explore`, medium depth): expand the memories, discover the entities, harvest
what is attached to them.

Done when: the strongest hits have their neighbourhood mapped, not just their own text.

## Step 4 — Open the linked material

Hits point outward — follow the pointers: `get_document` for linked documents,
`get_code_artifact` for reusable code, `search_skills` + `get_skill` for procedures that
already do the task, `get_skill_links` for what those procedures bundle.

Done when: load-bearing linked material is read, not just listed.

## Step 5 — Sweep for unlinked material

Link-following only surfaces what a hit already points to — a document or code artifact
that no surfaced memory links to stays invisible to that flow. Close the gap:
`list_documents` and `list_code_artifacts`, scoped with `project_id` when the task is
project-bound, then scan titles for relevance. `search_skills` already searches skills
directly, so no separate sweep is needed there.

Done when: documents and code artifacts have been swept by title, not just reached by link.

## Step 6 — Synthesize the pack

Assemble, in order of usefulness to the task:

- **Decisions** that constrain the work (cited by memory ID)
- **Patterns and preferences** that shape how it should be done
- **Constraints** — things ruled out, with the reason
- **Code pointers** — artifacts and source references worth opening
- **Procedures** — stored skills that cover part of the task
- **Gaps** — every angle that came up dry, stated as "no existing knowledge about X"

Done when: the pack cites its sources, states its gaps, and the task could start from it
without re-querying.
