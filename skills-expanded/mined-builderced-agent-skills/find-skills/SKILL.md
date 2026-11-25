---
name: find-skills
description: Helps users discover and install agent skills when they ask "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. Searches this repo first, then the broader ecosystem via npx skills.
version: "2.0.0"
last-updated: "2026-04-21"
model_tested: "claude-sonnet-4-6"
category: meta
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
  - url: "https://github.com/BuilderCed/agent-skills"
    check_frequency: "monthly"
    last_checked: "2026-04-21"
  - url: "https://skills.sh/"
    check_frequency: "monthly"
    last_checked: "2026-04-21"
license: MIT
---

# Find Skills

Discover and install skills from this repository and the broader ecosystem.

## When to Use

Activate when the user:
- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain

## Step 1: Check This Repository First

This repo specializes in **regulated industries, French professional skills, and underserved markets**. Check here first for:

### Compliance & Regulatory (EU)
| Skill | Use When |
|-------|----------|
| `eu-ai-act-compliance` | Deploying AI in EU, classifying risk, adding disclosures |
| `eu-nis2-compliance` | Cybersecurity obligations for essential/important entities |
| `eu-dora-compliance` | Digital resilience for financial sector |
| `gdpr-data-protection` | Processing personal data, DPIA, data rights |
| `eu-regulatory-router` | Unsure which EU regulation applies |

### French Professional & Personal
| Skill | Use When |
|-------|----------|
| `fr-comptabilite` | French accounting (PCG, TVA, liasse fiscale) |
| `fr-fec-generator` | Generating FEC files for tax authority |
| `fr-facturation-electronique` | E-invoicing (Factur-X, mandatory 2026) |
| `fr-fiscalite-particulier` | Personal income tax, brackets, deductions, crypto |
| `fr-droit-immobilier` | Leases, diagnostics, housing law, renovation aids |
| `fr-fiscalite-investissement` | PEA, CTO, assurance-vie, PER, capital gains |

### Security, Privacy & DevSecOps
| Skill | Use When |
|-------|----------|
| `skill-security-audit` | Auditing a skill before installation |
| `devsecops-supply-chain` | SBOM, SLSA, dependency security |
| `pii-detection` | Detecting personal data in code/data |

### Agent Eval, Data, Documents, Offline, Africa, Infra
| Skill | Use When |
|-------|----------|
| `agent-eval-framework` | Testing agent outputs systematically |
| `fr-open-data-explorer` | French open data (SIRENE, DVF, DPE) |
| `invoice-processing` | Extracting/validating invoices |
| `offline-first-development` | Building offline-capable apps |
| `africa-mobile-money` | M-Pesa, Orange Money integration |
| `api-resilience-patterns` | Circuit breakers, retry, rate limiting |
| `context-engineering` | Optimizing agent context and token usage |
| `skill-lifecycle-management` | Managing skill versioning and freshness |

## Step 2: Search the Broader Ecosystem

If no skill in this repo matches, search the open ecosystem using the Skills CLI:

```bash
npx skills find [query]
```

Examples:
- User asks "make my React app faster" → `npx skills find react performance`
- User asks "help with PR reviews" → `npx skills find pr review`
- User asks "create a changelog" → `npx skills find changelog`

Browse all skills at: https://skills.sh/

## Step 3: Verify Quality Before Recommending

Do not recommend a skill based solely on search results. Always verify:

1. **Install count** — Prefer skills with 1K+ installs. Be cautious under 100.
2. **Source reputation** — Official sources (`vercel-labs`, `anthropics`, `supabase`, `mongodb`) are more trustworthy than unknown authors.
3. **GitHub stars** — Skills from repos with <100 stars should be treated with skepticism.
4. **Security** — Use `skill-security-audit` to scan any skill from an untrusted source before installing.

## Step 4: Install

```bash
# From this repo
npx skills add BuilderCed/agent-skills --skill [skill-name]

# From another repo
npx skills add [owner/repo] --skill [skill-name]

# Global install (user-level)
npx skills add [source] --skill [name] -g -y

# Check for updates
npx skills check

# Update all
npx skills update
```

## Step 5: When No Skill Exists

If no relevant skill exists anywhere:
1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using general capabilities
3. Suggest creating a custom skill: `npx skills init my-skill-name`

## What This Skill Does NOT Do

- Does not install skills automatically without user confirmation
- Does not recommend skills it hasn't verified for quality
- Does not replace domain expertise (skills are guidance, not guarantees)
