---
name: nsl-compliance
description: >
  Provide structured compliance guidance for legal practitioners advising on matters touching the Hong Kong National Security Law (NSL), including risk assessment, procedural safeguards, ethical obligations, and cross-border considerations.
---
# NSL Compliance — Skill

## Purpose

Provide structured compliance guidance for legal practitioners advising on matters touching the Hong Kong National Security Law (NSL), including risk assessment, procedural safeguards, ethical obligations, and cross-border considerations.

## Scope

- NSL offences: secession, subversion, terrorism, collusion with foreign forces
- Designated judge system and judge-only trials
- Bail provisions (s.42 — restrictive)
- Pre-trial restraint orders and asset freezing
- Police powers under the NSL (National Security Department)
- Committee for Safeguarding National Security
- Extraterritorial application
- Interaction with the Basic Law and Hong Kong ordinances
- Professional ethical obligations when NSL issues arise

## Workflow

### 1. Assess Whether NSL is Engaged

Check for:
- Is the matter factually connected to national security?
- Does the client's activity involve any of the four NSL offences?
- Is there a cross-border element (HK ↔ Mainland)?
- Are there sensitive organisations, publications, or foreign connections involved?

### 2. Risk Analysis

- **Low risk**: Routine commercial activity, no national security nexus
- **Medium risk**: Client involved in sensitive sectors (academia, media, NGOs, publishing, political organising)
- **High risk**: Activity that could fall within one of the four offence categories; foreign connections to sensitive entities

### 3. Procedural Safeguards

- Right to legal representation (s.5(1) NSL — restricted access in certain circumstances)
- Right to bail — very limited (s.42: "no bail unless sufficient grounds" — higher threshold than normal HK law)
- Right to fair trial — qualified (s.5: judicial independence preserved)
- No jury for NSL offences (s.46)
- Closed hearings possible where national security is prejudiced
- Protection of sensitive evidence (PII/accreditation procedures)

### 4. Advice and Documentation

- Document all advice clearly
- Flag NSL risk to client at earliest appropriate opportunity
- Consider whether to recommend independent legal advice
- Maintain privilege — be aware of potential statutory overrides
- If concerned about client instructions engaging national security, seek senior counsel advice
- Follow Law Society / HKBA practice directions on NSL compliance

### 5. Ongoing Monitoring

- Monitor NSL case developments (CFA rulings on procedure)
- Check for new police practice directions
- Review SFO and ICE commentary
- Stay updated on designated judge appointments

## Key Provisions

| NSL Article | Subject | Key Detail |
|-------------|---------|-----------|
| Art 20 | Secession | Organising/participating in secession; up to life imprisonment |
| Art 22 | Subversion | Subverting state power; up to life imprisonment |
| Art 24 | Terrorism | Serious violence endangering national security |
| Art 29 | Collusion with foreign forces | Collusion with foreign/external elements |
| Art 42 | Bail | "No bail unless sufficient grounds" — narrow exception |
| Art 46 | Judge-only trial | No jury; CE designates judges |
| Art 55 | Special jurisdiction | Central Government may assume jurisdiction in exceptional cases |
| Art 59 | Committee for Safeguarding National Security | Established under CE; reports to Central Government |

## Ethical Considerations

- The Law Society of Hong Kong and HKBA have issued guidance on NSL practice
- Duty of confidentiality — limited where national security engaged
- Duty to the court — paramount
- Consider PII (Public Interest Immunity) in disclosure
- Be alert to potential conflict between client instructions and legal obligations

## Tools & Resources

- HKLII (https://www.hklii.hk) — NSL case law (HKSAR v Lai Chee Ying, Tam Sze Leung, Ma Chun Wai)
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — NSL full text
- CLAUDE.md for NSL overview and implications
- Law Society of HK / HKBA practice directions


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
