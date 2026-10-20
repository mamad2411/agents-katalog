---
name: agentic-development-security-ads
description: Implement Forrester's Agentic Development Security (ADS) framework to protect AI-powered software development end to end. Covers the four pillars (Prevent, Detect, Prioritize, Remediate), the eight capability clusters, agent-introduced vulnerability patterns with empirical rates (12-45%), slopsquatting and hallucinated dependency attacks, MCP server compromise, rules-file backdoors, agent identity and runtime accountability, the ADS maturity model, and a phased build-from-scratch playbook. Use when deploying AI coding agents at scale, building security review pipelines for agent-generated code, addressing the scale mismatch between agent output and security review capacity, or designing agent identity and provenance infrastructure. NOT for agentic commerce payment security (use agentic-payments-compliance-2026) or general agent supply chain exploit response (use agentic-supply-chain-exploit-defense).
---

# Agentic Development Security (ADS)

## Overview

AI coding agents now generate roughly 27% of all production code (DX Q1 2026), and teams with high AI adoption merge 98% more pull requests — but PR review time increased 91% (Faros AI). Empirical studies document security flaw rates from 12% to 45% of AI-generated code depending on methodology. Traditional AppSec tools, designed for human-paced development, cannot keep up. Forrester's Agentic Development Security (ADS) category, introduced at RSAC 2026, defines a new operating model where security decisions are autonomous, policy-driven, and continuous across code, dependencies, workflows, and running applications.

## When to Use

- Deploying AI coding agents (Claude Code, Copilot, Cursor, etc.) at team or organizational scale
- Building security review pipelines that can handle agent-generated code volume
- Addressing the scale mismatch: code generation outpacing security review capacity
- Designing agent identity, provenance tracking, and runtime accountability infrastructure
- Responding to AI-specific supply chain threats (slopsquatting, hallucinated dependencies, MCP compromise)
- Establishing governance policies for agent permissions, tool access, and human-in-the-loop checkpoints
- Evaluating or selecting ADS tooling across the eight capability clusters

NOT for:
- Agentic commerce payment security and compliance — use `agentic-payments-compliance-2026`
- General agent supply chain exploit response and incident handling — use `agentic-supply-chain-exploit-defense`
- Agent trust/authentication protocols (Visa TAP, FIDO, KYA) — use `agentic-trust-security-protocols-2026`
- MCP server security architecture — use `mcp-security-trust`

## Core Process / Workflow

### Step 1: Understand Why Traditional AppSec Breaks

Traditional application security assumes code moves through a sequential pipeline at human speed. AI coding agents violate every assumption simultaneously.

| Failure Mode | Core Mechanism | Tool Category That Fails |
|--------------|-----------------|---------------------------|
| Scale mismatch | Code volume grows faster than review capacity | All tools requiring human triage |
| High baseline vulnerability rates | AI code contains flaws at documented rates across studies | Relies on developer judgment that empirically fails |
| SAST context blindness | Text-based analysis cannot evaluate architectural correctness | SAST |
| SCA hallucination gap | Phantom packages undetectable before manifest commitment | SCA |
| Non-determinism defeats signatures | Same prompt produces different code; rules cannot generalize | SAST signature-based rules |
| Provenance and context loss | No tracking of AI authorship; positionally wrong code | SAST, DAST, code review |
| Fragmented stack correlation gap | Isolated tool reports cannot surface compound AI risk | All tools in isolation |
| Agentic privileged actor risk | Agents operate with developer-level access | No existing tool category |

**The arithmetic problem:** If you're generating code 10x faster and your security team isn't getting 10x faster, you're accumulating risk. AI-generated code accounts for ~27% of production code (DX Q1 2026), and teams with high AI adoption merge 98% more PRs with 91% more review time (Faros AI, 10,000+ developers).

### Step 2: Understand ADS — Forrester's New Category

**Forrester's formal definition:** ADS is "a new security paradigm focused on protecting AI-powered software development from end to end." It spans prevention, detection, prioritization, and remediation while providing continuous intelligence across code, dependencies, workflows, and running applications. Security decisions are autonomous, policy-driven actions — not alerts handed to overburdened teams.

