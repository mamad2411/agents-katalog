---
name: ai-video-shots
description: Choose and use paid AI video generators (Google Veo / Gemini Omni, Kling, Runway, Seedance, Hailuo, Luma) to add a few realistic shots to a code-made video — which tool for what, prices per second as of 2026-10-01, cost estimate before spending, image-to-video from our own still, and how to blend clips into a HyperFrames video. Use when Alexey mentions Veo, Kling, Sora, Runway, Seedance, AI video, AI-generated footage or realistic shots. For detailed Seedance prompting, see the community seedance-2.0 skill (github.com/Emily2040/seedance-2.0).
---

# AI video generators (for a few realistic shots)

Code (HyperFrames, see `video-studio`) is still the backbone: it renders exact words, numbers, UI and
brand colours perfectly. AI generators are for 2–4 short realistic shots code can't draw (a tired
recruiter at a desk, hands on a keyboard, an office, a video call). Never for text, numbers, logos
or UI.

Full research with sources, tagged OFFICIAL / 2ND / UNCONFIRMED, checked 2026-10-01:
`references/tools-research.md`. Prices change monthly: re-check the
official pricing page before quoting a cost.

## Money rule (always)
Every generation costs money. Before any call: say the tool, clip count, seconds, resolution and the
total in dollars (×3–5 for re-rolls), then wait for the owner's yes. Free tiers usually add a
watermark or forbid commercial use, so they're for look tests only. Use a generator's API only
with a key the owner has set up; never sign up for anything on their behalf.

## Which one (as of 2026-10-01)
| Need | Pick | Price (per second of video) |
|---|---|---|
| Default, scriptable via API, image-to-video | Google **Veo 3.1** via the Gemini API | Lite $0.05 (720p) / $0.08 (1080p, 8 s clips only); Fast $0.12 (1080p) |
| Most realistic people, strong image-to-video | **Kling 3.0 Pro** (e.g. via fal) | ~$0.11–0.17 |
| Newest Google model, edits by conversation, up to 4K | **Gemini Omni Flash 1.1** | ~$0.10 (720p), ~$0.15 (1080p) |
| Cheap look tests | Veo 3.1 Lite, Hailuo H3 (~$0.08, 768p) | |
| Strong motion, multi-shot | **Seedance** (ByteDance) | ~$0.23 at 720p (2nd-hand figure) |
Gone or not usable: **OpenAI Sora** (app closed April 2026; API removed 2026-09-24). No "Veo 4"
exists. Open models (Wan 2.2, LTX) need an NVIDIA GPU; without one, free hosted GPUs are
too slow to be practical.

Example estimate: 4 clips × 4 s at 1080p ≈ $2–3 on Kling 3.0 Pro or Veo 3.1 Lite (Veo Lite bills
8 s per 1080p clip). With re-rolls, budget $8–15. Start with the same 2 prompts on two tools
(~$1–2), pick the winner, then do the rest.

## Workflow that keeps the brand
1. Design the shot's first frame as a still in our style (`hyperframes snapshot` of a scene, or a
   frame from the video) and generate **image-to-video** from it. Use last-frame conditioning
   where the tool offers it, so the clip ends where the next code scene begins.
2. Prompt the feeling and the camera, not every detail (the community seedance-2.0 skill explains this well):
   subject, action, camera move, light, mood, "no text, no logos".
3. Keep clips 2–4 s. Conform them with FFmpeg: 30 fps, 1920×1080 (or crop for square), BT.709.
4. Grade towards the brand: lift shadows towards your background colour, tint highlights with your accent colour, the
   same film grain as the code scenes (4–6 %) on top, so AI and code shots read as one film.
5. Bring each clip into HyperFrames as a `<video>` layer (see the `media-use` and `hyperframes`
   skills in the project's `.claude/skills`), muted; sound stays our music and SFX.
6. Download results straight away: Veo files are deleted from Google's server after 2 days.

## Traps
- Text inside AI clips comes out garbled: never ask for signs, screens with words, or logos.
- Hands and fingers on keyboards still fail often; frame them loosely or out of focus.
- No real people's likeness, no real brands. Check the tool's rules on realistic people.
- Many 2026 blog posts are out of date (they still say "use Sora 2"). Trust the official pricing
  and model pages, with a date.
- Watermarked or non-commercial free-tier clips must never end up in a posted video.
