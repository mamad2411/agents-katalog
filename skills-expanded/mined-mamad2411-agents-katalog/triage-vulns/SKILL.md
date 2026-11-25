---
name: triage-vulns
description: Triage Snyk findings — classify exploitable / reachable / dev-only, propose upgrade or accept-with-justification, never auto-ignore.
---

# triage-vulns

> Read Snyk findings and classify them by what's actually exploitable in this codebase. Output is per-finding action.

> **MCP binding (read before any tool call):** resolve which server backs `vulnerability_scanner` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.snyk` — when `source` is `host`, the CURRENT host agent's own `snyk` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- A scheduled Snyk scan produced findings.
- A new dependency adds vulnerabilities and the team needs to decide what to do.

## Procedure

1. **Fetch findings** via the snyk MCP (`list_issues`, filtered to the project or target).
2. **For each finding**, classify:
   - **Exploitable + reachable** — patch immediately. The vulnerable function is called from this codebase.
   - **Reachable, not exploitable in our config** — patch in the next routine bump; document.
   - **Unreachable (Snyk reachability says no)** — defer until the next major bump; still upgrade if cheap.
   - **Dev-only / test-only dependency** — patch in routine bumps; CVSS-critical in build tooling still matters for supply-chain risk.
3. **Action per class**:
   - Patch: bump version, run `snyk test` locally, commit.
   - Defer: open a tracking ticket with the finding ID, classification reason, and re-evaluation date (default: 30 days).
   - Accept: only with a documented justification in `.snyk` (the policy file) and an explicit expiration date.
4. **Never auto-`snyk ignore`**. Ignoring without a justification + expiration is how vulns become permanent.

## Output

```text
Snyk triage: refund-service (project ID …)

Critical findings (3):
  - SNYK-JS-LODASH-1234567  package: lodash@4.17.20
    Reachability: REACHABLE (used in src/util/format.ts:42)
    Action: PATCH — upgrade lodash to ≥ 4.17.21 in this PR.

  - SNYK-JS-MINIMIST-2345678  package: minimist@1.2.5 (transitive via gulp)
    Reachability: NOT REACHABLE
    Action: DEFER 30d — track in JIRA-PROJ-1234. Re-check at next gulp bump.

  - SNYK-JS-MARKED-3456789  package: marked@2.0.0 (devDependency)
    Reachability: dev-only
    Action: PATCH in routine bump PR (next week's renovate run).

Acceptance via .snyk: NONE (no findings accepted in this triage).
```

## Quality bar

- Every finding has a class + a concrete action + a date (for defer/accept).
- No vague "we'll look later".
- `.snyk` accept entries are time-boxed.
- The PR that patches a critical finding mentions the SNYK ID in the commit body.

## Anti-patterns to avoid

- "Ignore until next release."
- Bulk `snyk ignore` to clear the noise.
- Accepting a critical "because it's transitive" without confirming non-reachability.

