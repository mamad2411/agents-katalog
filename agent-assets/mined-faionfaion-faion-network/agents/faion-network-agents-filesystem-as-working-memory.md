# Filesystem as Working Memory — Offload Before Summarize

## Summary

**One-sentence:** Equips long-running agents with write_file/read_file/ls/grep tools backed by a real or virtual FS, offloads every tool output above ~2K tokens to disk, and reserves lossy LLM-based summarisation for context >85% utilisation only after no offload remains.

**One-paragraph:** Give every long-running agent a `write_file` / `read_file` / `ls` / `grep` tool surface backed by real disk, S3, or a state-dict virtual FS. Whenever a tool produces a large blob, write it to the FS and pass back only a filename plus a short snippet. Reserve LLM-based context summarisation for the moment context hits ~85% AND nothing remains to offload — file offload preserves information losslessly, summarisation does not.

**Ефективно для:** дослідницьких агентів, codegen-агентів, будь-якого циклу понад 20 ходів, що мусить зберігати інформацію між процесами.

## Applies If (ALL must hold)

- Research agents reading more than 5 documents per task.
- Codegen across many files (Claude Code, Aider, OpenHands, Cursor).
- Tasks expected to run more than ~20 turns.
- Pipelines where step N's output feeds step N+1 — paths flow, not blobs.
- Agents must survive process restart (FS persists, conversation does not).

## Skip If (ANY kills it)

- Short chat sessions under ~10 turns.
- Single-document QA — the document already fits in context.
- Hard real-time loops where every disk write adds unacceptable latency.
- Untrusted code execution where a writable FS is a security problem.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| FS backend | Real disk path, S3 bucket, or in-memory dict | Agent config |
| Checkpointer | Postgres/Redis/SQLite store for conversation state | Orchestrator config |
| Path taxonomy | search/ docs/ plan/ scratch/ | SKILL or system prompt |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `file-reference-passing` | The offloaded files are passed by reference, not content. |
| `compaction-preserve-refs` | When summarisation finally triggers, refs in the compaction point at offloaded files. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules: offload-2k, four-tool surface, taxonomy, atomic-checkpoint, compact-last | ~1000 |
| `content/02-output-contract.xml` | essential | Tool definitions JSON; offloaded-envelope schema | ~900 |
| `content/03-failure-modes.xml` | essential | Premature compaction, round-trip blobs, dangling paths | ~800 |
| `content/06-decision-tree.xml` | essential | Per-tool-call: inline or offload? Per-turn: offload or compact? | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Decide inline vs offload per tool result | code | Pure size check; no LLM needed |
| Choose path taxonomy for new agent | sonnet | One-shot design |
| Audit existing agent for premature compaction | sonnet | Pattern detection |

## Templates

| File | Purpose |
|------|---------|
| `templates/fs-tools.json` | OpenAI/Anthropic tool definitions for the four FS primitives |
| `templates/_smoke-test.json` | Minimum valid offloaded-envelope for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-filesystem-as-working-memory.py` | Validates an offloaded-envelope against the schema | After every tool wrapper that may offload |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[file-reference-passing]]
- [[compaction-preserve-refs]]
- [[handoff-id-payload]]

## Decision tree

See `content/06-decision-tree.xml`. The root question per tool call is whether the result exceeds the ~2K token threshold. The root question per turn is whether utilisation passed 85%. The tree routes to inline-return, offload-with-snippet, or LLM-based compaction depending on what is still available.
