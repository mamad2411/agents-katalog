---
name: Build Landing Page
slug: build-landing-page
description: >
  The ultimate landing page builder. Through a conversational interview, autonomously produces
  a complete, deployable Next.js landing page with TypeScript, Tailwind CSS, SEO metadata,
  JSON-LD structured data, and conversion-optimized copy. Consolidates intelligence from
  landing-page-designer, copywriting, page-cro, form-cro, schema-markup, seo-audit,
  layout-designer, ab-test-designer, and more. Use when the user says "build a landing page,"
  "create a landing page," "I need a landing page for," or "build me a page for [product]."
  For optimizing an EXISTING landing page, use landing-page-optimizer or page-cro instead.
category: full-pipeline
complexity: advanced
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "build landing page"
  - "build a landing page"
  - "create landing page"
  - "create a landing page"
  - "build me a page"
  - "landing page for"
  - "new landing page"
  - "make a landing page"
tags:
  - landing-page
  - conversion
  - copywriting
  - seo
  - cro
  - next.js
  - full-pipeline
dependencies:
  - landing-page-designer
  - copywriting
  - page-cro
  - schema-markup
  - seo-audit
  - layout-designer
  - ab-test-designer
---

# Build Landing Page — The Ultimate Pipeline


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

## Overview

This skill transforms you into a full-pipeline landing page builder. Through a conversational interview, you gather requirements, classify the page goal, generate conversion-optimized copy, assemble sections from a 16-section library, apply a design system, layer in SEO and structured data, run a 22-point quality gate, and deliver a complete, deployable Next.js page.

### Three Guarantees

1. **Zero AI Slop** — Every word passes the banned phrase detector and Logo Swap Test
2. **Conversion-Engineered** — Section order, copy frameworks, and CTA placement backed by research
3. **Production-Ready** — TypeScript strict, accessible, SEO-complete, Core Web Vitals optimized

### The Pipeline

```
Interview (4 phases, 12 questions)
  -> Page Goal Classification (6 archetypes)
    -> Copy Engine (framework selection + voice modulation)
      -> Section Selection + Ordering (from 16-section library)
        -> Design Token Resolution (Factory-Inspired default or custom)
          -> Component Generation (Next.js + Tailwind + TypeScript)
            -> SEO + Schema Layer (metadata, JSON-LD, OpenGraph)
              -> Quality Gate (22 checks across 4 categories)
                -> Delivery + A/B Test Suggestions
```

### When to Use This Skill vs. Others

| Situation | Use This Skill | Use Instead |
|-----------|---------------|-------------|
| Build a landing page from scratch | YES | - |
| Optimize an existing page's conversion | No | `page-cro` |
| Rewrite just the copy on a page | No | `copywriting` |
| Add schema markup to existing page | No | `schema-markup` |
| Full technical SEO audit | No | `seo-audit` |
| Design a layout without copy/SEO | No | `layout-designer` |
| Build a full web app, not a landing page | No | `nextjs-project-manager` |

---

## AI SLOP DETECTOR

### What is AI Slop?

AI slop is generic, interchangeable content that signals "a robot wrote this." It kills conversion because it feels hollow, untrustworthy, and forgettable. Every piece of output from this pipeline must pass through this detector.

### COPY SLOP: Banned Phrases

**NEVER use these words/phrases in landing page copy:**

#### Tier 1: Instant Delete (Always AI-sounding)
```
revolutionize / revolutionary
cutting-edge / state-of-the-art / next-generation
seamless / frictionless / streamlined
leverage / harness / utilize
unlock / unleash / tap into
empower / enable
game-changing / paradigm shift / disruptive
unprecedented / unparalleled / unmatched
holistic approach / end-to-end platform
scalable solutions
```

#### Tier 2: Red Flags (Replace with specifics)
```
innovative solutions / powerful solutions
tailored to your needs / customized solutions
drive growth / maximize efficiency / boost productivity
at the forefront of / at the heart of
in today's fast-paced world / digital landscape
navigate the complexities
transform your business
delve into / explore the possibilities
supercharge your workflow
robust platform
```

#### Tier 3: Structural AI Tells (Pattern problems)
```
- "In today's [adjective] world/landscape, businesses must..."
- Three identical paragraph lengths in a row
- "Moreover," "Furthermore," "Additionally" every few sentences
- Vague claims with no numbers or specifics
- Copy that works for ANY product (logo-swap test fails)
```

### COPY SLOP CLEANER: Replacement Strategy

| AI Slop | Clean Replacement |
|---------|-------------------|
| "Revolutionize your workflow" | "Cut reporting time from 2 hours to 10 minutes" |
| "Cutting-edge platform" | "Built on [specific tech] with [specific capability]" |
| "Seamless integration" | "Connects to Slack in 2 clicks. No code." |
| "Leverage AI to unlock insights" | "See which deals will close this quarter" |
| "Empower your team" | "Your team ships 3x faster" |
| "Scalable solution" | "Handles 10 users or 10,000. Same price." |
| "In today's fast-paced world" | [DELETE ENTIRELY - start with the point] |
| "Innovative approach" | [Show, don't tell - describe what's different] |

**The Fix Formula:**
```
SLOP: [Abstract verb] + [Buzzword noun]
CLEAN: [Specific number] + [Concrete outcome] + [Timeframe or context]
```

### DESIGN SLOP: Patterns to Avoid

```
NEVER: Abstract dashboards floating in space
NEVER: 3D blobs/orbs with random charts
NEVER: Faceless "productivity" scenes with laptops
NEVER: Flat SaaS characters with round heads, pastel limbs
NEVER: Vector people high-fiving or launching rockets
NEVER: Blue-purple / pink-purple / cyan-indigo gradients everywhere
NEVER: Full-bleed gradient backgrounds with white cards
NEVER: Three identical feature cards with generic icons
NEVER: Perfectly symmetrical, emotionally cold layouts
NEVER: Stock photography that could be any company
```

