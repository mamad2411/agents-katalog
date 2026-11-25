---
name: r-lib-mirai
license: CC-BY-4.0
description: >-
  Write and fix async, parallel, and distributed R code with the mirai
  package: mirai(), daemons(), mirai_map(), everywhere(), explicit dependency
  passing, error values, Shiny ExtendedTask and promises, remote/HPC daemons,
  and migration from future, furrr, or parallel. Use for parallelising R
  loops or lapply/purrr maps across worker processes.
compatibility: >-
  Requires R and the mirai package. Examples verified with mirai 2.7.2
  (nanonext 1.10.3), shiny 1.14.0, bslib 0.12.0, and promises 1.5.0 on
  R 4.5.3, 2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# mirai: async and parallel R

mirai evaluates R expressions in separate processes (daemons). When the user
gives code, fix it or convert it to correct mirai code; when they describe a
task, write the code. Verify against https://mirai.r-lib.org when an installed
mirai is older or newer than 2.7.2 or an API detail matters; say so if you
cannot check.

## Choose a reference

| Read | When you need |
|---|---|
| [references/shiny-promises.rst](references/shiny-promises.rst) | A complete Shiny `ExtendedTask` app, `input_task_button()`, or promise piping with `%...>%`/`then()` |
| [references/remote-hpc.rst](references/remote-hpc.rst) | Daemons on other machines: SSH (direct or tunnelled), Slurm/SGE/PBS/LSF, or an HTTP launcher such as Posit Workbench |
| [references/migration.rst](references/migration.rst) | Converting from future, furrr, or parallel, or a drop-in `parallel` cluster (`make_cluster()`, `makeCluster(type = "MIRAI")`) |
| [references/advanced.rst](references/advanced.rst) | Switching compute profiles with `local_daemons()`/`with_daemons()`, or nested parallelism inside daemons |

## Core Principle: Explicit Dependency Passing

mirai evaluates expressions in a **clean environment** on a daemon process. Nothing from the calling environment is available unless explicitly passed. This is the #1 source of mistakes.

There are two ways to pass objects:

### `.args` (recommended for most cases)

Objects in `.args` are placed in the **local evaluation environment** of the expression. They are available directly by name inside the expression.

```r
my_data <- data.frame(x = 1:10)
my_func <- function(df) sum(df$x)

m <- mirai(my_func(my_data), .args = list(my_func = my_func, my_data = my_data))
```

**Shortcut** — pass the entire calling environment:

```r
process <- function(x, y) {
  mirai(x + y, .args = environment())
}
```

### `...` (dot-dot-dot)

Objects passed via `...` are assigned to the **daemon's global environment**. Use this when objects need to be found by R's standard scoping rules (e.g., helper functions that are called by other functions).

```r
m <- mirai(run(data), run = my_run_func, data = my_data)
```

**Shortcut** — pass the entire calling environment via `...`:

```r
df_matrix <- function(x, y) {
  mirai(as.matrix(rbind(x, y)), environment())
}
```

When `...` receives a single unnamed environment, all objects in that environment are assigned to the daemon's global environment.

### When to use which

| Scenario | Use |
|----------|-----|
| Data and simple functions | `.args` |
| Helper functions called by other functions that need lexical scoping | `...` |
| Passing the entire local scope to local eval env | `.args = environment()` |
| Passing the entire local scope to global env | `mirai(expr, environment())` via `...` |
| Large persistent objects shared across tasks | `everywhere()` first, then reference by name |

## Common Mistakes and Fixes

### Mistake 1: Not passing dependencies

```r
# WRONG: my_data and my_func are not available on the daemon
m <- mirai(my_func(my_data))

# CORRECT: Pass via .args
m <- mirai(my_func(my_data), .args = list(my_func = my_func, my_data = my_data))

# CORRECT: Or pass via ...
m <- mirai(my_func(my_data), my_func = my_func, my_data = my_data)
```

### Mistake 2: Using unqualified package functions

```r
# WRONG: dplyr is not loaded on the daemon
m <- mirai(filter(df, x > 5), .args = list(df = my_df))

# CORRECT: Use namespace-qualified calls
m <- mirai(dplyr::filter(df, x > 5), .args = list(df = my_df))

# CORRECT: Or load the package inside the expression
m <- mirai({
  library(dplyr)
  filter(df, x > 5)
}, .args = list(df = my_df))

# CORRECT: Or pre-load on all daemons with everywhere()
everywhere(library(dplyr))
m <- mirai(filter(df, x > 5), .args = list(df = my_df))
```

The same applies inside `mirai_map()` callbacks: write
`function(x) dplyr::filter(x, val > 0)`, or call `everywhere()` first.

### Mistake 3: Expecting results immediately

`m$data` accesses the mirai's value — but it may still be unresolved. Use `m[]` to block until done, or check with `unresolved(m)` first.

```r
m <- mirai(slow_computation())
result <- m$data                     # WRONG: may be an 'unresolvedValue'
result <- m[]                        # CORRECT: blocks, returns the value
call_mirai(m); result <- m$data      # CORRECT: wait, then read $data
if (!unresolved(m)) result <- m$data # CORRECT: non-blocking check
```

### Mistake 4: Mixing up .args names and expression names

