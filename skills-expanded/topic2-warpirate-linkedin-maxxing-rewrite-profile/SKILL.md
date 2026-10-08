---
name: rewrite-profile
description: |
  Use when user wants to improve their LinkedIn profile, is preparing
  for a job search, has changed roles, is positioning for a new audience
  (founder, consultant, recruiter), or has not touched their profile in
  over a year. Trigger phrases include "rewrite my LinkedIn profile,"
  "optimize my profile," "fix my headline," "my About section sucks," "I
  want my profile to position me as X." Run audit-profile first if not
  already done.
license: MIT
---

# Rewrite profile

LinkedIn profiles are positioning documents that read top to bottom. The headline is the first impression, the About section is where the visitor decides whether to keep reading, Featured signals what the user wants to be known for, and Experience is the proof. Rewriting one section without the others produces a profile that pulls in different directions. This skill rewrites the page as one unit.

## Why this skill exists

LinkedIn's 2026 ranking system increasingly treats the profile as a "living landing page" rather than a resume. The headline is the most heavily search-indexed text on the page (the first ~50 characters specifically). The About section's "see more" cut at ~250 characters has to earn the click. Featured selection signals what the user wants visitors to look at. Experience bullets get scanned by hiring managers and AI candidate-ranking systems.

Each section serves the others. A headline that says "Building the future of fintech" matched with an About section that talks about consulting work creates dissonance. The visitor leaves. This skill rewrites everything together so the page reads coherently.

## When to use this skill

Trigger when:
- The user is preparing for a job search
- The user changed roles, companies, or career direction
- The user is positioning for a new audience (e.g., from IC to founder, from employee to consultant)
- The user has not updated their profile in over a year
- audit-profile output identified problems that need a full rewrite
- A new role calls for repositioning

Do NOT trigger when:
- The user only wants to fix one section. Even then, push them gently to consider the whole page; one change usually requires others.
- The user is happy with their current positioning and just wants tweaks. Suggest audit-profile first.

## What you need from the user

1. **Their current profile content.** Either pasted into chat (headline, About, Experience bullets, Featured items) or via LinkedIn data export. If they want it audited first, send to audit-profile.

2. **The audience they want to attract.** Not their job title; the audience. "I want recruiters in B2B SaaS to find me." "I want potential coaching clients (early-career engineers) to land on this and book a call." "I want investors to take me seriously as a technical founder."

3. **The one thing they want to be known for.** If they cannot answer in one sentence, this is the deeper problem and we should solve it first. Ask: "If a stranger were going to remember one thing about you from this profile, what should it be?"

4. **Job titles, companies, dates, real numbers from past roles.** Do not invent any of these.

5. **What they want to NOT say.** Anything off-limits: a company name, a specific role, a region, a specific claim. Useful to know upfront.

If voice-profile.md exists, read it.

## How LinkedIn profiles work in 2026

A few format-specific facts:

**Headline.** 220 characters. The first ~50 are most heavily search-indexed (this is the part that determines whether you show up for "[role] in [city]" searches). Everything past character 50 is read-by-humans, not search.

**About section.** 2,600-character limit. The first ~250 characters are visible before "see more." The visitor decides at the fold whether to expand. The body should not be a resume restatement; it should answer "who is this person and why should I care."

**Featured.** Up to 5 items pinned at the top of the profile. Posts, articles, links, media. These are the things the user is signaling they want visitors to look at.

**Experience bullets.** 2-5 bullets per role, written with verb + metric + keyword pattern. Hiring managers scan these in seconds. AI candidate-ranking systems also parse them.

**Skills.** Up to 50, with the top 3 pinned for search. The pinned three carry the most search weight.

## How to rewrite

The order matters: nail the positioning first, then write the sections in this order.

### Step 1: Lock the positioning

Before any copy, get clear on:
- The one sentence answering "who is this person and why should I care?"
- The audience they want to attract.
- The trait or work they want to be known for.

If any of these is unclear, ask once and commit. Do not loop on this.

### Step 2: Headline

220 characters. Structure:

```
[role/identity in 30-50 chars] | [proof or specificity] | [hook for the audience]
```

Examples:
- "Engineering manager scaling teams from 5 to 30 | Ex-Stripe, Ex-Brex | Hiring across data infra and payments"
- "I help early-career engineers get promoted | 200+ coached | Building [newsletter name]"
- "Product designer for B2B SaaS | Shipped at Notion, now at [company] | Carousels on design systems and product judgment"

Rules:
- The first ~50 characters carry the search weight. Put the search term (role, function, industry) there.
- Avoid "passionate about" / "driven by" / "evangelist for" / "ninja" / "guru."
- Specific over impressive. "Engineering manager who has scaled three teams from 5 to 30" beats "Visionary engineering leader."
- No emojis unless the user uses them in posts (voice-profile.md will tell you).

### Step 3: About section

Aim for 1,000-1,500 characters. Structure:

**Above the fold (~250 chars).** A hook. The strongest claim the user can make about themselves, written for the audience they want to attract. Not "I have 10+ years of experience" (everyone says this). Specific: a number, a position, a contrarian claim about their field.

**Body.** Tell the story of the positioning. Not the resume. Two or three short paragraphs that answer:
- What is the user actually trying to do (the work, not the title)
- What makes them able to do it (the proof, the specifics, the trajectory)
- Where they want to go (forward-looking, but not aspirational filler)

**Close.** A specific invitation. Not "feel free to connect." Examples: "DM me if you are hiring data infra ICs in NYC." "I write a weekly newsletter on early-career promotion. Link in Featured." "If you are building in [domain] and want to compare notes, my calendar is in Featured."

