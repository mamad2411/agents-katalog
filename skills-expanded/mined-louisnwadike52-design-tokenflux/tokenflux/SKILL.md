---
name: tokenflux
description: Token and context efficiency discipline for coding work. Use at the start of any coding task that involves exploring a repository, reading files, or running commands — especially in large codebases or long sessions. Gather the minimum context needed to act correctly — search before reading, read targeted ranges, filter command output, avoid redundant reads and tool calls — while never trading correctness for token savings.
---

# TokenFlux

Use the minimum context and output needed to complete the task **correctly**. Optimize token efficiency, not token count: a cheap read that prevents a wrong edit is efficient; a skipped read that causes one is not. When token savings and correctness conflict, correctness wins — always.

## Core loop

Search → Identify → Targeted read → Reason → Act.

Before any retrieval, ask:

1. Is this already in context?
2. Can a search replace a read?
3. Can a narrow range replace a full file?
4. Will the output change my next action?

If the answer to 4 is no, skip the call.

## Repository exploration

Discover progressively: structure → relevant directories → relevant files → relevant symbols → implementation.

- Enter through package manifests, entry points, and configuration relevant to the task — not an indiscriminate crawl.
- Never bulk-read: `node_modules`, build/dist output, generated files, lockfiles (unless dependency versions are the question), binaries, images, large logs, caches, unrelated docs.
- No speculative exploration: do not inspect modules "just in case."

## File reading

- Search first (`rg`, `grep`, Grep tool) to locate the symbol; then read a narrow range around the match; widen only when needed.
- Full-file reads are appropriate for small files, or when whole-file understanding genuinely matters (refactors, reviews, tricky state).
- Prefer targeted shell filters (`rg -n`, `sed -n '120,180p'`) over dumping whole files.

## Tool calls

- Skip calls whose output will not change your next action.
- Batch independent lightweight operations into one step.
- Use the cheapest sufficient source: existing context → search → targeted read → full read.
- Do not repeat a call whose result is already known and unchanged.

## Command output

- Prefer quiet forms: `git status --short`, `git log --oneline -20`, `--reporter=dot`, `--silent` where safe.
- Filter at the source: `| head`, `| tail`, `rg pattern`, redirect known noise.
- After test runs, inspect failures — not passing logs.
- Never suppress or truncate errors needed for debugging.

## Context reuse

- Track what you have already established (file locations, symbols, decisions) and reuse it.
- Do not reread an unchanged file to reconfirm a known fact. Reread only if: the file changed, your memory of it is uncertain, or more detail is genuinely required.

## Context priority

- **P0 — never drop:** user requirements, explicit constraints, security requirements, API contracts, active errors and test failures, current implementation decisions.
- **P1 — preserve:** relevant architecture, source, interfaces, data models, dependencies, task state.
- **P2 — compressible:** supporting details, exploration history, secondary docs.
- **P3 — droppable:** repeated explanations, unrelated files, stale command output, redundant observations.

When working notes grow repetitive, compress them into a compact map (`auth: service src/auth/service.ts · middleware src/auth/jwt.ts · strategy JWT`) — but never compress away implementation-critical detail.

## Modes

If the project has a `.tokenflux.json`, honor its `"mode"` (and other preferences); otherwise use `balanced`.

- `balanced` — cut obvious waste; when in doubt, gather the context.
- `aggressive` — also trim marginal reads and redundant tool output; still verify anything correctness-critical.
- `maximum` — minimum viable context wherever it is safe; correctness checks remain mandatory.

## Safety

Never do any of the following to save tokens: skip validation or tests; guess instead of reading required code; ignore security-relevant information; hide, trim, or soften errors; drop user requirements or constraints; modify files merely to shrink context. When uncertainty materially affects correctness, retrieve more context — that is the efficient move.

## Anti-patterns

- `cat huge-file.ts` to find one function → `rg -n "functionName" huge-file.ts`, then read that range.
- Reading the whole repository tree before knowing what the task needs.
- Rereading a file you just wrote or edited yourself.
- Pasting a full verbose command dump when one filtered line answers the question.
- Skipping the one read that would confirm an API signature before using it.
