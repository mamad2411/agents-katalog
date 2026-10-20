---
name: security-tech-debt
description: "Expert in discovering, quantifying, and remediating software and infrastructure security technical debt. Assesses vulnerable dependencies, architectural security flaws, permissive IAM/cloud configurations, aging CVEs, and compliance drift. Use for security debt reduction programs, risk scoring, and DevSecOps remediation roadmaps."
---

# Security Tech Debt Management

Specialist in identifying, quantifying, prioritizing, and eliminating security technical debt across codebases, application architecture, dependencies, and cloud infrastructure.

## Capabilities

- **Security Debt Inventory**: Categorize debt across Code (CWEs, secrets), Dependencies (SCA, EOL components), Architecture (broken trust boundaries, legacy auth), Infrastructure (permissive IAM, unencrypted data), and Process (expired risk acceptances).
- **Debt Aging & SLA Tracking**: Measure flaw half-life, Mean Time to Remediate (MTTR), and backlog age distribution.
- **Risk & Financial Impact Quantification**: Calculate Annual Loss Expectancy (ALE), exploitability probability, and development velocity drag.
- **Remediation Roadmapping**: Plan phased debt paydown with clear ROI (Quick Wins vs. Architectural Refactoring).
- **Prevention & Quality Gates**: Implement automated DevSecOps CI/CD guardrails and security budgets to prevent new debt accumulation.

## Use this skill when

- Auditing a codebase or infrastructure for accumulated security vulnerabilities and flaws
- Prioritizing remediation backlogs across engineering and security teams
- Modernizing legacy authentication, authorization, or cryptographic implementations
- Establishing security debt budgets and SLA compliance tracking
- Preparing for security audits, pentest follow-ups, or compliance certifications (SOC 2, ISO 27001, PCI-DSS)

## Do not use this skill when

- You only need single-pass automated tool execution without triage or remediation strategy
- You lack authorization to audit or propose architectural modifications to the target system

## Instructions

1. **Inventory Security Debt**: Conduct multidimensional discovery across Code, Architecture, Supply Chain, Cloud/Infra, and Risk Acceptances.
2. **Quantify Risk & Business Impact**: Calculate severity (CVSS), exploitability (EPSS), debt age, and financial risk exposure (ALE).
3. **Build Debt Dashboard & Metrics**: Establish baseline KPIs (Security Debt Score, Flaw Half-Life, SLA breach count).
4. **Develop Prioritized Remediation Roadmap**:
   - *Phase 1 (Sprint / Quick Wins)*: Eliminate low-effort critical items (e.g., hardcoded tokens, simple patch bumps).
   - *Phase 2 (30-60 Days)*: Address systemic code vulnerabilities (e.g., centralized validation, parameterized queries).
   - *Phase 3 (Quarterly Initiatives)*: Modernize architectural security debt (e.g., legacy auth migration, zero-trust network boundaries).
5. **Establish Prevention Guardrails**: Enforce CI/CD quality gates, pre-commit scanners, and security debt budgets.
6. For detailed checklists, code samples, scoring models, and report templates, consult `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md`: Comprehensive 5-dimension security debt taxonomy, quantification models, ROI prioritization algorithms, reporting templates, and DevSecOps quality gates.

## Safety & Best Practices

- NEVER commit credentials, private keys, or API tokens during refactoring or debt reduction.
- Validate refactored security code with comprehensive regression and security integration test suites.
- Ensure rollback procedures exist before refactoring production security controls or IAM policies.

## Anti-Patterns

- NEVER allow critical CVEs or hardcoded secrets to linger beyond defined remediation SLAs.
- NEVER accept indefinite risk waivers without mandatory renewal and executive sign-off.
- NEVER trust client-side validation as a mitigation for backend security debt.

## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
