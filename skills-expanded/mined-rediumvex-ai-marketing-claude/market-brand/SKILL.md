---
name: market-brand
description: Brand voice, tone, and archetype analysis with generated voice guidelines. Invoke whenever the user mentions "brand voice", "tone of voice", "how do we sound", "brand guidelines", "archetype", or runs `/market brand <url>`. Produces BRAND-VOICE.md with 4 voice dimensions, archetype mapping, do/don't chart, vocabulary lists, and 8 copy samples.
---

# Market Brand — Voice, Tone, and Archetype

Analyze how a brand communicates across every touchpoint and produce a usable voice guide that a new copywriter could pick up and write on-brand within an hour.

## Source material (in priority order)

1. **Homepage** — the most curated representation
2. **About page** — how they describe themselves
3. **Product / pricing pages** — how they sell
4. **Blog (3–5 recent posts)** — extended voice
5. **Social profiles** — conversational voice
6. **Error / empty states / microcopy** — unguarded voice
7. **Email or newsletter** if accessible
8. **Job postings** — internal culture signal

Use `scripts/analyze_page.py` to pull raw text from each page.

## The 4 Voice Dimensions (score each 1–10)

### Formal ↔ Casual
Signals: contractions, sentence length, "we/you" vs "the company/one", greetings, slang.

### Serious ↔ Playful
Signals: exclamation marks, emoji, puns, metaphors, error message style, self-deprecation.

### Technical ↔ Simple
Signals: jargon density, acronym explanation, detail depth, assumed expertise.

### Reserved ↔ Bold
Signals: hedged claims ("may help") vs direct claims ("guaranteed"), opinionated stances, competitor mentions.

**Every score needs 3 quoted examples from the source material** — no score without evidence.

### Voice map (ASCII visualization)

```
Formal    |----------[●]-----------| Casual     (6/10)
Serious   |-------[●]--------------| Playful    (4/10)
Technical |-----------------[●]----| Simple     (7/10)
Reserved  |--------------[●]-------| Bold       (6/10)
```

## Archetype Detection (Jung's 12, collapsed to 12 for brand use)

Map the brand to 1 primary and optionally 1 secondary archetype:

| Archetype | Driver | Voice cue |
|---|---|---|
| **Sage** | Wisdom, truth | Educational, cited, measured |
| **Innocent** | Simplicity, optimism | Warm, direct, positive |
| **Explorer** | Freedom, discovery | Adventurous, independent |
| **Hero** | Mastery, courage | Bold, challenge-oriented |
| **Outlaw** | Disruption | Provocative, anti-establishment |
| **Magician** | Transformation | Visionary, "imagine if" |
| **Regular Guy/Gal** | Belonging | Plain-spoken, relatable |
| **Lover** | Intimacy, beauty | Sensual, emotional, curated |
| **Jester** | Joy, play | Witty, irreverent, memeable |
| **Caregiver** | Service, protection | Nurturing, supportive |
| **Creator** | Craft, imagination | Artisan, detail-loving |
| **Ruler** | Control, quality | Authoritative, premium |

Give the archetype score with evidence. Many brands blend two — e.g., Notion is Creator + Sage; Liquid Death is Outlaw + Jester.

## Tone by Context

Voice is consistent; tone shifts. Map how the brand should sound in each context:

| Context | Tone | Example (quoted or drafted) |
|---|---|---|
| Homepage hero | | |
| Product description | | |
| Blog post | | |
| Social post | | |
| Error / 404 | | |
| Email subject | | |
| CTA button | | |
| Support reply | | |

## Vocabulary

### Signature words (15–20)
Words the brand uses repeatedly, grouped by action verbs, descriptive adjectives, value words, industry terms.

### Words to avoid
Off-brand words, clichés, competitor terminology.

### Signature phrases
Taglines, recurring openers, linguistic patterns (e.g., "always starts with a verb").

## Do / Don't Chart

| DO | DON'T |
|---|---|
| Use contractions | Use legalese |
| Lead with the benefit | Lead with the feature |
| Address the reader as "you" | Refer to "users" or "customers" |
| Be specific with numbers | Say "world-class" or "best-in-class" |

## Consistency Audit

For each channel, rate Consistent / Mostly / Inconsistent with a one-line note. Identify the top 1–2 divergences (e.g., "homepage is bold and confident, but support emails are formal and hedged — this erodes trust").

## 8 Copy Samples

Generate these so writers have references:

1. Homepage H1
2. Product one-liner
3. Feature description (100 words)
4. Blog post intro (50 words)
5. Social post (platform-appropriate)
6. Email subject line (3 variants)
7. CTA button (primary + secondary)
8. Error message / empty state

## Output: BRAND-VOICE.md

```markdown
# Brand Voice — [Brand]
**Analyzed:** [YYYY-MM-DD]  |  **Sources:** [list]

## Voice Summary
[2–3 sentences: archetype, dimensions, what makes this voice distinct.]

## Voice Dimensions
### Formal ↔ Casual: X/10
Evidence:
> "quoted example 1"
> "quoted example 2"

... repeat for all 4 dimensions ...

### Voice Map
[ASCII visualization]

## Archetype
**Primary:** [name] — [why, with evidence]
**Secondary:** [name] — [why]
**Fit:** [Strong / Moderate / Weak]

## Tone by Context
[Table]

## Vocabulary
### Signature words
### Avoid
### Signature phrases

## Do / Don't Chart
[Table]

## Copy Samples
[8 examples]

## Consistency Audit
[Channel-by-channel + overall score]

## Recommendations
### This week
### This quarter
```

## Quality Bar

- Voice is diagnosed, not invented. Don't tell the brand who they should be — tell them who they already are and where they're inconsistent.
- Every dimension score and archetype choice needs quoted evidence.
- The 8 copy samples must sound like the brand, not like generic marketing. Write them after the analysis, not before.
