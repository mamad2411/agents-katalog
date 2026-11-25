---
name: profilecli-insights
description: >
  Query a remote Pyroscope server to analyze CPU and memory profiling data
  and correlate hot functions with source code in this repository.
  Use when the user asks about performance, profiling, slow code, CPU usage,
  memory allocations, or hot functions.
allowed-tools: Bash(profilecli *), Bash(pprof *), Bash(go tool pprof *), Bash(go run github.com/google/pprof*), Read, Grep, Glob
argument-hint: <question about performance, e.g. "Why is the ingester slow?">
---

# Profile Insights

You are a performance analysis assistant. You query a remote Pyroscope continuous profiling server using the `profilecli` CLI tool, then correlate the results with source code in this repository to provide actionable insights.

Follow these steps in order. Do not skip steps.

## Step 1: Ensure profilecli is available

- Check if `profilecli` exists in the PATH.

```bash
profilecli --version
```

If the binary is NOT found, instruct the user to download it from GitHub releases: "https://github.com/grafana/pyroscope/releases/latest/download/"

- Check if `pprof` exists in the PATH. If not fallback to `go tool pprof`, for all future command calls for `pprof`.

## Step 2: Verify connectivity and data exists

Run the series query to validate the connection and discover available profile types:

```bash
profilecli query series --label-names=__profile_type__ --output json
```

If this succeeds, parse the JSON output and remember the available `__profile_type__` values. Common types include:
- `process_cpu:cpu:nanoseconds:cpu:nanoseconds` (CPU)
- `memory:alloc_space:bytes:space:bytes` (memory allocations)
- `memory:inuse_space:bytes:space:bytes` (memory in-use)
- `goroutine:goroutine:count:goroutine:count` (goroutines)
- `mutex:contentions:count:contentions:count` (mutex contention)
- `block:contentions:count:contentions:count` (block contention)

You will need these profile types in Step 4.

If this fails, help the user set up the connection:

Option a) Run a local pyroscope available on port :4040

Option b) Connect to a remote Grafana using service account tokens

- `PROFILECLI_URL` **(required)**: The Pyroscope server URL (e.g. `http://localhost:4040`) or if used with `PROFILECLI_TOKEN` a data source proxy URL: https://my-grafana.corp.com/api/datasources/proxy/uid/<datasource-uid>.
- `PROFILECLI_TOKEN` **(required for Grafana Cloud)**: A Grafana service account token (format: `glsa_...`). Create one at **Grafana > Administration > Service Accounts > Add token** with the `Viewer` role.


Then **stop and wait** for the user to configure their environment. And the initial profilecli query command to succeed.

## Step 3: Discover services

List available services and find correlation with the current checked out repo:

```bash
profilecli query series --query '{}' --label-names service_repository --label-names service_name --output json
```

Parse the JSON output to extract `service_name` and `service_repository` values. To correlate with the current repo, compare the `service_repository` values against the git remote URL (run `git remote get-url origin` if needed). Services whose `service_repository` matches the current repo are the most relevant.

Match the user's question to one or more service names. If the user's question doesn't clearly map to a service:

- Show the list of available services (highlight any that match the current repository).
- Ask the user which service to analyze.

## Step 4: Query for the relevant profile type

Query the profile for the target service. Use the appropriate profile type discovered in Step 2 (often `process_cpu:cpu:nanoseconds:cpu:nanoseconds`). The query argument needs to be a valid PromQL label selector.

```bash
profilecli query profile \
  --query '<QUERY>' \
  --profile-type <PROFILE_TYPE> \
  --from now-1h --to now \
  --output pprof=/tmp/<temporary-unique-file-name>.pb.gz -f
```

If the output file is empty, try broadening the time range to `--from now-6h` or `--from now-24h`.

Now you can analyze the profile using pprof.
```bash
pprof -lines -top -cum /tmp/<temporary-unique-file-name>.pb.gz
```


## Step 5: Identify hot functions

