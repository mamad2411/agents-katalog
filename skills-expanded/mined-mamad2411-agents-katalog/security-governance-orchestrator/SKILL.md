---
name: "security-governance-orchestrator"
description: "Orchestrates end-to-end security governance for any repository: audits, compliance, threat modeling, vulnerability scanning, Architectural Decision Records (ADRs), supply chain & cryptographic governance (SBOM/CBOM), and GitHub security CI/CD integration."
version: 2
created: "2026-07-31"
updated: "2026-09-27"
---

## When to Use

Use this skill to establish, audit, or enforce complete security governance across any repository. Trigger when:
- Onboarding a new repository to organizational security and compliance standards.
- Conducting comprehensive security audits, threat models, or compliance readiness checks.
- Codifying security designs, cryptographic choices, or risk acceptances as Architectural Decision Records (ADRs).
- Implementing automated GitHub security pipelines (SAST, secret scanning, Dependabot, SARIF uploads, and branch protections).
- Reviewing high-risk PRs for architectural security impact.

---

## Bundled Templates & Scripts

This skill provides cross-platform Python scripts and native PowerShell ports for Windows:
- **Security ADR Template**: [Security_ADR_Template.md](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/Security_ADR_Template.md) — Specialized SecADR template with threat model context, STRIDE tags, CIA triad impact, and residual risk tracking.
- **GitHub Actions Workflow**: [security-governance.yml](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/security-governance.yml) — Starter CI workflow for secret scanning (Gitleaks), SAST (Semgrep), dependency scanning (Trivy), and an ADR gatekeeper check with SARIF uploads.
- **Dependabot Configuration**: [dependabot.yml](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/dependabot.yml) — Standard Dependabot configuration with the required 7-day security cooldown for multiple ecosystems.
- **Repository Initializers**:
  - Python (Cross-platform): [init_security_governance.py](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/scripts/init_security_governance.py)
  - PowerShell (Windows): [init-security-governance.ps1](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/scripts/init-security-governance.ps1)
- **ADR Security Gatekeeper**:
  - Python (Cross-platform): [adr_security_gatekeeper.py](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/scripts/adr_security_gatekeeper.py)
  - PowerShell (Windows): [adr-security-gatekeeper.ps1](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/scripts/adr-security-gatekeeper.ps1)
- **Pre-Commit Git Hooks**:
  - Python: [pre_commit.py](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/pre_commit.py)
  - PowerShell: [pre-commit.ps1](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/pre-commit.ps1)
  - Windows Batch launcher: [pre-commit.bat](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/pre-commit.bat)
  - Unix Bash launcher: [pre-commit.sh](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/pre-commit.sh)

---

## Execution Modes

1. **Full Repo Security Onboarding / Complete Audit**: Executes Phases 1 through 6 to establish full security posture, ADR documentation, and GitHub automation.
   - **Linux / macOS**:
     ```bash
     python3 /Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/scripts/init_security_governance.py <repo_path>
     ```
   - **Windows (PowerShell)**:
     ```powershell
     powershell -File C:\Users\<user>\.gemini\config\skills\security-governance-orchestrator\scripts\init-security-governance.ps1 -TargetDir <repo_path>
     ```
2. **PR / Pre-Merge Gatekeeper**: Focuses on Phase 3 (ADR check) and Phase 5 (GitHub PR security checks & secret scanning).
   - Python: `python3 scripts/adr_security_gatekeeper.py --base origin/main`
   - Windows PowerShell: `.\scripts\adr-security-gatekeeper.ps1 -Base "origin/main"`
3. **Threat Modeling & Architectural Review**: Focuses on Phase 1, Phase 2, and Phase 3 to evaluate new system components or auth architectures.

---

## Step-by-Step Procedure

### Phase 1: Repository Profiling & Security Baseline Discovery
1. Identify repository tech stack, languages, framework versions, package managers, and existing CI/CD setups.
2. Run `security-auditor` and `security-compliance-compliance-check` to evaluate current controls against baseline standards (OWASP Top 10, SOC2, CIS).
3. Inspect `docs/adr/` via `adr-discovery` to catalog existing architectural assumptions, cryptographic choices, and accepted technical debt.

### Phase 2: Threat Modeling & Security Architecture
1. Map trust boundaries, external interfaces, and sensitive data flows.
2. Execute STRIDE threat analysis using `threat-modeling-expert` and `stride-analysis-patterns`.
3. Construct attack scenarios with `attack-tree-construction`.
4. Derive concrete mitigations and security user stories using `threat-mitigation-mapping` and `security-requirement-extraction`.

