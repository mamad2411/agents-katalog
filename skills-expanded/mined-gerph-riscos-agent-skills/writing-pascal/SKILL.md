---
name: writing-pascal
description: Use when writing, reading, updating, building, or reviewing Pascal code in the RISC OS build environment, especially when compiling with riscos-p2cc/riscos64-p2cc, creating a pcommand project with riscos-project, or building for 32-bit and 64-bit RISC OS.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-project:*) Bash(riscos-amu:*) Bash(riscos-build-run:*) Bash(riscos-p2cc:*) Bash(riscos64-p2cc:*)
---

# Writing Pascal for RISC OS

Use this skill for Pascal work in the RISC OS build environment.

Read only the reference files needed for the task:

* Build, source layout, and command lines (32-bit and 64-bit, direct and
  project builds): `references/building.md`
* Common pitfalls, language quirks, and review checks: `references/pitfalls.md`

## Core Rules

Pascal source is translated to ANSI C by the P2C translator, then compiled
and linked with the normal C toolchain. `riscos-p2cc` (32-bit and 26-bit) and
`riscos64-p2cc` (64-bit) drive translation, compilation, and linking
together.

Pascal source files live in `p/`. Unlike the C, C++, and Fortran wrappers,
`riscos-p2cc` takes the host path directly, so pass `p/hello`, not `p.hello`
or `hello.p`.

Always pass `-26`, `-32`, or `-64` explicitly. Without one, `riscos-p2cc`
defaults to 26-bit code, which fails at run time with
`26 bit absolute files are not executable on this system` on a 32-bit or
64-bit system.

The `o/` directory must exist before compiling with a 32-bit target, even
for a combined translate-compile-link command; the 32-bit compiler writes an
intermediate object there. The 64-bit compiler does not need this.

**Do not print a `real` value with `write`/`writeln` in a 32-bit build.**
This currently produces incorrect output (`0.0`, or garbage for an
unformatted `writeln`) due to a variadic-double calling-convention bug in
the 32-bit toolchain. `real` arithmetic and comparisons are unaffected, and
64-bit builds print `real` values correctly. If a 32-bit program must show a
computed value, convert with `trunc`/`round` to an integer, or target 64-bit.

To create a project: `riscos-project create --type pcommand --name <name>
--skeleton`, then `riscos-amu` for 32-bit or `riscos-amu BUILD64=1` for
64-bit.

Assignment is `:=`, comparison is `=`. Boolean operators are the words
`and`, `or`, `not`. Array bounds are declared explicitly (eg
`array[1..3] of integer`), not fixed at a language-defined start index.