**Three converging forces that made ADS necessary:**
1. **Detection commoditization** — SAST, DAST, SCA, secrets scanning are now table stakes. Leaders differentiate through correlation with real-world context (exploitability, reachability, runtime exposure, business impact).
2. **LLMs reshaping security reasoning** — LLMs excel at correlating disparate data sources into coherent insights. Value shifts from detection volume to understanding and action.
3. **Agentic development generating insecure code at scale** — AI agents commonly ship unauthenticated endpoints, trust client-supplied data for security-critical decisions, and omit basic controls (input validation, rate limiting, server-side checks).

### Step 3: Apply the Four ADS Pillars

#### Pillar 1: Prevent

Stop insecure AI-generated code from entering the codebase, with controls at or before the point of code generation.

**Key controls:**
- **Provenance tracking of AI-generated code:** Mandate tracking of which code was AI-generated, which model produced it, and with what parameters (NIST SP 1800-44A)
- **Real-time IDE/editor scanning:** Integrated with AI coding tools, identifying insecure patterns and recommending secure alternatives before code reaches staging
- **Security review gates on agent-suggested PRs** for critical code areas
- **Model, modification, and annotation traceability** throughout development

**Defense-in-depth placement:** Provenance tracking at commit time, IDE scanning during code generation, review gates at PR submission.

#### Pillar 2: Detect

Identify vulnerabilities and anomalous behaviors in AI-generated code at both code level and runtime, including AI-specific vulnerability classes that traditional scanning misses entirely.

**SAST/DAST/API Security/SCA remain necessary as baseline** but ADS-specific detection adds:
- AI-aware dependency scanning capable of detecting hallucinated and slopsquatted packages not yet in manifests
- Runtime behavioral monitoring of agent actions across the development environment
- Continuous visibility into code execution paths and material changes across the SDLC
- OWASP AIVSS scoring for AI agent-specific risk quantification
- Prompt injection and excessive agency detection per the OWASP agentic risks taxonomy

#### Pillar 3: Prioritize

Risk-rank vulnerabilities so security teams focus on findings that are exploitable and material, given the volume AI-scale code generation produces.

- OWASP AIVSS v0.8 for risk quantification and mitigation prioritization
- ASPM platforms correlating findings across SAST, SCA, DAST, and runtime data
- Execution authority analysis: what code runs, why it runs, how authority is applied
- Context-aware risk scoring distinguishing AI-generated from human-authored code

**Critical dependency:** Context-aware risk scoring requires reliable provenance metadata. Until provenance tracking matures, use explicit tagging policies enforced at commit time rather than automated classification after the fact.

#### Pillar 4: Remediate

Replace manual developer effort with autonomous agentic fix generation including self-validation loops.

- Autonomous agentic fix generation with static analysis and integration checks validating the fix itself
- Agent-as-reviewer loops: a second agent evaluates the first agent's output against the original finding
- Human escalation points at defined risk thresholds (required architectural control)
- Near-real-time identify-fix-test-deploy loops
- Traceability of model, modifications, and annotations

### Step 4: Map Agent-Introduced Vulnerability Patterns

AI coding agents introduce specific, measurable vulnerability patterns — not random bugs. Multiple independent studies document with CWE-level precision.

**Measured vulnerability rates across studies:**

| Study | Methodology | Finding |
|-------|-------------|---------|
| Veracode | 80 tasks across 100+ LLMs | 45% of AI-generated code contains security flaws; Java worst at 72% |
| Schreiber & Tippe | 7,703 files from public GitHub repos, CodeQL | 12.1% of AI-generated files contain ≥1 CWE-mapped vulnerability |
| Pearce baseline | GitHub Copilot, security-relevant scenarios | ~40% vulnerable output |
| Liu et al. | 31,132 AI agent skills analyzed | 26.1% contain ≥1 security vulnerability |

**Dominant vulnerability patterns by CWE:**

