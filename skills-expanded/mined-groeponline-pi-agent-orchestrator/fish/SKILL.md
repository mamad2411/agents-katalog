---
name: fish
description: "Fish-shell safety guide for agents. Use when generating shell commands that run under the fish shell (the user's default login shell). Prevents heredoc/loop/pipe breakage by providing fish-safe patterns."
trigger: /fish
---

# /fish — Fish-Shell Command Safety

The user's default login shell is **fish** (`/home/linuxbrew/.linuxbrew/bin/fish`, v4.8).
When the agent emits a `shell` command that is executed through fish, POSIX/bash-only
syntax breaks. This skill collects the patterns that fail and their fish-safe fixes so
generated commands actually run.

## Patterns that BREAK under fish

| POSIX/bash | Why it breaks in fish | Fish-safe fix |
|------------|----------------------|---------------|
| `for x in a b; do ...; done` | fish has no `do`/`done` | `for x in a b; ...; end` |
| `cmd <<'EOF' ... EOF` heredoc | fish heredoc quoting differs / broken | use the `write` tool to create the file, then `node file.mjs` (preferred), OR `echo "..." \| bash -c '...'` |
| `VAR=$(cmd)` | works in fish but `$VAR` interpolation is feature-rich; avoid mixing | use `bash -c '...'` for any complex POSIX script |
| `if [ -z "$x" ]; then ...` | `[` test builtin differs | `if test -z "$x"; ...; end` or wrap in `bash -c` |
| `grep -rE "x" --include="*.ts" dir` | fine, but glob expansion differs | use the Glob/Grep tools instead of shell globs |
| `2>&1 \| head` | fine in fish | fine |
| `command1 && command2` | fine in fish | fine |
| `export FOO=bar; npm test` | fine | fine |

## Golden rule

For anything beyond a single simple pipeline, **wrap the whole thing in `bash -c '...'`**
or write a temporary script file with the `write` tool and execute it with `node`/`bash`.
The agent's own tools (`glob`, `grep`, `read`, `write`, `edit`) should be used INSTEAD of
shell one-liners wherever possible — they avoid shell quoting entirely.

## Fish-safe snippets

```fish
# Loop over files (fish native)
for f in .pi/agents/*.md
  echo $f
end

# Run a POSIX script reliably
bash -c 'for f in a b c; do echo "$f"; done'

# Count matching lines
grep -rc "pattern" src/ | wc -l

# Test condition
if test -f README.md
  echo exists
end
```

## When to use this skill

Activate whenever a shell command fails with errors like:
- `Expected a variable name after this $`
- `Missing end to balance this for loop`
- `Expected a string, but found a redirection` (heredoc)
- `Unknown error while evaluating command substitution`

Re-issue the command using one of the fish-safe forms above.
