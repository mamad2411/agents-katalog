---
description: Shape and filter `hostinger-cli` output for parsing or downstream commands using `-o json`, `--jq`, `--template`, and the HOSTINGER_OUTPUT env var. Use when piping CLI results into scripts, extracting specific fields, or composing multi-step workflows.
---

# Output shaping for `hostinger-cli`

The CLI auto-picks **table** in a TTY and **JSON** when piped or in CI.
For agent-driven work, you should make that choice explicit.

## Force machine-readable output

- Per command: `-o json` (or `-o yaml`, `-o template`).
- Whole session: `export HOSTINGER_OUTPUT=json`.
- Compact (single line, good for `xargs`): add `--compact`.

```sh
hostinger-cli vps vm list -o json --compact
```

## Filter with `--jq`

`--jq '<expr>'` runs a pure-Go `gojq` filter **before** rendering, so the
expression sees the raw response shape (typically a top-level array or
object — not a CLI-wrapped envelope).

| Goal | Example |
| --- | --- |
| All VM IDs | `vps vm list --jq '.[].id'` |
| Hostnames of running VMs | `vps vm list --jq '.[] | select(.state=="running") | .hostname'` |
| Count owned domains | `domains portfolio list --jq 'length'` |
| Map of name→state | `vps vm list --jq '[.[] | {(.hostname): .state}] | add'` |
| First action's status | `vps vm actions <vm-id> --jq '.[0].state'` |

If a `--jq` expression yields multiple results, the CLI emits them as a
JSON array; a single result is emitted bare. Force array shape with
`--jq '[ ... ]'` if a script depends on it.

## Go templates

Use `--output template --template '<body>'` for cheap, dependency-free
formatting (no `jq` required):

```sh
hostinger-cli vps vm list -o template \
  --template '{{ range . }}{{ .id }}	{{ .hostname }}	{{ .state }}{{"\n"}}{{ end }}'
```

Templates see the same data structure as `--jq`.

## Patterns

- **Pipe to `xargs`**: pair `-o json --compact --jq '.[].id'` with
  `tr -d '[]"' | tr ',' '\n'` or use the template form for tab-separated
  rows.
- **Diff state**: dump a zone or VM to disk with
  `dns zone get --domain X -o json > before.json`, mutate, then `diff`.
- **Don't parse table output.** It's TTY-styled and version-unstable.
  Always switch to JSON for downstream consumption.
