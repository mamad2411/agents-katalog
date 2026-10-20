---
name: framework-migrations
description: Port an existing application between agent, web, runtime, or orchestration frameworks while preserving framework-independent behavior, safety invariants, durability, and verifiable build quality.
---

# Framework Migrations

Use this skill when moving an existing application to a different framework or runtime, especially when the source mixes reusable domain logic with framework-specific agents, tools, routers, persistence, providers, or test harnesses.

## Goal

Produce a working target application that preserves behavior and safety contracts without importing the source framework into the new implementation. Treat the source as a behavioral specification, not as a directory to copy wholesale.

## Workflow

### 1. Inspect Before Editing

Read in parallel:

- source package structure and framework-independent libraries;
- source tests/evals and safety assertions;
- target workspace instructions and sibling package conventions;
- authoritative examples or source for the target framework APIs;
- root package manager, TypeScript, build, and workspace configuration.

Check repository status before writing. In shared worktrees, re-read a file immediately before patching if another agent may be editing it.

### 2. Draw the Boundary

Classify source files into:

- **portable core:** parsers, reducers, selectors, prompts, domain types, deterministic orchestration;
- **host adapters:** authenticated HTTP, database, queues, reporting, environment configuration;
- **authoring boundary:** agents, tools, hooks, routes, framework directives;
- **deployment/build boundary:** package manifest, TypeScript, bundler, database entrypoint.

Keep the portable core free of both the source and target framework. Replace source-specific adapters rather than carrying their dependency graph forward.

### 3. Characterize Before Porting

For a behavior-preserving port, strict greenfield TDD is adapted as follows:

1. Write or port characterization/safety tests against target module paths.
2. Run them and confirm an expected RED due to missing target modules or missing behavior.
3. Port the reusable core.
4. Implement target-framework boundaries separately.
5. Add focused adapter tests for credentials, mutation gates, replay behavior, and malformed outputs.

Do not delete proven source code merely because it predates the new tests. The source implementation is part of the specification; tests prove the target preserves it.

### 4. Implement Safety at the Host Boundary

Never rely solely on model output for mutation authorization. Put deterministic gates in host code:

- explicit allowlists and target narrowing;
- dry-run terminal behavior;
- attempt and concurrency limits;
- exact external-state readback before consequential mutation;
- credential presence checks before dispatching mutation-capable model stages;
- pessimistic parsing of malformed or ambiguous model output;
- fork/default-branch/force-push restrictions;
- secret-safe logging.

When a stage can mutate, do not even invoke that stage without required host credentials and verification capabilities. A later refusal cannot undo an earlier claim/comment/push.

### 5. Make Durability Explicit

For durable runtimes:

- give each logical stage a stable replay identity;
- wrap side effects in the framework's durable step primitive;
- keep stage return values JSON-serializable;
- use a persistent database adapter rather than an in-memory default;
- preserve deterministic stage ordering and idempotent external writes;
- keep the database entrypoint and path configurable by the host.

### 6. Verify Dependencies Against Reality

Before finalizing package pins, resolve/install the exact requested versions. Do not claim a requested prerelease exists because a local reference checkout uses related APIs. If the exact pin cannot resolve, try the authoritative registry/source path, then use a known-compatible available version only when needed to produce a working artifact—and report the deviation precisely.

### 7. Coordinate Parallel Ports Safely

When delegating several target applications:

- scaffold and pin shared packages before dispatching workers;
- give every worker a disjoint directory and prohibit edits to root manifests, lockfiles, and sibling apps;
- do not patch a worker-owned manifest while that worker is still running—it may overwrite the correction later;
- wait for workers to finish, reconcile framework versions once, then install once at workspace root;
- avoid interpreting build/version failures observed during a concurrent dependency install as stable results.

For transport migrations, prefer the target framework's official SDK over hand-authored HTTP. Test the exact admission body and receipt shape with an injected fetch/client transport.

### 8. Verify in Two Scopes

Run target-package verification first:

1. typecheck;
2. offline tests;
3. production build.

Then run workspace-wide equivalents. This separates regressions in the migrated app from unrelated sibling-package failures. If the workspace fails elsewhere, capture the exact package/error and do not modify unrelated code unless it is explicitly in scope.

### 9. Final Review

Before reporting completion, verify:

- no imports from the source framework remain;
- required standing rules/instructions are mounted on every root and child agent;
- generated output and durable data are ignored where appropriate;
- router paths and database entrypoints are included in the build;
- tests cover dry-run, malformed output, attempt limits, claim refusal, external verification, and mutation refusal;
- the final report distinguishes target success, workspace status, and dependency deviations.

## Pitfalls

- Copying source agents/tools wholesale and retaining hidden source-framework coupling.
- Mounting subagents but accidentally running every stage through an undifferentiated root model without stage-specific instructions.
- Treating a readback check after a claim as sufficient when the claim itself is already a mutation.
- Using a mock-only adapter shape in live code instead of a token-backed host adapter.
- Returning objects with optional `undefined` fields where a framework requires strict JSON values; use a stable shape with `null` where appropriate.
- Stopping after tests while typecheck or production build still fails.
- Trusting compile/build alone in hook-based frameworks; invalid delegate hooks may fail only when the agent renders.
- Leaving a workspace `test` script on a package with no discovered tests; aggregate runners often treat “No tests found” as failure.
- Letting parallel workers share manifests or lockfiles, then racing their installs and version corrections.
- Fixing unrelated workspace packages to make a root command green.
- Recording transient registry or setup failures as permanent framework limitations.

## References

- See `references/durable-agent-framework-port.md` for a general file map and verification checklist for durable agent applications.
- See `references/flue-2-port.md` for the concrete Flue 2 authoring, provider, SDK dispatch, durability, and workspace-verification traps.
- For package-versus-app ownership during a Flue monorepo migration, load `filesystem-first-agents` → `references/flue-logical-agent-package-boundaries.md`; it is the canonical source for `@agents/*`, app-local `src` scanning, thin wrappers, host contracts, runtime assets, and generator migration.
- See `references/flue-vs-eve-computer-user.md` for the Studio browser/payment agent port (MCP stdio CUA lib shared; Eve wins on evals; Flue wins on ops shell).
- Studio transport detail lives under `filesystem-first-agents` → `references/eve-cua-mcp-ssh-transport.md`.
