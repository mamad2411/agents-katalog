---
name: publicist-us-compliance
description: Apply before US earned-media work involving commercial email, endorsements, public-company information, journalist data, or broadcast sponsorship. Covers CAN-SPAM, FTC, SEC Reg FD, state privacy, and FCC rules.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# US compliance gate, US market

Use this as the compliance gate for every US earned-media activity. Pair it with `publicist-us` and the relevant US platform skill.

---

## Legal framework (must recheck at task time)

| Law/Regulation | Scope | Key Requirement | Penalty |
|---|---|---|---|
| **CAN-SPAM Act (2003)** | Commercial email | Opt-out, physical address, honest subject, no harvested lists | $50,120/violation |
| **FTC Act Section 5** | Deceptive practices | Material connections disclosed, clear & conspicuous | $50,120/violation |
| **FTC Endorsement Guides** | Influencer/creator content | #ad/#sponsored, clear disclosure | $50,120/violation |
| **SEC Reg FD** | Public companies | No selective disclosure; broad public dissemination | SEC enforcement |
| **State Privacy Laws** | Personal data | Opt-out, deletion, sensitive data limits | $2,500-7,500/violation |

---

## CAN-SPAM Act (every commercial email)

### Mandatory requirements
| Requirement | Implementation |
|---|---|
| **Accurate headers** | From, To, Reply-To = real identity |
| **Non-deceptive subject** | Subject = actual content |
| **Ad identification** | Clear "Advertisement" or similar |
| **Physical address** | Valid postal address in footer |
| **Opt-out mechanism** | One-click unsubscribe, honor in 10 business days |
| **No harvested lists** | No purchased/scraped email lists |

### PR email template (compliant)
```
Subject: [Beat] [Topic]: [Specific value]

Hi [First Name],

[Personalized opening referencing their work]

[1-2 sentences: news hook + evidence]
[One sentence: what you're offering, such as an interview, data, or an expert]
[1 sentence: why their readers care now]

Available [specific days/times] for brief call.
Press kit: [link]
Direct: [phone] | [email]

[Your Full Name]
[Title], [Company]
[Physical Address: Street, City, State ZIP]
[Phone] | [Email]

Unsubscribe: [one-click link] | Reply "REMOVE"
```

### PR exemptions (narrow)
- **Transactional/relationship emails**. Not "commercial" if primarily transactional
- **B2B existing customer**. Narrow, must be existing business relationship
- **Pitch emails**. **Grey area.** Safest to include opt-out + physical address.

---

## FTC endorsements & native advertising

### Material connections (must disclose)
| Relationship | Disclosure Required |
|---|---|
| **Paid partnership** | #ad / #sponsored / "Paid partnership with @brand" |
| **Free product** | "Thanks @brand for the free [product]" |
| **Affiliate link** | "Affiliate link" / #ad |
| **Employee/friend** | "My company..." / "My friend @X works at..." |
| **Ownership stake** | "I own shares in..." |

### Disclosure standards
| Requirement | Standard |
|---|---|
| **Clear & conspicuous** | Unavoidable, same format as content |
| **Platform-native** | Instagram: overlay + caption; YouTube: verbal + description |
| **Proximity** | Near claim/endorsement, not buried |
| **Language** | Plain English, same language as content |

### Native advertising
| Format | Disclosure |
|---|---|
| **Sponsored content** | "Sponsored" / "Paid Post" in headline + byline |
| **In-feed native** | "Sponsored" label adjacent to content |
| **Recommendation widget** | "Sponsored" / "Promoted" header |
| **Influencer post** | #ad / #sponsored in first 3 lines |

---

## SEC Regulation FD (public companies)

### Core rule
> **No selective disclosure** of material non-public information. Must disclose broadly to public simultaneously.

### Material information triggers
| Event | Action |
|---|---|
| **Earnings/guidance change** | Wire service (Business Wire, PR Newswire, GlobeNewswire) |
| **M&A/major contract** | Simultaneous public release |
| **Executive departure** | 8-K + press release |
| **Product recall/safety** | Immediate public disclosure |
| **Regulatory action** | Simultaneous public disclosure |

### Compliance protocol
1. Draft the release and send it for legal review.
2. Get approval from the CEO or CFO and the general counsel.
3. Distribute it through a wire service and the company website at the same time.
4. Monitor media pickup and analyst calls.
5. Keep the records for five years.

### Selective disclosure prohibited
- Do not brief analysts or selected journalists before public release.
- Do not post social media teasers before the wire release.
- Release through the wire service, company website, and social media at the same time.

---

## State privacy law patchwork (2024-25)

