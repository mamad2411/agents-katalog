---
name: cpp-formatting
description: Use in C/C++ projects for clang-format. Changed-lines-only; never reformat unchanged code mid-feature. .clang-format from root or LLVM baseline.
---

# C/C++ Formatting (clang-format)

`clang-format` is the de-facto C/C++ formatter. Like Prettier or rustfmt, it's deterministic and removes formatting debates.

## Prerequisites

- `clang-format` reachable — see "Is clang-format actually here?" below before concluding
  it's missing; only then `brew install clang-format` / `apt install clang-format`.
- `.clang-format` config at project root (use `templates/cpp/.clang-format.tpl` if not present — `/cpp-init` drops it for you)

## Format changed lines only (preferred)

```bash
git diff -U0 --no-color HEAD | clang-format-diff -p1 -i
```

Or, for staged changes:

```bash
git clang-format
```

This formats **only changed lines** — does not touch unrelated code. Critical for keeping diffs clean.

## Is clang-format actually here?

Before concluding clang-format is unavailable, resolve it properly:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/cpp-tool-discovery.sh clang-format
```

A `FOUND` line gives you an absolute path — invoke it directly; the binary does
not need to be on PATH. Only `NOT_FOUND` licenses "unavailable", and then the
honest phrasing is **"searched PATH + \<listed locations\>, not found (as of \<YYYY-MM-DD\>)"**,
never "not installed" / "on this machine" (an empty `command -v` only tells you about PATH —
the VS-bundled LLVM on Windows and keg-only Homebrew llvm on macOS both sit off it).
The date matters as much as the scope: a scope-less negative is wrong about *where*
you looked, a date-less one is wrong about *when*.

## Format a whole file

```bash
clang-format -i path/to/file.cpp
```

Only use this on files you OWN this session, or when starting fresh. Reformatting an unchanged file in the middle of a feature pollutes the diff and obscures review.

## Verify (CI-friendly)

```bash
clang-format --dry-run --Werror path/to/file.cpp
```

Returns non-zero if anything would change. Useful in pre-commit / CI.

## Common .clang-format settings

The template uses LLVM as the base with a few popular tweaks:

```yaml
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
AllowShortIfStatementsOnASingleLine: Never
AllowShortFunctionsOnASingleLine: Empty
SortIncludes: true
```

Project teams should agree on `BasedOnStyle` (LLVM / Google / Mozilla / WebKit) early and stick with it. Don't tweak per-PR.

## When NOT to run clang-format

- Mid-merge / mid-rebase — let the merge complete first, then format
- On generated code (e.g., `.pb.cc` from protobuf) — exclude via `.clang-format-ignore`
- On vendored third-party — exclude via the same

## Hook integration

The harness-anchor `Stop` hook (Phase 3+) is currently advisory; it doesn't auto-format. Format manually with `git clang-format` before `/session-end` to keep the diff clean.

## Sanity check after format

```bash
git diff --stat   # should show only changed lines' format
```

If clang-format touched files you didn't change, your `.clang-format` may have drifted between machines (different versions produce different output). Pin clang-format major version in CI.

## Looking up clang-format options

For an unfamiliar `.clang-format` key (e.g. `PenaltyExcessCharacter`, `BreakInheritanceList`) — invoke the `docs-lookup` skill. It encodes the Context7 → WebSearch fallback and the "Context7 unavailable" detection rules.

Typical entry query: `clang-format <option-name>` or `clang-format style options`.