| Pattern | CWEs | Mechanism |
|---------|------|-----------|
| Injection flaws | CWE-89, 78, 94, 79 | Highest average CVSS scores; SQL injection, OS command injection, code injection. Snyk: Copilot draws on insecure context from surrounding codebase, replicating and amplifying existing insecure patterns. |
| Hardcoded secrets | CWE-259, 798, 532 | AI-assisted code leaked secrets at ~2x GitHub baseline (GitGuardian 2026). Claude Code commits: 3.2% secret-leak rate vs 1.5% baseline. 28.65M new hardcoded secrets pushed to public GitHub in 2025 (+34% YoY). AI service credential leaks: 1.28M (+81% in one year). |
| Missing security controls | CWE-307, 306, 400 | Agents omit defensive controls. CWE-307 in 5.91% of ChatGPT JS output. CWE-400 in 7.00%. Tenzai: every app built with 5 major AI coding tools lacked CSRF protection, security headers, and contained SSRF vulnerabilities. |

**The false confidence multiplier:** 56.4% of developers frequently encounter security issues in AI-generated code, yet 80% still bypass their organization's AI code security policies. 80% believe AI tools generate more secure code — directly contradicting empirical findings. ADS treats this confidence gap as first-order risk.

### Step 5: Defend Against AI-Specific Supply Chain Attacks

#### Slopsquatting: Hallucinated Package Exploitation

Coined by Seth Larson. Attackers register package names that LLMs predictably hallucinate. Unlike typosquatting (exploits human typing errors), slopsquatting exploits model-specific errors that are predictable and repeatable.

**USENIX Security 2025 finding:** 45% of hallucinated package names are consistently regenerated every time the model is queried with the same prompt; ~60% reappear at least once across 10 subsequent queries. Attackers identify which fictitious names a model reliably suggests, register them, and position malicious packages for auto-installation.

**Documented incident (Jan 2025):** Google's AI Overview recommended @async-mutex/mutex, which typosquatted the legitimate async-mutex library. The package stole Solana private keys and exfiltrated them via Gmail SMTP.

**Detection gap:** No existing tooling validates AI-recommended packages at the point of selection. SCA tools scan manifests for known-vulnerable packages — they cannot intercept a hallucinated dependency before it's committed.

#### MCP Server Compromise

The MCP ecosystem resembles npm in 2015: rapidly growing, predominantly built by individual developers, minimally governed.

- ~75% of MCP servers built by individual developers (Endor Labs)
- ~40% lack license information
- ~82% interact with sensitive APIs requiring careful access controls
- **First documented malicious MCP server (Sep 2025):** npm package `postmark-mcp` impersonated Postmark, operated as functional email MCP server through 15 versions, then added a one-line backdoor in v1.0.16 that BCCed every message to an attacker-controlled address

#### Rules File Backdoor

Attackers embed malicious instructions into AI coding tool configuration files (`.cursorrules`). Agents consuming these files inject embedded malware into projects automatically. The same technique can steer agent dependency selection toward attacker-controlled packages — a vector no package manager or SCA tool inspects.

### Step 6: Build Runtime Accountability Infrastructure

Accountability for AI-generated code changes remains an unresolved problem. ADS requires binding agent identity to code output.

**Three interlocking components:**
1. **Agent identity** — Treat AI agents as distinct, first-class identity principals with credentials, permissions, and audit trails separate from human users (NCCoE concept paper)
2. **Code attribution** — Bind every commit, PR, or artifact to the agent that produced it with cryptographic verifiability
3. **Provenance tracking** — Tamper-evident record of who did what, when, and why across the entire supply chain including AI-generated steps

**The emerging technical stack:**

| Layer | Standards/Tools |
|-------|-----------------|
| 4: Policy Enforcement | in-toto layout policies, SLSA levels |
| 3: Provenance Attestation | in-toto Attestation Framework, SLSA provenance schema |
| 2: Cryptographic Signing | Sigstore (Cosign + Rekor transparency log) |
| 1: Agent Identity | SPIFFE/SPIRE, OIDC tokens, OpenID Foundation spec |
| 0: Regulatory Baseline | NIST SSDF, NCCoE concept paper |