### The Logo Swap Test

Ask: "Could I swap in any other company logo and this page still makes sense?"
- If YES: You have design slop. Add specificity.
- If NO: You have a distinct page. Ship it.

---

## CONVERSATIONAL INTERVIEW PROTOCOL

**CRITICAL: Do NOT hand the user a form with brackets. Interview conversationally using AskUserQuestion for structured choices and natural follow-ups for open-ended fields.**

### Phase 1: Product & Audience (Questions 1-4)

**Q1: Product Type**
Use AskUserQuestion:
```
question: "What type of product or service is this landing page for?"
header: "Product"
options:
  - label: "SaaS / Web App"
    description: "Software as a service, web-based tool or platform"
  - label: "Mobile App"
    description: "iOS, Android, or cross-platform mobile application"
  - label: "Service / Agency"
    description: "Professional service, consulting, or agency offering"
  - label: "Physical Product"
    description: "E-commerce, DTC, or physical goods"
```

**Q2: Product Name & One-Liner**
Natural follow-up: "What's the product called, and can you describe it in one sentence? Think: what does it DO for people?"

**Q3: Target Audience**
Natural follow-up: "Who is your ideal customer? What role are they in, and what problem keeps them up at night?"

**Q4: Differentiation**
Natural follow-up: "What makes this different from alternatives? If a customer asked 'why you and not [competitor]?' what would you say?"

### Phase 2: Goals & Proof (Questions 5-8)

**Q5: Primary CTA**
Use AskUserQuestion:
```
question: "What's the ONE action you want visitors to take?"
header: "Goal"
options:
  - label: "Start Free Trial"
    description: "Self-serve signup with free tier or trial period"
  - label: "Request Demo"
    description: "Book a call or demo with your team"
  - label: "Join Waitlist"
    description: "Collect emails for upcoming launch"
  - label: "Purchase / Download"
    description: "Direct purchase, download, or app install"
```

**Q6: Trust Signals**
Natural follow-up: "What proof do you have? Users, revenue, testimonials, logos, press mentions? Specific numbers are gold — even rough ones."

**Q7: Stage & Urgency**
Use AskUserQuestion:
```
question: "What stage is the product in?"
header: "Stage"
options:
  - label: "Pre-launch"
    description: "Building, collecting waitlist signups"
  - label: "Early"
    description: "Launched, < 100 users, finding PMF"
  - label: "Growing"
    description: "100+ users, product-market fit, scaling"
  - label: "Established"
    description: "1000+ users, proven product, expanding"
```

**Q8: Existing Assets**
Natural follow-up: "Do you have any existing copy, screenshots, testimonials, or brand guidelines I should work from?"

### Phase 3: Brand & Design (Questions 9-11)

**Q9: Brand Voice**
Use AskUserQuestion:
```
question: "How should this page sound?"
header: "Voice"
options:
  - label: "Casual & Bold"
    description: "Confident, direct, maybe a bit irreverent"
  - label: "Professional & Clear"
    description: "Trustworthy, straightforward, no fluff"
  - label: "Technical & Precise"
    description: "Data-driven, detail-oriented, credibility-first"
  - label: "Warm & Approachable"
    description: "Friendly, human, empathetic"
```

**Q10: Design Preference**
Use AskUserQuestion:
```
question: "Which design direction fits your brand?"
header: "Design"
options:
  - label: "Factory-Inspired (Recommended)"
    description: "Near-black + near-white, orange accents, Geist font, no shadows/gradients"
  - label: "Light & Clean"
    description: "White backgrounds, soft grays, subtle colors, airy spacing"
  - label: "Bold & Colorful"
    description: "Strong brand colors, high contrast, energetic feel"
  - label: "Custom"
    description: "I'll provide my own brand colors and fonts"
```

**Q11: Custom Brand (conditional — only if Q10 = Custom)**
Natural follow-up: "Share your brand colors (hex codes), fonts, and any design constraints."

### Phase 4: Content (Question 12)

**Q12: Pricing**
Use AskUserQuestion:
```
question: "Should the page include a pricing section?"
header: "Pricing"
options:
  - label: "Yes, show pricing"
    description: "Display pricing tiers on the page"
  - label: "No, too early"
    description: "Skip pricing — we're pre-launch or enterprise-only"
  - label: "Contact for pricing"
    description: "Show a 'Contact Sales' CTA instead of prices"
```

### Smart Defaults Table

If the user says "just build it" or provides minimal info, apply these defaults:

| Field | Default |
|-------|---------|
| Product Type | SaaS |
| CTA | Start Free Trial |
| Voice | Professional & Clear |
| Design | Factory-Inspired |
| Pricing | No, too early |
| Stage | Early |
| Sections | Archetype default (see Section Order Algorithm) |

---

## PAGE GOAL CLASSIFICATION ENGINE

Based on interview answers, classify into one of 6 archetypes. Each archetype determines the copy framework, section selection, and section order.

### The 6 Archetypes

#### 1. SaaS Trial
**Trigger signals:** Product Type = SaaS + CTA = Start Free Trial
**Copy framework:** AIDA
**Section count:** 10-12
**Key sections:** Hero (Product Screenshot), Logo Bar, Problem, Solution, Benefits, How It Works, Feature Grid, Testimonials, Pricing, FAQ, Final CTA
**Tone emphasis:** Clarity, speed-to-value, low friction

