---
name: zvm
version: 1.0.0
description: "Zig Version Manager (zvm): install or update zvm, install Zig toolchains, switch active Zig versions, resolve SemVer patterns such as 0.15 / 0.15.2-esp, and troubleshoot PATH issues where zig does not point to ~/.zvm/bin/zig. Use when the user mentions zvm, Zig version management, ESP Zig builds, zvm install/use/current/doctor, or asks why zig version does not match zvm current."
---

# zvm Agent Skill

Use this skill when a user wants to install, update, or operate zvm, the Zig Version Manager.

## When to Use This Skill

Use this skill when the user wants to:

- Install, update, or verify zvm itself.
- Install or switch Zig toolchains with `zvm install` or `zvm use`.
- Resolve version patterns such as `0.15`, `0.16`, `0.15.2-esp`, or `0.15.2-esp.*`.
- Troubleshoot `zig version`, `zvm current`, `which zig`, PATH, or `~/.zvm/bin/zig` symlink issues.
- Work with official Zig releases or ESP Zig bootstrap builds.

Do not use this skill for general Zig language debugging unless the task involves zvm, Zig installation, version selection, or PATH behavior.

## Install zvm

zvm is distributed as prebuilt release binaries. Users do not need Zig installed.

```sh
curl -fsSL https://github.com/embed-zig/zvm/releases/latest/download/install.sh | sh
```

Useful environment variables:

- `ZVM_VERSION`: release tag, default `latest`
- `ZVM_INSTALL_DIR`: install root, default `$HOME/.zvm`

The installer writes `zvm` to `$ZVM_INSTALL_DIR/bin/zvm` and tries to add `$ZVM_INSTALL_DIR/bin` to existing shell startup files. If the current shell does not see zvm yet, run:

```sh
export PATH="$HOME/.zvm/bin:$PATH"
```

## Install This Agent Skill

If the user wants agent support, install zvm first, then install this skill globally:

```sh
curl -fsSL https://github.com/embed-zig/zvm/releases/latest/download/install.sh | sh
npx skills add embed-zig/zvm --skill zvm -g -y
```

## Update zvm Itself

Run:

```sh
zvm self-update
```

If zvm reports that it is Homebrew-managed, use:

```sh
brew upgrade zvm
```

## Install and Switch Zig

List available versions:

```sh
zvm list-remote
zvm list-remote '0.15.*'
```

Install and switch:

```sh
zvm install 0.15
zvm use 0.15
```

Pattern examples:

```sh
zvm install 0.15          # highest 0.15.x release
zvm install 0.15.2-esp    # highest 0.15.2 ESP build
zvm use 0.16              # highest installed 0.16.x version
```

Verify:

```sh
zvm current
zig version
zvm doctor
```

zvm uses one PATH directory: `$HOME/.zvm/bin`. The active Zig is `$HOME/.zvm/bin/zig`, a symlink to `../versions/<version>/zig`.

## Troubleshooting Rules

If `zvm current` and `zig version` disagree:

1. Run `zvm doctor`.
2. Check `which zig` or `command -v zig`.
3. The expected path is `$HOME/.zvm/bin/zig`.
4. If another Zig appears first, put `$HOME/.zvm/bin` before it in PATH and run `rehash` for zsh.

Useful checks:

```sh
zvm current
command -v zig
zig version
zvm doctor
```
