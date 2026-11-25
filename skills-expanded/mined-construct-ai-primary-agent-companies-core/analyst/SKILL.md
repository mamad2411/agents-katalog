---
name: analyst
description: >
  Use when: applying sector-specific rules (oil-gas, infrastructure, construction, energy, etc.) to app features, validating features against regional/regulatory requirements, or creating sector-specific test cases.
  Don't use when: mapping features to engineering disciplines (use advisor), creating general QA strategies (use validator), or testing workflow coordination (use coordinator).
allowed-tools:
  - Read
  - Grep
  - Write
  - Glob
  - Bash
metadata:
  paperclip:
    tags:
      - sector-analysis
      - construction-sectors
      - compliance
---

# Sector Analysis Skill

## Purpose

This skill applies sector-specific regulations, standards, and rules to app features, ensuring that construction industry requirements (oil-gas, infrastructure, commercial, industrial, residential) are correctly implemented.

## When to Use

- When features have sector-specific implications
- During compliance reviews
- As part of the requirements gathering for sector projects
- When sector regulations are updated

## Steps

### 1. Sector Identification

Identify which sectors are affected by the feature:

```bash
# Find sector-specific documentation
find ../docs-construct-ai/disciplines/00300_construction -name "*.md" -type f

# Check for sector-specific workflows
grep -r "sec:" ../docs-construct-ai --include="*.md"
```

**Sector Categories:**
| Sector | Tag | Key Focus |
|--------|-----|-----------|
| Oil & Gas | `sec:oil-gas` | Upstream, midstream, downstream |
| Infrastructure | `sec:infrastructure` | Roads, bridges, utilities |
| Commercial | `sec:commercial` | Office, retail, mixed-use |
| Industrial | `sec:industrial` | Manufacturing, processing |
| Residential | `sec:residential` | Housing, multi-family |

### 2. Regulatory Research

Research applicable regulations for each sector:

**Oil & Gas**
- API (American Petroleum Institute) standards
- ASME (American Society of Mechanical Engineers) codes
- OSHA Process Safety Management (PSM)
- EPA environmental regulations

**Infrastructure**
- DOT (Department of Transportation) requirements
- FHWA (Federal Highway Administration) standards
- EPA water and environmental rules
- State-specific infrastructure codes

**Commercial**
- IBC (International Building Code)
- ADA (Americans with Disabilities Act)
- Local building codes
- Fire safety regulations

**Industrial**
- OSHA safety standards
- EPA emissions and waste regulations
- NFPA (National Fire Protection Association) codes
- Industry-specific standards

**Residential**
- IRC (International Residential Code)
- Local building codes
- Energy efficiency standards
- Habitability requirements

### 3. Compliance Verification

Verify feature compliance with sector regulations:

**Documentation Review**
- Check that required documentation is present
- Verify compliance certificates are obtainable
- Ensure audit trails are maintained

**Technical Compliance**
- Verify technical requirements are met
- Check safety systems are implemented
- Ensure monitoring and alerting are in place

**Process Compliance**
- Verify approval workflows are correct
- Check that required inspections are supported
- Ensure reporting requirements are met

### 4. Edge Case Identification

Identify sector-specific edge cases:

**Environmental Conditions**
- Extreme temperatures
- Corrosive environments
- Hazardous locations

**Operational Scenarios**
- Emergency shutdown procedures
- Maintenance workflows
- Inspection requirements

**Regulatory Scenarios**
- Compliance reporting deadlines
- Permit renewal processes
- Violation handling procedures

### 5. Cross-Sector Analysis

Analyze features that span multiple sectors:

- Identify conflicting requirements
- Propose harmonization strategies
- Document sector-specific variations
- Create sector-specific test cases

## Output

```markdown
# Sector Analysis Report

## Affected Sectors
| Sector | Tag | Compliance Status |
|--------|-----|-------------------|
| [Sector] | [tag] | Compliant / Needs Work |

## Regulatory Requirements
### [Sector Name]
- **API/Standard**: [Reference]
- **Requirement**: [Description]
- **Status**: Met / Partial / Not Met

## Compliance Verification
- [ ] Technical requirements verified
- [ ] Process requirements verified
- [ ] Documentation requirements verified

## Sector-Specific Edge Cases
1. [Edge case] — [Handling strategy]
2. [Edge case] — [Handling strategy]

## Cross-Sector Conflicts
- [ ] No conflicts detected
- [ ] Conflicts found — see below
  - [Conflict description and resolution]
```

## Error Handling

- If regulations are unclear, flag for legal review
- If compliance cannot be verified, require manual audit
- If sector requirements conflict, propose compromise solutions

## Related Skills

- `sector-qa` — Creates sector-specific test cases
- `discipline-strategy` — Maps sector workflows
- `app-guardian` — Enforces sector compliance gates
- `qa-strategy` — Integrates sector tests into overall strategy