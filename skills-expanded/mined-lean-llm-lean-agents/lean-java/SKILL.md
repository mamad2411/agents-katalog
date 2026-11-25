---
name: lean-java
description: "Load lean-java when working on Java/JVM projects: Bukkit/Spigot/Paper/Folia plugins, Maven, testing, concurrency, performance, libraries or Spring Boot. Also load lean-web for mixed-stack tasks."
---

# lean-java

## Contract
Co-load `lean-code`; `AGENTS.md` controls routing.

## Detect before edits
Inspect configured bytecode, Maven/Gradle, modules and tests. Minecraft plugins default to **Java 8 bytecode and 1.8–1.21+ compatibility** unless repo explicitly differs; modern Spigot/Paper compilation does not prove legacy linkage. Check Folia runtime detection and ownership. Don't add Lombok or storage stacks without need.


## Design/API
Keep one authority for scheduler, state, history, storage and menu lifecycle; avoid duplicate listeners. Adapt at platform/API boundaries; select implementation once, not per event. Constructor-inject stable collaborators; minimize mutable state. Choose collections by access pattern; avoid hot-event streams/boxing and speculative `parallelStream()`. Preserve exception causes, interrupts, `equals`/`hashCode` and lock release in `finally`. Trace event/callback timing, persistence order, reload and failure paths.

## Concurrency / Folia (ownership first)
Reuse existing `FoliaAPI` / `RuntimeScheduler` bridge. Player/entity/inventory/GUI → **entity owner scheduler** (follows teleport); block/location/world changes → **region owner**; server-wide → **global**; SQL/disk/network/pure CPU → **async**. Async handles detached snapshots only, never Bukkit world/entities off-owner; return results to the correct owner. No raw threads, per-item scheduling, owner blocking or Bukkit scheduler fallback on Folia. Act on teleport futures' **actual completion**; callbacks aren't guaranteed owners. Isolate modern Folia/Paper symbols from legacy Spigot classloading. Set `folia-supported: true` only with verified ownership safety.

Shared state: prefer single ownership; otherwise immutable messages, `volatile`/atomics/locks with happens-before. `ConcurrentHashMap` read-modify-write is not atomic. Bound executors, per-UUID queues, caches and retries; batch I/O, backpressure, cancellation, orderly shutdown. No SQL/SQLite, YAML parsing/writing or future waits in events/commands/Netty/owner threads. Hot-path GETs stay in memory; async persistence needs ordered writes, stale-update protection and disable-time flush/drain. `CompletableFuture`: `thenCompose` dependencies, explicit executor/owner hops, propagate failures; preserve interrupts. Virtual threads require runtime support, never a plugin default.

## Build/dependencies
Follow BOM, scopes and Maven-first conventions; Gradle only in Gradle repos. Focused: `mvn -B -Dtest=ClassName test`; full: `mvn -B verify`; diagnose: `mvn dependency:tree` / `mvn help:effective-pom`. Java 8: configured `--release 8` where supported, otherwise source/target plus **bytecode and API audit**. Check legacy linkage, optional hooks, shading/relocation and classloaders; never bundle Bukkit API. Keep universal JAR/single module unless complexity warrants splitting; shade minimally.

## Tests
Red/green when feasible. Reuse JUnit/Mockito; independent AAA tests, parameterized distinct inputs, assert effects/invariants, not internals. Use real Bukkit event fixtures/fakes, not mocks of final event methods. Cover ordinary/special tools, disabled config, pre-cancelled events, other plugins, reload/shutdown, persistence order, Folia callbacks, old-API linkage, failure/cancellation. Observe at `MONITOR` without mutation; honor `ignoreCancelled`; don't cancel gameplay events merely for effects unless required. Preserve vanilla drops, durability, XP and progression. Runtime tests must verify ownership and real event ordering where relevant; counts/`BUILD SUCCESS` don't cover missing scenarios.

## Security/reliability review
Cache capability/reflection lookups **including misses**; invalidate mutable config caches on reload. Use existing logger. Incompatible APIs need cached safe alternatives, not reflective exceptions every tick.

## Spring Boot only (when detected)
Keep Boot version/persistence choice. Feature-oriented structure when helpful; constructor injection (`final` deps), typed external config. Validate DTOs (`@Valid`), don't expose entities; centralize API errors (`@ControllerAdvice`), transact at service boundaries. Test auth/CSRF, DB behavior, N+1/projections; check `javax`/`jakarta` compatibility.

## JVM diagnosis/perf (only when requested or implicated)
Use `top -H`, `jcmd <pid> Thread.print`, JFR/async-profiler and heap/GC evidence; dumps may pause production. Compare CPU/alloc/TPS, not microbenchmarks alone. Plugins: **no work when disabled**, no allocations/location/ItemStack/reflection on ordinary events, O(1) scoped indexes, cached material/API resolution, bounded expiry/eviction, aggregated schedulers, batched I/O; avoid global scans/repeated snapshots.
