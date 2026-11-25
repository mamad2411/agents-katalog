---
name: local-pages
description: Write SEO-optimised service pages and location pages for local businesses. Combines copywriting best practices with on-page SEO, Perplexity research, and minimum 1000-word counts. Triggers include requests to write, create, or draft service pages, location pages, area pages, town pages, or city pages for local businesses. Also triggers for "local SEO content", "local landing pages", or requests combining copywriting with local SEO.
user-invocable: true
---

# Local Pages Skill

Write high-converting, SEO-optimised service pages and location pages for local businesses. Combines classic copywriting principles, on-page SEO best practices, and subject matter research.

## Key Features

- **Perplexity research** — Research the subject matter before writing
- **Copywriting principles** — Reason-why framework, proof-based selling
- **On-page SEO** — Keyword-rich titles, H1s, H2s, H3s, meta descriptions
- **Word count minimums** — 1000+ words (configurable for more)
- **Local relevance** — Area-specific content that isn't thin filler

## Input Requirements

Extract from user request or ask if not provided:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| page_type | Yes | - | `service` or `location` |
| primary_keyword | Yes | - | Main target keyword |
| business_name | Yes | - | Client's business name |
| business_type | Yes | - | What the business does (plumber, electrician, etc.) |
| location | Conditional | - | Required for location pages |
| services | Conditional | - | Services to cover (for location pages) |
| word_count_target | No | 1000 | Minimum word count (can specify more) |
| secondary_keywords | No | - | Additional keywords to include |

## Workflow

### Phase 1: Research (Perplexity)

Before writing any content, use `mcp__perplexity__perplexity_ask` to gather subject matter expertise.

**Note:** Use `perplexity_ask` (sonar-pro) for cost efficiency. Only use `perplexity_research` (sonar-deep-research) when explicitly requested for complex topics requiring extensive citations.

**Research Prompt Template:**

```
Research the following for a local business website:

Topic: [SERVICE/BUSINESS TYPE]
Location: [LOCATION if applicable]
Target audience: Homeowners/businesses looking for [SERVICE]

Provide:
1. Common problems/pain points customers face with [SERVICE]
2. Key questions customers ask when hiring a [BUSINESS TYPE]
3. Important certifications, qualifications, or accreditations in this field (UK-specific)
4. Common misconceptions about [SERVICE]
5. Typical price ranges or pricing factors (UK market)
6. Seasonal considerations or timing factors
7. Red flags customers should watch for when choosing a provider
8. What differentiates quality providers from poor ones

Focus on factual, specific information that demonstrates expertise.
```

### Phase 2: Keyword Integration Plan

Before writing, plan keyword placement:

**Primary Keyword Must Appear In:**
- Title tag (front-loaded)
- H1 heading
- First 100 words of body copy
- At least one H2 heading
- Meta description
- URL slug

**Secondary Keywords/Variations:**
- Distribute naturally across H2/H3 headings
- Use in body copy where relevant
- Include in image alt text

### Phase 2.5: Content Differentiation Planning

Before writing, ensure each page will be genuinely unique. See `../copywriting/references/seo-indexing-guidelines.md` for full indexing principles.

**For Location Pages:**
- Identify 3+ locally-specific details (landmarks, neighbourhoods, local issues)
- Find location-specific customer pain points
- Include area-specific proof (local testimonials, jobs completed in area)
- Avoid: identical structures with just town names swapped

**For Service Pages:**
- Identify unique angle vs competitors (specialisation, approach, experience)
- Include specific examples, case studies, or scenarios
- Add genuine expertise competitors haven't covered

**Differentiation Test:** Could a competitor copy this content by just changing the business name? If yes, it needs more specificity.

### Phase 3: Content Structure

See `references/page-structures.md` for detailed templates.

**Service Page Structure (1000+ words):**
```
[Title Tag: Primary Keyword + Benefit + Location | Business Name]
[Meta Description: 150-155 chars with keyword + benefit + CTA]

H1: [Primary Keyword] + [Benefit/Differentiator]
    Lead paragraph (100-150 words): Address reader's situation, core promise

H2: [Keyword variation] - What We Do / How It Works
    (200-300 words): Clear explanation of service

H2: [Keyword variation] - Why Choose [Business Name]
    (200-300 words): Differentiators with proof, credentials, guarantees

H2: [Related keyword] - Common [Service] Problems We Fix
    (200-300 words): Demonstrate expertise, address specific situations

H2: Frequently Asked Questions About [Primary Keyword]
    (150-250 words): FAQ schema opportunity, address objections

H2: [Location] Areas We Cover
    (50-100 words): Local signals, nearby areas

H2: Get Your [Service] Sorted Today
    (50-100 words): Clear CTA with contact details
```

