---
name: lang-lua
description: Lua 5.4/LuaJIT scope discipline, strict global variable protection, sandboxed execution, and explicit module exports.
---

# Lua Scope Protection & Sandboxing Contract

## 1. Scope Discipline
- All variable declarations must be explicitly `local`. Accidental global variable assignments fail quality gates.
- Metatable manipulation (`setmetatable`) must be strictly encapsulated within module definitions.

## 2. Sandboxing
- Untrusted user scripts must execute inside a restricted environment with stripped dangerous globals (`os`, `io`, `debug`, `package`).
