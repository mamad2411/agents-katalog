---
name: website-builder
description: "Build a complete website for a local business with mandatory quality gates. Interviews the user if no spec exists. Triggers: 'build website', 'build site', 'create website', 'implement the site', 'build from spec'."
---

# Website Builder Skill

**You are a coordinator. You do NOT write code yourself. You orchestrate agents and enforce quality gates.**

**Local SEO source of truth:** `~/.agents/skills/references/shared-seo/local-seo-playbook-2026.md` (Whitespark 2026, Sterling Sky, December 2025 core update). The location/matrix page strategy, schema, GBP link, and launch rules in this skill follow that playbook. Read it for the evidence behind these rules.

## AUTONOMOUS EXECUTION MODE

**After Phase 0 brief confirmation, execute ALL remaining phases (1-9) without stopping for user input.**

Rules:
1. When a gate **PASSES** → immediately begin the next phase. Do not summarize, do not ask "shall I proceed?", do not pause.
2. When a gate **FAILS** → spawn agents to fix the issues, re-run the gate, and continue when it passes. Do NOT escalate to the user unless stuck.
3. Never ask "shall I proceed?" or "ready for the next phase?" after Phase 0. Just do it.
4. If stuck after 3 fix attempts on the same gate, document the blocker in `/spec/build-state.md` and skip to the next phase if possible.
5. Update `/spec/build-state.md` at the start and end of every phase (see Build State Tracking below).

## BUILD STATE TRACKING

Maintain `/spec/build-state.md` throughout the build. Create it at the start of Phase 1 (after Phase 0 confirmation). This file is critical for resumption if the session is interrupted.

**Format:**
```markdown
# Build State

## Current Phase
Phase [N]: [Phase Name] - [in_progress / completed]

## Phase Checklist
- [x] Phase 0: Gather Requirements
- [x] Phase 1: Content Research & Planning
- [ ] Phase 1.5: Design Concepting
- [ ] Phase 2: Content Writing & Image Generation
- [ ] Phase 3: Foundation
- [ ] Phase 4: Core Pages
- [ ] Phase 5: Additional Pages
- [ ] Phase 6: Polish & Animations
- [ ] Phase 7: SEO Implementation
- [ ] Phase 8: Production Build Test
- [ ] Phase 9: Final Quality Check

## Gate Results Log
| Phase | Gate | Result | Attempts | Notes |
|-------|------|--------|----------|-------|
| 1 | 1.1 | PASS | 1 | content-requirements.md created |
| 1 | 1.2 | PASS | 1 | keyword-mapping.md created |

## Blockers
[None currently]
```

**On every ralph-loop re-entry, read `/spec/build-state.md` FIRST to determine where to resume.** Check the filesystem for artifacts from completed phases. Do not repeat completed work.

## COMPLETION SIGNAL

When all phases are complete and the final quality check returns "READY TO SHIP":

Output: `<promise>BUILD COMPLETE</promise>`

**WARNING**: Do not output this tag unless ALL completion criteria are genuinely met. The ralph-loop stop hook watches for this exact string. Outputting it prematurely will end the build with an incomplete site.

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
- List of services offered
- List of locations/areas served
- **Proof per location:** for EACH town, does the client have real evidence there (reviews from that town, jobs completed there, original photos of that work)? Capture which towns qualify. This decides which towns earn their own page.
- Page strategy. **Default is PROOF-GATED, not a full grid:** one pillar page per service (always); a location page ONLY for towns the client can evidence with reviews/jobs/photos, capped at 3-6 for most trades; matrix (service × location) pages ONLY for proof-backed combinations. Every other town served is named on a single "Areas We Cover" page. Templated full matrices now actively harm rankings (doorway-page filtering, Dec 2025 core update).

**Round 4 - Design & Tech:**
- Design mood/tone — free text with examples to spark ideas:
  - "Warm & approachable" / "Bold & edgy" / "Minimal & refined" / "Playful & energetic" / "Luxury & premium" / "Raw & industrial" / or describe your own
  - Emphasize there's no wrong answer — this sets the creative direction for a unique design
- Reference websites for inspiration (strongly encouraged — "Share 2-3 websites you love the look of, from any industry. These don't need to be competitors — could be a restaurant site, a fashion brand, anything with a vibe you want")
- Brand colors (or "pick for me" — default)
- Tech stack — default: Next.js + ShadCN + Tailwind CSS
- Logo file path (optional, can add later)

**Round 5 - Content & Features:**
- Competitor URLs (for research — optional but recommended)
- Testimonials. REAL ones strongly preferred (named town, named job). Generated placeholders are permitted for the build ONLY and MUST be flagged as launch blockers for the client to replace before go-live.
- Original photos. REAL photos of the client's work, van, team, or premises are strongly preferred over stock or generated images (stock/AI imagery is a negative E-E-A-T signal; Google strips EXIF so geotagging does nothing). Generated placeholders are permitted for the build ONLY and MUST be flagged as launch blockers to replace.
- E-E-A-T details for the per-page block: who is the named person with a real credential (e.g. Gas Safe registration number) to feature on service/location pages?
- Accreditations/certifications
- Special features — default: contact form + Google Maps embed

### Step 0.2: Generate the Brief
Write `/spec/brief.md` from the interview answers using the SPEC_TEMPLATE format. Fill in all sections with the gathered information. Use smart defaults for anything the user skipped.

Include a "Design Direction" field recording the user's mood/tone choice, reference websites, and any specific creative preferences. This will feed into the Design Concepting phase.

### GATE 0: Brief Confirmation
Present a summary of the generated brief to the user and ask them to confirm before proceeding. Use `AskUserQuestion` with options like "Looks good, proceed" / "I need to change something".

**If the user wants changes, update the brief and re-confirm.**

---

## CRITICAL: Content Is Not Optional