**The gap:** Most agents commit code under the invoking developer's identity rather than their own. Unless organizations implement dedicated agent service accounts, SLSA authentication requirements remain unmet for AI-generated changes. Current in-toto implementations assume functionaries are deterministic build tools, not probabilistic models — adapting requires policy definitions that validate output properties rather than exact reproducibility.

**The identity-to-behavior gap (RSAC 2026):** Five vendors shipped agent identity frameworks, but they focused on tracking agent identity rather than what the agent actually did. Full accountability requires binding identity to behavior: which agent generated which code, under which instructions, with what tool access, and whether output matched declared intent.

### Step 7: Build an ADS Practice from Scratch

#### Phase 0: Current State Assessment (Weeks 1–4)

1. **Agent discovery:** Full inventory of all AI agents in the development environment. Capture which agents exist, what credentials they run with, what tools/APIs they can call, who owns them. Governance rules must be centralized.
2. **Threat model against OWASP Agentic Risks:** Map each agent against OWASP AIVSS. Prioritize immediate actions: tool scoping, credential isolation, audit trail verification.
3. **SSDF gap analysis:** Use NIST SP 800-218A as a checklist against current secure development practices.

#### Phase 1: Policy Development (Weeks 4–8)

Five policies form the minimum viable ADS governance layer:

1. **Least agency / minimum permissions:** Agents receive only the minimum permissions, capabilities, tools, and decision-making authority necessary for a specific task (Forrester AEGIS core control). Documented failure: Amazon's internal AI tool Kiro caused a 13-hour production outage by deleting and recreating a production environment.
2. **Human-in-the-loop checkpoints:** Classify which agent actions require human approval:
   - Routine changes (formatting, docs, tests): auto-approved with logging
   - Refactoring and isolated bug fixes: AI-approved with logging
   - New features and business logic: human review required
   - Security and infrastructure changes: mandatory human review before execution
3. **Agent identity policy:** Each agent gets a non-human identity (dedicated service account). Credentials not shared with human accounts. Agent identity captured in all audit trails.
4. **MCP and tool integration policy:** Any MCP server or external tool integration must pass security review before agents are permitted to use it.
5. **AI SBOM policy:** Adopt SPDX 3.0 for AI-aware Software Bills of Materials.

#### Phase 2: Tooling Selection (Weeks 6–12)

No single vendor covers all ADS capabilities. Prioritize in this order for limited budgets:

| Priority | Category | Purpose | Examples |
|----------|----------|---------|----------|
| Start here | Agent identity & access management | Scope credentials, audit logs, SSO | GitHub Copilot Enterprise, Claude Code (audit on paid plans) |
| Phase 1 | SAST with AI awareness | Detect AI-specific vulnerability patterns | Checkmarx, Snyk |
| Phase 1 | Observability & audit logging | Agent monitoring with KPIs (MTTD <5min, MTTR <15min, coverage 100%) | — |
| Phase 2 | Agentic AI security platforms | Discovery, red teaming, runtime protection, guardrails | Geordie AI, Sysdig, Realm Labs |
| Phase 2 | Policy-as-code in CI/CD | Automated compliance enforcement | AWS AIRI, Microsoft AI compliance rules |
| Phase 3 | Validation pipelines | Multi-layer verification of agent output | — |

**Selection criteria for any tool:** (1) Does it distinguish AI-generated from human-authored code? (2) Does it integrate with existing CI/CD without workflow redesign? (3) Does it provide API-level audit logging capturing agent identity? Tools that can't answer yes to at least two of three will create governance gaps.

#### Phase 3: Workflow Integration (Weeks 10–16)

1. **Centralize agent configuration:** One security engineer can disable a tool in one place, automatically disabled across all agents. Centralized revocation is a prerequisite for expanding autonomy.
2. **Integrate agentic security into threat modeling:** OWASP agentic guide as required checklist for any PR introducing or modifying agent capabilities.
3. **Adopt spec-driven development for agent tasks:** Require written specifications for any agent task touching security-critical code paths (authentication, authorization, payment processing, PII handling). Expand to all agent tasks once spec review discipline is established.

