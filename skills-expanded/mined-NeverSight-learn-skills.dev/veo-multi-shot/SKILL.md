---
name: veo-multi-shot
description: Multi-shot video generation for marketing materials, promotional content, and brand stories. Creates multiple cohesive video clips with consistent visual language that assemble into longer-form content (18-60+ seconds).
---

This skill creates cohesive multi-clip video sequences using Google Veo 3.1. Where the single-shot `veo` skill excels at loops and hero backgrounds, `veo-multi-shot` builds narrative arcs—marketing videos, brand stories, product launches, social ads.

The core innovation is **Visual DNA**: a system that locks visual parameters across all clips to ensure cohesion.

---

## When to Use This Skill

| Use Case | Duration | Clips | Example |
|----------|----------|-------|---------|
| Product Launch | ~26s | 4 | Teaser → Reveal → Detail → Context |
| Brand Story | ~34s | 5 | Establishing → Journey → Discovery → Connection → Resolution |
| Social Ad | ~18s | 3 | Hook → Message → CTA Setup |
| Explainer | ~26s | 4 | Problem → Insight → Solution → Outcome |

For single clips (loops, hero backgrounds, motion graphics), use the standard `veo` skill instead.

---

## Visual DNA System

Visual DNA defines the locked visual parameters that ensure cohesion across all clips:

### Locked Parameters (Must Match Across All Clips)

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| **Color Palette** | Primary, secondary, and accent colors | Cool blues with warm accent; earth tones |
| **Lighting Style** | Quality, direction, and mood of light | Soft diffused; hard directional; backlit |
| **Atmosphere/Mood** | Overall emotional tone | Ethereal; kinetic; contemplative; industrial |
| **Camera Energy** | Pace and movement intensity | Measured/slow; moderate; dynamic |

### Variable Parameters (Can Differ Per Clip)

| Parameter | Description |
|-----------|-------------|
| **Camera Movement** | Dolly, orbit, tracking, static, etc. |
| **Subject** | What appears in each shot |
| **Shot Size** | Wide, medium, close-up, macro |
| **Duration** | 4s, 6s, or 8s per clip |

### Visual DNA Template

```
VISUAL DNA: [Project Name]
═══════════════════════════════════════

COLOR PALETTE
  Primary:    [e.g., Deep blue #1a365d]
  Secondary:  [e.g., Slate gray #64748b]
  Accent:     [e.g., Warm amber #f59e0b]
  Shadows:    [e.g., Lifted blacks, never pure black]

LIGHTING STYLE
  Quality:    [Soft/Hard/Mixed]
  Direction:  [e.g., Side-lit with rim separation]
  Mood:       [e.g., Dramatic but not harsh]

ATMOSPHERE
  Overall:    [e.g., Premium tech, aspirational]
  Texture:    [e.g., Subtle depth haze, particle atmosphere]

CAMERA ENERGY
  Baseline:   [e.g., Measured, contemplative]
  Progression: [e.g., Can increase slightly toward end]
```

See `templates/visual-dna/` for industry-specific presets.

---

## Workflow (FOLLOW IN ORDER)

**CRITICAL**: Follow these phases sequentially. Never skip validation. Never generate without user approval. Each phase builds on the previous.

### PHASE 1: UNDERSTAND

Gather context for the entire narrative arc:

**Required Context:**
- **USE CASE**: product-launch | brand-story | social-ad | explainer | custom
- **TOTAL DURATION TARGET**: How long should the assembled video be?
- **BRAND CONSTRAINTS**: Colors, tone, existing visual identity
- **NARRATIVE GOAL**: What story are we telling? What emotion at the end?
- **ANTI-GOALS**: What must NOT appear?

**If the request is vague, ASK clarifying questions:**

```
Before I plan your multi-shot video, I need to understand:
1. What type of video? (product launch, brand story, social ad, explainer)
2. Target duration? (15-30s, 30-45s, 45-60s)
3. What story does this tell? What should viewers feel at the end?
4. Any brand colors, fonts, or visual identity to match?
5. What should the video absolutely NOT contain?
```

### PHASE 2: PLAN (NEW)

Create the shot list and define Visual DNA.

**Step 2a: Select or Create Shot List Structure**

Choose from `templates/shot-lists/` or create a custom narrative arc:

| Template | Shots | Duration | Narrative Arc |
|----------|-------|----------|---------------|
| product-launch.md | 4 | ~26s | Teaser → Reveal → Detail → Context |
| brand-story.md | 5 | ~34s | Establishing → Journey → Discovery → Connection → Resolution |
| social-ad.md | 3 | ~18s | Hook → Message → CTA Setup |
| explainer.md | 4 | ~26s | Problem → Insight → Solution → Outcome |

**Step 2b: Define Visual DNA**

