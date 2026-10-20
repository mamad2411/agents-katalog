---
name: financial-osint
description: |
  Methodological foundation for financial OSINT analysis.

  [WHAT] Follow-the-money, ownership-structure analysis, network analysis,
  sanctions checking. Frameworks for financial investigations with public-data tools.

  [WHEN] Use when: follow the money, ownership structure, beneficial owner,
  sanctions, oligarch, money laundering, shell company, offshore, UBO.

  [EXPERTISE] Corporate intelligence, sanctions checking, network analysis.

Workflow: SKILL = methodology | MCP = data collection | Agents = research
allowed-tools: Read, Grep, Glob, Write, Bash, WebFetch, WebSearch
---

# Financial OSINT

**Role:** methodology for following money, ownership, and economic relationships.

## When the skill activates

- Investigating ownership behind a company or transaction
- Mapping a network of related entities (companies, beneficial owners)
- Sanctions checking
- Shell-company / offshore-structure analysis
- Following payments, contracts, or political donations

## Core principles

### 1. Follow the structure, not just the name
Companies are nested. Always look one level up (parent), one level sideways (sister companies), one level down (subsidiaries) to find the real picture.

### 2. Beneficial ownership > legal ownership
Legal owner can be a nominee/trustee. Always ask: who is the **ultimate beneficial owner (UBO)**? Most jurisdictions now require UBO registers.

### 3. Sanctions are a fact-check, not a verdict
Match against multiple sanctions lists. False positives are common (similar names). Confirm with date of birth or other identifiers.

### 4. Time-stamp every relation
Companies merge, split, dissolve. A 5-year-old structure may be irrelevant.

### 5. Document the trail
Every claim has a source. Screenshots of registry pages with date/URL.

## Methodological frameworks

### Ownership chain mapping

For target company X:
1. Direct shareholders (>5% typical disclosure threshold)
2. Parent company (if any) — recurse upward
3. Subsidiaries (X's children)
4. Sister companies (other children of the same parent)
5. Board members and executives — look for crossovers
6. UBO (where registered)

### Beneficial owner identification

Ladder:
1. Legal owner (per registry)
2. Nominee / trustee analysis (if legal owner is a corporate entity, recurse)
3. UBO register (where mandated by law)
4. Press / leaks (Panama Papers, Pandora Papers, OCCRP)
5. Inference (only if multiple converging signals)

### Sanctions check

Always check against:
- OFAC SDN List (US)
- EU consolidated sanctions list
- UK OFSI list
- UN Security Council list
- Country-specific lists where relevant

Tools:
- OpenSanctions.org (consolidated, searchable)
- Each list's own search
- Aleph (OCCRP) for cross-referencing

### Politically Exposed Persons (PEP) check

Identify if a person/owner is a PEP. Sources:
- World-Check (paid)
- Open PEP databases (Wikidata, Aleph)
- Government lists where published

### Network analysis (financial)

Map relationships:
- Shared addresses (red flag for shell-company nests)
- Shared directors / nominees
- Shared funding sources
- Common consultants / law firms
- Transaction patterns (where data available)

Use the **osint-network** skill for the structural analysis.

## Standard data sources

### International
- **OpenCorporates** — global company registry data
- **OCCRP Aleph** — leaked documents + structured data
- **OpenSanctions.org** — consolidated sanctions
- **GLEIF** — Legal Entity Identifiers
- **Wikidata** — structured entity data with links to news

### National (configure per project)
Most jurisdictions have:
- Public company registry (e.g. Companies House UK, SEC EDGAR US)
- Beneficial owner register (per AMLD5/UBO directives)
- Court records
- Government procurement databases
- Property registries

### Investigative journalism
- **OCCRP** — Eastern European focus, global cases
- **ICIJ** — Panama/Pandora Papers, FinCEN Files
- Domestic investigative outlets

## Workflow

### Phase 1: scope
- What's the question? (ownership / sanctions / network / specific transaction)
- Sensitivity? (regulated due diligence vs. journalism vs. research)
- Public information only? (always yes for public OSINT)

### Phase 2: target identification
- Exact entity name + jurisdiction
- Tax/registration ID where available
- Disambiguation (multiple companies with similar names)

### Phase 3: structural mapping
Per the framework above. Document each step with source.

### Phase 4: sanctions / PEP check
Cross-reference against multiple lists. Document hits and false positives.

### Phase 5: network analysis
If relevant: extend to related entities and persons. Use the osint-network skill.

### Phase 6: synthesis
Produce report:
- Ownership structure (with mermaid diagram if useful)
- Beneficial owner conclusion (with confidence)
- Sanctions / PEP findings
- Network observations
- Sources and dates
- Gaps and caveats

## Output template

```markdown
# Financial OSINT: [Entity]

## Scope
- Target: [Entity name + ID]
- Question: [What we're investigating]
- Sensitivity: [Public OSINT / regulated DD / journalism]

## Ownership structure
[Mermaid diagram]

### Direct shareholders
| Owner | Stake | Type | Source |
|-------|-------|------|--------|

### Parent company / UBO
[Per the framework]

## Sanctions / PEP
- OFAC: [hit/no hit + match details]
- EU: ...
- PEP: ...

## Network observations
[Key findings from network analysis]

## Sources
[Numbered, with URLs and dates]

## Gaps and caveats
- [What couldn't be confirmed]
```

## Ethical limits

- Public information only. Avoid leaked data unless ethically published (OCCRP, ICIJ).
- Distinguish facts from inference. Mark speculative chains.
- Be careful of accusations. Sanctions / fraud claims need solid evidence.
- Time-stamp everything. Networks change.
- Right of reply for serious allegations being published.

## Integration with other skills

- **person-osint** for the persons behind companies
- **osint-network** for structural relationship mapping
- **intelligence-{signal,structure,context,synthesis}** for the analytical pipeline

---

🎯 COMPLETED: [SKILL:financial-osint] [financial OSINT on X]
🗣️ CUSTOM COMPLETED: [SKILL:financial-osint] [Financial OSINT done]
