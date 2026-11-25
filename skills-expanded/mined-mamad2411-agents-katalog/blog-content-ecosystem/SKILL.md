---
name: blog-content-ecosystem
description: Transform a completed blog post into a complete content marketing ecosystem including lead magnets, bibliographies with abstracts, and LinkedIn posts with CTAs. Use when user requests to create supporting content assets for a blog post, build a content campaign, create lead magnets from articles, or needs LinkedIn promotion for published content.
---

# Blog Content Ecosystem

## Overview

Transform a single blog post into a complete top-of-funnel (TOF) content marketing system. Generate lead magnets, bibliographies with abstracts, and multi-variant LinkedIn promotional posts—all optimized for audience engagement and lead capture.

**Provenance gate.** Before publishing, route every statistic and factual claim through citation verification (the research-pipeline citation-verifier or an equivalent source-and-date check). No unverified claim ships; flag what can't be verified rather than printing it.

## Workflow

This skill follows a sequential 5-step process:

1. **Analyze Blog Post** - Extract key insights, structure, and citations
2. **Create Lead Magnet** - Generate downloadable checklist, guide, or framework
3. **Generate Bibliography** - Create BibTeX entries with abstracts from sources
4. **Craft LinkedIn Posts** - Write 3 promotional post variants with CTAs
5. **Create Multimedia Assets** - Generate video/audio prompts for NotebookLM and infographic design specs

## Step 1: Analyze Blog Post

**Inputs:**
- Blog post content (markdown, text, or URL)
- Target audience information
- Blog topic/theme

**Actions:**
- Extract main themes, key statistics, and actionable insights
- Identify quotable content and data points
- Note any sources or citations that need bibliography entries
- Determine content depth (strategic/tactical, technical/accessible)

**Outputs:**
- Content analysis summary
- Key themes and hooks for promotion
- List of sources requiring bibliography entries

## Step 2: Create Lead Magnet

**Objective:** Create a high-value, immediately actionable download that extends blog insights.

**Format Options:**
- Checklist (90-day implementation roadmap, audit checklist)
- Quick reference guide (top 10 lists, comparison matrices)
- Framework document (decision trees, workflow diagrams)
- Resource compilation (tool lists, template collections)

**Lead Magnet Structure:**
```markdown
# [Compelling Title with Benefit]
## [Subtitle: Specific Outcome or Use Case]

[Brief intro paragraph - 2-3 sentences explaining value]

---

## [Section 1: Actionable Content]
- [ ] Specific action item with context
- [ ] Specific action item with context

## [Section 2: Organized by Phase/Category]
[Content structured for scanability]

## [Reference Section: Quick lookups]
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data | Data | Data |

## Red Flags / Common Mistakes
- Warning signs to watch for
- Mistakes to avoid

---

## About This [Asset Type]
[Brief attribution paragraph with source reference]

*Last Updated: [Date] | Based on [Blog Post Title]*
```

**Key Principles:**
- **Scannable** - Use checkboxes, tables, bullet points
- **Actionable** - Every item should be a concrete next step
- **Comprehensive** - Cover 80% of common use cases
- **Professional** - Clean formatting, clear hierarchy
- **Branded** - Include attribution to source blog/author

**See:** `references/lead-magnet-examples.md` for complete examples

## Step 3: Generate Bibliography with Abstracts

**Objective:** Create a properly formatted BibTeX bibliography where each entry includes a substantive abstract summarizing the source's contribution.

**Process:**

### 3a. Extract Citation Information

From the blog post, identify all sources:
- Direct quotes with URLs
- Referenced statistics or data
- Frameworks or methodologies mentioned
- Industry reports or studies cited

### 3b. Fetch Source Content

For each source with a URL:
- Use web_search or web_fetch to retrieve content
- Extract key information: title, author/organization, publication date, URL/DOI
- Read enough to understand the source's main contribution

### 3c. Write Abstracts

**Abstract Quality Standards:**
- **Length:** 2-4 sentences (50-150 words)
- **Content:** Summarize the source's main argument, findings, or contribution
- **Specificity:** Include specific data points, methodologies, or claims when relevant
- **Relevance:** Explain why this source matters to the blog topic
- **Neutrality:** Objective summary, not evaluation

**Good Abstract Example:**
```
abstract = {Analysis of CMMC compliance costs and automation strategies 
for Defense Industrial Base contractors. Examines how STIG automation 
through ConfigOS reduces implementation time from months to hours, 
addresses the challenge of quarterly STIG updates (every 90 days), and 
provides cost estimates ranging from $2,999.56 for Level 1 to $51,095.60 
for Level 2+ compliance with $41,666 in recurring engineering costs.}
```

