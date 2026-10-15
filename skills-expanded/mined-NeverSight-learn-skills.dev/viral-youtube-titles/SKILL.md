---
name: viral-youtube-titles
description: Generates viral-style YouTube titles using psychology-backed curiosity gaps, specific pain points, and proven high-CTR structures. Titles feel natural, intriguing, and clickable without sounding spammy.
---

# Viral YouTube Titles

Generate YouTube titles that earn clicks by making the viewer feel like they _have_ to watch — not because it's loud, but because skipping would feel like a mistake.

This skill is optimized for:

- Curiosity-gap and open-loop structures
- Specific, credible pain points (not vague hype)
- High-CTR formulas backed by real viewing psychology
- Natural language that avoids clickbait fatigue

## When To Use

Use this skill when the user asks for:

- YouTube video titles
- Title rewrites or A/B variations
- Thumbnail text that pairs with the title
- Titles for tutorials, vlogs, essays, product reviews, or case studies
- Help making titles feel less generic or flat

## Core Outcome

Produce 5 ready-to-test YouTube title options that:

- Create an open loop the viewer needs to close by watching
- Use specific details (numbers, timeframes, names) to signal credibility
- Match the video's actual content — no misleading bait
- Are under 70 characters when possible (fits desktop truncation)

## Input Contract

Collect these inputs first:

1. What is the video about? (topic + main point)
2. Who is the target viewer?
3. What result, surprise, or revelation does the video deliver?
4. Any specific numbers, names, or facts from the video?
5. What emotion should the title trigger? (curiosity, urgency, relief, validation)

If key context is missing, ask up to 5 short questions.

If the user does not respond, proceed with clear assumptions and state them in one line before output.

## Non-Negotiable Rules

1. Return exactly 5 title options per request.
2. Each title must use a different formula from the Writing System.
3. No all-caps words except acronyms.
4. No more than one exclamation mark across all 5 titles.
5. Avoid these words: amazing, incredible, insane, mind-blowing, shocking, epic, crazy, ultimate, best ever, you won't believe, must-watch, hustle, grind, disrupt, next level, game changer, transform.
6. Do not start two titles with the same first word.
7. Every title must be true to the video content — no false promise.
8. Specificity over vagueness: "lost 12 lbs" beats "lost weight", "$4,200/month" beats "passive income".
9. Under 70 characters preferred. Flag if over 80.
10. No hashtags or emojis in the title.

## Writing System

### Formula 1 — The Honest Result

Show the outcome first. Let credibility carry the click.

**Shape:**

- "how i [specific result] in [timeframe]"
- "how i [specific result] without [expected requirement]"
- "how i went from [before] to [after] in [timeframe]"

**Rules:**

- First-person ("i") makes it feel real
- Result must be specific and measurable
- Timeframe creates urgency and credibility

**Examples:**

- "how i got 10,000 youtube subscribers without paid ads"
- "how i went from $0 to $4,200/month in 90 days"

### Formula 2 — The Reframe / Myth Bust

Challenge something the viewer already believes. Make them doubt themselves enough to click.

**Shape:**

- "why [common belief] is wrong"
- "stop [common advice] — do this instead"
- "the real reason [problem the viewer has]"

**Rules:**

- Name the wrong belief specifically, not vaguely
- The "instead" or "real reason" must be genuinely surprising
- Tone is calm and authoritative, not antagonistic

**Examples:**

- "why posting every day is killing your channel growth"
- "stop optimizing your thumbnails — fix this first"

### Formula 3 — The Curiosity Gap

Give partial information. Make completing the thought feel necessary.

**Shape:**

- "the [adjective] [thing] nobody talks about"
- "what [authority/most people] get wrong about [topic]"
- "i did [unusual thing] for [time] — here's what happened"

**Rules:**

- The gap must be real — the viewer must not already know the answer
- Avoid fake gaps: "the secret to success" tells them nothing
- Best when paired with a specific, unusual angle

**Examples:**

- "the youtube metric nobody talks about (that actually matters)"
- "i posted every day for 6 months — here's the honest truth"

### Formula 4 — The Numbered List with a Twist

Listicle structure with tension built in. The number creates completion drive.

**Shape:**

- "[number] [things] that [result/caused problem]"
- "[number] mistakes [audience] makes without knowing it"
- "[number] reasons why [painful situation]"

**Rules:**

- Odd numbers feel more credible than even
- Add a qualifier that implies the viewer is affected ("without knowing it", "that cost me")
- Avoid generic lists — the content must be specific to this video

