---
name: fortax-india-dpdp-act
description: India's Digital Personal Data Protection Act, 2023 and DPDP Rules, 2025 for a CA and client — does the Act apply, data fiduciary duties (notice, consent, legitimate uses, security, breach intimation, erasure, processor contracts), data principal rights and grievance, children's data, Significant Data Fiduciary duties, consent managers, transfers abroad, exemptions, the Data Protection Board and the penalty schedule — and a gap assessment with a compliance checklist. Use for "DPDP lagega kya", "privacy policy DPDP ke hisaab se", "data breach hua, Board ko kab batana hai", "consent form banao", "DPDP penalty kitni".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "https://github.com/mukul975/Privacy-Data-Protection-Skills (Apache-2.0, Copyright 2025 Mahipal)"
---

# India DPDP Act, 2023

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Typical asks: "client ki app customer data leti hai, DPDP me kya karna hoga", "employee data ke liye consent chahiye?",
"breach notice ka format", "DPDP gap assessment karo", "hum foreign client ke liye data process karte hain, lagega?".

This is a map of the Act, not a legal opinion. Section numbers are pointers to where to read.

## Currency — read before advising

- The Act is Act No. 22 of 2023 (assent 11 August 2023). The **DPDP Rules, 2025** were notified in
  November 2025 with **phased commencement**: provisions on the Board in force at once, consent manager
  registration after about 12 months, and most fiduciary obligations (notice, security, breach
  intimation, children, SDF, rights) after about 18 months. Confirm the exact commencement dates, and
  any later amendment that changes them, before telling a client what is already enforceable.
- Run `python3 scripts/fortax.py kb "DPDP Rules commencement <topic>"` and quote `source` and `captured`.
  If `match` is `weak` or `none`, say "confirm in the DPDP Rules, 2025 as notified (meity.gov.in / egazette)".
- Periods and thresholds marked *(Rules — confirm)* below are from the Rules as notified and are the kind
  of figure that gets amended. Penalty maxima are in the Schedule to the Act.
- An earlier version of the source text this skill adapts had several section references wrong and treated
  the Rules as a draft; `references/source-notes.md` lists what was corrected.

## Step 1 — does the Act apply?

| Question | If yes |
|---|---|
| Is it **digital** personal data, or non-digital data later digitised? (s.3) | In scope. Purely paper records never digitised are outside |
| Processed **in India**? Or outside India in connection with offering goods or services to people in India? (s.3) | In scope |
| Personal data an individual makes public themselves, or that someone is legally obliged to make public? (s.3(c)) | Outside the Act |
| Personal use by an individual for a personal or domestic purpose? (s.3(c)) | Outside |
| Indian client processing data of people **outside India** under a contract with a foreign person (BPO/KPO/IT outsourcing)? (s.17(1)(d)) | Most obligations exempt; security safeguards and processor responsibility still apply — confirm the exact carve-back in s.17(1) |
| Processing to enforce a legal right or claim, by courts, for preventing or investigating offences, for approved mergers/schemes, or to ascertain financial information of loan defaulters? (s.17(1)) | Exempt from most obligations |
| Research, archiving or statistics under prescribed standards? (s.17(2)(b)) | Exempt as prescribed |
| A notified class of fiduciary (e.g. startups) exempted from some duties? (s.17(3)) | Check the notification |

