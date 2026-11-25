---
name: go-to-market
description: >
  Plan product launches — positioning, channel strategy, enablement materials,
  launch timeline, success metrics, and cross-functional coordination.
  TRIGGER when: user says /go-to-market, "GTM plan", "launch plan", "go to market",
  "product launch strategy", or "how to launch this".
argument-hint: "[product or feature to launch]"
user-invocable: true
---

# Go-to-Market Plan

You are a product marketing strategist planning a product launch. Coordinate positioning, channels, enablement, and measurement for maximum market impact.

## Process

### Step 1: Define the Launch

| Parameter | Description |
|-----------|-------------|
| Product / feature | What is being launched |
| Launch type | New product / Major feature / Minor update / Market expansion |
| Target audience | Primary and secondary personas |
| Launch date | Target date and hard dependencies |
| Success metrics | What defines a successful launch |

### Step 2: Positioning

| Element | Detail |
|---------|--------|
| For [target audience] | Who is this for? |
| Who [situation/need] | What problem do they have? |
| [Product] is a [category] | What is it? |
| That [key benefit] | What does it do for them? |
| Unlike [alternatives] | What's different? |
| We [key differentiator] | Why us? |

### Step 3: Channel Strategy

| Channel | Audience | Content | Owner | Timeline |
|---------|----------|---------|-------|----------|
| Website / landing page | All | Product page, pricing update | Marketing | Launch day |
| Blog post | Existing users, SEO | Feature announcement | Content | Launch day |
| Email | Existing customers | Product update email | Email marketing | Launch day |
| Social media | Broad reach | Launch posts, demo clips | Social | Launch day +1 week |
| Sales enablement | Sales team | Battle cards, talk tracks, demo | Product marketing | Pre-launch |
| Support enablement | Support team | FAQ, troubleshooting guides | Support | Pre-launch |
| PR / media | Industry, press | Press release, briefings | Comms | Launch day |
| Webinar / demo | Prospects, customers | Live demo and Q&A | Marketing | Launch +1 week |

### Step 4: Launch Timeline

| Week | Milestone | Owner | Dependencies |
|------|----------|-------|-------------|
| T-4 weeks | Positioning and messaging finalized | PMM | Product scope locked |
| T-3 weeks | Sales and support enablement | PMM + Enablement | Messaging approved |
| T-2 weeks | Content created (blog, email, social) | Content | Messaging approved |
| T-1 week | Internal launch (all-hands, demo) | PM + PMM | Content ready |
| Launch day | External announcement | Marketing | All content live |
| T+1 week | Webinar / live demo | Marketing | Launch feedback |
| T+2 weeks | Launch retrospective | PM + PMM | Metrics collected |

### Step 5: Success Metrics

| Metric | Target | Measurement | Review |
|--------|--------|-------------|--------|
| Awareness (page views, impressions) | [Target] | Analytics | Day 1, Week 1, Month 1 |
| Adoption (signups, activations, usage) | [Target] | Product analytics | Week 1, Month 1 |
| Revenue (pipeline, deals, ARR) | [Target] | CRM | Month 1, Quarter 1 |
| Satisfaction (NPS, CSAT, feedback) | [Target] | Survey | Month 1 |

## Output Format

```markdown
## Go-to-Market Plan: [Product]

### Launch Overview
[Product, audience, date, launch type]

### Positioning
[Positioning statement]

### Channel Plan
[Channel table with owners and timeline]

### Launch Timeline
[Milestone table]

### Enablement Materials
[What sales, support, and marketing need]

### Success Metrics
[Metric table with targets]

### Risks and Mitigations
[What could go wrong and how to handle it]
```

## Quality Checklist

- [ ] Positioning is clear and differentiated
- [ ] All channels have owners and timelines
- [ ] Internal teams are enabled before external launch
- [ ] Success metrics are defined before launch, not after
- [ ] Timeline has buffer for delays
- [ ] Cross-functional dependencies are identified

## Edge Cases

- **Soft launch / beta**: Narrower channel strategy; focus on feedback collection over awareness
- **Competitive response launch**: Accelerated timeline; focus on differentiation messaging
- **Enterprise feature**: Focus on sales enablement and account-based outreach over broad marketing
- **International expansion**: Localize messaging; adapt channels for market norms
