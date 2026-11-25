---
name: demo-builder
description: "Build an impressive demo website (homepage + sample service/location pages) for client presentations and feedback. Generates a brief compatible with /website-builder for full build continuation. Triggers: 'build demo', 'demo site', 'client demo', 'demo website', 'pitch site', 'sample site'."
---

# Demo Builder Skill

**You are a coordinator. You do NOT write code yourself. You orchestrate agents and enforce quality gates.**

This skill builds an impressive but reduced-scope demo site to show clients what you can deliver. When the client approves, `/website-builder` continues the full build using the same brief and artifacts.

## AUTONOMOUS EXECUTION MODE

**After Phase 0 brief confirmation, execute ALL remaining phases (1-4) without stopping for user input.**

Rules:
1. When a gate **PASSES** -> immediately begin the next phase. Do not summarize, do not ask "shall I proceed?", do not pause.
2. When a gate **FAILS** -> spawn agents to fix the issues, re-run the gate, and continue when it passes. Do NOT escalate to the user unless stuck.
3. Never ask "shall I proceed?" or "ready for the next phase?" after Phase 0. Just do it.
4. If stuck after 2 fix attempts on the same gate, document the blocker and skip to the next phase if possible.

---

## Phase 0: Gather Requirements

Before any research or coding, you need a specification. There are two paths:

### Step 0.0: Check for Existing Spec
Read `/spec/brief.md`. If it exists and contains filled-in business information (not just the template), **skip to Phase 1**.

### Step 0.1: Interview the User (if no spec exists)
If no spec exists, interview the user using `AskUserQuestion` in 5 grouped rounds. Use smart defaults so users can breeze through quickly.

**Round 1 - Business Basics:**
- Business name
- Phone number
- Email address
- Physical address (if applicable)

**Round 2 - What You Do:**
- Business description (2-3 sentences)
- Unique selling points (what makes you different?)
- Target audience (homeowners, businesses, etc.)
- Years in business

**Round 3 - Services & Locations:**
- List of ALL services offered (full list -- needed for brief compatibility with /website-builder)
- List of ALL locations/areas served (full list)
- **Proof per location**: "For the full build, a town only earns its own page if there's real proof there. For EACH town, do you have reviews from there, jobs completed there, and original photos of that work?" Capture which towns qualify. This carries forward so /website-builder can build proof-backed location and matrix pages (not a templated grid).
- **Demo selection**: "For the demo, I'll build 2-3 representative service pages and 2-3 location pages. Which services and locations are most important to showcase first?" (Default: prioritise the proof-backed towns; otherwise first 2-3 of each list)

**Round 4 - Design & Tech:**
- Design aesthetic -- present these options:
  - **Premium Agency** (high-end feel -- luxury fonts, spring animations, layered depth) -- default
  - **Clean Editorial** (minimal, Notion/Linear inspired -- warm monochrome, serif contrast, flat grids)
  - **Bold Industrial** (raw, mechanical -- Swiss typography, rigid grids, utilitarian)
  - **Pick for me** -- auto-select based on business type
- Brand colors (or "pick for me" -- default)
- Reference websites for inspiration (optional)
- Tech stack -- default: Next.js + ShadCN + Tailwind CSS
- Logo file path (optional, can add later)

**Round 5 - Content & Features:**
- Competitor URLs (for research -- optional but recommended)
- Testimonials (real ones, or "generate placeholders")
- Accreditations/certifications
- Special features -- default: contact form + Google Maps embed

### Step 0.2: Generate the Brief
Write `/spec/brief.md` from the interview answers using the SPEC_TEMPLATE format. Fill in all sections with the gathered information. Use smart defaults for anything the user skipped.

Include a "Design Aesthetic" field recording the chosen style and as the aesthetic direction to pass to `frontend-design:frontend-design`.

**Add the `## Demo Build Scope` section at the bottom** listing which pages are included in the demo and which are deferred to the full build.

### GATE 0: Brief Confirmation
Present a summary of the generated brief to the user and ask them to confirm before proceeding. Use `AskUserQuestion` with options like "Looks good, proceed" / "I need to change something".

**If the user wants changes, update the brief and re-confirm.**

---

## CRITICAL: Content Is Not Optional

The whole point of a demo is to impress the client. Placeholder content will NOT impress anyone.

**Content research and writing happens BEFORE coding. This is non-negotiable.**

