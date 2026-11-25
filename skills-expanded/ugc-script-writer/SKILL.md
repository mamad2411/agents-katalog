---
name: ugc-script-writer
description: "When the user wants direct-response UGC scripts, TikTok scripts, Reels scripts, Shorts scripts, creator briefs, native-feeling organic video ads, hooks, voiceovers, product demos, testimonial-style scripts, or performance creative scripts for a DTC product. For new angle generation before scripting, use creative-angle-lab."
metadata:
  version: 1.0.0
---

# UGC Script Writer

Write direct-response UGC scripts that feel native to TikTok, Reels, and Shorts.

## Before Writing

1. Read `.agents/vibemarketer-context.md` if it exists.
2. Read `data/ugc-swipe-library/swipe-library.md` if it exists.
3. If no user swipe library exists, read `references/seed-swipe-patterns.md`.
4. If no context exists, ask for product, target customer, offer, proof, objections, and landing page.
5. If an angle is not provided, either infer one from context, read the latest `creative-angle-lab` output, or suggest using `creative-angle-lab`.
6. Ask for constraints only when needed: video length, creator persona, claim restrictions, CTA, platform, and number of variants.
7. If the user provides top organic TikTok posts, saved videos, transcripts, Creative Center examples, comments, or competitor posts, extract patterns from them before writing. Do not copy scripts, hooks, or distinctive wording.

## Reference

Load only what is needed:

- `references/script-patterns.md` for structures, hooks, and quality checks.
- `references/swipe-library.md` for the local swipe folder workflow.
- `references/seed-swipe-patterns.md` when the user has no swipe library yet.

## Scripts

Use these when the user wants to build or refresh a swipe library:

- `scripts/analyze_reference_video_gemini.py`: analyze one local reference video with Gemini and output a reusable swipe entry.
- `scripts/build_swipe_library.py`: scan a local folder of reference videos/notes and write `data/ugc-swipe-library/swipe-library.md`.

Build or refresh the library:

```bash
python3 skills/ugc-script-writer/scripts/build_swipe_library.py \
  --input-dir /path/to/local/swipe-folder \
  --output data/ugc-swipe-library/swipe-library.md
```

Add `--analyze-videos` when Gemini access is available and the user has permission to process the local videos externally.

## Swipe Library Rules

- Treat provided swipe videos as a pattern library, not training data.
- Extract hook pattern, opening frame, visual beats, pacing, emotional driver, proof mechanism, CTA style, and reusable structure.
- Never copy exact hooks, scene order, jokes, personal stories, creator identity, or distinctive wording.
- Prefer user-provided winners over built-in seed patterns.
- If no user library exists, use seed patterns as a baseline for native UGC rhythm.

## Script Principles

- Make it sound like a real person noticed a real problem.
- Lead with a specific hook, not a brand introduction.
- Use simple words and concrete moments.
- Show the product naturally.
- Build around one core idea per script.
- Include delivery notes, visual beats, on-screen text, and CTA.
- Avoid polished ad-speak, exaggerated claims, and generic hype.
- Model the rhythm of organic creator content: quick context, specific tension, visible proof, casual phrasing, and a natural next step.

## Default Output

When writing from `creative-angle-lab`, start with a compact `Source Snapshot` table. Do not stack source metadata as loose lines above the strategy read.

```markdown
## Source Snapshot

| Field | Detail |
| --- | --- |
| Source creative |  |
| Angle |  |
| Product/collection |  |
| Performance |  |
| Patterns borrowed |  |

Guardrail:
```

Then include a short `Strategy Read` explaining why the source worked and how the new scripts evolve it.

For each script:

```markdown
## Script [Number]: [Angle]
Creator persona:
Length:
Format:

### Hook
Spoken:
On-screen text:
Visual:

### Beat 1
Spoken:
Visual:

### Beat 2
Spoken:
Visual:

### Beat 3
Spoken:
Visual:

### CTA
Spoken:
On-screen text:

### Notes
- Delivery:
- Props/assets:
- Pattern source:
- Claim/compliance watchouts:
```

## Variants

When writing multiple scripts, vary the angle, not only the wording. Use formats such as:

- Problem confession
- Comment reply
- Founder or employee demo
- Customer story
- Myth busting
- Before/after routine
- Objection handling
- Comparison
- Unboxing or first use
- "Things I wish I knew"

## Quality Bar

Before finalizing, revise once for:

- Native speech rhythm.
- Specific product use moments.
- Early hook strength.
- Visual clarity.
- One clear CTA.
- Claims the brand can actually support.
