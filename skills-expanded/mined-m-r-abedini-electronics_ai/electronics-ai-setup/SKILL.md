---
name: electronics-ai-setup
description: Install, configure or diagnose the Electronics AI plugin and its Altium Designer connection on Windows without editing designs.
---

# Set up Electronics AI

Resolve the plugin root from this skill's location (two parents above `electronics-ai-setup`). Use the bundled `scripts/plugin_runtime.py` and read [setup commands](../../docs/PLUGIN_PACKAGE.md) when selecting arguments. Dependencies and settings belong in writable per-user data outside the package cache.

Run `doctor` with Python 3.12 to inspect configuration. Before configuration, the launcher exposes only `suite_status`; this proves neither native bridge readiness nor Altium connectivity.

For setup, run `bootstrap --altium-exe <X2.EXE>` with `--library-dir` for intended existing library directories. Bootstrap builds an independent private Python environment and installs the packaged EDA wheel. It configures exactly two backends: EDA and native Python libraries. Re-running bootstrap preserves configured library roots, tool restrictions, timeouts and native workspace identity while preparing a new environment. Altium Designer itself is a separate prerequisite.

The connection and plugin ID is `mcp-electronics-ai`, marketplace `electronics-ai`. Default writable data is `~/.codex/plugins/data/mcp-electronics-ai`; native runtime/workspace are under `%LOCALAPPDATA%/ElectronicsAI`. Use `ELECTRONICS_AI_PLUGIN_DATA` only when an explicit data location is needed. Do not use old plugin IDs, old backend manifests or a second concurrently active connection to the native editor.

Normal `serve` resolves current package code and never installs dependencies or launches Altium. Use `configure-clients --apply` only for clients requested by the user; read [client setup](../../docs/INSTALLER.md) for supported selections. Keep unrelated client settings and a recoverable configuration backup.

After setup, reconnect the plugin, discover `eda__app_context` through `suite_catalog`, and run a read-only `suite_invoke` check when Altium is open and native testing is in scope. Check the installed package version and native script version separately. A successful initialize/list-tools response alone proves catalog readiness, not a working editor. Test a library reader only on an explicit permitted file. A production circuit is not a setup fixture.

Do not clear native ownership markers to force a launch or switch a live editor to another workspace. Report failed initialization with its diagnostic and stop rather than replaying native writes.

For design tasks use `electronics-ai-circuit-design` or `electronics-ai-pcb-layout`. Provider accounts/API access are separate from installation. Optional structural dataset sharing defaults off. Read [native edit safeguards](../../docs/PRODUCT_SAFETY.md) for checkpoints and units, and [autorouting limits](../../docs/AUTOROUTE.md) before router setup; generated SES data does not prove native import or clean DRC.
