---
name: create-landing-page
description: Generates prospect-specific landing pages, microsites, and conversion-optimized standalone web pages for ABM/named-account selling, ad campaigns, partnerships, or product launches. Make sure to use this skill whenever the user says build a landing page for [prospect/campaign], create a microsite, make a conversion page, design a campaign page, build an ABM page for [account], partner co-branded page with [partner], or describes any standalone web page intended to convert specific traffic. Includes hero, social proof, conversion path, FAQ, and cybersec-specific trust elements (compliance badges, security architecture summary). Do NOT use for: full marketing sites with multi-page navigation (different scope — describe to Claude directly), multi-slide presentations (use create-deck), single-page printable collateral (use create-one-pager), or product walkthroughs (use create-workflow-demo). Defining characteristic: "standalone web page, conversion-focused, often campaign- or account-specific, lives at its own URL."
---

# Create Landing Page

Standalone conversion-focused web pages for ABM, campaigns, partnerships, and launches.

## When to use vs. adjacent asset skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Output is a single web page with conversion intent | Multi-slide presentation → `create-deck` |
| Lives at its own URL (microsite or campaign page) | Printable single-page handout → `create-one-pager` |
| Often prospect-, campaign-, or partner-specific | Walkthrough/demo script → `create-workflow-demo` |
| Includes form / CTA / tracking | Full marketing site with nav → describe to Claude directly |

## Landing page types this skill handles

### ABM (account-based) landing page
Hyper-personalized for one named account. Frequently used for strategic deals.

Standard structure:
1. **Hero** — Their logo + your logo + headline naming their world
   ("[CompanyName] runs on real-time data — your security shouldn't slow it down.")
2. **The relevance** — Why this page exists for them specifically
3. **The 3 outcomes** — quantified, framed in their KPIs
4. **Customer proof** — ideally a customer in their industry or with similar tech
5. **The proposed engagement** — pilot, eval, kickoff plan
6. **Direct booking** — calendar link to their named AE
7. **Resources** — relevant case studies, technical brief, security overview
8. **Footer** — company info + privacy + contact

### Campaign landing page
For a paid traffic campaign (Google, LinkedIn, conference sponsor). Optimized for traffic conversion.

Standard structure:
1. **Hero** — headline matching the ad copy + sub-headline + primary CTA
2. **Social proof row** — customer logos + ratings/awards
3. **The problem statement** — mirror of the ad targeting
4. **The 3-pillar solution** — what you do, structured around their problem
5. **Proof / testimonial** — quote with photo + outcome metric
6. **CTA repeat** — same as hero, mid-page anchor
7. **FAQ** — 5-7 questions handling top objections
8. **Final CTA** — different language, same destination
9. **Footer**

### Partner / co-branded landing page
For a joint go-to-market with another company.

Standard structure:
1. **Joint hero** — both logos, joint value prop
2. **The combined offer** — what you do better together
3. **Use case** — specific scenario where both products matter
4. **Implementation pattern** — how the integration works
5. **Customer story** (if applicable) — joint customer with quantified outcome
6. **CTA** — joint trial / joint demo / joint contact
7. **Resources from both companies**

### Product launch landing page
For announcing a new product or major release.

Standard structure:
1. **Hero** — new product name + tagline + visual
2. **Why we built this** — problem statement
3. **What it does** — 3 capabilities with visuals
4. **Demo or video**
5. **Availability / pricing / how to get it**
6. **Press / launch coverage row**
7. **Sign-up / trial / waitlist CTA**

## Conversion mechanics (apply to all types)

**Above the fold must answer:** What is this? Who is it for? What do you want me to do?

**One primary CTA per page.** Repeat it 2-4 times depending on length, but it's the same CTA. Multiple competing CTAs reduce conversion.

**Form length is conversion drag.** Each additional field drops conversion ~10%. Defaults:
- Demo request: name, work email, company. (Job title optional.)
- Trial: name, email. Verify email post-signup.
- Whitepaper: email only. Maybe company.
- Contact us: name, email, message.

**Loading speed matters.** Heavy hero images with no compression destroy mobile conversion. Aim for <2.5s LCP.

**Mobile-first.** 60%+ of B2B traffic is mobile. Layout must work in single-column.

**Trust elements:**
- Customer logos (real ones, with permission)
- Quantified social proof ("4.8 stars from 200 reviews on G2")
- Security/compliance badges (SOC 2, ISO 27001, etc.)
- Privacy assurances near forms ("We'll never share your email")
- Contact info visible (phone, address — increases trust)

## Cybersecurity-specific landing page elements

For security/cybersec product landing pages, layer in:

- **Compliance badge row** below hero — SOC 2 Type II, ISO 27001, HIPAA, PCI, FedRAMP
- **"How we secure your data" section** — encryption (in transit + at rest), data residency options, key management, sub-processor list link
- **Pen test / responsible-disclosure mention** — links to security page
- **Security architecture diagram** — high-level, not implementation-specific
- **Trust center link** — if you have one (e.g., trust.yourcompany.com), prominent placement
- **Customer attribution by security tier** — "Trusted by 12 SOC 2 Type II customers in healthcare" beats "trusted by enterprises"

## SEO defaults for organic-discovery landing pages

Even campaign pages benefit from organic findability:

- Title tag: primary keyword + value prop, ≤60 chars
- Meta description: primary + secondary keyword + soft CTA, ≤160 chars
- H1: matches the hero headline, contains primary keyword
- URL slug: short, keyword-led, hyphenated
- Schema markup: Organization, Product, FAQPage as applicable
- Image alt text: descriptive, accessibility + SEO double duty
- Internal links: 2-3 to related content / case studies / resources

## Anti-patterns

- **Generic headline** — "Welcome to AcmeSec" tells the visitor nothing
- **Hero hidden behind animation** — fancy intro that delays the value prop
- **Auto-playing video with sound** — instant bounce
- **Sticky popup before they scroll** — newsletter modal interrupting on page load
- **Form with 12 fields** — kills conversion, drops only marginally for shorter
- **Buried CTA** — visitor must scroll 4 screens to find what to do
- **Stock-photo hero** — handshake stock photos signal "generic vendor"
- **Inconsistent brand vs. parent site** — looks like phishing
- **Dead links** — case studies that 404, certifications that go to old PDF
- **No mobile testing** — half your traffic sees broken layout

## Output

Produces:
1. Full HTML landing page (single file, inline CSS, deployable)
2. Section-by-section content in markdown for review
3. SEO metadata (title, description, OG tags)
4. Form integration recommendation (HubSpot, Marketo, Pardot, plain email)
5. Tracking recommendation (analytics events to instrument)
6. Suggested A/B test (one specific variant worth testing)
7. Mobile-responsive layout verified
