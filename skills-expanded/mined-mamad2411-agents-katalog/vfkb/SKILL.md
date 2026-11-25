---
name: vfkb
description: Work with vfkb (ViloForge KnowledgeBase), this project's per-project knowledge substrate — resume prior session context, record decisions/facts/gotchas/patterns, search past knowledge, or check wiring health. Use when the user asks to "resume", "what did we decide", "remember this", "record a decision/gotcha/pattern", "search the brain/knowledge base", or when a project has a `.vfkb/entries.jsonl` that should be consulted before answering.
---

# vfkb

vfkb is a per-project, append-only knowledge substrate: decisions, facts, gotchas, patterns, and
links, captured deliberately and reranked back into context when it matters. This skill is the
**human-facing** entry point — an agent acting autonomously should prefer the `mcp__vfkb__*` MCP
tools directly (this plugin also bundles the vfkb MCP server, so both are always available in the
same session).

## Orient first

Before doing anything else, check whether `.vfkb/entries.jsonl` exists in the current project. If
it doesn't, this project isn't using vfkb yet — say so plainly rather than fabricating context.

## Resuming a session

Call `mcp__vfkb__kb_resume` (or `node ${CLAUDE_PLUGIN_ROOT}/dist/bundles/vfkb.mjs resume` from the
project root) to get the handoff digest: what the last session left as "next," and the current
knowledge bundle. Lead with this when a session starts if the user asks "what's the state of
things" or "where did we leave off."

## Recording knowledge — do this immediately, don't defer

When the user states a decision, a rationale, a gotcha, or a durable fact, capture it right away
with `mcp__vfkb__kb_add`:

- `type: "decision"` — a load-bearing choice. Always include `why` (the rationale). Decisions
  default to `status: "proposed"` and are immutable once accepted — to change one later, the tool
  supersedes rather than edits.
- `type: "fact"` / `"gotcha"` / `"pattern"` — durable, editable knowledge.
- `type: "link"` — a pointer to another file/URL. Include the actual path/URL in the `text` itself
  (e.g. `"See the deploy runbook: docs/runbooks/deploy.md"`), not just a description.

Ask the user before recording something you're inferring rather than something they explicitly
stated — don't put words in their mouth as if they were a decision.

## Searching past knowledge

Use `mcp__vfkb__kb_search` for a targeted query, or `mcp__vfkb__kb_list` to browse recent entries
by type/tag. Prefer these over re-deriving something from scratch that the project may have
already settled — search first when a question smells like "haven't we already decided this?"

## Checking wiring health

If vfkb seems inactive (no resume digest at session start, tools erroring), suggest running
`node ${CLAUDE_PLUGIN_ROOT}/dist/bundles/vfkb.mjs doctor` from the project root and relay its
output plainly — don't guess at what's wrong.

## What this skill does not do

It does not reimplement vfkb's engine logic — every action above is a thin call into the same
CLI/MCP surface this plugin bundles. If a request needs something the tools don't support, say so
rather than approximating it by hand-editing `.vfkb/entries.jsonl` (writes to that file must go
through the engine, never a direct file edit).