Previous builds failed because:
- Content was "placeholder" that never got replaced
- Pages had thin 100-word content while competitors had 1500+ words
- Copywriting was skipped "to save time"
- SEO suffered because content didn't match search intent

**Content research and writing happens BEFORE coding. This is non-negotiable.**

---

## CRITICAL: Quality Gates Are Non-Negotiable

This skill exists because previous builds failed due to:
- No visual verification during development
- Quality checks running only after user complained
- Code reviewers only reading code, never looking at the browser
- Animation bugs making content invisible

**You MUST enforce quality gates at every phase. This is not optional.**

---

## DESIGN STANDARDS

**Previous builds failed because sites looked generic, bland, and text-heavy. These rules prevent that.**

### Hero Sections
- Hero text MUST be concise: headline (6-10 words max) + subheadline (1-2 short sentences) + CTA button
- NEVER dump a full paragraph into the hero. Long descriptions belong BELOW the fold.
- Hero should create visual impact through typography scale, imagery, and whitespace — not word count.
- Hero headline should use a large, distinctive display font size (e.g., text-5xl/6xl on desktop, text-3xl/4xl on mobile).

### Typography Hierarchy
- There MUST be clear visual distinction between H1, H2, H3, and body text (size, weight, AND spacing)
- H1 should be dramatically larger than body text, not just slightly bigger
- Use font weight contrast (bold headings, regular body) not just size
- Line height and letter spacing matter — body text needs comfortable reading line-height (1.6-1.8)

### Content Layout (Anti-Wall-of-Text)
- Break long content into scannable sections with: subheadings, bullet points, icons, cards, or grid layouts
- No section should present more than 3-4 sentences as a continuous block without a visual break
- Use cards, grids, or columns to present service lists, features, and benefits — NOT sequential paragraphs
- Alternate section layouts (e.g., text-left/image-right, then image-left/text-right, then full-width cards)

### Visual Interest
- Every page needs visual rhythm: vary section backgrounds (white, light grey, brand-tinted, dark)
- Use the brand's accent color intentionally for CTAs, highlights, and key elements — not everywhere
- Add subtle depth: shadows on cards, hover states on interactive elements, border treatments
- Icons or images should accompany service/feature lists, not just text

### Spacing
- Generous whitespace between sections (py-16 to py-24, not py-4 to py-8)
- Consistent internal padding on cards and containers
- Mobile spacing can be tighter but should still breathe

### What NOT to Do
- DO NOT create heroes with 3+ sentences of text
- DO NOT use the same layout pattern for every section on a page
- DO NOT present services/features as a plain text list — use cards or a grid
- DO NOT use identical section backgrounds throughout the page
- DO NOT use generic/safe fonts (Inter, Roboto, Arial) unless the brief specifically requests them

---

## DESIGN SKILL INTEGRATION

The design concept created in Phase 1.5 is the primary creative direction. The `frontend-design` skill supports that direction with design craft and anti-pattern avoidance — it does NOT replace it.

**Always include in EVERY coder agent prompt:**
- `frontend-design:frontend-design` — distinctive, intentional visual design that avoids templated defaults; applied in service of the design concept, not in place of it
- **`/spec/design-concept.md`** — the PRIMARY source for all creative decisions: fonts, colors, layouts, components, motion approach

**Always include in EVERY copywriter agent prompt:**
- `no-ai-slop` — bans AI writing defaults (stock phrases, structural patterns, tonal habits, word-level cliches)

**How to include in coder prompts:**
"Read and follow `/spec/design-concept.md` for ALL design decisions — typography, colors, layout patterns, component styles, and motion. Use the `frontend-design:frontend-design` skill for design craft and to avoid generic AI patterns. The design concept overrides any default aesthetic — follow its specific font, color, and layout choices."

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

### Phase 1: Content Research & Planning (BEFORE ANY CODING)

**This phase is MANDATORY. Do not skip to coding.**

#### Step 1.1: Market Research
Spawn `market-research` agent with this prompt:
```
Research content requirements for a [BUSINESS TYPE] website targeting [LOCATIONS].

1. COMPETITOR CONTENT ANALYSIS:
   - Analyze the competitor URLs from the brief
   - For each competitor, document:
     - Homepage word count and structure
     - Service page word counts (average and range)
     - Location page word counts (if they have them)
     - What content sections they include (FAQs, process steps, trust signals, etc.)

2. SERP CONTENT ANALYSIS:
   For each primary keyword in the brief:
   - What type of content is ranking? (service pages, guides, directories)
   - What's the average word count of top 5 results?
   - What content sections do top results include?
   - What questions are being answered?

3. OUTPUT REQUIREMENTS:
   Create `/spec/content-requirements.md` with:
   - Minimum word count per page type (homepage, service, location, matrix)
   - Required content sections per page type
   - Content gaps competitors are missing (opportunities)
   - Recommended FAQs based on "People Also Ask"
```

**GATE 1.1**: Verify `/spec/content-requirements.md` exists and contains word count requirements. If it does, immediately proceed to Step 1.2. If not, re-run the market-research agent.

#### Step 1.2: SEO Keyword Mapping
Spawn `seo-research` agent (or use market-research if unavailable) with:
```
Create keyword mapping for each page planned in the brief.

For each page type:
1. Primary keyword (1 per page)
2. Secondary keywords (2-3 per page)
3. LSI/related terms to include naturally
4. Search intent (informational, commercial, transactional)
5. Content angle based on what's ranking

Output to `/spec/keyword-mapping.md`
```

**GATE 1.2**: Verify `/spec/keyword-mapping.md` exists with keywords for every planned page. If it does, update `/spec/build-state.md` and immediately proceed to Phase 1.5. If not, re-run the seo-research agent.

---

### Phase 1.5: Design Concepting (BEFORE CONTENT OR CODING)

