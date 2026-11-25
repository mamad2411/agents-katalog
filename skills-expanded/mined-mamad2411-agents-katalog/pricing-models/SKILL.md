---
name: pricing-models
description: "When to activate: B2B pricing strategy, pricing tiers, enterprise deals, discounting policy, price increases, packaging, competitive pricing, freemium, usage-based pricing"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: business-ops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Pricing Models

## SaaS Pricing Structures

| Model | Mechanics | Best for | Watch out for |
|-------|-----------|---------|---------------|
| Per seat | Flat rate × number of users | Collaboration tools, broad adoption | Customers reduce seats; usage doesn't grow revenue |
| Usage-based | Pay for what you consume (API calls, GB, events) | Developer tools, infra, data products | Revenue unpredictability; churn at contract renewal |
| Flat recurring | Fixed fee per period regardless of usage | Simple products, small teams | Doesn't scale with customer value |
| Tiered flat | Fixed bands (0–10 users: $X; 11–50: $Y) | Mid-market SaaS | Cliff effect at tier boundaries |
| Outcome-based | Fee tied to measurable business outcome | High-trust, high-value vertical apps | Hard to measure, complex to administer |
| Hybrid | Seat floor + usage overage | Enterprise tools with variable workloads | Complexity in billing and quoting |

---

## Packaging Tiers

### Three-Tier Architecture (Good / Better / Best)

```
STARTER (self-serve, low friction)
  Price: $X/mo (billed annually) or $Y/mo (monthly)
  Seats: Up to N users
  Features:
    - [Core value prop — enough to get value]
    - [Limited quota on key resource: e.g., 1,000 API calls/mo]
    - Community support only
    - Standard integrations
  Target: SMB, individual teams, trial/evaluation
  Goal: capture demand, prove value

PROFESSIONAL (team-level, most common)
  Price: $X/seat/mo or $Y flat/mo
  Seats: N–N users
  Features:
    - Everything in Starter
    - [Key differentiating features]
    - [Higher quotas]
    - Email/chat support (SLA: N hours)
    - Advanced integrations / SSO
    - [Collaboration features]
  Target: growing teams, mid-market
  Goal: primary revenue driver (highest volume of customers)

ENTERPRISE (custom, negotiated)
  Price: Custom (floor: $X/year)
  Seats: Unlimited or custom
  Features:
    - Everything in Professional
    - [Compliance features: audit logs, SAML SSO, data residency]
    - [Advanced security: IP allowlists, role-based access]
    - Dedicated CSM
    - SLA: 99.9% uptime + defined response times
    - Custom contracts, invoicing, MSA
    - Security review / SOC 2 report sharing
  Target: 1,000+ employee organizations, regulated industries
  Goal: high ACV, long contracts, low churn
```

### Packaging Design Principles
- Gate on value-creating features, not usability-limiting ones
- Upgrade triggers should be natural parts of success (more users, more data)
- Downgrade should be painful but possible — don't trap customers with bad UX
- Put the most important feature in the middle tier to pull upgrades
- Enterprise features: security, compliance, control, SLAs — not features SMBs need

---

## Discounting Policy

### Discount Authorization Matrix
| Discount depth | Authorization required |
|---------------|----------------------|
| 0–10% | AE discretion |
| 11–20% | Sales manager approval |
  21–30% | VP Sales approval |
| 31–40% | CRO + CFO approval |
| > 40% | CEO approval + documented strategic rationale |

### Legitimate Discount Justifications
- Multi-year commitment (1yr → 2yr: 10%, 3yr: 15–20%)
- Upfront annual payment vs. monthly
- High-volume commitment above standard tier
- Strategic reference customer (logo, case study, co-marketing)
- Competitive displacement with documented proof
- Accelerated close within quarter (time-limited)

### Illegitimate Discounts (Red Flags)
- "Just to get the deal" with no business rationale
- Matching a competitor without verifying the competitor quote
- Repeated discounts to same customer without new commitments
- End-of-quarter pressure with no customer urgency on their side