**Location Page Structure (1000-1500 words):**
```
[Title Tag: Primary Service + Location | Business Name]
[Meta Description: 150-155 chars with location + service + CTA]

H1: [Primary Service] in [Location]
    Lead paragraph (100-150 words): Location-specific opening, local credibility

H2: [Service 1] in [Location]
    (250-350 words): Full service description for this location

H2: [Service 2] in [Location]
    (250-350 words): Full service description

H2: [Service 3] in [Location]
    (250-350 words): Full service description

H2: Why [Location] Residents Choose [Business Name]
    (150-200 words): Local proof, testimonials, differentiators

H2: Areas We Cover Near [Location]
    (50-100 words): Nearby towns, postcodes

CTA section with contact details
```

### E-E-A-T Block (Required Per Page)

Post-December 2025, Google applies E-E-A-T expectations to competitive local queries, not just YMYL topics. Every service and location page must include a visible E-E-A-T block alongside the persuasive copy:

- **A named person with a real, verifiable credential:** e.g. a Gas Safe registration number, displayed and linkable, not a vague "our qualified team"
- **An original photo of real work completed in that area:** never stock imagery. Geotagging the photo does nothing: Google strips EXIF data on upload. The photo matters as E-E-A-T evidence, not as a coordinate signal
- **A specific testimonial naming the town and the job:** "Sorted our burst pipe in Dartford within the hour" beats "Great service!"

See `~/.agents/skills/references/shared-seo/local-seo-playbook-2026.md` for the full reasoning behind this requirement.

### Phase 4: Writing

Apply copywriting principles from `references/copywriting-rules.md`:

1. **Reason-Why Framework** — Every claim must have proof
2. **Rule of One** — One dominant message per section
3. **Customer Awareness** — Match approach to reader awareness level
4. **Specificity** — Numbers, credentials, named testimonials over vague claims

Apply SEO integration from `references/seo-rules.md`:

1. **Natural keyword usage** — Never stuff, always readable
2. **Keyword-rich headings** — Include variations in H2/H3s
3. **Local signals** — Geographic terms, local proof, contact info
4. **Schema markup** — Recommend LocalBusiness (specific subtype), FAQ, Review schemas
5. **Summarisable for AI:** Give the page extractable answers: prices or price ranges, hours, coverage areas, FAQs in conversational language. AI Overviews now appear on roughly 68% of local queries, and AI systems recommend businesses they can confidently summarise

### Phase 5: Quality Check

Before delivering, verify:

**Word Count:**
- [ ] Meets minimum target (1000 words or specified amount)
- [ ] No padding or filler content

**SEO Checklist:**
- [ ] Primary keyword in title, H1, first 100 words, one H2, meta description
- [ ] Secondary keywords in H2/H3 headings
- [ ] Heading hierarchy logical (H1 → H2 → H3)
- [ ] Meta description 150-155 characters, includes CTA
- [ ] Internal linking opportunities noted

**Copywriting Checklist:**
- [ ] Every claim has a reason-why
- [ ] Specific proof (numbers, names, credentials) not vague claims
- [ ] Addresses reader's situation in opening
- [ ] Clear, single call-to-action
- [ ] Sounds human, not AI-generated slop

**Indexability Checklist:**
- [ ] Content offers something top 10 results don't
- [ ] Page differs significantly from other pages on this site
- [ ] Removed-city-name test passed: take the town name out of a location page; if it isn't still obviously about that place, it's a doorway page. Target roughly 50% genuinely location-specific content per location page
- [ ] Language sounds natural (read aloud test passed)
- [ ] Primary topic crystal clear in first paragraph
- [ ] Search intent matches what's ranking for target keyword

**Local Checklist:**
- [ ] Location mentioned naturally, not forced
- [ ] Local proof elements included where possible
- [ ] Nearby areas/postcodes listed
- [ ] Contact details present

## Reference Files

- `references/page-structures.md` — Detailed templates with word count targets
- `references/copywriting-rules.md` — Reason-why, proof, persuasion techniques
- `references/seo-rules.md` — Keyword placement, heading optimisation, local SEO
- `references/research-prompts.md` — Perplexity prompt templates by industry

## Quick Start

When `/local-pages` is invoked:

1. **Check for required parameters in user's message**
   - If user provided details (e.g., "/local-pages service page for boiler repair in Dartford"), extract them
   - If missing required info, ASK using AskUserQuestion:
     - "What type of page?" (service/location)
     - "What's the primary keyword?"
     - "What's the business name and type?"
     - "What location?" (for location pages)
     - "Target word count?" (default 1000)

2. **Run Perplexity research** on the subject matter

3. **Plan keyword integration** — Map primary/secondary keywords to headings

4. **Write the content** following structure templates

5. **Verify quality** against all checklists

6. **Deliver** with:
   - Complete page copy
   - Meta title and description
   - Schema markup recommendations
   - Word count confirmation
   - Internal linking suggestions
