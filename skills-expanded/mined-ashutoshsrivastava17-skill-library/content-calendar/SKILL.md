---
name: content-calendar
description: >
  Build a content calendar: themes, formats, channels, publishing schedule,
  ownership, and promotion plan.
  TRIGGER when: user says /content-calendar, "content plan", "editorial calendar", "publishing schedule", "content strategy".
argument-hint: "[time period, e.g. 'Q3 2026' or 'next 30 days']"
user-invocable: true
---

# Content Calendar

Build a structured content calendar that aligns publishing activity with business goals, audience needs, and team capacity. Produces a ready-to-use calendar with themes, formats, channels, owners, and promotion plans.

---

## Process

### Step 1 — Define Goals and Constraints

Establish what the content calendar must achieve and the boundaries it operates within.

| Input | Question | Example |
|---|---|---|
| Business goals | What should content drive? | Lead generation, brand awareness, SEO traffic |
| Time period | How far out are we planning? | 1 month, 1 quarter, 6 months |
| Channels | Where will content be published? | Blog, LinkedIn, Twitter/X, YouTube, newsletter, podcast |
| Team capacity | How many pieces per week can the team produce? | 3 blog posts, 5 social posts, 1 newsletter per week |
| Existing assets | Any content to repurpose or refresh? | Old blog posts, webinar recordings, case studies |
| Key dates | Product launches, events, holidays, industry moments? | Product launch May 15, conference June 3 |
| Brand guidelines | Tone, style, topics to avoid? | Professional but approachable, no political topics |

If the user provides only a vague brief ("plan content for next quarter"), ask for at minimum: goals, channels, and team capacity.

### Step 2 — Develop Content Pillars and Themes

Organize content around 3-5 pillars that map to audience needs and business goals.

| Pillar | Audience Need | Business Goal | Example Topics |
|---|---|---|---|
| Thought leadership | Stay informed on trends | Brand authority | Industry analysis, predictions, opinion pieces |
| Educational | Learn how to solve problems | SEO traffic, lead gen | How-to guides, tutorials, frameworks |
| Product / Solution | Evaluate solutions | Pipeline, conversion | Use cases, comparisons, feature deep-dives |
| Social proof | Validate decisions | Trust, conversion | Case studies, testimonials, customer stories |
| Culture / Brand | Connect with company | Employer brand, loyalty | Team stories, values, behind-the-scenes |

For each pillar, define:
- 3-5 recurring topic clusters
- Target keywords (for SEO-driven content)
- Content formats that work best for this pillar

### Step 3 — Map Content Formats to Channels

Match formats to channels based on what performs in each environment.

| Format | Best Channels | Production Effort | Shelf Life |
|---|---|---|---|
| Long-form blog post (1500+ words) | Blog, SEO | High | Long (evergreen) |
| Short-form blog post (500-800 words) | Blog, newsletter | Medium | Medium |
| Listicle / roundup | Blog, social | Medium | Medium |
| Infographic | Blog, LinkedIn, Pinterest | High | Long |
| Short-form video (< 60s) | TikTok, Reels, Shorts | Medium | Short |
| Long-form video (5-20 min) | YouTube, website | High | Long |
| Podcast episode | Podcast platforms, blog (transcript) | High | Long |
| Social post (text-only) | Twitter/X, LinkedIn | Low | Very short |
| Social post (image/carousel) | LinkedIn, Instagram | Medium | Short |
| Newsletter issue | Email | Medium | Short |
| Case study | Blog, sales collateral | High | Long |
| Webinar / live stream | YouTube, LinkedIn Live, Zoom | High | Medium (with recording) |

### Step 4 — Build the Publishing Schedule

Create the actual calendar entries. Use this structure for each entry:

| Field | Description |
|---|---|
| Publish date | Target date (day of week matters for engagement) |
| Content title | Working title |
| Pillar | Which content pillar it belongs to |
| Format | Blog, video, social, etc. |
| Channel(s) | Where it will be published |
| Target keyword | Primary SEO keyword (if applicable) |
| Owner | Who writes / produces it |
| Status | Idea / Drafting / Review / Scheduled / Published |
| Due dates | Draft due, review due, publish date |
| Promotion plan | How it will be amplified after publishing |
| Notes | Dependencies, assets needed, approvals required |

Optimal publishing cadences by channel:

| Channel | Minimum Viable | Good | Aggressive |
|---|---|---|---|
| Blog | 1x/week | 2-3x/week | Daily |
| Newsletter | 1x/month | Bi-weekly | Weekly |
| LinkedIn | 2x/week | 3-5x/week | Daily |
| Twitter/X | 3x/week | 1-2x/day | 3-5x/day |
| Instagram | 2x/week | 3-5x/week | Daily |
| YouTube | 1x/month | Bi-weekly | Weekly |
| Podcast | Bi-weekly | Weekly | 2x/week |

### Step 5 — Plan Content Repurposing

Maximize ROI by repurposing each anchor piece into multiple derivative assets.

Example repurposing chain from a single blog post:

```
Long-form blog post (anchor)
  ├── LinkedIn article (condensed version)
  ├── Twitter/X thread (key takeaways)
  ├── Instagram carousel (visual summary)
  ├── Newsletter feature (with commentary)
  ├── Short video (1-min summary for Reels/Shorts)
  ├── Infographic (data/process visualization)
  └── Podcast talking point (discussion topic)
```

For each anchor piece in the calendar, define at least 2-3 derivative pieces with their own publish dates and channels.

### Step 6 — Define Promotion Plan

Every published piece needs a promotion plan — organic reach alone is rarely sufficient.

| Promotion Tactic | When | Effort |
|---|---|---|
| Share on owned social channels | Day of publish | Low |
| Email to subscriber list | Day of or next newsletter | Low |
| Internal Slack / team share for employee amplification | Day of publish | Low |
| Engage in comments and related discussions | Day 1-3 | Low |
| Repurpose into social-native format | Week 1 | Medium |
| Pitch to relevant newsletters or communities | Week 1-2 | Medium |
| Paid social boost (top performers only) | Week 2+ | Medium |
| Update and reshare older related content with links | Month 1 | Low |
| Syndicate to Medium, LinkedIn articles, etc. | Month 1 (after indexing) | Low |

---

## Output Format

Deliver the content calendar in two parts:

**Part 1 — Strategy Overview**
1. Goals and success metrics
2. Content pillars with topic clusters
3. Channel strategy and cadence
4. Repurposing framework
5. Promotion playbook

**Part 2 — Calendar (table format)**

| Week | Mon | Tue | Wed | Thu | Fri |
|---|---|---|---|---|---|
| Week 1 | [Blog] Title — Owner | | [Newsletter] Title — Owner | [LinkedIn] Title — Owner | |
| Week 2 | ... | ... | ... | ... | ... |

Each cell includes: [Format] Title — Owner. Provide a separate detailed table with full metadata for each entry.

---

## Quality Checklist

- [ ] Every content piece maps to a business goal and content pillar
- [ ] Publishing frequency is realistic given stated team capacity
- [ ] Key dates (launches, events, holidays) are incorporated
- [ ] Each anchor piece has a repurposing plan
- [ ] Each piece has a clear owner
- [ ] Status tracking fields are included for workflow management
- [ ] SEO-driven content has target keywords assigned
- [ ] The calendar has a mix of formats, not just one type
- [ ] Promotion plan is specified for each piece, not assumed
- [ ] There is buffer time for delays — not every slot is critical-path

---

## Edge Cases

- **Solo creator / one-person team**: Reduce frequency dramatically. Focus on one primary channel and one repurposing path. Prioritize evergreen content over timely pieces.
- **No existing content**: Start with a "foundation" phase — create pillar pages and cornerstone content before filling a high-frequency calendar.
- **Multiple products or business lines**: Create separate pillar structures per product line. Use a shared calendar view but tag entries by product.
- **Highly regulated industry**: Add a compliance review step between "Review" and "Scheduled" status. Build in extra lead time for legal/compliance approval.
- **Seasonal business**: Weight content volume toward pre-season and in-season. Use off-season for evergreen and SEO content that builds authority.
- **B2B with long sales cycle**: Align content to funnel stages (TOFU / MOFU / BOFU). Ensure each stage has adequate coverage, not just top-of-funnel.
- **User wants daily social but has no content**: Implement a 70/20/10 mix — 70% curated/shared content, 20% repurposed owned content, 10% original. Build toward higher original % over time.
- **Content calendar already exists but is stale**: Audit existing calendar first. Identify what to keep, refresh, retire, or fill. Do not start from zero without reviewing what exists.