**Poor Abstract Example:**
```
abstract = {This article discusses CMMC and automation.}
```

### 3d. Format BibTeX Entries

**Entry Template:**
```bibtex
@misc{citationkey2025,
  author = {{Organization Name}},
  title = {Full Article Title},
  year = {2025},
  month = {January},
  url = {https://example.com/article},
  note = {Accessed January 2026},
  abstract = {2-4 sentence summary of the source's contribution, 
  including specific data points, findings, or arguments that make 
  this source valuable. Explains relevance to the topic.}
}
```

**Citation Key Format:** `authorlastname` or `organization` + `year` + optional descriptor
- Examples: `steelcloud2025cmmc`, `nist800171`, `mack2026stig`

**Entry Types:**
- `@misc` - Blog posts, web articles, company pages
- `@techreport` - Government reports, technical documents
- `@article` - Journal articles (include journal, volume, pages if available)

**Output:** Save as `[topic]_bibliography_with_abstracts.bib`

## Step 4: Craft LinkedIn Posts

**Objective:** Create 3 distinct post variants targeting different engagement styles, all driving traffic to the blog with clear CTAs.

**Three Variants:**

### Variant 1: Direct/Urgent Tone
- **Hook:** Recent event, deadline, or breaking development
- **Length:** 1,300-1,500 characters
- **Structure:** 
  - Urgent opening (3 months ago X, today Y)
  - Brutal reality (3-5 data points with →)
  - Competitive advantage angle
  - Strong CTA with reason to act now

### Variant 2: Insight/Strategy Tone
- **Hook:** Contrarian insight or hidden pattern
- **Length:** 1,300-1,500 characters
- **Structure:**
  - Pattern observation opening
  - Strategic framework explanation
  - Concrete example comparison (❌ weak vs ✅ strong)
  - CTA with strategic benefit

### Variant 3: Personal/Narrative Tone
- **Hook:** Personal experience or observation
- **Length:** 1,300-1,500 characters
- **Structure:**
  - Personal credibility opening
  - Specific inflection point or change
  - "And here's what almost everyone is missing"
  - CTA with personal endorsement

**Universal Requirements:**
- **Formatting:** Use line breaks, bullets (→), bold sparingly
- **CTAs:** Always include both blog link and lead magnet download link
- **Hashtags:** 4-6 relevant hashtags at end
- **Value-first:** 80% value, 20% promotion
- **Authentic voice:** Match the author's style and expertise

**CTA Format:**
```
📊 **In this week's analysis on [Blog Name], I examine:**
• Key point 1
• Key point 2  
• Key point 3

**👉 Read the full analysis:** [BLOG LINK]

**📥 Download our free [Asset Name]:** [LEAD MAGNET LINK]

#Hashtag1 #Hashtag2 #Hashtag3
```

**See:** `references/linkedin-post-examples.md` for complete templates

## Step 5: Create Multimedia Assets

**Objective:** Generate NotebookLM prompts for video/audio content and design specifications for infographic, all optimized for the target audience.

### Target Audience (STIGViewer ICP)

**Primary Personas:**
- Compliance professionals tracking quarterly STIG updates
- Defense contractors (DIB) requiring CMMC certification
- System administrators implementing STIGs on infrastructure
- CISOs/security leaders managing strategic compliance
- IT security teams handling day-to-day STIG deployments

**Audience Characteristics:**
- **Technical sophistication:** HIGH - expect technical depth, not marketing fluff
- **Weekly engagement:** 35,000+ regular visitors
- **Content consumption:** Practical, actionable, data-driven focus
- **Pain points:** Quarterly update tracking, multi-STIG management, audit preparation
- **Time sensitivity:** Updates and deadlines matter significantly

### 5a. Video Content (5-10 Minutes)

**Format:** NotebookLM AI-generated video discussion

**Objective:** Create an engaging conversation between two cybersecurity compliance experts that drives interest in both the blog post and lead magnet.

**Pronunciation Guide (CRITICAL):**
- **STIG** = "stig" (rhymes with "pig")
- **DISA** = "dissah" (DISS-ah, not DEE-sah)
- **CMMC** = "C-M-M-C" (spell out each letter)

**Three-Act Structure:**