**Examples:**

- "7 youtube mistakes that are quietly killing your views"
- "5 thumbnail errors i made before hitting 100k"

### Formula 5 — The Personal Stakes

Make the viewer feel the consequence of not watching.

**Shape:**

- "i almost [negative outcome] because of [surprising cause]"
- "what i wish i knew before [thing viewer is about to do]"
- "the [timeframe] i'll never [do again / forget]"

**Rules:**

- Loss aversion is more powerful than gain framing
- The stakes must be real and relatable to the target viewer
- First-person ("i") maintains authenticity

**Examples:**

- "what i wish i knew before starting a youtube channel"
- "i almost quit youtube — then this happened"

## Thumbnail Text Pairings (Optional)

If the user asks for thumbnail text, pair it with the best-fit title:

- Thumbnail text extends the title's emotional payload — never duplicates it exactly
- Max 3–5 words on the thumbnail
- Should work without reading the title first

| Title                                   | Thumbnail Text          |
| --------------------------------------- | ----------------------- |
| "how i got 10k subs without paid ads"   | "NO ADS. NO TRICKS."    |
| "7 youtube mistakes killing your views" | "are you doing #3?"     |
| "i posted every day for 6 months"       | "honest results inside" |

## Voice And Tone

Titles should sound like a knowledgeable person talking directly to one viewer:

- calm, specific, and direct
- slightly vulnerable when using first-person
- authoritative when using reframes
- never performative or hype-driven

**Avoid:**

- sensationalism
- vague promises
- tone that implies the viewer is foolish for not knowing already

## Psychology (Use Internally)

Apply these while generating — never explain them in the output:

- **Zeigarnik Effect** — open loops create tension that demands resolution; the title is incomplete, the video completes it
- **Curiosity Gap** — partial information is more compelling than full information
- **Loss Aversion** — "what you're losing" outperforms "what you could gain"
- **Specificity Bias** — exact numbers ("12 lbs", "47 days") feel more credible than round ones
- **Pratfall Effect** — admitting struggle or failure ("i almost quit") increases trust
- **In-group Signaling** — titles that speak to a specific audience ("what youtubers don't tell you") make that audience feel seen

## Output Format

Return output in this exact structure:

### Title Options

**1. [Formula Name]**
[title text]
`XX characters`

**2. [Formula Name]**
[title text]
`XX characters`

**3. [Formula Name]**
[title text]
`XX characters`

**4. [Formula Name]**
[title text]
`XX characters`

**5. [Formula Name]**
[title text]
`XX characters`

### Recommended

**Option X** — [One sentence explaining why it fits this video best.]

Do not add extra commentary unless the user asks for explanation.

## Quality Checklist Before Finalizing

- Each title uses a different formula.
- No two titles start with the same word.
- All specifics (numbers, timeframes, names) match the actual video content.
- No banned words.
- No fake curiosity gaps (the gap must be genuinely surprising).
- Character counts are under 70 where possible; flagged if over 80.
- Titles read naturally out loud — not like ad copy.
- Recommended pick is clearly the strongest option.

## Optional Variations

If the user asks for more options:

- Provide 3 alternate titles using the same formula but a different angle, or
- Provide a full set of 5 using only one specified formula, or
- Provide a **safe vs. bold** pair: one lower-risk title and one high-variance title for A/B testing

## Domain Defaults (If User Gives No Context)

Assume:

- **Audience:** general YouTube creators under 50K subscribers
- **Goal:** grow faster or earn more from YouTube
- **Pain:** not getting views despite putting in effort
- **Emotional trigger:** curiosity + mild loss aversion

## Example

**Input:** Video about how the creator grew from 0 to 8,000 subscribers in 4 months by focusing on SEO instead of thumbnails. Target: beginner YouTubers.

### Title Options

**1. Honest Result**
how i got 8,000 subscribers in 4 months (without good thumbnails)
`62 characters`

**2. Reframe / Myth Bust**
stop obsessing over thumbnails — fix this first
`47 characters`

**3. Curiosity Gap**
the youtube seo strategy nobody talks about (that got me 8k subs)
`64 characters`

**4. Numbered List with a Twist**
5 youtube seo mistakes keeping beginners stuck at zero views
`59 characters`

**5. Personal Stakes**
what i wish i knew before wasting 6 months on bad thumbnails
`60 characters`

### Recommended

**Option 1** — leads with a credible, specific result and immediately defuses the most common objection beginners have ("but my thumbnails aren't good enough"), which is exactly what this video answers.
