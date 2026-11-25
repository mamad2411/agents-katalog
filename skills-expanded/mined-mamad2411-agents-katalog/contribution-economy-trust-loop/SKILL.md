---
name: contribution-economy-trust-loop
description: Design community contribution systems where transparent contribution provenance, verifiable reputation, and privacy-first identity create a self-reinforcing trust loop that drives open-source community growth and monetization. Use when designing community platforms, building contribution-based economies, creating reputation systems for developer communities, or structuring open-source community monetization.
---

# Contribution Economy Trust Loop

## Overview

Open-source communities die without a contribution flywheel and survive but don't thrive without trust. The contribution economy trust loop is the design pattern that fuses contribution attribution, verifiable reputation, and privacy-first identity into a self-reinforcing cycle: contribution builds reputation, reputation builds trust, trust enables monetization, monetization funds more contribution. This skill operationalizes the loop for A-Tech's community products.

## When to Use

- Designing or redesigning a community platform where contribution is the primary value
- Building reputation or trust systems for open-source or developer communities
- Structuring community monetization (paid tiers, marketplace, contributor compensation)
- Responding to "how do we grow our open-source community?" or "how do we compensate contributors?"
- Creating contribution tracking, attribution, or governance systems
- NOT for pure top-down marketing funnels or communities where consumption (not contribution) is the value
- NOT as a replacement for `community-led-growth` or `nanocommunity-strategy` — this skill adds the trust-loop and monetization architecture layer

## Core Process / Workflow

### 1. Map the Trust Loop

The loop has five stages, each feeding the next:

```
1. CONTRIBUTION → 2. ATTRIBUTION → 3. REPUTATION → 4. TRUST → 5. MONETIZATION
       ↑                                                              │
       └──────────────────── funds / enables ─────────────────────────┘
```

**Stage 1 — Contribution:** A member creates value (code, docs, answers, reviews, teaching). The barrier to contribution must be low (one-click PRs, templates, "good first issue" labeling, nanocommunity pair-programming per `nanocommunity-strategy`).

**Stage 2 — Attribution:** The contribution is attributed to the contributor with a verifiable provenance trail. This is the critical differentiator: in most communities, attribution is informal (GitHub profile, commit history). In a trust loop, attribution is structured, portable, and cryptographically verifiable.