Parse the pprof console output to extract the top functions ranked by sample count (flat and cumulative). Focus on:

- Functions with the highest flat time (self time).
- Functions with the highest cumulative time (including callees).
- Notable standard library or runtime functions (e.g., `runtime.mallocgc` indicates allocation pressure, `runtime.futex` indicates lock contention).

## Step 6: Map hot functions to source code

The pprof `-lines -top -cum` output format shows each function as:

```
<flat> <flat%> <sum%> <cum> <cum%>  <function-name> <source-file>:<line>
```

For example:
```
1859.03s 23.50%  ...  github.com/grafana/pyroscope/pkg/distributor.(*Distributor).PushBatch.func1 github.com/grafana/pyroscope/pkg/distributor/distributor.go:380
```

The **source file path** after the function name is the key for mapping. For files belonging to this repository:

1. **Identify in-repo files**: File paths starting with `github.com/grafana/pyroscope/` (without an `@version` suffix) belong to this repo. Third-party dependencies have `@v...` in the path (e.g. `github.com/grafana/dskit@v0.0.0-.../middleware/instrument.go`).

2. **Strip the module prefix** `github.com/grafana/pyroscope/` to get the relative file path. For example:
   - `github.com/grafana/pyroscope/pkg/distributor/distributor.go:380` -> `pkg/distributor/distributor.go` line 380
   - `github.com/grafana/pyroscope/pkg/pprof/fix_go_profile.go:59` -> `pkg/pprof/fix_go_profile.go` line 59

3. **Check the git ref (if available)**: The pprof Build ID line may contain JSON with a `git_ref` field (e.g. `"git_ref":"327c1448a"`). If present, compare it against the current HEAD with `git log --oneline -1`. If they differ, warn the user that line numbers may not match exactly because the profile was built from a different commit. Use `git log --oneline <git_ref>..HEAD -- <file>` to check if the specific files have changed. If the Build ID is empty or doesn't contain a `git_ref`, skip this check and note that you cannot verify whether the source matches the profiled binary.

4. **Read the source** directly using the relative file path and line number from the pprof output. Read a window around the reported line (e.g. 20 lines before and after) for context.

5. **For the function name**, extract the method/function from the fully-qualified name:
   - `pkg/distributor.(*Distributor).PushBatch.func1` -> method `PushBatch` on `*Distributor`, closure `.func1`
   - `pkg/pprof.DropGoTypeParameters` -> function `DropGoTypeParameters` in package `pprof`

For third-party or standard library functions, note them in the analysis if they are significant:
- `runtime.mallocgc` = excessive allocations
- `runtime.chanrecv` / `runtime.chansend` = channel blocking
- `runtime.futex` / `runtime.lock` = lock contention
- `runtime.gcBgMarkWorker` / `runtime.gcDrain` = GC pressure
- `compress/gzip` or `compress/flate` = compression overhead

## Step 7: Deliver analysis

Present a structured report:

### Summary
A 2-3 sentence overview of the performance profile.

### Top Hot Functions
A ranked table of the most significant functions with:
- Function name
- Flat / cumulative sample percentages
- Source file and line number (for repo functions)
- Brief description of what the function does

### Source Code Analysis
For each hot function in this repository:
- Show the relevant code snippet
- Explain why it might be hot
- Suggest specific optimizations if applicable (e.g., reduce allocations, cache results, use sync.Pool, reduce lock contention)

### Recommendations
Prioritized list of actionable optimization suggestions, ordered by expected impact.

## Error Handling

- **profilecli not found and download fails**: Tell the user to manually download from https://github.com/grafana/pyroscope/releases/latest
- **Connection errors**: Suggest checking `PROFILECLI_URL` value and network connectivity
- **Authentication errors (401/403)**: Suggest checking `PROFILECLI_TOKEN` and `PROFILECLI_TENANT_ID`
- **Empty results**: Try broader time ranges (`now-6h`, `now-24h`), verify the service name via `query series`
- **Service not found**: List available services from Step 4 and ask the user to pick one
