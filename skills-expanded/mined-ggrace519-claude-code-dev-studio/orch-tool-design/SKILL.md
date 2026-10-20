---
name: orch-tool-design
description: Tool-design specialist for agents. Owns individual tool specs — name, description, schema, examples, error behavior — and the tool-catalog discipline that shapes agent reliability. Auto-invoked when designing, adding, or refining tools exposed to an agent.
---

# Agent Tool Design

Tools are APIs for a non-deterministic consumer. Vague descriptions, loose
schemas, and silent failures don't surface as type errors — they surface as
wrong calls, retry loops, and confident hallucination.

## When to reach for this

- Adding a tool to an agent, or wrapping an existing API for agent use
- An agent picks the wrong tool, passes bad arguments, or loops on failures
- Pruning or restructuring a tool catalog that has grown overlapping tools
- Writing the error responses a tool returns to the model

## Principles

1. **The description is UX for a model.** Write it for the caller: what the
   tool does, when to use it over siblings, what it returns, and what it costs
   (side effects, latency). Implementation details are noise.
2. **Tight schemas.** Enums beat free text; required beats optional; one clear
   parameter beats two that interact. Every optional parameter must state its
   default — the model will otherwise guess one.
3. **One tool, one job.** A tool whose behavior forks on a `mode` parameter is
   two tools wearing one name, and the model will pick the wrong mode.
4. **Error messages coach.** A failure response says what was wrong *and what
   to do next* ("`user_id` not found — call `search_users` first"). "Error 422"
   teaches nothing and invites a blind retry of the same call.
5. **Declare side effects and idempotency.** Mark read-only vs mutating in the
   description; give mutating tools an idempotency key or make retries safe,
   because the agent runtime *will* retry.
6. **Examples over prose.** 1–2 canonical calls in the description beat 200
   words of explanation — they pin down format, units, and ID shapes.
7. **Catalog size is a budget.** Each added tool dilutes selection accuracy
   across all of them; past roughly 15–20 tools, group, namespace, or split the
   catalog rather than appending.

## Spec checklist (short form)

- [ ] Name is `verb_noun`, consistent with catalog conventions
- [ ] Description: purpose, when-to-use-vs-siblings, return shape, side effects
- [ ] Every parameter: type, constraint/enum, default if optional, example value
- [ ] Errors enumerated, each with a coaching message and whether retry helps
- [ ] Idempotency stated; mutating tools safe to retry or keyed
- [ ] Output bounded (pagination/truncation) so one call can't flood the context

A worked good-vs-bad tool definition, an error-catalog pattern, and the full
quality checklist are in
[`references/tool-spec-checklist.md`](references/tool-spec-checklist.md).

## Pitfalls

- Descriptions written by the API team for humans, pasted verbatim — full of
  internal jargon, silent about when *not* to use the tool
- Overlapping tools (`search`, `find`, `lookup`) with no guidance on which wins
- Free-text parameters where an enum exists (`status: string` vs four known values)
- Errors returned as empty results — the model concludes "nothing exists"
  instead of "I called this wrong"
- Tool output dumping unbounded JSON (entire DB rows, base64 blobs) into context
- Renaming or re-typing a parameter without rerunning evals — tool-choice
  behavior is prompt-sensitive and regresses silently

---
*Related: `orch-prompt-engineer` (tool guidance in the system prompt), `orch-eval`
(tool-call shape checks and selection evals), `orch-sandbox-safety` (authority
gating behind the schema) · domain agent: `orch-architect` · output/ADR format:
`playbook-conventions`*
