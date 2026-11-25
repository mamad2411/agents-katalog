---
name: riscos-commands
description: Commands ('*Commands') used by the RISC OS command line, in Command files (for *Exec), Obey files, OSCLI in BASIC, passed as `--command`s to `riscos-build-run`, executed within `.robuild.yaml` and `--commands` to RISC OS Pyromaniac. Use when needing to know about RISC OS commands in *Obey, OSCLI in BASIC, `.robuild.yaml` executions.
metadata:
  author: gerph@gerph.org
license: MIT
---

# RISC OS Commands

This skill provides a reference for commands used in RISC OS (the `*` commands).

## Common Operations

- **Conditionals**: Use `*IF` and `*IfThere` for flow control. See [references/conditionals.md](references/conditionals.md).
- **Variable Handling**: Set and evaluate system variables with `*Set`, `*SetEval`, etc. See [references/variables.md](references/variables.md).
- **Filesystem Operations**: Core commands for managing files and directories (`*Copy`, `*Delete`, `*Dir`, etc.). Includes configuration for ADFS, CDFS, NetFS, etc. See [references/filesystem.md](references/filesystem.md).

## Specialized Commands

- **Wimp & Desktop**: Commands for managing the desktop environment, Filer, and Wimp tasks. See [references/wimp.md](references/wimp.md).
- **Network**: Commands for network configuration, IP, AppleTalk, and DHCP. See [references/network.md](references/network.md).
- **General System**: System settings, module management, and utility commands (e.g. `*AMInfo`, `*Do`, `*HOff`). See [references/system.md](references/system.md).

## Syntax format

For information on syntax format, see [references/syntax.md](references/syntax.md).
