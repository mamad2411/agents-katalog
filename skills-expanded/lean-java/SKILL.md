---
name: lean-java
description: "Load lean-java when working on Java/JVM projects: Bukkit/Spigot/Paper/Folia plugins, Maven, testing, concurrency, performance, libraries or Spring Boot. Also load lean-web for mixed-stack tasks."
---

# lean-java

## Contract
Use with `AGENTS.md` for roles/delegation. This skill governs Java implementation, not task routing. Read current source; keep the requested scope. Delegated CODER loads it; ORCHESTRATOR need not duplicate reads. Stop at verified outcome or explicit blocker.

## Detect before edits
Identify JDK + configured bytecode, Maven/Gradle, modules, framework, deploy targets, test setup. Preserve public contracts and the project's chosen architecture. Minecraft plugins default to **Java 8 bytecode and 1.8–1.21+ compatibility** unless repository explicitly differs; compiling against modern Spigot/Paper APIs does not prove legacy linkage. Check Folia ownership and runtime detection. No Java upgrade, new framework, dependency, Lombok, storage stack, or generated-file edits without need.

## Work: root cause → minimal patch → proof
Reproduce or trace a falsifiable failing path. Fix the owner of the defect, not its symptom; inspect event order, callback timing, persistence ordering, reload and failure paths. Preserve null/error contracts, units, permissions, security and UX. No speculative features, unrelated refactors or Git mutations.

## Design/API
Use simple cohesive classes and reusable utilities only when they remove real duplication. Prefer **one authority** for scheduler, state, history, storage or menu lifecycle; avoid god-managers, facade chains, one-use abstractions and duplicate listeners. Put adapters at true platform/API boundaries; select implementation once, not per event. Constructor-inject stable collaborators; minimize mutable state. Choose collections by lookup/update pattern; avoid streams/boxing in hot events and speculative `parallelStream()`. Preserve exception causes, interrupts, `equals`/`hashCode`, resource closure and lock `finally` semantics.

## Concurrency / Folia (ownership first)
Minecraft: reuse existing `FoliaAPI` / `RuntimeScheduler` bridge. Player/entity/inventory/GUI → **entity owner scheduler** (follows teleport); block/location/world changes → **region owner**; server-wide → global; SQL/disk/network/pure CPU → async. Async tasks only process detached snapshots; never access Bukkit world/entities off-owner. Marshal results back to the correct owner. No raw threads, one-task-per-item schedules, blocking owners, or Bukkit scheduler fallback when on Folia. Handle teleport futures by their **real completion**, not guessed success; callback threads are not guaranteed owners. Bridge must isolate modern Folia/Paper symbols from legacy Spigot classloading. Mark `folia-supported: true` only with real ownership safety.

Shared state: single owner when possible; otherwise immutable messages, `volatile`/atomics/locks with happens-before. `ConcurrentHashMap` does not make read-modify-write atomic. Bound executors, per-UUID work queues, caches and retries; batch I/O, use backpressure, cancellation and orderly shutdown. Never query SQL/SQLite, parse/write YAML or wait on futures in events/commands/Netty/owner threads. Keep hot-path GETs in memory; persist asynchronously with ordered writes, stale-update protection and flush/drain on disable. `CompletableFuture`: `thenCompose` for dependent futures, deliberate executor/owner hop for continuations, propagate failures; don't swallow interrupts. Virtual threads only if supported by actual runtime, never as a plugin default.

## Build/dependencies
Follow repo wrapper, BOM, scopes and Maven-first conventions. Maven focused: `mvn -B -Dtest=ClassName test`; full: `mvn -B verify`; diagnose dependencies via `mvn dependency:tree` / `mvn help:effective-pom`. Gradle only when repo uses it. For Java 8 use configured `--release 8` where supported, otherwise target/source + **bytecode and API audit**. Check legacy linkage, optional plugin hooks, shading/relocation and classloader constraints; Bukkit API must not be bundled. Keep universal JAR/single module unless genuine complexity warrants splitting; shade minimally. Do not claim a skipped/failed test as PASS; record exit code and tested artifact.

## Tests
Behavioral regression first: red before / green after when feasible. Reuse existing JUnit/Mockito setup; AAA, independent tests, parameterize distinct inputs, assert **effects and invariants**, not implementation details. Avoid mocks of final Bukkit event methods; use real event fixtures/fakes. For plugins test: ordinary vs special tool, disabled config, event already cancelled, other plugins, reload, shutdown, persistence order, Folia callbacks, old-API linkage, failure/cancel paths. Bukkit listeners should observe at `MONITOR` without mutation; never cancel a gameplay event merely to implement effects unless explicitly required, and honor `ignoreCancelled`. Verify that changing a listener does not break vanilla drops, durability, XP or progression. Use integration/runtime tests when ownership and real event ordering matter. Counts or `BUILD SUCCESS` are not proof of missing scenarios; identify unrun runtime tests.

## Security/reliability review
Validate commands/config/input and permissions at boundaries; parameterize SQL; protect secrets, paths, auth and serialization. Preserve transaction/rollback semantics and idempotent retries. Cache capability/reflection lookups **including misses**; invalidate mutable config caches deliberately on reload. Prefer existing logger; diagnose failures, never hide them behind broad catch/fallback. Incompatible API needs a cached safe alternative, not repeated reflective exceptions per tick.

## Spring Boot only (when detected)
Keep existing Boot/version and persistence choice. Feature-oriented structure when helpful; constructor injection (`final` deps), typed external config, no secrets in source. Validate DTOs (`@Valid`), do not expose entities, centralize API errors (`@ControllerAdvice`), put transactions at appropriate service boundary. Test auth/CSRF and DB behavior, N+1/projections. Use version-matched docs for `javax`/`jakarta` transitions; no unsolicited stack migration.

## JVM diagnosis/perf (only when requested or implicated)
Profile first: `top -H`, `jcmd <pid> Thread.print`, JFR/async-profiler, heap/GC evidence as available; dumps can pause production. In plugins prioritize **no work when disabled**, no allocations/location/ItemStack/reflection on ordinary events, O(1) scoped indexes, cached material/API resolution, bounded expiry/eviction, aggregated schedulers and batched I/O. Avoid global scans and repeated snapshots. Optimization loop: baseline → isolate hotspot → smallest change → focused correctness gate → same-load CPU/alloc/TPS comparison; state scenario, hardware, command, repetitions and uncertainty. Microbenchmarks alone cannot establish server TPS gains. Stop if improvement falls within noise; do not invent measurements.

## Hybrid Java + web (only if relevant)
For React/Next.js, Better Auth, Turborepo, JS/TS or Node.js code alongside Java, also load `skills/lean-web/SKILL.md` for web-specific rules. Skip it on Java-only tasks.

## Report
`STATUS` (PASS/UNVERIFIED/BLOCKED/FAILED); `CHANGES` (file paths + behavior); `CHECKS` (exact command, exit, counts); `RISKS` (untested compatibility/runtime/integration); measured numbers only with repeatable method. No claim of success without relevant proof.
