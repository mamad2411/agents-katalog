---
name: fortax-legal-compliance-check
description: Before a client launches something new (a product, referral or cashback scheme, app feature, marketing campaign, foreign deal, data project), list the Indian laws, registrations and approvals it touches, the requirements met and unmet, and rate each legal risk by severity x likelihood with when to take an advocate. Indian law first; GDPR/CCPA only when the client really has that data. Use for "yeh karne se pehle kaunse compliance lagenge", "legal risk kitna hai", "risk assessment memo bana do", "board ko risk batana hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/compliance-check (Apache-2.0); https://github.com/anthropics/knowledge-work-plugins/tree/main/legal/skills/legal-risk-assessment (Apache-2.0)"
---

# Legal compliance check and risk assessment

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Typical asks: "client referral program me cash reward dena chahta hai, kya dikkat hai", "app me Aadhaar/biometric
login lagana hai", "foreign company se investment aa raha hai, kya approvals", "is risk ko rate karo",
"risk register me daalo".

This is not legal advice. It tells the CA which laws a plan touches, what each needs, what is still
unknown, and how big each risk is. Requirements change often: every threshold, rate, deadline and form is
looked up (Rule 5 below), never recalled.

## Step 1 — get the plan in specific words

Ask for, if not given:

- **What exactly** — "email all our users a cashback offer" beats "marketing campaign".
- **Who does it** — entity type (company, LLP, firm, proprietor), listed or not, sector regulator if any.
- **Where** — states in India, and any foreign country (customers, servers, investors, vendors).
- **What data** — personal data involved? children's? financial, health, biometric, Aadhaar?
- **Money flow** — who pays whom, in what form (cash, wallet, points, crypto, shares), cross-border?
- **When** — launch date, so deadlines can be set.

## Step 2 — map the laws it touches

Go down this list and keep only what applies. For each, say *why* it applies in one line.

| Area | Typical Indian law and regulator | Triggers |
|---|---|---|
| Corporate approvals | Companies Act, 2013: board powers (s.179), special resolution for borrowing/sale of undertaking (s.180), loans to directors (s.185), loans and investments (s.186), related party transactions (s.188), CSR; LLP Act, 2008; SEBI LODR for listed entities | New business line, borrowing, guarantee, deal with a related party, share issue |
| Objects and registrations | MoA objects; Shops and Establishments Act (state); trade licence; Udyam; IEC for import/export; FSSAI; Legal Metrology packaged commodities; BIS; drug, cosmetic or medical-device licences | New activity, new premises, product sale |
| GST | CGST/IGST Acts: registration in each state, place of supply, e-invoice, e-way bill, e-commerce operator TCS, vouchers, cashback and free supplies, ITC on promotional goods | Any new supply, state, discount or reward scheme |
| Income tax / TDS | Income-tax Act: TDS on commissions, prizes, winnings, e-commerce payments, perquisites to dealers; business-promotion disallowance; transfer pricing for associated enterprises abroad | Rewards, incentives, payments to agents, foreign group payments |
| Foreign exchange | FEMA, 1999 and RBI rules: FDI (sectoral caps, entry route, pricing, FC-GPR), ODI, ECB, LRS, export realisation, import payments | Foreign investor, foreign subsidiary, foreign loan, cross-border service |
| Data | Digital Personal Data Protection Act, 2023 and DPDP Rules (see `fortax-india-dpdp-act`); IT Act, 2000 s.43A/72A and reasonable-security rules while they remain in force; Aadhaar Act restrictions on collecting and storing Aadhaar; CERT-In incident reporting directions; RBI payment data storage | Collecting, storing or sharing personal data, biometric or Aadhaar, a breach |
| Online platforms | IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021; Consumer Protection Act, 2019 and Consumer Protection (E-Commerce) Rules, 2020; CCPA guidelines on dark patterns and misleading ads | App, website, marketplace, user content |
| Advertising and marketing | Consumer Protection Act (misleading advertisements, endorsement guidelines for influencers); ASCI Code; TRAI commercial communication regulations (DLT registration, consent for SMS/calls); sector-specific ad rules (food, drugs, financial products) | Ads, testimonials, influencer posts, bulk SMS/WhatsApp |
| Schemes, prizes, games | Prize Chits and Money Circulation Schemes (Banning) Act, 1978; state lottery and gaming laws; Promotion and Regulation of Online Gaming Act, 2025 and its rules (confirm current status); BNS provisions on lotteries | Referral chains, cash prizes, contests needing payment, online games |
| Payments and lending | Payment and Settlement Systems Act, 2007 and RBI directions (payment aggregators, PPIs/wallets); RBI digital lending directions; NBFC registration; Banning of Unregulated Deposit Schemes Act, 2019 | Holding customer money, wallets, credit, EMI, collecting deposits or advances |
| Securities | SEBI Act and regulations: investment advice, research analysts, collective investment schemes, crowdfunding, private placement limits under Companies Act s.42 | Pooling money for returns, share offers to many people |
| Competition | Competition Act, 2002: anti-competitive agreements, abuse of dominance, merger control thresholds and deal-value threshold | Exclusive dealing, resale price maintenance, acquisitions |
| Employment | Labour codes as notified and state rules; EPF, ESI, Payment of Gratuity, POSH Act, 2013 (internal committee); contract labour; gig and platform worker provisions | Hiring, contractors, delivery partners, new office |
| IP | Trade Marks Act, Copyright Act, Patents Act, Designs Act | New brand, content, software, product design |
| Anti-corruption and AML | Prevention of Corruption Act, 1988 (including for commercial organisations); PMLA, 2002 reporting entities; foreign contribution (FCRA) for NGOs | Dealing with public officials, cash-heavy business, foreign donations |
| Stamp and property | State stamp acts; Registration Act, 1908; RERA | New lease, property deal, agreements |
| Foreign regimes | GDPR / UK GDPR, CCPA/CPRA, and others — only if the client actually offers goods or services to, or monitors, people there. Detail in `references/foreign-privacy-and-dpa.md` | EU/UK/US customers or data |