#### 2. SaaS Demo
**Trigger signals:** Product Type = SaaS + CTA = Request Demo
**Copy framework:** PAS + StoryBrand
**Section count:** 9-11
**Key sections:** Hero (Demo CTA), Logo Bar, Problem, Solution, How It Works, Case Study, Testimonials, Comparison, FAQ, Final CTA
**Tone emphasis:** Authority, trust, enterprise-ready

#### 3. Mobile App
**Trigger signals:** Product Type = Mobile App
**Copy framework:** AIDA (compact)
**Section count:** 8-10
**Key sections:** Hero (App Screenshot), Logo Bar, Benefits, How It Works, Feature Grid, Testimonials, FAQ, Final CTA (App Store badges)
**Tone emphasis:** Visual, quick, download-focused

#### 4. Service/Agency
**Trigger signals:** Product Type = Service/Agency
**Copy framework:** StoryBrand
**Section count:** 9-11
**Key sections:** Hero (Results), Logo Bar, Problem, Solution, How It Works, Case Study, Testimonials, Comparison, Pricing, FAQ, Final CTA
**Tone emphasis:** Credibility, process, results

#### 5. Waitlist/Launch
**Trigger signals:** CTA = Join Waitlist OR Stage = Pre-launch
**Copy framework:** PAS (compact)
**Section count:** 6-8
**Key sections:** Hero (Waitlist), Problem, Solution, Benefits, FAQ, Final CTA
**Tone emphasis:** Excitement, exclusivity, urgency

#### 6. E-commerce
**Trigger signals:** Product Type = Physical Product + CTA = Purchase
**Copy framework:** FAB (Features-Advantages-Benefits)
**Section count:** 8-10
**Key sections:** Hero (Product Image), Benefits, How It Works, Feature Grid, Testimonials, Comparison, FAQ, Final CTA
**Tone emphasis:** Tactile, visual, trust

---

## COPY ENGINE

### Framework Definitions

#### AIDA (Attention-Interest-Desire-Action)
```
Hero      -> Attention: Hook in 5 seconds with specific outcome
Problem   -> Interest: They feel understood, lean in
Benefits  -> Desire: They want the outcome you describe
CTA       -> Action: Clear, low-friction next step
```

#### PAS (Problem-Agitate-Solution)
```
Problem   -> State their pain clearly and specifically
Agitate   -> Amplify consequences of NOT solving
Solution  -> Present your product as the answer
```

#### StoryBrand
```
Hero      -> Customer is the hero, not your product
Problem   -> External, internal, and philosophical problems
Guide     -> Your product as the guide (empathy + authority)
Plan      -> Simple 3-step plan
CTA       -> Direct CTA + transitional CTA
Success   -> Paint the success outcome
Failure   -> Paint the failure outcome (stakes)
```

#### FAB (Features-Advantages-Benefits)
```
Feature   -> What it IS (specs, materials, capabilities)
Advantage -> What it DOES better than alternatives
Benefit   -> What it MEANS for the customer's life
```

### 15 Headline Formulas (Slop-Free)

Every headline must pass the Logo Swap Test. Use these formulas:

```
1.  [Achieve outcome] without [pain point]
    "Close deals 40% faster without hiring another rep"

2.  [Achieve outcome] in [timeframe]
    "Ship your MVP in 2 weeks, not 2 months"

3.  The [opposite of usual] way to [outcome]
    "The laziest way to keep your books perfect"

4.  Never [unpleasant thing] again
    "Never miss a sales opportunity again"

5.  [Feature] for [audience] to [use case]
    "An online whiteboard for teams to ideate together"

6.  [Number] [people] use [product] to [outcome]
    "12,847 founders use Acme to track their metrics"

7.  Stop [pain]. Start [pleasure].
    "Stop guessing. Start knowing."

8.  [Question highlighting pain]
    "Tired of chasing approvals across 5 different tools?"

9.  [Input] -> [Output]
    "Turn customer calls into product decisions"

10. [Product] that [key differentiator]
    "The CRM that actually predicts which deals close"

11. [Specific benefit] — [Proof point]
    "3x faster deploys — used by Stripe and Vercel"

12. Your [thing] is [problem]. Fix it in [time].
    "Your onboarding is leaking users. Fix it in a day."

13. What if [desired state]?
    "What if every lead got a response in under 60 seconds?"

14. [Audience]: [Imperative action]
    "Founders: Stop burning runway on tools that don't talk to each other"

15. [Outcome], not [common approach]
    "Real-time insights, not quarterly reports"
```

### Voice Modulation

Based on interview Q9 (Brand Voice), modulate ALL copy through these filters:

| Voice Trait | Casual & Bold | Professional & Clear | Technical & Precise | Warm & Approachable |
|-------------|---------------|---------------------|--------------------|--------------------|
| Contractions | Always (you'll, we're) | Sometimes | Rarely | Always |
| Sentence length | Short. Punchy. | Medium, clear | Longer, structured | Medium, flowing |
| Humor | Yes, irreverent | Subtle at most | No | Gentle, relatable |
| Numbers | Round ("~10K") | Specific ("10,847") | Very specific ("10,847.3") | Rounded ("over 10,000") |
| CTAs | "Let's go" / "Try it" | "Start Free Trial" | "Begin Implementation" | "Get Started Today" |
| Problem framing | "This sucks" | "This is costing you" | "The data shows" | "We've been there" |
| Proof style | Social ("everyone's using it") | Metrics ("47% improvement") | Data ("p < 0.05") | Stories ("Here's Sarah's story") |
| Exclamation marks | Sparingly | Never | Never | Occasionally |

---

## SECTION LIBRARY (16 Sections)

Each section includes: purpose, when to include, copy framework, and component specification.

### Section 1: Navigation

