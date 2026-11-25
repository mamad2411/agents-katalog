---
name: copy-review
description: "Line-edit for readability, accessibility, and SEO without touching facts. This is your technical publishing QA before editorial review—catch typographical errors, rhythm problems, ad placement conflicts, and metadata gaps that confuse search engines."
---

# Copy Review Skill

## Overview

Copy review is **technical publishing QA**, not editorial judgment or fact verification. This skill focuses on:

- **Readability** for your target audience (parameterized, not assumed)
- **Typographical correctness** (grammar, spelling, consistency)
- **Accessibility compliance** (alt text, heading hierarchy, color contrast assumptions)
- **SEO metadata integrity** (title tags, meta descriptions, structured data)
- **Ad placement safety** (no conflicts with inline ad slots, no ad-adjacent content problems)
- **Style consistency** enforcement (house style, voice, terminology)

**This skill does NOT:**
- Alter facts or sourcing
- Dispute editorial choices or story angles
- Change article tone or angle
- Verify claims (that's `final-editor-review`)

---

## Readability Optimization

### Target Audience Parameterization

Before copy review, establish your audience profile:

| Audience Factor | Example Values | Impact on Review |
|---|---|---|
| **Reading Level** | High school (8.0), College (12.0+), Professional jargon-heavy | Flesch-Kincaid score targets; vocabulary simplification; jargon explanations |
| **Time Budget** | 2 min (news brief), 8 min (investigative), 30 min (whitepaper) | Paragraph length, sentence density, scannable structure |
| **Domain Knowledge** | Lay audience, Domain experts, Mixed | Define technical terms in context; assume no prior knowledge or assume deep knowledge |
| **Device** | Mobile-first, Desktop, Print | Sentence length (shorter = mobile-friendly); heading density; link density |
| **Language** | English (native), English (second language), Bilingual | Passive voice reduction; Latinate word replacement; sentence length |

**Red Flag:** Copy review proceeding without audience parameters = uneven readability standards.

### Readability Checklist

- [ ] **Sentence length:** Median 15–20 words. Max 40 words (except intentional emphasis).
- [ ] **Paragraph length:** 2–4 sentences max for web. Longer in longform, but break at idea boundaries.
- [ ] **Passive voice:** <10% of sentences. Flag all instances; keep only when actor is unknown or irrelevant.
- [ ] **Jargon:** Every technical term defined in context on first mention. No acronyms without expansion (first use: "Federal Bureau of Investigation (FBI)").
- [ ] **Verbs:** Active, present-tense preferred. Weak verbs ("was"), intensifiers ("very"), hedges ("somewhat") flagged and rewritten.
- [ ] **Transitions:** Logical flow between paragraphs. No abrupt jumps. Signpost phrases present where needed.
- [ ] **Subheading hierarchy:** H1 > H2 > H3. No skipping levels. Alt text present on all images.

---

## Ad Placement Validation

### Generic Ad Pattern Safety

Most publishers use one of these patterns:

| Pattern | Description | Copy Review Focus |
|---|---|---|
| **Top-of-page ad (leaderboard)** | 728×90 or 970×250, pre-headline | No image captions or critical content in top 250px; headline spacing clean |
| **In-article ads (mid-roll)** | 300×250 or 336×280 sidebar/inline | No tombstoning (two ads touching); text wrapping correct; no ad labels bleeding into article text |
| **Native ads (sponsored content)** | Clearly labeled "Sponsored" or "Partner Content"; same grid system as articles | Review sponsor disclosure is visible, not buried; sponsor links don't masquerade as story links |
| **Sticky footer (mobile)** | Persistent footer ad on mobile | No footer ad text overlapping article body text; sufficient margin below content |
| **Sidebar ads (desktop)** | Vertical 160×600 or 300×600 | Article content doesn't narrow to <500px; ad containers have breathing room |

**Critical Safety Rules:**
- No article text directly adjacent to sponsored content without visual separation.
- No mention of advertiser in body copy without disclosure ("Partner post" at top).
- No affiliate links disguised as citations.

### Checklist

- [ ] Ad placement zones match expected container sizes (no content crowding).
- [ ] Tombstoning (two ad blocks touching) avoided.
- [ ] Sponsored/native ads clearly labeled above-the-fold.
- [ ] No content reflow issues on mobile (sticky footer doesn't crush text).
- [ ] Image captions don't overlap ad zones.
- [ ] CTAs in article don't visually mimic ad CTAs (color, button style).

---

## SEO Metadata Verification

### Required Metadata Elements

| Field | Character Limit | Requirement | Example |
|---|---|---|---|
| **Meta Title** | 50–60 chars | Unique per article; keyword + brand optional; no clickbait | "How Pesticide Runoff Pollutes County Water: 2025 Investigation" |
| **Meta Description** | 155–160 chars | Compelling summary; no keyword stuffing; includes hook | "Investigative report reveals how agricultural chemicals contaminate drinking water. Read our analysis of state testing failures." |
| **H1 (Article Headline)** | — | One per page; matches or closely mirrors meta title | (same as title, usually) |
| **Image Alt Text** | <125 chars | Describe what's in image; don't repeat caption; include relevant keywords naturally | Alt: "Water sample from Miller County aquifer glowing under UV light, showing fluorescent chemical residue" |
| **Open Graph (og:title, og:description, og:image)** | — | Mirror meta title/description; 1200×630px image; JPG/PNG | og:image should be unique per article (not site-wide placeholder) |
| **Structured Data (JSON-LD, NewsArticle)** | — | Include author, datePublished, dateModified, headline, image, description | Required for news index eligibility |

### Checklist

- [ ] Meta title: 50–60 chars, includes primary keyword, no clickbait.
- [ ] Meta description: 155–160 chars, compelling hook, no keyword stuffing.
- [ ] H1 tag present and unique on page.
- [ ] All images: alt text present, <125 chars, descriptive not repetitive.
- [ ] Open Graph tags populated (og:title, og:description, og:image).
- [ ] og:image is unique per article, 1200×630px, JPG or PNG.
- [ ] Structured data (NewsArticle schema) present and valid JSON.
- [ ] No duplicate meta titles across site (check against published articles).

---

## Accessibility Checks

### WCAG 2.1 AA (Minimum Standard)

| Element | Requirement | How to Verify |
|---|---|---|
| **Color Contrast** | 4.5:1 (text), 3:1 (graphics) | Use WebAIM contrast checker; assume no user color-blindness mode |
| **Heading Hierarchy** | H1 → H2 → H3 (no skips); one H1 per page | Outline test: press Tab, verify logical reading order |
| **Links** | Descriptive text, not "click here"; sufficient size (24×24px); underlined or high contrast | "Read the investigation" not "click here" |
| **Images** | Alt text present (or decorative: alt=""); captions for charts/graphs | Every image has alt attribute; charts have long descriptions |
| **Video** | Captions (live speech), transcript (background audio) | Assume deaf user; assume no audio |
| **Forms** | Labels associated with inputs (for/id attributes); error messages clear | No placeholder-only labels |
| **Mobile** | Touch targets 24×24px; zoom to 200% doesn't break layout | Test on real device, not just browser zoom |

### Checklist

- [ ] No color used as only means of conveying information (e.g., "red text = error").
- [ ] Heading hierarchy: H1 (single), H2s, H3s; no skips.
- [ ] Alt text on all images; captions on charts/graphs/infographics.
- [ ] Links descriptive ("Read investigation" vs. "Click here"); not underlined link pseudo-text.
- [ ] Video captions present; transcripts provided.
- [ ] 200% zoom: no text cutoff, no horizontal scroll introduced.
- [ ] Assume reader uses screen reader: link text makes sense out of context.

---

## Style Consistency Enforcement

### House Style Template

Create a **style reference** for your publication (update once, reuse always):

| Category | Rule | Example/Counterexample |
|---|---|---|
| **Numbers** | Spell out zero–nine; numerals 10+; exceptions: addresses, percentages, dollar amounts | "Five people" vs. "25 people"; "$5.2M" not "five point two million" |
| **Dates** | Month DD, YYYY or DD Month YYYY (not MM/DD/YY) | "March 15, 2025" not "3/15/25" |
| **Time** | 12-hour with a.m./p.m., not 24-hour | "3:30 p.m." not "15:30" |
| **Oxford Comma** | Use in lists | "Red, white, and blue" not "red, white and blue" |
| **Quotes** | Double quotes; single quotes inside; attribution after period | "He said, 'Hello.'" not 'He said "Hello."' |
| **Acronyms** | Expand on first use | "Federal Bureau of Investigation (FBI)" then "FBI" thereafter |
| **Emphasis** | Italics for publication titles, vessels; bold for headers only | *New York Times* vs. **New York Times** |
| **Contractions** | Use or avoid consistently (decide once per publication) | "don't" or "do not" — pick one, apply everywhere |
| **Titles Before Names** | "Mayor Jane Smith" or "Jane Smith, mayor"? | Decide; apply consistently |
| **State/Country Abbreviations** | Two-letter postal codes (AP style) or spell out? | "TX" vs. "Texas" — decide |

**Red Flag:** Inconsistent application of style rules (some articles spell out numbers, others don't).

### Checklist

- [ ] Numbers 0–9 spelled out; 10+ numerals (except special cases: addresses, percentages, dollars).
- [ ] Dates: Month DD, YYYY format.
- [ ] Times: 12-hour with a.m./p.m.
- [ ] Acronyms expanded on first mention.
- [ ] Quotes: double quotes with single inside; attribution after period.
- [ ] Emphasis: italics for titles/vessels; bold for headers only.
- [ ] Titles/names: consistent format across article.
- [ ] Contractions: consistent within publication.

---

## Implementation Workflow

### Step-by-Step Copy Review Process

1. **Establish Parameters** (5 min)
   - Target audience reading level
   - Expected time to read
   - Device priority (mobile-first or desktop)
   - House style reference (or inherit from publication defaults)

2. **Readability Pass** (10–15 min)
   - Read article aloud (catch rhythm/flow problems).
   - Sentence length: mark anything >40 words.
   - Paragraph length: flag anything >4 sentences.
   - Jargon/acronyms: circle unexpanded terms.
   - Passive voice: underline instances.
   - Use Flesch-Kincaid calculator (target score: 50–60 for general audience).

3. **Accessibility Audit** (10 min)
   - Run WAVE or Axe DevTools (browser extension).
   - Check all images for alt text.
   - Verify heading hierarchy (H1→H2→H3, no skips).
   - Test 200% zoom; check mobile tap targets.
   - (If video present: captions verified? Transcript available?)

4. **SEO Metadata Check** (5 min)
   - Meta title: 50–60 chars? Keyword present? Unique?
   - Meta description: 155–160 chars? Hook compelling?
   - og:image: 1200×630px? Unique to article?
   - H1: present, unique on page?
   - JSON-LD structure: valid? (Test with Google Structured Data Tester)

5. **Ad Placement Safety** (5 min)
   - Mock layout: where will ads render?
   - No text overlap? No tombstoning?
   - Native/sponsored clearly labeled?
   - Sufficient spacing around ad zones?

6. **Style Consistency Pass** (10 min)
   - Spot-check against house style guide.
   - Numbers: spell-out vs. numeral consistency.
   - Dates/times: format consistency.
   - Acronyms: all expanded on first mention?
   - Emphasis: italics vs. bold usage consistent?

7. **Final Read** (5 min)
   - Read opening + closing paragraphs aloud.
   - Scan subheadings; do they summarize sections?
   - Click all links; confirm they work and go to intended destination.
   - Check for widow/orphan words (single word on its own line).

8. **Sign-Off**
   - Document findings: list of edits, explanations.
   - Mark as "Ready for Final Editor Review" (NOT "Ready to Publish").
   - If major changes needed: request author rewrite; re-run accessibility check.

---

## Common Mistakes & Red Flags

### Readability Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| Entire paragraph is one sentence (>50 words) | Reader loses thread; accessibility burden (screen reader pause required) | Break into 2–3 sentences at natural pause points |
| All paragraphs 1 sentence | Feels choppy; no rhythm | Vary: some single, some 2–3 sentences |
| Passive voice everywhere ("The report was issued by the agency.") | Buried actors; weaker voice; harder to parse | Rewrite active: "The agency issued the report." |
| Acronym used without first expansion ("The EPA warned...") | New reader lost; accessibility failure (screen readers spell out "EPA") | First use: "Environmental Protection Agency (EPA) warned..." |
| "Very," "really," "quite," "somewhat" | Weak intensifiers; editorial bias | Delete or replace: "really good" → "increased by 40%" (fact, not opinion) |
| Heading caps: "Flood Waters Rise In Three Counties" | Harder to scan; unclear emphasis | Use sentence case: "Flood waters rise in three counties" |

### Accessibility Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| Red text (no underline) for links on blue background | Color-blind readers can't distinguish; fails 4.5:1 contrast | Underline all links; confirm 4.5:1 contrast ratio |
| Heading hierarchy: H1 → H3 (skips H2) | Screen reader users can't navigate by skipped levels | Follow strict H1 → H2 → H3 hierarchy |
| Alt text is caption or redundant ("Image: Flooded street") | Screen reader repeats caption; wasted alt space | Write unique alt: "Main Street submerged under 4 feet of water, Sept 2025" |
| Decorative image with alt text ("Decorative line separator") | Screen readers read unnecessary text; auditory clutter | Use alt="" (empty) for purely decorative images |
| Video captions auto-generated (unchecked) | Auto-captions often wrong ("river" → "reever"); fail accessibility | Manually review captions; sync timing |

### SEO Metadata Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| Meta title = article headline (always) | No brand recognition; missed keyword opportunities | Meta title can be slight variation: headline vs. title |
| Meta description copied from first paragraph (no hook) | No reason to click; low CTR | Write benefit-driven summary: "Investigative analysis reveals..." not "The report shows..." |
| og:image is site-wide placeholder | Social shares don't show article-specific image | Generate unique social card per article |
| H1 ≠ meta title | Search engines confused about primary topic | Align H1 and meta title; allow minor variation for readability |
| Keyword stuffed in title ("Water Pollution Investigation Water Pollution Report Water") | Google penalizes keyword stuffing; unreadable | Use keyword once naturally: "Water Pollution Investigation: County Failed Safety Standards" |
| Structured data missing or invalid JSON | News articles not eligible for Google News index | Test with Google Structured Data Tester; include author, datePublished, headline, image |

### Ad Placement Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| Article text flows directly into sidebar ad (no margin) | Visual confusion; readers click ad by accident (high bounce rate) | Add 20–30px margin; visual border/background color difference |
| Two ad blocks side-by-side with no gap (tombstoning) | Reads as single mega-ad; low CTR; looks cheap | Ensure grid system prevents adjacent ad slots |
| Sponsored content not labeled "Sponsored" (or buried) | FTC violation; reader deception; destroys trust | Label above-the-fold in 14+ pt font, contrasting color |
| Sticky footer ad covers article body on mobile | Unreadable; high bounce; low engagement | Test on real mobile device; ensure sufficient bottom margin |
| Affiliate links disguised as citations ("Click here for more info [affiliate link]") | Deceptive; undermines credibility; potential legal exposure | Disclose affiliate status upfront; use [Affiliate Link] label if policy requires |

---

## Boundary: What Copy Review Does NOT Cover

- **Fact-checking** (belongs to `final-editor-review`)
- **Tone/angle disputes** (editorial decision; assign to editor if concern)
- **Structural changes** (if article needs reordering, request author rewrite)
- **Sourcing critique** (belongs to `final-editor-review`)
- **Headline rewrite** (that's the editor's domain; copy review validates existing headline)

---

## Escalation

If copy review uncovers **factual inconsistencies** (dates, titles, quotes), do NOT fix them:

1. Flag for `final-editor-review` with note: "Copy review found potential factual discrepancy: (specific example)"
2. Do not proceed with publication until editorial confirms.

---

## Checklist for Publication

Before marking "Ready for Final Editor Review":

- [ ] Readability: target audience parameters met (Flesch-Kincaid score in range).
- [ ] Accessibility: WCAG 2.1 AA audit passed (zero contrast failures, heading hierarchy clean).
- [ ] SEO metadata: title, description, og:image, H1, structured data all present and valid.
- [ ] Ad placement: no text overlap, spacing adequate, native ads labeled.
- [ ] Style consistency: numbers, dates, acronyms, emphasis uniform.
- [ ] All links working; no broken URLs.
- [ ] No spelling/grammar errors.
- [ ] Sign-off document attached with detailed notes.
