---
name: platform-trust-system
description: "Designs trust and safety systems with review policies, dispute resolution, and fraud prevention measures. Use when building trust infrastructure for marketplace platforms."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Platform Trust System

## When to Use This Skill

Use this skill when you need to:
- Design a trust and safety system for a marketplace or platform
- Create review and rating policies that build confidence
- Build dispute resolution workflows for buyer-seller conflicts
- Implement fraud prevention measures and detection triggers

**DO NOT** use this skill for payment processing setup, legal compliance (consult a lawyer), or customer support ticketing. This is for trust infrastructure design.

---

## Core Principle

TRUST IS THE CURRENCY OF MARKETPLACES — WITHOUT IT, BUYERS WILL NOT PAY AND SELLERS WILL NOT LIST. BUILD TRUST INTO EVERY TRANSACTION TOUCHPOINT.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Platform type** | "What does your marketplace connect? Products, services, rentals?" | No default — must be provided |
| **Transaction value** | "What is the average transaction value?" | Under $500 |
| **Current issues** | "What trust problems do you face? Fraud, disputes, fake reviews?" | Designing from scratch |
| **Risk tolerance** | "How strict should verification and moderation be?" | Moderate — balance trust with ease of use |
| **Team size for moderation** | "Who handles disputes and moderation?" | Solo founder |

**GATE: Confirm the brief before designing the system.**

---

## Phase 2: Design Trust Architecture

### Three Pillars of Platform Trust

**1. Prevention** — Stop bad actors before they transact
**2. Detection** — Identify problems as they happen
**3. Resolution** — Handle disputes fairly and quickly

### Prevention Layer

| Mechanism | Description |
|-----------|-------------|
| **Identity verification** | Require ID or business verification for sellers |
| **Profile completeness** | Higher-trust signals for complete profiles (photo, bio, credentials) |
| **Payment verification** | Verified payment method before transacting |
| **Content moderation** | Review listings before they go live (or spot-check) |
| **New user limits** | Cap transactions or listing volume for new accounts |

### Detection Layer

| Signal | Action |
|--------|--------|
| Multiple accounts from same IP/device | Flag for review |
| Sudden spike in listings or transactions | Automated hold |
| Buyer reports within first 24 hours | Priority review |
| Messaging contains off-platform payment links | Auto-block message |
| Review patterns suggesting manipulation | Flag and investigate |

### Resolution Layer

See Phase 3 for detailed dispute resolution workflow.

**GATE: Confirm the three-pillar approach before writing policies.**

---

## Phase 3: Write Trust Policies

### Review and Rating System

**Review eligibility:** Only users who completed a transaction can leave a review
**Review window:** 14 days after transaction completion
**Review format:** Star rating (1-5) + written review (minimum 20 characters)
**Response:** Sellers can respond publicly (one response per review)

**Review removal criteria:**
- Contains hate speech, threats, or personal information
- Reviewer did not complete a transaction
- Review is about the platform, not the seller/product
- Proven to be fraudulent or incentivized

**Reviews are NOT removed for:**
- Being negative
- Containing criticism the seller disagrees with
- Low star ratings

### Dispute Resolution Workflow

```
1. Buyer or seller opens a dispute
   ↓
2. Both parties provide their side (48-hour window each)
   ↓
3. Platform reviews evidence (messages, transaction records, photos)
   ↓
4. Decision issued within 5 business days
   ↓
5a. Refund issued (partial or full)
5b. Dispute resolved in seller's favor
5c. Compromise offered
   ↓
6. Appeal option (one per dispute, reviewed by different team member)
```

**Evidence accepted:** Screenshots, messages on platform, photos, tracking numbers, contracts

### Fraud Prevention Measures

- **Transaction monitoring:** Flag transactions 3x above category average
- **Account velocity limits:** New sellers limited to 5 transactions in first 14 days
- **Payment holds:** First-time seller payments held for 7 days
- **Off-platform communication warning:** Automated message when users share emails or phone numbers
- **Chargeback tracking:** Sellers with 3+ chargebacks in 90 days face account review

---

## Phase 4: Polish

### 1. Trust Badges and Signals

Design visible trust indicators:
- **Verified badge** — Completed identity or business verification
- **Top Rated badge** — 4.8+ average with 10+ reviews
- **Quick Responder badge** — Responds within 4 hours on average
- **Established badge** — Active on platform for 6+ months
- **Buyer Protection icon** — Displayed on all transactions

### 2. Trust Metrics Dashboard

```
## Trust Health Metrics

- **Dispute rate:** % of transactions resulting in a dispute (target: under 2%)
- **Resolution time:** Average days to resolve a dispute (target: under 5)
- **Fraud detection rate:** % of flagged accounts confirmed as fraudulent
- **Review authenticity:** % of reviews verified as genuine
- **Repeat transaction rate:** Proxy for trust (higher = more trust)
- **Chargeback rate:** % of transactions resulting in chargebacks (target: under 0.5%)
```

### 3. Quality Checklist

```
## Trust System Checklist

- [ ] Identity verification process defined for sellers
- [ ] Review system only allows verified transaction participants
- [ ] Review removal criteria are documented and fair
- [ ] Dispute resolution workflow has clear steps and timelines
- [ ] Fraud detection signals are defined and automated where possible
- [ ] New user transaction limits are in place
- [ ] Trust badges defined and criteria documented
- [ ] Payment hold policy documented for new sellers
- [ ] Off-platform communication monitoring is active
- [ ] Trust metrics are tracked and reviewed monthly
```

---

## Example

**Platform:** Freelance services marketplace

**Review response template for sellers:**
"Thank you for your feedback, [Name]. I appreciate you sharing your experience. [Address specific point]. I have since [improvement made]. I look forward to delivering excellent work for future clients."

**Dispute resolution message:**
"We have reviewed both sides of this dispute. Based on the project scope agreed upon in messages and the deliverables provided, we have decided to issue a 50% refund to the buyer. The seller delivered the core work, but key revisions outlined in the original agreement were not completed. Both parties can appeal within 7 days."

---

## Anti-Patterns

- **No review moderation** — fake reviews destroy marketplace credibility. Monitor and enforce policies.
- **Opaque dispute resolution** — if users cannot see the process, they assume it is unfair. Document and communicate every step.
- **Over-verifying** — requiring 5 documents to list an item kills supply. Verify what matters for trust, not bureaucracy.
- **Always siding with buyers** — always-refund policies attract fraudulent buyers and drive sellers away. Be fair to both sides.
- **Ignoring off-platform transactions** — users who transact off-platform avoid fees and your protections. Detect and discourage.

---

## Recovery

- **Spike in disputes:** Identify the pattern (specific seller, category, or buyer behavior). Tighten verification or listing standards in affected areas.
- **Fake review ring detected:** Remove all connected reviews, suspend involved accounts, and notify affected sellers/buyers.
- **Seller feels unfairly treated in dispute:** Offer the appeal process. Have a different person review. Transparency prevents escalation.
- **No resources for manual moderation:** Prioritize automated detection and focus manual review on high-risk transactions only.
