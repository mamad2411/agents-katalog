---
name: auto-setup
description: Bootstrap brand voice, ICP, and landing pages from your website URLs. Use when setting up the skill pack for the first time, or when onboarding a new client. Analyzes your website and pre-fills context skills automatically.
allowed-tools: Read, Write, Bash
---

# /auto-setup — Bootstrap Context from Your Website

Generate ready-to-use brand-voice, ICP, and landing-pages configurations by analyzing your existing website. Dramatically reduces setup time from 30+ minutes to under 5 minutes.

## Input Required

Ask the user for:
1. **Website URL(s)** — one or more pages to analyze. Recommended:
   - Homepage (required) — for brand voice, tone, key messaging
   - About/Team page — for company positioning and social proof
   - Pricing page — for offer structure and CTAs
   - Product/Features page — for USPs and feature language
   - Any localized pages (e.g., /de, /fr, /ar) — for multilingual setup
2. **Primary language** — the main language of the website (default: auto-detect)
3. **Target market** (optional) — if different from what the website suggests

Minimum viable input: just the homepage URL. Claude will extract what it can.

## Execution Steps

### Step 1: Fetch and Analyze Pages
For each provided URL:
- Fetch the page content
- Extract: headline copy, value propositions, feature descriptions, CTAs, trust signals, social proof (client logos, testimonials, numbers), pricing structure, navigation (to discover more pages), footer links, meta descriptions
- Detect language and tone
- If localized pages found in navigation (e.g., /de, /fr, /pl), note them for landing-pages setup

### Step 2: Generate Brand Voice Draft
Create a draft for `.claude/skills/brand-voice/SKILL.md` based on extracted data:

```
## Company
- Name: [extracted from logo/title/meta]
- Industry: [inferred from content]
- Primary market: [inferred from language, currency, references]

## Tone of Voice
- Primary tone: [analyzed from copy style — formal/casual, technical/accessible, etc.]
- Avoid: [inferred anti-patterns]
- Key adjectives: [extracted from self-description]

## Messaging Hierarchy
1. Primary: [main headline or hero value prop]
2. Secondary: [supporting benefit most prominent on page]
3. Tertiary: [differentiator or proof point]

## Social Proof Available
- [extracted numbers, client logos, testimonials, certifications, awards]

## CTAs Preferred
- EN: [extracted from buttons and CTA elements]
- [other languages if localized pages analyzed]

## Language-Specific Notes
- [populated per language detected]
```

### Step 3: Generate ICP Draft
Create a draft for `.claude/skills/icp/SKILL.md`:

- **Company-level ICP**: inferred from pricing (SMB vs enterprise), language (geography), industry references on the site, case studies/testimonials (who are their customers?)
- **Persona 1**: inferred from primary CTA target (who would click "Book a Demo"?), language/jargon used on the site, pricing page buyer (who signs the check?)
- **Persona 2** (if enough data): inferred from secondary navigation, different content sections targeting different roles

For each persona, fill in:
- Job titles (inferred from case studies, testimonials, "built for X" language)
- Pain points (extracted from "challenges we solve" or problem-oriented copy)
- Language they use (extracted from the site's own vocabulary)
- Ad messaging hints (based on what angles the site emphasizes)

### Step 4: Generate Landing Pages Registry
Create a draft for `.claude/skills/landing-pages/SKILL.md`:

- Register every URL the user provided
- Auto-detect language variants from navigation (hreflang, language switcher, /de/ /fr/ paths)
- Group by page type (homepage, pricing, demo, features, etc.)
- Cache the analysis for each page immediately

### Step 5: Present and Confirm
Show the user what was generated:

```
## Auto-Setup Complete

### Brand Voice (draft)
- Company: [name]
- Tone: [description]
- Primary message: [extracted]
- Social proof: [X items found]

### ICP (draft)
- Target company: [segment]
- Persona 1: [role] — [top pain point]
- Persona 2: [role] — [top pain point]

### Landing Pages
- [X] pages registered
- [X] languages detected
- [X] pages cached

### What to review:
1. Brand voice tone — is it accurate?
2. ICP personas — are these the right buyers?
3. Missing pages — any key URLs not included?
```

Ask: "Should I save these drafts? You can refine them later."

### Step 6: Save
If confirmed, write the generated content to:
- `.claude/skills/brand-voice/SKILL.md` (overwrite template)
- `.claude/skills/icp/SKILL.md` (overwrite template)
- `.claude/skills/landing-pages/SKILL.md` (overwrite template + create cache files)

If user wants to review first, save as:
- `output/draft_brand_voice.md`
- `output/draft_icp.md`
- `output/draft_landing_pages.md`

## Tips
- The more pages you provide, the better the output
- About/Team pages are gold for social proof extraction
- Pricing pages reveal the ICP (who they're selling to and at what price point)
- If the site has a blog, providing 1-2 blog posts helps with tone detection
- For multilingual sites, provide at least the homepage in each language

## After Auto-Setup
Once setup is complete, you're ready to generate ads:
- `/ads` — generate your first ad group
- `/ads-multi` — generate in all detected languages
- `/ads-review` — audit existing ads against the extracted brand context
