---
name: gtm-playbook
description: "When to activate: go-to-market strategy, product launch, GTM planning, ICP definition, positioning, launch checklist, sales enablement, market entry"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: marketing
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Go-To-Market Playbook

## GTM Strategy Framework

### The 5 GTM Questions
1. **Who** is your ideal customer? (ICP)
2. **What** problem do you solve better than alternatives? (Positioning)
3. **Where** do customers discover and evaluate solutions? (Channels)
4. **How** do you reach and convert them? (Motion)
5. **Why** will they pay? (Value + Pricing)

## ICP Definition

### ICP Template
```
Firmographic:
- Company size: [employees / revenue]
- Industry: [verticals]
- Geography: [regions]
- Growth stage: [startup / SMB / mid-market / enterprise]
- Tech stack: [relevant tools they use]

Demographic (buyer):
- Title / role: [Economic buyer vs Champion]
- Seniority: [VP / Director / Manager / IC]
- Team size they manage: [X]

Psychographic:
- Goals: [What success looks like for them]
- Pain: [What keeps them up at night]
- Fears: [Switching risk, budget scrutiny, career risk]
- Motivations: [Career, team, company, personal]

Behavioral:
- Where they consume content: [Communities, publications]
- How they buy: [Self-serve / demo / pilot / procurement]
- Buying group size: [Solo / 2-5 / 5+]
- Sales cycle length: [Days / weeks / months]
```

### ICP Scoring Model
Score each prospect 1-5 on:
- Firmographic fit (company size, industry)
- Champion strength (title, influence)
- Pain urgency (actively looking to solve)
- Budget availability (can pay within cycle)
- Technical fit (can implement your solution)

Target: Accounts scoring 18+ out of 25

### Anti-ICP (Define Who NOT to Sell To)
- Too small to get value
- Industry where regulation blocks your product
- Too price-sensitive for your model
- Requires extensive customization
- High churn risk characteristics

## Positioning

### Positioning Statement Template (Geoffrey Moore)
```
For [target customer]
Who [has this problem/need]
[Product name] is a [category]
That [key benefit/capability]
Unlike [primary alternative]
Our product [key differentiator]
```

### Competitive Positioning Matrix
| Criteria | You | Competitor A | Competitor B |
|----------|-----|-------------|-------------|
| Feature 1 | ✓ | ✓ | ✗ |
| Feature 2 | ✓ | ✗ | ✓ |
| Price | $$ | $$$ | $ |
| Ease of use | High | Low | High |
| Support | High | Low | Low |

### Value Proposition Hierarchy
1. **Headline**: Single most important benefit (what + for whom)
2. **Sub-headline**: How it works / key feature (2-3 sentences)
3. **Bullets**: 3-5 specific benefits (avoid features, use outcomes)
4. **Social proof**: Number of customers, notable logos, stats

## GTM Motions

### Motion Selection by Customer Segment
| Segment | ACV | Motion | Team |
|---------|-----|--------|------|
| SMB | <$5k | Product-led / self-serve | Marketing |
| Mid-market | $5k-$50k | Sales-assisted PLG | SDR + AE |
| Enterprise | $50k+ | Enterprise sales | AE + SE + CS |

### Product-Led Growth (PLG) Motion
1. Free tier or trial (remove friction)
2. Aha moment in < 5 minutes (activation optimization)
3. Viral loop built into product (invite, share, embed)
4. PQL (product-qualified lead) score for sales handoff
5. Sales-assist on high-usage free users

### Sales-Led Motion
1. SDR outbound → Discovery call (1:1 ratio call:connect)
2. AE demo → Technical evaluation
3. POC/pilot → Champion builds business case
4. Procurement → Legal → Signature
5. CS handoff → Onboarding → QBR

## Launch Sequencing

