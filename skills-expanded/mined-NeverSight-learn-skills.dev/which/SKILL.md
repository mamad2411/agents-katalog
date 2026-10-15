---
name: which
description: >-
  Forbids using the `which` command to check whether a command exists or
  to resolve its path. Always use the POSIX shell builtin `command -v`
  instead.
when_to_use: >-
  Use whenever about to probe a command's availability or resolve its path
  in a shell — install scripts, CI checks, README snippets, Makefiles,
  shell scripts, mise/asdf hooks, ad-hoc terminal commands. Triggers:
  «есть ли команда», «проверь, установлен ли», «найди путь к бинарю»,
  «which foo», «check if X is installed», «is X on PATH»,
  «resolve binary path», «find executable».
---

# which

Never use `which` to test for a command or to print its path.
Use `command -v` instead.

## Why

- `command -v` is a POSIX-mandated shell builtin
  (bash, zsh, dash, ash, ksh, busybox sh).
  `which` is an external program
  and may be missing,
  aliased,
  or replaced by a shell function.
- `which` behavior varies across implementations:
  BSD, GNU, Debian's shell-script `which`, zsh's builtin,
  and busybox's applet
  differ in flags,
  output format,
  and exit codes.
- `command -v` reports shell builtins,
  functions,
  and aliases —
  not just files on `$PATH` —
  which is what callers usually actually want.
- `command -v` returns a reliable non-zero exit code
  when the name is not found,
  with no output on either stdout or stderr.

## Direct substitutions

| Don't                       | Do                                       |
| --------------------------- | ---------------------------------------- |
| `which foo`                 | `command -v foo`                         |
| `which foo >/dev/null 2>&1` | `command -v foo >/dev/null`              |
| `if which foo; then …`      | `if command -v foo >/dev/null; then …`   |

The `2>&1` is dropped because `command -v` writes nothing to stderr when
the name is not found.

Two cases have no one-liner replacement and need the idioms below:

- `path=$(which foo)` — `command -v` may return a builtin name or alias
  string, not a filesystem path.
- `which -a foo` — `command -v` resolves only the first hit.

## Idioms

Existence check (silent):

```sh
if command -v foo >/dev/null; then
  # ...
fi
```

Existence check with a clear failure message:

```sh
command -v foo >/dev/null || {
  echo "foo is required but not installed" >&2
  exit 1
}
```

Resolve a filesystem path:

```sh
foo_path=$(command -v foo) || {
  echo "foo not found" >&2
  exit 1
}
case "$foo_path" in
  /*) ;;
  *)  echo "foo is not an external binary (got: $foo_path)" >&2
      exit 1 ;;
esac
```

`command -v` may output:

- `/usr/bin/foo` — external file on `$PATH`;
- `foo` — shell builtin or function;
- `alias foo='…'` — alias.

The `/*` guard accepts only the first form.

## Edge cases

- **Listing every match on `$PATH` (`which -a`)**
  has no single-call POSIX equivalent.
  Walk `$PATH` explicitly:

  ```sh
  ( IFS=:
    for dir in $PATH; do
      candidate=${dir:-.}/foo
      [ -f "$candidate" ] && [ -x "$candidate" ] && printf '%s\n' "$candidate"
    done )
  ```

  `[ -f ]` together with `[ -x ]` filters to regular executable files —
  matching what `which -a` reports;
  `[ -x ]` alone would also accept directories with the execute bit.

  In bash and zsh, `type -a foo` is shorter
  but not portable.

- **Makefiles.**
  Recipes run through `$(SHELL)`,
  default `/bin/sh`.
  If a project sets `SHELL` to a non-POSIX shell,
  pin recipes back to a POSIX shell —
  e.g. `SHELL := /bin/sh` —
  before relying on `command -v`.

## Scope

This rule applies to anything written or run as POSIX shell:
`Bash` tool invocations,
snippets in `SKILL.md` / `README.md`,
scripts under `scripts/`,
Makefiles,
CI configs,
Dockerfiles,
install instructions,
suggested one-liners.

Out of scope:
fish,
and tooling that wraps `which` internally
(CMake's `find_program`, `npm bin`, etc.).

If you encounter a `which` call while editing a file,
replace it with the equivalent `command -v` form as part of the same edit.