### Step 4: Featured

Choose up to 5 items. Pin the ones that:
- Show the work, not the credentials (a project, a piece of writing, a talk)
- Signal what the user wants to be known for
- Are recent or evergreen (not three years old)

If the user has nothing strong to feature, say so and suggest they create one piece of work to feature. Featured slots without strong content hurt more than empty Featured.

### Step 5: Experience bullets

For each role, 2-5 bullets. Structure:

```
[strong verb] [what specifically] [metric or named outcome] [tool/method/scale]
```

Bad: "Worked on improving the product and growing the team."
Good: "Rewrote the onboarding flow for new free users, increasing day-7 activation from 22% to 41% over six months. Led a team of three engineers and worked across product and design."

Rules:
- Numbers wherever truthful. If the user does not have the numbers, use "by [order of magnitude]" but mark for them to add real numbers if they have them.
- One bullet per accomplishment, not one bullet per responsibility.
- Mix scale: one strategic bullet, one tactical bullet, one cross-functional bullet per role works well.

### Step 6: Skills (top 3 pinned)

Pick the three skills that:
- Match what recruiters search for in the user's domain
- Are actually backed by evidence in the rest of the profile
- Are listed exactly as recruiters would search (e.g., "Product Management" not "Product Strategy & Vision")

## Drafting constraints (apply WHILE writing, not after)

Output must read as written by a human on the first pass. The constraints below are how you write, not a checklist to apply later. Do not narrate this process to the user. Do not show a "before humanizer / after humanizer" sequence. Just produce clean output.

**Hard bans — never appear in output:**
- Em dashes (—) and en dashes (–). Use period, comma, colon, or parentheses.
- "It's not just X, it's Y" / "Not only X but Y" constructions.
- "The real question is," "at its core," "fundamentally," "what really matters."
- Signposting: "Let's dive in," "here's what you need to know," "let's break this down," "without further ado."
- Sycophancy: "Great question," "you're absolutely right," "I hope this helps," "let me know if..."
- Knowledge-cutoff hedges: "based on available information," "as of my last update."
- AI vocabulary: leverage, delve, tapestry, underscore, pivotal, crucial, vibrant, testament, landscape (abstract), interplay, intricate, fostering, enduring, garner, valuable, enhance, showcase, align with, additionally.
- Copula avoidance: "serves as," "stands as," "marks a," "represents a," "boasts," "features." Use is/are/has.
- Emoji decoration on bullets or headings.
- Title Case In Headings. Use sentence case.
- Curly quotes ("..."). Use straight quotes (") only.
- Bold for random emphasis. Bold only for genuine key terms.
- Rule-of-three padding where the third item is filler.
- Generic upbeat conclusions ("The future looks bright," "exciting times ahead").
- Aphorism formulas ("X is the language of Y," "X becomes a trap," "X is not a tool but a mirror").
- Theatrical openers: "Honestly?" "Look," "Here's the thing," used as standalone pause-and-reveal.
- Inline-header bullet lists (`- **Speed:** ...`). Write as prose.
- "-ing" tag-ons that add fake depth: "highlighting," "underscoring," "fostering," "reflecting," "showcasing," "ensuring," "contributing to."

**Required patterns:**
- Specific, hard-to-fabricate detail. Real numbers, real names, real quotes from the user's input.
- Vary sentence length. Short. Then longer ones that take their time. Mix.
- Active voice over passive. Concrete actor over hidden subject.
- Simple copulas (is/are/has) over fancy substitutes.
- One opinion or mixed feeling where the format allows (not for neutral reference text).
- Cut every filler phrase ("in order to" → "to," "due to the fact that" → "because," "at this point in time" → "now," "has the ability to" → "can").

**Final scan before output:**
1. Scan for `—` and `–`. Any hit means redraft.
2. Scan for any word in the AI-vocabulary list above. Any hit means rewrite that sentence.
3. Scan for "it's not X, it's Y" pattern. Any hit means rewrite.
4. If three short fragments appear in a row mid-paragraph, the rhythm is engineered. Vary.

Full 33-pattern reference: see humanizer/SKILL.md in this plugin.

## Output format

```
# Profile rewrite for [user's name]

Audience: [the audience they are positioning for]
One-line positioning: [the one sentence]

---

## Headline (NEW)
[new headline, character count]

## Headline (BEFORE)
[old headline if available]

## About (NEW)
[new About, character count, with the "see more" fold marked]

## About (BEFORE)
[old About if available]

## Featured recommendations
[what to pin, in priority order, with reasoning]

## Experience bullets (NEW)
[For each role]
Role: [title at company]
Bullets:
- [bullet 1]
- [bullet 2]
- [bullet 3]

## Experience bullets (BEFORE)
[old bullets if available, for comparison]

## Skills to pin (top 3)
1. [skill]
2. [skill]
3. [skill]

---

## Notes on the rewrite
[2-4 sentences on what changed and why]

## What the user still needs to do
- [Action items: add real numbers to bullets, choose Featured items, update photo, etc.]
```

## What this skill does not do

- Invent roles, dates, companies, or accomplishments. Everything in the rewrite must come from what the user actually did.
- Translate "passionate about X" into something more elegant. The right move is to cut the line and replace it with a specific claim, not to refine the cliché.
- Choose the user's positioning for them. If the user says "I want to be known for X," the skill positions for X. The skill can push back once if the positioning is unclear, but then commits.
- Produce three variations of the headline by default. One good headline. Variants on request.
- Promise a specific increase in profile views or recruiter outreach. Outcomes depend on too many variables.
