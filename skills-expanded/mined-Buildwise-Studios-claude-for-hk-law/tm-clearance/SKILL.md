---
name: tm-clearance
description: >
  Guide legal practitioners through conducting trade mark clearance searches in Hong Kong under the Trade Marks Ordinance (Cap 559), assessing availability risks, and developing filing strategies.
---
# Trade Mark Clearance — Skill

## Purpose

Guide legal practitioners through conducting trade mark clearance searches in Hong Kong under the Trade Marks Ordinance (Cap 559), assessing availability risks, and developing filing strategies.

## Scope

- IPD trade mark register search
- Company name search via Companies Registry
- Common law use / passing off risk assessment
- Well-known mark considerations
- Domain name and social media handle checks
- Absolute and relative grounds analysis
- Filing strategy and class selection
- Risk assessment and opinion writing

## Workflow

### 1. Understand the Client's Mark and Use

- Exact mark (word, device, composite, 3D, colour, sound, scent)
- Goods/services to be covered (Nice Classification)
- Priority date required (any earlier Paris Convention filing?)
- Geographic scope of current and intended use
- Existing rights (if any) — registered mark, application, common law use, design registration, domain name

### 2. Conduct IPD Register Search

- Search the IPD trade mark register via e-Search:
  - Exact match search
  - Phonetic/confusingly similar search
  - Class-specific search
  - Proprietor search (competitors, brand owners in same sector)
- Review identical and similar marks in relevant classes
- Check status (registered, pending, opposed, expired, surrendered)
- Note earlier filing dates and priority claims

### 3. Assess Absolute Grounds (s.11 Cap 559)

Check whether the mark is:
- Devoid of distinctive character (s.11(1)(b))
- Descriptive of goods/services (s.11(1)(c))
- Customary in current language / bona fide trade practices (s.11(1)(d))
- Contrary to public policy or accepted principles of morality (s.11(3)(a))
- Deceptive (s.11(3)(b)) — nature, quality, geographical origin
- Specially protected emblems, flags, armorial bearings (s.11(4))

### 4. Assess Relative Grounds (s.12 Cap 559)

- Identical/similar marks for identical/similar goods/services (s.12(1)–(2))
- Well-known marks — protection against identical/similar marks for identical/similar or dissimilar goods/services (s.12(3)–(4))
- 5-year limitation: an earlier mark registered for 5+ years cannot be relied upon if the applicant can prove the applicant's use of the mark had become accepted in the relevant sector (s.56)

### 5. Conduct Common Law Search

- Company name search via Companies Registry e-Search (company/business names)
- Domain name search (.hk, .com.hk, .com, others)
- Social media handle check
- Marketplace search (Lazada, HKTVmall, Amazon HK, Carousell)
- Trade press and media search
- Google/industry search for unregistered use

### 6. Assess Passing Off Risk

- Does the unregistered user have goodwill in HK?
- Would the client's use constitute misrepresentation?
- Is damage likely?
- Factors: length of use, geographic extent, advertising spend, reputation recognition, survey evidence

### 7. Risk Categorisation and Opinion

| Risk Level | Description | Recommended Action |
|------------|-------------|-------------------|
| Low | No identical/similar marks found; mark is inherently distinctive | Proceed with filing; IPD search confirmation |
| Moderate | Similar marks found in same class but with different goods; or descriptive concerns | Consider;
- Specification narrowing
- Consent letter from earlier proprietor
- Evidence of acquired distinctiveness
- Co-existence argument |
| High | Identical/similar mark for identical/similar goods; or well-known mark conflict | Do not proceed without:
- Revocation action against non-use of conflicting mark
- Invalidity action
- Settlement/co-existence agreement
- Rebrand consideration |

### 8. Filing Strategy

- Determine classes needed (current + future expansion)
- Consider single-class or multi-class application
- Use Paris Convention priority (if applicable) to preserve earlier date
- Consider Madrid Protocol designation (if a wider international portfolio exists)
- Prepare the application with appropriate representation (HK trade mark agent or solicitor)
- File with IPD (e-filing available)

### 9. Post-Filing Monitoring

- Track publication date in HK Intellectual Property Journal
- Monitor for oppositions (3-month period from publication)
- Respond to any IPD objections (6-month deadline, extendable)

## Key Provisions

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.7 | Well-known marks | Protection without registration |
| s.11 | Absolute grounds | Distinctiveness, descriptiveness, morality |
| s.12 | Relative grounds | Earlier marks, well-known marks |
| s.42 | Filing date | Date of receipt by IPD |
| s.43 | Priority | 6-month Paris Convention priority |
| s.52 | Non-use revocation | 3 consecutive years of non-use |
| s.56 | 5-year limitation | Acquiescence / acceptance |

## Key Cases

- **Société des Produits Nestlé SA v Unicafe Inc** — Likelihood of confusion
- **San Miguel Brewing International Ltd v Liang Bichun** — Goodwill in HK
- **Kabushiki Kaisha Toshiba v HKC International Ltd** — Well-known mark protection

## Tools & Resources

- IPD Hong Kong (https://www.ipd.gov.hk) — Trade mark register search, e-filing
- Companies Registry e-Search (https://www.icris.cr.gov.hk) — Company name search
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 559 absolute/relative grounds
- HKLII (https://www.hklii.hk) — Opposition and infringement decisions
- Nice Classification — WIPO classification database

## Practice Guidance

1. **Searches are not exhaustive** — register search may miss unregistered rights and common law use
2. **Company name search is essential** — a company name identical to a mark may create passing off risk and be challenged by the Companies Registry
3. **Well-known marks** — even if not registered in HK, may block registration under s.7
4. **Consent letters** — from earlier mark owners can overcome relative grounds objections
5. **IPD objections** — respond within 6 months; evidence of use / acquired distinctiveness may overcome absolute grounds
6. **Opposition risk** — be prepared; opposition proceedings can be costly (CFI proceedings)
7. **Always dual-track** — consider both registered (IPD) and unregistered (passing off) rights


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
