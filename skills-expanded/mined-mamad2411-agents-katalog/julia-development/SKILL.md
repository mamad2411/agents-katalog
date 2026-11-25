---
name: julia-development
description: Julia package development on a warm REPL session, verifying each edit with Revise and TestItemRunner rather than at the end
---

# Julia package development

Work on a warm Julia session and verify each edit as you make it.
The cost of a fresh process is time-to-first-execution paid once per
session, so keep one alive and check every change against it.
An agent that verifies per step writes better Julia: genuinely
non-allocating where asked, and more likely to get the task right
first time.

## Warm session

Start one session and reuse it.
Under Claude Code the AgentREPL.jl plugin gives a warm MCP session
over STDIO, with no open port.
Its `eval` tool is synchronous, so a call returns when evaluation
finishes.
A PostToolUse hook nudges you to reload after editing a `.jl` file.

Point the session at the project with `activate`, then `instantiate`.
Redefining state or types Revise cannot reload means restarting the
worker with `reset`.

## Revise

Call the `revise` tool after editing a `.jl` file; session state is
kept.
Struct and type edits now reload on Julia 1.12+ with Revise 3.16+ and
`revise_structs = true`, but objects built before the edit keep the
old type, so a session holding such state is still stale.

Still needs a fresh worker:

- macro and generated-function changes
- a struct reached only through a type alias or global binding
- corrupted or polluted state; restart rather than debug it

## Testing with TestItemRunner

Write tests as `@testitem "name" begin ... end`.
Each item runs in a fresh module, so runs stay isolated even in a
shared session.

Run `using TestItemRunner` once, then filter to what you changed:

```julia
# by file
@run_package_tests filter=ti->contains(ti.filename, "foo.jl")
# by name
@run_package_tests filter=ti->contains(ti.name, "edge")
# by tag
@run_package_tests filter=ti->!(:slow in ti.tags)
```

Run the narrowest filter that covers the change while iterating.
Run the full suite on a fresh session before finishing.

## Hot versus cold

Run most work on the warm session.
Fall back to a fresh process for:

- final verification before commit
- precompilation, load-time, or TTFX work
- struct, type, or const redefinitions Revise cannot reload
- stale state

## Dependencies

Use `Pkg.update()` rather than editing `Project.toml` by hand.
You can `Pkg.add` then `using` in a live session, but restart the
worker afterwards if the new package changes what is already loaded.

## Formatting and quality

Format with JuliaFormatter, usually through a pre-commit hook.
Keep Aqua.jl tests in `test/` for package-quality checks.
Follow the project style: 80-character lines, no trailing
whitespace, type-stable code.
Check type stability with `@code_warntype` and watch for `Any`.

## Docstrings

Use DocStringExtensions templates, and mind template expansion:

- `@doc "..."` (regular string) lets templates expand
- `@doc raw"..."` does not expand templates; use only without them
- for templates with LaTeX, use `@doc """..."""` and escape
  backslashes (`\\int`, not `\int`)

```julia
@doc "
$(TYPEDSIGNATURES)

Brief description.

# Fields
$(TYPEDFIELDS)
"
struct MyType
    "Field description"
    field::Int
end
```

Keep interface docstrings to a line or two and cross-reference
related methods with a ``See also: [`other`](@ref)`` line rather than
repeating content.

## When to use this skill

Use it when developing, testing, documenting, or profiling Julia
packages.
Project-specific architecture and domain knowledge belong in the
project `CLAUDE.md`, not here.
