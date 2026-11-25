---
name: dotnet-diagnostics-profiling
description: Investigate live .NET CPU, allocations, GC, contention, ThreadPool backlog and memory symptoms with dotnet-diagnostics-mcp; connect runtime evidence to source and verify focused performance repairs. Use for runtime profiling and performance diagnosis, not ordinary compiler errors or unsupported performance claims.
---

# .NET diagnostics and profiling

Use the user's selected `dotnet-diagnostics-mcp` to investigate an actual owned .NET process, locate the responsible source, repair a confirmed problem and repeat the same investigation. Installation or skill activation does not authorize attaching to unrelated processes, starting a workload, changing infrastructure or publishing results. Follow the repository's profiling, benchmark and execution policies.

## Connect and identify

Check `dotnet tool list -g`; when absent, install with the requested `dotnet tool install -g dotnet-diagnostics-mcp`. Use the available MCP connector. Its local stdio launch command is `dotnet-diagnostics-mcp --stdio`. Do not silently edit global MCP configuration or replace this server with another package. If its tools are unavailable, report that the installed executable is not a connected MCP server; tool installation alone does not prove attachment. Inspect the installed version and exposed tool schemas before invoking collectors: documentation from main can describe features newer than the installation.

When a connector is unavailable, use the self-contained [scripts/invoke.cs](scripts/invoke.cs), a .NET 10 file-based client using the official MCP C# SDK. It launches the selected server with `--stdio`, saves original request/response JSON, and retains handles until EOF closes the session. Use an absolute repository-owned capture directory and a fresh response directory for each session; do not reuse numbered response files. No global MCP configuration change is needed.

```sh
dotnet run --file /absolute/path/to/dotnet-diagnostics-profiling/scripts/invoke.cs -- /absolute/capture-root /absolute/fresh-response-directory
```

Send `{"tool":"tools/list"}` first, then JSON lines shaped as `{"tool":"inspect_process","arguments":{"view":"preflight","processId":12345}}`. The helper saves each request before calling the server, records client timeout/transport failure separately from native results, and allows a follow-up request after a bounded client failure. It sets `MCP_ARTIFACT_ROOT`; optional `DOTNET_DIAGNOSTICS_SERVER` selects the executable and `timeoutSeconds` sets a bounded per-request deadline. EOF disposes the SDK client and owned diagnostics server. Keep the session open for handle queries.

Run `inspect_process(view="list", commandLineContains="application-assembly")` and select the explicit actual PID. A path substring can also match the diagnostics client; confirm the managed entrypoint and never profile the helper as the application. Use `view="info"`, `view="preflight"` and `view="capabilities"` for that process. Reconfirm process identity after restart. Match the target to the actual owning application/container, source revision and compiled DLL/PDB identities. Never infer a database worker PID from a public HTTP port or treat the diagnostics host or load generator as the target server.

For permission or unsupported-runtime failures, preserve the returned reason and use the preflight remediation relevant to the requested operation. Do not weaken host security, auto-elevate an unrelated target or report unavailable collectors as empty successful evidence.

## Capture a bounded investigation

Choose the actual operation, dataset, concurrency, topology, resource limits and capture window before collecting. Preserve original workload correctness assertions, cancellation and joined cleanup. Start with Summary output and a short bounded window appropriate to the workload. Increase detail or duration only to resolve a concrete uncertainty.

- `collect_events(kind="sweep")` gives initial correlated runtime signals.
- CPU and allocation sampling use `collect_sample(kind="cpu")` and `collect_sample(kind="allocation")`.
- GC, contention and ThreadPool event investigations use `collect_events` kinds `gc`, `contention` and `threadpool`.
- `collect_batch` can align 1–4 independent collectors on one explicit PID/window. Its depth is `full` or `compact`; individual event/sample calls use `Summary`, `Detail` or `Raw`. Inspect each child error/quality result even when the batch succeeds. Collect contention/ThreadPool in a second bounded batch if the first already has four entries; `sweep` and `method-params` are excluded from batch.
- Follow returned handles through `query_snapshot` using views actually supported for that artifact. Preserve handle identity, expiry and collection window; do not invent handle values or mix captures from different processes.

