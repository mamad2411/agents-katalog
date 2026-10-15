---
name: loci-post-edit
description: >
  Compare pre-edit and post-edit compiled artifacts to report execution
  timing % diff, energy consumption, and control-flow analysis.
when_to_use: >
  MANDATORY after any Edit/Write/MultiEdit to C/C++/Rust source
  (.c,.cc,.cpp,.cxx,.h,.hpp,.hxx,.rs). Invoke IMMEDIATELY — do not skip,
  batch, or wait. Also: "analyze the change", "measure the edit", "timing diff".
---

# loci-post-edit

This skill merges execution-trace (timing/energy) and control-flow (CFG)
analysis into a single post-edit report. It compares pre-edit and post-edit
compiled artifacts to show exactly how the change affects hardware execution.


Check that loci MCP is connected and authenticated, you see the tools before
running the preflight steps that require it. If the MCP is unavailable, tell
the user:

> LOCI MCP server is not connected. Please run `/mcp` in Claude Code to
> manage MCP servers, then approve the **loci** server. If it does not
> appear, restart Claude Code — the plugin registers it automatically on
> startup.

For plugin to work mcp should be authenticated and connected.

## Step 0: Check session context

Read the persisted detection results from `state/project-context.json` in the
plugin directory. This file is written once by setup.sh at session start and is
the single source of truth for compiler, architecture, and build system.
**Do NOT re-run detection or fall back to ELF/build-system sniffing.**

```json
{
  "compiler": "...",
  "build_system": "...",
  "architecture": "...",
  "loci_target": "...",
  ...
}
```

If the file does not exist, stop and tell the user:

> LOCI session context not found. Please restart Claude Code so the plugin
> setup runs and detects the project environment.

Also check the `system-reminder` block emitted at session start for:

```
Target: <target>, Compiler: <compiler>, Build: <build>
LOCI target: <loci_target>
```

Map the LOCI target to loci MCP supported architectures and binary targets:

| LOCI target |   Time from CPU  |
|---|---|
| aarch64 | A53 |
| armv7e-m | CortexM4|
| armv6-m | CortexM0P |
| tc3xx | TC399 |

If the architecture is **not** in this table, emit and stop:

```
Supported: aarch64 , armv7e-m , armv6-m , tc399
```

## Step 1: Identify pre-edit and post-edit artifacts

Locate the compiled artifact (`.o` or linked binary) for the edited source.
Check build output directories from the project's build system, not just the
source directory.

If no post-edit `.o` exists, compile the edited source with `-c` using the
compiler and flags from step 0 (same as preflight Step 1).
Always include `-g` to emit DWARF debug info (required by asm-analyze):
```
<compiler> -g <flags> -c <source> -o <basename>.o
```

**Validate the .o after compilation** — a standalone `-c` compile can exit 0
yet produce an empty object file when the source is wrapped in `#if` / `#ifdef`
guards whose defines (`-D`) were not on the command line. After compiling, run:
```
<asm-analyze-cmd> extract-symbols --elf-path <basename>.o --arch <loci_target>
```
If the result shows 0 symbols or returns an error mentioning "no code" or
"preprocessor", the target function was compiled out. In that case fall back to
the existing linked binary (`.elf`, `.out`) for analysis instead. If no linked
binary exists, report that standalone compilation produced an empty object and
the full project build system is required.

For the pre-edit artifact: the preflight hook saves `<name>.o.prev`
automatically. If preflight did not run (no `.o.prev`), proceed with
absolute timing only — no % diff.

## Step 2: diff-elfs — find modified/added functions

Read `asm-analyze command:`, `venv python:`, and `plugin dir:` from the LOCI session context (system-reminder at session start). Use these as `<asm-analyze-cmd>`, `<venv-python>`, and `<plugin-dir>` in the commands below.

```
<asm-analyze-cmd> diff-elfs --elf-path <pre.o> --comparing-elf-path <post.o> --arch <loci_target>
```

This returns lists of `modified` and `added` functions. Only these functions
need analysis — skip unchanged code entirely.

If there is no pre-edit artifact, treat all functions in the post-edit artifact
as "added".

## Step 3: extract-assembly (pre + post)

For **modified** functions, extract assembly from both artifacts:

```
<asm-analyze-cmd> extract-assembly --elf-path <pre.o> --functions <func1>,<func2> --arch <loci_target>
<asm-analyze-cmd> extract-assembly --elf-path <post.o> --functions <func1>,<func2> --arch <loci_target>
```

For **added** functions, extract from post-edit only:

```
<asm-analyze-cmd> extract-assembly --elf-path <post.o> --functions <new_func> --arch <loci_target>
```

The JSON output contains `timing_csv` and `timing_architecture` fields needed
for the MCP call.
The JSON also contains the `control_flow_graph` field that contains annotated CFG's in text-format optimized for LLM analysis.

the calls for extracting fields from the json output:

  data = json.load(...)
  cfg_text = data["control_flow_graph"]    # all functions, annotated CFG blocks
  timing_csv_chunks = data["timing_csv_chunks"]  # list of per-block CSV chunks for MCP
  timing_architecture = data["timing_architecture"]    # timing architecture

## Step 4: LOCI MCP timing — compute % diff

