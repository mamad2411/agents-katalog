---
name: cpp-build-systems
description: Use in C/C++ projects for build configure/errors, compile_commands.json generation, or selecting CMake/Meson/Make/Bazel commands.
---

# C/C++ Build Systems

The build system is the single most important piece of C/C++ tooling — it determines how every other tool (clang-tidy, IWYU, language servers, debuggers) understands your code.

## The compile_commands.json invariant

> **Every C/C++ project must export `compile_commands.json`.**

It's a JSON database of compiler invocations per file. Without it, clang-tidy/IWYU/clangd can't parse your code correctly (they need to know macros, includes, standard, flags). The `cpp-static-analysis` skill enforces this prerequisite.

## Per-build-system commands

### CMake

```bash
cmake -S . -B .build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build .build -j
```

- `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` is **mandatory** unless already in `CMakeLists.txt` via `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`
- Out-of-source build (`.build/`) keeps the source tree clean
- Symlink from project root so tools find it: `ln -sf .build/compile_commands.json .`

### Meson

```bash
meson setup builddir
meson compile -C builddir
```

- Meson emits `compile_commands.json` in builddir automatically. Symlink it to root if tooling expects it there.

### Make (raw)

Pure Makefile projects don't generate compile_commands.json natively. Use [`bear`](https://github.com/rizsotto/Bear):

```bash
bear -- make -j
```

Or [`compiledb`](https://github.com/nickdiego/compiledb):

```bash
compiledb make -j
```

### Bazel

```bash
bazel build //...
bazel run @hedron_compile_commands//:refresh_all
```

Bazel requires the [`hedron_compile_commands`](https://github.com/hedronvision/bazel-compile-commands-extractor) rule. If not configured, suggest the user add it; do NOT try to hand-edit BUILD files.

## Build failure triage (you fix common ones, escalate the rest)

1. **CMake "could not find package X"** → likely missing `find_package(X REQUIRED)` cleanup or wrong CMAKE_PREFIX_PATH. Suggest: `cmake -L .build` to inspect, or pass `-DX_DIR=...`.

2. **Linker "undefined reference"** → missing source in target or missing link library. Check `target_link_libraries(...)` lists everything.

3. **"No such file: <header.h>"** → missing `target_include_directories` or system header missing. For system headers, suggest installing the dev package.

4. **Configure step fails on macOS** → often missing Command Line Tools: `xcode-select --install`.

5. **Anything cryptic** → escalate: dispatch the `cpp-build-doctor` subagent with the full error log.

6. **Anything you have now failed to fix twice** → escalate, even if it looked obvious. The first
   diagnosis is yours; a second failed attempt at the *same* failure means your hypothesis is the
   problem, and fresh context beats another iteration on a wrong prior. (Fixing it on the first
   try and moving on is the expected path — this is a repeat-failure trigger, not a "always
   delegate build errors" rule. The Session Pulse hook independently nudges at ≥3 repeats; this
   fires earlier and is yours to honour.)

## Multi-config builds (Debug + Release + Sanitizer)

Keep separate build dirs:
```
.build/debug
.build/release
.build/asan
```

This is critical for `cpp-sanitizers` skill — the sanitizer build is a separate config, not a flag toggle on the same build.

## When the user has NO build system yet

Don't pick one for them. Ask:

- Single-file experiment → suggest plain CMake (most portable)
- Header-only library → suggest CMake INTERFACE target
- Existing autotools project → keep it; just add `bear` for compile_commands.json
- Bazel monorepo → it's a one-way door, only suggest if user already uses it elsewhere

## Detection helper

Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/cpp-detect.sh --target .` to get a JSON summary of what's present. Used by the SessionStart hook to gate C/C++ skills.

## References

- See `cmake-reference.md` for CMake idioms used in this codebase / project conventions.
- See `meson-reference.md` for Meson equivalents.
- See `compile-commands-guide.md` for the deep-dive on compile_commands.json semantics.

## When NOT to invoke this skill

- Pure C/C++ language questions (use docs / Context7 instead)
- Build performance tuning — separate concern; use after the build works
- Cross-compilation — out of scope for harness-anchor; consult build system docs

## Calibrated uncertainty

If you propose a build fix you haven't verified by running the build:

> "I believe the fix is `<change>`. Please run `cmake -S . -B .build && cmake --build .build` and share the output before we mark this resolved."

## Looking up tool errors

Unfamiliar CMake/Meson/Bazel error or missing-package message? **Don't guess** — invoke the `docs-lookup` skill, which encodes the canonical Context7 → WebSearch → calibrated-uncertainty fallback chain (with explicit "Context7 is unavailable" detection so you don't silently degrade to guessing).

Typical entry queries: `cmake find_package`, `meson dependency`, `bazel cc_binary`, exact error string in quotes.
