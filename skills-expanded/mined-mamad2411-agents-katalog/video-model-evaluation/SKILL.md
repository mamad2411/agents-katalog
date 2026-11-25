---
name: video-model-evaluation
description: Fairly compare AI video-generation models (or any generative model where output quality is easy to cherry-pick) using a controlled five-clip test — same shot brief, source image, duration, aspect ratio, and evaluation rubric across every model before comparing cost or quality. Use this whenever the user is choosing between multiple AI video models (or evaluating any generative model against alternatives), asks "which video model should I use," wants to benchmark generation quality, or is at risk of picking a tool based on a single hand-picked demo clip rather than a controlled comparison. Pairs with claude-code-tooling's open video-generation model list (Wan 2.2, LTX-Video, HunyuanVideo, CogVideo, Mochi).
---

# Video Model Evaluation: The Five-Clip Test

Source: "AI Power User Stack — 5 open AI video models that can replace a production day" carousel (@zhiprompts). A controlled comparison method for picking a video-generation model based on usable footage, not a hand-picked demo.

## The core problem this solves

Every video model's own showcase reel is a hand-picked best-case example — comparing showcase reels tells you which team curates best, not which model performs on your actual use case. "Same brief. Same edit." is the discipline: hold everything constant except the model, then compare.

## The four steps

| Step | What to do |
|---|---|
| **1. Brief** | Write one shot brief and use it identically across every model — subject, action, camera movement, style. Also fix the source image (if image-to-video), duration, and aspect ratio before generating anything. Changing any of these between models invalidates the comparison. |
| **2. Generate** | Run every model against the exact same brief/source/duration/aspect ratio. Generate more than one clip per model if the model has meaningful output variance, and say so — a single generation per model still risks a lucky/unlucky draw. |
| **3. Edit** | Apply the same edit (cuts, color, pacing) to every model's output before judging it — an ungraded clip and a graded clip aren't comparable, and the point is to see how the raw output holds up after the same real-world post-production pass it would get in production. |
| **4. Score** | Score every clip against a rubric fixed *before* generation, not chosen after seeing results — otherwise the rubric quietly drifts toward whichever model happened to look best. |

## Building the rubric before generating anything

Fix specific, checkable criteria in advance — examples, adapt to the actual use case:

- Motion coherence (does the subject stay consistent frame to frame, or drift/warp)
- Prompt adherence (does the output actually match the brief, not just "AI video quality" in general)
- Usable duration (how much of the clip is actually usable footage vs. degrading toward the end)
- Artifacts (visible warping, flicker, inconsistent lighting)
- Generation cost/time (only compare this *after* quality scoring — a cheap model that fails the brief isn't a contender regardless of price)

## Output conventions when using this skill

- State the fixed brief, source image, duration, aspect ratio, and rubric explicitly before generating anything — if any of these is still undefined, the test isn't ready to run, the same discipline `night-shift-canvas` applies to workflow readiness.
- Don't let cost or star count substitute for the actual quality comparison — check `claude-code-tooling`'s model list for star count/license/activity as a starting filter, but the five-clip test is what actually decides fit for the specific use case.
- Report results as a comparison table (model × rubric criteria), not a prose recommendation — the whole point is a defensible, re-checkable comparison, not a vibe-based pick.
- This methodology generalizes beyond video models — the same "same brief, same rubric, fixed before generating" discipline applies to comparing any generative model (image, audio) where a vendor's own demo reel is not a reliable signal.

## Related skills in this repo

- **claude-code-tooling**: Lists the five open video-generation model repos (Wan 2.2, LTX-Video, HunyuanVideo, CogVideo, Mochi) this skill's test methodology applies to.
- **night-shift-canvas** (procedure): Same "define everything before running, or it isn't ready" discipline, applied to a scheduled workflow's readiness instead of a model comparison's fairness.
- **design-review-audit**: A similar fixed-checklist discipline (spacing/hierarchy/contrast/consistency) applied to a finished design build instead of a generative-model comparison.

## Notes

Source: "AI Power User Stack — 5 open AI video models that can replace a production day" carousel (@zhiprompts).
