---
name: linkedin-draft
description: |
  Gated drafting workflow for LinkedIn posts that enforces source reading, thesis-level adversarial review, voice pre-flight, and antislop before presenting a draft. This skill should be used when drafting LinkedIn content — it handles writing only, not publishing (use /linkedin-publish to publish).
version: 2.0.0
last_modified: 2026-03-23
user-invocable: true
effort: max
---

# LinkedIn Draft

Five-gate workflow that produces voice-matched LinkedIn drafts requiring minimal editing. Separates drafting (this skill) from publishing (`/linkedin-publish`).

**Why this exists:** Without gates, Claude consistently drafts before reading sources, defaults to consensus takes, violates voice rules even when loaded, and runs adversarial review too late to matter. This skill enforces the right sequence.

**Target:** The user should need 1-2 editing passes, not 4-5.

---

## Prerequisites

The user must have a voice profile at `./VOICE.md`. If one does not exist, prompt the user to create one via `/voice-analyzer` before proceeding.

---

## Gate 1: Source Material

**Trigger:** User references any article, study, report, or external content.

1. If a URL is mentioned or implied, ask for it before writing anything
2. Read the source via WebFetch
3. Extract and note:
   - Authors and publication
   - Key data points and statistics
   - Methodology (what data, what timeframe, what scope)
   - Nuances and caveats the authors include
   - What the source does NOT say (gaps the post can address)
4. If no external source, skip to Gate 2

**Rule:** Never draft a post about research you haven't read.

---

## Gate 2: Thesis + Adversarial Review

This is the most important gate. It catches consensus takes before they become 300 words of sunk cost.

### Step 1: Form the thesis

State it in 1-2 sentences. Then ask yourself:

| Check | Question |
|-------|----------|
| Consensus test | Is this what most commentators would say about this source? |
| User's framing | What did the user emphasize? What did they call interesting? That's probably the lede. |
| Audience fit | Who is this for, and what will stop them scrolling? |

### Step 2: Run epistemic agents on the thesis

Launch in parallel (use Agent tool with appropriate subagent_type):

| Agent | What to ask |
|-------|-------------|
| **epistemic-violet** | "Is this the consensus take? What's the more interesting, contrarian, or reframed angle? What would make someone stop scrolling?" |
| **epistemic-green** | "Is this thesis logically sound? What are the strongest counterarguments? What assumptions need surfacing?" |

### Step 3: Present options to the user

Show 2-3 thesis options with one sentence each:
- **Option A:** The obvious/consensus take
- **Option B:** The reframed/contrarian take (usually from Violet)
- **Option C:** (if applicable) A synthesis or third angle

Let the user choose before writing a single paragraph.

---

## Gate 3: Draft

### Context to load (auto-load, don't ask permission)

| File | Path | Required? |
|------|------|-----------|
| Voice Profile | `./VOICE.md` | **Yes** — do not draft without this |

If the user has additional strategy or content plan files referenced in their vault, load those too. But the voice profile is the only hard requirement.

### Drafting rules

- **Length:** 200-400 words. Under 200 feels thin; over 500 gets truncated by LinkedIn.
- **Structure:** Insight leads. Experience follows as evidence. Anecdote serves the idea, not the reverse.
- **Warmth:** Include at least one human-reaction beat. The author responds to findings as a person, not just an analyst. Self-aware hedges, honest reactions, acknowledgment of difficulty.
- **Contractions:** Use naturally (doesn't, won't, isn't). Conversational register.
- **Closing:** End with practical implications, operational specificity, or genuinely specific questions aimed at the target audience. Never end with engagement bait or soft closes.

---

## Gate 4: Voice Pre-Flight

**This gate is internal. Do not present the draft until it passes.**

Scan the draft against every item. If any check fails, fix it silently and re-check.

### Hard failures (fix before presenting)

| # | Check | What to look for |
|---|-------|-----------------|
| 1 | No credentials-forward openings | "After working with...", "In my X years of...", "Every major shift I've worked through..." |
| 2 | No positioning | "What most executives miss...", "Unlike standard approaches...", "Here's what others get wrong..." |
| 3 | No artificial coyness | "I'm still figuring this out...", "a puzzle I'm still working on..." |
| 4 | No soft closes | "What do you think?", "I'd love to hear...", "If this resonates..." |
| 5 | No sentence fragments | Every sentence has a subject and a verb. "Not X. Not Y. Real Z." → combine into one sentence |
| 6 | Max 2 em dashes | Count them. If >2, convert extras to commas, periods, or parentheticals |
| 7 | No forbidden phrases | "delve", "game-changing", "leverage", "moreover", "furthermore", "it's worth noting" |

### Warmth and voice checks (fix before presenting)

| # | Check | What to look for |
|---|-------|-----------------|
| 8 | Warmth beats present | At least one moment of human reaction, self-awareness, or genuine feeling |
| 9 | Insight leads, experience follows | The idea comes first. The anecdote supports it. Never "That tracks with what I've seen..." as the opening move |
| 10 | Sentence rhythm varies | Mix short punchy sentences (5-8 words) with longer explorations (20-30 words). No uniformity |
| 11 | Contractions sound natural | "does not" → "doesn't" unless emphasis requires the formal form |
| 12 | Reader treated as peer | Capable professional, not student. No over-explaining |

---

## Gate 5: Antislop

1. Run `/antislop` on the draft
2. Fix any issues the scan identifies
3. Present the clean draft with the antislop report summary (score + any fixes applied)

---

## Presenting the Final Draft

After all gates pass, present:

1. The draft (clean, ready for editing)
2. Brief antislop summary (score, risk level)
3. Word count
4. Any remaining considerations that require human judgment (not AI judgment)
5. Ask: "Ready for your editing pass, or anything you want adjusted?"

---

## After User Edits

When the user provides edits or feedback:
- Apply the changes
- If the feedback reveals a pattern (something Claude keeps getting wrong), suggest encoding it in memory
- If the user is satisfied, offer to publish via `/linkedin-publish`

---

## Campaign Mode

When invoked by `/campaign-draft`, additional context will be pre-loaded:
- Campaign plan (objectives, audiences, themes)
- Sprint assignment (theme, post type, coordination message)
- Theme-specific source materials

In campaign mode, Gate 2 uses the campaign's "Themes to Stress / Avoid" section as an additional filter on thesis options. The campaign plan has already passed epistemic review, so agents focus on the specific post angle rather than re-validating the campaign concept.

---

## What This Skill Does NOT Do

- Publish posts (use `/linkedin-publish`)
- Create image posts or carousels
- Manage LinkedIn profile or org pages
- Handle engagement strategy
