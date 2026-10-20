---
name: e-filing
description: >
  Contains verified MeF rejection code resolution procedures (R0000-901 through R0000-905-01
  with 10-day perfection-period workflows), EFIN application and annual renewal checklists,
  and Form 8879-CORP e-signature retention rules. C-corp electronic filing, IRS MeF XML
  schema validation, acknowledgment tracking (A/R/D/P ack types), mandatory e-file threshold
  (10-return aggregation per T.D. 9972), provider type selection (ERO vs transmitter),
  advertising standards, and sanction tiers. Consult when e-filing 1120 returns, diagnosing
  MeF rejection codes, managing EFIN credentials or renewal, preparing Form 8879-CORP for
  e-signature, determining mandatory e-file applicability, onboarding a firm as an authorized
  e-file provider, or resolving e-file provider compliance issues.
---

# E-Filing

Operational skill for electronic filing of C-corporation tax returns through the IRS
Modernized e-File (MeF) system. Synthesized from MeF transmission specifications and
EFIN provider authorization requirements.

## MeF System Overview

MeF is the IRS platform for electronically filing the Form 1120 family (1120, 1120-F,
1120-H, 1120-REIT, 1120-RIC, 1120-S, 1120-X). Returns transmit as XML documents
through the IRS Integrated Enterprise Portal (IEP).

**Filing window**: Current tax year plus two prior years. Returns outside this window
must be paper-filed.

**Annual shutdown**: MeF production closes in late December (typically December 26) for
year-end maintenance and schema updates, reopening mid-to-late January with new tax
year schemas.

## Mandatory E-Filing Threshold

Effective January 1, 2024 (T.D. 9972, Taxpayer First Act Section 2301): any corporation
or preparer filing **10 or more returns** of any type during the calendar year must e-file.
The count aggregates across all return types — income, employment, excise, and information
returns.

- No separate asset-size threshold exists for corporate e-filing
- Penalty for failure to e-file when required: up to **$310 per return** (IRC Section 6721, inflation-adjusted for TY 2024+)
- Hardship waivers available via **Form 8508**

## Transmission Workflow

```
1. Preparation    → Tax software generates XML return conforming to current schema
2. Validation     → Software validates against business rules locally (pre-transmission)
3. Transmission   → Transmitter sends XML package to IRS via MeF/IEP
4. Receipt        → IRS assigns a Submission ID and begins processing
5. Acknowledgment → IRS returns electronic acknowledgment (typically within 48 hours)
```

**Fed/State program**: MeF supports single-point submission for federal and state returns
simultaneously for registered transmitters and participating state agencies.

Poll for acknowledgment status approximately 3 business days after submission.

## XML Schema and Business Rules

Schemas are published annually per tax year through the IRS Registered User Portal
(e-Services mailbox). Multiple schema versions ship per tax year (v1.0 through v5.0+),
with incremental updates for legislative changes.

**Business rules validation** occurs at two stages:

1. **Pre-transmission** — Software validates locally before submission
2. **IRS processing** — MeF re-validates on receipt; failures produce rejection acknowledgments

Business rules check for:
- Schema conformance (valid XML structure)
- Data completeness (required fields present)
- Arithmetic consistency (computed totals match component sums)
- Cross-form logic (schedules agree with main return)
- EIN/name control matching against IRS master file

Always verify the software uses the latest production schema version for the applicable
tax year before transmitting.

## Acknowledgment Types

- **Accepted (A ack)** — Passed all validation; stored in Modernized Tax Return Database (M-TRDB)
- **Rejected (R ack)** — Failed one or more business rules; includes specific error codes and descriptions
- **Duplicate (D ack)** — Return for this EIN/tax period already accepted
- **Pending (P ack)** — Still processing; poll again later

## Common Rejection Codes (Form 1120)

- **R0000-901** — Duplicate submission. Verify prior acceptance; if filing amended, mark as amended return
- **R0000-902** — Name control mismatch. First four characters of business name + EIN do not match IRS records. Verify EIN, business name spelling, and indicate name change if applicable
- **R0000-900-01** — Invalid return header data (EFIN, return type mismatch)
- **R0000-905-01** — Invalid EFIN or EFIN not listed for the transmitter
- **Arithmetic errors** — Computed line totals do not match sum of components
- **Missing required schedules** — Schedule M-1/M-3, Schedule L, or other required attachments absent

