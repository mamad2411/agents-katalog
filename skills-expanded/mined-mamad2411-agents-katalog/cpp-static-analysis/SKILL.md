---
name: cpp-static-analysis
description: Use in C/C++ projects when reviewing changes or hunting bugs. Runs clang-tidy/cppcheck/IWYU. Needs compile_commands.json. Changed lines only.
---

# C/C++ Static Analysis

Static analysis catches an enormous class of bugs at zero runtime cost: null derefs, leaks, dangling refs, integer overflow, missing initializers, unused includes, banned APIs.

Three core tools cover most needs:

| Tool | What it catches | Cost |
|---|---|---|
| **clang-tidy** | Style + correctness + modernize + bugprone | Heavy (uses full AST) |
| **cppcheck** | Quick correctness, leaks, off-by-one | Light (own parser) |
| **IWYU** | Missing/superfluous `#include` | Heavy (compile-driven) |

## Prerequisites (hard)

- `compile_commands.json` exists at project root or symlinked
- A `.clang-tidy` config exists at project root (use template if not)
- The tool is actually reachable — **resolve this with the discovery script, not with `command -v`**:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/cpp-tool-discovery.sh clang-tidy cppcheck include-what-you-use
```

`FOUND` lines carry the absolute path — use it directly (the tool need not be on
PATH to be usable). Only a `NOT_FOUND` line licenses you to call a tool unavailable.

**An empty `command -v` / `where` proves nothing.** On Windows the VS-bundled LLVM
only joins PATH after `vcvars64.bat`; on macOS Homebrew's llvm is keg-only. Report
absence as **"searched PATH + \<listed locations\>, not found (as of \<YYYY-MM-DD\>)"** —
never "not installed" / "on this machine". The first is a falsifiable claim about
your search; the second is an unfalsifiable claim about the world, and it tends to
get written into AGENTS.md where it silently disables this skill for every later session.
The date carries the other half: a scope-less negative is wrong about *where* you
looked, a date-less one is wrong about *when*. Both turn one observation into a
standing fact — and AGENTS.md is exactly where standing facts go unchallenged.

If any prerequisite is missing, **say so explicitly** instead of pretending to analyze:

> "Cannot run clang-tidy because compile_commands.json is missing. Generate it via `cmake -S . -B .build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON` then symlink to root."

## clang-tidy — daily-driver

### Incremental usage (preferred)

After an Edit/Write to a .c/.cpp/.h file:

```bash
clang-tidy -p .build --quiet path/to/changed_file.cpp
```

- `-p .build` points at compile_commands.json's directory
- `--quiet` suppresses progress noise
- Returns 0 if clean, non-zero if warnings
- **macOS + Homebrew clang-tidy: add the SDK sysroot** or the run fails to parse — see
  "macOS failure mode" below (or just use `scripts/lint.sh`)

For changed lines only (large existing codebases), use [`clang-tidy-diff.py`](https://github.com/llvm/llvm-project/blob/main/clang-tools-extra/clang-tidy/tool/clang-tidy-diff.py):

```bash
git diff -U0 main | clang-tidy-diff.py -p1 -path .build
```

### Full-project scan

```bash
run-clang-tidy -p .build -quiet -j$(nproc) > clang-tidy-report.txt 2>&1
```

Use sparingly — slow on large codebases.

### macOS failure mode: `'<header>' file not found` (Homebrew clang-tidy)

`compile_commands.json` produced with Apple clang (`/usr/bin/c++`) implies the macOS SDK;
Homebrew clang-tidy does **not** know it. Without a sysroot it fails to parse the TU
(`error: 'atomic' file not found` or similar) — and **diagnostics from a failed parse are
garbage**: the half-parsed TU yields false positives (bogus const/naming/static
suggestions). Do not act on them; capture the real signal first (`self-correction-loop`).

Fix — point clang-tidy at the active SDK:

```bash
clang-tidy -p .build \
  --extra-arg=-isysroot --extra-arg="$(xcrun --show-sdk-path)" \
  path/to/changed_file.cpp
