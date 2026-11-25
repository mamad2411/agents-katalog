---
name: lua-scripting
description: "Write safe Lua for embedding and automation: tables and metatables, module layout, sandboxing untrusted chunks, and performance-conscious loops."
type: procedural
category: programming
domain: programming
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - lua metatable usage
  - lua sandbox untrusted code
  - neovim lua config
  - lua performance loop
  - lua module layout
keywords:
  - lua
  - metatable
  - sandbox
  - neovim
  - embedding
  - luajit
source: custom
enabled: true
---

# Lua Scripting

## Purpose

Write safe Lua for embedding and automation: tables and metatables, module layout, sandboxing untrusted chunks, and performance-conscious loops.

## When to Use

- You are writing Lua embedded in a host application (Neovim, Redis, nginx, a game engine).
- Untrusted Lua must run with restricted globals and a bounded environment.
- A Lua hot path allocates too much or uses the wrong table structure.

## When NOT to Use

- The task is a general-purpose application better served by a language with stronger tooling.
- You need typed data contracts across service boundaries.
- The host API is unknown; ask for the embedding documentation first.

## Capabilities

- Use tables and metatables for object-like structure without excess ceremony.
- Sandbox chunks with a restricted `_ENV` and no `os`/`io` access.
- Structure modules for `require` without leaking globals.
- Reduce allocations in loops and pick appropriate table shapes.

## Inputs

- The host runtime (Lua 5.1/5.4, LuaJIT) since semantics differ.
- The API surface the host exposes to scripts.
- The trust boundary: who authors the script.

## Workflow

1. Identify the Lua version and the host-provided API before writing code.
2. Keep state in locals or a table; declare no new globals.
3. For untrusted code, build a restricted environment table and pass it as `_ENV`.
4. Measure the hot loop with the host's profiler or `os.clock` deltas.
5. Add a test that asserts the sandbox denies file and process access.

## Tools

- lua / luajit
- busted (unit tests)
- the host's own script console

## Examples

- `lua -e 'print(_VERSION)'`
- `luacheck .`
- `busted spec/`

## Safety

- Never `loadstring`/`load` untrusted input with the default global environment.
- 1-based indices and `#` on sparse tables are common bug sources; keep tables dense.
- Redis Lua scripts block the server; keep them short and deterministic.

## Source

All-Skills canonical library (`skills/programming/lua-scripting`). First-party skill, maintained in this repository.

## Notes

- Metatables are the idiomatic mechanism for inheritance and operator behaviour.
- `local` everything hot: global lookups go through `_ENV`.
- Pairs with: `programming/bash-scripting`, `development/debugging`.
