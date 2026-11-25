---
name: native-wsl-workspaces
description: Reliably inspect, create, edit, validate, and transfer files in a Windows-hosted WSL workspace. Use when a task names a WSL path, a `\\wsl.localhost` path, a Windows/WSL project location, or when remote file writes, UNC paths, mounted workspaces, and WSL shell execution may disagree.
---

# Native WSL Workspaces

Use this skill to establish one authoritative **native WSL** workspace before modifying a Windows-hosted WSL project. Do not assume that a Windows path, UNC path, agent-mounted path, and Linux path are interchangeable.

## Mandatory workflow

1. **Resolve the canonical workspace.** Extract the exact distribution and native Linux path from the user. Treat a path such as `\\wsl.localhost\Ubuntu-26.04\home\idols\project` as the native path `/home/idols/project` in distribution `Ubuntu-26.04`.
2. **Start outside UNC.** Run the remote Windows shell from `C:\`. Do not invoke WSL while the current Windows directory is a `\\wsl.localhost\…` path.
3. **Verify before writing.** Invoke `scripts/verify_wsl_workspace.sh` through `wsl.exe -d <distro> -- bash …` with `--probe-write`. Stop if it reports `/mnt`, `drvfs`, a nonexistent directory, or a write/read/delete failure.
4. **Treat non-native routes as non-authoritative.** Use `\\wsl.localhost\…` and any agent mount only for inspection or explicitly verified transport. Never write through them and assume WSL will see the change.
5. **Write deterministically.** For generated or large files, upload the generated artifact, record its SHA-256, and run `scripts/install_verified_url.sh` inside native WSL to download, verify, and atomically install it. For a short change, use a single noninteractive WSL command from `C:\`, then verify the target in the same WSL shell.
6. **Validate in place.** Run the project’s own tests, Git status, and build tools only from the verified native WSL path.
7. **Recover explicitly.** If prior work occurred in another route, do not overwrite it. Compare hashes, retain the other copy as a backup, declare the native WSL path authoritative, then perform a verified transfer.

## Command patterns

Read [references/remote-execution.md](references/remote-execution.md) before selecting a route. Use the following sequence conceptually:

```text
Windows shell at C:\
  → wsl.exe -d <distro> -- bash verify_wsl_workspace.sh <native-path> --probe-write
  → deterministic atomic write from a local source
  → WSL-native hash/read verification
  → project operations in the verified native workspace
```

## Non-negotiable constraints

- Never run a large interactive heredoc in a WSL terminal session.
- Never initialize Git, install dependencies, configure services, or deploy before the native-path probe succeeds.
- Never move or expose secrets as part of a workspace transfer.
- Never use a `\\wsl.localhost\…` working directory to launch a command that calls `wsl.exe`.
- Never silently choose a different workspace than the user specified.

## Bundled resources

| Resource | Use |
|---|---|
| `scripts/verify_wsl_workspace.sh` | Use first. It checks location/filesystem and runs an optional atomic write probe. |
| `scripts/install_verified_url.sh` | Use after uploading a generated artifact; it verifies SHA-256 and atomically installs it into native WSL. |
| `references/remote-execution.md` | Read for safe/unsafe route guidance and recovery. |
