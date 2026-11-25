# Security Policy

## Scope

This repository ships the **OutSystems MCP integration manifests and skill content** for AI assistant harnesses (Claude Code plugin, Kiro Power, and a generic `SKILL.md` for other harnesses). The actual MCP server is **hosted by OutSystems** and is **not** part of this repo.

Reports are routed differently depending on what you found:

| What you found | Where to report |
|---|---|
| A vulnerability in the manifests, skill content, install snippets, or any other file in **this repository** | GitHub private security advisory on `OutSystems/outsystems-mcp` (see below) |
| A vulnerability in the **hosted MCP server**, the OAuth flow served by OutSystems, the OutSystems platform itself, or any service reachable via the MCP transport | OutSystems Trust Center: <https://www.outsystems.com/trust/> |

If you're unsure which bucket your finding falls into, default to the GitHub private advisory on this repo and we'll route it.

## Reporting a vulnerability in this repository

**Please do not open a public GitHub issue.** Public issues are visible to everyone and can put users at risk before a fix ships.

Use GitHub's private security advisory flow:

1. Go to <https://github.com/OutSystems/outsystems-mcp/security/advisories/new>.
2. Describe the issue, including:
   - The affected file(s) and commit SHA or release version.
   - Reproduction steps.
   - Impact — what an attacker could do, and under what preconditions.
   - Any suggested fix or mitigation, if you have one.
3. Submit. Repository maintainers receive a private notification.

## What to expect

- **Acknowledgment**: we'll confirm receipt as soon as we can, typically within a few business days.
- **Status updates**: we'll keep you posted as the investigation progresses.
- **Fix priority**: driven by severity and impact, on a best-effort basis — critical findings get the fastest turnaround we can manage.
- **Disclosure**: once a fix is released, we publish a GitHub security advisory (with a CVE if applicable). Reporters are credited unless they request anonymity.

## Out of scope

- Issues that require a compromised local machine, a malicious AI assistant harness, or the user pasting an attacker-controlled install snippet. Those are the harness's threat model, not this integration's.
- Findings against third-party dependencies that this repo does not customize. Report those upstream.
- Best-practice opinions, missing rate limits, or non-vulnerability concerns. Open a normal issue or PR instead.

## Supported versions

Only the latest release tagged on `main` receives security fixes. We do not back-port to older plugin or Power versions; bump to the latest version to pick up fixes.