### Price Protection
- Multi-year contracts: lock price for contract term
- Annual contracts: give 90-day price increase notice before renewal
- Define in contract: "Pricing subject to up to X% annual increase"

---

## Enterprise Deal Mechanics

### Negotiating Large Deals
1. **Anchor high**: Quote list price first — never start with discount
2. **Trade, don't give**: Every concession comes with a concession in return
3. **Use deal desk**: Structured review for deals > $X to ensure margin
4. **Expand scope**: Before discounting price, add value (training, PS, extended term)
5. **Economic buyer vs. champion**: Pricing decisions made by economic buyer — ensure access

### Common Enterprise Negotiation Levers
| Lever | Their ask | Your counter |
|-------|-----------|-------------|
| Lower price | 25% discount | 2-year term for 15% discount |
| More seats | Add 50 seats free | Add 25 seats; include in year 2 expansion |
| Extended trial | 3-month free pilot | 60-day paid POC with credits applied |
| Payment terms | Net 60 | Net 30 with 2% early pay discount |
| Unlimited users | Unlimited tier | Custom enterprise tier with annual true-up |

---

## Price Increases

### Price Increase Playbook
1. **Set policy**: state price increase rights in contract (e.g., "up to X% annually")
2. **Give advance notice**: 90 days minimum for annual contracts
3. **Lead with value**: communicate what's improved since they signed
4. **Segment sensitivity**: flag accounts most likely to churn; plan outreach
5. **Grandfather selectively**: consider locking current price for existing customers if < N% below new price
6. **Train CS**: CSMs own the conversation — they know the account best
7. **Track outcomes**: monitor churn rate post-increase vs. pre-increase

### Price Increase Communication Template
```
Subject: [Product] pricing update — effective [Date]

Hi [Name],

We're writing to let you know that [Product] pricing will increase
by X% effective [Date]. This affects your account as follows:

  Current: $X/[period]
  New:     $Y/[period]
  Effective: [Date]

Since you joined, we've shipped [N major features/improvements].
[2–3 specific examples of value added.]

Your current contract runs through [date]. We'll apply the new pricing
at your next renewal.

If you'd like to lock in your current price for an additional year,
we'd be happy to extend your contract before [early commitment date].

[Name, title]
```

---

## Competitive Pricing Response

### Frameworks for Competitive Situations

**When priced above competitor:**
- Quantify total cost of ownership: include implementation, switching, support costs
- Prove ROI: X% outcome improvement × their scale = payback period
- Reduce risk: guarantee: "If you don't see X result in Y days, we'll refund Z"
- Focus on differentiated outcomes the competitor can't match

**When priced below competitor:**
- Avoid "cheapest" positioning — attracts price-sensitive, high-churn customers
- Use pricing as qualifying signal: "We're the right fit for growing teams"
- Package more value at your price point rather than simply undercutting

**When asked to match a competitor price:**
1. Ask to see the competitive quote (many don't have one)
2. If quote is real: compare apples-to-apples (scope, terms, support)
3. If genuinely lower for same scope: escalate to deal desk
4. Never match verbally — only after documentation confirms it's real

---

## Freemium and Free Trial Design

### Freemium Limits (Value-Preserving)
| Limit type | Example | Goal |
|-----------|---------|------|
| Usage cap | 1,000 API calls/month free | Hit cap → upgrade |
| Seat cap | 3 users free | Team growth → upgrade |
| Feature gate | Reporting locked to paid | See value → unlock |
| Time-based | Full features for 14 days | Urgency to convert |

### Conversion Optimization
- Free-to-paid conversion benchmark: 2–5% (PLG), 10–15% (sales-assisted)
- Time to value: minimize steps between signup and first "aha" moment
- Upgrade triggers: contextual (hit a limit) beat generic (email campaigns)
- Sales engagement: flag accounts with heavy usage but no upgrade intent → SDR outreach
