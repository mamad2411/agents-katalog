---
name: ai-code-provenance-generative-authorship
description: Establish cryptographic provenance, generative authorship attribution, and SBOM governance for AI-generated code. Use when building compliance-ready development workflows, defending against slopsquatting and model poisoning, or creating audit trails for regulated environments. NOT for general code quality without provenance context.
---

# AI Code Provenance & Generative Authorship

## Overview

By 2026, an estimated 41% of global code is AI-generated, rising to 61% in Java projects. This shift introduces a fundamental governance problem: who — or what — authored the code, and can its origin, integrity, and lineage be verified? Without provenance, organizations cannot audit, license, secure, or trust their software supply chains. The EU Cyber Resilience Act, US Executive Orders, and insurance underwriters now mandate that digital products carry Software Bills of Materials (SBOMs) and attestations of origin.

This skill provides a practical framework for generative authorship: cryptographic provenance tracking, AI-generated code labeling, SBOM governance that includes model and prompt metadata, and slopsquatting defense. It extends supply-chain security into the realm of generative AI, where traditional git history and dependency scanning are insufficient.

## When to Use

- Building CI/CD pipelines that must distinguish human-authored from AI-generated code
- Creating compliance documentation for regulated industries (healthcare, finance, government, critical infrastructure)
- Defending against slopsquatting attacks where AI hallucinates non-existent dependencies
- Establishing audit trails for AI-assisted development in enterprise or open-source contexts
- Designing licensing and attribution frameworks for mixed human-AI creative works

NOT for:
- Teams without CI/CD or version control infrastructure
- Prototypes with no production deployment path
- Organizations that do not require external audit or compliance certification

## The Provenance Problem

### Traditional Provenance
In conventional development, provenance is straightforward:
- Author: The human who wrote the commit
- Time: The commit timestamp
- Tool: The IDE or editor used
- Review: The approver who merged the code

### Generative Provenance Complexity
AI-generated code introduces new, ungoverned variables:
- **Model provenance:** Which model, version, and fine-tune produced the code?
- **Prompt provenance:** What instructions, context, and constraints guided generation?
- **Human provenance:** Who reviewed, modified, or approved the AI output?
- **Chain provenance:** How many AI-to-AI transformations occurred before final code?
- **Dependency provenance:** Which libraries did the AI reference, and were they real or hallucinated?

Without recording these variables, an organization cannot answer basic governance questions:
- "Can we trust this code's security if we don't know which model generated it?"
- "Are we compliant with AGPL if the AI was trained on copyleft code?"
- "Who is liable if this AI-generated component causes harm?"

## The Generative Authorship Stack

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Generation Metadata                                 │
│ • Model ID, version, temperature, system prompt hash          │
│ • Context window summary (not full text; privacy-preserving)    │
│ • Generation timestamp and session identifier               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Layer 2: Human Agency Layer                                    │
│ • Reviewer identity and comprehension attestation             │
│ • Modification delta (what human changed vs. AI output)       │
│ • Approval signature (cryptographic or procedural)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Layer 3: SBOM Extension                                        │
│ • AI-generated components flagged in SPDX/CycloneDX         │
│ • Model provenance recorded as build tool metadata            │
│ • Hallucinated dependency detection and blocking              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Layer 4: Verification & Audit                                │
│ • Reproducibility check: same prompt + model → same output? │
│ • Drift detection: model updates change previously generated code│
│ • Security attestation: SAST results tied to generation metadata│
└─────────────────────────────────────────────────────────────┘
```

## Core Process / Workflow

### Step 1: Generation Metadata Capture
Record the minimal viable provenance at generation time.

**Required fields:**
```yaml
ai_provenance:
  model_id: "anthropic/claude-4-sonnet-20260501"
  model_version: "2026.05.01"
  temperature: 0.4
  system_prompt_hash: "sha256:a3f2..."
  generation_timestamp: "2026-06-14T09:23:11Z"
  session_id: "sess_8x9k2m"
  tool_name: "a-coder-agent-mode"
  tool_version: "2.3.1"
  human_operator: "jane.doe@atech.dev"