**This phase creates a unique design direction for this specific site. No two builds should look the same.**

#### Step 1.5.1: Design Research
Spawn a `ui-expert` agent with:
```
You are creating a unique design concept for a website. Use the `/frontend-design:frontend-design` skill's Design Thinking framework.

INPUTS:
- Read /spec/brief.md for: business type, mood/tone, reference websites, brand colors, target audience
- Read /spec/content-requirements.md for: page types, content structure, competitor analysis

YOUR PROCESS:
1. UNDERSTAND THE CONTEXT
   - What kind of business is this? What does their audience expect?
   - What mood/tone did the user request?
   - If reference websites were provided, analyze what makes them visually effective

2. COMMIT TO A BOLD AESTHETIC DIRECTION
   - Pick a clear conceptual direction and execute it with precision
   - This is NOT "Premium Agency" or "Clean Editorial" — it's a bespoke direction for THIS business
   - What's the ONE THING someone will remember about this site?
   - Bold maximalism and refined minimalism both work — the key is intentionality

3. MAKE SPECIFIC CHOICES (not generic ones)
   - Pick exact fonts (Google Fonts preferred for easy implementation)
   - Define exact hex values for the full palette
   - Choose specific layout patterns for each section type
   - Decide on a motion philosophy

ANTI-SLOP RULES (generic AI defaults to avoid):
- Do NOT default to: Inter, Roboto, Arial
- Do NOT default to: gradient blobs, frosted glass, radial glows
- Do NOT default to: centered hero with two buttons
- Do NOT default to: hero -> proof strip -> features -> pricing -> testimonials -> CTA
- Do NOT default to: 3-column equal card grids
- Do NOT default to: "Trusted by..." / "Get Started" / "Everything you need"
- If you catch yourself reaching for ANY common AI default, stop and make a genuinely different choice

OUTPUT: Create /spec/design-concept.md with this exact structure:

# Design Concept: [Business Name]

## Creative Direction
- **Tone:** [One clear sentence — not a generic label like "modern and clean"]
- **The Memorable Thing:** [What makes this site visually distinctive — be specific]
- **Differentiation:** [How this differs from competitor sites found in research]

## Typography
- **Display/Heading Font:** [Specific Google Font name] — [why this font suits the business]
- **Body Font:** [Specific Google Font name] — [why this pairing works]
- **Font Scale:** [Specific sizes — e.g., "H1: text-5xl md:text-7xl, H2: text-3xl md:text-4xl, Body: text-base md:text-lg"]
- **Special Treatment:** [Any distinctive typographic choices — large quotes, oversized numbers, etc.]

## Color Palette
- **Primary:** [#hex] — [what it conveys]
- **Secondary:** [#hex] — [usage]
- **Accent:** [#hex] — [used sparingly for CTAs and highlights]
- **Backgrounds:** [Not just "white" — specify section background variation: e.g., "#FAFAF8 main, #1a1a1a dark sections, #F0EDE8 warm sections"]
- **Text:** [#hex primary, #hex secondary/muted]

## Layout Patterns
For each section type, specify the EXACT layout approach:

### Hero
- **Layout:** [e.g., "Split screen — headline left (60%), atmospheric image right (40%)" or "Full-bleed image with overlay text bottom-left" — NOT "centered headline with two buttons"]
- **Content:** [What goes in the hero and what goes below the fold]

### Services/Features
- **Layout:** [e.g., "Asymmetric bento grid — 2 large cards top, 3 smaller below" or "Horizontal scroll cards" — NOT "3 equal columns"]
- **Card Style:** [If using cards — what makes them distinctive]

### Testimonials
- **Layout:** [e.g., "Large pull-quote with editorial typography" or "Stacked cards with photo + text side by side" — NOT "star rating + quote + avatar chip"]

### CTA Sections
- **Layout:** [e.g., "Dark section with large serif headline and single button" — NOT "Ready to get started?"]

### Footer
- **Layout:** [e.g., "Minimal single-line with links" or "Large 4-column with newsletter signup"]

## Motion & Animation
- **Philosophy:** [e.g., "Subtle and weighty — spring physics on interactions, gentle fade-ups on scroll" or "Bold and theatrical — staggered reveals, parallax depth"]
- **Page Load:** [What happens when the page first loads]
- **Scroll Behavior:** [How elements enter as user scrolls]
- **Hover States:** [How interactive elements respond]

## Component Style
- **Buttons:** [e.g., "Rounded pill with subtle shadow, no icon" or "Square with arrow trailing icon"]
- **Navigation:** [e.g., "Floating pill nav detached from top" or "Minimal left-aligned with hamburger on mobile"]
- **Cards:** [If used — specific border radius, shadow, padding, border treatment]
- **Icons:** [Style and source — e.g., "Phosphor Light, strokeWidth 1.5"]

## What NOT To Do (Site-Specific)
- [Patterns that would undermine this specific concept]
- [Common defaults for this business type to explicitly avoid]
- [At least 3 specific anti-patterns]
```

**GATE 1.5**: Verify `/spec/design-concept.md` exists and meets these criteria:
- Every section is filled in with SPECIFIC choices (no "TBD", no "standard", no "modern and clean")
- Font choices are NOT Inter, Roboto, or Arial
- Hero layout is NOT "centered headline with two buttons"
- At least 3 site-specific anti-patterns are listed
- The design concept reads as genuinely unique — not a template that could apply to any business

**If the design concept is too generic, re-spawn the ui-expert agent with stricter instructions. When it passes, update `/spec/build-state.md` and immediately proceed to Phase 2.**

---

### Phase 2: Content Writing & Image Generation (PARALLEL — BEFORE CODING)

**Do NOT proceed to coding until BOTH content and images are ready.**

Content writing and image generation run in parallel to save time. Images are generated from the brief and research output (not from content files, since content is being written simultaneously).