Call `mcp__loci__get_assembly_block_exec_behavior` for **all chunks in
parallel** (one call per chunk, all in the same response):
- `csv_text`: the chunk
- `architecture`: the `timing_architecture` value from step 3

IMPORTANT: Issue all chunk calls simultaneously in a single message — do NOT
call them sequentially. Concatenate the result CSVs (skip duplicate headers)
before computing metrics.

Do this for both pre-edit and post-edit assembly of modified functions, and
for post-edit only of added functions.

From the MCP response and also using the annotated CFG's from step 3, compute:
- **Happy path** = `execution_time_ns` - `std_dev`
- **Worst path** = `execution_time_ns` + `std_dev`
- **Energy** = `energy_ws` (report in uWs)

For modified functions, compute % diff:
```
diff_pct = ((post_value - pre_value) / pre_value) * 100
```

### Graceful degradation

- **LOCI MCP unavailable** — report CFG analysis only, note "(timing unavailable — MCP not connected)"
- **No pre-edit artifact** — report absolute timing only, no % diff

## Step 5: Emit report

### Modified functions

```
## Post-Edit: <FunctionName>

### Execution (<loci_target>)
                  Before          After           Diff
Happy path:   XXX.XX ns       XXX.XX ns       +X.X% | -X.X%
Worst path:   XXX.XX ns       XXX.XX ns       +X.X% | -X.X%
Energy:       XXX.XX uWs      XXX.XX uWs      +X.X% | -X.X%

### Control Flow
<brief CFG analysis from step 4>

### Reasoning
<implementation verification — see below>
```

### New/added functions

```
## Post-Edit: <FunctionName> (NEW)

### Execution (<loci_target>)
Happy path:   XXX.XX ns
Worst path:   XXX.XX ns
Energy:       XXX.XX uWs

### Control Flow
<CFG analysis from step 4>

### Reasoning
<implementation verification — see below>
```

### No pre-edit artifact (absolute only)

```
## Post-Edit: <FunctionName>

### Execution (<loci_target>)
Happy path:   XXX.XX ns
Worst path:   XXX.XX ns
Energy:       XXX.XX uWs
(no pre-edit artifact — showing absolute values only)

### Control Flow
<CFG analysis>

### Reasoning
<implementation verification — see below>
```

### Reasoning section guidelines

The **Reasoning** section verifies whether the implementation is sound based
on the LOCI timing, energy, and CFG data above. Address each of these:

1. **Timing impact** — Is the timing diff expected given the code change?
   Flag unexpected regressions (e.g. a "simple guard" that adds >10% worst
   path). Note when the change is timing-neutral or improves performance.
2. **Hotspot check** — Using the CFG and per-block timing, identify the
   hottest block(s). Does the new/changed code sit on the hot path? If yes,
   call it out.
3. **Std-dev confidence** — High `std_dev` means the assembly pattern is
   underrepresented in LCLM training data. Flag any block where
   `std_dev > execution_time_ns` as low-confidence.
4. **Energy budget** — Is the energy delta acceptable for the target? For
   battery-powered / embedded targets, flag increases above 5%.
5. **Verdict** — One line: does the implementation look correct from an
   execution perspective? Use: OK, CAUTION (with reason), or FLAG (with
   specific concern).

### Action on CAUTION or FLAG

When the verdict is **CAUTION** or **FLAG**, do not just report — act on it:

1. **Propose a fix** — based on the LOCI timing, energy, and CFG data, describe
   a specific code change that would resolve the concern (e.g., cache a result,
   use a lighter callee, move work off the hot path, flatten the call chain).
2. **Ask the user** — present the concern and proposed fix, and ask whether to
   apply the rewrite. Do not silently proceed or ignore the finding.

Example:
```
Verdict: FLAG — worst path regressed +42% due to new snprintf call on hot path.
Proposed fix: replace snprintf with a bounded itoa + memcpy (saves ~180 ns worst case).
Apply this rewrite? [user decides]
```

## LOCI voice remark

Before the footer, add one short LOCI voice remark (max 15 words) that
acknowledges the user's work grounded in a specific number from the
analysis. Attribute improvements to the user ("clean work", "smart move",
"tight code"). For concerns, be honest and constructive with specifics.
Skip if the analysis produced no results or the user needs raw data only.

## LOCI footer

After emitting all per-function reports, append this footer once as the very
last thing printed — **only if N > 0**. If no functions were processed, do NOT emit the footer.

**Record cumulative stats** (run via Bash before rendering the footer):
```
<venv-python> <plugin-dir>/lib/loci_stats.py record --skill post-edit --functions <N> --mcp-calls <M> --co-reasoning <R>
```

**Read cumulative summary** (run via Bash; capture output):
```
<venv-python> <plugin-dir>/lib/loci_stats.py summary
```

Render the footer — include the summary line only if the command produced output:
```
─── LOCI · post-edit ───────────────────
  <N> functions · <M> MCP calls · <R> co-reasoning
  Verdict: <OK | CAUTION | FLAG> — <one-line summary>
    <cumulative-summary-output>        ← omit if empty
────────────────────────────────────────
```

- **N** = unique functions (modified + added) whose assembly was sent to LOCI
- **M** = MCP calls to `mcp__loci__get_assembly_block_exec_behavior` (exec-behaviors)
  (typically 2 for modified functions: pre + post; 1 for added functions)
- **R** = co-reasoning (one per function that has a Reasoning section)
