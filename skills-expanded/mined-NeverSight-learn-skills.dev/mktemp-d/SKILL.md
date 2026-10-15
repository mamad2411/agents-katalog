---
name: mktemp-d
description: >-
  Forbids creating temporary files or directories at hardcoded paths
  under `/tmp`. Always allocate a private directory with `mktemp -d`
  and place every temporary artifact inside it.
when_to_use: >-
  Use whenever about to write a temporary file or directory in a shell —
  `Bash` tool calls, scripts, snippets in `SKILL.md` / `README.md`.
  Triggers: «временный файл», «временная папка», «положи в /tmp»,
  «создай файл в /tmp», «scratch dir», «temporary file»,
  «put it in /tmp», «mktemp», «mkdir /tmp/», «touch /tmp/».
---

# mktemp-d

Never create a temporary file or directory at a hardcoded path
under `/tmp`.
Always allocate a private directory with `mktemp -d`
and place all temporary artifacts inside it.

## Why

`mktemp -d` returns a unique, private directory.
A hardcoded path under `/tmp` does not —
it collides with concurrent runs and any leftover state from prior runs.

## Rule

One `mktemp -d` per logical scope, then build paths inside it:

```sh
tmpdir=$(mktemp -d)

cp something "$tmpdir/input"
do_work > "$tmpdir/output.log"
```

## Direct substitutions

| Don't                  | Do                                           |
| ---------------------- | -------------------------------------------- |
| `mkdir /tmp/work`      | `work=$(mktemp -d)`                          |
| `touch /tmp/out.log`   | `work=$(mktemp -d); : > "$work/out.log"`     |
| `cmd > /tmp/output`    | `work=$(mktemp -d); cmd > "$work/output"`    |
| `tar xf x.tar -C /tmp` | `work=$(mktemp -d); tar xf x.tar -C "$work"` |

If you encounter a hardcoded `/tmp/...` path while editing a file,
replace it with the `mktemp -d` idiom as part of the same edit.