---

## CRITICAL: Quality Gates Are Non-Negotiable

This is a pitch site. Every page must look premium. Quality gates exist to ensure this.

**You MUST enforce quality gates at every phase. This is not optional.**

---

## DESIGN STANDARDS

**The demo MUST look like premium agency work. These rules prevent generic-looking output.**

### Hero Sections
- Hero text MUST be concise: headline (6-10 words max) + subheadline (1-2 short sentences) + CTA button
- NEVER dump a full paragraph into the hero. Long descriptions belong BELOW the fold.
- Hero should create visual impact through typography scale, imagery, and whitespace -- not word count.
- Hero headline should use a large, distinctive display font size (e.g., text-5xl/6xl on desktop, text-3xl/4xl on mobile).

### Typography Hierarchy
- There MUST be clear visual distinction between H1, H2, H3, and body text (size, weight, AND spacing)
- H1 should be dramatically larger than body text, not just slightly bigger
- Use font weight contrast (bold headings, regular body) not just size
- Line height and letter spacing matter -- body text needs comfortable reading line-height (1.6-1.8)

### Content Layout (Anti-Wall-of-Text)
- Break long content into scannable sections with: subheadings, bullet points, icons, cards, or grid layouts
- No section should present more than 3-4 sentences as a continuous block without a visual break
- Use cards, grids, or columns to present service lists, features, and benefits -- NOT sequential paragraphs
- Alternate section layouts (e.g., text-left/image-right, then image-left/text-right, then full-width cards)

### Visual Interest
- Every page needs visual rhythm: vary section backgrounds (white, light grey, brand-tinted, dark)
- Use the brand's accent color intentionally for CTAs, highlights, and key elements -- not everywhere
- Add subtle depth: shadows on cards, hover states on interactive elements, border treatments
- Icons or images should accompany service/feature lists, not just text

### Spacing
- Generous whitespace between sections (py-16 to py-24, not py-4 to py-8)
- Consistent internal padding on cards and containers
- Mobile spacing can be tighter but should still breathe

### What NOT to Do
- DO NOT create heroes with 3+ sentences of text
- DO NOT use the same layout pattern for every section on a page
- DO NOT present services/features as a plain text list -- use cards or a grid
- DO NOT use identical section backgrounds throughout the page
- DO NOT use generic/safe fonts (Inter, Roboto, Arial) unless the brief specifically requests them

---

## DESIGN & ANTI-SLOP INTEGRATION

Based on the design aesthetic chosen in Phase 0, include these skills in ALL agent prompts:

**Always include in EVERY coder agent prompt:**
- `frontend-design:frontend-design` -- distinctive, intentional visual design that avoids generic AI layout patterns, visual defaults, typography cliches, stock copy, and component templates. Prevents the demo from looking like every other AI-generated site.

**Always include in EVERY copywriter agent prompt:**
- `no-ai-slop` -- bans AI writing defaults (stock phrases, structural patterns, tonal habits, word-level cliches). Ensures content sounds human, not like a median of all AI writing.

