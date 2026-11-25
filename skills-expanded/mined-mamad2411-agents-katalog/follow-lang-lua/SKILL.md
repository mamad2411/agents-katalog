---
name: follow-lang-lua
description: Lua guidelines with best practices for embedded scripting and lightweight automation
argument-hint: "[scope|setup-project|create-module]"
related:
  - follow-lang-javascript
  - follow-best-practice
  - setup-cicd
  - use-scripts
  - deep-research

---

## Goal

Develop Lua per best practices for embedded scripting and lightweight automation

## Scope

For all Lua work: game development, embedded systems, scripting within applications (Neovim, OpenResty, Roblox), rapid prototyping, config files, lightweight automation. Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/` — dispatch: `setup-project` → `workflows/setup-project/SKILL.md`, `create-module` → `workflows/create-module/SKILL.md`; verify the interpreter/dialect (PUC Lua, LuaJIT, Luau) and library availability via `/deep-research` at use time (official docs: https://www.lua.org/manual/)

## Execute

### 1. Check Dialect And Setup Environment

> Goal: install the right interpreter and tooling for the host context

1. Identify the dialect the host expects (PUC Lua 5.4, LuaJIT, Luau, or an embedded host like Neovim/OpenResty) and its version — run `/deep-research` + `/follow-best-practice` when unsure to live-check current versions and practices; language features differ between them
2. Install the interpreter (`mise use -g lua` or the host's bundled runtime) and the `LuaRocks` package manager; verify `lua -v` / `luajit -v` / `luarocks --version`
3. Manage packages: `luarocks install|remove|search|show|list|update <pkg>`
4. Set module search paths via `LUA_PATH`/`LUA_CPATH` (env) or `package.path`/`package.cpath` (runtime) when modules live outside defaults
5. Configure LuaLS (lua-language-server) with `Lua.runtime.version` matching the dialect; add host globals (`vim`, `love`, `ngx`) to `Lua.diagnostics.globals`

### 2. Understand Core Concepts

> Goal: build on Lua's actual model

1. Tables are the only data structure — arrays, objects, and modules are all table usage patterns
2. Metatables add behavior (`__index` inheritance, `__call`, `__tostring`, operator overloading)
3. Coroutines give cooperative multitasking (`create`/`resume`/`yield`, status handling)
4. Know the host VM limits: LuaJIT is 5.1-based (no integer/float split, `goto`, FFI); global environment is the main shared state

### 3. Use Data Structures And Async

> Goal: use tables, metatables, and coroutines correctly

1. Prefer array-part or hash-part usage consistently per table; avoid `nil`-holes from sparse indices
2. Metatables: `__index` for inheritance, `__newindex` for proxies, `__tostring` for representation; share one metatable per "class"
3. Coroutines for cooperative flows and generators; handle `resume` errors via the returned status, never swallow

### 4. Organize And Handle Errors

> Goal: structure code with modules and handle errors properly

1. Modules: return a table from `require`; keep functions `local` (faster, avoids global pollution)
2. Errors: `error()` with a clear message or table-based custom error types; catch with `pcall`, add context with `xpcall` + a traceback handler
3. At embed boundaries, convert host errors to Lua errors and vice versa explicitly — never let a silent `pcall` discard a failure

### 5. Create Modules And Project Layout

> Goal: standard module shape and project structure

1. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`); add a module → run the workflow `workflows/create-module/SKILL.md` (argument `create-module`)
2. Module pattern: `local M = {}` — public `function M.func()`, private `local function` — then `return M`; snake_case file/function names, UPPER constants, PascalCase class/metatable tables
3. Document every public function in LDoc form (`---` description, `-- @param`, `-- @return`)
4. Error convention at API boundaries: return `nil, err` or `error(msg, 2)` — pick one per module and stay consistent

### 6. Test, Debug, And Optimize

> Goal: verify correctness and tune performance

1. Unit tests with `busted` (`luarocks install busted`); coverage with `luacov`; static analysis with `luacheck` in CI
2. Debug with the LuaLS debugger or ZeroBrane; inspect with `print`/`tostring` early, structured logging later
3. Hot paths: minimize table allocations (reuse tables, string buffers), keep locals, avoid `__index` lookups in loops; for LuaJIT, check traces with `luajit -jv`, dump IR with `-jdump`
4. Watch GC pressure in long-running hosts; tune with `collectgarbage("setpause"/"setstepmul")` only with measurements

## Rules

### 1. Code Style

- `local` always over implicit globals; meaningful names; consistent indentation (2 spaces is common); comments only where intent isn't obvious; never leak globals (a `luacheck` gate enforces this)

### 2. Data Structures

- Tables for arrays/objects/modules; metatables for OOP and operator overloading; `__index` inheritance, `__call` callable objects, `__tostring` representation

### 3. Coroutines

- `coroutine.create`/`resume`/`yield` for cooperative multitasking; check status and resume results; prefer `coroutine.wrap` when you want errors propagated

### 4. Error Handling

- `pcall`/`xpcall` at boundaries; `error()` with messages or custom error tables; log with context; never silently ignore a failed `pcall`

### 5. Dialect Discipline

- Never assume 5.4 semantics on LuaJIT or vice versa; check feature availability for the target dialect via `/deep-research` before using integer division, bitwise ops, `goto`, or FFI

- Use /follow-lang-javascript if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed

## Expected Outcome

- Standard, maintainable Lua code with correct table/metatable usage
- Efficient cooperative flows with coroutines
- Lightweight, fast code tuned for the target VM
- Proper error handling and clear messages
- Tested (busted), checked (luacheck), and debugged before delivery
