---
name: deepseek-harness-plugin
description: Develop, extend, test, review, or troubleshoot plugins in the DeepSeek Harness repository. Use for new @deepseek-ai/dsh-* packages, Cordis service providers or consumers, model-facing tools, hooks, LLM adapters, session events, bundles, profiles, host/client plugins, and related documentation or test changes.
---

# DeepSeek Harness Plugin Development

Use this skill as repository-specific guidance, not as a substitute for reading the current source. DeepSeek Harness is a Cordis plugin tree: add behavior at an existing extension point, preserve reversible lifecycles, and validate the assembled entry path.

## Orient Before Editing

1. Locate the repository root. Prefer `git rev-parse --show-toplevel`; if the current workspace is a guide or symlink, resolve the actual `deepseek-harness` checkout before reading files.
2. Read the root `AGENTS.md`, then the nearest `AGENTS.md` for `packages/`, `packages/client/`, `examples/`, `docs/`, `scripts/`, or `.github/` as applicable.
3. Read `docs/architecture.md` before changing `packages/`. Load the focused source-of-truth document only when needed:
   - `docs/cookbook/adding-a-package.md` for a workspace package;
   - `docs/cookbook/adding-a-tool.md` for a model-facing tool;
   - `docs/cookbook/adding-an-llm-adapter.md` for a model provider;
   - `docs/cookbook/adding-a-conversation-node.md` for a Web Client node;
   - `docs/defensive-patterns.md` for lifecycle, async, subprocess, or teardown work;
   - `docs/testing.md` for test tier and snapshot requirements.
4. Find the closest shipped analogue and trace its Service Definition, Provider, Consumer, `cordis.yml` composition, tests, README, and package entrypoints before choosing a design.
5. Classify the change: single plugin, capability seam, model-visible behavior, durable session state, Host/Client split, or generated/documentation change. This classification determines package topology and evidence.

## Architecture Rules

- Treat every product feature as a plugin. Prefer a documented event, registry, service, or `agent.ctx` scope over modifying `agent-loop`.
- A swappable capability is complete only when its Service Definition, Service Provider, and Consumer responsibilities are represented. Keep roles in one package only when they do not evolve independently.
- Function plugins named-export `name`, `inject` when needed, `Config` when needed, and `apply`; they have no default export. Service packages default-export their service class. Do not mix the forms.
- Every registration is an owned effect: use `ctx.effect()`, `ctx.on()`, or a registry method that returns a disposer. Verify disposal and HMR cleanup.
- Use declared `ctx.<service>` injections only for required services. Use `ctx.get(name)` for optional services so topology changes do not turn an optional dependency into a hard injection.
- Select the event domain deliberately. Durable facts belong in the session log; live interception belongs in `agent/*`, capability events, or `tools/*`. Waterfall listeners must call `next()` unless they intentionally return a typed denial or replacement.
- Anything sent to a model must be reconstructable from the session log. A new model-visible input therefore needs a session event and replay/rendering support.
- Resolve deployment-varying behavior through validated `Config` fields and explicit `resolve(request)` logic. Do not hide defaults in `run()`, hardcode tunables, or silently skip missing references.
- Keep opaque cross-boundary identifiers branded, use discriminant switches with `assertNever` for closed unions, and keep public contracts in JSDoc and package README files.
- Trust TypeScript at typed same-process boundaries. Validate parser/config, model/tool JSON, durable/file, worker, process, and wire inputs; do not add defensive parsing solely for values statically guaranteed by a local interface.
- Keep source-plane checks on `src` and artifact-plane checks on built `lib/`; never use stale build output to make source tests pass. Do not edit `vendor/` directly; follow its sync manifest procedure.

## Choose the Implementation Path

### New workspace package

Follow `docs/cookbook/adding-a-package.md` and [package-and-config.md](references/package-and-config.md). Create `packages/<group>/<pkg>/` with `package.json`, `tsconfig.json`, `src/index.ts`, the paired README sources (`README.md`, `README.zh.md`, `README.i18n.yaml`) when the package is public, tests, and (when needed) `src/invariant.ts`. Use `@deepseek-ai/dsh-<name>`, ESM, explicit `.ts` source imports, strict TypeScript, and the exact package export/files contract. Register the package in the matching Host or Client aggregate; ordinary packages belong to one aggregate only.

### Model-facing tool

Read [plugin-recipes.md](references/plugin-recipes.md) and the tool cookbook. Register a typed `defineTool` definition on `ctx.tools`; make `output.schema` the canonical JSON API and keep human text in `output.render`. Honor `exec.signal`, use `exec.agent` only for durable follow-up context, and use `ctx.jobs` for published background work. Keep `presentCall`/`presentResult` pure and derive replayable UI metadata from arguments and canonical results. Put allow/deny/ask policy on `tools/pre-execute`, dispatch wrappers on `tools/execute`, transformations on `tools/post-execute`, and final observation on `tools/result`.

