---
name: ccpa-checklist
description: "When to activate: CCPA, CPRA, California privacy, consumer rights, opt-out, data deletion, privacy notice, California residents, do not sell"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: compliance
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# CCPA / CPRA Checklist

## Applicability Thresholds

CCPA/CPRA applies to for-profit businesses that collect California residents' personal information AND meet **at least one** of:

| Threshold | Value |
|-----------|-------|
| Annual gross revenue | > $25 million |
| Personal records bought/sold/shared annually | ≥ 100,000 consumers or households |
| Revenue from selling/sharing personal info | ≥ 50% of annual revenue |

CPRA (effective Jan 1, 2023) raises the data threshold to 100,000 (was 50,000 under original CCPA).

## Consumer Rights

| Right | What it means | Response deadline |
|-------|--------------|-------------------|
| Right to Know | What categories/pieces of PI collected, sources, purposes, third parties | 45 days (+ 45 extension) |
| Right to Delete | Request deletion of their PI (with exceptions) | 45 days (+ 45 extension) |
| Right to Correct (CPRA) | Correct inaccurate PI | 45 days (+ 45 extension) |
| Right to Opt-Out | Stop sale or sharing of their PI | Honored within 15 business days |
| Right to Limit (CPRA) | Limit use/disclosure of sensitive PI | Honored within 15 business days |
| Right to Non-Discrimination | No penalty for exercising rights | Ongoing |
| Right to Data Portability | Receive their data in portable format | 45 days (+ 45 extension) |

## Privacy Notice Requirements

Must disclose at or before collection:

- [ ] Categories of personal information collected
- [ ] Purposes for which each category is used
- [ ] Whether PI is sold or shared (and categories of recipients)
- [ ] Retention period for each category (or criteria for determining it — CPRA)
- [ ] Consumer rights and how to exercise them
- [ ] Contact info for privacy requests
- [ ] "Do Not Sell or Share My Personal Information" link (if applicable)
- [ ] "Limit the Use of My Sensitive Personal Information" link (if applicable)
- [ ] Date of last update

### Privacy Notice Update Frequency
- Review and update at least annually
- Update within 30 days of any material change in data practices

## Data Mapping for California Compliance

For each data category, document:

| Field | Example |
|-------|---------|
| Category of PI | Identifiers (name, email, IP address) |
| Specific data elements | First name, last name, email, cookie ID |
| Source of collection | Directly from consumer, third-party data broker |
| Business purpose | Order fulfillment, analytics, marketing |
| Shared with | Analytics vendor, ad network |
| Sold? | Yes / No |
| Shared for cross-context behavioral advertising? | Yes / No |
| Retention period | 3 years post last interaction |

## Sensitive Personal Information (CPRA)

Sensitive PI requires special handling (additional disclosures + opt-down right):

- Social Security / government ID numbers
- Financial account numbers with access credentials
- Precise geolocation
- Racial or ethnic origin
- Religious beliefs
- Union membership
- Contents of mail, email, text (unless business purpose)
- Genetic data
- Biometric data for identification
- Health information
- Sexual orientation or sex life

## Opt-Out Mechanisms

### "Do Not Sell or Share My Personal Information"
- [ ] Prominent link on homepage and privacy policy
- [ ] Global Privacy Control (GPC) signal must be honored (CPRA)
- [ ] No re-enrollment without explicit consent (12-month wait)
- [ ] Process honored within 15 business days
- [ ] Downstream notification to third parties within 90 days

### "Limit the Use of My Sensitive Personal Information"
- [ ] Separate link or same page as opt-out of sale/share
- [ ] Honored within 15 business days

## Service Provider vs Third Party

| | Service Provider | Third Party |
|-|-----------------|-------------|
| Definition | Processes PI on your behalf per written contract | Receives PI for their own purposes |
| Contract required? | Yes — must include CCPA-required terms | N/A |
| CCPA "sale"? | No (not a sale if SP contract in place) | Yes (if consideration involved) |
| Risk | SP violating contract terms | Disclosure = potential "sale" |

### Required Service Provider Contract Terms
- PI used only for specified business purpose
- No selling or sharing of PI
- No retaining/using/disclosing PI outside the service
- Must notify you if they can no longer meet obligations
- Must permit and assist with consumer rights requests

## Consumer Request Handling Process

### Intake
1. Receive request via designated method (web form, toll-free number, email)
2. Acknowledge within 10 business days
3. Verify identity (2+ verification factors for sensitive requests)

### Verification Methods
- For online accounts: authenticate via account credentials
- For non-account holders: match 2+ data points to records
- For sensitive PI or financial info: strict verification required

### Response
1. Search all data systems (databases, backups, logs, marketing platforms)
2. Compile response or confirm deletion completed
3. Respond within 45 days (document if extension needed — max 45 more)
4. Log request, verification, response for recordkeeping

## Enforcement and Penalties

| Violation | Penalty |
|-----------|---------|
| Unintentional violation | Up to $2,500 per violation |
| Intentional violation | Up to $7,500 per violation |
| Children's data (under 16) | Up to $7,500 per intentional violation |
| Private right of action (data breach) | $100–$750 per consumer per incident or actual damages |

**California Privacy Protection Agency (CPPA)** enforces CPRA. 30-day cure period removed under CPRA (was available under original CCPA).

## CPRA Key Changes vs Original CCPA

| Area | CCPA | CPRA (2023+) |
|------|------|-------------|
| Data threshold | 50,000 consumers/households | 100,000 consumers/households |
| Right to correct | Not included | Added |
| Sensitive PI | No special category | Defined, separate rights |
| GPC signal | Guidance only | Must honor |
| Retention disclosure | Not required | Required |
| Enforcement | AG only | CPPA + AG |
| Cure period | 30 days | Eliminated |
| Employee/B2B data | Temporary exemption | Exemption expired Jan 2023 |

## Annual Compliance Calendar

| Month | Activity |
|-------|----------|
| January | Review privacy notice for accuracy vs current practices |
| March | Audit data map — new vendors, new data types |
| June | Employee privacy training refresher |
| September | Audit opt-out mechanisms — test GPC signal |
| October | Review service provider contracts for CCPA terms |
| December | Compile annual metrics (requests received/fulfilled/denied) |
