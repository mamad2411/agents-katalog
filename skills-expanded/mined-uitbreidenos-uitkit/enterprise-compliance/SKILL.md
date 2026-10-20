---
name: "enterprise-compliance"
description: "Deploying Claude Code in a regulated industry (finance, healthcare, government); enterprise security review of AI tooling; data residency or sovere..."
---

# Enterprise Claude Code Deployment — Compliance and Security

## When to activate
Deploying Claude Code in a regulated industry (finance, healthcare, government); enterprise security review of AI tooling; data residency or sovereignty requirements; questions about on-premises or private cloud deployment; HIPAA, SOC2, PCI, or FedRAMP compliance requirements.

## When NOT to use
Individual developers or small teams without compliance requirements; standard Claude Code usage with no enterprise data handling constraints; teams that have already completed their compliance review and just need feature help.

## Instructions

**Identity and authentication:**
- Use `ANTHROPIC_WORKSPACE_ID` for workload identity federation — eliminates long-lived API keys from environment variables and CI secrets
- Enterprise SSO via SAML 2.0 or OIDC for team access control (Okta, Azure AD, Google Workspace all supported)
- Rotate API keys quarterly at minimum if workload identity federation is not in use

**Zero Data Retention (ZDR):**
- Available on Enterprise plans
- Prompts and responses are not logged or stored by Anthropic
- Required for HIPAA; required for some PCI DSS scenarios
- Get a signed BAA from Anthropic before sending any PHI — ZDR alone does not constitute a BAA
- Confirm ZDR is active on your workspace before allowing regulated data in sessions

**Network configuration:**
- Claude Code requires outbound HTTPS only — no inbound ports required
- Works behind corporate proxies: set `HTTPS_PROXY` environment variable
- No special firewall rules beyond outbound port 443 to Anthropic endpoints
- For private endpoint deployments, set `ANTHROPIC_BASE_URL` to your Bedrock or Vertex endpoint

**Data residency — use cloud providers for regional processing:**

| Region requirement | Provider and region |
|---|---|
| US only | Direct Anthropic API (us-east-1) or Bedrock us-east-1 |
| EU only | Bedrock eu-west-1 or Vertex AI eu-west-4 |
| APAC | Bedrock ap-northeast-1 |

Direct Anthropic API processes in US data centers only — use Bedrock or Vertex for non-US residency requirements.

**Audit logging:**
All Claude Code tool calls log to `.claude/` session files locally. For SIEM integration:
- Ship logs to Splunk, Datadog, or Elastic via a PostToolUse hook
- Log fields: timestamp, tool name, input summary, exit code, session ID
- Retain logs per your regulatory retention schedule (7 years for most financial regulations)

**Healthcare (HIPAA):**
- ZDR + Bedrock or Vertex required (never direct API for PHI)
- BAA from Anthropic required — obtain before first PHI session
- Deploy Claude Code in a VPC with private endpoints; no public internet egress for PHI-handling sessions
- Never paste PHI into prompts without ZDR confirmed active

**Finance (SOC2/PCI):**
- Secret scanner hook mandatory on all developer sessions (prevent accidental key commits)
- Disable internet access in CI environments running Claude Code
- Audit log all tool calls — at minimum log every file write and shell command
- Code review hook required before any production deploy initiated by Claude Code
- PCI DSS scope: confirm with your QSA whether Claude Code sessions touch cardholder data environments

**Government (FedRAMP):**
- FedRAMP-authorized deployment via AWS GovCloud with Bedrock
- Check current FedRAMP authorization status on the FedRAMP marketplace before procurement — authorization levels and scope change
- GovCloud endpoints require separate API credentials from commercial AWS

**Air-gapped / private network:**
- Claude Code can run entirely against private Bedrock or Vertex endpoints
- Set `ANTHROPIC_BASE_URL` to your private endpoint URL
- All MCP servers referenced in `.claude/mcp.json` must also be reachable without public internet access
- No telemetry or update checks phone home if `ANTHROPIC_BASE_URL` is set to a private endpoint

## Example

Financial services firm deploying to 50 engineers:
- SSO via Okta SAML bound to `ANTHROPIC_WORKSPACE_ID`
- Bedrock eu-west-1 for EU data residency requirement
- `HTTPS_PROXY` set at the org level via IT-managed environment
- Secret scanner hook applied to all sessions via shared `CLAUDE.md` in the monorepo root
- PostToolUse hook ships audit logs to Splunk with session ID and tool name
- ZDR agreement in place; BAA not required (no PHI)
- No direct Anthropic API access — all traffic routes through the private Bedrock endpoint

---
