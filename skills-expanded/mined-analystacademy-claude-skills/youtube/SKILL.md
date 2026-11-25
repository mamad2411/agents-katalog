---
name: youtube
description: Search YouTube intelligently for the best video on any topic. Use this skill whenever the user wants to find YouTube videos, search for tutorials, watch something, or discover content on a topic — even if they just say "find me a video about X" or "look up X on YouTube." Runs multiple searches, interprets the user's intent, and returns one clear recommendation plus a few alternatives.
compatibility:
  required_tools: [Zapier:youtube_find_video]
---

# YouTube Search Skill

Find the single best YouTube video for what the user needs, plus 3–4 solid alternatives. No filters, no menus — just good judgment.

---

## Workflow

### Step 1 — Interpret the intent

Before searching, think about what the user actually wants:
- Are they a beginner or do they seem technical?
- Do they want a quick overview or a deep dive?
- Is this a how-to, an explainer, a review, or something else?
- What would the ideal video look like for this person?

Use this to guide your search strategy and final pick.

### Step 2 — Run multiple searches

Generate 3–4 distinct search angles and run them via `Zapier:youtube_find_video`. Each search should approach the topic differently — vary the framing, vocabulary, and specificity. Don't just repeat the same query with minor tweaks.

Example for "what is MCP":
- `"Model Context Protocol explained"` — direct explainer angle
- `"MCP AI agents tutorial beginner"` — hands-on/beginner angle  
- `"why MCP matters AI tools 2025"` — strategic/why-it-matters angle

For each search call use:
```
max_results: 10
order: relevance
published_after: <12 months ago in ISO 8601>
output_hint: title, video URL, duration, published date, channel name
```

### Step 3 — Pool and evaluate candidates

Combine all results across searches (deduplicating by video ID). For each candidate assess:
- **Relevance**: Does it directly address what the user needs?
- **Quality signals**: Channel credibility, title clarity, not clickbait
- **Duration fit**: Does the length match the likely intent? (Quick explainer vs. deep dive)
- **Recency**: More recent is generally better
- **Avoid**: Shorts under 2 min, tangentially related content, duplicate channels (max 1 per channel in final output)

### Step 4 — Pick the best and select alternatives

Choose the single video you'd genuinely recommend if a friend asked. Then pick 3–4 alternatives that offer something meaningfully different — different depth, angle, channel style, or length. Don't just list the next highest-ranked; make sure each alternative has a distinct reason to exist.

### Step 5 — Present results

Use this format exactly:

---

**Recommended**
[Title](url) · Channel · Duration
One sentence on why this is the best pick for what they asked.

**Also worth watching**
1. [Title](url) · Channel · Duration — one phrase on what makes this different
2. [Title](url) · Channel · Duration — one phrase on what makes this different
3. [Title](url) · Channel · Duration — one phrase on what makes this different
4. [Title](url) · Channel · Duration — one phrase on what makes this different (optional)

---

Keep the "also worth watching" descriptions short — a phrase, not a sentence. The recommendation gets the full sentence; the alternatives just need a differentiating hook.

---

## Tone

- Confident. You picked one. Don't hedge with "this might be good" — say why it's the best fit.
- Don't narrate the search process.
- If the topic is ambiguous, interpret and go — don't ask for clarification first.