**Stage 3 — Reputation:** Attributed contributions accumulate into a reputation score. The score is not a vanity metric (per `trust-calibration-ux-pattern`'s vanity trust score anti-pattern) — it is tied to demonstrated outcomes (merged PRs, resolved issues, upvoted answers, maintained projects).

**Stage 4 — Trust:** Reputation enables trust from other members, maintainers, and potential clients/employers. Trust manifests as: merge authority, mentorship opportunities, paid project invitations, speaking invitations, marketplace visibility.

**Stage 5 — Monetization:** Trusted contributors earn (paid support, consulting, marketplace sales, sponsorships, bounties). Earnings fund more time for contribution, closing the loop.

### 2. Design the Attribution Layer

The attribution layer is the trust foundation. Without verifiable attribution, reputation is guesswork.

**Minimum viable attribution:**
```yaml
# contribution-record.yaml
contribution_id: ctr-2026-07-19-001
contributor_id: did:web:builderclub.com:members:alice
type: code  # code | docs | answer | review | teaching | mentorship
artifact:
  url: https://github.com/atech/project/pull/42
  hash: sha256:abc123...
  description: "Add retry logic to payment client"
provenance:
  created_at: 2026-07-19T10:00:00Z
  reviewed_by: [did:web:builderclub.com:members:bob]
  merged_by: did:web:builderclub.com:members:maintainer
  verification: "tests pass, spec validated"
impact:
  - metric: "downstream_prs_referencing"
    value: 7
  - metric: "issues_resolved_by_artifact"
    value: 3
  - metric: "stars_on_resulting_feature"
    value: 24
```

**Key design principles:**
- **Decentralized identity (DID):** Contributor identity is self-sovereign (W3C DID), not platform-locked. Contributors own their reputation and can port it across platforms.
- **Cryptographic provenance:** Every contribution is hash-linked to its artifact. Tampering is detectable.
- **Outcome-linked:** Reputation accrues from demonstrated impact, not activity volume. 1 merged PR that resolves 10 issues > 100 unmerged PRs.
- **Multi-type:** Code, docs, answers, reviews, teaching, and mentorship all count. Non-code contributions are often the highest-trust-building (per `trust-portfolio-distributed-authorship`).

### 3. Design the Reputation System

**Anti-pattern (avoid):** Vanity reputation that rises with usage, not accuracy. A contributor who submits 1,000 low-quality PRs should not outrank one who submits 10 high-impact ones.

**Design pattern:**
```
reputation_score = f(impact_weight × contribution_count × type_diversity × recency_decay)
```

Where:
- `impact_weight` — derived from outcome metrics (downstream references, issues resolved, stars)
- `contribution_count` — count of verified contributions
- `type_diversity` — bonus for contributing across multiple types (code + docs + mentoring)
- `recency_decay` — exponential decay; recent contributions weighted higher (prevents reputation rot)

**Domain-specific reputation:** Track reputation per domain (e.g., "reputation in: payment-systems, reputation in: security, reputation in: documentation"). This prevents a high-reputation contributor in docs from being trusted on security without demonstrated competence (per `trust-calibration-ux-pattern`'s per-domain track record pattern).

### 4. Design the Monetization Layer

The monetization layer converts reputation into revenue, closing the loop.

| Monetization mechanism | How it works | Trust loop role |
|---|---|---|
| **Paid support tiers** | Community members with high reputation offer paid support; platform takes a fee | Reputation → trust → clients → revenue → more contribution time |
| **Bounty system** | Organizations post bounties on issues; high-reputation contributors claim and resolve | Contribution → attribution → reputation → bounty claim → revenue |
| **Marketplace** | Contributors sell agents, tools, courses, templates; reputation drives visibility | Reputation → trust → sales → revenue → more building |
| **Sponsorship** | High-reputation contributors are sponsored by organizations using their work | Attribution → visibility → sponsorship → revenue |
| **Consulting introductions** | Platform introduces high-reputation contributors to clients; fee on engagement | Reputation → trust → introduction → revenue |
| **Creator revenue share** | Contributors who create educational content earn from platform revenue share | Teaching contribution → attribution → reputation → revenue share |

**Privacy-first payment:** Use the agentic payment protocols (AP2, x402 per `agentic-payments-protocol-ap2`) for microtransactions. Contributors can receive payments without exposing personal financial details to the platform. This is the privacy moat: competitors that require KYC for contributor payments lose privacy-conscious contributors.

### 5. Build the Privacy-First Identity Layer

The trust loop requires identity that is:
- **Verifiable:** others can confirm the contributor is real and the contributions are theirs
- **Portable:** contributors own their identity and reputation; they can leave without losing it
- **Privacy-preserving:** contributors can build reputation without exposing personal data

**Architecture:**

```
┌─────────────────────────────────────────────┐
│  Self-Sovereign Identity (W3C DID)           │
│  did:web:builderclub.com:members:alice        │
│  ┌───────────────────────────────────────┐    │
│  │ Verifiable Credentials (W3C VC)       │    │
│  │ - contribution-provenance credential  │    │
│  │ - reputation-score credential         │    │
│  │ - skill-domain credential             │    │
│  └───────────────────────────────────────┘    │
│  Selective disclosure: contributor chooses    │
│  what to reveal to whom                      │
└───────────────────────────────────────────────┘
                    │
                    │ Cryptographic proof
                    ↓
┌─────────────────────────────────────────────┐
│  Platform (Builder's Club)                   │
│  Verifies credentials without storing PII    │
│  Payment via x402/AP2 (no bank details)     │
└─────────────────────────────────────────────┘
```

The contributor's identity and reputation live in their DID wallet. The platform verifies credentials cryptographically (zero-knowledge proof where possible) without storing the underlying personal data. Payment is handled via agentic payment protocols that don't require KYC for microtransactions.

This is the privacy differentiator: a contributor can build reputation, earn revenue, and participate in the community without surrendering personal data to the platform.

### 6. Measure Trust Loop Health

| Metric | What it measures | Healthy pattern |
|---|---|---|
| Contribution growth rate | New contributions per period | Increasing |
| Attribution completeness | % of contributions with full provenance records | > 90% |
| Reputation-to-revenue conversion | % of high-reputation contributors earning | Increasing |
| Revenue-to-contribution reinvestment | % of contributor earnings that fund more contribution time | Increasing (the loop is closing) |
| New contributor retention | % of first-time contributors who contribute again in 30 days | > 40% |
| Trust sentiment (community survey) | Do members trust each other's contributions? | > 80% positive |
| Identity portability adoption | % of contributors with portable DID credentials | Increasing |

## References
- See [references/trust-loop-design-patterns.md](references/trust-loop-design-patterns.md) for detailed design patterns for each loop stage, including anti-patterns and case studies.
- See [references/identity-and-payment-architecture.md](references/identity-and-payment-architecture.md) for the technical architecture of the privacy-first identity and payment layer.