**Purpose:** Global navigation with primary CTA in nav bar.
**Include:** Always (every archetype).

```typescript
// Server Component — no interactivity needed for desktop
// Mobile nav toggle requires 'use client' — separate MobileNav component

interface NavProps {
  logo: { text: string; href: string }
  links: { label: string; href: string }[]
  cta: { label: string; href: string }
}
```

**Design rules:**
- Sticky on scroll (not fixed from start — reveal on scroll-up)
- CTA button in nav, right-aligned, uses primary accent color
- Mobile: hamburger menu, CTA remains visible
- Max-width container, consistent with page sections
- No dropdown menus on a landing page — keep navigation flat

### Section 2: Hero — Product Screenshot Variant

**Purpose:** Hook in 5 seconds. Value prop + primary CTA + social proof.
**Include:** SaaS Trial, SaaS Demo, Mobile App (with app mockup)
**Copy framework:** Headline formula + subheadline + CTA + social proof badge

```typescript
interface HeroProductProps {
  headline: string           // 6-12 words, specific outcome, from formula list
  subheadline: string        // Who it's for + what they get, 1-2 sentences
  primaryCTA: { label: string; href: string }
  secondaryCTA?: { label: string; href: string }
  socialProof?: string       // "Trusted by 2,847 teams" — SPECIFIC number
  productImage: { src: string; alt: string }  // Real screenshot, NOT mockup
}
```

**Layout:** Split layout (60% text / 40% image) on desktop, stacked on mobile.
**Copy rules:** Headline from formula list. Subheadline expands with audience + outcome. Social proof uses exact numbers.

### Section 3: Hero — Results Variant

**Purpose:** Lead with the outcome, not the product.
**Include:** Service/Agency, E-commerce

```typescript
interface HeroResultsProps {
  headline: string           // Outcome-focused, from formula list
  subheadline: string
  primaryCTA: { label: string; href: string }
  secondaryCTA?: { label: string; href: string }
  metrics: { value: string; label: string }[]  // 2-3 key metrics
  socialProof?: string
}
```

**Layout:** Centered text with metric cards below headline.

### Section 4: Hero — Waitlist Variant

**Purpose:** Capture emails with urgency and exclusivity.
**Include:** Waitlist/Launch

```typescript
interface HeroWaitlistProps {
  headline: string           // Excitement + specificity
  subheadline: string        // What's coming + why sign up now
  waitlistCount?: string     // "1,247 people already signed up"
  emailPlaceholder: string   // "you@company.com"
  ctaLabel: string           // "Join the Waitlist" / "Get Early Access"
}
```

**Layout:** Centered, single-column focus. Email input + CTA button inline.
**This section requires `'use client'`** for form handling.

### Section 5: Logo Bar

**Purpose:** Instant social proof. Recognizable names build trust.
**Include:** SaaS Trial, SaaS Demo, Service/Agency, Mobile App (as "Featured In"), E-commerce
**Skip:** Waitlist/Launch (unless you have press logos)

```typescript
interface LogoBarProps {
  heading?: string           // "Trusted by" / "Featured in" / "Used by teams at"
  logos: { name: string; src: string }[]  // 4-8 logos
  metric?: string            // "2,847 companies" — SPECIFIC number
}
```

**Design rules:** Grayscale logos, full color on hover. Single row with wrap. Subtle top/bottom borders.

### Section 6: Problem

**Purpose:** Make visitors feel understood. Be specific about THEIR pain.
**Include:** SaaS Trial, SaaS Demo, Service/Agency, Waitlist/Launch, E-commerce
**Copy framework:** PAS (Problem-Agitate-Solution) for the Problem step

```typescript
interface ProblemProps {
  headline: string           // "Sound familiar?" / Address the pain directly
  problems: {
    stat: string             // Specific number: "6 hours/week"
    pain: string             // The problem: "Switching between 12 tools"
    consequence: string      // The cost: "Missed deadlines and frustrated teams"
  }[]                        // 3 problems maximum
}
```

**Copy rules:**
- NEVER start with "In today's fast-paced world..."
- Use second person ("you" / "your team")
- Each problem has a specific stat, pain, and consequence
- Problems should resonate immediately — use customer language

### Section 7: Solution

**Purpose:** Bridge from problem to your product. Transition moment.
**Include:** SaaS Trial, SaaS Demo, Service/Agency, Waitlist/Launch

```typescript
interface SolutionProps {
  headline: string           // "There's a better way" / "Meet [Product]"
  description: string        // 2-3 sentences: what it is + core value
  keyPoints: string[]        // 3 bullet points of immediate value
  visual?: { src: string; alt: string }  // Product screenshot or diagram
}
```

### Section 8: Benefits

**Purpose:** Show outcomes, not features. Before/after transformation.
**Include:** All archetypes (core section)

```typescript
interface BenefitItem {
  before: string             // The old way (pain)
  after: string              // The new way (outcome)
  proof: string              // Specific result with number
  visual?: { src: string; alt: string }
}

interface BenefitsProps {
  headline: string           // "What changes for you"
  benefits: BenefitItem[]    // 3 benefits maximum
}
```

**Layout:** Alternating rows (image-text, text-image) for visual rhythm.
**Copy rules:** Every benefit has a before/after and a proof point with a number.

### Section 9: How It Works

**Purpose:** Reduce perceived complexity. Show the path to value.
**Include:** SaaS Trial, SaaS Demo, Service/Agency, Mobile App, E-commerce

```typescript
interface HowItWorksProps {
  headline: string           // "How it works" / "3 steps to [outcome]"
  steps: {
    number: number
    title: string            // Short action: "Connect your tools"
    description: string      // What happens + timeframe: "2 minutes, no code"
  }[]                        // 3-4 steps maximum. Never more than 4.
}
```