**Aesthetic direction (from the brief's Design Aesthetic), passed to `frontend-design`:**

| Aesthetic | Direction | Notes |
|-----------|-----------|-------|
| Premium Agency | Refined, high-end | Default. Luxury type, layered depth, spring-based motion. Sub-vibes: ethereal glass, editorial luxury, soft structuralism |
| Clean Editorial | Minimal, editorial | Warm monochrome, serif/sans contrast, flat bento grids |
| Bold Industrial | Raw, utilitarian | Swiss typography, rigid grids, mechanical feel |

**Demo-site tone:** professional rather than experimental, with subtle motion (reduces animation-related gate failures) and default content density.

**How to include in coder prompts:**
"Use the `frontend-design:frontend-design` skill with the aesthetic direction from the brief's Design Aesthetic. Keep the design professional rather than experimental and the motion subtle."

**How to include in copywriter prompts:**
"Use the `no-ai-slop` skill. Avoid all banned phrases, structural patterns, and tonal habits listed in that skill."

---

## Pre-Flight Checks (BEFORE ANY CODING)

### 1. Verify Browser Tools
```
FIRST, verify you can use browser automation:
- Try to navigate to any URL
- Try to take a screenshot
- If either fails: STOP and tell user to fix browser tools
```

**If browser tools don't work, DO NOT proceed with website building.**

### 2. Start Dev Server
After the first coder creates the initial project:
```
npm run dev
```
Verify it's accessible at localhost:3000 (or configured port).

### 3. Take Initial Screenshot
Navigate to localhost and take a screenshot. This confirms tools work.

---

## Build Process (With Mandatory Quality Gates)

### Phase 1: Quick Research & Content (BEFORE ANY CODING)

**This phase is MANDATORY. Do not skip to coding.**

#### Step 1.1: Light Market Research
Spawn `market-research` agent with:
```
Research content requirements for a [BUSINESS TYPE] website targeting [LOCATIONS].

ABBREVIATED SCOPE (demo build):
1. Analyze 2-3 competitor URLs from the brief
2. For the top 3 primary keywords, check what content is ranking
3. Note word count ranges and required sections

OUTPUT:
Create /spec/content-requirements.md with:
- Minimum word count per page type (homepage, service, location)
- Required content sections per page type
- Key content gaps competitors are missing
```

#### Step 1.2: Write Content for Demo Pages (parallel with 1.3)
Spawn `copywriter` agent with:
```
Write content for the demo pages defined in the brief.

INPUTS:
- Read /spec/brief.md for business info, services, locations
- Read /spec/content-requirements.md for word count minimums
- Check the "Demo Build Scope" section for which pages to write

IMPORTANT: Use the `no-ai-slop` skill. Follow ALL its rules:
- Never use banned phrases ("In today's landscape", "Let's dive in", "Here's the thing", "At its core", etc.)
- Never use banned structural patterns (broad sweeping opener, "Final thoughts" section, rhetorical question transitions)
- Never use banned tonal patterns (breathless enthusiasm, false-authority voice, hedging every claim)
- Never use banned words (landscape, paradigm, leverage, robust, seamless, ecosystem, delve, navigate, unlock)
- Write like a specific human with a specific voice — not like a median of all writing on the internet

PAGES TO WRITE:
- homepage.md (full effort)
- about.md (full effort)
- contact.md (contact info + form description)
- services/[demo-service-1].md (full effort)
- services/[demo-service-2].md (full effort)
- services/[demo-service-3].md (full effort, if 3 selected)
- locations/[demo-location-1].md (full effort)
- locations/[demo-location-2].md (full effort)
- locations/[demo-location-3].md (full effort, if 3 selected)

NO matrix page content needed.

Each file should contain:
- Meta title
- Meta description
- H1
- Full page content with H2/H3 structure
- CTA text

QUALITY: This is a client pitch. Content must be compelling and professional.
```

#### Step 1.3: Generate Images (parallel with 1.2)
Spawn `art-director` agent with:
```
Generate images for the demo website based on the brief.

INPUTS:
- Read /spec/brief.md for business info, style direction, and brand

IMAGES TO GENERATE:
1. Homepage hero image (1920x1080)
2. Service page images (one per demo service, 1200x800)
3. About page image (1200x800)

OUTPUT:
Save to /public/images/ with clear naming.
Create /spec/image-manifest.md listing all images with alt text.
```

**GATE 1 (Combined)**: Verify ALL content files exist for demo pages, meet word counts, no placeholder text, AND images exist and are professional. If any fail, re-spawn the appropriate agent to fix. Proceed when all pass.

---

### Phase 2: Foundation + Homepage

#### Step 2.1: Project Setup + Homepage
Spawn coder agent(s) for:
- Next.js project creation, dependencies, base layout
- Navigation with links to all demo pages
- Footer with business info
- Full homepage build with real content from `/spec/content/homepage.md`

**IMPORTANT: Include in the coder prompt:**
- "Use the `frontend-design:frontend-design` skill with the aesthetic direction from the brief's Design Aesthetic. Keep the design professional rather than experimental and the motion subtle."
- "Read `/spec/brief.md` for brand colors, style direction, and typography preferences"
- "Follow the Design Standards -- especially hero section and typography rules"
- "Avoid generic AI defaults -- no default SaaS stack layout, no gradient blobs, no frosted glass cards, no stock copy patterns, no Inter font, no 3-column pricing cards"
- "Choose a distinctive heading font that matches the style direction (NOT Inter, Roboto, or Arial)"
- "Use real content from `/spec/content/homepage.md` -- NO placeholder text"

#### GATE 2: Homepage Quality Check
After coder completes:
- Start dev server if not running
- Spawn quality-check agent
- Quality check MUST screenshot at 375px, 768px, 1440px
- Quality check MUST verify real content is present
- **The homepage is the most important page for the demo. It must be impressive.**
- If quality check returns NOT READY with Critical issues: spawn coder agent(s) to fix, re-run quality-check. Proceed when it passes.

---

### Phase 3: Sample Pages + Light Polish

#### Step 3.1: Build Remaining Demo Pages
Spawn coder agent(s) for:
- About page (with content from `/spec/content/about.md`)
- Contact page (with content from `/spec/content/contact.md`)
- 2-3 service pages (with content from `/spec/content/services/`)
- 2-3 location pages (with content from `/spec/content/locations/`)

**CRITICAL**: All pages use real content from `/spec/content/`. NO placeholder text.
**CRITICAL**: Service and location pages must NOT be walls of text -- use cards, grids, icons, alternating layouts.
Coders MUST use `frontend-design:frontend-design` with the brief's aesthetic direction.
**CRITICAL**: Avoid generic AI defaults -- no stock layout patterns, no generic visual defaults, no cliche copy patterns.

#### Step 3.2: Light Polish
Same or new coder agent adds:
- Subtle animations (conservative)
- Hover states on cards and buttons
- Smooth transitions
- Mobile navigation (hamburger menu)

No separate gate between pages and polish -- tested together in Phase 4.

---

### Phase 4: Production Build + Final Quality Check

#### Step 4.1: Basic SEO
Spawn `seo-onpage` agent for:
- Meta tags on all demo pages (from content files)
- Basic LocalBusiness structured data
- No sitemap needed for demo

#### Step 4.2: Production Build
1. Run `npm run build`
2. Fix any build errors
3. Run `npm run start` (production server)

#### Step 4.3: Final Quality Check
Spawn quality-check agent for comprehensive review:

```
You are checking if this DEMO SITE is ready to show a client.

REMEMBER:
- Default to FAIL, not pass
- You're judging if this will win a paying client
- List EVERY issue, not just a few
- Compare to professional sites (Apple, Stripe, Linear)
- If ANY doubt, verdict is NOT READY

TEST THESE PAGES:
- Homepage
- About page
- Contact page
- 1 service page
- 1 location page

AT THESE VIEWPORTS:
- 375px (mobile)
- 768px (tablet)
- 1440px (desktop)

CHECKS:
- Real content on every page (no placeholders)
- No console errors
- No failed network resources
- Animation multi-screenshot test (immediately, after 2s, after scroll)
- All images load correctly
- Navigation works on all pages
- Mobile menu works

DESIGN VERIFICATION:
- Hero: concise (headline + subheadline + CTA) not wall of text
- Typography: clear visual hierarchy
- Layout variety: alternating section layouts
- Spacing: generous whitespace between sections
- Visual rhythm: varying section backgrounds

ANTI-SLOP DESIGN CHECK (generic AI defaults):
- Does the layout follow the generic SaaS stack (hero -> proof strip -> features -> pricing -> testimonials -> CTA)? = NOT READY
- Are there radial glows, blurred orbs, or gradient haze behind the hero? = NOT READY
- Are there frosted glass cards or translucent panels? = NOT READY
- Is the heading font Inter/Roboto/Arial without explicit brief justification? = NOT READY
- Stock copy patterns: "Trusted by...", "Built for...", "Everything you need", "Get Started"? = NOT READY
- Does it look like every other AI-generated website? = NOT READY

ANTI-SLOP CONTENT CHECK (from `no-ai-slop`):
- Content starts with "In today's landscape/world"? = NOT READY
- Uses "Let's dive in", "Here's the thing", "At its core"? = NOT READY
- Uses "seamless", "robust", "leverage", "ecosystem", "delve"? = NOT READY
- Ends with "Final thoughts" or "Key takeaways"? = NOT READY
- Feels like generic AI writing rather than a specific human voice? = NOT READY

WEB DESIGN PREMIUM-FEEL CHECK (any = NOT READY):
Halo-effect destroyers from `~/.claude/knowledgebase/website-design/checklist.md` (canonical gate). See `~/.claude/knowledgebase/website-design/applying-to-skills.md` for context.
- Hero fails 50ms blink test — within half a second, viewer cannot tell what the business is and why it matters; one feeling, not a buffet [KB: principles.md → Halo Effect]
- Stock-photo cliches — boardroom high-fives, group-around-laptop, faceless suits [KB: anti-patterns.md]
- No "star of the show" — nothing anchors the eye long enough to convert attention [KB: principles.md]
- All text at 100% opacity — no opacity hierarchy (anchor 100, body 87, meta 60) [KB: principles.md]
- No felt hover states on interactive elements — buttons/cards feel dead [KB: checklist.md]
- Hidden pricing or about-page-as-CV (founder bio instead of trust-building) [KB: anti-patterns.md]

The Three Questions:
1. Does this look like premium agency work? [YES/NO]
2. Would a client be impressed enough to pay for a full site? [YES/NO]
3. Does this compete with the best? [YES/NO]

If ANY answer is NO, verdict is NOT READY.
```

**GATE 4**: Must pass final quality check. If critical issues, fix and re-run (max 2 attempts). When it passes, proceed to completion.

---

## Completion & Handoff

When the final quality check passes, output:

```
DEMO COMPLETE
```

Then present the handoff summary to the user:

```markdown
## Demo Site Ready for Client Presentation

### What was built:
- Homepage
- About page
- Contact page
- [N] service pages: [list them]
- [N] location pages: [list them]

### Artifacts saved for full build:
- /spec/brief.md (complete specification with ALL services and locations)
- /spec/content/ (content for demo pages -- reusable)
- /spec/content-requirements.md (market research -- reusable)
- /spec/image-manifest.md (image inventory)
- Generated images in /public/images/
- Complete codebase with layout, components, and styles

### To continue with the full build:
Run `/website-builder` in this project directory.

It will:
1. Detect the existing brief and skip the interview
2. Extend content research to cover all planned pages
3. Write a dedicated pillar page for every service (the #1 local organic ranking factor)
4. Build proof-backed location pages (only towns with real reviews/jobs/photos, capped at 3-6) and matrix pages only for evidenced service+location combinations -- NOT a templated grid, which now harms rankings
5. Entity, GBP, and schema work: one source of truth for name/NAP/services terminology; specific LocalBusiness subtype schema with sameAs; GBP website link pointed at a strong non-homepage page (UTM-tagged); Bing Places + IndexNow at launch
6. Full SEO implementation with sitemap
7. Comprehensive quality gates at every phase

### What the full build adds:
- A dedicated pillar page for every remaining service
- Proof-backed location pages (evidenced towns only, capped at 3-6) with an "Areas We Cover" page for the rest
- Proof-backed service+location pages where real jobs/reviews/photos exist -- each passing the removed-city-name test
- Entity consistency, specific-subtype LocalBusiness schema with sameAs, and the GBP link/Bing Places/IndexNow launch steps
- Complete sitemap and internal linking
- Extended SEO optimization
- Exhaustive multi-phase quality gates
```

---

## Red Flags That Require Immediate Quality Check

If a coder mentions ANY of these, spawn quality-check immediately:
- "animation" / "opacity" / "transition" / "fadeIn"
- "should work" (without verification)
- Any console error, even "minor"
- "done" without mentioning screenshots
- Hero with more than 2 sentences of body text
- All sections using the same background color
- Services listed as paragraphs instead of cards/grid
- Coder uses Inter font, gradient blobs, frosted glass cards, or "Trusted by" copy (generic AI defaults)
- Layout follows generic hero -> proof strip -> features -> pricing -> testimonials -> CTA stack
- CTA text is "Get Started", "Book a Demo", or "Start Free Trial" (stock AI copy)

---

## Content Red Flags (STOP and FIX immediately)

If you see ANY of these, STOP and fix content first:
- "Lorem ipsum" or placeholder text anywhere
- "TODO", "FIXME", "[INSERT]", "[PLACEHOLDER]" in content
- Coder saying "I'll add content later"
- Pages with thin content that doesn't match spec
- Generic content without business name or location references

**This is a pitch site. Content shortcuts are NOT acceptable.**

---

## Anti-Sycophancy Reminder

The quality-check agent may try to be "helpful" by approving mediocre work.

If a quality check comes back positive but you have doubts:
1. Ask for a more critical re-evaluation
2. Request specific comparison to professional sites
3. Ask "Would a client be impressed enough to pay for a full build?"

**Do not trust rubber-stamp approvals. Challenge them if needed.**