For a shipped `packages/<group>/tool-*` package, update the explicit `TOOL_PACKAGES` boot manifest and import in `scripts/gen-tool-catalog.ts`; run `pnpm run gen-tool-catalog` and verify the generated bilingual catalog through `pnpm run doc-sync`. Add the package to the relevant bundle/example composition only when the feature is shipped by that profile; opt-in tools stay out of shipped defaults.

### Provider or capability seam

Define the stable interface first, then implement a provider and a real consumer. Register providers through the owning registry/service, make duplicate and disposal behavior explicit, and let the consumer use the interface rather than provider-specific details. For filesystem, shell, subprocess, sandbox, subagent, web, compaction, or storage work, inspect the corresponding package README and capability graph before adding another abstraction.

### LLM adapter

Read `docs/cookbook/adding-an-llm-adapter.md` and the `llm-deepseek` analogue. Extend `LlmAdapter`, register one adapter per provider route, declare `Config` with schemastery and environment fallbacks, and honor `GenerateOptions.signal`. Emit `usage` before `finish` and nothing after; preserve raw JSON tool-argument fragments; allocate block indexes in first-seen order; reject unsupported options with `LlmError`; and choose documented throw versus in-band error semantics. Preserve minimal validated provider replay state when follow-up requests require it.

### Host/Client or Web feature

Read `packages/client/AGENTS.md`, the relevant client package README, and `docs/cookbook/adding-a-conversation-node.md`. Keep Host and Client compiler faces explicit. A client plugin normally extends the client base config, declares its `dsh.client` metadata, exports the client entry, uses the shared tsdown preset, and keeps browser rendering free of server-only imports. Render conversation data from the session/event projection and register keyed node renderers rather than coupling a package to a concrete UI component.

### Durable state, hooks, or protocol bridge

Choose a session event for durable state, an `agent/*` or `tools/*` listener for live policy, and a protocol adapter for external peers. Make cancellation, ownership, callback containment, and teardown quiescence explicit. A protocol prompt normally returns its enqueue receipt; do not infer turn completion by correlating a message id. Use `AgentHandle.dispose()` for agent-owned lifetimes.

## Implement and Document

- Keep module and export JSDoc focused on caller-visible behavior, timing, ownership, cancellation, durability, failures, and non-obvious invariants. Do not narrate obvious code or test steps.
- Update the owning package README with configuration, events, extension points, model-visible effects, limitations, and the required `Model Experience` / `Known Limitations and Deferred Work` sections. Generated catalogs and `type-equiv` blocks are updated through their generators, never by hand.
- For bilingual documentation, edit the canonical pair (`foo.md`, `foo.zh.md`, `foo.i18n.yaml`) according to `docs/AGENTS.md`; do not create locale directories or edit projected website output.
- A non-trivial change needs an Agent Note in the same change when it records a durable decision, mechanism, rejected alternative, or coverage gap. Keep it present-tense when implemented and never edit archived notes.
- Add a real runnable composition when behavior is product-visible. A hand-built `ctx.plugin(...)` fixture cannot replace a Loader/`cordis.yml` smoke for plugin export, composition, or entrypoint regressions.

## Validate the Change

Select the smallest evidence that covers the changed surface; do not default to the full suite.

1. Add or update keyless snapshots for non-trivial model-, protocol-, or UI-visible behavior through the owning runnable example. Review every fixture and expected-output diff.
2. Run real-API e2e only when provider behavior is in scope; suites self-skip without the relevant key. Never commit credentials.
3. Use built-artifact smokes for package bins, workers, subprocesses, or published exports; run `pnpm run build` first when a check consumes `lib/`.
4. For a new package or public contract, run the relevant subset of `pnpm run doc-sync`, `pnpm run constraints`, `pnpm run typecheck`, `pnpm run lint`, `pnpm run build`, and `pnpm run hygiene`. For a `tool-*` package, run `pnpm run gen-tool-catalog` and `pnpm run verify-tool-catalog`.
5. Run `git diff --check` and inspect generated files and the final package graph. Report exactly which commands ran and distinguish environment skips from product failures.

When a required command is blocked by the agent sandbox (credentials, network, IPC, file watching, or nested sandboxing), retry the unchanged command with the narrowest host escalation before diagnosing a project failure. Never bypass a genuine failure or weaken a gate.

## Reference Routing

Load only the reference needed for the current task:

- [plugin-recipes.md](references/plugin-recipes.md): plugin exports, event selection, tool contracts, capability seams, and LLM obligations.
- [package-and-config.md](references/package-and-config.md): package layout, manifests, TypeScript faces, build order, config/profile composition, and environment rules.
- [testing-and-docs.md](references/testing-and-docs.md): test tiers, real-entry-path requirements, snapshots, README/docs gates, Agent Notes, and check selection.

The referenced repository documents remain authoritative when a summary and the checkout differ.
