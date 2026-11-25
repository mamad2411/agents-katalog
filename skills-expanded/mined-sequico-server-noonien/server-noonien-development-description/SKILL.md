---

name: server-noonien development description: How to work on the server-noonien repository — layout,
commands, CRDT rules and gates. Use when editing, adding tools, or reviewing code in this project.
---

# server-noonien development

## Layout

```
src/index.ts        bin `server-noonien`: the MCP server (no args, or `serve`)
src/noonien.ts     bin `noonien`: the maintenance CLI
src/gossip.ts       bin `nooniend`: the peer-to-peer replication daemon (no args)
src/server.ts       the tools, the graph and changes resources, and their subscriptions
src/serve.ts        stdio server bootstrap
src/cli.ts          CLI commands: serve / import / export / merge / compact / query / help
src/config.ts       environment configuration and backend wiring
src/env.ts          shared environment parsing (parseFlag, parseInteger)
src/host.ts         node-id resolution and injection-safe sanitising
src/errors.ts       shared ENOENT helper
src/diagnostics.ts  the single stderr channel
src/metrics.ts      dependency-free Prometheus registry
src/package.ts      package identity (name/version) for `initialize`
src/migrate.ts      official server-memory JSONL import
src/graph/          CRDT model: types, operations (the nine operations + shard.compact), hlc, codec, fold, graph
src/store/          shard log: read every shard, append to and compact the local one (online)
src/sync/           sync backends behind one interface: backend, file, s3, s3-aws, memory
src/gossip/         daemon: address, bootstrap, collection, config, daemon, digest, exchange, hook, knowledge, membership, protocol, replica, sampler, server, transport, types
scripts/            release preflight and the MCPB bundle (not shipped in the package)
test/               Vitest: unit, integration and CRDT property tests
docs/wayforward/    forward-looking plans: scaling.md, tools.md (not current state)
```

The package ships **three commands**: `server-noonien` (the MCP server), `noonien` (the CLI) and
`nooniend` (the replication daemon). Convergence needs a path between nodes: a shared area for
`file`/`s3`, or peer-to-peer replication for `nooniend`.

## Commands

```sh
npm run check       # Biome: lint + format + import order
npm run typecheck   # tsc --noEmit
npm run test        # Vitest (fast-check property tests live here)
npm run build       # tsc -> dist/
npm run gate        # all of the above

npm run release:check   # release preflight: versions, packaged bins, changelog heading
npm run mcpb            # build server-noonien-<version>.mcpb
```

Run `npm run gate` before claiming any work done. Zero errors, zero warnings.

## Adding or changing a tool

1. Keep the nine official tool names, inputs and outputs identical (drop-in contract). Extensions
   beside them are allowed while the nine stay exact; the `update_*`, `merge_entities`,
   `read_conflicts`, `resolve_conflict`, `read_changes`, `find_nodes`, `expand_nodes`,
   `find_duplicates`, `read_history` and `set_observations` tools are the current ones.
2. Model the change as operations in `src/graph/` — additive or tombstone (the `shard.compact`
   metadata op aside), never in-place mutation.
3. If it touches merge/serialization/order, add or extend property tests for idempotence,
   commutativity, associativity and convergence.
4. Update `README.md` if user-visible behaviour changed.

## Rules

- SSOT and no duplication within code/config and within docs; no workarounds.
- English content. Clean tree. Commit finished work locally as the standard operation; push only
  when the owner asks.
- Releases are automated with release-please: see the `server-noonien releases` skill before touching
  versioning or the release/CI workflows.
