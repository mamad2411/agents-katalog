---
name: pocketpatch
description: Use this skill whenever a user wants an agent to use PocketPatch for diff review
license: MIT
metadata:
  author: Kaden Cartwright
  version: "0.1.0"
---

# PocketPatch

PocketPatch reviews the current uncommitted git diff in a local, phone-friendly
web UI. Use it when handing agent-generated changes to a human for line-level
review before a PR.

## Basic Workflow

Run from the repository being reviewed:

```sh
npx pocketpatch register
```

Share the printed review URL with the human. The command starts the local daemon
if needed and registers the current working directory.

After the human reviews, read unresolved feedback from the same repository:

```sh
npx pocketpatch comments
```

Address each comment, then resolve handled comments:

```sh
npx pocketpatch comments resolve <id>
```

Re-run `npx pocketpatch comments` before reporting done. Mention any unresolved
comments that remain.

## Notes

- Use `pocketpatch ...` instead of `npx pocketpatch ...` if the user has a
  global install.
- Use `--project <id>` when the current directory does not match the registered
  project or the user gives a specific project id.
- Read `references/config.md` only for Tailscale/network setup, daemon
  debugging, config/state paths, or running PocketPatch from its source repo.
