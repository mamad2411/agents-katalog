# Skill: Generate Content

## Trigger
User provides a theme and asks for content. Supports multiple formats.

**Trigger patterns:**
- "Write about {theme}" → LinkedIn (default)
- "Write a newsletter about {theme}" → Newsletter format
- "Write a thread about {theme}" → Twitter/X format
- "Write about {theme} for all formats" → Newsletter first (pillar), then distribute
- "Create a carousel about {theme}" → Carousel format

## Format Parameter

| Format | Target | Key Reference |
|--------|--------|---------------|
| `linkedin` (default) | 800-1200 characters, 3 angles | `references/linkedin-practices.md` |
| `newsletter` | 1500-3000 words, 3 angle variants | `references/newsletter-practices.md` |
| `twitter` | 7-10 tweets, 280 chars each, 3 angle variants | `references/twitter-practices.md` |
| `carousel` | 5-10 slides, 1 point per slide | `references/carousel-practices.md` |
| `all` | Newsletter first (pillar), then run `skills/distribute/SKILL.md` | `references/format-adaptation-matrix.md` |

## Process

### Step 1: Load references (tiered)
- **Always load:** `references/generation-angles.md`
- **Format-specific:**
  - LinkedIn: `references/linkedin-practices.md`
  - Newsletter: `references/newsletter-practices.md` + `experts/ogilvy-headlines.md` + `experts/brunson-storytelling.md`
  - Twitter: `references/twitter-practices.md`
  - Carousel: `references/carousel-practices.md`
  - All: `references/format-adaptation-matrix.md` + `references/newsletter-practices.md` (start with pillar)
- **Load if research done:** The research brief and gap map from the research step
- **Load for critique:** `references/rubber-duck-escalator.md`

### Step 2: Load Brain context
Read `data/brain/pmm_brain.json` and extract:
- For drafting: `synthesized_mental_models`, `argumentation_playbook`, `insight_generation_patterns`
- For voice: `voice_profile_sourav` (differentiators, forbidden_patterns, visual_signature)
- For critique: `quality_bar_examples`

### Step 3: Generate 3 drafts
For each angle (contrarian, framework, story), generate in the target format:

**LinkedIn (default):**
1. Follow the structure in `references/generation-angles.md`
2. Use the assigned evidence anchors from the research brief
3. Write in Sourav's voice (data-driven, specific, teardown-oriented, startup-focused)
4. Think at Pierri's depth (nuanced, anti-dogmatic, framework-rich)
5. Apply LinkedIn best practices from `references/linkedin-practices.md`
6. Target 800-1200 characters

**Newsletter:**
1. Follow `references/newsletter-practices.md` structure (opening → bridge → deep section → practitioner callout → landing → P.S.)
2. Use Epiphany Bridge (from `experts/brunson-storytelling.md`) for story-led angles
3. Minimum 3 evidence anchors, 2 newsletter source cross-references
4. Generate 5 subject line variations (Ogilvy headline principles)
5. Target 1500-3000 words

**Twitter/X:**
1. Map each angle to a thread type (see `references/twitter-practices.md`)
2. Write hook tweet first — compress best hook to 280 chars
3. One idea per tweet, tweet 2 = strongest insight
4. Vary rhythm, include line breaks within tweets
5. Verify EVERY tweet ≤280 characters
6. Target 7-10 tweets

**Carousel:**
1. Extract framework/progression from each angle
2. One key point per slide, max 3-4 lines
3. Cover slide with adapted hook, close slide with CTA
4. Follow visual design rules from `references/carousel-practices.md`
5. Target 5-10 slides

**All formats:**
1. Generate newsletter first (pillar)
2. Run `skills/distribute/SKILL.md` to atomize into LinkedIn + Twitter + Carousel

### Step 4: Critique each draft (Rubber Duck Escalator)
Run all 5 phases from `references/rubber-duck-escalator.md`:
1. MIRROR → PROBE → CHALLENGE → ILLUMINATE → CRYSTALLIZE
2. Each phase sees prior phase results (cascading context)
3. Score 1-10 per phase
4. If any phase < 8: rewrite addressing failures, protecting passes
5. Max 3 iterations before surfacing to user with notes

### Step 5: Present to user
For each draft that passes (or after max iterations):
- Show the draft
- Show the scorecard (5 phase scores + composite)
- If any phase failed, show the critique notes
- Ask: APPROVE / TWEAK / SKIP

### Step 6: Generate visual
**LinkedIn framework posts:** If the post contains a framework, matrix, comparison, progression, or structural concept → follow `skills/visual/SKILL.md` to produce a visual brief and image.

**Carousel format:** Generate visual brief for all slides using carousel-practices.md design rules. Produce Pillow-based images.

**Newsletter:** No visual unless explicitly requested.

**Twitter:** No visual (text-only threads perform best).

## Output Format
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANGLE 1: CONTRARIAN REFRAME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Draft text]

SCORECARD
Mirror: 8 | Probe: 9 | Challenge: 8 | Illuminate: 8 | Crystallize: 9
Composite: 8.4 | Status: PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANGLE 2: FRAMEWORK / MENTAL MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Draft text]

SCORECARD
Mirror: 8 | Probe: 8 | Challenge: 9 | Illuminate: 8 | Crystallize: 8
Composite: 8.2 | Status: PASS

VISUAL BRIEF
Layout: [Pattern]
Title: [Header]
[Sections with colors]
[Generated image]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---
**See also:** `skills/research/` (runs before generate) → `skills/critique/` (runs after generate) → `skills/distribute/` (atomizes pillar output)

---
**See also:** `skills/research/` (runs before generate) → `skills/critique/` (Rubber Duck gate) → `skills/distribute/` (atomize to other formats) | `skills/_index.md` for full data flow