**Act 1: The Wake-Up Call (0-3 min)**
- Open with the enforcement date or inflection point
- "Why didn't we see this coming when [X] has been around for [Y] years?"
- Reveal the hidden dependency/connection
- Set up the "brutal reality" with 2-3 data points

**Act 2: The Technical Reality (3-7 min)**
- Deep dive on the core technical challenge
- Walk through the math that makes manual approaches untenable
- Discuss cost-benefit with specific numbers
- Explain the strategic concept (compliance multiplier, etc.)
- Include a debate moment where hosts push back on assumptions

**Act 3: The Strategic Play (7-10 min)**
- Timeline urgency with specific dates
- Who wins/loses in this environment
- Competitive advantage reframing
- Practical next steps (mention the checklist)
- Closing insight that reframes the challenge as opportunity

**Discussion Angle Guidance:**

*Primary Focus (60% of time):*
- The "hidden in plain sight" revelation - why this connection wasn't obvious before
- The automation imperative - math that proves manual is dead
- Timeline urgency - specific dates and preparation windows

*Secondary Focus (30% of time):*
- Strategic implications - who benefits, market consolidation effects
- The multiplier effect - how one investment satisfies multiple requirements
- Real cost analysis - move beyond estimates to actual ROI calculations

*Engagement Moments (10% of time):*
- Debate point where hosts disagree, then resolve
- "Let's do the math together" moment
- Analogies that make technical concepts accessible
- Recognition beats ("Oh, that's why audits have been painful")

**Emotional Arc:**
- Minute 0-2: Recognition/Validation ("This explains so much")
- Minute 3-5: Overwhelm ("This seems impossible manually")
- Minute 5-7: Hope ("But automation makes it feasible")
- Minute 7-9: Urgency ("We need to start now")
- Minute 9-10: Empowerment ("Here's the exact roadmap")

**Key Quotes to Reference:**
[Include 3-5 most impactful quotes from blog post]

**Closing CTA:**
- Mention the 90-day implementation checklist
- Direct to blog for full analysis
- Position as immediate actionable resource

**See:** `references/multimedia-asset-guide.md` for complete video prompt templates

### 5b. Audio Content (1.5 Minutes)

**Format:** NotebookLM AI-generated audio-only discussion

**Objective:** Create a concise, high-impact summary perfect for commutes or quick consumption.

**Pronunciation Guide:** Same as video (STIG = "stig", DISA = "dissah")

**Ultra-Condensed Structure:**

**Opening (0-15 sec):**
- Hook: The single most important development or data point
- Example: "On November 10, 2025, the DoD made CMMC 2.0 mandatory for 338,000 defense contractors. Most are discovering the secret to passing audits too late."

**Core Insight (15-60 sec):**
- The one thing listeners must understand
- The brutal reality in 2-3 bullet points with data
- Why this matters RIGHT NOW

**Action (60-75 sec):**
- What listeners should do immediately
- Mention the lead magnet as the starting point
- Create FOMO without being salesy

**Closing (75-90 sec):**
- Single memorable quote or reframe
- Direct to blog for full details
- End with urgency

**Tone:** Direct, data-driven, no filler. Every sentence must earn its place.

**Key Principle:** Audio-only listeners can't reference visuals, so use verbal signposting:
- "Here's the critical stat..."
- "Three things matter..."
- "The timeline looks like this..."

### 5c. Infographic Design

**Objective:** Create a visually striking, data-rich infographic using MoxyWolf branding that can stand alone as social media content.

**MoxyWolf Color Palette:**

