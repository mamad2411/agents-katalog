---
name: gomtm-installer
description: Use when initializing a fresh Linux server with gomtm install over SSH, validating gomtm install command contracts, or deciding whether to run gomtm install versus gomtm install --dev. Also use when repairing gomtm install docs or avoiding obsolete --stage/installer --target workflows.
---

# gomtm Installer

## Core Rules

- Treat `gomtm install` as the only public initialization command.
- Use `gomtm install --dev` when the target needs the gomtm development environment.
- For a fresh development server, the expected public command is `gomtm install --dev` after the `gomtm` binary is installed.
- Do not use or document `gomtm install --stage=...` as a user-facing command.
- Do not use `gomtm installer --target=...`; that is not the current public contract.
- Confirm the local command contract before touching a remote host if the task says install was recently refactored or broken.
- On a fresh server, avoid ad-hoc setup commands beyond installing/updating the `gomtm` binary itself; initialization should be driven by `gomtm install` commands.

## Safety Workflow

1. Verify source truth first: read `cmd/install.go`, `pkg/mtinstall/mtinstall.go`, `pkg/mtinstall/mtinstall_stage_runner.go`, and `pkg/mtinstall/remote/bootstrap_script.go`.
2. Verify command help locally: `gomtm install --help` or `go run ./cmd install --help` must show `--dev` and must not expose `--stage`.
3. If the contract is wrong, stop and ask before changing code or running remote initialization.
4. After repair, run targeted tests for `cmd`, `pkg/mtinstall`, `pkg/mtinstall/core`, and `pkg/mtinstall/remote` before using the command on a server.
5. Only after the contract is confirmed, connect to the target and run the gomtm install command.

## Command Contract

| Scenario | Command shape |
| --- | --- |
| Base runtime install | `gomtm install [packages...]` |
| Development environment install | `gomtm install --dev [packages...]` |
| Internal root-stage reentry | `GOMTM_INSTALL_STAGE=root gomtm install --dev [packages...]` |
| Internal user-stage reentry | `GOMTM_INSTALL_STAGE=user gomtm install --dev [packages...]` |

The environment variable stage is internal plumbing for two-phase bootstrap. Do not present it as the normal user command unless source-level repair or generated bootstrap scripts require it.

## Remote Initialization

1. Install or update the `gomtm` binary on the fresh server using the current project-approved distribution path.
2. Run `gomtm install --help` on the server and confirm the same public contract.
3. Run `gomtm install --dev` for a development server, or `gomtm install` only for base runtime setup.
4. Prefer the generated bootstrap path in `pkg/mtinstall/remote` when available; do not hand-author a parallel installer.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Running `gomtm install --stage=root` because old docs mention it | Use `gomtm install --dev`; only generated/internal code may set `GOMTM_INSTALL_STAGE` |
| Running arbitrary apt/npm/docker setup on the target | Let `gomtm install` own initialization unless the user explicitly approves a repair step |
| Trusting a draft skill over source and tests | Source and tests are canonical; update the skill after confirming them |
| Connecting to a fresh server before checking a suspected broken CLI | Build a local feedback loop first, then ask before remote changes |

## Verification

Use the smallest command set that proves the touched surface:

```bash
go run ./cmd install --help
go run ./cmd install --dev --help
go test ./cmd ./pkg/mtinstall ./pkg/mtinstall/core ./pkg/mtinstall/remote
```

For remote use, verify post-install behavior through `gomtm` commands and gomtm's own smoke checks before claiming initialization is complete.
