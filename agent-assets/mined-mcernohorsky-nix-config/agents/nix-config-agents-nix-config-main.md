# Agent notes

- Deploy only through the `just` recipes in DEPLOYMENT.md. OrbStack is not a deployment backend.
- Never evaluate `nixosConfigurations.matt-desktop.config` on macOS (many GB of RAM); build it on `matt-desktop`.
- Report `just deploy-desktop`'s reboot warning. If it advises a reboot, you may run `tailscale ssh matt@matt-desktop.tailc41cf5.ts.net sudo reboot`.
- Use `jj` on the single `main` bookmark; no side branches or stashes unless asked. After reviewing `jj status`/`jj diff`: `jj commit -m '…'`, `jj bookmark set main -r @-`, `nix develop -c just sync`, then confirm both hosts report the same `main` and clean working copies.
- Keep Markdown short: DEPLOYMENT.md holds only bootstrap, deploy, and recovery steps. Put rationale in code comments, not docs.