**Design rules:** Numbered steps with connecting line/arrows. Horizontal on desktop, vertical on mobile.

### Section 10: Feature Grid

**Purpose:** Show specific capabilities for visitors who want detail.
**Include:** SaaS Trial, SaaS Demo, Mobile App, E-commerce
**Skip:** Waitlist/Launch (too early for feature depth), Service/Agency (use Case Study instead)

```typescript
interface FeatureGridProps {
  headline: string
  features: {
    title: string            // 2-4 words: "Real-time sync"
    description: string      // 1-2 sentences: what it does + why it matters
    icon?: string            // Icon name from Heroicons — NO generic icons
  }[]                        // 4-6 features in 2x2 or 3x2 grid
}
```

**Copy rules:** Each feature title is specific (not "Advanced Analytics" — say "See which deals close this quarter"). Description connects feature to outcome.

### Section 11: Testimonials

**Purpose:** Social proof with specific outcomes. Real people, real results.
**Include:** SaaS Trial, SaaS Demo, Service/Agency, E-commerce, Mobile App

```typescript
interface TestimonialItem {
  quote: string              // Specific outcome: "We closed $847K from leads Acme surfaced"
  metric?: string            // "47x ROI" / "+340% leads"
  author: string             // Real name
  role: string               // Real title
  company: string            // Real company
  avatar?: string            // Real photo path — NEVER stock
}

interface TestimonialsProps {
  headline?: string          // Optional: "Don't take our word for it"
  testimonials: TestimonialItem[]  // 3 testimonials (odd number for grid)
}
```

**Copy rules:** NEVER use generic testimonials like "Great product!" Every quote must include a specific outcome or number. If the user has no testimonials, skip this section and use Logo Bar or metrics instead.

### Section 12: Case Study

**Purpose:** Deep proof. One customer story with measurable results.
**Include:** SaaS Demo, Service/Agency
**Skip:** All others unless user provides case study data

```typescript
interface CaseStudyProps {
  headline: string           // "How [Company] achieved [result]"
  company: string
  challenge: string          // 1-2 sentences
  solution: string           // 1-2 sentences
  results: { metric: string; label: string }[]  // 2-3 result metrics
  quote?: { text: string; author: string; role: string }
  logo?: string
}
```

### Section 13: Comparison

**Purpose:** Address "how is this different?" objection directly.
**Include:** SaaS Demo, Service/Agency, E-commerce
**Optional:** SaaS Trial (if competitive landscape is crowded)

```typescript
interface ComparisonProps {
  headline: string           // "Why teams switch to [Product]"
  product: string            // Your product name
  competitors: string[]      // 1-2 competitor names or "Traditional approach"
  features: {
    label: string
    product: boolean | string    // true/false or specific value
    competitors: (boolean | string)[]
  }[]
}
```

**Design rules:** Table format on desktop, card-based on mobile. Your product column highlighted.

### Section 14: Pricing

**Purpose:** Make the decision easy. Clear tiers, clear value.
**Include:** When user said "Yes, show pricing" (Q12)
**Skip:** Pre-launch, enterprise-only, "Contact for pricing"

```typescript
interface PricingTier {
  name: string               // "Starter" / "Pro" / "Enterprise"
  price: string              // "$29" or "Free"
  period: string             // "month" / "year"
  description: string        // WHO this tier is for specifically
  features: string[]         // What they GET, not vague capabilities
  cta: { label: string; href: string }
  highlighted?: boolean      // true for recommended tier
}

interface PricingProps {
  headline: string           // "Simple pricing. No surprises."
  subheadline?: string       // Guarantee: "Cancel anytime. No questions asked."
  tiers: PricingTier[]       // 2-3 tiers. 3 is ideal.
  billingToggle?: boolean    // Monthly/annual toggle
}
```

**Copy rules:**
- Tier descriptions say WHO it's for: "For solo founders just getting started"
- Features list concrete things: "Up to 5 team members" not "Team collaboration"
- Recommended tier uses `highlighted: true`
- NEVER use "Contact us for pricing" as a tier — that goes in a separate CTA

### Section 15: FAQ

**Purpose:** Handle objections. Reduce support burden. Boost SEO with FAQPage schema.
**Include:** All archetypes (critical for SEO and objection handling)
**This section requires `'use client'`** for accordion behavior

```typescript
interface FAQProps {
  headline: string           // "Questions? Answers." — keep it short
  faqs: { question: string; answer: string }[]  // 5-8 FAQs
}
```

**Copy rules for FAQ content:**
- Questions should be REAL objections, not softballs
- NEVER: "What makes your platform unique?" (softball)
- INSTEAD: "What if I've already tried 3 other tools and they all failed?" (real objection)
- Answers should be direct, specific, and honest
- Include at least one pricing/refund FAQ if relevant
- Include at least one "Is this right for me?" FAQ

**FAQ generates FAQPage JSON-LD automatically** — see SEO section.

### Section 16: Final CTA

**Purpose:** Last chance to convert. Restate the promise. Handle final objection.
**Include:** All archetypes

```typescript
interface FinalCTAProps {
  headline: string           // Restate the core promise from Hero
  subheadline: string        // Handle the final "but what if..." objection
  primaryCTA: { label: string; href: string }  // Same CTA as Hero
  guarantee?: string         // Risk reversal: "30-day money-back guarantee"
}
```

**Copy rules:** Headline mirrors Hero but from a slightly different angle. If Hero said "Close deals 40% faster," Final CTA says "Start closing more deals today." Always include a guarantee or risk reversal.

### Section 17: Footer

**Purpose:** Legal, navigation, and secondary links.
**Include:** Always

