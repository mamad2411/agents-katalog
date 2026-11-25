---
name: direct-marketing
description: Provide a direct marketing compliance checklist under the Personal Data (Privacy) Ordinance (Cap 486) sections 35A-J, covering opt-in consent requirements, opt-out mechanisms, third-party data transfer, and record-keeping obligations.
---

# Direct Marketing — Skill

## Purpose

Advise on compliance with the direct marketing provisions of the Personal Data (Privacy) Ordinance (Cap 486), Part VI (s.35A-J), ensuring organisations understand their obligations regarding opt-in consent, opt-out mechanisms, third-party data transfers, and record-keeping.

## Scope

- Definition of "direct marketing" under s.35A
- Opt-in consent requirements (s.35B)
- Use of personal data in direct marketing (s.35C)
- Transfer of personal data to third parties for direct marketing (s.35D)
- Opt-out mechanisms (s.35E)
- Information requirements in marketing communications (s.35F)
- Record keeping and consent management
- Penalties for non-compliance
- Exceptions (existing customer relationships, business-to-business)

## Workflow

### 1. Determine if the Activity is Direct Marketing

**Definition** (s.35A): Direct marketing means the offering or advertising of the availability of:
- Goods, facilities, or services
- Donations or contributions (charitable purposes)

**Key characteristics**:
- Targeted to specific individuals (not mass advertising)
- Uses personal data to direct communications
- Includes: email, SMS, phone calls, postal mail, targeted social media, app notifications

**Not direct marketing**:
- Service/transactional messages (order confirmations, account updates)
- Product recall notices
- Legal/regulatory compliance communications
- B2B communications to a corporate contact at their place of work (but careful — still involves personal data)

### 2. Assess Consent Requirements

#### Use of Personal Data for Direct Marketing (s.35B and 35C)

Before using a data subject's personal data for direct marketing, you MUST:

1. **Inform** the data subject in writing:
   - The intention to use their personal data in direct marketing
   - The classes of goods/services/facilities to be marketed
   - Whether the data will be transferred to third parties for their direct marketing
   - The classes of persons to whom data will be transferred
   - Provide a means to respond (opt-in mechanism)

2. **Obtain consent**: 
   - Written consent is not strictly required for use (s.35C uses "consent" which may be given orally)
   - BUT best practice: written consent (email, signed form, ticked checkbox)
   - **No pre-ticked boxes** — consent must be affirmative

3. **Record consent**: maintain an auditable record of:
   - What the data subject was told
   - When and how they consented
   - Scope of consent (which products/services)

#### Transfer to Third Parties for Direct Marketing (s.35D)

Before transferring personal data to a third party for that third party's own direct marketing, you MUST:

1. **Inform** the data subject in writing (same as above, plus identity of the third-party class)
2. **Obtain written consent** (expressly required by s.35D — "written consent")
3. **Record consent** as above

### 3. Provide Opt-Out Mechanism

- **Every** marketing communication must include a free-of-charge opt-out mechanism
- Methods: reply email, unsubscribe link, SMS STOP, telephone opt-out
- **Response time**: cease using data within 30 calendar days of opt-out request
- **No re-marketing** after opt-out (even under different product categories)
- **Record**: maintain an opt-out register (do-not-contact list)

### 4. Marketing Communication Requirements

Each marketing message should clearly identify:
- The sender identity (organisation name)
- The purpose (marketing offer or promotion)
- The opt-out mechanism (clearly stated, easy to use)
- Contact details for opt-out requests

### 5. Third-Party Data Transfers

If an organisation wishes to transfer data to a third party for that third party's own direct marketing:

1. Separate, specific consent is required (not bundled with the initial PICS)
2. The data subject must understand who the third party is (or class of third parties)
3. Written consent is mandatory
4. Consider whether the third party has adequate data protection measures
5. Contractual data protection provisions with the third party are strongly recommended

### 6. Record-Keeping and Audit

Maintain a direct marketing compliance register:

| Field | Detail |
|-------|--------|
| Data subject ID | Internal reference |
| Consent date | When consent was obtained |
| Scope of consent | Which products/services |
| Consent mechanism | How consent was obtained |
| Third-party sharing consent? | Yes/No |
| Third-party details | Who data was transferred to |
| Opt-out date | When opt-out was received |
| Compliance verification | Audit trail |

### 7. Penalties for Non-Compliance

| Breach | Maximum Penalty |
|--------|-----------------|
| Use for direct marketing without consent (s.35C) | Fine HK$500,000 + 3 years imprisonment |
| Transfer to third parties without written consent (s.35D) | Fine HK$1,000,000 + 5 years imprisonment |
| Failure to cease use on opt-out (s.35E) | Fine HK$500,000 + 3 years imprisonment |
| Sale of personal data for direct marketing (s.35G) | Fine HK$1,000,000 + 5 years imprisonment |

### 8. Common Issues and Mitigation

| Issue | Risk | Mitigation |
|-------|------|------------|
| Pre-ticked consent boxes | Consent invalid | Implement affirmative opt-in checkboxes |
| Bundled consent (marketing with PICS) | Consent not freely given | Separate marketing consent from PICS |
| Existing customer list before 2013 | May not have compliant consent | Obtain fresh consent for post-2013 marketing |
| Third-party data purchased for marketing | Very high risk (s.35D) | Obtain written consent from data subject OR use only data collected directly |
| B2B marketing via work email | Still personal data under PDPO | Obtain business contact consent where possible |
| Opt-out not honoured | Criminal liability | Implement automated opt-out processing |
| No consent records | Unable to defend investigation | Maintain auditable consent registry |

## Key Provisions (Cap 486)

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.35A | Definition | Direct marketing meaning |
| s.35B | Information requirement | What data user must tell data subject |
| s.35C | Use for marketing | Consent required |
| s.35D | Transfer for marketing | **Written** consent required |
| s.35E | Opt-out | Right to cease use |
| s.35F | Penalty | Fine + imprisonment |
| s.35G | Sale of data for marketing | Aggravated penalty |

## Tools & Resources

- PCPD (https://www.pcpd.org.hk) — direct marketing compliance guidance, enforcement decisions
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 486 s.35A-J
- PCPD Guidance on Direct Marketing
- Direct marketing consent log template
- Opt-out register template


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
