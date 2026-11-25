---
name: elixir-otp
description: "Design Elixir and OTP systems: supervision trees, GenServer state ownership, Phoenix channels, Task concurrency and fault-tolerant releases."
type: procedural
category: programming
domain: programming
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - elixir supervision tree
  - genserver design
  - phoenix channel scaling
  - otp fault tolerance
  - elixir release deploy
keywords:
  - elixir
  - otp
  - genserver
  - phoenix
  - supervisor
  - beam
source: custom
enabled: true
---

# Elixir and OTP

## Purpose

Design Elixir and OTP systems: supervision trees, GenServer state ownership, Phoenix channels, Task concurrency and fault-tolerant releases.

## When to Use

- You are designing a concurrent Elixir component and need to decide process ownership.
- A crash cascade or stuck GenServer needs supervision and backpressure analysis.
- A release must be built, configured at runtime and rolled out safely.

## When NOT to Use

- The task is plain Erlang with no Elixir tooling; idioms differ.
- You only need Phoenix templates or LiveView markup changes with no process design.
- The system is a short-lived script where OTP structure adds cost without benefit.

## Capabilities

- Choose between GenServer, Agent, Task and plain function calls with justification.
- Design supervision strategies that isolate failure instead of restarting the world.
- Add backpressure and timeouts so queues cannot grow without bound.
- Build and configure OTP releases with runtime configuration.

## Inputs

- The runtime version (Elixir/OTP) and the deployment target (release, container, bare VM).
- The failure mode observed: crash logs, mailbox growth, timeouts.
- Expected concurrency and message volume.

## Workflow

1. Model the state ownership: which process owns which data, and who may mutate it.
2. Pick the smallest primitive that satisfies it; prefer functions and `Task` over long-lived servers.
3. Place the process under a supervisor with a restart strategy that matches its dependencies.
4. Add timeouts, `handle_continue` for slow init and telemetry for queue length.
5. Verify by killing the process in a test (`Process.exit/2`) and asserting recovery.

## Tools

- mix
- iex / Observer
- ExUnit
- :telemetry

## Examples

- `mix test --only integration`
- `iex> :observer.start()`
- `MIX_ENV=prod mix release`

## Safety

- Unbounded mailboxes and unbounded `Task.async_stream` concurrency will exhaust the VM.
- Never call a remote node synchronously without a timeout.
- Runtime configuration secrets belong in `config/runtime.exs`, not compile-time config.

## Source

All-Skills canonical library (`skills/programming/elixir-otp`). First-party skill, maintained in this repository.

## Notes

- Let it crash works only when the supervisor's restart strategy is intentional.
- `handle_continue` keeps a GenServer responsive while doing slow setup.
- Pairs with: `programming/go-concurrency`, `devops/containers`.
