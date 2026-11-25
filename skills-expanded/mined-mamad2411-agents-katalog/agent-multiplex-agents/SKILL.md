# Repository instructions for coding agents

Agent Multiplex is a protocol-v5 distributed control plane. Before changing it,
read the single fresh-session handoff at
[`docs/wiki/Current-State.md`](docs/wiki/Current-State.md), then the topical
guide and deep design for the role you are touching. Use
[`docs/wiki/Home.md`](docs/wiki/Home.md) only as the documentation index; the
checkpoint is an evidence ledger, not a second onboarding document.

## Maintained boundary

- Active roles are control node, runtime node, access gateway, client, and
  harness adapter.
- `apps/host` and `packages/host-core` are archived protocol-v2 evidence. Never
  import, repair, build, test, or use them as a v5 compatibility layer.
- Protocol v5 has no `sessions.spawn`; public creation is `launches.create` via
  an exact launch profile fence.
- `@arduano/p2prpc-core` is an exact, independently released transport
  dependency. Use `../p2prpc` to develop and qualify transport changes, but do
  not commit a local/file dependency to a release candidate.
- Image bytes and first-display file snapshots belong to runtime nodes and
  remain immutable until archive. Read [the image design](docs/design/images-v5.md)
  before changing image paths, transfer, retention, or native envelopes.
- Runtime code never fetches remote image URLs or renders/converts SVG; clients
  own interpretation of transferred `image/svg+xml` bytes.
- Native history belongs to Codex/Copilot. Never parse vendor history files or
  use terminal scrollback as canonical history.

## Data-role invariants

- Control nodes alone own canonical catalog state and flat namespaced JSON
  metadata. An attached aggregate has no independent metadata authority.
- Runtime nodes own native bindings, adapter calls, provider checkpoints,
  runtime journals, and managed PTYs.
- Gateways have zero domain-data authority. They observe one or more control
  sources and propose routed actions; gateways cannot be chained.
- Control nodes form a strict tree. Disconnect never promotes a branch. Partial
  overlap, authority forks, and duplicate domain identities fail closed.
- Stop preserves resumability. Archive is a separate durable operation after
  backend/provider release and must never be inferred from age or liveness.
- Ambiguous side effects become `outcomeUnknown` and are reconciled by stable
  operation ID, never blindly retried.
- Model, mode, interaction, command, event, and history shapes may be
  harness-specific. Preserve native semantics rather than flattening them.

## Where code belongs

- Wire schemas and tRPC-compatible contracts: `packages/protocol`.
- SQLite engine behavior: `packages/storage-sqlite`.
- Authority, catalog, metadata, tree routing: `packages/control-node-core`.
- Bindings, launch providers/backends, path policy, terminals:
  `packages/runtime-node-core`.
- Multi-source validation/selection/routing and restricted plugin capability:
  `packages/gateway-core`.
- Node-to-node binding: `packages/transport-p2prpc`.
- Browser-safe HTTP/WS construction and retry/cursor helpers: `packages/client`.
- Node-only direct control-source client: `packages/client-p2prpc`.
- Harness-native behavior: the corresponding `packages/adapter-*` package.
- Reference process composition: `apps/*`.
- Company/workflow policy: a statically composed gateway plugin plus runtime
  provider/backend, not protocol core.

## Change discipline

- Inspect current source and tests before editing; do not rely on archived docs
  or generated `dist` declarations as implementation truth.
- Preserve unrelated workspace changes. Use small patches and avoid destructive
  Git or filesystem commands.
- Do not hand-edit `packages/adapter-codex/src/generated`. Regenerate it from the
  exact pinned Codex CLI and review the complete generated diff.
- Treat protocol IDs, profile/schema hashes, authority and boot fences,
  migration names, and operation payload hashes as compatibility boundaries.
- Append SQLite migrations. Never reorder, rename, or rewrite released entries.
- Keep credentials in runtime/gateway configuration, not launch input, metadata,
  logs, receipts, tests, screenshots, or URL query strings.
- Plugins/providers are trusted static code, not a sandbox or dynamic loader.
- UI changes under `apps/web` should also follow
  `.agents/skills/agent-multiplex-ui/SKILL.md`.

## Verification

Run focused tests while iterating, then the repository gates for a checkpoint:

```bash
npm run typecheck
npm test
npm run check:checkpoint
npm run check:docs
npm run check:release
```

Validate `../p2prpc` independently when changing the transport package. Use the
deterministic Docker tree and mock-scale suites for topology/scale changes. Run the real
four-container suite only when native Codex/Copilot behavior needs qualification
and model-credit use is authorized.

Do not call a run qualified unless the exact source and dependency boundary
produced a successful, scrubbed, checksummed receipt. Failed receipt directories
are diagnostics, not evidence. Never publish raw tickets, bearers, shared
secrets, provider credentials/endpoints, terminal lease secrets, or auth homes.
The complete `receipts/` tree is intentionally local and gitignored; use the
tracked checkpoint and linked release evidence for facts available to a fresh
clone.

## Documentation

Update the relevant wiki page and deep design document when a maintained
boundary changes. Keep examples on protocol v5 terminology and link to source
contracts rather than copying large unstable type definitions. Security-impacting
changes also require review of `SECURITY.md` and `THIRD_PARTY_NOTICES.md`.

`docs/wiki/Current-State.md` owns current release/session-handoff facts,
topic pages own operational guidance, maintained design documents own detailed
invariants, and `docs/checkpoint-v4.md` owns qualification evidence. Update the
owner instead of repeating changing facts across several pages.
