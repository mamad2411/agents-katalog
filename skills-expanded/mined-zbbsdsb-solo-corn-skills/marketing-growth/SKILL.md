---
name: marketing-growth
description: Provides comprehensive marketing and growth support for solo entrepreneurs, guiding them from zero to one customer acquisition. Covers customer acquisition strategy, content marketing, conversion optimization, growth hacking, analytics, and brand building. Use this skill when users need marketing guidance, growth strategies, or customer acquisition support.
---

# Marketing Growth Skill

A comprehensive AI skill that transforms ideas into customers through data-driven marketing strategies.

## Core Capabilities

1. **Customer Acquisition**: Market segmentation, value proposition, GTM strategy
2. **Content Marketing**: Blog posts, social media, email sequences, video outlines
3. **Conversion Optimization**: Landing pages, sales funnels, A/B testing
4. **Growth Hacking**: Viral loops, referral programs, partnerships
5. **Analytics**: KPI definitions, attribution models, reporting
6. **Brand Building**: Positioning, messaging, visual identity

## Marketing Phases

The marketing workflow follows these phases:

```
Phase 1: Customer Research
    ↓
Phase 2: Strategy Development
    ↓
Phase 3: Channel Selection
    ↓
Phase 4: Content Creation
    ↓
Phase 5: Conversion Optimization
    ↓
Phase 6: Growth Experiments
    ↓
Phase 7: Analytics & Iteration
```

## Quick Start

### 1. Develop Customer Acquisition Strategy

```
User: "I have a new SaaS product for project management"
→ Customer persona creation
→ Value proposition development
→ Go-to-market strategy
→ Channel selection and prioritization
```

### 2. Create Marketing Content

```
User: "Help me create a content calendar"
→ Blog post templates
→ Social media content
→ Email sequences
→ Video content outlines
```

### 3. Optimize Conversions

```
User: "My landing page isn't converting"
→ Landing page audit
→ A/B testing framework
→ CTA optimization
→ Lead magnet creation
```

## Directory Structure

```
marketing-growth/
├── SKILL.md (this file)
└── references/
    ├── customer-acquisition/      # Phase 1 resources
    │   ├── market-segmentation.md
    │   ├── customer-personas.md
    │   ├── value-proposition.md
    │   └── gtm-strategy.md
    ├── content-marketing/         # Phase 2 resources
    │   ├── blog-templates.md
    │   ├── social-media.md
    │   ├── email-sequences.md
    │   └── video-outlines.md
    ├── conversion/                # Phase 3 resources
    │   ├── landing-pages.md
    │   ├── sales-funnels.md
    │   └── ab-testing.md
    ├── growth-hacking/           # Phase 4 resources
    │   ├── viral-loops.md
    │   ├── referral-programs.md
    │   └── partnerships.md
    ├── analytics/                 # Phase 5 resources
    │   ├── kpi-definitions.md
    │   ├── attribution-models.md
    │   └── reporting.md
    ├── paid-acquisition/         # Phase 6 resources
    │   ├── ad-platforms.md
    │   ├── campaign-templates.md
    │   └── budget-strategies.md
    ├── brand-building/            # Phase 7 resources
    │   ├── positioning.md
    │   ├── messaging.md
    │   └── visual-identity.md
    └── playbooks/
        ├── zero-to-100.md
        ├── product-hunt.md
        └── growth-experiments.md
```

## Marketing Methodologies

### Customer Acquisition
- **Jobs-to-be-Done (JTBD)**: Focus on customer jobs, pains, and gains
- **Lean Marketing**: Build-Measure-Learn for rapid iteration
- **Value Proposition Canvas**: Match product to customer needs

### Growth Strategies
- **Pirate Metrics (AARRR)**: Acquisition, Activation, Retention, Referral, Revenue
- **Bullseye Framework**: Focus on most impactful growth channels
- **Growth Loops**: Create self-reinforcing growth mechanisms

### Conversion Optimization
- **Value Ladder**: Guide customers through increasing value
- **Lead Magnet Strategy**: Attract with free, upsell with paid
- **Behavioral Psychology**: Use scarcity, social proof, urgency

## Supported Channels

### Organic
- Content marketing (SEO, blogging)
- Social media (LinkedIn, Twitter, Instagram, TikTok)
- Email marketing
- Community building
- PR and media relations

### Paid
- Google Ads (Search, Display, YouTube)
- Meta Ads (Facebook, Instagram)
- LinkedIn Ads (B2B focus)
- Twitter Ads
- Retargeting campaigns

## Best Practices

1. **Start with research**: Always understand customers before creating content
2. **Test before scaling**: Validate channels before heavy investment
3. **Measure everything**: Data-driven decisions beat intuition
4. **Iterate rapidly**: Build-Measure-Learn loop
5. **Focus on retention**: Acquisition without retention is leaky bucket

## Trigger Keywords

This skill activates when users mention:
- "marketing strategy"
- "customer acquisition"
- "content marketing"
- "growth hacking"
- "conversion optimization"
- "social media marketing"
- "email marketing"
- "landing page"
- "SEO"
- "paid ads"
- "brand building"
- "go-to-market"

## Related Skills

- **Research Integration**: Market insights and competitive analysis
- **Product Builder**: Landing page and funnel implementation
- **Customer Success**: Retention and support strategies

---

## Interface Definition

### Metadata
```typescript
{
  "name": "marketing-growth",
  "version": "2.0.0",
  "description": "Comprehensive marketing and growth support for solo entrepreneurs, from zero to one customer acquisition",
  "author": "SOLO CORN SKILLS",
  "category": ["marketing", "growth"],
  "tags": ["marketing", "growth", "customer-acquisition", "content-marketing"]
}
```

### Input Schema
```typescript
{
  "inputs": [
    {
      "name": "product",
      "type": "string",
      "required": true,
      "description": "Product or service description"
    },
    {
      "name": "phase",
      "type": "string",
      "required": false,
      "description": "Marketing phase (research, strategy, content, conversion, growth)",
      "default": "strategy"
    },
    {
      "name": "budget",
      "type": "string",
      "required": false,
      "description": "Marketing budget range"
    }
  ]
}
```

### Output Schema
```typescript
{
  "outputs": [
    {
      "name": "strategy",
      "type": "object",
      "description": "Complete marketing strategy and channel plan"
    },
    {
      "name": "content",
      "type": "object",
      "description": "Content calendar and templates"
    },
    {
      "name": "metrics",
      "type": "object",
      "description": "KPI definitions and tracking plan"
    }
  ]
}
```

### Invoke Method
```typescript
async invoke(params: InvocationParams): Promise<SkillResult> {
  // Execute marketing workflow
  // 1. Customer research and persona creation
  // 2. Marketing strategy development
  // 3. Channel selection and prioritization
  // 4. Content creation and optimization
  // 5. Growth experiment design
  // 6. Return results
}
```

---

## Usage via CLI
```bash
# Basic invocation
scs invoke marketing-growth --input '{"product": "My new SaaS app"}'

# Interactive mode
scs invoke marketing-growth --interactive

# With specific phase
scs invoke marketing-growth --input '{"product": "My SaaS", "phase": "content"}'
```
