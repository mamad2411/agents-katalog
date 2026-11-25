---
name: gstack-upgrade
description: Update workflow for this Codex port package. Use when the repo or local skill install should be refreshed and revalidated.
---

# GStack Upgrade

Use this skill when the local Codex port package should be updated, reinstalled, or checked against upstream changes.

This port was reconciled against `garrytan/gstack` at commit
`76535826f5d50c721f95820f300037a3efe833a9`.

## Workflow

1. Identify whether the request is about the repo, the local skill install, or both.
2. Check the installed Codex version and refresh the current official Codex manual before deciding whether a fallback is still needed:
   - `codex --version`
   - `node "${CODEX_HOME:-$HOME/.codex}/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs"`
3. Read the manual sections relevant to the port, usually skills, plugins, MCP, `AGENTS.md`, sandboxing and approvals, hooks, memories, automations, browser behavior, and local/cloud environments.
4. Refresh upstream refs for both `garrytan/gstack` and `garrytan/gbrain` when parity is in scope.
5. Port upstream changes into Codex-native skill files instead of copying Claude-specific preambles.
6. Reinstall or re-link local skills if needed.
7. Run validation and summarize what changed, including the Codex version and any documentation-driven decisions.

## Select the installed channel and host

Resolve the skill path and its backing repository. An upstream checkout can
follow stable releases or main. Inspect its configured channel and version.
An install ahead of stable waits for stable to catch up. Preserve local edits
and use a separate checkout for comparison. The Codex port keeps its own
registry, installer and checks.

Upstream provides a Codex host and model-specific instruction sets called
loadouts. Unknown models use the full set. The measured lite exception for
Opus 5.5 applies only to that model and upstream workflow. Test any smaller
Codex prompt on the same tasks before changing its default.

[Release channels](https://github.com/garrytan/gstack/blob/76535826f5d50c721f95820f300037a3efe833a9/docs/releases.md) · [Loadouts](https://github.com/garrytan/gstack/blob/76535826f5d50c721f95820f300037a3efe833a9/docs/loadouts.md)

## Codex Host Audit

When upstream changed since the last port, explicitly decide which parts are:

- clean to port into `skills/`, `data/`, `docs/`, or `tests/`
- useful locally but not publishable, such as generated `brain/` corpus pages
- blocked on upstream runtime, database, MCP, browser daemon, or Claude-specific behavior

Prefer current Codex install behavior over older Claude Code fallbacks when Codex has a direct equivalent. Keep fallbacks only for host-variable runtimes such as browser automation, upstream `gbrain` CLI availability, and remote credentials.

Record Codex documentation refresh results in `docs/codex-documentation-refresh.md` or the specific runtime/audit doc changed by the upgrade.

## Guardrails

- Do not claim an upgrade succeeded without revalidating the install.
- Be explicit about what was updated and what was left alone.
- Do not move baseline source pins forward if only a subset of upstream changes was ported; use per-skill `source_commit` metadata instead.
- Do not rely on remembered Codex behavior when the current docs can be checked during the port.