### Step 8: Assess ADS Maturity

| Stage | Characteristics | Key Indicator |
|-------|----------------|---------------|
| Ad Hoc | Agents deployed by individuals with personal credentials; no inventory; no audit trail | No agent in any security/infrastructure inventory |
| Defined | Agent inventory maintained; written policies for least agency, human-in-loop, agent identity; basic audit logging | Policy Pass Rate measurable; Agent Inventory complete |
| Managed | Centralized agent configuration; tool registry with revocation; validation pipelines blocking non-compliant outputs | Agent Coverage at 100% under monitoring |
| Optimized | AI red team running periodic tests; policy-as-code in CI/CD; NIST AI RMF compliance documented | Automated evaluation against compliance requirements |
| Autonomous-Safe | Agent identities with verified credentials; SLSA-level provenance for AI-generated code; continuous automated evaluation | Automated compliance reporting capabilities |

**Note:** Maturity is not always linear — a single incident (like the Kiro production outage) can force regression. Assess maturity per agent category rather than organization-wide. A team's CI/CD agents may be at Managed while IDE coding agents remain at Ad Hoc.

## A-Tech Applications

### A-Coder (IDE)
- Embed security-first architecture by default: SBOM generation, dependency scanning, vulnerability alerts in the IDE
- Agent provenance tracking: every AI-generated change tagged with model, parameters, and agent identity
- Real-time security scanning integrated with agent suggestions, recommending secure alternatives before code reaches staging
- Spec-driven development enforcement for security-critical code paths
- Agent-as-reviewer loops: a verification agent validates implementation against the spec before surfacing to developer

### Be Practical (Playbooks)
- Mandatory security chapter in all playbooks: "Secure by Default with AI Agents"
- Module: "The False Confidence Multiplier" — why 80% of developers think AI generates secure code when it doesn't
- Module: "Slopsquatting and Hallucinated Dependencies" — how to defend against AI-specific supply chain attacks
- Module: "Agent Identity and Provenance" — binding code to agent identity for accountability
- The ADS maturity model as a self-assessment tool for Builder's Club members

### Builder's Club (Community)
- Security audit track for community MCP servers (addressing the 75% individually-built, 40% unlicensed, 82% sensitive-API problem)
- Bug bounty program for agent-generated code vulnerabilities
- Security certification for members demonstrating ADS maturity
- Open-source slopsquatting detection tools: community-maintained databases of known hallucinated package names per model
- AI SBOM generation toolkit: open-source SPDX 3.0 templates for agent-built projects
- Red team exercises: community-led AI security testing events

## Cross-Skill Connections

- `agentic-supply-chain-exploit-defense` — Q1 2026 exploit landscape and incident response (this skill provides the systematic ADS framework that prevents those incidents)
- `agentic-trust-security-protocols-2026` — Agent authentication and trust protocols (Visa TAP, FIDO, KYA); this skill is the development-security layer
- `mcp-security-trust` — MCP server security architecture; this skill provides the governance framework for MCP at scale
- `vibe-coding-security-defense` — Vibe coding security risks; this skill is the enterprise-scale framework
- `supply-chain-agentic-security` — Supply chain security for agentic systems; this skill adds the Forrester ADS operating model
- `agentic-coding-trends-2026` — Trend 8 dual-use risk; this skill operationalizes the security-first architecture recommendation
- `code-health-mcp-integration` — Code health monitoring via MCP; this skill adds the security dimension
- `ai-code-provenance-generative-authorship` — Provenance and authorship tracking; this skill provides the security framework that makes provenance actionable

## References

- See [references/vulnerability-patterns-and-supply-chain.md](references/vulnerability-patterns-and-supply-chain.md) for the complete empirical vulnerability rate data, CWE-level taxonomy, slopsquatting attack analysis, MCP compromise case studies, and rules-file backdoor patterns.
- See [references/ads-implementation-playbook.md](references/ads-implementation-playbook.md) for the phased build-from-scratch playbook, tooling selection matrices, policy templates, agent identity technical stack details, and the maturity model assessment framework.