Select from `templates/visual-dna/` or create custom:

| Template | Best For |
|----------|----------|
| tech-saas.md | Software products, digital services |
| luxury-premium.md | High-end products, premium brands |
| corporate.md | Enterprise, B2B, professional services |

**Step 2c: Build Shot Table**

Create a table showing all shots with their specific requirements:

```
SHOT LIST: [Project Name]
═══════════════════════════════════════

Visual DNA: [Selected template or "Custom"]

| # | Beat | Duration | Shot Size | Camera | Subject | Key Action |
|---|------|----------|-----------|--------|---------|------------|
| 1 | Teaser | 8s | Wide | Slow dolly | Environment | Establishing atmosphere |
| 2 | Reveal | 6s | Medium | Push in | Product | First glimpse |
| 3 | Detail | 6s | Close-up | Orbit | Product detail | Material beauty |
| 4 | Context | 6s | Wide | Pull out | Product in use | Emotional payoff |

Total Duration: ~26s
Estimated Cost: ~$2.00 (4 clips × $0.50)
```

### PHASE 3: CRAFT

Build prompts for ALL shots, enforcing Visual DNA consistency.

**For each shot, include:**
1. Visual DNA elements (color, lighting, atmosphere) - MUST match across shots
2. Specific camera movement for this shot
3. Subject with material specificity
4. Action in present continuous tense
5. Shot-specific context

**Prompt Template for Multi-Shot:**
```
[Camera movement], [shot size], [specific subject with material detail], [action],
[Visual DNA lighting], [Visual DNA color palette], [Visual DNA atmosphere],
[shot-specific context if needed]
```

**Example - Product Launch Shot 1 (Teaser):**
```
Slow dolly forward through sleek tech environment, abstract geometric forms
floating in mid-distance, cool blue palette with warm amber accent highlights,
soft diffused lighting with subtle rim separation, ethereal premium tech atmosphere,
mysterious anticipation building
```

**Example - Product Launch Shot 2 (Reveal):**
```
Smooth push in toward centered product silhouette gradually illuminating,
cool blue palette with warm amber accent highlights, soft diffused lighting
with subtle rim separation, ethereal premium tech atmosphere,
first glimpse of form emerging from shadow
```

Note how Visual DNA elements (palette, lighting, atmosphere) repeat exactly.

### PHASE 4: VALIDATE (MANDATORY)

Perform TWO validation passes:

**Pass 1: Single-Prompt Validation**
For each prompt, verify against `validation/prompt-checklist.md` (from veo skill):
- [ ] Single camera movement (no stacking)
- [ ] No text/UI requests
- [ ] No conflicting descriptors
- [ ] Material specificity present
- [ ] Lighting direction included