```typescript
interface FooterProps {
  logo: { text: string; href: string }
  columns: {
    title: string
    links: { label: string; href: string }[]
  }[]
  social?: { platform: string; href: string }[]
  legal: string              // "(c) 2026 Company Name. All rights reserved."
}
```

---

## SECTION ORDER ALGORITHM

Each archetype has a default section order. The algorithm also applies insertion rules for CTA repetition and social proof distribution.

### Default Orders by Archetype

**SaaS Trial (10-12 sections):**
1. Nav
2. Hero (Product Screenshot)
3. Logo Bar
4. Problem
5. Solution
6. Benefits
7. How It Works
8. Feature Grid
9. Testimonials
10. Pricing (if included)
11. FAQ
12. Final CTA
13. Footer

**SaaS Demo (9-11 sections):**
1. Nav
2. Hero (Product Screenshot)
3. Logo Bar
4. Problem
5. Solution
6. How It Works
7. Case Study
8. Comparison
9. Testimonials
10. FAQ
11. Final CTA
12. Footer

**Mobile App (8-10 sections):**
1. Nav
2. Hero (Product Screenshot — app mockup)
3. Logo Bar ("Featured In")
4. Benefits
5. How It Works
6. Feature Grid
7. Testimonials
8. FAQ
9. Final CTA (App Store badges)
10. Footer

**Service/Agency (9-11 sections):**
1. Nav
2. Hero (Results)
3. Logo Bar
4. Problem
5. Solution
6. How It Works
7. Case Study
8. Testimonials
9. Pricing (if included)
10. FAQ
11. Final CTA
12. Footer

**Waitlist/Launch (6-8 sections):**
1. Nav
2. Hero (Waitlist)
3. Problem
4. Solution
5. Benefits
6. FAQ
7. Final CTA
8. Footer

**E-commerce (8-10 sections):**
1. Nav
2. Hero (Results — product image)
3. Benefits
4. How It Works
5. Feature Grid
6. Testimonials
7. Comparison
8. FAQ
9. Final CTA
10. Footer

### Insertion Rules

1. **CTA Repetition:** Insert a mid-page CTA after the Benefits or How It Works section if the page has 10+ sections. Use a simple centered CTA block, not a full Final CTA.
2. **Social Proof Distribution:** If testimonials come late (position 8+), insert a single inline testimonial quote after the Problem or Solution section.
3. **Serial Position Effect:** The most important conversion arguments go in positions 2-4 (primacy) and the last 2 sections before footer (recency). The middle is for detail/depth.

---

## DESIGN SYSTEM LAYER

### Factory-Inspired (Default)

This is the id8Labs design system. Applied by default unless user chooses otherwise.

```typescript
const factoryTokens = {
  colors: {
    background: '#020202',       // Near-black
    foreground: '#eeeeee',       // Near-white
    muted: '#737373',            // Warm gray for secondary text
    border: '#262626',           // Subtle borders
    accent: '#ef6f2e',           // Orange — primary action color
    accentSecondary: '#f59e0b',  // Amber — highlights, badges
    accentTertiary: '#4ecdc4',   // Teal — success states, links
    surface: '#0a0a0a',          // Slightly lighter than background for cards
  },
  typography: {
    fontFamily: {
      sans: "'Geist', system-ui, -apple-system, sans-serif",
      mono: "'Geist Mono', 'SF Mono', 'Fira Code', monospace",
    },
    fontWeight: {
      normal: 400,
      medium: 500,               // Body emphasis
      semibold: 600,             // Headings
    },
    letterSpacing: {
      tight: '-0.02em',         // Headings
      normal: '-0.01em',        // Body
    },
  },
  spacing: {
    section: 'py-20 md:py-28',  // Between sections
    container: 'max-w-6xl mx-auto px-6',
  },
  rules: [
    'NO shadows',
    'NO gradients',
    'NO glow effects',
    'NO border-radius larger than 8px (rounded-lg max)',
    'NO decorative elements that serve no function',
    'Borders: 1px solid, subtle',
    'Cards: surface background + border, no shadow',
    'Buttons: solid fill, no gradients, sharp or slightly rounded',
  ],
}
```

### Light & Clean Preset

```typescript
const lightTokens = {
  colors: {
    background: '#ffffff',
    foreground: '#1a1a1a',
    muted: '#6b7280',
    border: '#e5e7eb',
    accent: '#2563eb',           // Blue
    accentSecondary: '#7c3aed',  // Purple
    surface: '#f9fafb',
  },
  // Typography: Same Geist family, weight 400-600
  // Rules: Subtle shadows allowed, rounded-xl allowed
}
```

### Bold & Colorful Preset

```typescript
const boldTokens = {
  colors: {
    background: '#0f172a',       // Dark navy
    foreground: '#f8fafc',
    muted: '#94a3b8',
    border: '#334155',
    accent: '#f43f5e',           // Rose
    accentSecondary: '#8b5cf6',  // Violet
    surface: '#1e293b',
  },
  // Typography: Geist or custom display font, weight 600-800
  // Rules: Gradients on CTA buttons only, larger border-radius allowed
}
```

### Custom Override System

When user selects "Custom" and provides brand colors/fonts:

1. Map provided colors to the token system (background, foreground, accent, etc.)
2. If fewer than 3 colors provided, fill gaps from nearest preset
3. Generate Tailwind config extension with custom colors
4. Apply custom font via `next/font` or CDN import
5. Validate contrast ratios: accent-on-background must be WCAG AA (4.5:1 minimum)

---

## COMPONENT ARCHITECTURE

### File Structure

