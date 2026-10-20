---
name: nix-darwin-hermes-deployment
description: Deploy Hermes Agent and local CuaDriver declaratively on a dedicated macOS Studio using a nix-darwin/Home Manager repository, with safe Git, build, secret, and activation verification.
---

# nix-darwin Hermes deployment

Use this skill when a dedicated macOS machine should host Hermes Agent and CuaDriver locally, rather than routing browser control through another machine.

## Target architecture

Prefer:

```text
Hermes Agent on Mac Studio
  -> local cua-driver MCP (stdio)
  -> local CuaDriver daemon
  -> local Chrome
```

A Mac Pro Hermes session connected through SSH/Tailscale is a remote bridge, not the preferred steady-state architecture. Keep it only as a fallback or for remote administration.

## 1. Inspect before editing

1. Load `hermes-agent` when the task concerns Hermes itself; treat the official Hermes docs as authoritative.
2. Inspect the target host, Home Manager profile, and current Git status.
3. Preserve unrelated working-tree changes. Never reset, checkout, or overwrite them.
4. Inspect the existing package source before adding a second Hermes package source. On macOS, the official Hermes Nix support is the flake package/profile workflow; the NixOS service module is Linux-only.
5. Keep secrets out of Git and out of generated config files.

Useful checks:

```bash
git -C ~/darwin status --short --branch
ssh user@studio 'command -v hermes; hermes --version; command -v cua-driver'
```

## 2. Add durable local configuration

Put the non-secret Hermes config under the Darwin repo, typically `files/hermes/config.yaml`, and install it for the Studio Home Manager profile. The MCP entry must use the Studio-local binary, not SSH:

```yaml
mcp_servers:
  cua-driver:
    command: ~/.local/bin/cua-driver
    args: [mcp]
    enabled: true
```

Keep the config minimal and declarative: provider/model defaults, local terminal/browser behavior, and the local MCP server. Do not copy the Pro's session database, browser state, OAuth files, API keys, or `.env` contents.

If an environment file is rendered by activation, make it conditional on the decrypted secret path and use mode `0600`; do not fail the entire Home Manager activation merely because a privileged secret service has not run yet.

## 3. Verify and commit safely

1. Build the exact Studio Darwin target from the Pro/repository checkout before pushing when possible:

```bash
nix build --no-link --fallback '.#darwinConfigurations.<StudioName>.system'
```

2. Stage only the intended Hermes files. Check `git diff --cached --check`.
3. Commit and push the focused change. Leave unrelated changes unstaged.
4. On the Studio, preserve unrelated local modifications (especially `flake.lock`) before pulling. A temporary stash of only the conflicting file is acceptable; restore it immediately after the fast-forward.

## 4. Build and activate on Studio

Run the repository's rebuild wrapper or the equivalent exact target. Distinguish these outcomes:

- **Evaluation/build failure:** the configuration is not deployable yet.
- **Build success, sudo failure:** the system is built but not activated; do not claim deployment complete.
- **Activation success:** verify the installed config, Hermes version, MCP connection, and secret services.

If the full Darwin build is blocked by an unrelated package, a Home Manager activation package can deploy the user-level Hermes config, but this is only partial deployment. Do not call it a complete system rebuild.

## 5. Verify the complete local chain

Run on the Studio:

```bash
readlink ~/.hermes/config.yaml
hermes --version
hermes mcp test cua-driver
```

Expected MCP evidence:

```text
Transport: stdio -> ~/.local/bin/cua-driver
Connected
Tools discovered: 49   # or the current discovered count
```

Then separately verify privileged secret activation without printing values:

```bash
test -r /run/agenix/openrouter-api-key && echo available || echo missing
launchctl print system/org.nixos.activate-agenix
```

Do not infer secret availability from a successful Hermes MCP test; MCP can work while provider credentials and agenix remain unavailable.

## 6. Agenix / SOPS troubleshooting on macOS

Deep identity-path, LaunchDaemon, and path-ownership recipes live in umbrella skill **`sops-nix-ops`** (Modes B + C). Short checklist if `/run/agenix/<secret>` is missing:

1. Confirm encrypted file exists in `secrets/` and recipients include the Studio.
2. Test decryptability to `/dev/null` only; never print plaintext.
3. `launchctl print system/org.nixos.activate-agenix` + inspect `/private/var/run/agenix.d`.
4. A missing host SSH key is not automatically fatal if user age identities decrypt; if decrypt works but the job exits nonzero, fix LaunchDaemon/RAM-disk — do not rotate secrets blindly.

Also see `sops-nix-ops` when app settings under `~/.config` stop sticking after sops-nix templates own the live path.

## Pitfalls

- Do not preserve the Pro->Studio SSH MCP bridge as the final architecture when Hermes can run locally on Studio.
- Do not copy API keys, browser credentials, MFA state, or `.env` contents into `~/darwin`.
- Do not claim a successful rebuild when only `nix build` passed; activation requires privileged sudo.
- Do not remove unrelated profile packages to work around Home Manager collisions without explicit scope.
- Do not treat stale `flake.lock` changes on the Studio as disposable.

## Reference

See `references/macos-hermes-nix.md` for the official macOS Nix support distinction and the Studio-specific verification checklist.