#### Track A: Content Writing

##### Step 2A.1: Write All Page Content
Spawn `copywriter` agent with:
```
Write content for all pages defined in the brief.

INPUTS:
- Read /spec/brief.md for business info, services, locations
- Read /spec/content-requirements.md for word count minimums
- Read /spec/keyword-mapping.md for SEO requirements

IMPORTANT: Use the `no-ai-slop` skill. Follow ALL its rules:
- Never use banned phrases ("In today's landscape", "Let's dive in", "Here's the thing", "At its core", etc.)
- Never use banned structural patterns (broad sweeping opener, "Final thoughts" section, rhetorical question transitions)
- Never use banned tonal patterns (breathless enthusiasm, false-authority voice, hedging every claim)
- Never use banned words (landscape, paradigm, leverage, robust, seamless, ecosystem, delve, navigate, unlock)
- Write like a specific human with a specific voice — not like a median of all writing on the internet

REQUIREMENTS:
- Each page MUST meet the minimum word count from content-requirements.md
- Include all required sections identified in research
- Naturally incorporate keywords from keyword-mapping.md
- Use the business's voice and USPs from the brief
- Write compelling CTAs
- Include local references for location pages
- E-E-A-T BLOCK on every service and location page: a named person with a real credential (e.g. Gas Safe registration number), reference to an original photo of real work, and a specific testimonial (named town, named job). Content must read as written from experience, not from a keyword brief. Where the client has not supplied a real testimonial or photo, use a clearly marked placeholder and note it as a launch blocker to replace.

OUTPUT:
Create /spec/content/ folder with:
- homepage.md
- about.md
- contact.md
- services/[service-slug].md (one per service, ALWAYS)
- locations/[location-slug].md (ONLY for proof-backed towns, capped at 3-6; see Matrix Page Guide)
- matrix/[location]-[service].md (ONLY for proof-backed combinations, NOT a full grid; see Matrix Page Guide)
- areas-we-cover.md (single page naming every other town served, not given its own URL)

Each file should contain:
- Meta title
- Meta description
- H1
- Full page content with H2/H3 structure
- CTA text

LOCATION & MATRIX PAGE CONTENT (CRITICAL, PROOF-GATED):
- Build location and matrix pages ONLY for towns/combinations with real proof (reviews, jobs, photos) recorded in the brief's proof-per-location fields. Do NOT generate a full service × location grid; templated matrices now harm rankings.
- Each location/matrix page MUST pass the removed-city-name test: swap the town name out and it must NO LONGER read fine. Aim for roughly 50% genuinely locally-unique content.
- Each page MUST have a unique opening paragraph with genuine local context
- At least 300 words per page must be unique to that specific place/combination
- Follow the Matrix Page Template Structure (see Matrix Page Guide below)
- Do NOT copy-paste between pages - each must be genuinely unique
```

**GATE 2A (CONTENT QUALITY CHECK)**:
Verify ALL content files exist and meet requirements:

```
For each content file, check:
[ ] File exists in /spec/content/
[ ] Word count meets minimum from content-requirements.md
[ ] Contains meta title and description
[ ] Has clear H1, H2, H3 structure
[ ] Includes primary keyword naturally
[ ] Has compelling CTA
[ ] No placeholder text ("Lorem ipsum", "[INSERT]", "TODO")

LOCATION & MATRIX PAGE VERIFICATION (if applicable):
[ ] ONLY proof-backed towns/combinations have content files (no full grid; unproven areas live on areas-we-cover.md instead)
[ ] Location pages capped at 3-6 for most trades
[ ] Spot-check 3+ location/matrix pages for uniqueness
[ ] Each passes the removed-city-name test (roughly 50% locally-unique content)
[ ] Opening paragraphs are DIFFERENT between pages
[ ] Meta descriptions are UNIQUE per page
[ ] Local context is genuine (not generic "We serve [location]")
```

**If ANY content file fails this check, re-spawn the copywriter agent to fix the failing content. Re-run this gate. Proceed only when all checks pass.**
**If location/matrix pages are duplicative, templated, or built as a full grid without proof, this is a CRITICAL failure. Re-spawn copywriter with specific instructions to make each page proof-backed and genuinely unique.**

#### Track B: Image Generation (runs in PARALLEL with Track A)

**Images are generated from the brief and research — NOT from content files (which are still being written).**

**REAL photos are strongly preferred over generated ones.** Original photography of the client's actual work, van, team, and premises is an E-E-A-T signal; stock and AI-generated imagery is a negative signal a quality rater (and increasingly the algorithm) can spot. Generated images are permitted for the build ONLY as placeholders and MUST be flagged in the image manifest as launch blockers for the client to replace with real photos before go-live. Do not waste effort geotagging; Google strips EXIF on upload.

##### Step 2B.1: Plan Image Requirements
Review the brief and research output to identify required images:

```
Required images (minimum):
- Hero image for homepage
- Hero/header image for each service page
- Hero/header image for each location page (if distinct)
- About page team/business image
- Any images referenced in the brief
```

##### Step 2B.2: Generate Images
Spawn `art-director` agent with:
```
Generate images for the website based on the brief and research.

INPUTS:
- Read /spec/brief.md for business info, style direction, and brand
- Read /spec/content-requirements.md for page types and structure
- Note the design requirements (colors, style direction) from the brief

IMAGES TO GENERATE:
1. Homepage hero image
   - Should convey: [main business value proposition from brief]
   - Style: [from brief - modern/traditional/etc.]
   - Dimensions: 1920x1080 (will be cropped responsively)

2. Service page images (one per service)
   - Should represent the service being performed
   - Professional, trustworthy appearance
   - Dimensions: 1200x800

3. About page image
   - Should convey trust and professionalism
   - Could be: team at work, business premises, or professional portrait style
   - Dimensions: 1200x800

OUTPUT:
Save images to /public/images/ (or /src/assets/images/) with clear naming:
- hero-homepage.jpg
- hero-[service-slug].jpg
- hero-[location-slug].jpg (if needed)
- about-team.jpg

Create /spec/image-manifest.md listing all generated images with:
- Filename
- Purpose
- Dimensions
- Alt text recommendation
- Launch-blocker flag: mark every AI-generated/placeholder image as "REPLACE WITH REAL PHOTO before launch" so the client knows which images are placeholders
```