```

Or use the project wrapper `scripts/lint.sh` (dropped by `/cpp-init`), which locates the
compilation database (root / `.build/` / `build/` / `builddir/`, same search order as the
PostToolUse hook) and injects the sysroot automatically on macOS. The hook applies the
same fix and suppresses its diagnostics entirely when the TU still fails to parse.

### Common check categories

| Category | What it covers | Recommendation |
|---|---|---|
| `bugprone-*` | Likely bugs | Always on |
| `cert-*` | CERT secure coding | Often on |
| `clang-analyzer-*` | Path-sensitive analysis | Always on |
| `cppcoreguidelines-*` | C++ Core Guidelines | Selective |
| `modernize-*` | Convert to modern idioms | Off in legacy code, on in greenfield |
| `performance-*` | Perf antipatterns | Selective |
| `readability-*` | Style | Selective |

The template `.clang-tidy` enables a safe baseline; tune per project.

## cppcheck — second opinion

```bash
cppcheck --enable=warning,style,performance,portability --suppress=missingIncludeSystem -j$(nproc) src/ 2>&1
```

cppcheck catches things clang-tidy misses (and vice versa). Run before claiming a feature done.

## IWYU — keep includes honest

```bash
include-what-you-use -Xiwyu --no_fwd_decls path/to/file.cpp 2>&1
```

Reports: which includes are unused, which symbols come from indirect includes (should be added). Use `iwyu_tool.py` for project-wide.

Note: IWYU has false positives; review suggestions, don't auto-apply.

## Clang Static Analyzer — you're already running it

The `clang-analyzer-*` checks in the baseline `.clang-tidy` **are** the Clang Static Analyzer
(path-sensitive, inter-procedural symbolic execution), run per translation unit. clang-tidy
already gives you CSA coverage — don't treat a separate analyzer run as "new" findings.

`scan-build` is the *same engine* driven across a **whole build**: it wraps your compiler
(no `compile_commands.json` needed) and emits browsable HTML reports tracing each bug's path.

```bash
scan-build --view make            # wraps the build; --view opens the HTML report
```

Reach for `scan-build` only for whole-program / cross-TU findings or HTML triage — otherwise
the per-file clang-tidy path (including the PostToolUse hook) already covers you.

## GCC -fanalyzer (C only)

GCC 10+ ships its own static analyzer — a **different engine** from clang-tidy, so it's a
genuine second opinion: double-free, use-after-free, leaks, null derefs, taint, fd misuse.

```bash
gcc -fanalyzer -c path/to/file.c    # warnings on stderr; uses the compiler you already have
```

**Caveat (important):** the GCC manual states `-fanalyzer` is "only suitable for use on C
code" — **C++ is not officially supported**. For C++, stay on clang-tidy + cppcheck. Use
`-fanalyzer` as a free extra pass on **C** builds.

## Warn-only philosophy

The PostToolUse hook surfaces clang-tidy warnings as `additionalContext`. You see them on the next turn. You decide whether to fix each one — there are legitimate reasons to suppress (e.g., `// NOLINT(specific-check)` with a comment).

Anti-patterns:
- Silencing warnings with broad disables (`// NOLINTBEGIN/NOLINTEND` on hundreds of lines)
- Adding the suppressed check to `.clang-tidy` to "make it stop"
- Ignoring warnings indefinitely

If a warning is wrong (false positive), file a one-line `// NOLINT(check-name) — reason` with explanation. Be specific.

## When to defer

If a warning is in code you didn't change (legacy area) and not a regression risk, defer it: note in `progress.md`, don't fix in this session. Scope discipline.

## Looking up unfamiliar checks

When you encounter a clang-tidy check name you don't recognize (e.g. `bugprone-suspicious-enum-usage`, `cert-err58-cpp`), or an unfamiliar cppcheck ID / IWYU pragma — invoke the `docs-lookup` skill. It handles Context7 → WebSearch fallback (with explicit failure-mode detection) so you don't silently substitute a guess.

Typical entry query: `clang-tidy <check-name>` or `cppcheck <id>`.

## Templates

- `.clang-tidy` baseline config: `templates/cpp/.clang-tidy.tpl` (copied by `/cpp-init`)
- `scripts/lint.sh` sysroot-aware clang-tidy wrapper: `templates/cpp/lint.sh.tpl` (copied by `/cpp-init`)
- See `tool-comparison.md` for clang-tidy vs cppcheck vs IWYU side-by-side decisions.

## Windows notes

- clang-tidy needs a `compile_commands.json`; **CMake + Ninja** (`-DCMAKE_EXPORT_COMPILE_COMMANDS=ON -G Ninja`)
  produces one on Windows — MSBuild generators do NOT. No sysroot injection is needed
  (that is a macOS-only concern); the PostToolUse hook already skips `xcrun` off-Darwin.
- With an MSVC-flavored database (`cl.exe` commands), clang-tidy auto-detects driver
  mode in most setups; if the TU fails to parse, the diagnostics-are-garbage rule
  applies unchanged — verify via the build or `scripts/lint.sh`, don't act on them.
- GCC `-fanalyzer` guidance is unchanged (MinGW GCC works; still C-only).