```
app/
  page.tsx                    # Main landing page (Server Component)
  layout.tsx                  # Root layout with metadata
  globals.css                 # Tailwind + custom tokens
  components/
    nav.tsx                   # Navigation (Server Component)
    hero.tsx                  # Hero variant (Server Component)
    logo-bar.tsx              # Logo bar (Server Component)
    problem.tsx               # Problem section (Server Component)
    solution.tsx              # Solution section (Server Component)
    benefits.tsx              # Benefits section (Server Component)
    how-it-works.tsx          # How It Works (Server Component)
    feature-grid.tsx          # Feature grid (Server Component)
    testimonials.tsx          # Testimonials (Server Component)
    case-study.tsx            # Case study (Server Component)
    comparison.tsx            # Comparison table (Server Component)
    pricing.tsx               # Pricing (Server Component)
    faq.tsx                   # FAQ accordion ('use client')
    final-cta.tsx             # Final CTA (Server Component)
    footer.tsx                # Footer (Server Component)
    mobile-nav.tsx            # Mobile hamburger ('use client')
    waitlist-form.tsx         # Waitlist email form ('use client')
```

### Server/Client Component Boundaries

**Server Components (default):** All content sections. Landing pages are content-heavy — server rendering is correct for performance and SEO.

**Client Components (only when interactive):**
- `faq.tsx` — Accordion open/close state
- `mobile-nav.tsx` — Hamburger menu toggle
- `waitlist-form.tsx` — Email form submission (Waitlist archetype only)
- `pricing.tsx` — Only if billing toggle is included

### Conventions

- All components are functional, TypeScript strict
- Props interfaces exported alongside components
- No `any` types
- Tailwind only — no CSS modules or styled-components
- `next/image` for all images with explicit width/height
- `next/font` for font loading (Geist from `geist` package)
- `next/link` for internal links
- Semantic HTML elements: `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- Each section wrapped in `<section>` with descriptive `id` for anchor links

---

## SEO & STRUCTURED DATA LAYER

### Metadata Template

Generated in `layout.tsx` using Next.js Metadata API:

```typescript
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: '[Product Name] — [Core Value Prop in 5-8 words]',
  description: '[150-160 char meta description with primary keyword, value prop, and CTA hint]',
  keywords: ['primary keyword', 'secondary keyword', 'brand name'],
  openGraph: {
    title: '[Product Name] — [Value Prop]',
    description: '[Same as meta description or slightly varied]',
    url: 'https://[domain]',
    siteName: '[Product Name]',
    type: 'website',
    images: [
      {
        url: '/og-image.png',     // 1200x630 recommended
        width: 1200,
        height: 630,
        alt: '[Product Name] — [Brief description of what's shown]',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: '[Product Name] — [Value Prop]',
    description: '[Meta description]',
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
  },
  alternates: {
    canonical: 'https://[domain]',
  },
}
```

### JSON-LD Structured Data

Generate as a `<script type="application/ld+json">` in `layout.tsx`.

**Always include:**

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "name": "[Company Name]",
      "url": "https://[domain]",
      "logo": "https://[domain]/logo.png",
      "sameAs": ["[social URLs]"]
    },
    {
      "@type": "WebSite",
      "name": "[Product Name]",
      "url": "https://[domain]"
    }
  ]
}
```

**Conditional schemas:**

- **SaaS / Mobile App:** Add `SoftwareApplication` with `applicationCategory`, `operatingSystem`, `offers`
- **E-commerce:** Add `Product` with `offers`, `aggregateRating` (if available)
- **FAQ section present:** Add `FAQPage` with all Q&A pairs from the FAQ section
- **Pricing section present:** Add `offers` to the appropriate type

**FAQPage schema (auto-generated from FAQ section):**

```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[answer text]"
      }
    }
  ]
}
```

### Semantic HTML Rules

- One `<h1>` per page (the Hero headline)
- `<h2>` for each section headline
- `<h3>` for sub-section headers within sections
- Never skip heading levels (h1 -> h3)
- Use `<main>` wrapper around all content sections
- Use `<nav>` for navigation
- Use `<footer>` for footer
- Use `<blockquote>` for testimonials
- Use `<ul>` / `<ol>` for lists (not divs with dashes)
- All images have descriptive `alt` text
- All interactive elements are keyboard-accessible

---

## PERFORMANCE & ACCESSIBILITY

### Core Web Vitals Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| LCP | < 2.5s | Server Components, optimized images, `next/font` preload |
| INP | < 200ms | Minimal client JS, no heavy event handlers |
| CLS | < 0.1 | Explicit image dimensions, font `display: swap`, no layout shifts |

### Performance Rules

- **Images:** Always use `next/image` with explicit `width` and `height`. Use `priority` on hero image only. Use `loading="lazy"` on all below-fold images.
- **Fonts:** Load via `next/font/google` or `next/font/local` for Geist. Subset to `latin`. Use `display: swap`.
- **JavaScript:** Minimal. Only FAQ accordion, mobile nav, and waitlist form need client JS. No animation libraries.
- **CSS:** Tailwind utility classes only. No unused CSS. Purge in production build.

### WCAG 2.1 AA Requirements

- **Color contrast:** 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold)
- **Focus states:** Visible focus ring on all interactive elements (buttons, links, form fields)
- **Keyboard navigation:** All interactive elements reachable via Tab. Logical tab order.
- **Screen reader:** Semantic HTML, proper heading hierarchy, descriptive alt text, ARIA labels on icon-only buttons
- **Reduced motion:** Respect `prefers-reduced-motion` — no animations for users who opt out
- **Touch targets:** Minimum 44x44px on mobile

---

## QUALITY GATE

**All 22 checks must pass before delivery. Any failure gets explained and fixed.**

### Copy Quality (6 checks)

