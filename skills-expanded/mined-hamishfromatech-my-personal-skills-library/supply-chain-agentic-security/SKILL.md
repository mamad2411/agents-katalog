---
name: supply-chain-agentic-security
description: Secure the modern software supply chain where AI-generated code, autonomous dependency management, and agentic package retrieval introduce novel attack vectors. Use when designing CI/CD pipelines, managing dependencies in AI-assisted projects, or building SBOM governance. NOT for general application security without supply chain context.
---

# Supply Chain Agentic Security

## Overview
In 2026, software supply chain security demands agentic governance — AI-generated dependencies, autonomous package retrieval, and model weight provenance create attack surfaces no static scanner can fully cover. This skill operationalizes SBOM management, agentic dependency verification, and slopsquatting defense for A-Tech products.

## When to Use
- Building or securing CI/CD pipelines with AI-generated code
- Managing dependencies in projects using agentic coding assistants
- Evaluating or creating SBOMs for open-source distributions
- Defending against slopsquatting, typosquatting, and AI-hallucinated packages
- Auditing third-party AI model weights and training data provenance
- NOT for: runtime application security, network security, or physical security

## Core Process / Workflow

### 1. The Agentic Threat Model
Understand how AI agents expand the attack surface:

| Attack Vector | Mechanism | Frequency (2026) |
|---|---|---|
| **Slopsquatting** | AI hallucinates non-existent package names; attackers register them | 20% of AI samples recommend phantom packages |
| **Rules File Backdoor** | Hidden Unicode in .cursorrules / .claude.md executes malicious commands | Confirmed in GitHub Copilot and Cursor |
| **Credential Sprawl** | AI commits secrets 2× human baseline | 3.2% vs 1.5% baseline leak rate |
| **Dependency Injection** | AI introduces vulnerable transitive deps without review | 45% of AI-generated code contains vulns |
| **Model Weight Poisoning** | Fine-tuned weights embed backdoors | Emerging threat, limited detection tools |
| **SBOM Drift** | AI updates dependencies without updating declared SBOM | Near-universal in agentic workflows |

### 2. Four-Layer Defense Architecture

#### Layer 1: Pre-Generation Guardrails
Prevent bad inputs from entering the agent context:

- **Curated Package Allowlist** — Agents only see packages from verified registries
- **Dependency Budget** — Max transitive depth enforced (recommended: 3 levels)
- **Prompt Injection Shield** — Scan `.cursorrules`, `.claude.md`, system prompts for hidden Unicode / suspicious commands
- **Knowledge Base Pinning** — Lock agent to specific model versions and known-good docs

```yaml
# .atech-guardrails.yml
allowed_registries:
  - npm:https://registry.npmjs.org
  - pypi:https://pypi.org/simple
blocked_patterns:
  - "^[^\\x00-\\x7F]"  # hidden unicode
  - "curl.*\\|.*sh"    # pipe-to-shell
max_dependency_depth: 3
require_sbom_update: true
```

#### Layer 2: Static Analysis Gates
Block dangerous outputs before commit:

| Tool | Purpose | AI-Specific Rule |
|---|---|---|
| **TruffleHog** | Secret detection | Lower threshold; expect AI-generated placeholder secrets |
| **Semgrep** | SAST | Custom rules for AI-common bugs (missing CSRF, incorrect authz) |
| **jscpd / SonarQube** | Duplication detection | 8× higher duplication from AI code demands stricter gates |
| **OWASP Dependency-Check** | Known CVE scanning | Verify transitive closure, not just declared deps |
| **Sigstore / cosign** | Artifact signing | All SBOMs and container images signed |

Semgrep AI-specific rule example:
```yaml
rules:
  - id: ai-missing-csrf
    patterns:
      - pattern: |
          @app.route("...", methods=["POST"])
          def $FUNC(...):
            ...
      - pattern-not-inside: |
          @csrf_exempt
          def $FUNC(...):
            ...
    message: "AI commonly omits CSRF protection. Verify intentional exemption."
```

#### Layer 3: Dynamic Verification
Validate runtime behavior matches declared intent:

- **Sandboxed Integration Tests** — Install candidate dependencies in isolated environment
- **Network Policy Validation** — Confirm outbound connections match SBOM declarations
- **Behavioral Fuzzing** — Test AI-generated endpoints with unexpected inputs
- **Drift Detection** — Continuously compare running SBOM to declared SBOM

