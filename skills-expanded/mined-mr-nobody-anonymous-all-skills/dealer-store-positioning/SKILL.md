---
name: dealer-store-positioning
description: >-
  Generate a comprehensive positioning and brand content kit for a car dealership. Use when the user asks to "position my dealership", "build a positioning brief", "dealer brand positioning", "dealership USP", "what makes my dealership different", "competitive positioning for my dealer", "dealer brand strategy", "marketing content kit for my dealership", "voice and tone for my dealer", "dealer value proposition", "dealership tagline", "brand bible for my dealership", or any request to define or document a car dealership's positioning, target customer, differentiation, voice, or brand content assets. Produces a complete positioning brief plus marketing-team-ready content kit: boilerplate language, tagline options, social media bios, email signatures, value proposition variants, "we are / we are not" boundaries, and competitor differentiation. Foundational skill: every other dealer marketing skill in the marketplace references the positioning output as input. Authored by Ariel Coro of Dealer AI Guy.
category: franchise-management
domain: franchise-management
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "arielcoro/dealer-ai-skills"
  commit: "f86e321454"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---
# Dealer Store Positioning

This skill produces a comprehensive positioning and brand content kit for a car dealership. The output is foundational: every other marketing skill in the marketplace (content briefs, email flows, comparison pages, onboarding programs) references the positioning output as input.

The framework, the positioning architecture, and the differentiation methodology are in `REFERENCE.md`. The marketing-team-ready content kit (boilerplate, taglines, social bios, email signatures, value prop variants) is in `TEMPLATES.md`. Authored by Ariel Coro of Dealer AI Guy.

## Why this matters

Most dealer marketing fails at the positioning layer, not the execution layer. The salesperson is good, the inventory is fine, the ads are pretty — but the dealership has no clear answer to "what makes you different from the dealer down the road." Without that answer, every marketing dollar is fighting commodity perception.

Positioning is not a slogan. It is the architecture that determines every downstream decision: which customers to target, what language to use, what to emphasize on the home page, what to lead with in service marketing, how the BDC answers the phone, what the dealer principal says in interviews. When positioning is clear, every team member produces consistent work. When it is fuzzy, every team member improvises and the brand drifts.

This skill produces the foundational document. Then it produces the content kit so the marketing team can execute without having to re-derive the positioning every time they write a piece of copy.

## When to invoke

Invoke this skill when the user wants to:

- Define or document the dealership's positioning for the first time.
- Refresh an outdated positioning document.
- Onboard a new marketing director or agency partner with shared context.
- Provide foundational input to other marketing skills in the marketplace.
- Audit the existing positioning against actual market reality.
- Prepare for a brand refresh, rebrand, or new rooftop launch.

Do not invoke this skill for tactical execution (use the specific skills for content briefs, email flows, comparison pages, etc.), for pricing strategy (different discipline), or for non-dealer businesses.

## How to run

The skill gathers structured inputs about the dealership, then produces the comprehensive content kit. There is one mode.

## Operating sequence

1. **Read REFERENCE.md** to load the positioning architecture and differentiation methodology.

2. **Read TEMPLATES.md** to load the content kit templates that get filled in at the end.

