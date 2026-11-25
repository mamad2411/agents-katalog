---
name: scope-of-work-generator
description: Generate a complete real estate engagement scope of work (SOW), listing agreement summary, or service fee proposal. Use this skill whenever a user asks to scope a listing engagement, write a service agreement, explain what's included in the commission, price a custom real estate service, define change-order triggers, or build a fee proposal for a client. Also use when a seller asks "what do I get for your commission" or when the agency needs to protect scope creep. Produces a fully itemized SOW with included services, exclusions, change-order policy, and compensation terms.
---

# Scope of Work Generator

Produces a complete, commercially sound scope of work for any real estate engagement. This is Derek's work: every service itemized, every change-order trigger defined, every client clear on what's included before anyone signs anything.

## What You Need From the User

- **Engagement type:** listing / buyer representation / property management / investor advisory / relocation concierge / custom
- **Property:** address or type, estimated value/price range
- **Seller/client name**
- **Timeline:** list date, expected close window
- **Any non-standard elements:** unique property, difficult situation, compressed timeline, additional services requested

## Output Format

```markdown
## Statement of Work
**Engagement Type:** [Listing Representation / Buyer Representation / Other]
**Property:** [Address]
**Client:** [Name(s)]
**Prepared by:** Derek, Estimator & SOW Specialist | [Date]
**Effective Date:** [Date] | **Estimated Duration:** Through [close date / X months]

---

### Section 1: Scope of Services

#### 1.1 Pre-Market Preparation
| Service | Included | Notes |
|---------|----------|-------|
| Comparative Market Analysis (CMA) + pricing consultation | ✅ | |
| Pre-listing walkthrough + improvement recommendations | ✅ | |
| Pre-inspection coordination (inspection cost not included) | ✅ | |
| Repair vendor referrals (up to [X] vendors) | ✅ | |
| Staging consultation | ✅ | Stager fees billed separately if used |
| Additional staging sessions | ❌ | Add-on: $[X]/session |

#### 1.2 Marketing
| Service | Included | Notes |
|---------|----------|-------|
| Professional photography ([X] photos) | ✅ | |
| Video walkthrough | [✅ / ❌ Add-on: $[X]] | |
| Drone aerials | [✅ / ❌ Add-on: $[X]] | |
| MLS listing (Zillow, Redfin, Realtor.com syndication) | ✅ | |
| Property email blast to agency database | ✅ | |
| Social media campaign ([X] weeks, Instagram + Facebook) | ✅ | |
| Extended social campaign beyond [X] weeks | ❌ | Add-on: $[X]/week |
| Just Listed postcards ([X] to [X] radius) | ✅ | |
| Property brochure ([X] copies) | ✅ | |
| Custom property microsite | [✅ / ❌ Add-on: $[X]] | |
| 3D Matterport tour | [✅ / ❌ Add-on: $[X]] | |

#### 1.3 Showings & Open Houses
| Service | Included | Notes |
|---------|----------|-------|
| Showing coordination via electronic lockbox | ✅ | |
| Showing feedback collection and summary | ✅ | |
| Broker preview (agent community first-look) | ✅ | |
| Open houses (up to [X]) | ✅ | |
| Additional open houses | ❌ | $[X] each |

#### 1.4 Offer & Negotiation
| Service | Included | Notes |
|---------|----------|-------|
| Offer review and analysis | ✅ | |
| Negotiation (up to [X] counter-offer rounds) | ✅ | |
| Additional negotiation rounds | ❌ | $[X]/round |
| Multiple offer management | ✅ | |

#### 1.5 Transaction Management
| Service | Included | Notes |
|---------|----------|-------|
| Contract-to-close coordination | ✅ | |
| Disclosure preparation and delivery tracking | ✅ | |
| Vendor coordination (inspector, escrow, lender liaison) | ✅ | |
| Compliance and document management | ✅ | |

---

### Section 2: Compensation

**Commission:** [X]% of final sale price
- Listing side: [X]%
- Buyer's agent compensation offered via MLS: [X]%

**Minimum commission:** $[X]
*(Applies if property sells below $[X])*

**Add-on services invoiced separately at time of service.**

---

### Section 3: Out of Scope

The following are **not included** in this engagement and require a written amendment before work begins:

- Property management or tenant coordination of any kind
- Renovation project management or contractor oversight
- Legal advice, contract interpretation, or representation in litigation
- Tax or financial planning advice
- Services related to any property not listed in this SOW
- Marketing beyond the [X]-week campaign if property remains unsold
- Any service not explicitly listed in Section 1 above

---

### Section 4: Change Order Policy

Any request outside this scope will be:
1. Confirmed in writing with a fee estimate
2. Approved by client in writing before work begins
3. Invoiced upon completion

**Verbal agreements are not binding amendments to this SOW.**

Common change-order triggers:
- Extended listing period beyond [X] weeks
- Additional marketing channels or campaigns
- Multiple price reduction communications requiring new marketing assets
- Relocation or concierge services added mid-engagement
- Unusual inspection or negotiation complexity exceeding [X] rounds

---

### Section 5: Timeline & Assumptions

This SOW assumes:
- List date: [Date]
- Target close: [Date] ([X] days)
- Property is [vacant / owner-occupied / tenant-occupied]
- Seller completes staging/prep by [Date]

If the listing period extends beyond [X] weeks due to market conditions or seller decisions, a supplemental scope and fee may apply.

---

### Section 6: Risk Adjustments Applied

*[Include only if risk adjustments were made]*

| Risk Factor | Adjustment | Notes |
|-------------|------------|-------|
| [e.g., compressed timeline] | +$[X] | [reason] |
| [e.g., tenant-occupied] | +[X] hrs TC | [reason] |

---

### Signatures

**Client:** _________________________________ Date: _________

**Agent:** _________________________________ Date: _________

*By signing, both parties confirm they have read and understood this Scope of Work.*
```

## Risk Adjustment Reference

Apply these automatically when risk factors are present — or flag them:

| Factor | Risk Level | Adjustment |
|--------|------------|------------|
| Close required in < 21 days | Medium | +$[X] or flag |
| Tenant-occupied with friction | High | +TC hours + note |
| Estate / probate sale | Medium | +TC hours |
| Out-of-state / remote seller | Low | +communication hours |
| History of prior failed listing | Medium | Requires pricing conversation |
| Unusual property type | High | Custom scope required |
| Significantly overpriced at outset | High | Flag risk of extended DOM; note in SOW |

## Behavior Notes

- Always produce every section — a SOW without a change-order policy is incomplete.
- If the user says "just tell me what to charge" — give a fee recommendation AND produce the SOW. The two go together.
- If the engagement is buyer representation: adapt Section 1 to buyer services (needs analysis, tours, offer writing, negotiation, transaction management) and note that compensation is typically paid by the seller via MLS cooperation.
- If a user asks to scope a property management engagement: see the Property Manager agent for the full PM framework; adapt the SOW accordingly.
- Always note at the bottom: "This SOW is a summary of services. It does not constitute a listing agreement. A separate listing agreement is required before marketing begins."
