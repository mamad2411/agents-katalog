# Shared agent operating contract

Read the root `SKILL.md` before every task, then README.md, the relevant architecture documents, this file, your role file, and ops/memory. This contract applies to all participating agents by explicit task instruction; its directory placement does not automatically scope tooling to the entire repository.

Agents are engineering assistants only. GitHub owns code/config/tests; OVH Object Storage owns immutable raw originals; OVH Managed PostgreSQL owns normalized KMX/Evidence/Rules. The VM is an execution environment only.

One writer per task. CODEX assigns a task ID, one writer, allowed files, branch, worktree, acceptance criteria and reviewers using ops/tasks/TEMPLATE.yaml. Reviewers return findings without changing the writer's files. Independent tasks may run concurrently only with explicitly disjoint ownership. Do not launch other agents or provider calls merely because roles are documented. Ordinary tasks may never own governance paths; the only exception is a `phase_0` `FOUNDATION-` task on its matching `agent/<writer>/FOUNDATION-*` branch, which may own the engineering-governance files it must build while `SKILL.md`, `ops/memory/INVARIANTS.md`, `.git`, `.env` and the clinical domain stay forbidden.

Use `agent/<agent>/<task-id>` task branches and PRs into main, the single permanent branch; there is no develop branch. When all required automated gates pass, GitHub squash-merges automatically and the resulting main SHA deploys to the OVH development environment automatically. No direct main pushes, no manual runtime editing, no self-approval. Do not commit or push this Phase 0 change until the owner approves. Never include secrets in Git, prompts, logs or handoffs. Reference secret names only; do not read or print credential values.

The engineering harness chain is Codex + GPT-6 Astra (primary), OpenCode + GLM 5.3 (first fallback) and OpenCode + MiniMax-M3 (second fallback). Switching harnesses is an explicit human-approved writer handoff that preserves the same task, branch, base/HEAD SHA, Git-backed memory, reports and deterministic coordinator state.

SKILL.md is mandatory. Follow ops/memory/INVARIANTS.md. No agent approves Clinical Evidence or activates clinical Rules. Human clinical approval is separate from engineering review. If identity has zero, multiple or conflicting matches, preserve the conflict for mapping_exception; never guess.

Phase 0 permits engineering foundation 0A–0F: operating documentation, configuration/CI/CD tooling, provider smoke tooling, canonical memory/context, deterministic task coordination, disabled-backend research and worktree/dry-run preparation. Do not implement KMX, Evidence, Rules, source adapters or production migrations. Leave migrations/001_kmx.sql, 002_evidence.sql and 003_rules.sql unchanged.

On handoff, report changed files, exact checks and results, unresolved issues and the next action. Separate verified facts from operator-reported status and plans. Update memory through its assigned writer; do not mark unperformed checks as passing. Stop dependent work on scope conflicts and ask the owner to resolve them.

Use docs/AGENT_COORDINATION.md for task schema v2 and docs/AGENT_MEMORY.md for lifecycle persistence. Only the active writer owns task production paths; all other roles may write only their designated report. User authorization governs whether a checkpoint may actually commit/push; the current foundation task prohibits both. Human approval flags are operator-only attestations.