**Vibrant Colors (Energy, Movement, Insight):**
- **Fire Orange** (#FF6B35) - PRIMARY ACCENT, use for emphasis and CTAs
- **Electric Blue** (#00B4D8) - Strategic clarity, frameworks, data
- **Vivid Magenta** (#E63946) - Urgency, critical warnings
- **Solar Gold** (#FFD23F) - Positive outcomes, success metrics
- **Pulse Teal** (#06FFA5) - Innovation, forward momentum

**Structural Colors (Grounding, Framework, Precision):**
- **Obsidian Black** (#1A1A1A) - Text, structure, depth
- **Deep Purple** (#5A1F84) - Secondary headers, depth
- **Steel Gray** (#5D5D5D) - Supporting text, dividers

**Color Usage Rules:**
- Fire Orange for main headline and key CTAs
- Electric Blue for framework diagrams and data visualization
- Vivid Magenta for warnings, deadlines, critical stats
- Use structural colors (black, purple, gray) for text and grounding
- Balance vibrant with structural to embody "wild intelligence through structured recursion"

**Typography:**
- **Headlines:** Aeonik Bold (fallback: Inter Bold, Helvetica Neue Bold)
- **Body Text:** Aeonik Regular (fallback: Inter, Helvetica Neue)
- **Data/Stats:** Aeonik Bold or Mono for emphasis
- Maintain generous spacing - let typography breathe

**Infographic Structure Options:**

**Option 1: Timeline Infographic**
- Horizontal timeline showing key dates and milestones
- Use Vivid Magenta for critical deadlines
- Include "You Are Here" marker in current date
- Show what happens at each phase
- Bottom CTA to download checklist

**Option 2: Data Visualization**
- Central statistic in massive type (Fire Orange)
- Supporting data points radiating outward (Electric Blue)
- Comparison bars or pie charts
- "Before vs. After automation" visual
- Include source citations in small type

**Option 3: Process Flow**
- Step-by-step visual of the compliance journey
- Use numbered circles with Electric Blue
- Arrows showing progression
- Warning callouts in Vivid Magenta for common mistakes
- Success outcome in Solar Gold

**Option 4: Comparison Matrix**
- "Manual vs. Automated" two-column layout
- Icons or symbols for each comparison point
- Clear winner highlighted with Fire Orange
- Cost/time/risk comparisons
- Bottom stat showing ROI

**Required Elements:**
- **Headline:** Bold, Fire Orange, captures main insight (10 words max)
- **Subheadline:** Elaborates on headline context (15 words max)
- **Key Statistics:** 3-5 data points in large, bold type
- **Visual Hierarchy:** Largest to smallest guides eye flow
- **MoxyWolf Logo:** Small, in corner, maintains brand presence
- **Source Attribution:** "Based on [blog title] | STIGViewer.com" in small type
- **CTA:** "Download the full 90-day implementation guide" with QR code or URL
- **Negative Space:** Generous breathing room, not cluttered

**Design Principles:**
- **Structure is Sacred:** Use clear grid system, evident hierarchy
- **Recursion Reveals Depth:** Layer information thoughtfully, build complexity through iteration
- **Porosity is Power:** Use negative space generously, create contrast
- **Clarity is Grace:** Simple layouts with high contrast, every element has purpose

**Dimensions:**
- **Social Media:** 1080×1080px (Instagram/LinkedIn square)
- **Blog Featured Image:** 1200×630px (horizontal)
- **Pinterest:** 1000×1500px (vertical)
- **Print-Ready:** Create at 300dpi if offering PDF download

**See:** `references/multimedia-asset-guide.md` for infographic templates and examples

### 5d. Video Thumbnail Design

**Objective:** Create click-worthy thumbnail that works at small sizes (mobile-friendly).

**Specifications:**
- **Dimensions:** 1280×720px (16:9 aspect ratio)
- **Format:** JPG or PNG
- **File size:** Under 2MB

**Design Elements:**

**Text Overlay:**
- Large, bold headline (5-7 words max)
- Use Fire Orange or Vivid Magenta for headline
- High contrast against background
- Aeonik Bold, readable at thumbnail size

**Visual Focus:**
- One dominant element (person, icon, or graphic)
- Electric Blue or Fire Orange color blocking
- Avoid clutter - thumbnail shows at 320×180px on mobile

**Brand Elements:**
- MoxyWolf logo in corner (subtle)
- Optional: STIGViewer logo if co-branded

**Best Practices:**
- Test at thumbnail size (does text read clearly?)
- Avoid fine details that disappear when small
- Use bold colors with high contrast
- Include human faces if available (higher CTR)

**Example Concepts:**
- Split screen: "Manual" (chaos) vs "Automated" (order)
- Large statistic in Fire Orange: "338,000 CONTRACTORS AFFECTED"
- Timeline showing critical deadline approaching
- Before/after visual comparison

### 5e. Social Media Clips (30-60 Seconds)

**Objective:** Extract high-impact moments from main video for social distribution.

**Clip Types:**

**Type 1: Shocking Stat Clip (30 sec)**
- Opens with jaw-dropping data point
- Context in next 15 seconds
- Ends with "Full analysis in comments" CTA
- Square format (1080×1080px) for Instagram/LinkedIn

**Type 2: Key Insight Clip (45-60 sec)**
- Hosts discussing the "hidden in plain sight" moment
- The "aha" realization
- Teaser that makes viewers want full video
- Horizontal format (1920×1080px) for YouTube/LinkedIn

**Type 3: Action Step Clip (30 sec)**
- Practical next step from conversation
- "Here's what you need to do immediately..."
- Direct CTA to lead magnet
- Vertical format (1080×1920px) for Reels/Shorts/Stories

**Clip Best Practices:**
- Add burned-in captions (80% watch without sound)
- Use MoxyWolf colors for caption styling
- Include hook in first 3 seconds
- End with clear CTA and logo
- Export with high-quality audio

### 5f. Distribution Checklist

**Day 1 (Publication Day):**
- [ ] Publish blog post to website
- [ ] Upload lead magnet to gated landing page
- [ ] Publish full video to YouTube
- [ ] Post Variant 1 LinkedIn post (Direct/Urgent tone)
- [ ] Share infographic on LinkedIn as native image post
- [ ] Send email announcement to subscriber list

**Day 2:**
- [ ] Post 30-sec stat clip to LinkedIn
- [ ] Share infographic to Instagram
- [ ] Post Variant 2 LinkedIn post (Insight/Strategy tone)
- [ ] Respond to all comments on Day 1 posts

**Day 3:**
- [ ] Post 60-sec insight clip to YouTube as Short
- [ ] Share audio version on Twitter with link to blog
- [ ] Cross-post infographic to Twitter

**Day 4:**
- [ ] Post Variant 3 LinkedIn post (Personal/Narrative tone)
- [ ] Share vertical clip to Instagram Stories/Reels
- [ ] Engage with comments across all platforms

**Day 7 (Week Later):**
- [ ] Reshare top-performing content with fresh commentary
- [ ] Email nurture sequence: Day 3 email with video link
- [ ] Pin top-performing LinkedIn post to profile

**Ongoing:**
- [ ] Monitor video analytics for drop-off points
- [ ] Track lead magnet download conversions
- [ ] Note which content variant performed best
- [ ] Repurpose for next week's content

**Platform-Specific URLs:**
- Blog post: [URL]
- Lead magnet: [Gated landing page URL]
- YouTube video: [URL with timestamps]
- Infographic download: [Direct link or embed]

**UTM Tracking:**
- LinkedIn organic: `?utm_source=linkedin&utm_medium=organic&utm_campaign=[topic]`
- YouTube: `?utm_source=youtube&utm_medium=video&utm_campaign=[topic]`
- Email: `?utm_source=email&utm_medium=newsletter&utm_campaign=[topic]`

**See:** `references/multimedia-asset-guide.md` for complete distribution templates

## Output Checklist

Before completing, verify:

**Lead Magnet:**
- [ ] Immediately actionable with checkboxes/clear steps
- [ ] Professionally formatted with tables and sections
- [ ] Includes attribution and date
- [ ] Scannable in under 2 minutes
- [ ] Provides genuine value beyond blog post

**Bibliography:**
- [ ] All blog sources have BibTeX entries
- [ ] Every entry includes a substantive abstract (2-4 sentences)
- [ ] Abstracts include specific data/findings/claims
- [ ] Proper citation keys and formatting
- [ ] File saved as .bib format

**LinkedIn Posts:**
- [ ] Three distinct variants created
- [ ] Each under 1,500 characters
- [ ] Clear CTAs for both blog and lead magnet
- [ ] Authentic voice maintained
- [ ] Relevant hashtags included
- [ ] Formatting optimized for readability

**Multimedia Assets:**
- [ ] Video prompt (5-10 min) with three-act structure and pronunciation guide
- [ ] Audio prompt (1.5 min) ultra-condensed version
- [ ] Infographic design specifications using MoxyWolf colors
- [ ] Video thumbnail design specifications
- [ ] Social clip guidelines (30-60 sec variants)
- [ ] Distribution checklist with platform-specific timing
- [ ] ICP targeting notes applied throughout

## File Outputs

Save all deliverables to `/mnt/user-data/outputs/`:

1. `[topic]_lead_magnet.md` - Lead magnet in markdown
2. `[topic]_bibliography_with_abstracts.bib` - BibTeX file with abstracts
3. `[topic]_linkedin_posts.md` - All 3 post variants
4. `[topic]_multimedia_assets.md` - Video/audio prompts, infographic specs, thumbnail design, distribution checklist

Present all files to user with succinct summary of what was created.

## References

- `lead-magnet-examples.md` - Complete lead magnet examples and templates
- `linkedin-post-examples.md` - Full LinkedIn post examples with analysis
- `multimedia-asset-guide.md` - Video/audio prompts, infographic templates, distribution strategies