Preserve native quality and loss fields; absent loss metadata is unknown, not zero. For allocation evidence, byte-weighted leaf attribution and call-tree sample occurrence counts are different measures. Treat hotspots, correlated counters and ranked hypotheses as leads. Distinguish sampling uncertainty, unresolved frames, filtered events, buffer loss, retention caps, collector failures and unsupported capabilities. Missing events do not prove absence. Managed CPU stack samples can include waiting threads; check wait evidence before assigning scheduler CPU cost to a parked stack.

For installed 0.28.0, `cpuBackend="EventPipe"` selects managed stack sampling explicitly; `Os` uses Linux perf or Windows ETW and is unavailable on macOS. Do not assume an Automatic/native backend refusal makes every managed collector unavailable: use actual capabilities and the native result. EventPipe `runningSamples=0` is not measured zero CPU; its evidence is stack frequency with heuristic waits. CPU collector `timings` describe collection/drain/symbol/source/aggregation wall cost, not target slowdown. Quantify target overhead only with matched instrumented and uninstrumented runs.

For GC events, legacy `totalPauseTime`, `maxPauseTime` and `pauseDuration` are collection elapsed time. Use `suspension.totalSuspensionTime`, `suspension.maxSuspensionTime`, `measurementVersion`, `measurementStatus` and `quality` for actual fully suspended intervals; missing suspension evidence stays unavailable.

Avoid raw payloads, method-parameter instrumentation, dumps, arbitrary logs and sensitive heap contents by default. Use aggregate runtime evidence first. Follow the actual server safety/authorization response and existing user scope when a more intrusive collection is necessary. Do not enable extra capture modifiers or retention merely because a tool supports them.

## Resolve and repair

Map sampled module/method identity to the matching compiled source and symbols. Use existing Roslynk semantic navigation where available, then read the owning feature requirements and lifecycle before editing. Inspect actual call paths, allocations, waits and ownership; a hot framework frame alone is not a product defect.

State the concrete hypothesis and evidence, make a narrow correctness-preserving change in the owning repository, and run meaningful operation regressions. Preserve authorization, cancellation, durability, replay, bounded admission and disposal. Dependency defects belong to their owning project; do not hide them with a duplicated consumer implementation.

Reprofile the same operation with matched source/build evidence, hardware, topology, dataset, operation counts, concurrency, resource limits and collector settings. Retain before/after captures and actual refusals or data loss. Separate the supported conclusion from remaining uncertainty.

## Performance claims and evidence

Diagnostic collection adds overhead and is not a clean benchmark result. Use a separate clean measurement lane for latency, throughput, allocation and memory comparisons; preserve complete result/state correctness. For KeyLoad, all benchmark-stage execution belongs to isolated Linux GitHub Actions under its canonical scenario inventory, real native topology and original artifact provenance. Do not start a local benchmark or substitute a microfixture for the required scale. Profiling permission remains governed by the current task and repository policy.

Report the actual target/source/image identity, workload and capture bounds, supported findings, source repair, regression results, matched reprofile and open clean-measurement gates. Skill validation, tool presence, connector discovery and successful capture are distinct receipts.

## Primary references

Installed 0.28.0 is bound by its NuGet repository metadata to commit `551dd045a87de0e49ffe3165103a6df6450d2adf`. Use its [matching tool reference](https://github.com/pedrosakuma/dotnet-diagnostics/blob/551dd045a87de0e49ffe3165103a6df6450d2adf/docs/tool-reference.md) to reconcile the observed schemas; recheck package metadata after upgrades.

Consult the maintained [client setup](https://github.com/pedrosakuma/dotnet-diagnostics/blob/main/docs/client-setup.md) for transport/attachment issues and [tool reference](https://github.com/pedrosakuma/dotnet-diagnostics/blob/main/docs/tool-reference.md) for exact current schemas, supported query views and quality limitations. The [owning repository](https://github.com/pedrosakuma/dotnet-diagnostics) is the source authority; reconcile its documentation with the installed tool surface before using newer features.

## Repository-local standalone client

This copy isolates its SDK client from package metadata/central-package imports with its local scripts/Directory.Build.props and explicit MSBuild flags:

```sh
dotnet run --file .codex/skills/dotnet-diagnostics-profiling/scripts/invoke.cs -p:ImportDirectoryBuildProps=false -p:ImportDirectoryBuildTargets=false -p:ManagePackageVersionsCentrally=false -- /absolute/capture-root /absolute/response-root
```