```

**Privacy preservation:**
- Record prompt hash, not prompt content (prevents leakage of proprietary instructions)
- Summarize context window by topic, not by file names or data contents
- Store raw prompts locally; only metadata travels to compliance systems

**Implementation:**
- IDE plugin intercepts AI generation calls and injects provenance header as comment block
- Git pre-commit hook extracts provenance from comments and writes to `.ai-provenance.yml`
- CI/CD pipeline validates that all AI-generated files carry provenance metadata

### Step 2: Human Agency Attestation
Ensure every AI-generated contribution has a human reviewer who understands and approves it.

**The Comprehension Contract for AI Code:**
1. Reviewer reads every line of AI-generated code
2. Reviewer identifies the design pattern and one potential failure mode
3. Reviewer confirms fit with existing architecture
4. Reviewer signs attestation (cryptographic or procedural)

**Attestation format:**
```yaml
human_agency:
  reviewer: "alex.chen@atech.dev"
  review_timestamp: "2026-06-14T10:45:02Z"
  comprehension_confirmed: true
  modifications_made: "refactored error handling, renamed variables for clarity"
  security_verified: true
  architecture_aligned: true
  attestation_signature: "sig_7h3k9m"
```

**Tooling:**
- GitHub/GitLab bot that requires reviewer attestation on PRs with >50% AI-generated lines
- Attestation stored in repository alongside code, not in external system
- Blockchain-optional: attestation hash anchored to public ledger for immutable audit trail

### Step 3: SBOM Governance for AI Components
Extend Software Bills of Materials to include generative components.

**SPDX/CycloneDX extension:**
```json
{
  "bomFormat": "CycloneDX",
  "components": [
    {
      "type": "library",
      "name": "auth-middleware",
      "properties": [
        {
          "name": "ai-generated",
          "value": "true"
        },
        {
          "name": "ai-model",
          "value": "anthropic/claude-4-sonnet-20260501"
        },
        {
          "name": "human-reviewer",
          "value": "alex.chen@atech.dev"
        },
        {
          "name": "comprehension-attested",
          "value": "true"
        }
      ]
    }
  ]
}
```

**Dependency verification:**
- AI-referenced packages checked against registry before SBOM acceptance
- Hallucinated packages flagged as "unresolved dependency risk"
- Installation blocked for packages <30 days old and <100 downloads
- Automated daily re-verification of all declared dependencies

### Step 4: Slopsquatting Defense
Prevent AI hallucinated package names from becoming malware vectors.

**Detection pipeline:**
1. **Registry lookup:** Every package referenced by AI is verified against npm/PyPI/Go registry before installation
2. **Levenshtein distance check:** Package names compared against known packages; typosquatting variants flagged
3. **Age heuristic:** New packages (<30 days) trigger manual review before inclusion
4. **Community blocklist:** Shared registry of known slopsquatted packages across A-Tech and partner organizations
5. **Namespace pre-registration:** Pre-register plausible variations of internal package names before AI exposure

```python
def verify_ai_referenced_package(package_name, registry):
    info = registry.lookup(package_name)
    if not info.exists:
        raise SlopsquattingRisk(f"AI referenced non-existent package '{package_name}'")
    if info.age_days < 30 and info.downloads < 100:
        raise SuspiciousPackageRisk(f"Package '{package_name}' is new and unverified")
    if levenshtein_distance(package_name, known_package) < 3:
        raise TyposquattingRisk(f"Package '{package_name}' is similar to '{known_package}'")
    return True
