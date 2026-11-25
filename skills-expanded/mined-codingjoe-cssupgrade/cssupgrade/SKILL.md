---
name: cssupgrade
description: CSSupgrade auto-updates CSS syntax to new features based on browser support. Use when the user asks to modernize, upgrade, or clean up CSS syntax.
allowed-tools: Bash(npx -y cssupgrade *) Read
---

Use the CLI with `npx` on files or standard input:

```console
npx -y cssupgrade [--baseline <newly-available|widely-available>] [--check] [--write] <files|->
```

- Use `--check` to preview changes and fail when updates are needed.
- Use `-` to read from standard input and write the transformed code to standard output.
- Use `--write` to apply updates in place for file inputs.
- Use `--baseline` to choose `newly-available` or `widely-available` (default).
