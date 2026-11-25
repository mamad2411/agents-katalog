---
name: open-supports-install
description: Install or update open_supports packages for a project (-t) or user-wide (-g), one package (-n) or from a list, by using scripts/install-open-supports.sh.
argument-hint: '-t <project> | -g [-n <pkg> [-- args] | -l <list>] [--skills-only|--no-skills|--dry-run|-F]'
---

# Open Supports Install

Use this Skill when the user asks to install, update, vendor, or inspect
`open_supports/` packages for a project.

## Pre-read

Before running commands:

1. Read the target project's `.claude/open_supports_name_list.txt`.
2. Read this repository's `open_supports/README.md`.

## Procedure

Default to the current working directory as the target project when the user does
not specify a target.

Run from the rule source repository:

```sh
sh scripts/install-open-supports.sh -t /path/to/project
```

Useful modes:

```sh
sh scripts/install-open-supports.sh -t /path/to/project --dry-run
sh scripts/install-open-supports.sh -t /path/to/project --skills-only
sh scripts/install-open-supports.sh -t /path/to/project --no-skills
sh scripts/install-open-supports.sh -t /path/to/project -F
```

Install a single package instead of a list (arguments after `--`):

```sh
sh scripts/install-open-supports.sh -t /path/to/project -n colbymchenry/codegraph -- --target=claude --location=local {PROJECT_DIR}
```

User-level (global) install: replace `-t <project>` with `-g`. It reads
`~/.claude/open_supports_name_list.txt` by default, runs install scripts from this
repository without vendoring, generates no wrapper Skill, rejects `-F` and
`--skills-only`, and refuses the whole list if any entry has `{PROJECT_DIR}`,
`--local`, or `--location=local`. Always run `--dry-run` first and ask before a
real global install, because it changes user-level configuration:

```sh
sh scripts/install-open-supports.sh -g --dry-run
```

To copy the repository's global list to `~/.claude/` and install it in one step,
use `sh scripts/install-claude-project.sh -g -d` (drop `-d` after confirming).

If a custom list file is requested:

```sh
sh scripts/install-open-supports.sh -t /path/to/project -l /path/to/open_supports_name_list.txt
```

If a custom `open_supports/` source root is requested:

```sh
sh scripts/install-open-supports.sh -t /path/to/project -s /path/to/open_supports
```

## Reporting

After the command finishes, report:

- which packages were vendored or reused;
- which wrapper Skills were generated or reused;
- which install scripts ran successfully;
- any `missing`, `no_script`, `failed`, or `conflict` counts;
- the next command the user should run if the script reported manual follow-up.