```r
# WRONG: .args names don't match what the expression uses
m <- mirai(process(input), .args = list(fn = process, data = input))

# CORRECT: Names in .args must match names used in the expression
m <- mirai(process(input), .args = list(process = process, input = input))
```

## Setting Up Daemons

### No daemons required

`mirai()` works without calling `daemons()` first — it launches a transient background process per call. Setting up daemons is only needed for persistent pools of workers.

### Local daemons

```r
daemons(4)                      # 4 local daemons with dispatcher (default)
daemons(4, dispatcher = FALSE)  # direct: lower overhead, round-robin, no cancellation
info()                          # status
daemons(0)                      # daemons persist until reset
```

### Scoped daemons (auto-cleanup)

`with(daemons(...), {...})` **creates** daemons and automatically cleans them up when the block exits.

```r
with(daemons(4), {
  m <- mirai(expensive_task())
  m[]
})
```

To switch between existing profiles with `local_daemons()` or
`with_daemons()`, read [references/advanced.rst](references/advanced.rst).

### Compute profiles (multiple independent pools)

```r
daemons(4, .compute = "cpu")
daemons(2, .compute = "gpu")

m1 <- mirai(cpu_work(), .compute = "cpu")
m2 <- mirai(gpu_work(), .compute = "gpu")
```

## mirai_map: Parallel Map

Requires daemons; without them it errors with "No daemons set". Maps `.x`
element-wise over a function, distributing across daemons.

```r
daemons(4)

# Basic map — collect with []
results <- mirai_map(1:10, function(x) x^2)[]

# With constant arguments via .args
results <- mirai_map(
  1:10,
  function(x, power) x^power,
  .args = list(power = 3)
)[]

# With helper functions via ... (assigned to daemon global env)
results <- mirai_map(
  data_list,
  function(x) transform(x, helper),
  helper = my_helper_func
)[]

# Flatten results to a vector
results <- mirai_map(1:10, sqrt)[.flat]

# Progress bar (requires cli package)
results <- mirai_map(1:100, slow_task)[.progress]

# Early stopping on error
results <- mirai_map(1:100, risky_task)[.stop]

# Combine options
results <- mirai_map(1:100, task)[.stop, .progress]

# Data frame: each row becomes the function's arguments
params <- data.frame(mean = 1:5, sd = c(0.1, 0.5, 1, 2, 5))
results <- mirai_map(params, function(mean, sd) rnorm(100, mean, sd))[]
```

## everywhere: Pre-load State on All Daemons

```r
daemons(4)

# Load packages on all daemons
everywhere(library(DBI))

# Set up persistent connections
everywhere(con <<- dbConnect(RSQLite::SQLite(), db_path), db_path = tempfile())

# Export objects to daemon global environment via ...
# The empty {} expression is intentional — the point is to export objects via ...
everywhere({}, api_key = my_key, config = my_config)
```

## Error Handling

```r
m <- mirai(stop("something went wrong"))
m[]

is_mirai_error(m$data)       # TRUE only for errors raised by your code
is_mirai_interrupt(m$data)   # TRUE for a user interrupt on the daemon
is_error_value(m$data)       # TRUE for any error value, incl. timeout (5) and cancel (20)

m$data$message               # Error message
m$data$stack.trace           # Full stack trace
m$data$condition.class       # Original error classes

# Timeouts work with or without dispatcher: the mirai resolves to errorValue 5.
# Only with dispatcher is the task also cancelled; without it the daemon
# keeps running the task to completion.
m <- mirai(Sys.sleep(60), .timeout = 5000)  # 5-second timeout

# Cancellation requires dispatcher (stop_mirai() returns FALSE without it).
# A cancelled mirai resolves to errorValue 20, not a miraiInterrupt.
m <- mirai(long_running_task())
stop_mirai(m)
```

## Shiny and promises

A mirai is a promise, so it plugs into Shiny `ExtendedTask` and the promises
package directly. The essentials:

- Call `daemons(n)` once at start-up and `onStop(function() daemons(0))`.
- The `ExtendedTask` function takes plain values and passes them to `mirai()`
  through `.args`; reactive values cannot be read on the daemon.
- Every `input$...` the server reads must be defined in the UI; a missing
  input is `NULL` and the task fails (for example `rnorm(NULL)` gives
  "invalid arguments").

```r
task <- ExtendedTask$new(
  function(n) mirai(rnorm(n), .args = list(n = n))
) |> bind_task_button("run")
observeEvent(input$run, task$invoke(input$n))  # UI defines numericInput("n", ...)
```

For the complete app and promise piping, read
[references/shiny-promises.rst](references/shiny-promises.rst).

## Random number generation

```r
# Default: an L'Ecuyer-CMRG stream per daemon (statistically safe, not reproducible)
daemons(4)

# Reproducible: a stream per mirai call; results do not depend on daemon
# count or scheduling
daemons(4, seed = 42)
```

## Debugging

```r
# Synchronous mode runs in the host process and supports browser()
daemons(sync = TRUE)
m <- mirai({
  browser()
  tricky_function(x)
}, .args = list(tricky_function = tricky_function, x = my_x))
daemons(0)

# Show daemon stdout/stderr in the host
daemons(4, output = TRUE)
```