**GATE 2B**: Verify images exist and are appropriate:
```
For each required image:
[ ] File exists in /public/images/ or equivalent
[ ] Image is appropriate for a professional business site
[ ] Image matches the style direction from the brief
[ ] No AI artifacts that look unprofessional
[ ] /spec/image-manifest.md exists with alt text recommendations
```

**If images look unprofessional or have obvious AI artifacts, re-spawn the art-director agent to regenerate them. Re-check. Proceed when all images pass.**

#### GATE 2 (Combined): Both Tracks Must Pass
**Do NOT proceed to Phase 3 until BOTH GATE 2A and GATE 2B pass. When both pass, update `/spec/build-state.md` and immediately begin Phase 3.**

---

### Phase 3: Foundation
1. Spawn coder agent(s) for project setup, dependencies, base layout
   **IMPORTANT: Include in the coder prompt:**
   - "Read and follow `/spec/design-concept.md` for ALL design decisions — typography, colors, layout patterns, component styles, and motion approach"
   - "Use the `frontend-design:frontend-design` skill for design craft and to avoid generic AI patterns"
   - "The design concept is your PRIMARY reference — follow its specific font, color, layout, and component choices exactly"
   - "Avoid generic AI defaults — no default SaaS stack layout, no gradient blobs, no frosted glass cards, no stock copy patterns, no Inter font, no 3-column pricing cards"
2. **GATE 3**: After coder completes:
   - Verify dev server is running
   - Navigate to localhost
   - Take screenshot
   - Check console for errors
   - If ANY issues: spawn coder agent to fix them, re-verify. When clean, update `/spec/build-state.md` and immediately proceed to Phase 4.

### Phase 4: Core Pages (WITH REAL CONTENT)
1. Spawn coder agent(s) for homepage, main pages
2. **CRITICAL**: Coders MUST use content from `/spec/content/` - NO placeholder text
3. **CRITICAL**: Coders MUST follow Design Standards:
   - Hero: use the specific layout pattern from `/spec/design-concept.md`. Move remaining content below the fold.
   - Break all long-form content into scannable layouts (cards, grids, alternating sections)
   - Vary section backgrounds per the palette defined in design-concept.md
   - Read and follow `/spec/design-concept.md` for all design decisions. Use the `frontend-design:frontend-design` skill
   - Avoid generic AI defaults — no stock layout patterns, no generic visual defaults, no cliche copy patterns
4. **GATE 4**: After coders complete:
   - Spawn quality-check agent
   - Quality check MUST screenshot at 375px, 768px, 1440px
   - Quality check MUST test homepage AND at least one inner page
   - **Quality check MUST verify real content is present (not Lorem ipsum)**
   - If quality check returns NOT READY or NEEDS WORK with Critical issues: spawn coder agent(s) to fix the issues, then re-run quality-check. When it passes, update `/spec/build-state.md` and immediately begin Phase 5.

### Phase 5: Additional Pages (Location/Service/Matrix) - WITH REAL CONTENT
1. Spawn coder agent(s) for remaining pages: service pillars, the proof-backed location/matrix pages, and the "Areas We Cover" page
2. **CRITICAL**: Coders MUST use content from `/spec/content/` for EVERY page
3. **CRITICAL**: Service and location pages must NOT be walls of text — use cards, grids, icons, alternating layouts
4. Coders MUST follow `/spec/design-concept.md` and use the `frontend-design:frontend-design` skill
5. **LOCATION & MATRIX PAGES**: Build ONLY the proof-backed pages defined in the brief and `/spec/content/`, NOT a full service × location grid (see Matrix Page Guide below)
4. **GATE 5**: After coders complete:
   - Spawn quality-check agent
   - Quality check MUST test representative pages from EACH template type
   - **Quality check MUST verify word counts on rendered pages match spec**
   - **Quality check MUST flag any placeholder or thin content**
   - If quality check fails: spawn coder/copywriter agent(s) to fix the issues, then re-run quality-check. When it passes, update `/spec/build-state.md` and immediately begin Phase 6.

### Phase 6: Polish & Animations
1. Spawn coder agent(s) for animations, transitions, polish
   - Coders MUST follow the motion approach from `/spec/design-concept.md`, use animation performance best practices (hardware-accelerated properties, no layout shift), and use `frontend-design:frontend-design` to avoid generic patterns
2. **GATE 6 (CRITICAL for animations)**:
   - Spawn quality-check agent
   - Quality check MUST take MULTIPLE screenshots:
     - Immediately on page load
     - After 2 seconds
     - After scrolling
     - After returning to top
   - If ANY screenshot shows invisible content: CRITICAL FAIL. Spawn coder agent to fix animation initial states (ensure content is visible without requiring scroll/interaction). Re-run the multi-screenshot check. When it passes, update `/spec/build-state.md` and immediately begin Phase 7.

### Phase 7: SEO Implementation & Final Touches
1. Spawn `seo-onpage` agent to implement:
   - Meta tags from `/spec/content/` files
   - **Structured data (schema), following the playbook:**
     - `LocalBusiness` with the SPECIFIC subtype (e.g. Plumber, HVACBusiness, Electrician) on the homepage and location pages, NOT the generic `LocalBusiness` type
     - NAP in schema character-identical to the Google Business Profile
     - `sameAs` array on the homepage listing the GBP, social profiles, and key directory listings (this tells Google these profiles are the same entity)
     - `Service` schema on service pages
     - `FAQPage` schema ONLY where there are genuine FAQs on the page
     - `Review`/`AggregateRating` ONLY where reviews are legitimately displayed on the page
   - Sitemap generation
   - Internal linking optimization
