---
name: runlua
description: Required operating guide for the runlua and runlua_session tools. Before either tool is used, load this guide with the native skill tool using name runlua; never use luaskill to retrieve it.
---

# RunLua

Before calling `runlua` or `runlua_session`, load this guide through the native prompt-Skill tool:

```json
{"name":"runlua"}
```

The tool id is `skill`, singular. It reads prompt Skills. Do not call `luaskill`, a LuaSkills entry, or LuaSkills help to retrieve this guide.

## When to Use It

- Use `runlua` for one calculation or data transformation that a short script does better than several tool calls: counting, filtering, reshaping files, comparing data.
- Use `runlua_session` only when values must survive across several evaluations.
- Use `shell_command` for ordinary commands and the file tools for reading or editing individual files.
- Lua cannot call your other tools. MCP tools, `shell_command`, `read_media`, and every other tool in this conversation are not reachable from Lua; call them directly.

## Your First Call

```json
{
  "task": "Sum values",
  "code": "local total = 0\nfor _, v in ipairs(args.values) do total = total + v end\nprint('count', #args.values)\nreturn total, { average = total / #args.values }",
  "args": {"values": [2, 4, 6]}
}
```

- `task` is a short label for the conversation card; `code` is inline Lua source.
- `args` is optional JSON; your code reads it as the local `args`.
- `timeout_ms` is optional, from 1 to 60000; default 60000.

The result is Markdown:

````text
# Runtime Execution Result

## Task
Sum values

## Status
SUCCESS

## Printed Output
```text
count	3
```

## Returned Values
1. 
```json
12
```

2. 
```json
{
  "average": 4
}
```
````

Reading the result:

- Check `## Status` first. `FAILED` with an `## Error` section means your Lua failed, even though the tool call itself completed. Printed output before the failure is still shown.
- Error locations point at your own code: `runlua:3:` is line 3 of `code`, and `runtime_session:3:` is line 3 of a session `eval`.
- Each returned value is listed separately. Strings appear as text; numbers, booleans, and tables appear as JSON. No `return` shows `null`.
- Return tables instead of printing them: `print` shows a table only as an opaque reference.
- An empty table returns as `[]`. Use `vulcan.json.object()` when an empty object is meant.

## Lua Dialect

The runtime is LuaJIT: Lua 5.1 with Lua 5.2 compatibility.

- Available: `table.unpack`, `goto`, `load`, `string.format`, `pcall`, the `bit` library.
- Not available: the `//` operator, the `utf8` library, and other Lua 5.3/5.4 features. Use `math.floor(a / b)` for integer division.
- Arrays start at 1. `#` is unreliable on tables with holes. Not-equal is `~=`; concatenation is `..`.
- String patterns are Lua patterns, not regular expressions. For a literal search use `s:find(text, 1, true)`.

## Common Tasks

Relative paths resolve from the current workspace.

Files:

```lua
local names = vulcan.fs.list("data")        -- entry names only, not full paths
local text = vulcan.fs.read("data/a.txt")   -- whole file as UTF-8 text
for line in text:gmatch("[^\n]+") do --[[ ... ]] end
vulcan.fs.mkdir("out", { recursive = true })
vulcan.fs.write("out/result.txt", text)     -- overwrites; parent must exist
return vulcan.fs.stat("data/a.txt")          -- nil when missing; size, kind, modified_unix_ms
```

Also available: `vulcan.fs.exists`, `is_dir`, `copy`, `rename`, `remove`, and `read_bytes` / `write_bytes` for non-UTF-8 content as Base64. `vulcan.path.join`, `dirname`, `basename`, `stem`, `extname`, and `normalize` build paths. Standard `io.open` also works.

JSON:

```lua
local data = vulcan.json.decode(vulcan.fs.read("data/config.json"))
data.count = #data.items
vulcan.fs.write("out/config.json", vulcan.json.encode(data))
```

`vulcan.json.object()`, `vulcan.json.array()`, and `vulcan.json.null` keep empty containers and nulls exact.

Processes:

```lua
local r = vulcan.process.exec({
  program = "git",
  args = { "status", "--short" },
  timeout_ms = 10000,
})
return { ok = r.ok, code = r.code, stdout = r.stdout, stderr = r.stderr }
```

The result also has `success`, `timed_out`, and `error`. A string such as `vulcan.process.exec("git status")` runs through the default shell, which is `cmd` on Windows; `vulcan.process.launchers()` lists the shells. Always pass `timeout_ms`.

Additional Lua or native modules are installation-dependent. Probe before relying on one:

```lua
local ok, module_or_error = pcall(require, "module_name")
return { available = ok, detail = tostring(module_or_error) }
```

## Not Available in RunLua

- Other tools of this conversation (see above).
- Databases: RunLua has no database binding. A registered LuaSkills entry that owns a database is called through `vulcan.call`.
- `vulcan.runtime.log`, persistent `vulcan.cache`, file-mode execution, and nested RunLua calls.

## Timeouts and Limits

- `timeout_ms` stops runaway Lua: the run ends with `FAILED` and a timeout error. Keep loops bounded anyway; a timed-out run returns no values.
- Give `vulcan.process.exec`, Python, and Node calls their own `timeout_ms`; the Lua timeout cannot interrupt them.
- Lua source is limited to 128 KiB per call.
- Tool output is limited to 64 KiB inline. Larger output is written to a project `.vulcan/temp/` page file with bounded read instructions; return a summary instead of large raw data.
- There is no Lua memory quota. Avoid unbounded tables, recursion, and generated source.
- FFI, `os`, and `io` are full host capabilities. Touch only the paths the task needs.

## Persistent `runlua_session`

Start a session, evaluate code in it, and close it when finished:

```json
{"action": "start", "name": "csv-analysis", "ttl_sec": 600}
```

```json
{
  "action": "eval",
  "session_id": "opaque id returned by start",
  "code": "counter = (counter or 0) + args.increment\nreturn { counter = counter }",
  "args": {"increment": 1}
}
```

```json
{"action": "close", "session_id": "opaque id"}
```

- `list` shows this conversation's sessions; `status` reports one.
- Globals and `package.loaded` survive successful evaluations; use globals, not `local`, for values you need later.
- `eval` returns one JSON-compatible value through `return`. `print` output is not captured in sessions.
- Functions, threads, userdata, and cyclic tables cannot be returned.
- Default idle TTL is 600 seconds, maximum 3600. Each successful eval refreshes it.
- At most four sessions may be open in one conversation. A LuaSkills runtime reload invalidates all sessions.

## Runtime Versions

- LuaSkills: `0.9.1`.
- mlua: `0.12.0`.
- LuaJIT: `LuaJIT 2.1.ROLLING`.
- LuaJIT source: `luajit-src 210.7.2+b925b3e`.

## Before Finishing

1. Return results in a bounded form.
2. Close sessions you no longer need, unless the user wants to continue later.
3. Confirm `## Status` is `SUCCESS` before reporting that a script worked.
