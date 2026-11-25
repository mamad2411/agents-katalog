---
name: learnings-write
description: Use this skill when capturing patterns, lessons learned, or architectural decisions worth surfacing in future sessions — to perform a curated write to L4 (project) or L5 (user-global, opt-in) learnings memory. Spawns memory-curator agent to dedupe + PII-filter + schema-validate before append.
context: fork
argument-hint: "<learning text> [--committed]"
---

# /learnings-write — Capture a Durable Learning

Append a curated entry to `learnings.md` (L4 project, default) or `~/.claude/ai-skills/learnings.md` (L5 user-global, with `--global`). Spawns the `memory-curator` agent for dedupe, PII filter, schema validation per `learnings-schema.md`.

## When to use

- After solving a tricky bug: "Async state in React 18 needs `startTransition` for non-urgent updates"
- After a design decision: "We chose gRPC over REST because client SDKs are lower-friction"
- After a pattern emerges: "Repository pattern works better than direct ORM for our team"
- After a gotcha: "Postgres `text` column ignores trailing whitespace in indexes"

## Invocation

```
/learnings-write "Async state management — startTransition for non-urgent updates"
/learnings-write "Why we chose gRPC over REST" --global
/learnings-write "Postgres text column index trailing whitespace gotcha" --tags "postgres,index"
/learnings-write "ADR: adopt outbox pattern for cross-service events" --committed
```

## Arguments

| Flag | Default | Effect |
|---|---|---|
| `<text>` (positional) | required | The learning to capture (1 sentence to 1 paragraph) |
| `--global` | off | Write to L5 (requires `userConfig.user_global_memory_enabled: true`) |
| `--tags "tag1,tag2"` | none | Comma-separated tags for search |
| `--source <id>` | auto | Workflow run-id this learning came from |
| `--committed` | off | Write to the committed L4 layer (`.ai-skills-memory/.committed/learnings.md`) — routes through the `pre-tool-use-committed-write.py` allowlist hook |

## Behavior

1. Validate `--global` permission per `memory-discipline.md` rule 3 — must have BOTH `userConfig.user_global_memory_enabled: true` AND `--global` flag.
2. Spawn `memory-curator` agent (the agent is spawn-only — not user-invocable) with G7 spawn payload:
   - `goal`: "Add a learning entry the user wrote: <text>"
   - `state_slice`: existing learnings.md (target layer) for dedupe context
   - `allowed_tools`: Read, Write
3. Memory-curator:
   - Reads existing learnings.md (target layer) for dedupe per `memory-validation.md`
   - Applies L5 scope check if `--global` (rejects entries with project paths/names per `memory-discipline.md` rule 4)
   - Applies PII filter (`apply_pii_filter()` from `_lib.py`)
   - Formats per `learnings-schema.md` (H2 entity heading + Type/Source/Confidence/Created/Last confirmed/Scope frontmatter + body)
   - Appends to target file (append-only)
4. Receive G7 return contract:
   - `status: ok` → entry written; report path + entity heading
   - `status: partial` → some content rejected (e.g., L5 scope violation); report what was rejected and why
   - `status: needs_clarification` → conflict with existing entry; surface the question to user

## Hard rules

- **Spawn-only memory-curator** — never bypass and write learnings.md directly per `memory-discipline.md` rule 1
- **PII filter mandatory** — every write passes through filter; redactions logged to `redactions.log`
- **`.committed/` writes route through `pre-tool-use-committed-write.py` hook** — committed learnings must match the allowlist pattern (default: `learnings.md`, `architecture-decisions/*.md`, etc.)
- **L5 strict scope** — entries with project-specific paths or names are rejected (must be generalizable patterns)

## Failure modes

- **`--global` without permission:** refuse with same error as `/memory-recall`
- **Entry too short (< 20 chars):** refuse — entries should be substantive
- **Entry duplicates existing:** memory-curator returns `status: needs_clarification` with the existing entry; user picks merge / skip / supersede
- **PII filter unavailable (`_lib.py` import error):** memory-curator returns `status: failed`; never write without filter

## Memory writes

| Layer | Trigger | Path |
|---|---|---|
| L4 (default) | Always | `<repo>/.ai-skills-memory/learnings.md` |
| L4 (`.committed/`) | If user explicitly opts in via `--committed` flag | `<repo>/.ai-skills-memory/.committed/learnings.md` (allowlist-validated) |
| L5 | Requires `--global` AND `userConfig.user_global_memory_enabled` | `~/.claude/ai-skills/learnings.md` |

## Integration

- **Spawns**: `memory-curator` agent (Read, Write only; no Task; no Bash)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Templates**: `plugin/memory/templates/learnings-schema.md` (entry format), `plugin/memory/templates/committed-allowlist.txt` (committed write rules)
- **Rules**: `memory-discipline` (write rules + PII filter mandate + L5 scope), `memory-validation` (dedupe + conflict resolution)
- **Hooks**: `pre-tool-use-committed-write.py` (committed allowlist enforcement)
- **Companion**: `/memory-recall` to search; `/memory-init` to initialize the tree
- **Layer model**: `plugin/docs/concepts/memory.md` documents the L0–L5 layers (L4 = project memory, L5 = user-global). This skill writes only to L4 (default) and L5 (opt-in).
