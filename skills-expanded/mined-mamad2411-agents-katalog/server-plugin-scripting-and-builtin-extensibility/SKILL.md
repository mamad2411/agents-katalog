---
name: server-plugin-scripting-and-builtin-extensibility
description: Dual plugin system for a monitoring server — hot-reload script plugins (alert rules, filters) plus compiled JAR plugins for stateful, performance-critical data handlers
category: backend
version: 1.0.0
source_type: extracted-from-git
source_url: https://github.com/kjuhwa/scouter
source_ref: master
source_commit: 126bb19f07d1fe4fe915eb408c381e2c140cc94c
source_project: scouter
version_origin: extracted
tags: [plugin, extensibility, scripting, hot-reload, monitoring]
confidence: medium
---

# Dual Plugin Model: Scripted + Compiled

Apply when your server needs both "let ops change alert rules without a deploy" AND "let partners ship stateful integrations (InfluxDB sink, webhook pool)."

## Pattern

1. **Script plugins** — Groovy / JavaScript (or your preferred JSR-223 engine) files on disk, reloaded on change. Keep the API narrow: `on_alert(ctx)`, `on_xlog(ctx)`. Context is a read-only bag of pack fields + helper methods (log, notify).
2. **Compiled plugins** — JARs in a plugin dir, loaded at startup via a `ServerPlugin` interface. Can hold connection pools, background threads, state.
3. **Pipeline stage hooks** — `counter.plug`, `xlog.plug`, `xlogprofile.plug`, `alert.plug`, `summary.plug`, `object.plug`. Each intercepts data at a specific stage; ordering is deterministic.
4. **Sandbox script plugins** — disable file I/O, reflection, `System.exit`. Ops should not be able to DOS the server by editing a .plug file.
5. **Versioned plugin API** — breaking changes in ServerPlugin require major bump; scripts require a conversion script.

## Evidence

- `scouter.document/main/Plugin-Guide.md`
- `scouter.document/main/Alert-Plugin-Guide.md`
- `scouter.server/src/main/java/scouter/server/plugin/`

## Trade-offs

- Scripts = fast iteration, weak tooling, no compile-time safety.
- JAR plugins = type safety, hard to upgrade without restart.
- Two plugin surfaces = more docs, more examples, more bug surface.

## Related knowledge

- `plugin-architecture-runtime-vs-startup-loading` (arch)