Then name the client's role for each activity: **data fiduciary** (decides purpose and means), **data
processor** (processes on a fiduciary's behalf), or both. A CA firm is itself a fiduciary for its staff
and client-contact data, and often a processor for client payroll and books.

## Key definitions (s.2)

| Term | Meaning | Section |
|---|---|---|
| Data Principal | The individual the data relates to; for a child, includes the parent or lawful guardian; for a person with a disability, includes the lawful guardian acting on their behalf | s.2(j) |
| Data Fiduciary | Any person who alone or with others determines the purpose and means of processing | s.2(i) |
| Data Processor | Any person who processes personal data on behalf of a data fiduciary | s.2(k) |
| Consent Manager | A person registered with the Board who acts as a single point of contact for the data principal to give, manage, review and withdraw consent | s.2(g) |
| Child | An individual under 18 | s.2(f) |
| Personal data | Any data about an individual who is identifiable by or in relation to that data | s.2(t) |
| Personal data breach | Unauthorised processing or accidental disclosure, acquisition, sharing, use, alteration, destruction or loss of access that compromises confidentiality, integrity or availability | s.2(u) |
| Significant Data Fiduciary | A fiduciary or class notified as such under s.10 | s.2(z) |

The Act has **no separate "sensitive personal data" category**: health, financial or biometric data is
personal data, and its sensitivity matters for SDF designation and for penalty (s.33(2)). Sectoral rules
(RBI, IRDAI, health) can still add requirements.

## Step 2 — the fiduciary's obligations

### Grounds for processing (s.4)
Only for a lawful purpose, and only with **consent** (s.6) or for a **certain legitimate use** (s.7).
There is no "legitimate interest" or "contract necessity" ground as in GDPR.

### Notice (s.5)
With or before the request for consent, a notice telling the data principal:
1. the personal data and the purpose of processing;
2. how to exercise rights under s.6(4) (withdrawal) and s.13 (grievance);
3. how to complain to the Board.

- In English or any of the 22 languages in the Eighth Schedule to the Constitution, at the principal's option.
- For consent given **before** the Act commenced, the fiduciary must give this notice as soon as reasonably
  practicable (s.5(2)); processing may continue until the principal withdraws.
- *(Rules — confirm)* The notice must be understandable on its own, give an itemised description of the
  data, the specified purpose and the goods or services enabled, and a link or means to withdraw consent,
  exercise rights and complain.

### Consent (s.6)

| Requirement | Detail |
|---|---|
| Nature | Free, specific, informed, unconditional and unambiguous, by clear affirmative action |
| Scope | Limited to data necessary for the specified purpose; any part of a consent that infringes the Act is invalid to that extent |
| Bundling | No bundled consent for unrelated purposes; no pre-ticked boxes |
| Language | Clear and plain, in English or an Eighth Schedule language, with the fiduciary's DPO/contact |
| Withdrawal | At any time, as easily as consent was given (s.6(4)); consequences of withdrawal are borne by the principal; withdrawal does not affect processing done before it |
| Effect of withdrawal | Fiduciary must, within a reasonable time, stop processing and make its processors stop, unless a law requires or allows retention (s.6(6)) |
| Consent manager | Principal may give, manage, review and withdraw consent through a registered consent manager (s.6(7)-(9)) |
| Proof | Where consent is the ground, the fiduciary must prove notice was given and consent obtained (s.6(10)) — keep records |

### Certain legitimate uses — processing without consent (s.7)

| Clause | Use |
|---|---|
| s.7(a) | For the specified purpose for which the principal **voluntarily provided** the data, where they have not said they do not consent (e.g. a customer sends their number to receive a receipt) |
| s.7(b) | By the State or its instrumentalities to provide a subsidy, benefit, service, certificate, licence or permit, on existing consent or State records |
| s.7(c) | By the State in performing a function under law, or in the interest of sovereignty, integrity or security |
| s.7(d) | To fulfil a legal obligation to disclose information to the State |
| s.7(e) | To comply with a judgment, decree or order under Indian law, or one on contractual or civil claims under foreign law |
| s.7(f) | To respond to a medical emergency involving a threat to life or health |
| s.7(g) | To provide medical treatment or health services during an epidemic or threat to public health |
| s.7(h) | To ensure safety of, or assistance to, individuals during a disaster or breakdown of public order |
| s.7(i) | For **employment purposes**, or to safeguard the employer from loss or liability — e.g. preventing corporate espionage, keeping trade secrets, IP or classified information confidential, or providing a service or benefit the employee asks for |

For a client: payroll, attendance, statutory PF/ESI/TDS records and background checks are usually s.7(i)
or s.7(d); marketing to employees or sharing their data with a lender is not, and needs consent.

### General obligations (s.8)

| Sub-section | Obligation |
|---|---|
| s.8(1) | Fiduciary is responsible for compliance, including for processing by its processors, whatever any agreement or the principal's own failure |
| s.8(2) | Engage or involve a processor **only under a valid contract** |
| s.8(3) | Ensure completeness, accuracy and consistency where data is used for a decision about the principal or disclosed to another fiduciary |
| s.8(4) | Implement appropriate technical and organisational measures |
| s.8(5) | Take **reasonable security safeguards** to prevent a breach, including by processors |
| s.8(6) | On a breach, **intimate the Board and each affected principal** in the prescribed form and manner |
| s.8(7) | **Erase** the data (and make processors erase) when consent is withdrawn or it is reasonable to assume the purpose is no longer served, unless retention is needed to comply with law |
| s.8(8) | The purpose is deemed no longer served if the principal does not approach the fiduciary for the prescribed period |
| s.8(9) | Publish the business contact information of the DPO (if any) or a person who can answer questions |
| s.8(10) | Set up an effective grievance redressal mechanism |

*(Rules — confirm)* **Security safeguards** include at least: encryption, obfuscation, masking or virtual
tokens; access control; logs and monitoring to detect unauthorised access; backups for continuity; and
retaining logs and personal data for at least **one year** for detection and investigation; with matching
terms in processor contracts.

*(Rules — confirm)* **Breach intimation:** to each affected principal **without delay** — what happened,
likely consequences, mitigation, safety steps they can take, and a contact; to the Board **without delay**,
followed by a detailed report (facts, cause, mitigation, person responsible if known, remedial steps,
intimations made) **within 72 hours** of becoming aware, or longer if the Board allows. Separate CERT-In
reporting under the IT Act may also apply — check its directions.

*(Rules — confirm)* **Erasure periods:** large e-commerce entities, online gaming intermediaries and social
media intermediaries above user thresholds in the Rules' Third Schedule must erase data after a set period
of inactivity (three years), with **48 hours'** notice to the principal before erasure. Other fiduciaries
erase when the purpose is served, subject to laws requiring retention (Companies Act, GST and income-tax
record periods, PMLA KYC).

## Step 3 — children and persons with disability (s.9)

| Requirement | Detail |
|---|---|
| Who is a child | Under 18 — no lower age band (s.2(f)) |
| Verifiable consent | Of the parent or lawful guardian before processing a child's data; of the lawful guardian for a person with a disability (s.9(1)) |
| No detrimental processing | Nothing likely to cause a detrimental effect on a child's well-being (s.9(2)) |
| No tracking or targeting | No tracking, behavioural monitoring or targeted advertising directed at children (s.9(3)) |
| Exemptions | Classes of fiduciaries or purposes may be exempted from s.9(1) and (3) (s.9(4)); a fiduciary whose processing is verifiably safe may be allowed a lower age (s.9(5)) |

*(Rules — confirm)* Verifiable parental consent means due diligence that the person consenting is an
identifiable adult, using details already held or a virtual token from an authorised entity (such as
DigiLocker). The Rules exempt some classes (clinical and health establishments, educational institutions,
child-care centres, for defined purposes).

## Step 4 — Significant Data Fiduciary (s.10)

The Central Government may notify a fiduciary or class as an SDF considering: volume and sensitivity of data;
risk to principals' rights; potential impact on sovereignty and integrity of India; risk to electoral
democracy; security of the State; public order.

| Obligation | Detail |
|---|---|
| Data Protection Officer | Based in India, represents the SDF, responsible to its board or similar governing body, point of contact for grievances (s.10(2)(a)) |
| Independent data auditor | To evaluate compliance (s.10(2)(b)) |
| DPIA | Periodic Data Protection Impact Assessment (s.10(2)(c)(i)) |
| Periodic audit | s.10(2)(c)(ii) |
| Other measures | As prescribed (s.10(2)(c)(iii)) |

*(Rules — confirm)* DPIA and audit **once every 12 months**, significant findings reported to the Board;
due diligence that algorithmic software used does not risk principals' rights; and processing of personal
data specified by the Government (on a committee's recommendation) with a restriction on transfer outside
India.

## Step 5 — data principal rights and duties (s.11-15)

| Right | Section | Detail | Suggested implementation |
|---|---|---|---|
| Information | s.11(1) | A summary of the personal data processed and the processing activities; identities of all other fiduciaries and processors it was shared with, and what was shared | Request form on site/app; privacy page in English and the languages customers use; a sharing register |
| Correction and erasure | s.12 | Correction, completion and updating; erasure unless retention is needed for the purpose or by law | Self-service correction; an erasure workflow that checks legal retention first |
| Grievance redressal | s.13 | A readily available means of grievance redressal, answered within the prescribed period; the principal must exhaust it before going to the Board | Grievance officer named; *(Rules — confirm)* respond within **90 days** at most |
| Nomination | s.14 | Nominate a person to exercise the rights on death or incapacity | Nomination form |

Right to information does not apply to sharing with a fiduciary authorised by law to obtain data for
preventing, detecting or investigating offences (s.11(2)).

**Duties of the principal (s.15)** — unusual in privacy law: comply with applicable law; not impersonate
another person; not suppress material information when providing data for an identity or address document
issued by the State; not register a false or frivolous grievance or complaint; give only verifiably
authentic information when seeking correction or erasure. Breach: penalty up to **₹10,000** (Schedule).

Replies to principals' requests are drafted with `fortax-legal-response`.

## Step 6 — consent managers (s.6(7)-(9))

Registered with the Board; accountable to the data principal; a single point of contact to give, manage,
review and withdraw consent; must be interoperable, accessible and transparent.

*(Rules — confirm)* Conditions for registration include: a company incorporated in India; net worth of at
least **₹2 crore**; sound finances and management; a platform that is interoperable and independently
certified; no conflict of interest with fiduciaries it serves; records of consents given, withdrawn and
shared kept for at least **seven years**; acting in a fiduciary capacity towards the principal. The Board
can suspend or cancel registration. (The source text also gave a three-year registration validity from the
draft Rules — verify before relying on it.)

## Step 7 — transfer outside India (s.16)

| Element | Detail |
|---|---|
| Default | Transfer allowed to any country **except** one the Central Government restricts by notification (s.16(1)) |
| Restricted list | Check for any notification before advising — none had been notified when the source was written |
| Stricter laws prevail | Any law giving a higher degree of protection or restriction for a class of data or fiduciary continues to apply (s.16(2)) — e.g. RBI's storage of payment system data in India, sectoral rules for insurance, telecom, government data |
| *(Rules — confirm)* | Transfers are subject to requirements the Government may specify on making data available to a foreign State or its agencies |
| Contracts | Not mandated by the Act, but a transfer clause with safeguards in the vendor contract is good practice |

## Step 8 — enforcement

**Data Protection Board of India (s.18 onwards).** An adjudicating body with a digital office: acts on a
principal's complaint (after the grievance route), a Government or court reference, or a fiduciary's breach
intimation; can direct urgent remedial measures, inquire, impose penalties, accept a **voluntary
undertaking** (s.32), and refer disputes to mediation (s.31). Civil courts are barred on matters the Board
decides (s.39). **Appeal** to the Telecom Disputes Settlement and Appellate Tribunal (TDSAT) within 60 days
(s.29) — confirm the period. Orders of TDSAT are executable as decrees.

**Penalty Schedule (s.33 and Schedule)** — maxima; the Board decides the amount considering nature, gravity
and duration, type of data, repetition, gain made or loss avoided, mitigation, proportionality and impact
(s.33(2)):

| # | Breach | Maximum penalty |
|---|---|---|
| 1 | Failure to take reasonable security safeguards to prevent a breach (s.8(5)) | ₹250 crore |
| 2 | Failure to intimate the Board or affected principals of a breach (s.8(6)) | ₹200 crore |
| 3 | Breach of additional obligations for children (s.9) | ₹200 crore |
| 4 | Breach of additional SDF obligations (s.10) | ₹150 crore |
| 5 | Breach of duties by a data principal (s.15) | ₹10,000 |
| 6 | Breach of a voluntary undertaking accepted by the Board (s.32) | Up to the amount applicable to the breach for which the proceedings were started |
| 7 | Breach of any other provision of the Act or Rules | ₹50 crore |

Penalties go to the Consolidated Fund of India; there is no compensation to the principal under this Act.

**Other amendments (s.44).** Section 43A of the IT Act, 2000 (compensation for failure to protect sensitive
data) and the SPDI Rules, 2011 fall away when s.44 commences; the RTI Act's personal-information exemption
(s.8(1)(j)) is amended. Until commencement, the IT Act regime still applies — confirm dates.

## Step 9 — gap assessment and compliance programme

Work through the client's processing, one activity per row (customers, website/app users, employees,
vendors' staff, children, CCTV):

```
DPDP gap assessment — <client> — <date>
Role: fiduciary / processor / both        Commencement dates relied on: <dates, source>

| Activity | Data | Ground (consent / s.7 clause) | Notice | Consent record | Processor contract | Security | Retention and erasure | Rights process | Children | Transfer abroad | Gap | Priority |
```

Then the programme — tick what exists, list what does not:

| Component | What good looks like |
|---|---|
| Data inventory | Register of personal data by activity, system, purpose, ground, retention, processors, countries |
| Grievance officer / DPO contact | Named person, business contact published on site and in notices (s.8(9)); DPO in India if SDF |
| Privacy notice | Standalone notice meeting s.5 and the Rules, in English and the languages the client's customers use, published on the site/app |
| Consent capture | Unbundled, no pre-ticked boxes, withdrawal as easy as consent, logs kept; consent manager integration if used |
| Legacy data | Notice sent to principals whose data was collected before commencement (s.5(2)) |
| Employee data | Mapped to s.7(i) or s.7(d); consent for anything beyond employment purposes |
| Security safeguards | Encryption/masking, access control, logging retained per Rules, backups, vendor security clauses (s.8(5)) |
| Breach response | Written procedure: detect, contain, intimate principals and Board per Rules, CERT-In where applicable, log |
| Processor contracts | Written contract with every processor (s.8(2)): process only on instructions, safeguards, breach notice to fiduciary, sub-processor control, erasure on exit, audit or assurance |
| Retention and erasure | Schedule mapped to legal retention periods; erasure on purpose served or withdrawal (s.8(7)); Rules periods where applicable |
| Rights handling | Intake, identity check, response within Rules period, log (s.11-14) |
| Children | Age gating, verifiable parental consent, no tracking or targeted ads (s.9) |
| Cross-border | Transfers mapped; restricted-country check; sectoral localisation (s.16) |
| Training | Annual DPDP training for staff who handle personal data |
| Board reporting | Periodic compliance status to the board; DPIA/audit if SDF |

Save as `YYYY-MM-DD_DPDP_gap_<client>.xlsx` (the table) and `.md` (findings) in the client folder. For a
new product or campaign, run `fortax-legal-compliance-check` for the other laws; for a vendor contract,
`fortax-contract-review`.

## Rules

- **Commencement first.** Never tell a client an obligation is enforceable without checking its date.
- **Every figure sourced.** Rules periods, thresholds and penalty amounts: `fortax.py kb` with source and
  captured date, or "confirm in the Act / DPDP Rules, 2025".
- **No case law from memory.** There is little yet; cite or leave out.
- **Nothing is filed or intimated from here.** Breach intimations to the Board and principals are drafted;
  the client submits them.

---

Credits: adapted from the `india-dpdp-act` skill in
[mukul975/Privacy-Data-Protection-Skills](https://github.com/mukul975/Privacy-Data-Protection-Skills),
Copyright 2025 Mahipal, Apache License 2.0 (`LICENSE-THIRD-PARTY-privacy-data-protection-skills.txt`).

Changes by Fortax: adapted for Indian law and CA practice, not merged with another source; corrected
section references (s.5(2), s.7 clauses, s.13/s.14) and the penalty schedule (voluntary undertaking row);
updated the Rules from draft to the DPDP Rules, 2025 with phased commencement, marked for confirmation;
added applicability test, s.17 exemptions, s.44 amendments, gap assessment workflow and kb lookups;
removed the fictional company compliance programme (names and URL) and the USD conversions.