### Active laws (must comply if processing residents' data)

| Law | State | Effective | Key PR Obligations |
|---|---|---|---|
| **CCPA/CPRA** | CA | 2020/2023 | Opt-out sale, deletion, sensitive data limits, "Do Not Sell" link |
| **VCDPA** | VA | 2023 | Opt-out, deletion, appeals, data protection assessments |
| **CPA** | CO | 2023 | Universal opt-out (GPC), sensitive data consent |
| **CTDPA** | CT | 2023 | Children's data, targeted ads opt-out |
| **UCPA** | UT | 2023 | Business-friendly, opt-out sale |
| **ICDPA** | IA | 2025 | Similar to VCDPA |
| **MCDPA** | MT | 2024 | Similar to CTDPA |
| **TIPA** | TN | 2025 | NIST privacy framework alignment |
| **OCPA** | OR | 2024 | Strong consumer rights |
| **TDPSA** | TX | 2024 | Business-friendly, controller/processor duties |

### PR data processing checklist
- [ ] **Lawful basis** for journalist contacts (legitimate interest = primary)
- [ ] **Data minimization**, only name, outlet, beat, contact
- [ ] **Opt-out honored**, "Reply REMOVE" in every email
- [ ] **Data retention**, 2 years post-last-contact default
- [ ] **Vendor contracts**, DPAs with CRM, email, monitoring tools
- [ ] **Cross-border**, SCCs if using US tools for EU/UK journalists
- [ ] **Sensitive data**, Avoid collecting race, health, political, biometric

### Consent vs legitimate interest
| Scenario | Basis |
|---|---|
| **Media list building** | Legitimate interest (Art. 6 GDPR / CCPA §1798.140) |
| **Newsletter signup** | Explicit consent |
| **Event registration** | Contract performance |
| **Media monitoring** | Legitimate interest |
| **Crisis contact** | Vital interests / legal obligation |

---

## FCC & broadcast compliance

### Sponsorship identification
| Scenario | Requirement |
|---|---|
| **Paid TV/radio placement** | "Sponsored by [Company]" announced |
| **VNR/B-roll distribution** | Source identification on materials |
| **Satellite media tour** | Disclosure to stations |
| **Paid social boosting** | Platform ad library + #ad |

### Political file
| Trigger | Action |
|---|---|
| **Political ads** | Public inspection file at station |
| **Issue ads (candidate)** | FCC political file |
| **Candidate appearance** | Equal time rule |

---

## Compliance checklist (per pitch/campaign)

### Pre-launch
- [ ] **CAN-SPAM**. Opt-out link, physical address, honest subject
- [ ] **FTC**. Disclosures for any material connections
- [ ] **SEC Reg FD**. Distribute public-company material information through a wire service first.
- [ ] **State privacy**. Opt-out honored, vendor DPAs signed
- [ ] **FCC**. Sponsorship ID for broadcast/social paid
- [ ] **Records**. 5-year retention (SEC), 3-year (FTC)

### Per communication
- [ ] **Opt-out link** in every commercial email
- [ ] **Physical address** in every email footer
- [ ] **Honest subject line** (no clickbait/deception)
- [ ] **Disclosures** for any paid/expert relationships
- [ ] **Opt-out honored** within 10 business days (CAN-SPAM) / 15 days (CCPA)

### Data lifecycle
- [ ] **Retention policy** documented (2 years default)
- [ ] **Deletion process** for opt-outs (10 days CAN-SPAM, 45 days CCPA)
- [ ] **Access/deletion requests** process (45 days CCPA)
- [ ] **Vendor DPAs** for all processors (CRM, email, monitoring)
- [ ] **Cross-border SCCs** if any journalist data leaves US

---

## Patterns to avoid
- Do not use harvested email lists. CAN-SPAM restricts their use.
- Add an unsubscribe method and a physical address to commercial email.
- Require influencers to disclose material connections.
- Do not give analysts material information before public release.
- Check cross-border data rules before storing EU journalist data in a US service.

---

## References
- `https://www.ftc.gov/can-spam`, CAN-SPAM compliance
- `https://www.ftc.gov/endorsements`, Endorsement guides
- `https://www.sec.gov/regfd`, Regulation FD
- `https://iapp.org/resources/article/us-state-privacy-legislation-tracker/`, State tracker
- `https://www.fcc.gov/media`, FCC media rules
- `skills/publicist-us/references/law-and-ethics.md`

## What this skill does not do
- It does not provide legal advice. Escalate legal questions to counsel.
- It does not run an automated compliance check.
- It has no MCP or CLI tools; it is a reference.
