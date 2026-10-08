---
name: ai-influencer-prompt-builder
description: 'Generates a foundational image prompt for an AI influencer character from five inputs — age, gender, ethnicity, niche/personality, and a defining visual quirk. Use whenever the user wants to design an AI influencer, virtual creator, synthetic character, or reusable visual identity.'
---

# AI Influencer Prompt Builder

Turns five basic inputs into a complete, foundational image prompt for a consistent AI influencer character — the kind you'll regenerate across dozens of future posts, videos, and sponsor placements. Because the character has to survive many separate generations, the prompt needs identity anchors baked in from the start, not just a nice one-off description.

This is different from a one-off image prompt: this builds a repeatable foundational identity meant for reuse across many future generations.

---

## Step 1: Collect the five inputs

| Input | What it controls |
|---|---|
| **Age** | Bone structure, skin texture stage, styling era, cultural reference points |
| **Gender** | Presentation, styling codes, grooming details |
| **Ethnicity** | Facial structure, skin tone, hair texture, features — be specific, not vague |
| **Niche / personality** | Everything downstream: wardrobe, setting, energy, camera style, platform |
| **Defining visual quirk** | The one memorable, repeatable detail that makes the character recognizable at a glance |

If any input is missing, ask for it directly — don't silently guess ethnicity, age, or gender, and don't default to a generic look. If the user gives a rough one-liner, extract whatever's already there and ask only for what's genuinely missing.

---

## Step 2: Read the visual-language reference before writing

The bundled `references/influencer-visual-language.md` covers:
- Why AI influencers read as fake, and the specific imperfection markers that fix it
- Lighting language for influencer content
- Camera and angle language native to how influencers are actually shot
- Niche-by-niche visual codes
- How to write consistency anchors that survive regeneration

---

## Step 3: Build the foundational prompt

**Formula:**
`[Core Identity] + [Face & Features] + [Defining Quirk] + [Skin & Imperfection Realism] + [Niche-Coded Styling] + [Lighting] + [Camera & Angle] + [Setting] + [Style Signature]`

**Key principles:**
- Lead with age, ethnicity, and gender in one clean identity clause — don't scatter them across the prompt.
- Describe facial features with enough anatomical specificity that the model can't drift between generations: eye shape and color, brow shape, jaw line, nose bridge, lip fullness, cheekbone prominence.
- Give the defining quirk its own sentence. It should be the single most specific, describable detail — a gap tooth, a scar above the left brow, a freckle cluster on the left cheek, a septum ring, an asymmetric dimple. Vague quirks don't survive regeneration; anatomically specific ones do.
- Always include 2–3 imperfection markers from the reference doc. This is the single biggest lever for avoiding the uncanny-valley render look.
- Match lighting and camera language to how the niche is actually shot. Don't default to generic studio photography.
- End with a style signature that locks in "shot by a real person on a real device," not a commercial render.
- For turnaround sheets, also capture silhouette anchors: hair length and texture, how the hair falls at the nape, build, posture, and any profile- or rear-visible mark.

---

## Step 4: Output format

Always output these sections:

**1. Foundational Character Prompt**
One clean, paste-ready prompt block.

**2. Consistency Anchors**
3–5 bullets listing the exact phrases that must be repeated verbatim in every future prompt for this character. These are the forward-visible identity DNA.

**3. Silhouette Anchors**
2–4 bullets listing the exact phrases that hold the character from profile and rear views: hair length and texture, hairline and nape behavior, build, posture, and any rear-visible marks.

**4. Niche Alignment Notes**
2–3 sentences on why these visual choices read as authentic within the chosen niche, not generic or stock.

**5. What Can Vary**
A quick list of what's safe to change shot-to-shot without breaking character consistency: outfit, setting, lighting mood, expression, and pose.

When the bundled Pi extension is available, call `influencer_save` after the foundational prompt is agreed so the full prompt, consistency anchors, silhouette anchors, and style signature persist. When it is not available, preserve those sections in a character sheet and repeat them verbatim in future prompts.

---

## Tool notes

- **Higgsfield**: pair the foundational prompt with a Soul Character or Reference Element so the identity locks across generations instead of re-describing the character from scratch every time.
- **Nano Banana / Gemini Image, Midjourney (`--cref`)**: feed the Consistency Anchors and Silhouette Anchors back in on every subsequent generation — this is what keeps the face and profile from drifting.
- **Seedance 2.0**: use the foundational image as the first-frame reference for video generation rather than re-prompting the character from text alone. Text-only regeneration is where identity drifts fastest.

---

## Quick decision guide

```
User gives all 5 inputs clearly       → build directly
User gives a partial one-liner        → ask only for what's missing, in one message
User wants to tweak an existing char  → keep Consistency Anchors and Silhouette Anchors fixed, vary only the requested section
User wants several characters at once → run the workflow separately per character, never blend traits
User wants a turnaround sheet        → use one reference-sheet image recipe with front, left profile, right profile, rear, and close-up panels
```
