---
name: opencrawl-setup
description: Resume this plugin's explicitly bound OpenCrawl installation.
---

# Continue this OpenCrawl installation

Read `.opencrawl-binding.json` at this plugin's root. It contains the selected
API origin, CLI command and configuration home, never credentials. Use that
exact command with `OPENCRAWL_CONFIG_HOME` set to its `configHome`, and pass
`--api` with its `api` value. Do not infer a cloud endpoint or choose a default
profile. Missing configuration means installation needs completion in the CLI.

Run `setup status --local --json` first. Preserve saved recording/history choices,
native disabled hooks, completed trust and existing authentication. Use the
normal harness permission review when required; never bypass it or edit trust
records. Resume the CLI's terminal onboarding for unresolved choices.

Use this plugin's native MCP connection at the configured origin plus `/mcp`.
CLI sign-in does not prove native MCP authentication. Call `installation_status`
with the saved installation ID and this client, then `verify_installation` with
its proof ID in this harness. When forward recording is enabled, emit its exact
proof marker once as visible assistant text. Do not repeat it in summaries.
Verify both searchable capture and MCP correlation before reporting completion.
A connection test, installed files and historical imports are not that proof.
Check at most twice, at least 15 seconds apart, then leave pending work visible
and continue normally. Never request an extra user message merely to trigger a
hook. Do not reconstruct unrecorded history or change an opt-out.

Context suggestions default on for clients recording new sessions.
`context-suggestions status` reports effective choices. A suggestion's receipt can be assessed with
`context-suggestions feedback --harness CLIENT --check UUID --rating useful --source agent`.
Other ratings are `irrelevant`, `distracting`, `stale` and `duplicate`; `--result 0`
labels the first snippet. Send feedback only after assessing it. Do not infer
usefulness merely because a suggestion arrived, and do not report an agent
assessment as a user judgment.

For Codex, read `setup hooks --json` before requesting trust again. That inspects
this exact plugin's current native trust; an older server hookTrust value is not
current evidence. If the inspection shows all hooks trusted and none disabled,
do not repeat completed review. Never inspect another client's trust records.
Read the native MCP configuration in this bundle: Codex uses `pluginName` from
the binding as its server key; other personal harnesses use the plugin's own
`opencrawl` server. Preserve manual connections and other deployments, and never
substitute them for this installation's verification.

Compare local effective recording choices with `installation_status` first.
If they disagree, preserve local opt-outs and resume normally authorized CLI
reconciliation before following a stale capture task. For forward=true, require
both proof.state=verified and mcp.state=authenticated. For an existing
forward=false installation, proof.state=not_selected with mcp.state=observed is
sufficient; do not enable recording to obtain proof. Preserve skipped history.
If CLI network access is unavailable, the authenticated native MCP verification
path remains usable; do not reinstall, copy tokens or weaken sandbox policy.

For Devin Cloud, startup uses renewable workload identity. Do not run interactive
terminal setup or human browser login. Preserve the startup error, repair the
official provider helper or organization binding, then resume that Cloud session.
Never claim capture for a first turn whose native startup hook did not run.
