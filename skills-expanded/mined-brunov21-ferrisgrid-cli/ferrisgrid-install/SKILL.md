---
name: ferrisgrid-install
description: Install and verify the published FerrisGrid CLI from crates.io. Use when setting up FerrisGrid, checking prerequisites, installing the ferrisgrid command, or confirming screen/input permissions.
---

# FerrisGrid Install

Use this when a machine needs the normal published FerrisGrid CLI. Only use a local checkout when the user explicitly asks for source development.

## Steps

1. Check Rust is available and whether `ferrisgrid` is already on `PATH`:

```bash
cargo --version
which ferrisgrid
```

If Rust is missing, tell the user Rust/Cargo must be installed before the published CLI can be installed.

2. Install or update the published CLI from crates.io. The crates.io package name is `ferrisgrid-cli`; it installs the executable named `ferrisgrid`:

```bash
cargo install ferrisgrid-cli
```

If this fails with DNS, crates.io index, or other network-related errors in a sandboxed agent environment, retry the same command with the normal escalation flow because `cargo install` needs network access.

3. Confirm the installed binary is available and responds:

```bash
which ferrisgrid
ferrisgrid help
```

Do not use `ferrisgrid --version` as the verification command unless the CLI has added that command; older releases report it as an unknown command.

4. Run diagnostics:

```bash
ferrisgrid doctor
```

On macOS, `doctor` can exit successfully while reporting native capture problems such as `CoreGraphics returned no displays` and `screens: 0`. Treat that as an environment or permission issue, not an install failure, if `ferrisgrid help` and the fake backend smoke test work.

5. Smoke-test capture without touching the real desktop:

```bash
ferrisgrid observe --backend fake
```

This verifies the CLI protocol and output writing path even when native desktop capture is unavailable.

## Development from source

Use these commands only inside a local FerrisGrid checkout when modifying the project:

```bash
cargo build -p ferrisgrid-cli
cargo test --workspace
cargo run -q -p ferrisgrid-cli -- doctor
```

## Notes

- On macOS, real capture needs Screen Recording permission.
- On macOS, real capture may also require running from a logged-in desktop session.
- Real actions need Accessibility permission.
- Default output is `.ferrisgrid/`.
- Use `--backend fake` only for protocol smoke tests; normal usage should use the native backend.
