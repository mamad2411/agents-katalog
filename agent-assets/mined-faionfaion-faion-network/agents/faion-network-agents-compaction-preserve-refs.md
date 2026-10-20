# Compaction Templates That Preserve References

## Summary

**One-sentence:** Hard-codes a compaction schema that preserves file paths, function names, error messages, decisions, URLs, and IDs verbatim and drops reasoning, producing a reference manifest for resume.

**One-paragraph:** When a long-running agent must compact its conversation to free context, the compaction prompt must hard-code which fields survive and which are dropped. Always preserve: file paths, function names, error messages, decisions, URLs, IDs. Always drop: intermediate reasoning chains and verbatim tool output. The compacted summary is itself a manifest of references — not a narrative — so the agent can re-fetch any dropped detail by path or ID instead of re-reasoning from scratch.

**Ефективно для:** довгограючих агентів, що пересічуть межу контексту і мусять відновитися в наступній сесії без втрати критичних посилань.

## Applies If (ALL must hold)

- Agent loop is expected to exceed approximately 30 turns or its context window — compaction will trigger.
- Multi-session SDD work where the next session reads the compacted output and resumes from it.
- Pipelines where compaction is automated by middleware (opencode, Claude Code auto-compaction).
- The agent depends on file paths, error texts, or external IDs to make further progress.

## Skip If (ANY kills it)

- Stateless single-turn agents — there is no later step that needs the references.
- Conversations that compact only the user-facing answer for display, not for the agent's own continuation.
- Agents whose only "state" is a closed-form result (a number, a yes/no) — references add noise.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Raw conversation transcript | List of `{role, content}` messages or middleware-supplied buffer | Agent loop runtime (Claude Code, opencode, custom harness) |
| Workspace path roots | Absolute filesystem prefixes the agent's tools dereference | Agent config / `cwd` |
| Active goal statement | One-sentence task description from the user or upstream planner | Initial user message or last `goal:` update |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `filesystem-as-working-memory` | Defines the offload primitives the compacted refs must point into. |
| `file-reference-passing` | Establishes the broader pattern of refs-not-content between stages. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Three testable rules: keep verbatim, drop reasoning, fixed schema | ~900 |
| `content/02-output-contract.xml` | essential | YAML schema for compacted state, good/bad examples | ~900 |
| `content/03-failure-modes.xml` | essential | Free-form summarization, ad-hoc keys, lost refs | ~700 |
| `content/04-procedure.xml` | recommended | Five-step compaction pipeline with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from trigger to compaction strategy | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate compacted YAML from transcript | haiku | Schema-bounded transformation; no reasoning needed |
| Audit a compacted blob for missing refs | sonnet | Pattern-matching across the full transcript + the compaction |
| Design the schema for a new compaction target | opus | One-shot design with long-tail edge cases |

## Templates

| File | Purpose |
|------|---------|
| `templates/compaction-prompt.txt` | Drop-in compaction system prompt enforcing the references-only schema |
| `templates/compacted-state.yaml` | Reference compacted-state file with all required keys |
| `templates/_smoke-test.yaml` | Minimum viable filled-in compacted state for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-compaction-preserve-refs.py` | Validates a compacted YAML against the schema (required keys, no free-text summary) | After every compaction call, before passing state downstream |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[filesystem-as-working-memory]]
- [[file-reference-passing]]
- [[handoff-id-payload]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether the agent's context window is approaching the compaction threshold AND whether the next session will resume work from the compacted output; both must be true before the methodology applies. Subsequent branches pick the compaction strategy (full schema vs. delta-only) based on how much of the prior state already lives on the agent's filesystem.
