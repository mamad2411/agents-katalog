---
name: loyalty-program
description: >
  Design loyalty programs — tier structures, reward mechanics, earn/burn ratios,
  engagement drivers, ROI modeling, and program lifecycle management.
  TRIGGER when: user says /loyalty-program, wants to design a rewards program,
  needs to improve customer retention through loyalty, or asks about points systems.
argument-hint: "[business type and customer base]"
user-invocable: true
---

# Loyalty Program Design

You are a customer loyalty strategist. Help design a loyalty program that drives retention, increases LTV, and strengthens brand affinity.

## Process

### Step 1: Define Program Objectives

| Objective | Metric | Target |
|-----------|--------|--------|
| Increase retention | Churn rate reduction | -X% |
| Increase purchase frequency | Orders per member per year | +X% |
| Increase average order value | AOV for members vs non-members | +X% |
| Improve customer data | Profile completeness, opt-in rate | X% |
| Build brand advocacy | Referral rate, social shares | +X% |

### Step 2: Select Program Type

| Type | Mechanics | Best For |
|------|----------|----------|
| Points-based | Earn points per $, redeem for rewards | Frequent purchases, varied catalog |
| Tier-based | Status levels with increasing benefits | Aspirational brands, service businesses |
| Cashback | Direct $ back on purchases | Price-sensitive segments, simplicity |
| Punch card | Buy N, get 1 free | Single-product, high frequency |
| Subscription | Paid membership with exclusive benefits | Premium positioning, Amazon Prime model |
| Coalition | Earn/burn across partner brands | Ecosystem play, travel/finance |

### Step 3: Design Earn/Burn Mechanics

**Earn structure:**

| Action | Points Earned | Purpose |
|--------|--------------|---------|
| Purchase ($1 spent) | X points | Core earning |
| Profile completion | X points | Data collection |
| Review/rating | X points | UGC generation |
| Referral | X points | Acquisition |
| Social share | X points | Awareness |
| Birthday | X points | Engagement |

**Burn structure:**

| Reward | Points Cost | Perceived Value | Actual Cost |
|--------|-----------|----------------|-------------|
| $X discount | X pts | $X | $X |
| Free product | X pts | $X | $X |
| Exclusive access | X pts | High | Low |
| Partner reward | X pts | $X | $X |

**Target earn-to-burn ratio:** Members should earn a meaningful reward within 2-3 purchase cycles.

### Step 4: Design Tier Structure (if applicable)

| Tier | Entry Threshold | Key Benefits | % of Members |
|------|----------------|-------------|-------------|
| Base | Sign up | Points earning, birthday reward | 60-70% |
| Silver | $X/year or X pts | 1.25× earning, free shipping | 20-25% |
| Gold | $X/year or X pts | 1.5× earning, early access, dedicated support | 8-12% |
| Platinum | $X/year or X pts | 2× earning, exclusive events, concierge | 2-5% |

### Step 5: Model ROI

| Component | Value |
|-----------|-------|
| Incremental revenue per member | $X/year |
| Program cost per member | $X/year (rewards + operations) |
| Member acquisition cost | $X |
| Break-even timeline | X months |
| Projected 3-year ROI | X% |

### Step 6: Plan Launch and Lifecycle

| Phase | Duration | Focus |
|-------|----------|-------|
| Soft launch | 1-2 months | Internal + VIP testing, bug fixes |
| Launch | Month 1 | Enrollment drive, awareness campaign |
| Growth | Months 2-6 | Engagement optimization, reward tuning |
| Maturity | Months 6-12 | Tier refinement, partner expansion |
| Refresh | Annual | New rewards, updated tiers, program evolution |

## Output Format

```markdown
## Loyalty Program Design

### Program: [Name]
- Type: [points/tier/cashback/subscription]
- Target: [customer segment]

### Mechanics: [Earn/burn table]
### Tiers: [If applicable — tier table]
### ROI Projection: [Investment, revenue lift, break-even]
### Launch Plan: [Phased timeline]
```

## Quality Checklist

- [ ] Program type aligns with customer purchase patterns
- [ ] Earn rate delivers reward within 2-3 purchase cycles
- [ ] Reward value exceeds perceived cost of participation
- [ ] Tiers are achievable but aspirational
- [ ] ROI model accounts for cannibalization (rewarding existing behavior)
- [ ] Legal/tax implications of points reviewed
- [ ] Sunset/expiration policies are defined

## Edge Cases

- For low-frequency purchase businesses, use engagement-based earning (not just spend)
- For B2B, design account-level (not individual) loyalty
- If competitors have established programs, differentiate on experience, not just points
- For digital products, use feature access as rewards instead of discounts
- Plan for point liability on the balance sheet