2. **Launch SEO steps (from the local SEO playbook):**
   - **GBP website link:** set (or document for the client to set) the Google Business Profile website link to a STRONG service or location page, NOT the homepage if the homepage already ranks organically for the money terms (Sterling Sky Diversity Update: a URL in the local pack can be suppressed from page-one organic). UTM-tag that link so GBP traffic is measurable in analytics.
   - **Bing Places:** claim and complete the listing (ChatGPT local search runs on Bing's index).
   - **IndexNow:** enable it (a toggle on Cloudflare) so Bing indexes page changes immediately.
3. **GATE 7**:
   - Verify all meta titles/descriptions are implemented (not defaults)
   - Verify schema uses the specific `LocalBusiness` subtype, NAP matches the GBP character for character, and the homepage carries a `sameAs` array
   - Verify the GBP link target (strong non-homepage page + UTM), Bing Places, and IndexNow are done or documented for the client
   - Quick visual check that nothing broke
   - When verified, update `/spec/build-state.md` and immediately begin Phase 8.

### Phase 8: Production Build Test
1. Run `npm run build`
2. Check for build errors
3. Run `npm run start` (production server)
4. **GATE 8**:
   - Take screenshots of PRODUCTION build
   - Compare to dev screenshots
   - **Core Web Vitals pass criteria (from the playbook): LCP < 2.5s, INP < 300ms, measured at the 75th percentile (p75) in field data.** Lab checks (Lighthouse / PageSpeed Insights) are a proxy during the build; the client confirms against p75 field data once the site has traffic.
   - If production differs from dev OR the CWV targets are missed: spawn coder agent to investigate and fix, re-build, re-check. When production matches dev AND the CWV targets are met, update `/spec/build-state.md` and immediately begin Phase 9.

---

## Matrix Page Guide (Service × Location Pages)

Matrix pages target "[Service] in [Location]" searches (e.g., "Boiler Repair in Greenhithe"). **They are PROOF-GATED, not built as a full grid.**

### The Proof-Gated Rule (READ THIS FIRST)

Post-December 2025 core update, templated full matrices actively HARM rankings (doorway-page filtering; sitewide quality assessment under the helpful content system, now baked into core ranking). The old "build every service × location combination" approach now loses traffic. The 2026 rule:

- **One pillar page per service, always.** This is the #1 local organic ranking factor.
- **Location pages ONLY for towns the client can evidence** with real reviews, jobs done, and original photos. **Cap at 3-6 for most trades**, not 15+. Two or three strong, evidenced city pages outperform fifteen templated ones, and the fifteen can now actively hurt you.
- **Matrix (service × location) pages ONLY for combinations with real proof:** jobs done there, reviews from there, photos from there, for that specific service. The default is NOT to build these; each one must earn its existence.
- **Everything else** is named on a single "Areas We Cover" page, not given its own URL.

Which towns and combinations qualify comes from the proof gathered at intake (Round 3) and recorded in the brief's proof-per-location fields. If a town has no proof, it does not get a page.

### The Removed-City-Name Test

Take the town name out of the page. Is it still obviously about that specific place? If you can swap the town name for another and the page still reads fine, it FAILS: it's a doorway page regardless of intent. **Aim for roughly 50% genuinely locally-unique content per location/matrix page** (BrightLocal benchmark).

### URL Structure

```
/[location]/[service]/
Examples (only where proof exists for that combination):
- /greenhithe/boiler-repair/
- /dartford/gas-safety-certificates/
- /bexley/central-heating-installation/
```

### Content Uniqueness Rules (CRITICAL)

**The #1 failure mode for matrix pages is duplicate content.** Each page MUST be unique.

**What makes each matrix page unique:**

| Element | How to Make Unique |
|---------|-------------------|
| **H1** | Include BOTH location AND service: "Boiler Repair in Greenhithe" |
| **Opening paragraph** | Mention specific local context (landmarks, area characteristics) |
| **Service details** | Same service info is OK, but intro/outro must be location-specific |
| **Local proof points** | "We've completed X jobs in [location]" or local testimonials |
| **Travel/coverage info** | Specific to that location's geography |
| **CTA** | Location-specific: "Call for boiler repair in Greenhithe" |
| **Meta title** | "[Service] in [Location] | [Business Name]" |
| **Meta description** | Unique per page, mentioning both service and location |

**FORBIDDEN (will cause duplicate content penalties):**
- ❌ Same opening paragraph across all matrix pages
- ❌ Only changing the H1 and leaving body identical
- ❌ Generic "We serve [location]" with no real local content
- ❌ Identical meta descriptions with just location swapped
- ❌ Copy-pasting service description without local context

### Matrix Page Template Structure

```markdown
# [Service] in [Location]

## Opening (MUST be unique per page - 100+ words)
- Mention specific local context for [Location]
- Reference how the service relates to this area
- Include local landmarks, neighbourhoods, or characteristics

## Why Choose [Business] for [Service] in [Location] (150+ words)
- Local experience/jobs completed in area
- Response time to this specific location
- Knowledge of local property types/systems

## Our [Service] Process (can be shared across matrix pages)
- Step 1...
- Step 2...
- Step 3...

## [Service] for [Location] Properties (unique section - 150+ words)
- Property types common in this area
- Common issues in this location
- Local regulations or considerations

## Areas We Cover Near [Location] (unique)
- List nearby areas
- Internal links to adjacent location pages

## FAQs: [Service] in [Location] (2-3 unique FAQs)
- Location-specific questions
- Can share some service FAQs but include local ones

## Get [Service] in [Location] Today (CTA - unique)
- Location-specific call to action
- Phone number
- "Serving [Location] and surrounding areas"
```

### Minimum Word Counts for Matrix Pages

```
From content-requirements.md, but typically:
- Minimum: 800 words per matrix page
- Target: 1000-1200 words
- At least 300 words MUST be unique to that specific page
```

### Internal Linking for Matrix Pages

Each matrix page should link to:
- **Parent service page**: /services/[service]/
- **Parent location page**: /[location]/
- **Adjacent matrix pages**: Same service in nearby locations
- **Related services**: Other services in the same location

```
Example links on /greenhithe/boiler-repair/:
- "Learn more about our boiler repair services" → /services/boiler-repair/
- "See all services in Greenhithe" → /greenhithe/
- "Boiler repair in nearby Dartford" → /dartford/boiler-repair/
- "Need a gas safety certificate in Greenhithe?" → /greenhithe/gas-safety-certificates/
```

### Quality Check for Matrix Pages

When quality-checking matrix pages, verify:
```
[ ] ONLY proof-backed combinations exist (no full grid; unproven areas are on the "Areas We Cover" page instead)
[ ] Each page has unique H1 with service AND location
[ ] Each page passes the removed-city-name test (roughly 50% locally-unique content)
[ ] Opening paragraphs are NOT identical across pages
[ ] Meta descriptions are unique per page
[ ] Local content is genuinely local (not generic)
[ ] Internal links work to parent service/location pages
[ ] Word count meets minimum (check 3-5 random matrix pages)
[ ] No "thin content" warnings from SEO perspective
```

**If matrix pages look templated/identical, or a full grid was built without proof, this is a CRITICAL failure. Fix before proceeding.**

---

### Phase 9: Final Quality Check
1. Spawn quality-check agent for comprehensive review
2. Quality check MUST:
   - Test ALL THREE viewports (375px, 768px, 1440px)
   - Test representative pages from every template
   - Check network tab for failed resources
   - Check console for errors
   - **CONTENT VERIFICATION**:
     - Verify NO placeholder text anywhere
     - Spot-check word counts on 2-3 pages against `/spec/content-requirements.md`
     - Verify meta titles/descriptions are unique per page (not defaults)
   - Run the "Three Questions" test:
     - Does this look like £10k+ agency work?
     - Would a business owner be proud?
     - Does this compete with the best in the industry?
3. **ONLY output `<promise>BUILD COMPLETE</promise>` if quality check returns "READY TO SHIP"**
   - If quality check returns NOT READY: spawn agents to fix issues, re-run quality check. Repeat until READY TO SHIP or 3 attempts exhausted (then document blockers).

#### Web Design Quality Gate (Premium-Feel Halo Check)

Zero auto-fail items from `~/.claude/knowledgebase/website-design/checklist.md`. The quality-check agent's auto-fail criteria now cover: 50ms halo, opacity hierarchy, star of show, no felt hover states. Verify on homepage + one inner page at all three viewports:

- **50ms blink test** — within half a second of load, hero communicates what the business does and why it matters [KB: checklist.md → Hero/50ms].
- **Opacity hierarchy present** — body copy uses 100/87/60 tiers, not all 100% [KB: checklist.md → Typography/Opacity].
- **Star of the show** — one element on the landing page anchors the eye long enough to convert attention [KB: checklist.md → Star].
- **Felt hover states** — interactive elements respond with motion/shadow/colour shift, not just cursor change [KB: checklist.md → Hover].
- **Three-level type scale** — anchor headline dramatically larger than supporting copy [KB: checklist.md → Typography].
- **No generic AI patterns** — no gradient blobs, frosted glass, default Inter, stock "Trusted by" rows [KB: applying-to-skills.md].

---

## Code Review Placement

Code reviews happen WITHIN phases, but they are NOT the quality gate:

```
Coder completes → Code Review → Fix issues → THEN → Quality Check (visual)
```

Code review = reading code for bugs, security, best practices
Quality check = LOOKING at the site in a browser

**Both are required. Code review alone is NOT sufficient for UI work.**

---

## Quality Check Agent Instructions

When spawning a quality-check agent, remind it:

```
You are checking if this site is ready to ship.

REMEMBER:
- Default to FAIL, not pass
- You're a harsh client who paid £10k
- List EVERY issue, not just a few
- Compare to professional sites (Apple, Stripe, Linear)
- If ANY doubt, verdict is NOT READY

CONTENT VERIFICATION (MANDATORY):
- Read /spec/content-requirements.md to know minimum word counts
- Check AT LEAST 3 pages for actual word count vs. required
- Flag ANY placeholder text (Lorem ipsum, TODO, [INSERT], etc.)
- Verify meta titles are unique and descriptive (not "Page Title | Site Name" defaults)
- Check that content mentions the business name and is locally relevant
- Verify H1s exist and are unique per page

CONTENT FAILURES = AUTOMATIC NOT READY:
- Placeholder text anywhere = NOT READY
- Word count below spec = NOT READY
- Duplicate content across pages = NOT READY
- Generic content without local relevance = NOT READY

DESIGN VERIFICATION (MANDATORY):
- Hero section: Is it concise (headline + subheadline + CTA) or a wall of text? Wall of text = CRITICAL FAIL
- Typography: Is there clear visual hierarchy? (H1 dramatically larger than body, H2 distinct from H3)
- Layout variety: Does the page alternate between different section layouts, or is it the same pattern repeated?
- Spacing: Is there generous whitespace between sections, or does everything feel cramped?
- Visual rhythm: Do section backgrounds vary (alternating light/dark/tinted), or is every section identical?
- Content presentation: Are services/features shown as cards/grids, or as plain text paragraphs?
- Compare to Stripe.com or Linear.app — does the typography, spacing, and layout feel similarly intentional?

DESIGN FAILURES = AUTOMATIC NOT READY:
- Hero section with 3+ sentences of body text = NOT READY
- No visible typography hierarchy (headings barely distinguishable from body) = NOT READY
- Same section layout repeated 4+ times on one page = NOT READY
- All sections have identical white backgrounds with no variation = NOT READY
- Services/features presented as plain paragraph text (no cards, grids, or icons) = NOT READY

DESIGN CONCEPT ADHERENCE CHECK (MANDATORY):
- Read /spec/design-concept.md before starting the quality check
- Does the hero use the specific layout pattern defined in design-concept.md? If not = NOT READY
- Are the fonts from design-concept.md actually implemented? (Check rendered fonts, not just CSS) If not = NOT READY
- Does the color palette match design-concept.md? If not = NOT READY
- Do section layouts follow the patterns specified in design-concept.md? If not = NOT READY
- Does the site deliver on "The Memorable Thing" from the design concept? If not = NOT READY
- Could you swap the logo and this would look like any other business website? = NOT READY

ANTI-SLOP DESIGN CHECK (generic AI defaults):
- Does the layout follow the generic SaaS stack (hero -> proof strip -> features -> pricing -> testimonials -> CTA)? = NOT READY
- Are there radial glows, blurred orbs, or gradient haze behind the hero? = NOT READY
- Are there frosted glass cards or translucent panels as default polish? = NOT READY
- Is the heading font Inter, Roboto, or Arial without explicit brief justification? = NOT READY
- Are there stock copy patterns: "Trusted by...", "Built for...", "Everything you need", "Ready to...?", "Get Started"? = NOT READY
- Are testimonials shown as 5-star + quote + avatar chip default pattern? = NOT READY
- Does it look like every other AI-generated website? = NOT READY

ANTI-SLOP CONTENT CHECK (from `no-ai-slop`):
- Does content start with "In today's [adjective] landscape/world"? = NOT READY
- Does content use "Let's dive in", "Here's the thing", "At its core", "At the end of the day"? = NOT READY
- Does content use "seamless", "robust", "leverage", "ecosystem", "holistic", "delve"? = NOT READY
- Does content end with "Final thoughts" or "Key takeaways"? = NOT READY
- Does content use breathless enthusiasm ("fascinating", "game-changing", "transformative")? = NOT READY
- Does content feel like generic AI writing rather than a specific human voice? = NOT READY

The Three Questions:
1. Does this look like £10k+ agency work? [YES/NO]
2. Would a business owner be proud? [YES/NO]
3. Does this compete with the best? [YES/NO]

If ANY answer is NO, verdict is NOT READY or NEEDS WORK.
```

---

## Red Flags That Require Immediate Quality Check

If a coder mentions ANY of these, spawn quality-check immediately:
- "animation" / "opacity" / "transition" / "fadeIn"
- "should work" (without verification)
- Any console error, even "minor"
- "done" without mentioning screenshots
- Coder creates hero with more than 2 sentences of body text
- All sections on a page use the same background color
- Services listed as paragraphs instead of cards/grid
- Coder uses Inter font, gradient blobs, frosted glass cards, or "Trusted by" copy (generic AI defaults)
- Layout follows generic hero -> proof strip -> features -> pricing -> testimonials -> CTA stack
- CTA text is "Get Started", "Book a Demo", or "Start Free Trial" (stock AI copy)
- Coder ignores /spec/design-concept.md and uses different fonts, colors, or layouts than specified
- Site looks interchangeable with any other business site (fails the "swap the logo" test)

---

## Content Red Flags (STOP and FIX immediately)

If you see ANY of these, STOP the build and fix content first:
- "Lorem ipsum" or placeholder text anywhere
- "TODO", "FIXME", "[INSERT]", "[PLACEHOLDER]" in content
- Coder saying "I'll add content later"
- Pages with less than 300 words (unless specifically designed as minimal)
- Service/location pages with less than 800 words (check against spec)
- Repeated content across multiple pages (duplicate content)
- Generic content that doesn't mention the business name or location
- Meta descriptions that are defaults or identical across pages
- Missing H1 or multiple H1s on a page
- Content that doesn't match the keyword mapping

**Content shortcuts are NOT acceptable. Fix them before proceeding.**

---

## Completion Criteria

**You may ONLY output `<promise>BUILD COMPLETE</promise>` when:**
1. `/spec/brief.md` was either provided by user or generated from Phase 0 interview
2. Phase 1 research completed (content-requirements.md + keyword-mapping.md)
3. Phase 2 content + images completed in parallel (all content files + image manifest)
4. All coding phases completed (Phases 3-8)
5. All quality gates passed
6. Final quality-check returned "READY TO SHIP"
7. Production build works
8. All three viewports tested
9. No Critical issues remain
10. **Content requirements met:**
    - `/spec/content-requirements.md` exists with word count specs
    - `/spec/keyword-mapping.md` exists with keywords per page
    - All content files exist in `/spec/content/`
    - No placeholder text on any page
    - Word counts verified against spec
11. **Image requirements met:**
    - `/spec/image-manifest.md` exists listing all images
    - Hero images exist for homepage and key pages
    - Images are professional quality (no obvious AI artifacts)
    - Alt text defined for all images

**If any gate fails, fix issues autonomously by spawning the appropriate agents, re-run the gate, and continue. Do not ask the user for help unless stuck after 3 attempts on the same gate.**

---

## Anti-Sycophancy Reminder

The quality-check agent may try to be "helpful" by approving mediocre work.

If a quality check comes back positive but you have doubts:
1. Ask for a more critical re-evaluation
2. Request specific comparison to professional sites
3. Ask "Would a client paying £10k be satisfied?"

**Do not trust rubber-stamp approvals. Challenge them if needed.**
