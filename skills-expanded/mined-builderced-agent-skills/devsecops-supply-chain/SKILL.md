---
name: devsecops-supply-chain
description: Generate SBOM (CycloneDX/SPDX), verify SLSA provenance, audit dependency chains, and detect supply chain attack patterns.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: devsecops
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global]
priority: high
dependencies:
  mcp: []
  skills: []
  apis: []
  data: []
update_sources:
  - url: "https://slsa.dev/spec/v1.0/"
    check_frequency: "quarterly"
    last_checked: "2026-04-17"
license: MIT
---

# DevSecOps Supply Chain Security

## When to Use

- Setting up dependency security for a new project
- Generating SBOM for compliance or audit
- Investigating a suspicious dependency
- Responding to a supply chain incident
- Configuring CI/CD security gates

## SBOM Generation

### Formats
| Format | Standard | Best For |
|--------|----------|---------|
| CycloneDX | OWASP | Security-focused, VEX support |
| SPDX | Linux Foundation | License compliance, legal |

### Generation Commands

If a terminal is available, use these commands. Otherwise, describe what fields to include manually.

**Node.js/npm**:
```bash
npx @cyclonedx/cyclonedx-npm --output-file sbom.json
```

**Python/pip**:
```bash
pip install cyclonedx-bom
cyclonedx-py requirements -i requirements.txt -o sbom.json
```

**Go**:
```bash
cyclonedx-gomod mod -json -output sbom.json
```

## SLSA Compliance Levels

| Level | Requirement | How |
|-------|-------------|-----|
| SLSA 1 | Documentation of build process | Document build steps |
| SLSA 2 | Hosted build platform, signed provenance | Use GitHub Actions, sign with Sigstore |
| SLSA 3 | Hardened build platform, non-falsifiable provenance | Isolated builders, hermetic builds |

## Supply Chain Attack Patterns

| Pattern | Detection | Prevention |
|---------|-----------|------------|
| Typosquatting | Compare package name to known packages | Pin exact versions |
| Dependency confusion | Check if internal name exists on public registry | Scope packages, configure registry priority |
| Compromised maintainer | Monitor for unusual releases, new maintainers | Pin versions + hashes, delayed adoption |
| Malicious post-install | Audit install scripts | `--ignore-scripts` flag, review before install |
| Star-jacking | Verify GitHub URL matches npm/PyPI metadata | Cross-reference package metadata |

## Dependency Audit Checklist

1. Are all dependencies pinned to exact versions?
2. Are lockfiles committed and reviewed in PRs?
3. Are dependency hashes verified (pip `--require-hashes`, npm `--package-lock-only`)?
4. Is there a delay before adopting new package versions (7+ days)?
5. Are transitive dependencies audited (not just direct)?
6. Are install scripts reviewed for new dependencies?
7. Is there automated vulnerability scanning in CI?

## What This Skill Does NOT Do

- Does not patch vulnerabilities automatically
- Does not detect zero-day exploits
- Does not replace tools like Snyk, Dependabot, or pip-audit (complements them)
- Does not manage secrets rotation