#### Layer 4: Post-Deployment Monitoring
Detect supply chain compromises in production:

- **SBOM Telemetry** — Runtime SBOM generated from actual loaded modules
- **Anomaly Detection** — Unexpected network calls, file writes, child processes
- **Dependency Alerting** — New CVEs in transitive graph within minutes of disclosure
- **Rollback Trigger** — Automatic rollback on critical supply chain alerts

### 3. SBOM Lifecycle Management
Treat SBOMs as living documents, not static artifacts:

```
[Design] → [Generate] → [Sign] → [Distribute] → [Verify] → [Update]
   ↑                                              ↓
   └──────────────── Drift Alert ───────────────────┘
```

**Design Phase**: Declare intended dependencies with version constraints and known provenance  
**Generate Phase**: Use `syft` or `cdxgen` to create SPDX/CycloneDX SBOM from actual artifacts  
**Sign Phase**: Cosign signature + Rekor transparency log entry  
**Distribute Phase**: Attach to release, expose via API, embed in container labels  
**Verify Phase**: Consumers verify signature, compare against allowlist  
**Update Phase**: Automated PR when dependencies change; drift alert if SBOM doesn't match reality

### 4. Slopsquatting Defense Protocol
Defend against AI hallucinated packages becoming real malware:

1. **Hallucination Detection** — Compare agent-suggested packages against registry API before installation
2. **Namespace Reservation** — Pre-register plausible variations of your internal package names
3. **Installation Delay** — 24-hour cooling-off period for packages <30 days old or <100 downloads
4. **Typosquatting Database** — Check against known-typo lists (e.g., `pypy` vs `pypi`)
5. **Community Registry** — Participate in open-source package vetting initiatives

```python
def verify_package_safety(package_name, registry):
    info = registry.lookup(package_name)
    if not info.exists:
        raise SlopsquattingRisk(f"Package '{package_name}' does not exist in registry")
    if info.age_days < 30 and info.downloads < 100:
        logger.warning(f"New package '{package_name}' flagged for review")
        return False
    if info.similar_to_known_typo():
        raise TyposquattingRisk(f"Package '{package_name}' matches typo pattern")
    return True
```

### 5. Model Weight Provenance
Extend supply chain security to AI model artifacts:

- **Model Cards** — Document training data, hyperparameters, evaluation results
- **Weight Signing** — Cryptographic signatures on released model binaries
- **Training Attestation** — Verifiable claim about training data sources and filtering
- **Reproducibility Hash** — Deterministic training run hash for audit
- **Fine-Tune Lineage** — Chain of custody from base model to deployed variant

### 6. Compliance Mapping

| Regulation | Requirement | A-Tech Implementation |
|---|---|---|
| EU Cyber Resilience Act (CRA) | SBOM for products with digital elements | Automated SPDX generation per release |
| US Executive Order 14028 | SBOM for federal software | CycloneDX export, NTIA minimum elements |
| FDA Pre-Cert (medical) | Supply chain transparency for AI/ML | Model card + SBOM + training attestation |
| PCI DSS 4.0 | Dependency vulnerability management | Automated CVE scanning, 30-day remediation SLA |

### 7. Measurement Framework

| Metric | Target | Tool |
|---|---|---|
| SBOM coverage | 100% of releases | Release pipeline gate |
| Secret leak rate | <0.5% | TruffleHog, pre-commit hooks |
| Dependency drift | Detected within 24h | SBOM diff scanner |
| Slopsquatting blocks | 100% of phantom packages | Registry verification script |
| Mean time to patch (MTTP) | <72h for critical CVEs | Dependency update automation |
| Model weight signed | 100% of released models | Sigstore/cosign |

## References
- See [references/agentic-threat-intelligence.md](references/agentic-threat-intelligence.md) for 2026 threat actor tactics specific to AI-generated supply chains.
- See [references/sbom-tools-configuration.md](references/sbom-tools-configuration.md) for ready-to-use Syft, cdxgen, and SPDX Merge configurations.
- See `vibe-coding-security-defense` for IDE-level and developer-focused security patterns.
- See `mcp-security-trust` for Model Context Protocol specific security considerations.
