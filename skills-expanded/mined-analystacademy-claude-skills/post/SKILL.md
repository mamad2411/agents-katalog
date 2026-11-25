---
name: post
description: Write LinkedIn posts in the user's voice — based on a voice profile they fill in below. Use this skill whenever the user asks to write, draft, or brainstorm a LinkedIn post, social post, or caption. Also use when they describe something that happened, share an observation, want to promote content, or say "help me post about this." Even if they don't say "LinkedIn" — if they're sharing something publicly, this skill applies.
---

# LinkedIn Voice Skill

This skill writes LinkedIn posts in YOUR voice — not a generic LinkedIn thought-leader voice, not a "casual professional" AI impression.

To work well, it needs a real voice profile. The template below is a starting point — **you'll need to fill in your own examples and preferences before the skill is useful.** Once filled in, the skill will pattern-match to YOUR specifics rather than to a generic mold.

> **Setup tip:** When you customize this, replace every "[YOUR ...]" placeholder with the real thing. The more specific and real, the better it works. Vague answers produce vague posts.

---

## Step 1 — Fill in the voice profile (do this once)

### About you
- **Name:** [YOUR NAME]
- **Role / title / company:** [YOUR ROLE — e.g. "Founder, Acme Co." or "Senior data scientist at BigCorp"]
- **What you post about:** [YOUR TOPICS — 2–4 themes you publicly write about, e.g. "data viz, presentations, AI tools"]

### Five real posts you've written
Paste 5 of your own actual LinkedIn posts here — the ones that feel most like *you*. Don't paste polished "thought leader" posts you wrote performatively; paste the ones friends would recognize as yours.

```
[POST 1 — paste here]
```

```
[POST 2 — paste here]
```

```
[POST 3 — paste here]
```

```
[POST 4 — paste here]
```

```
[POST 5 — paste here]
```

### Distinctive traits in your writing
List 5–10 specific things you do that aren't generic. Examples to consider:
- A signature opening pattern (e.g. "I always lead with a concrete detail")
- A signature transition word (e.g. "I use 'Translation:' to flip from technical to plain English")
- A humor style (e.g. "dry asides in parentheses", "self-deprecating", "no jokes at all")
- A signoff pattern (e.g. "I always end with 'More to come!'")
- Word choices you avoid (e.g. "I never use 'leverage' or 'unlock'")
- Emoji usage (e.g. "1–2 emojis sometimes, usually none")
- Length tendency (e.g. "I write 100–250 words usually")

Fill in:

- [TRAIT 1]
- [TRAIT 2]
- [TRAIT 3]
- [TRAIT 4]
- [TRAIT 5]
- [TRAIT 6 — optional]
- [TRAIT 7 — optional]

### Things you NEVER do
List 5–10 patterns you find cringeworthy or AI-shaped. Examples:
- "I never write 'It's not X, it's Y'"
- "I never end with 'What do you think? Drop a comment!'"
- "I never use the rule of three (clear, concise, actionable)"
- "I never start with 'In today's world...' or any abstract opener"

Fill in:

- [NEVER 1]
- [NEVER 2]
- [NEVER 3]
- [NEVER 4]
- [NEVER 5]

---

## Step 2 — Drafting workflow

When asked to write a post:

1. **Understand what the user wants to say.** If the prompt is vague, ask one question: what's the real thing that happened, or the real thing they want people to know?

2. **Find the hook in the specifics.** What's the most concrete, true, slightly-unexpected detail here? Start there. Resist the urge to open with a broad statement.

3. **Draft the post.** Stay in the user's voice throughout (per the profile above). Write paragraphs, not line-per-sentence stacks (unless their voice profile says otherwise).

4. **Run the AI-tells check.** Open `references/avoid-ai-tells.md` and scan the draft for any of those patterns. Strip them out. Pay special attention to: constructed humor, rule of three, "It's not X, it's Y", corporate vocab, grand endings.

5. **Present the post.** If the request was open-ended, offer 2 versions with clearly labeled angles (e.g., "Option A — leads with the personal story / Option B — leads with the insight"). Otherwise, one draft is fine.

6. After the post, add a single line noting what choice you made and invite feedback.

---

## Common post structures

Most personal-voice LinkedIn posts fall into one of these shapes. Pick the one that fits the material — don't force material into a structure that doesn't fit.

### 1. Concrete Hook → Real Point
Open with a specific, true, slightly-weird detail. Then connect it naturally to something worth saying. The hook should be something that actually happened, not a constructed image — specificity is the whole point.

### 2. Observation → Practical Tips
Notice something real in the world. Explain why it matters. Give 3–5 numbered steps. End with a wry line.

### 3. Warm Team/Event Update
Describe a real trip or moment. Name people specifically. Be genuine. Don't moralize or draw lessons — let the story be the story.

### 4. Contrarian Take + Data
Push back on a popular narrative. Stay calm, not combative. Use real numbers when possible. End with a plain-English summary.

### 5. Tool/Test Breakdown
"I tested X across 5 real situations." Structured, honest about limitations. One clear verdict at the end.

---

## Output Format

- Full post, ready to copy-paste
- Paragraph breaks between ideas (not single-sentence line breaks throughout, unless that's part of the user's voice)
- 100–250 words is the typical sweet spot; longer only if the content clearly warrants it
- If offering variants: label them simply ("Option A / Option B")

---

## Final Gut-Check

Before finishing, read the post out loud (mentally). If any sentence sounds like a generic LinkedIn post rather than the user's voice — rewrite it or cut it.

The goal: someone who knows the user reads this and thinks "yep, that's them." Not "that's a good LinkedIn post."
