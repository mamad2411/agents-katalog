---
name: product-context
description: Foundational product marketing context that other skills reference. Establishes positioning, audience, messaging, and voice. Claude auto-references this when running GTM skills.
user-invocable: false
---

# Product Context Skill

Foundational product marketing context that all GTM skills reference for positioning, messaging, and voice consistency.

## Purpose

Provide the source of truth for product positioning, target audience, messaging framework, and brand voice. Other skills automatically reference this context to ensure consistency across all GTM outputs.

> **Note**: This is a **background reference skill** that Claude auto-loads when other GTM skills need product context. It is not meant to be invoked directly by users. To create or update your product context document, use the `messaging-positioning` or `brand-voice` skills.

---

## Skills That Reference This Context

The following skills automatically use product-context to ensure consistency:

- `copywriting` - Uses messaging framework and brand voice
- `email-sequences` - Applies value propositions and tone
- `social-content` - Maintains brand voice across channels
- `newsletter-writer` - References messaging pillars and voice
- `seo-content` - Uses positioning and key differentiators
- `competitive-intelligence` - References positioning against competitors
- `buyer-profiles` - Aligns persona messaging with framework
- `discovery-prep` - Uses value props for tailored questions
- `sales-playbook` - References positioning for talk tracks
- `outreach-templates` - Applies messaging to prospecting
- `case-study-builder` - Uses value pillars for storytelling
- `roi-builder` - References value metrics and proof points

---

## Required Integrations

> **Setup**: Connect these data sources to enable full functionality. Claude will prompt you to connect any missing integrations when you use this skill.

### Data Sources

```yaml
# PRODUCT CONTEXT DATA SOURCES
# Configure the sources for your product foundation

# Enterprise Search (searches across all internal sources)
- source: enterprise_search
  connector: "{{GLEAN | MOVEWORKS | ELASTIC}}"
  data:
    - internal_docs
    - wiki_content
    - shared_drives

# Product Documentation
- source: product_docs
  connector: "{{GOOGLE_DRIVE | SHAREPOINT | NOTION | CONFLUENCE}}"
  paths:
    - "/Product/Documentation/"
    - "/Product/Roadmap/"
    - "/Product Marketing/"

# Marketing Foundation
- source: marketing_docs
  connector: "{{GOOGLE_DRIVE | SHAREPOINT | NOTION}}"
  paths:
    - "/Marketing/Brand Guidelines/"
    - "/Marketing/Messaging/"
    - "/Marketing/Positioning/"

# Customer Research
- source: customer_research
  connector: "{{GOOGLE_DRIVE | SHAREPOINT | NOTION}}"
  paths:
    - "/Research/Persona Research/"
    - "/Research/ICP Documentation/"
    - "/Research/Customer Interviews/"

# Competitive Intelligence
- source: competitive_intel
  connector: "{{KLUE | CRAYON | KOMPYTE}}"
  data:
    - competitor_overview
    - market_landscape
```

### Output Destinations

```yaml
# Where to deliver product context outputs
outputs:
  # Always available - display in Claude UI
  - type: display
    enabled: true

  # Save as source of truth
  - type: documents
    connector: "{{GOOGLE_DRIVE | SHAREPOINT | NOTION}}"
    destination: "/Product Marketing/Product Context/"

  # Notify on updates
  - type: slack
    connector: "{{SLACK}}"
    channel: "#product-marketing"
```

---

## When to Use

- **First**: Run this skill before any other product marketing skills
- **Updates**: When product, market, or positioning changes significantly
- **New team members**: To onboard on product positioning

## Product Context Framework

### 1. Product Overview

**Core Product**
- What is the product?
- What problem does it solve?
- Who is it for?
- What makes it different?

**Product Category**
- Market category you compete in
- Adjacent categories
- How you want to be perceived

### 2. Target Audience

**Ideal Customer Profile (ICP)**
- Company characteristics (size, industry, tech stack)
- Buying triggers and signals
- Disqualifying criteria

**Buyer Personas**
- Primary persona: Role, responsibilities, goals, challenges
- Secondary personas: Other stakeholders in the buying process
- Anti-personas: Who is NOT a fit

### 3. Positioning