**Perfection period**: Rejected Form 1120 returns have a **10-day retransmission window**
to correct and resubmit. After this window, paper filing or additional procedures may
be required.

### Rejection Resolution Workflow

1. Identify the specific business rule code from the R ack
2. Correct the underlying data issue in the return
3. Re-validate locally against business rules
4. Retransmit within the 10-day perfection period
5. Monitor for a new acknowledgment

## Form 8879-CORP (E-File Signature Authorization)

Authorizes a corporate officer to sign Form 1120, 1120-F, or 1120-S electronically
using a self-selected Personal Identification Number (PIN).

- Both the corporate officer and the ERO sign the form
- Alternative to Form 8453-CORP (wet signature, requires mailing)
- Includes consent to electronic funds withdrawal when applicable
- ERO must retain Form 8879-CORP for **3 years** from the return due date or IRS receipt date, whichever is later
- **Not transmitted to IRS** — retained by ERO

**Decision**: Use Form 8879-CORP for PIN-based e-signature (simpler, no mailing). Use
Form 8453-CORP only if the client prefers a wet signature.

## EFIN and Provider Authorization

To e-file returns, a firm must become an **Authorized IRS e-File Provider** and obtain
an **Electronic Filing Identification Number (EFIN)** through the IRS e-Services portal.
EFINs are issued per firm, not per individual preparer.

### Application Process

1. **Create e-Services account** — Register with SSN, prior-year return data, address, contact info. Approval may take several business days.
2. **Submit application** — Select provider type (ERO for most tax firms), enter firm EIN, principals (5%+ partners or corporate officers), designate a Responsible Official with valid PTIN.
3. **Suitability check** — IRS reviews credit, tax compliance, criminal background, and prior e-file compliance. Processing: **up to 45 days**.

**Fingerprinting**: Required for individuals without professional licenses (CPA, attorney,
EA). Scheduled via the e-file application summary page through IRS-authorized Livescan
vendors.

### Provider Types

- **Electronic Return Originator (ERO)** — Most common for tax firms. Prepares and originates returns for e-filing. Responsible for obtaining taxpayer signatures.
- **Transmitter** — Operates the communication link with IRS MeF. Must pass ATS certification. Select only if firm operates its own transmission channel.
- **Software Developer** — Builds MeF-compliant tax software. Must pass ATS certification.
- **Intermediate Service Provider (ISP)** — Routes returns between EROs and transmitters.

### Responsible Official

- Must have a valid PTIN and pass the suitability check
- Oversees the firm's e-file operations and compliance
- Must update information within **30 days** of any changes
- Each firm must designate at least one

### EFIN Renewal

- Requires **annual renewal** through e-Services
- No fee for renewal
- Failure to renew results in deactivation — the firm cannot transmit returns
- Renewal confirms firm details, principals, and responsible official remain current

## Binary Attachment (PDF) Requirements

PDF attachments are permitted for supporting statements where no XML schema element
exists. File requirements:
- Use straightforward, descriptive file names
- Must be legible and under IRS file size limits
- Retain copies for **3 years**
- Scanned Form 8453-CORP may be attached as PDF when not using Form 8879-CORP

## Record Retention Requirements

- **Form 8879-CORP / Form 8453-CORP** — 3 years from return due date or IRS receipt date, whichever is later
- **Electronic return data** — 3 years (per Rev. Proc. 2007-40)
- **Advertising with fee information** — 36 months from last use
- **PDF binary attachments** — 3 years

## Advertising Standards

IRS-authorized e-file providers must follow advertising rules (Publication 3112,
Rev. Proc. 2007-40):

**Prohibited**: Using "Internal Revenue Service" or "IRS" in firm name, claiming
guaranteed refund timing, using IRS logo/insignia/Treasury seals, implying a special
IRS relationship.

**Permitted**: Using the "IRS e-file" logo without endorsing elements.

Non-compliant advertising triggers warnings escalating to sanctions (reprimand,
suspension, or expulsion from the e-file program).

## Provider Sanctions

- **Level 1** — Written reprimand
- **Level 2** — Suspension from e-file program
- **Level 3** — Expulsion from e-file program

Triggers include advertising violations, unauthorized disclosure of taxpayer data,
filing without proper authorization, and failure to comply with Rev. Proc. 2007-40.

