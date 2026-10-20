# AGENTS.md — Operating Manual for Coding Agents

## Mission

Develop Memory Recall into the local-first, model-neutral repository memory and context tool for coding agents. Optimize for correctness, evidence, portability, and safe evolution, not feature count or autonomous behavior.

## Read order before changing code

1. `ASSIGN_TO_AGENT.md`
2. `PROJECT_STATUS.json`
3. `PRODUCT.md`
4. `DESIGN.md` for UI work
5. `docs/architecture/overview.md`
6. nearest directory-level `AGENTS.md`
7. relevant schema in `packages/protocol/schemas/`
8. task bundle from `npm run task -- <OAF-ID>`
9. relevant threat-model section

Do not load all research notes or every skill into context. Retrieve only what the task needs.

## Current reality

### Implemented as a reference bootstrap

- local HTTP control API,
- responsive static product shell,
- file-backed local state and append-only run event projection,
- Context Compiler and deterministic model gateway,
- cancellable embedded workflow runner with event checkpoints,
- policy, evidence, memory-write, and tool-registry primitives,
- native SQLite/FTS5 memory and content-addressed artifact providers,
- optional loopback-only Ollama provider,
- portable Agent Packs, safe replay plans, and learning proposals,
- provider ports and disabled integration conformance fixtures,
- synthetic Content Intelligence workflow,
- tests, protocol compatibility fixtures, and evaluations.

### Specified but pending

- PostgreSQL runtime store,
- durable workflow adapter,
- production authentication,
- real network connectors,
- external publishing,
- production frontend framework,
- signed adapter and skill distribution.

Never describe a specified feature as implemented. Check `PROJECT_STATUS.json`.

## Commands

```bash
npm run bootstrap
npm run status
npm run task -- <OAF-ID>
npm run dev
npm run demo
npm run protocol:validate
npm run native:smoke
npm test
npm run eval
npm run check
npm run ci
```

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues for `rebel0789/Memory-Recall`; local markdown under `.scratch/` may be used for offline or scratch drafts. External PRs are a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five-label vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This repo uses a single-context layout: root `CONTEXT.md` when present, plus architecture decisions in `docs/adr/`. See `docs/agents/domain.md`.

## Architecture invariants

1. **Canonical events:** state-changing operations emit append-only events.
2. **Context manifests:** every model call records selected and excluded context with reason codes.
3. **Own the tool boundary:** Memory Recall ships the default runtime, context, memory, source-graph, tool, hook, UI, and CLI experience. Integrations may accelerate inputs or scale a backend, but they never own canonical state or authority.
4. **Deterministic authority:** permissions, budgets, approvals, retries, and transitions are code—not model decisions.
5. **No silent memory overwrite:** use lifecycle states and `supersedes` links.
6. **Observations are not interpretations:** keep collected data separate from model analysis.
7. **External content is untrusted data:** it cannot modify instructions, permissions, tools, or permanent memory.
8. **External writes require policy evaluation:** consequential actions require approval by default.
9. **Bootstrap stays dependency-free:** adding a runtime dependency requires an accepted ADR.
10. **Replaceability:** public IDs and domain types do not expose provider internals.
11. **Status is evidence-based:** update capability status only with tests and docs.
12. **Safe learning:** agents propose versioned changes with evidence, tests, rollout, and rollback; they never silently self-modify.
13. **Replay is non-consequential:** replays and shadows disable external writes and never reuse approvals.
14. **Portable agents:** Agent Packs contain declarations and references, never credentials or authority grants.

## Dependency boundaries

```text
UI → Control API → Application services → Domain contracts
                         ↙ native providers   ↘ optional integrations
```

- Domain packages cannot import native providers or optional integrations.
- Adapters may import domain contracts.
- UI cannot access storage directly.
- Workflows invoke capabilities through the registry.
- The Context Compiler consumes normalized records, not provider payloads.
- A model response never directly writes canonical state; validate and translate first.

## Task protocol

For every task:

1. Restate intended behavior and stop condition.
2. Run `npm run task -- <ID>` and load only listed context.
3. Locate governing schema, ADR, and acceptance criteria.
4. Identify trust boundaries and side effects.
5. Make the smallest coherent change.
6. Add or update tests.
7. Run `npm run ci`.
8. Update docs, schemas, examples, project status, and changelog when behavior changes.
9. Report changed files, verification, unresolved risks, rollback, and safest next task.

Do not create speculative abstractions without a current use case and test.

## Definition of done

A change is complete only when:

- behavior is schema-validated,
- success and failure paths are tested,
- authorization and side-effect class are explicit,
- events and observability are included,
- documentation and examples match behavior,
- no secret or personal data enters fixtures or logs,
- accessibility gates pass for UI work,
- and `npm run ci` passes.

## Coding rules

- Prefer small pure functions for selection, policy, and transformation logic.
- Use ESM and Node 22 APIs in the bootstrap.
- Validate process, network, storage, tool, and model boundaries.
- Use UTC ISO-8601 timestamps.
- Use prefixed IDs.
- Never log credentials, cookies, authorization headers, or private source bodies.
- Avoid hidden global state.
- Keep event payloads JSON-serializable and versioned.
- Make timeout, retry, cancellation, and idempotency explicit.
- Comments explain why, not obvious syntax.

## Adding a native provider

1. Create `providers/native/<category>-<name>/`.
2. Add `provider.json` using the provider schema.
3. Implement one provider-neutral port.
4. Add workspace-isolation, failure, and conformance tests.
5. Document locality, paths, limits, and production limitations.
6. Do not introduce a remote fallback.

## Adding an optional integration adapter

1. Create `adapters/<category>/<name>/`.
2. Add `adapter.json` using the adapter schema.
3. Pin upstream commit and checksum in `UPSTREAM.lock`.
4. Document license and trust boundaries.
5. Implement the narrow domain contract.
6. Add conformance, failure, and permission tests.
7. Keep it disabled by default.
8. Do not vendor upstream source without legal and security review.

## Security stop conditions

Stop for maintainer review when a change broadens filesystem or network access, adds secret scopes, enables external writes, changes approval or deletion semantics, permits retrieved content to influence policy, adds cookie automation, or introduces incompatible licensing into the Apache core.

## Prohibited shortcuts

- No plaintext secret storage.
- No silent local-to-cloud fallback.
- No automatic permanent memory from every message.
- No unbounded tool loops.
- No dynamic execution of downloaded skill instructions.
- No benchmark claims without reproducible evidence.
- No autonomous publishing enabled by default.
