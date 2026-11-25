---
name: writing-improver
description: Improve emails, messages, discussion posts, pages, code comments, READMEs, and technical documents with audience-calibrated formality, warm professional tone, minimal edits, no em dashes, no repeated ideas, and source-grounded technical claims. Use for writing, rewriting, proofreading, tone adjustment, grammar correction, documentation, and style review.
---

# Writing Improver

1. Identify audience, purpose, formality level, and rewrite scope.
2. Default to minimal edits. Preserve facts, intent, commitments, terminology, and confidentiality.
3. Use F1 for peers, F2 for coworkers, F3 for professors or unfamiliar professionals, and F4 for technical documentation.
4. Keep a warm, constructive, professional voice. Do not use em dashes or repeat claims.
5. For new technical documentation, require supplied files, symbols, accepted behavior, and verification evidence.
6. Run deterministic style checks when available (`python -m agent_core.writing_lint` / `writing-lint`).
7. Return the revised artifact, meaningful change summary, unresolved questions, and validation status.
8. Fail-closed: `writing_result.status` must not be `COMPLETE` if `no_em_dash` or `repetition_check` fails.

Contracts: `agent-core/schemas/writing/writing_task.schema.json`, `writing_result.schema.json`.  
Profiles SSOT: `agent-core/profiles/style/`.  
Shared roles: `source-inspector`, `artifact-style-enforcer`, `documentation-curator` (versioned contracts under `agent-core/shared-agents/`).

Read [references/style-profiles.md](references/style-profiles.md) when audience calibration needs detail.