For each area that applies, look up the current requirement:

```bash
python3 scripts/fortax.py kb "<specific question, e.g. TDS on referral rewards to individuals>" --topics itr,tds,gst
```

Quote `source` and `captured`. If `match` is `weak` or `none`, write the requirement as "confirm on the
Act / notification / regulator's site" and name the law. Never fill the gap from memory as though sourced.

## Step 3 — requirements, met or not

One row per concrete requirement, not per law. "Register the internal committee under POSH" not "POSH Act".
Status is **Met**, **Not met** or **Unknown** — Unknown is fine and honest; say what would settle it.

## Step 4 — rate each risk (severity x likelihood)

**Severity** — impact if it happens:

| Level | Label | Description |
|---|---|---|
| 1 | Negligible | Minor inconvenience; no material financial, operational or reputational impact |
| 2 | Low | Limited: financial exposure < 1% of the relevant contract/deal value; minor disruption; no public attention |
| 3 | Moderate | Meaningful: 1-5% of relevant value; noticeable disruption; limited public attention possible |
| 4 | High | Significant: 5-25% of relevant value; significant disruption; likely public attention; regulatory scrutiny possible |
| 5 | Critical | Severe: > 25% of relevant value; fundamental disruption; serious reputational damage; regulatory action likely; personal liability for directors/officers possible (prosecution, officer-in-default) |

**Likelihood** — probability it happens:

| Level | Label | Description |
|---|---|---|
| 1 | Remote | Highly unlikely; no known precedent; needs exceptional circumstances |
| 2 | Unlikely | Could occur but not expected; limited precedent; needs a specific trigger |
| 3 | Possible | May occur; some precedent; triggers are foreseeable |
| 4 | Likely | Probably will occur; clear precedent; triggers are common |
| 5 | Almost certain | Expected; strong precedent or pattern; triggers present or imminent |

**Score = Severity x Likelihood.** Work it in the table or a sheet, not in your head.

| Score | Level | Colour |
|---|---|---|
| 1-4 | Low | GREEN |
| 5-9 | Medium | YELLOW |
| 10-15 | High | ORANGE |
| 16-25 | Critical | RED |

```
                    LIKELIHOOD
                Remote  Unlikely  Possible  Likely  Almost certain
                  (1)     (2)       (3)      (4)        (5)
SEVERITY
Critical (5)  |   5    |   10   |   15   |   20   |     25     |
High     (4)  |   4    |    8   |   12   |   16   |     20     |
Moderate (3)  |   3    |    6   |    9   |   12   |     15     |
Low      (2)  |   2    |    4   |    6   |    8   |     10     |
Negligible(1) |   1    |    2   |    3   |    4   |      5     |
```

What each level means for the client:

