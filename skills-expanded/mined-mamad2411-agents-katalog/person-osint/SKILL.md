---
name: person-osint
description: |
  Person OSINT — professional person investigation using systematic methodology.

  [WHAT] A complete, verified person profile per OSINT methodology:
  document-first approach, financial-OSINT integration, content analysis,
  organizational + personal network, threat-actor perspective.

  [WHEN] Use when: person OSINT, person investigation, background check,
  due diligence, who is, prepare meeting.

  [LANGUAGE] Configurable.

  [EXPERTISE] OSINT methodology (Bazzell, Bellingcat), public registries,
  economic analysis, network analysis, threat modeling.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch, Bash, mcp__exa__web_search_exa, mcp__brightdata__scrape_as_markdown, mcp__linkedin__get_person_profile
---

# Person OSINT

**Role:** systematic person investigator.
**Methodology:** document-first, evidence-based, traceable.
**Output:** structured profile with verified sources.

## Investigation approach

Eight standard sections. Configure per project which are mandatory:

- **A. Identity and basic data** — name, DOB if public, contact, photo
- **B. Professional background** — current role, employment history, education, certifications
- **C. Public statements** — published texts, interviews, op-eds, theses
- **D. Organizational network** — boards, memberships, formal roles
- **E. Digital presence** — social media, blogs, podcasts, media appearances
- **F. Financial profile** *(optional)* — companies, ownership, board roles, sanctions
- **G. Personal network** *(use sparingly)* — family, close associates *only if publicly relevant*
- **H. Threat-actor / risk perspective** *(if applicable)* — for security investigations

## Methodology principles

### 1. Document-first
Every claim has a source. No inference without basis. Every statement traceable.

### 2. Verify, don't trust
- Same fact from 2+ independent sources before treating as confirmed
- Distinguish primary from secondary sources
- Mark unverified claims clearly

### 3. Public information only
- No paywalled material if license forbids
- No data from breaches/leaks
- No private persons without strong public-interest justification

### 4. Time-stamp everything
Information has a half-life. Every fact gets a date and source.

### 5. Distinguish facts from inference
Use clear language:
- "X stated Y on date Z"  → fact
- "X likely…" → inference (with reasoning)
- "X may…" → speculation (mark explicitly)

## Standard data sources

### Professional
- LinkedIn (own MCP or manual)
- Organisation websites
- Company registries (public)
- Academic profiles (Google Scholar, ORCID, ResearchGate)

### Publications
- Google Scholar / Scopus
- News archives
- Personal blog/website
- Government Hansard / parliamentary records

### Digital presence
- Bluesky / Mastodon (public profiles)
- LinkedIn posts
- YouTube / podcast appearances
- Conference presentations

### Public registries (jurisdiction-specific — configure per project)
- Companies House (UK) / SEC EDGAR (US) / similar national registries
- Sanctions lists (OFAC, EU, UK)
- Court records (where public)
- Property registries (where public and licensed for use)

## Workflow

### Phase 1: scope
Define:
- Investigation purpose (meeting prep / due diligence / journalism / security)
- Required sections
- Time-bound (how recent / how far back)
- Sensitivity (what to deliberately NOT investigate)

### Phase 2: gather
Per section, collect from designated sources. Log source + date for every claim.

### Phase 3: verify
For each claim:
- Independent confirmation?
- Date of verification
- Reliability rating (verified / uncorroborated / disputed)

### Phase 4: structure
Write the profile per the section template (below). Use wikilinks for entities.

### Phase 5: assess
- What's solid?
- What's uncertain?
- What's inference vs. fact?
- What couldn't be found?

### Phase 6: deliver
Profile document with:
- Frontmatter metadata
- Per-section table of facts
- Source list at end
- Caveats and gaps

## Output template (excerpt)

```markdown
---
type: person-profile
subject: [Name]
purpose: [investigation purpose]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sections_completed: [A, B, C]
---

# [[Name]]

## A. Identity
| Field | Value | Source | Verified |
|-------|-------|--------|----------|
| Full name | ... | LinkedIn | ☑ |
| DOB | (only if public) | ... | ☐ |

## B. Professional background

### Current
- **Role:** ...
- **Organization:** [[Org]]
- **Since:** YYYY-MM
- **Source:** [link]

### Previous
[Chronological table]

## C. Public statements
[Listed with date, outlet, key claim]

## D. Organizational network
[Board roles, memberships]

## E. Digital presence
[Per platform]

## Sources
[Numbered, with dates and URLs]

## Gaps and caveats
- [What couldn't be found]
- [Uncertainties]
```

## Ethical limits

- **No harassment vectors.** No information that primarily enables targeting.
- **Public-interest test.** For private citizens: justify why a profile is needed.
- **Right of reply.** If publishing claims about a person: consider whether they can respond.
- **Time decay.** Information older than 5 years is weakly evidential for current state.
- **Aggregation harm.** Individually public facts may be invasive in aggregate. Be deliberate.

## Anti-patterns

- Speculating about psychology, beliefs, or motives without quoted sources
- Mapping family members beyond explicit public roles
- Using private-sphere social media without strong justification
- Treating one source as definitive
- Skipping verification for "obvious" claims

## Integration with other skills

- **financial-osint** for company/ownership analysis
- **osint-network** when extending to broader network
- **social-researcher** agent for digital presence (Section E)
- **person-researcher** agent for sections A-B (writes directly to document)

---

🎯 COMPLETED: [SKILL:person-osint] [profile of X completed]
🗣️ CUSTOM COMPLETED: [SKILL:person-osint] [Person profile ready]
