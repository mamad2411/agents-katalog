---
name: kata
description: Use when creating, claiming, updating, or closing tasks/issues for this repository. Documents how the kata issue ledger is wired for the drskill project and the rules for tracking work in it.
---

# Kata task ledger (drskill)

This repository tracks work in **kata**, the shared issue ledger. The project is
bound by the committed `.kata.toml` (project name `drskill`). Run `kata` from the
repo root; `--workspace` overrides, `--project` targets another project.

Run `kata quickstart` for the full authoritative agent contract. This skill only
covers the project-local facts and the rules that are easy to get wrong.

## Facts

- Author resolves `$KATA_AUTHOR` > `$USER` > git `user.name`.
- Issue refs are `short_id`s derived from a ULID (e.g. `abc4`), or full 26-char
  ULIDs. Legacy numeric refs (`12`) no longer work. Cross-project: `kata#abc4`.
- `.kata.local.toml` is gitignored (per-workspace server override); `.kata.toml`
  is committed.

## Rules

1. **Search before creating.** `kata search "<topic>" --agent`, then update the
   matching issue instead of filing a duplicate.
2. **Use `--agent`** for ordinary reads and mutations. Reserve `--json` for when a
   script needs structured data (e.g. piping into `jq`).
3. **Closing asserts the work is complete.** Do not close unfinished work. If not
   done, `kata label add <ref> needs-review` and leave a comment saying what was
   attempted and what remains.
4. **Close each issue as soon as its work is verified** — never in a batch. Give a
   substantive message and typed evidence.
5. **Never run `delete` or `purge`** unless the user explicitly asks for that
   action and names the exact ref.
6. Real repository work only — no practice, tutorial, or scratchpad issues unless
   the user explicitly asks.

## Common commands

```sh
kata search "login race" --agent          # look first
kata create "fix X" --body "..." \
  --idempotency-key "drskill-fix-x-2026-05-02" --agent   # safe retries

kata ready --unowned --agent              # ready queue (no open blockers)
kata next --unowned --agent               # highest-priority ready issue
kata claim <ref>                          # fails if already owned

kata show <ref> --agent
kata comment <ref> --body "..."           # or --comment on a mutation
kata label add <ref> bug
kata edit <ref> --blocks <other>

kata close <ref> --done \
  --message "Fixed X; verified tests pass." \
  --commit <sha>
```
