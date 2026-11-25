---
name: every-format-from-one-edit
description: Derives content-aware 9:16, 1:1, and 4:5 siblings from one finished composition — same edit, every platform, no re-editing. Triggers on "make this vertical too", "I need this for TikTok and LinkedIn", "every aspect ratio", "square version of this", "resize for Reels", "one video, all platforms", "port this edit to Shorts".
---

# Every format from one edit

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

You finish ONE edit; you get back its siblings for every platform — 9:16 for
Reels/TikTok/Shorts, 1:1 and 4:5 for feeds — derived content-aware from the master,
subject-tracked rather than letterboxed, each judged and rendered on its own. The edit decisions
are made once; the formats are a job, not a re-edit.

## Before you start

Confirm which master and which target platforms before setup. When the first tool call
approaches and CueFrame isn't connected, load **`cueframe-connect`** and follow it once.

Then straight to deriving — this whole job is minutes when the master is good.

## Inputs

- **The master composition** (required): a finished, approved edit — find it via
  `list_compositions` if the user doesn't have the id. If the master isn't done, finish it first
  (this skill multiplies quality AND flaws).
- **Target aspects**: default all three siblings — 9:16, 1:1, 4:5. The documented derive lane
  starts from a 16:9 master.
- **Per-platform tweaks**: default none — determinism is the point. Take an explicit ask (e.g.
  "shorter for TikTok") as a separate edit on the derived sibling.

## Workflow

Use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md)
for each affected sibling. Check motion as well as layout where the new crop changes visibility.
A correction to one sibling does not require rendering the master or the other unchanged siblings.

1. **Verify the master is actually done.** It passed its class checklist, its audio was
   decided, its render was approved. Deriving from a draft ships the draft's flaws four times.
2. **Derive each sibling.** `derive_composition` per target aspect — the reframe is
   content-aware: it tracks the subject into the new frame instead of letterboxing. Each
   sibling is a real composition you can edit independently afterward; the master is never
   touched.
3. **Audit every sibling on real pixels — required, not optional.** `preview_frame` each
   sibling at t=0, hook-end, and each card's midpoint; describe each still. What to look for
   per aspect: the subject's head fully in the vertical frame; cards and captions inside the
   safe area (no critical copy in the outer ~8%); no beat where the tighter crop lost the thing
   the beat exists to show.
4. **Fix per-sibling, surgically.** Where a crop or card misbehaves, `apply_composition` on
   THAT sibling — nudge a `setCropIntents` segment, resize a card for the narrower frame
   (re-apply its `clip.setKeyframes` if you replace the card). Don't
   re-edit the story; the story is the master's.
5. **Confirm the audio carried.** The master's decided audio — bed, ducking, beat-aligned cuts
   (`materializeGrid` markers), or its intentional silence — rides into each sibling. Verify
   the bed is present and the silence decision, if any, still holds; the sibling's delivery
   note repeats it. If a sibling needs a different bed, `search_resources` honoring the brand
   kit's `musicMood` and swap it on that sibling only.
6. **Inspect each sibling as its own artifact.** Use `score_composition` only when useful for broader review and within budget, with the
   master's vision as `editorialIntent`. Changing aspect ratio does not change the approved editorial intent, pacing or acceptance criteria. Fix worst-first to
   meet the applicable acceptance criteria.
7. **Render each approved sibling.** `create_render` → `wait_job (kind:"render")` per
   composition. One final render per approval; iterate with previews.

## What good looks like

Use the relevant [craft review questions](../video-craft-standards/SKILL.md) and the [preview workflow](../cueframe-compose-loop/references/preview-workflow.md). Judge the brief's actual intent, visual relationships, timing and sound; format suggestions do not override the requested treatment. The cross-cutting rules in the [format standards](../video-craft-standards/references/format-standards.md) apply to every sibling. Apply the original brief at the new dimensions: aspect ratio alone does not impose a social-reel hook or pacing, and derivation changes the frame, never the bar.

## Delivering

The last message is a manifest, never "done":

- Every sibling's render link, labeled by aspect and platform, and where each lives (project +
  composition id — the master's id too, since it stays the source of truth).
- The master's attribution list (it covers all siblings — same assets).
- The intentional-silence note, restated once, if the master chose silence.
- Any sibling-specific edits you made (which crop nudged, which card resized) so future master
  edits know what to re-check after re-deriving.