| # | Check | How to Verify |
|---|-------|---------------|
| C1 | Zero Tier 1 banned phrases | Scan all text for Tier 1 words |
| C2 | All Tier 2 phrases replaced with specifics | Scan for Tier 2, verify replacements have numbers |
| C3 | No structural AI tells | Check for cookie-cutter intros, uniform paragraphs, transition word abuse |
| C4 | Every claim has a number, example, or proof | Read each benefit/feature claim — must have specificity |
| C5 | Passes Logo Swap Test | Read hero + benefits — could this be any product? |
| C6 | Voice matches brand (from Q9) | Read aloud — does it match the voice modulation table? |

### Design Quality (5 checks)

| # | Check | How to Verify |
|---|-------|---------------|
| D1 | No design slop patterns | Check against the 10-item design slop list |
| D2 | Color contrast WCAG AA | Verify accent-on-background ratio >= 4.5:1 |
| D3 | Consistent design tokens | All colors, fonts, spacing from the selected token set |
| D4 | Layout has personality | Fails if three identical card rows or perfectly symmetrical everything |
| D5 | Mobile-responsive | All sections work at 375px width |

### Technical Quality (6 checks)

| # | Check | How to Verify |
|---|-------|---------------|
| T1 | TypeScript strict — no errors | `npx tsc --noEmit` passes |
| T2 | Build succeeds | `npm run build` passes |
| T3 | One `<h1>`, proper heading hierarchy | Scan HTML output for heading tags |
| T4 | All images have alt text | Scan for `<img>` and `next/image` — all have `alt` |
| T5 | JSON-LD validates | Check structured data syntax |
| T6 | Server/Client boundaries correct | Only FAQ, mobile nav, and forms use `'use client'` |

### Conversion Quality (5 checks)

| # | Check | How to Verify |
|---|-------|---------------|
| V1 | Primary CTA visible above fold | Hero section has CTA without scrolling |
| V2 | CTA repeated at least 3 times | Nav CTA + Hero CTA + Final CTA minimum |
| V3 | Social proof within 2 scrolls of CTA | Logo bar or testimonial near top and bottom CTAs |
| V4 | Objections addressed (FAQ covers real concerns) | FAQ has genuine objections, not softballs |
| V5 | Risk reversal present | Guarantee, free trial, or "cancel anytime" messaging exists |

### Quality Gate Procedure

1. After generating all components, run each check sequentially
2. For any failure: explain what failed, why it matters, and fix it
3. Re-run the failed check after fixing
4. Report final gate status:
   ```
   QUALITY GATE: PASSED (22/22)
   - Copy: 6/6
   - Design: 5/5
   - Technical: 6/6
   - Conversion: 5/5
   ```
5. If build/typecheck fails, fix and re-run until passing

---

## DELIVERY & A/B TEST SUGGESTIONS

### Delivery Checklist

After the quality gate passes, deliver:

1. **All component files** in the file structure specified above
2. **Quality gate results** showing 22/22
3. **A/B test suggestions** (3 testable hypotheses)
4. **Next steps** for the user

### A/B Test Suggestion Generator

For every page, generate 3 testable hypotheses using this format:

```
HYPOTHESIS [1-3]:
If we [specific change],
then [primary metric] will [increase/decrease] by [estimated %],
because [rationale from conversion psychology].

TEST: [What to change — Control vs. Variant]
METRIC: [Primary metric to measure]
PRIORITY: [High/Medium/Low using ICE scoring]
```

**Default test ideas by archetype:**

**SaaS Trial:**
1. Headline A vs. Headline B (outcome-focused vs. specificity-focused)
2. Hero with product screenshot vs. hero with demo video
3. Pricing section present vs. "See Pricing" CTA that links to separate page

**SaaS Demo:**
1. Single CTA ("Request Demo") vs. dual CTA ("Request Demo" + "Watch 2-min Video")
2. Case study above testimonials vs. below
3. Comparison table included vs. excluded

**Waitlist/Launch:**
1. Waitlist count shown vs. hidden
2. "Join Waitlist" vs. "Get Early Access" CTA copy
3. Problem section included vs. hero-only minimal page

---

## QUICK REFERENCE

### Trigger Table

| User Says | This Skill Does |
|-----------|----------------|
| "Build a landing page for X" | Full pipeline: interview -> generate -> deliver |
| "Create a landing page" | Full pipeline with smart defaults |
| "I need a page for my SaaS" | Full pipeline, pre-classified as SaaS |
| "Landing page for [product name]" | Full pipeline |
| "Build me a page" | Full pipeline with smart defaults |

### When to Use Other Skills Instead

| Situation | Use This Instead |
|-----------|-----------------|
| "Optimize this existing page" | `page-cro` or `landing-page-optimizer` |
| "Rewrite the copy" | `copywriting` |
| "Add schema markup" | `schema-markup` |
| "Full SEO audit" | `seo-audit` |
| "Design a layout" | `layout-designer` |
| "Build a React component" | `ui-builder` |
| "A/B test this page" | `ab-test-designer` + `ab-test-setup` |
| "Optimize this form" | `form-cro` |

### Pipeline Shortcut Commands

- **Full pipeline:** "Build a landing page for [product]" — runs all phases
- **Skip interview:** "Build a landing page for [product]. SaaS trial, professional voice, factory design." — skips to generation
- **Specific archetype:** "Build a waitlist page for [product]" — pre-classifies and runs

---

*Consolidates intelligence from: landing-page-designer, copywriting, page-cro, form-cro, signup-flow-cro, schema-markup, seo-audit, layout-designer, ab-test-designer, ui-builder, and 50+ research sources on conversion psychology, CRO, and design.*