### Pre-Launch (8 Weeks Before)
- [ ] Define launch goal: metric + number + date
- [ ] Identify launch type: silent / beta / full launch
- [ ] Build ICP list for early access (500-1000 names)
- [ ] Create launch landing page
- [ ] Prepare launch content (blog, video, press release)
- [ ] Brief analyst/press contacts
- [ ] Set up tracking (UTMs, goals in GA4, conversion events)
- [ ] Build waitlist/early access email sequence

### Pre-Launch (4 Weeks Before)
- [ ] Launch product hunt listing drafted
- [ ] Social content scheduled
- [ ] Email sequences loaded
- [ ] Sales team briefed with new materials
- [ ] Customer testimonials collected
- [ ] Influencer/partner outreach sent
- [ ] Support team trained
- [ ] Pricing finalized and uploaded

### Launch Week
- [ ] Day -1: Teaser to email list
- [ ] Day 0: All channels simultaneously
  - Email blast to full list
  - Social posts (all platforms, same time)
  - Product Hunt submission (12:01am PST)
  - Blog post live
  - Press release distributed
  - Paid ads activated
- [ ] Day 1-7: Engage every comment/DM/review
- [ ] Day 7: Results roundup email

### Post-Launch (Weeks 2-4)
- [ ] Send case study to early adopters
- [ ] Double down on winning channel
- [ ] Retarget launch traffic with conversion offer
- [ ] Gather user feedback → rapid iteration
- [ ] Update sales materials with real data

## Sales Enablement Package

### Core Materials
1. **1-pager**: Problem → Solution → Proof → CTA (one page)
2. **Battle card**: How to win against each competitor
3. **Demo script**: Scripted narrative, 25-35 minutes
4. **Objection handling guide**: Top 10 objections + responses
5. **Case study library**: 2-3 stories per vertical
6. **ROI calculator**: Input company data → output $ value
7. **Pricing guide**: Packages, discounting rules, approval matrix

### Battle Card Template
```
## vs [Competitor Name]

**When you encounter them:**
[How to identify Comp deals in pipeline]

**Their strengths (acknowledge honestly):**
- [Strength 1]
- [Strength 2]

**Our advantages:**
- [Advantage 1] → Proof: [stat or customer quote]
- [Advantage 2] → Proof: [stat or customer quote]

**Their weaknesses:**
- [Weakness 1] → Ask: "How do you handle [scenario]?"
- [Weakness 2] → Ask: "What happens when [edge case]?"

**Trap questions to ask in discovery:**
- "How important is [our differentiator] to you?"
- "What's your experience with [their limitation]?"

**Customer quote we use:**
"[Quote from customer who switched from competitor]"

**Closing line:**
"[Competitor] is good if [condition]. We're better when [your ICP's condition]."
```

## Channel Strategy

### Channel-Market Fit Assessment
Test each channel with $1-5k budget or 2-week sprint:
- Measure: CAC, lead quality (ICP fit score), conversion rate
- Cut: channels with CAC > 3x target or <10% ICP fit
- Scale: channels with CAC < target + >30% ICP fit

### Channel Mix by Stage
| Stage | Primary channels |
|-------|----------------|
| Pre-PMF | Founder sales, warm intros, communities |
| Early growth | Content + SEO, product-led, partnerships |
| Scaling | Paid acquisition, outbound SDRs, events |
| Scale | All channels, brand, analyst relations |

## GTM Metrics Dashboard

| Metric | Formula | Target |
|--------|---------|--------|
| CAC | Spend ÷ New customers | < LTV/3 |
| LTV | ARPU × Avg lifetime | > 3x CAC |
| LTV:CAC ratio | LTV ÷ CAC | > 3:1 |
| Payback period | CAC ÷ Monthly margin | < 12 months |
| Win rate | Won ÷ Total opps | 20-30% |
| Sales cycle | Avg days to close | Benchmark vs industry |
| Pipeline coverage | Pipeline value ÷ Quota | 3-4x |
| MQL→SQL rate | SQLs ÷ MQLs | 20-40% |
