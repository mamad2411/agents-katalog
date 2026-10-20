---
name: elixir-genserver-basics
description: >
  Elixir GenServer patterns for owned services: callbacks, state, call/cast/info,
  supervision, timeouts, and testing with start_supervised. Use when implementing
  or reviewing GenServer, Agent alternatives, process mailboxes, or OTP process
  design in Elixir/Phoenix apps—not a full Phoenix security audit.
---

# Elixir GenServer Basics

## Scope And Authorization

- **In scope:** Elixir/OTP codebases you own or are authorized to modify.
- **Out of scope:** Attaching to production BEAM nodes without change control / break-glass process.
- GenServers hold state—avoid storing secrets in process state that gets logged on crash.
- Prefer non-prod for experiments with `Observer` and remote shells.
- Pair with `code-quality-standards` and `erlang-otp-release-handling` for releases.

## When To Use

- Introducing a process to own serializable state or serialize side effects.
- Choosing `GenServer.call` vs `cast` vs plain functions under a supervisor.
- Fixing timeouts, backlog, or “process mailbox growing” issues.
- Writing ExUnit tests that start servers under supervision.
- Deciding GenServer vs `Agent` vs `Task` vs `Phoenix.Channel` / `Registry`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| OTP releases / hot upgrade | `erlang-otp-release-handling` |
| Phoenix auth/CSRF/plugs | Phoenix/security skills; Sobelow workflows |
| Distributed Erlang security | clustering/security hardening skills |
| Implementation quality baseline | `code-quality-standards` |
| Pure functional core without processes | module design only—no GenServer |

## Domain Focus

| Area | Guidance |
| --- | --- |
| State | Minimal; recover from ETS/DB if process dies |
| call | Sync, must return promptly; use for queries/commands needing ack |
| cast | Async fire-and-forget; can hide backpressure |
| info | Messages from timers, ports, other processes |
| Supervision | `Restart` strategy intentional; id in child_spec |
| Atoms | Never `String.to_atom/1` on user input in callbacks |

## Workflow

### 1. Confirm scope and success criteria

1. What state is owned; single process vs pool; crash tolerance.
2. Success: clear API module, supervised start, tests green, no unbounded mailbox under expected load.

### 2. Inventory existing processes

```bash
mix xref graph --format stats 2>/dev/null | head
rg -n "use GenServer|GenServer\\.start" lib test
```

1. Map supervisors in `application.ex` / feature supervisors.
2. Note global names (`name: __MODULE__`) and clash risks.

### 3. Baseline behavior

1. Define public API functions that hide `GenServer.call` details.
2. List failure modes: timeout, badstate, dependency down.
3. Measure message rate expectations (casts/sec).

### 4. Implement a minimal GenServer

```elixir
defmodule MyApp.Counter do
  use GenServer

  # Client API
  def start_link(opts \\ []) do
    name = Keyword.get(opts, :name, __MODULE__)
    GenServer.start_link(__MODULE__, 0, name: name)
  end

  def incr(server \\ __MODULE__), do: GenServer.call(server, :incr)
  def value(server \\ __MODULE__), do: GenServer.call(server, :value)

  # Server callbacks
  @impl true
  def init(initial), do: {:ok, initial}

  @impl true
  def handle_call(:incr, _from, state), do: {:reply, state + 1, state + 1}

  @impl true
  def handle_call(:value, _from, state), do: {:reply, state, state}
end
```

```elixir
# supervision tree
children = [
  MyApp.Counter
]
```

1. Keep callbacks small; push domain logic to pure modules.
2. Use `handle_continue/2` for post-init work that must not block `init` too long.
3. For external IO, consider timeouts and `Task` under supervision rather than blocking `call` forever.

### 5. Timeouts, backpressure, and traps

```elixir
# Client with explicit timeout
GenServer.call(server, :slow_op, 5_000)

# Server: defer heavy work
def handle_cast({:work, job}, state) do
  # enqueue or spawn Task — do not block for minutes
  {:noreply, enqueue(state, job)}
end
```

1. Avoid `cast` storms without metrics on mailbox length.
2. `Process.flag(:trap_exit, true)` only when you intentionally handle exits.
3. Do not use GenServer as a global God-object for the whole app.

### 6. Verify with evidence

```bash
mix test
mix format --check-formatted
# Interactive lab:
# iex -S mix
# MyApp.Counter.incr()
```

```elixir
# test/counter_test.exs
defmodule MyApp.CounterTest do
  use ExUnit.Case, async: true

  test "increments", %{test: test_name} do
    start_supervised!({MyApp.Counter, name: test_name})
    assert MyApp.Counter.incr(test_name) == 1
    assert MyApp.Counter.value(test_name) == 1
  end
end
```

1. Assert crash restart behavior under supervisor when relevant.
2. Property or concurrency tests if state races are possible (usually serialize via the server).

### 7. Hand off

1. Document process name, restart strategy, and durable state location.
2. Telemetry: call duration, mailbox length, restarts.
3. Apply `code-quality-standards`; avoid logging full state structs with PII.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| API | Module functions wrapping call/cast | Callers know raw message tags only |
| Work | Short handle_* ; async heavy IO | 30s HTTP inside `handle_call` |
| Names | Via/Registry for many instances | Single global for multi-tenant state |
| Atoms | Fixed message atoms | `String.to_atom(user_id)` |
| Tests | `start_supervised!` | Orphan processes across tests |

## Output Checklist

- [ ] State ownership and restart strategy documented
- [ ] Client API hides GenServer details
- [ ] call vs cast choices justified
- [ ] Supervised child_spec registered
- [ ] Tests use start_supervised / unique names
- [ ] Timeout and mailbox risks reviewed
- [ ] No user-driven atom creation
- [ ] Telemetry/logging redaction considered

## Rules

- Owned code and authorized prod debugging only.
- GenServer is serialization + lifecycle—not a substitute for a database.
- Prefer pure functions for domain logic.
- Never store long-lived secrets only in volatile process memory without recovery plan.
- Releases/hot upgrade → `erlang-otp-release-handling`.