- **GREEN (1-4)** — accept with normal controls, record in the risk register, review quarterly or
  yearly, no escalation. E.g. a vendor contract with a minor deviation in a non-critical area; a routine
  NDA with a known counterparty; an administrative filing with a clear owner and date.
- **YELLOW (5-9)** — mitigate (controls or negotiation), name an owner, review monthly or on a trigger,
  brief the business owner, define what would raise it. E.g. liability cap below standard but negotiable;
  a vendor storing personal data abroad without clear safeguards; a pending regulatory change.
- **ORANGE (10-15)** — brief the promoters/board, written mitigation plan, weekly review, consider an
  advocate, full risk memo, contingency plan. E.g. uncapped indemnity in a material area; processing that
  may breach a requirement unless restructured; threatened litigation or a legal notice from a significant
  party; an IP infringement allegation with some basis; a departmental inquiry or audit.
- **RED (16-25)** — immediate escalation to promoters/board, engage an advocate now, a small response
  team with roles, notify insurers if covered, preserve documents (no deletion, see
  `fortax-legal-response` for a preservation notice), daily review, board reporting, and any statutory
  notification (e.g. DPDP breach intimation, CERT-In reporting, stock-exchange disclosure for listed
  companies). E.g. active litigation with large exposure; a personal data breach; enforcement action;
  search or summons from a department; a credible infringement claim against a core product.

Use `references/risk-assessment-memo.md` for the full memo format and the risk register fields.

## Step 5 — when it goes to an advocate

**Must**: any suit or arbitration filed by or against the client; any summons, search, show-cause or
inquiry from a regulator, police or agency (ED, SFIO, SEBI, CCI, DPB, consumer commission) — tax notices
go to `fortax-notice-reply`; any possible criminal exposure for the company or its people; anything
affecting a listed company's disclosures; matters needing board or shareholder approval where the legal
position is contested.

**Strongly recommended**: unsettled law where the client's position could set precedent; more than one
jurisdiction with conflicting rules; exposure above what the client can absorb; specialist areas
(competition, FEMA compounding, patents, anti-corruption, US FCPA or UK Bribery Act where there is a
nexus); new regulation needing a compliance programme; M&A due diligence and structuring.

**Consider**: significant contract disputes; employment claims (POSH, wrongful termination,
whistleblower); data incidents that may need notification; IP disputes on material products; insurance
coverage disputes.

When suggesting one, list what to weigh: subject expertise, the forum and state, industry familiarity,
conflict check, fee basis (fixed, hourly, retainer), existing relationships. Do not name a firm.

## Output

```
Compliance check — <initiative> — <client>, <date>

Summary: Proceed / Proceed with conditions / Needs further review
<two lines: why>

Laws and approvals it touches
| Law / regulator | Why it applies | Key requirement | Source (kb URL + captured, or "confirm") |

Requirements
| # | Requirement | Status (Met / Not met / Unknown) | Action needed | Owner | By |

Risks
| # | Risk | Severity (1-5) | Likelihood (1-5) | Score | Level | Mitigation |

Recommended actions
1. <most important>
2. …

Approvals needed
| Approver (board / shareholders / RBI / FDI government-route ministry / sector regulator / lender) | Why | Status |

Needs an advocate
- <only the points from Step 5>
```

Save next to the plan in the client folder as `YYYY-MM-DD_<initiative>_compliance.md`. Give the CA the
summary and the RED/ORANGE rows in chat.

## Rules

1. **Indian law first.** Foreign regimes only on facts that bring them in, and then say which fact.
2. **No figure from memory.** Thresholds, penalties, caps, deadlines, fees: `fortax.py kb` or "confirm"
   with the law named. Say which year's rule it is.
3. **No case law from memory.** Research and cite (`fortax-deep-research`) or leave it out.
4. **Unknown is a status.** Do not guess a requirement to Met.
5. **Nothing is filed or sent.** The CA and client apply, file and notify.

---

Credits: the compliance-check output and approach are adapted from `compliance-check`, and the severity x
likelihood framework, levels, memo, register and escalation lists from `legal-risk-assessment`, both in
[anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), © Anthropic,
Apache License 2.0 (`LICENSE-THIRD-PARTY-knowledge-work-plugins.txt`).

Changes by Fortax: adapted for Indian law and CA practice, merged with legal-risk-assessment
(knowledge-work-plugins); added the Indian law map and kb lookups; moved GDPR, CCPA, DPA and
data-subject-request material to `references/foreign-privacy-and-dpa.md`; "outside counsel" became an
advocate; connector steps removed.
