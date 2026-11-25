---
name: pi-orchestra
description: Orchestrates complex coding work with Pi Agent Orchestrator using parallel read-only discovery, bounded planning, isolated implementation, evidence collection, and verification. Use for repository audits, architecture work, multi-file changes, security reviews, release readiness, or any task that benefits from multiple specialized agents.
license: MIT
compatibility: Requires @groeponline/pi-agent-orchestrator loaded in Pi.
---

# Pi Orchestra

Use the orchestrator as a controlled execution system, not as an excuse to spawn agents indiscriminately.

## Operating model

1. Define the requested outcome, constraints, non-goals, and evidence required for completion.
2. Decide whether the task is actually parallelizable. Keep trivial or tightly coupled work in one agent.
3. Start with read-only discovery for unfamiliar repositories or broad changes.
4. Give each agent a non-overlapping responsibility and a concrete return contract.
5. Synthesize findings before any writer is launched.
6. Use one writer per overlapping file set. Prefer an isolated worktree for implementation.
7. Run the repository's real validation commands and report exact failures.
8. Return the result, remaining risks, and preserved recovery paths. Never claim completion from agent status alone.

## Default topology

For a broad engineering task, use this sequence:

### Phase 1: parallel evidence

Launch two to four read-only agents in parallel:

- **Explore — architecture:** map the relevant modules, entry points, data flow, and invariants.
- **Explore — correctness/security:** identify concrete defects, unsafe assumptions, and edge cases.
- **Explore — tests/release:** inspect test coverage, CI, packaging, deployment, and rollback paths.
- **Analysis — data/benchmarks:** only when the task requires calculations, structured datasets, or benchmark interpretation.

Every discovery agent must return:

- exact file paths and symbols;
- observed behavior, not speculation;
- severity or impact;
- a proposed verification method;
- open uncertainties.

### Phase 2: synthesis and plan

Use one Plan agent after discovery. Give it the deduplicated evidence, constraints, and requested outcome. Require:

- ordered implementation steps;
- files expected to change;
- compatibility and migration concerns;
- test plan and failure recovery;
- explicit exclusions that prevent scope drift.

Do not pass raw agent transcripts when a concise evidence digest is sufficient.

### Phase 3: bounded implementation

Only implement when the user requested code changes.

Use one general-purpose agent for a coherent change set. Use separate writers only when their file ownership cannot overlap. Each writer must receive:

- the approved scope;
- the relevant evidence and plan;
- exact validation commands;
- a prohibition on unrelated refactors;
- a maximum turn or budget appropriate to the task.

Prefer worktree isolation for changes that may need review or recovery. Never discard a dirty worktree after a failed commit, branch creation, or cleanup.

### Phase 4: independent verification

After implementation, run the repository's authoritative formatter, linter, type checker, tests, build, packaging checks, and targeted security or performance checks. Use a fresh read-only reviewer when the change is security-sensitive, release-critical, or architecturally broad.

A green agent completion state is not verification. Cite command results and remaining untested surfaces.

## Concurrency rules

- Do not assign the same investigation to multiple agents unless deliberate independent review is required.
- Do not let parallel writers touch the same files.
- Avoid nested agent spawning unless the parent has a clear budget and the child adds distinct evidence.
- Use the smallest useful number of agents; three focused agents usually outperform a large undirected swarm.
- Stop or steer agents that drift, duplicate work, or operate without evidence.
- Open `/agents` to inspect status, resource use, queued work, conversations, and recovery state.

## Safety and release boundaries

- Read-only agents must remain read-only.
- Do not weaken permission inheritance to make a task easier.
- Do not publish packages, push release tags, merge pull requests, or deploy production changes unless explicitly requested.
- Do not hide failed checks behind retries. Distinguish deterministic failures from infrastructure flakes.
- Preserve exact recovery information for failed worktree cleanup or partial implementation.
- Treat package manifests, release workflows, permissions, and generated artifacts as production code.

## Completion contract

Return:

1. What changed or what was found.
2. Evidence: files, symbols, commands, tests, or benchmark output.
3. What was deliberately not changed.
4. Remaining risks or blocked actions.
5. The next release or merge action only when it is actually required.
