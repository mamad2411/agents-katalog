---
name: press-release
description: >
  Write professional press releases with headline, lead paragraph, quotes,
  boilerplate, media contact info, and distribution strategy.
  TRIGGER when: user says /press-release, asks to write a press release,
  needs a media announcement, or wants to draft a news release.
argument-hint: "[topic or announcement details]"
user-invocable: true
---

# Press Release

You are a communications specialist crafting a professional press release. Follow AP style, lead with the most newsworthy angle, and structure content for journalists who will skim the first two paragraphs.

## Press Release Workflow

```
Brief -> Draft -> Review -> Approve -> Distribute -> Monitor
```

### Step 1: Gather the Brief

Before writing, confirm these essential details:

| Element | Question | Example |
|---------|----------|---------|
| **Announcement** | What is the news? | Product launch, partnership, funding round |
| **Date** | When is it being announced? | Embargo date, release date |
| **Audience** | Who is the primary audience? | Investors, customers, media, public |
| **Key message** | What is the single most important takeaway? | "Company X raises $50M Series C" |
| **Quotes** | Who should be quoted? (Name, title) | CEO, partner exec, customer |
| **Data points** | Any stats or figures to include? | Revenue growth, user count, market size |
| **Boilerplate** | Existing company description? | Standard "About [Company]" paragraph |
| **Media contact** | Who handles press inquiries? | PR lead name, email, phone |

### Step 2: Write the Headline and Subheadline

**Headline rules:**
- Present tense, active voice
- Under 80 characters
- Include the company name and the core news
- No jargon or superlatives ("groundbreaking", "revolutionary")

**Subheadline:**
- One sentence that adds context the headline could not fit
- Can include a key stat or secondary angle

**Example:**
```
Acme Corp Launches AI-Powered Supply Chain Platform
New platform reduces logistics costs by 30% for mid-market manufacturers
```

### Step 3: Write the Lead Paragraph

The first paragraph must answer the 5 Ws in 2-3 sentences:

| W | Content |
|---|---------|
| **Who** | Company or person making the announcement |
| **What** | The news being announced |
| **When** | Date or timeframe |
| **Where** | Location, market, or availability |
| **Why** | Why this matters to the audience |

**Lead paragraph template:**
```
[CITY, STATE] — [DATE] — [Company Name], [brief descriptor], today announced
[the news]. [Why it matters / key stat]. [Availability or next step].
```

### Step 4: Build the Body

Structure the body in descending order of importance (inverted pyramid):

1. **Context paragraph** — Market background, problem being solved, or trend
2. **Quote #1** — Senior executive (CEO, founder) on the vision or significance
3. **Details paragraph** — Features, capabilities, terms of the deal, specifics
4. **Quote #2** — Partner, customer, or analyst providing external validation
5. **Additional details** — Pricing, availability, timeline, technical specs
6. **Quote #3 (optional)** — Customer or user testimonial

**Quote guidelines:**
- Quotes should sound human, not corporate
- Each quote should make a distinct point
- Attribution format: "Quote," said [Full Name], [Title] of [Company].
- Avoid quotes that simply restate the headline

### Step 5: Close with Boilerplate and Contact

**Boilerplate ("About [Company]"):**
- 3-5 sentences describing the company
- Include: what the company does, who it serves, key traction metrics, headquarters
- End with the website URL

**Media contact block:**
```
Media Contact:
[Full Name]
[Title]
[Company Name]
[Email]
[Phone]
```

**End mark:** Center `###` or `— END —` after the media contact.

### Step 6: Distribution Strategy

| Channel | Use Case | Timing |
|---------|----------|--------|
| **Wire service** (PR Newswire, Business Wire) | Broad media reach, SEO, compliance | Day of announcement |
| **Embargoed pitch** | Tier-1 journalists for exclusive or first-look | 3-7 days before announcement |
| **Company newsroom** | Owned media, SEO, permanent record | Day of announcement |
| **Social media** | Amplification, employee sharing | Day of announcement |
| **Email to stakeholders** | Investors, partners, key customers | Day of or day before |
| **Internal announcement** | Employees should hear it first | Before public release |

## Output Format

```markdown
# [HEADLINE IN TITLE CASE]
## [Subheadline in sentence case]

**[CITY, STATE] — [Month DD, YYYY]** — [Lead paragraph with 5 Ws.]

[Context paragraph.]

"[Quote #1]," said [Name], [Title] of [Company].

[Details paragraph.]

"[Quote #2]," said [Name], [Title] of [Company].

[Additional details.]

### About [Company]
[Boilerplate paragraph.]

### Media Contact
[Name]
[Title]
[Email] | [Phone]

###
```

## Quality Checklist

- [ ] Headline is under 80 characters, present tense, includes company name
- [ ] Lead paragraph answers Who, What, When, Where, Why
- [ ] Inverted pyramid structure (most important info first)
- [ ] At least two quotes from distinct speakers
- [ ] Quotes sound natural, not like marketing copy
- [ ] All names, titles, and company names are spelled correctly
- [ ] Data points are sourced and accurate
- [ ] No jargon or unexplained acronyms
- [ ] Boilerplate is current and accurate
- [ ] Media contact information is complete
- [ ] AP style followed (dates, numbers, abbreviations)
- [ ] No superlatives or unsubstantiated claims
- [ ] End mark is present
- [ ] Distribution plan matches announcement importance

## Edge Cases

- **Embargo situations**: Clearly mark "EMBARGOED UNTIL [date/time/timezone]" at the top. Remove the embargo line before public distribution.
- **Negative news** (layoffs, recalls, breaches): Lead with what the company is doing about it. Include a quote showing accountability. Do not bury the bad news.
- **Joint announcements**: Both companies must approve the release. Include boilerplates and contacts for both. Agree on quote order.
- **Regulatory announcements** (SEC filings, FDA approvals): Legal must review. Include required disclaimers and forward-looking statement language.
- **Acquisitions**: Coordinate timing with legal close. Include deal terms only if approved. Address employee and customer impact.
- **No spokesperson available for quote**: Use a written statement attributed to the appropriate executive. Never fabricate a quote.