### Phase 3: Architectural Decision Recording (ADR Integration)
1. Evaluate architectural significance of identified risks and mitigations using `adr-discovery`.
2. For any significant architectural change (e.g., auth provider changes, encryption schemes, zero-trust network boundaries, accepted risk exceptions), draft a Security ADR using `adr-authoring`:
   - Use [Security_ADR_Template.md](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/Security_ADR_Template.md) or the Comprehensive ADR Template in `adr-templates`.
   - Ensure the *Threat Context*, *Residual Risk*, and *Compliance Traceability* sections are fully documented.
3. Update the ADR index table in `docs/adr/README.md` and manage statuses using `adr-lifecycle-management`.
4. Run `install-adr-gatekeeper` or deploy the bundled [security-governance.yml](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/security-governance.yml) to enforce ADR compliance on future PRs.

### Phase 4: Vulnerability & SAST Scanning
1. Execute multi-language SAST using `security-scanning-security-sast` (Semgrep, Bandit for Python, ESLint Security for JS/TS, CodeQL).
2. Scan dependencies and container images for known CVEs using `security-scanning-security-dependencies` and `secrets-management`.
3. Evaluate infrastructure-as-code and cloud configurations with `security-scanning-security-hardening`.
4. Inventory and audit Software Bill of Materials (SBOM) and Cryptographic Bill of Materials (CBOM) for Post-Quantum Cryptography (PQC) readiness and automated CI/CD verification using `sbom-cbom-generator`.

### Phase 5: GitHub Security Governance & CI/CD Setup
1. **GitHub Actions Security Workflows**: Deploy [security-governance.yml](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/security-governance.yml) into `.github/workflows/` (using patterns from `github-actions-templates`). Configure SARIF upload (`github/codeql-action/upload-sarif`) into the GitHub Security tab.
2. **Dependabot & Supply Chain**: Deploy [dependabot.yml](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/dependabot.yml) with the required `cooldown: default-days: 7` setting (following `git-pr-workflows-git-workflow`).
3. **CODEOWNERS & Branch Protection**: Configure `.github/CODEOWNERS` for security-sensitive paths (`auth/`, `crypto/`, `.github/workflows/`, secrets configs) and define required PR status checks.
4. **Pre-commit Hooks**: Deploy [pre-commit.sh](file:///Users/jsoehner/.gemini/config/skills/security-governance-orchestrator/templates/pre-commit.sh) into `.git/hooks/pre-commit` to catch plaintext credentials and remind developers about ADR requirements locally.

### Phase 6: Synthesis, Action Plan & Knowledge Capture
1. Synthesize all audit findings, threat models, active ADRs, and scanning results into a unified executive report (`SECURITY_POSTURE.md`).
2. Provide a prioritized developer remediation plan with severity ratings, file paths, and verification commands.
3. **Memory Sync**: Persist findings, newly approved ADRs, and security policies to local memory storage:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```

---

## Anti-Patterns & Critical Constraints

- **NEVER** accept a security risk or deviate from standard crypto/auth without documenting an accepted ADR in `docs/adr/`.
- **NEVER** permit pull requests to merge if secret scanners or critical SAST checks fail.
- **NEVER** write ADRs that conceal negative consequences, residual risk, or operational complexity.
- **NEVER** delete or rewrite historical ADRs when retiring a security control; always mark them `Superseded by ADR-XXXX` or `Deprecated`.
- **NEVER** release software without valid machine-readable SBOM/CBOM artifacts and automated verification test passes.
- **NEVER** deploy security CI/CD workflows without setting explicit least-privilege token permissions (`permissions: contents: read, security-events: write`).

---

## Verification Checklist

1. [ ] Existing security posture audited and benchmarked against target compliance frameworks.
2. [ ] Threat model completed with documented STRIDE vectors and mitigations.
3. [ ] All architectural security decisions documented in `docs/adr/` with bidirectional superseding links.
4. [ ] GitHub Actions security scanning workflow `.github/workflows/security-governance.yml` active with SARIF export.
5. [ ] `.github/dependabot.yml` configured with required security cooldowns.
6. [ ] Pre-commit hook active to catch plaintext credentials and bypass attempts.
7. [ ] Local memory capture triggered via `capture_knowledge.py`.

---

## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