```

### Step 5: Reproducibility & Drift Detection
Verify that AI-generated outputs are stable and detect when model updates change behavior.

**Reproducibility testing:**
- Monthly test: replay 100 stored prompts against current model version
- Compare output similarity (structural, not line-by-line) to baseline
- Flag significant drift (>20% structural difference) for review

**Model update protocol:**
- When model version changes, re-run SAST on all AI-generated components
- Compare security posture: new issues flagged for immediate remediation
- Document "drift impact" in release notes for compliance auditors

## Compliance Mapping

| Regulation | Requirement | Provenance Implementation |
|---|---|---|
| EU Cyber Resilience Act | SBOM for products with digital elements | CycloneDX with AI component flags |
| US EO 14028 | SBOM for federal software | SPDX with generation metadata |
| EU AI Act | Transparency for high-risk AI systems | Model provenance + human agency attestation |
| FDA Pre-Cert (medical software) | Traceability for AI/ML components | Generation metadata + reviewer attestation + drift logs |
| PCI DSS 4.0 | Change control and code review | Comprehension contract + cryptographic attestation |
| ISO 27001 | Asset inventory and risk assessment | SBOM with AI component risk classification |

## A-Tech Product Applications

### A-Coder (IDE)
- **Auto-provenance injection:** Every AI-generated file block carries embedded metadata comment
- **Reviewer dashboard:** Highlights AI-generated sections in PR review; enforces comprehension attestation
- **Slopsquatting shield:** Auto-verifies all package names referenced by AI before installation suggestion
- **Drift alerts:** Notifies maintainers when model updates may affect existing AI-generated code

### Be Practical (Playbooks)
- **Policy templates:** Ready-to-use AI code provenance policy for solo founders and small teams
- **Compliance checklists:** Step-by-step SBOM generation and attestation workflows
- **Case study:** How one member used provenance tracking to pass SOC 2 audit with AI-assisted development

### Builder's Club (Community)
- **Open-source provenance toolkit:** Git hooks, CI/CD templates, and SBOM generation scripts
- **Slopsquatting registry:** Community-maintained list of AI-hallucinated packages
- **Provenance benchmark:** Annual survey of member teams' provenance maturity
- **Contribution standards:** All community-contributed code requires provenance metadata

## Measurement Framework

| Metric | Target | Measurement |
|--------|--------|-------------|
| Provenance coverage | 100% of AI-generated files | Git + CI/CD audit |
| Attestation compliance | 100% of AI PRs reviewed | PR checklist automation |
| Slopsquatting blocks | 100% of phantom packages | Registry verification logs |
| SBOM freshness | Updated within 24h of every release | Release pipeline gate |
| Reproducibility score | >85% output stability | Monthly drift test |
| Audit pass rate | 100% of compliance audits | External auditor reports |

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Better Alternative |
|-------------|-------------|-------------------|
| Storing full prompts in compliance system | Leaks proprietary context and user data | Store hashes; keep prompts local |
| Treating AI code as "automatically reviewed" | Bypasses human accountability; creates liability | Mandatory comprehension attestation |
| SBOMs as static artifacts | Drift between declared and actual dependencies | Continuous SBOM verification |
| Ignoring model updates | Previously safe code may degrade with new model versions | Drift detection on every model change |
| Attestation without verification | Tick-box compliance without real review | Random audit sampling of attestations |

## Cross-References
- `developer-experience-and-flow/supply-chain-agentic-security` — Broader supply chain threat model and defense architecture
- `developer-experience-and-flow/augmented-coding-reality-protocol` — Evidence-based AI adoption with quality gates
- `ai-agents-and-workflows/agent-reputation-identity-framework` — DIDs and verifiable credentials for agent authorship
- `developer-experience-and-flow/vibe-coding-security-defense` — IDE-level security patterns for AI-generated code
- `privacy-and-trust/algorithmic-transparency-accountability` — Model cards and system fact sheets for AI transparency

## Sources
- Index.dev — Global code generation statistics (2026): 41% AI-generated globally, 61% in Java
- IEEE Computer Society — "Is Vibe Coding the Future of Software?" (2026): Critical examination of AI-generated code quality
- Mend.io — "AI-Powered Application Security: Evolution Or Revolution?" (2026): Code provenance and authorship in supply chain security
- ScienceDirect — "TRiSM for Agentic AI: A review of Trust, Risk, and Security Management" (2026): Structured analysis of LLM-based multi-agent systems
- ICSE 2026 — Research Track on SBOM for AI Supply Chains (ISO/IEC 5962:2021 extension)
- EU Cyber Resilience Act — Supply chain transparency requirements (2024–2026)
- US Executive Order 14028 — Federal software SBOM mandates
- NIST — Software Supply Chain Security Guidance (SP 800-161r1, 2025 update)
