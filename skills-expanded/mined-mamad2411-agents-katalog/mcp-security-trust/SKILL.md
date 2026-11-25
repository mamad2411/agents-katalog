---
name: mcp-security-trust
description: Secure and trust MCP server ecosystems against real-world attack vectors. Covers authentication gaps, supply-chain risks, mandate signing, and the three-tier server quality hierarchy. Use when deploying, publishing, or consuming MCP servers in production environments.
---

# MCP Security & Trust

## Overview

The Model Context Protocol ecosystem has grown to over 10,000 public servers and 97 million monthly SDK downloads by late 2025. This explosive growth has exposed a critical trust gap: 53% of community MCP servers rely on static API keys or long-lived Personal Access Tokens, over 1,800 servers run without any authentication, and the September 2025 Postmark MCP server compromise proved that supply-chain attacks on agent infrastructure are already happening.

For A-Tech, which champions open-source AI and user sovereignty, MCP security is not just a technical concern—it is a trust architecture problem. Every unauthenticated server that an A-Coder plugin connects to, every static credential in a community MCP server, and every unaudited tool invocation undermines the privacy-first promise.

## The Three-Tier Server Quality Hierarchy

By early 2026, the MCP ecosystem has stratified into three distinct quality tiers:

| Tier | Builder | Authentication | Maintenance | Trust Level |
|------|---------|---------------|-------------|-------------|
| **Class A** | Vendor-backed (AWS, GitHub, Stripe, Salesforce) | OAuth 2.0 / mTLS / short-lived tokens | Predictable update cycles, SLA | Enterprise-grade |
| **Class B** | Community / volunteer | Static API keys (53%), no auth (~18%), PATs | Sporadic, unmaintained | Fragile commons |
| **Class C** | Internal organizational | Varies by org maturity | Hidden from public directories | Unknown |

The quality gap between Class A and Class B is structural, not incidental. The absence of a sustainable business model for community servers leads to minimal security investment, creating what researchers call a "fragile commons" problem.

## Real-World Attack: The Postmark Server Compromise (September 2025)

An unofficial Postmark MCP server with 1,500 weekly downloads was covertly modified to add a blind carbon copy field to its email-sending function, silently routing a copy of every outbound message to an attacker's address.

**Why it matters:**
- Users had no indication anything changed
- The server appeared in public registries without distinction from official vendor servers
- AI agents, not just humans, were invoking the compromised tool
- The incident illustrates that agent infrastructure trust is not yet matched by verification mechanisms

## Core Security Risks

### 1. Authentication Gaps
- 53% of community servers use static API keys or PATs
- Only 8.5% implement modern OAuth
- 1,800+ servers have no authentication whatsoever
- Long-lived credentials are rarely rotated

### 2. Supply-Chain Attacks
- Community servers can be modified without user notification
- No mandatory code signing or checksum verification in most registries
- AI agents may silently invoke updated server versions
- Registry curation is minimal or absent

### 3. Agent-Specific Threats
- AI agents trigger hundreds of requests per session, making anomaly detection harder
- Agents can chain multiple tool calls, amplifying blast radius of a compromise
- Agents operate without human supervision for extended periods
- Traditional API monitoring assumes human pacing, which agent traffic violates

### 4. Data Exfiltration Vectors
- MCP servers with file-system access can read sensitive codebases
- Servers with network access can make unauthorized external calls
- Servers with database access can query or modify production data
- Composite workflows across multiple servers create unexpected data flows

## The Trust Architecture for A-Tech

### Principle 1: Verified Server Directory
Maintain a curated directory of MCP servers that A-Coder and Builder's Club tools are permitted to connect to, with explicit trust levels.

| Trust Badge | Meaning | Requirement |
|-------------|---------|-------------|
| **Gold** | Vendor-backed, enterprise-grade | OAuth 2.0, SOC 2, public audit |
| **Silver** | Community-audited, actively maintained | Code signing, CI/CD, 2+ maintainers |
| **Bronze** | Experimental, use with caution | Basic auth, single maintainer, no audit |
| **Blocked** | Known security risk | Compromised, unmaintained, or malicious |

### Principle 2: Mandate-Based Authorization
For paid or sensitive MCP servers, use AP2-style cryptographic mandates:
- Human signs an Intent Mandate authorizing specific spending and scope
- Every agent invocation carries a signed, auditable Cart Mandate
- Settlement generates a Payment Mandate with full traceability
- Users can revoke mandates instantly