**Positioning Statement**
For [target customer] who [has this need], [Product] is a [category] that [key benefit]. Unlike [alternatives], we [key differentiator].

**Value Pillars**
- Pillar 1: [Benefit] - [Proof point]
- Pillar 2: [Benefit] - [Proof point]
- Pillar 3: [Benefit] - [Proof point]

### 4. Messaging Framework

**Message House**
- Roof: Core brand promise / tagline
- Pillars: 3 key messages that support the promise
- Foundation: Proof points, evidence, credentials

**Messaging by Audience**
- Executive message (strategic)
- Manager message (operational)
- User message (tactical)

### 5. Competitive Landscape

**Primary Competitors**
- Direct competitors
- Indirect/alternative solutions
- Status quo (doing nothing)

**Differentiation**
- Where we win
- Where we're at parity
- Where we need to neutralize

### 6. Brand Voice

**Voice Attributes**
- Tone: [Professional/Casual/Technical/Friendly]
- Personality: [Traits that define how we communicate]
- Language: [Words we use / words we avoid]

**Writing Guidelines**
- Do: [Style guidelines]
- Don't: [What to avoid]

---

## How to Use This Skill

Invoke with natural language describing what you need:

**Initial Setup**
- "Create a product context document for our company"
- "Build our product marketing foundation"

**Updates**
- "Update our product context with the new feature launch"
- "Refresh our positioning based on competitive changes"

**Specific Sections**
- "Update the competitor section of our product context"
- "Add a new buyer persona to our product context"

---

## Output Format

```markdown
# Product Marketing Context: [Product Name]

**Created**: [Date]
**Data Sources Used**: [Product docs, research, competitive intel]
**Last Updated**: [Date]
**Version**: [X.X]

---

## 1. Product Overview

### What We Do
[Clear, concise description]

### The Problem We Solve
[Customer pain point]

### Our Solution
[How we solve it]

### Key Differentiators
1. [Differentiator 1]
2. [Differentiator 2]
3. [Differentiator 3]

---

## 2. Target Audience

### Ideal Customer Profile
| Attribute | Criteria |
|-----------|----------|
| Company Size | [Range] |
| Industry | [Verticals] |
| Tech Stack | [Requirements] |
| Buying Triggers | [Signals] |

### Primary Persona: [Title]
- **Role**: [Description]
- **Goals**: [What they want to achieve]
- **Challenges**: [What stands in their way]
- **Success Metrics**: [How they're measured]

### Secondary Persona: [Title]
[Same structure]

---

## 3. Positioning Statement

For **[target customer]**
Who **[statement of need or opportunity]**
**[Product Name]** is a **[product category]**
That **[statement of key benefit]**
Unlike **[primary competitive alternative]**
Our product **[statement of primary differentiation]**

---

## 4. Messaging Framework

### Core Promise
[One-line brand promise]

### Message Pillars

| Pillar | Message | Proof Points |
|--------|---------|--------------|
| [Theme 1] | [Key message] | [Evidence] |
| [Theme 2] | [Key message] | [Evidence] |
| [Theme 3] | [Key message] | [Evidence] |

### Elevator Pitches
- **10 seconds**: [Shortest version]
- **30 seconds**: [Standard version]
- **60 seconds**: [Detailed version]

---

## 5. Competitive Landscape

### Competitive Matrix
| Competitor | Positioning | Our Advantage | Their Advantage |
|------------|-------------|---------------|-----------------|
| [Comp 1] | [How positioned] | [Our edge] | [Their edge] |

### Battlecard Summary
[Quick reference for competitive situations]

---

## 6. Brand Voice

### Voice Attributes
- **We are**: [Traits]
- **We are not**: [Anti-traits]

### Language Guide
- **Use**: [Preferred terms]
- **Avoid**: [Terms to skip]

---

## Quick Reference

### Tagline
[Company tagline]

### Boilerplate
[Standard company description for press, bios, etc.]

### Key Stats
- [Stat 1]
- [Stat 2]
- [Stat 3]
```

---

## Automation Options

When configured with integrations, this skill can:

1. **Context validation** - Check that product context stays current with product changes
2. **Consistency checking** - Ensure other skills reference the latest product context
3. **Competitive updates** - Flag when competitive landscape changes
4. **Onboarding automation** - Share product context with new team members