## Decision Points

1. **Is e-filing required?** Count all return types filed during the calendar year. If 10+, mandatory (TY 2024+).
2. **Is the tax year within MeF's filing window?** Current year + 2 prior years only. Older returns must be paper-filed.
3. **Form 8879-CORP or Form 8453-CORP?** Use 8879-CORP for PIN-based e-signature (standard). Use 8453-CORP only if wet signature and mailing is preferred.
4. **Rejection received?** Identify the business rule code, correct the issue, retransmit within the 10-day perfection period.
5. **Schema version current?** Verify software uses the latest production schema for the applicable tax year.
6. **EFIN renewal current?** Check e-Services annually. Deactivated EFIN prevents filing.
7. **Which provider type?** Most tax firms select ERO. Choose transmitter only if operating the MeF communication channel.
8. **Fingerprinting needed?** Only for individuals without CPA, attorney, or EA credentials.

## Authoritative References

- IRC Section 6011(e) — Required electronic filing of returns
- IRC Section 6721 — Penalty for failure to file correct information returns
- T.D. 9972 — Final regulations reducing e-file threshold to 10 returns
- Taxpayer First Act (P.L. 116-25) Section 2301 — E-filing mandate authority
- IRS Publication 3112 — IRS e-file Application and Participation
- IRS Publication 4163 — Modernized e-File Information for Authorized IRS e-File Providers
- IRS Publication 4164 — MeF Guide for Software Developers and Transmitters
- IRS Publication 4557 — Safeguarding Taxpayer Data
- Rev. Proc. 2007-40 — E-file provider participation standards
- Form 8879-CORP Instructions — E-file signature authorization
- Form 8453-CORP Instructions — Corporate declaration for e-file

## Supporting References

Read these for deeper detail on specific topics:

- `references/mef-e-filing.md` — Full MeF system specification including XML schema structure, business rule validation stages, transmission process, acknowledgment types, common rejection codes with resolution procedures, Form 8879-CORP requirements, binary attachment rules, ATS certification process, and year-by-year schema version table for Form 1120. Read when troubleshooting a specific rejection code, verifying schema version compatibility, or reviewing MeF transmission procedures in detail.
- `references/efin-provider.md` — Complete EFIN application process (3-step), provider type definitions and selection guidance, Responsible Official requirements, annual renewal procedures, PTIN requirements, advertising standards, sanction tiers, and record retention schedules. Read when onboarding a new firm for e-filing, managing EFIN renewal, resolving provider compliance issues, or reviewing advertising rules.

## Cross-Plugin References

For return preparation that feeds into e-filing:
- Invoke `tax-prep:form-1120-prep` for completed Form 1120 data and return assembly
- Invoke `tax-prep:business-tax-schema` for tax data structure and field definitions
- Invoke `tax-prep:tax-forms` for supporting schedule preparation and form requirements

For state e-filing procedures:
- Invoke `tax-prep:state-returns` for state-specific electronic filing requirements including Florida e-filing procedures

For compliance and planning context:
- Invoke `tax-prep:tax-compliance` for filing deadline management and compliance calendar
- Invoke `tax-prep:tax-planning` for filing strategy and extension decisions
- Invoke `tax-prep:nol-tracking` for NOL carryforward data included in returns

For entity and engagement context:
- Invoke `accounting-foundation:entity-profile` for corporate entity details (EIN, business name, fiscal year) needed for MeF header data and name control validation
- Invoke `firm-operations:engagement-management` for engagement workflow and client authorization tracking
- Invoke `firm-operations:practice-management` for firm-level EFIN and provider credential management
- Invoke `firm-operations:quality-compliance` for e-file quality review procedures
- Invoke `firm-operations:data-governance` for taxpayer data safeguarding (Publication 4557 compliance)
- Invoke `firm-operations:workflow-automation` for e-filing task automation and status tracking

## Cross-Plugin Consumers

- `tax-prep:form-1120-prep` — e-filing status for return assembly and final review
- `tax-prep:tax-compliance` — e-file confirmation for compliance tracking and deadline management
- `tax-prep:state-returns` — federal acceptance status as prerequisite for state e-filing
- `firm-operations:engagement-management` — e-file acknowledgment status for engagement milestone tracking
- `firm-operations:quality-compliance` — e-file rejection rates for quality metrics