### Principle 3: Least-Privilege Sandboxing
- MCP servers run in isolated sandboxes with explicit capability declarations
- File-system access is read-only by default; writes require explicit grant
- Network egress is denied by default; allowed destinations are allow-listed
- Credential access is scoped to the minimum required permissions

### Principle 4: Continuous Attestation
- Servers must publish a Software Bill of Materials (SBOM)
- Automated vulnerability scanning on every registry update
- Community security audits for Silver-tier servers
- Real-time anomaly detection on invocation patterns

## Implementation Checklist

### For MCP Server Publishers
- [ ] Implement OAuth 2.0 or mTLS authentication (not static keys)
- [ ] Publish SBOM and sign releases with cosign or Sigstore
- [ ] Declare capabilities explicitly; request minimum permissions
- [ ] Set up automated dependency vulnerability scanning
- [ ] Maintain a security contact and publish a security policy
- [ ] Enable reproducible builds and CI/CD transparency
- [ ] Participate in community audit programs

### For MCP Consumers (A-Coder / Builder's Club)
- [ ] Maintain a verified server directory with trust badges
- [ ] Default to local / self-hosted MCP servers for sensitive workflows
- [ ] Require human approval before connecting to Bronze-tier servers
- [ ] Implement invocation logging and anomaly detection
- [ ] Enforce least-privilege sandboxing on all server connections
- [ ] Block servers with known vulnerabilities or compromise history
- [ ] Provide users with transparent visibility into all active server connections

### For Agent Developers
- [ ] Design agents to request explicit human confirmation for high-risk tool chains
- [ ] Implement circuit breakers when server behavior deviates from baseline
- [ ] Log every tool invocation with full parameter and response metadata
- [ ] Support mandate-based authorization for paid or sensitive operations
- [ ] Alert users when a server's trust tier changes or a new version is published
- [ ] Default to read-only capabilities; escalate only with explicit user grant

## A-Tech Application

### A-Coder (IDE)
- **Verified Plugin Directory:** All MCP-based plugins are classified Gold/Silver/Bronze/Blocked
- **Local-First Default:** Self-hosted MCP servers run on the user's machine by default
- **Trust Dashboard:** Users see every active MCP connection, its permissions, and its audit status
- **Approval Gates:** Bronze-tier servers require explicit user confirmation on every session start
- **Privacy Seals:** Servers that process code locally without cloud egress receive a privacy seal

### Be Practical (Book / Playbooks)
- Chapter: "Securing the Agent Supply Chain"
- Playbook: "MCP Server Security Audit Checklist"
- Case study: How the Postmark compromise could have been prevented
- Template: "Trust Badge System" for open-source MCP registries

### Open Source AI Builder's Club
- **Security Audit Track:** Community-led security reviews of member-published MCP servers
- **Bug Bounty Program:** Rewards for discovering vulnerabilities in Club-published servers
- **Security Certification:** Members can earn a "Security Verified" badge for their servers
- **Open Registry:** Transparent, community-curated registry with full audit history
- **Best Practices Repository:** Reference implementations of secure MCP server patterns

## Key Metrics

| Metric | Target | Why It Matters |
|--------|--------|--------------|
| Gold-tier server coverage | 100% of paid integrations | Revenue depends on trust |
| Silver-tier audit rate | >50% of community servers annually | Community health |
| Bronze-tier approval rate | <10% of active sessions | Reduce exposure to risk |
| Local-first adoption | >80% of sensitive-code workflows | Privacy preservation |
| Security incident response | <24 hours from disclosure to block | Protect users |
| SBOM publication rate | 100% of registry entries | Supply-chain transparency |

## Ethical Framework

### Transparency Over Obscurity
- All security findings are disclosed publicly (responsible disclosure timeline)
- Users are notified immediately when a server they use is downgraded or blocked
- Security audit reports are open and community-reviewable

### User Sovereignty
- Users control which servers their agents can connect to
- No silent updates to server trust tiers without user notification
- Local execution is always an available option

### Collective Defense
- Security intelligence is shared across the open-source MCP community
- Vulnerability patterns are documented as public knowledge, not proprietary secrets
- Community-driven standards outpace individual vendor efforts

## References
- Astrix Security — "State of MCP Server Security 2025" (research data on auth gaps and incidents)
- Gary Weiss / MCP-Server Medium — "The Rise of MCP: Protocol Adoption in 2026" (Postmark compromise details)
- arXiv — "Securing the Model Context Protocol" (academic threat analysis)
- Linux Foundation / Agentic AI Foundation — MCP governance and donation timeline

## Date Researched
2026-05-31 | Daily Research Process | A-Tech Research Division