**Pass 2: Cross-Shot Continuity Validation**
Verify against `validation/continuity-checklist.md`:
- [ ] Color palette descriptors match across ALL prompts
- [ ] Lighting descriptors match across ALL prompts
- [ ] Atmosphere/mood descriptors match across ALL prompts
- [ ] Camera energy progression is appropriate (can increase, shouldn't jarring decrease)
- [ ] No jarring conceptual transitions between adjacent shots

**If validation fails**, fix issues before proceeding.

### PHASE 5: PRESENT & AWAIT APPROVAL

**CRITICAL: Present the full shot list and WAIT for explicit user approval before generating.**

Format your presentation as:

```
MULTI-SHOT VIDEO READY FOR REVIEW
═══════════════════════════════════════

PROJECT: [Name]
TYPE: [product-launch | brand-story | social-ad | explainer]
TOTAL DURATION: ~[X]s assembled

VISUAL DNA:
  Palette: [description]
  Lighting: [description]
  Atmosphere: [description]
  Camera Energy: [description]

SHOT LIST:
┌─────┬──────────┬──────────┬─────────────────────────────────────────────┐
│ #   │ Beat     │ Duration │ Summary                                     │
├─────┼──────────┼──────────┼─────────────────────────────────────────────┤
│ 1   │ Teaser   │ 8s       │ Slow dolly through tech environment...      │
│ 2   │ Reveal   │ 6s       │ Push in on product silhouette...            │
│ 3   │ Detail   │ 6s       │ Orbit around product detail...              │
│ 4   │ Context  │ 6s       │ Pull out to show product in context...      │
└─────┴──────────┴──────────┴─────────────────────────────────────────────┘

FULL PROMPTS:

Shot 1 - Teaser (8s):
[Full prompt]

Shot 2 - Reveal (6s):
[Full prompt]

[etc...]

VALIDATION: PASSED
  Single-prompt: All 4 prompts validated
  Continuity: Visual DNA consistent across all shots

COST ESTIMATE: ~$2.00 (4 clips × ~$0.50)
GENERATION TIME: ~8-16 minutes

Shall I generate all clips? [Approve / Request Changes]
```

### PHASE 6: GENERATE

Only after user approval, execute batch generation using `scripts/veo-multi-generate.ts`:

```bash
npx ts-node scripts/veo-multi-generate.ts \
  --shots "prompt1:::prompt2:::prompt3:::prompt4" \
  --durations "8,6,6,6" \
  --output ./output/ \
  --project-name "product-launch"
```

**Report progress:**
```
Generating 4 clips...
  [1/4] Teaser (8s)... complete
  [2/4] Reveal (6s)... complete
  [3/4] Detail (6s)... complete
  [4/4] Context (6s)... complete

All clips generated successfully.
Output: ./output/product-launch/
  - shot-01-teaser.mp4
  - shot-02-reveal.mp4
  - shot-03-detail.mp4
  - shot-04-context.mp4
```

### PHASE 7: ASSEMBLE (NEW)

Concatenate clips with transitions using `scripts/assemble-clips.sh`:

```bash
./scripts/assemble-clips.sh \
  --clips ./output/product-launch/*.mp4 \
  --transition crossfade \
  --transition-duration 0.5 \
  --output ./output/product-launch-assembled.mp4
```

**Transition Options:**
| Type | Use When |
|------|----------|
| `cut` | High energy, fast pacing, intentional abruptness |
| `crossfade` | Default, smooth narrative flow, most uses |
| `fade-black` | Scene changes, chapter breaks, dramatic pauses |

**Report assembly:**
```
Assembly complete:
  Output: ./output/product-launch-assembled.mp4
  Duration: 26.0s
  Transitions: crossfade (0.5s each)

Ready for review. Play the assembled video to verify flow.
```

### PHASE 8: ITERATE (if unsatisfied)

If the user is not satisfied, guide targeted improvements:

**Ask**: "What specifically didn't work?"

| Problem | Scope | Solution |
|---------|-------|----------|
| One clip doesn't match | Single shot | Regenerate that clip with refined prompt |
| Colors feel inconsistent | Visual DNA | Strengthen color descriptors, regenerate affected clips |
| Transitions feel jarring | Assembly | Try different transition type or duration |
| Pacing feels off | Duration | Adjust individual clip durations, reassemble |
| Overall mood wrong | Visual DNA | Revise Visual DNA, regenerate all clips |
| Missing narrative beat | Shot list | Add or replace a shot |

**Iteration Workflow:**
1. Identify specific issue from user feedback
2. Determine scope: single shot, subset, or all
3. Modify relevant prompts (maintain Visual DNA consistency)
4. Re-validate modified prompts
5. Regenerate only affected clips
6. Reassemble with same or adjusted transitions

---

## Key Differences from Single-Shot Veo

| Aspect | veo (single-shot) | veo-multi-shot |
|--------|-------------------|----------------|
| Use case | Loops, hero backgrounds, motion graphics | Marketing videos, brand stories, promos |
| Clips | 1 | 3-6 typically |
| Duration | 4-8s | 18-60s assembled |
| Planning | Per-clip prompt | Shot list + Visual DNA |
| Validation | Single prompt | Cross-shot continuity |
| Output | Single video file | Assembled video with transitions |
| Cost | ~$0.50 | ~$1.50-$3.00 |

---

## Quick Reference

### Shot List Selection
```
product-launch  → Teaser → Reveal → Detail → Context
brand-story     → Establishing → Journey → Discovery → Connection → Resolution
social-ad       → Hook → Message → CTA Setup
explainer       → Problem → Insight → Solution → Outcome
```

### Visual DNA Selection
```
tech-saas       → Cool colors, soft lighting, ethereal particles
luxury-premium  → Warm highlights, hard directional light, high contrast
corporate       → Neutral palette, soft diffused light, measured energy
```

### Cost Estimation
```
3 clips × $0.50 = ~$1.50
4 clips × $0.50 = ~$2.00
5 clips × $0.50 = ~$2.50
6 clips × $0.50 = ~$3.00
```

### Transition Selection
```
Most cases      → crossfade (0.5s)
High energy     → cut
Scene change    → fade-black (0.5s)
```

---

## Implementation Files

- `scripts/veo-multi-generate.ts` - Batch generation orchestrator
- `scripts/assemble-clips.sh` - FFmpeg assembly script
- `templates/shot-lists/*.md` - Narrative structure templates
- `templates/visual-dna/*.md` - Visual parameter presets
- `validation/continuity-checklist.md` - Cross-shot validation rules
- `examples/multi-shot-projects.md` - Complete worked examples

---

Remember: Visual DNA is the glue that holds multi-shot videos together. Lock it down, enforce it religiously, and the clips will feel like they belong together. Without it, you have a slideshow of unrelated footage.