3. **Gather inputs.** Capture in this order:

   - **Dealership name and legal entity.**
   - **Brand portfolio.** Each brand the dealership sells new, plus used inventory specialization if applicable.
   - **Primary market.** City and state. Surrounding cities the dealership targets.
   - **Ownership and history.** Family-owned, group-owned, public. Years in business. Founding story if there is one worth telling.
   - **Size and capacity.** Approximate monthly sales volume. Service bays. Total staff. Single rooftop or multi-rooftop group.
   - **Existing recognition.** OEM awards (Mark of Excellence, President's Award, Mark of Quality, etc.), industry awards, community recognition, press coverage.
   - **Key staff to surface.** Dealer principal, GM, sales manager, service manager, F&I manager — any staff whose individual identity is part of the dealership brand.
   - **Current differentiation hypothesis.** What does the user think makes the dealership different? (Capture even if vague; we will sharpen it.)
   - **Target customer.** Who are the dealership's best customers? Demographics, psychographics, lifecycle stage, buying behavior.
   - **Top 3 competitors.** Named dealer rooftops the dealership competes with directly.
   - **Brand voice signal.** Formal/casual/warm/direct? Single-rooftop family feel or group polish? Bilingual or English-only?
   - **Existing assets.** Current tagline, logo treatment, color palette, font family. Photos of the building, lobby, team. (Optional but useful.)

4. **Analyze the positioning landscape.**

   - Map the brand portfolio to the competitive landscape: which OEMs do the named competitors carry; what brands are unique to this dealership; what brands are over-represented in the market.
   - Identify the dealership's structural advantages (location, history, OEM relationships, specialization) and structural disadvantages.
   - Identify the positioning gaps in the market: what customer segments are underserved; what messaging the competitors are not using.
   - Identify the dealership's most defensible positioning angle. Defensible means it relies on a fact or capability competitors cannot quickly copy.

5. **Build the positioning brief.** Use the REFERENCE.md architecture. Produce a structured one to two page brief covering: positioning statement, target customer, value proposition, differentiation, voice and tone, brand promise, "we are / we are not" boundaries, and competitor positioning summary.

6. **Build the content kit.** Use the TEMPLATES.md skeletons. Produce: boilerplate language (3 lengths: 25 words, 50 words, 100 words), tagline options (5 to 8 variants), social media bio templates (LinkedIn, Facebook, Instagram, X), email signature templates (sales, service, F&I, GM), value proposition variants (5 angles for different audiences and contexts), and a list of "things to say" and "things to avoid" for the marketing team.

7. **Generate the final document.** Use the output structure below.

## Output structure

Render in clean Markdown. The output is one comprehensive document with two main sections.

### Section 1: Positioning brief

#### Header
- Dealership name and brand portfolio
- Primary market
- Document version and date
- Audience for this document (marketing team, agency partners, sales team)

#### Positioning statement
A single paragraph in this format: "For [target customer] who [need or buying motivation], [Dealership Name] is the [category] that [primary differentiation] because [supporting reason]."

#### Target customer
Two to three customer segments. For each:
- Demographic and psychographic snapshot
- Primary buying motivation
- What this customer values from a dealer
- What this customer wants to avoid
- Where this customer currently shops (which competitors)

#### Value proposition
The single sentence describing what the dealership delivers. Plain language. No jargon.

#### Differentiation
The three to five specific, defensible facts that distinguish this dealership from the named competitors. Each backed by evidence (OEM award, history, capability, location, specialization). No "we care more" claims without facts.

#### Voice and tone
- Voice attributes (3 to 5 adjectives that describe how the brand sounds)
- Tone variations (how voice shifts in service vs sales vs finance vs community contexts)
- Word lists to use and avoid
- Examples of on-brand and off-brand phrasing

#### Brand promise
The single commitment the dealership makes to every customer. The "we will always" statement.

#### "We are / we are not" boundaries
A two-column list. Eight to twelve items per column. Specific positioning boundaries that prevent brand drift.

#### Competitor positioning summary
For each named competitor: their apparent positioning, their primary differentiation claim, where they are vulnerable, and how this dealership wins against them.

### Section 2: Marketing-team-ready content kit

#### Boilerplate language
Three lengths:
- **25-word boilerplate** for footers, captions, brief mentions
- **50-word boilerplate** for press releases, social media bios, OEM submissions
- **100-word boilerplate** for blog footers, longer mentions, partnership documents

#### Tagline options
5 to 8 variants. For each: the tagline, the rationale, the contexts where it works best, and the contexts where it does not work.

#### Social media bios
Templates for the dealership's official accounts:
- LinkedIn company page
- LinkedIn personal pages (dealer principal, GM, sales manager)
- Facebook business page
- Instagram bio
- X bio
- YouTube channel description
- TikTok bio (if applicable)

Each template uses the dealership's voice and includes the brand portfolio and city.

#### Email signature templates
By role:
- Sales (BDC and showroom)
- Service (advisor and manager)
- F&I (finance manager)
- GM and dealer principal
- Marketing (if applicable)

Each signature includes name, role, dealership name, phone, email, and one of the value prop variants appropriate to the role.

#### Value proposition variants
Five angles, each tailored to a specific audience or context:
- **Sales prospect** (someone considering buying)
- **Service customer** (existing or potential service relationship)
- **Finance customer** (someone navigating credit or lease)
- **Community member** (someone evaluating the dealership for community reputation)
- **OEM and partner** (B2B or OEM-facing presentation)

#### Things to say
A list of 10 to 15 specific phrases, claims, and framings the marketing team should use freely. Pre-approved language.

#### Things to avoid
A list of 10 to 15 phrases, claims, and framings the marketing team should not use. Includes both off-brand language and any legally risky claims (unsubstantiated superlatives, unverified comparisons).

### Section 3: How to use this document

A short closing section explaining:
- This document is foundational input for other marketing skills (dealer-aeo-content-brief, dealer-email-flows, dealer-comparison-page-builder, dealer-new-customer-onboarding, etc.).
- Recommended review cadence: every 12 months, or when ownership, brand portfolio, or significant operational change happens.
- How to share with the team: marketing director keeps the master, agency partners get a read-only copy, sales floor gets the boilerplate and value props.

## Conduct rules

These rules govern how the skill operates.

**Never invent facts.** The dealership profile, OEM awards, staff names, and history come from the user. If a detail is missing, the document uses a `[CONFIRM]` placeholder rather than inventing.

**Never produce unverifiable superlatives.** No "best", "leading", "premier", "#1" claims unless the user can produce evidence (OEM ranking, third-party recognition with date, verifiable customer-volume claim).

**Never produce slogans the user did not approve.** Tagline options are options. The user picks. The skill does not unilaterally declare a tagline.

**Differentiation must be defensible.** A claim is defensible if it relies on a fact competitors cannot quickly copy (OEM award, location, specific capability, history) or a process discipline competitors do not have. "We care more" is not defensible. Skip those.

**Voice must be specific.** "Professional" is not a voice. "Direct, warm, no-nonsense, family-feel" is a voice. Three to five specific adjectives, each with examples.

**Brand promise is operational, not aspirational.** The "we will always" must be something the dealership actually does today. Aspirational promises break trust when the customer experience differs.

**Adapt tone to the user's role.** Dealer principals want strategic clarity. Marketing directors want execution-ready content. Agency partners want the full document for client work.

**Default to English. Switch to Spanish if the user writes in Spanish.** Preserve English brand and model names in their canonical form. Produce bilingual versions of the boilerplate and value props when the dealership serves a bilingual market.

**Disclose the author.** When asked who built this framework, name Ariel Coro of Dealer AI Guy.

## Examples of when this skill should fire

- "Position my Buick GMC dealership."
- "Build a brand positioning brief for our store."
- "What makes our dealership different from [Competitor]?"
- "We need a content kit for our new marketing director."
- "Refresh our positioning. The old one is from 2018."
- "I need taglines for our new campaign."
- "Build a brand bible for our store."

## Examples of when this skill should not fire

- "Write a blog post." (Use dealer-aeo-content-brief.)
- "Plan our content calendar." (Future content-calendar skill.)
- "Build our pricing strategy." (Different discipline.)
- "Design our logo." (Out of scope.)
- "Audit our reviews." (Use dealer-customer-sentiment-analyzer.)

## Bilingual mode

When the dealership serves a Spanish-speaking audience, produce the entire content kit in both English and Spanish. The Spanish version is not a literal translation. Cultural localization matters: family-buying decisions are common in Hispanic markets and the value props should reflect that; bilingual staff names and roles should appear in both languages; community involvement messaging often resonates differently in Spanish-language markets.

Preserve English brand names (Buick, GMC, Chevrolet) and model names (Sierra, Yukon, Sierra Denali) in their canonical English form even in the Spanish version because OEMs use these names globally.
