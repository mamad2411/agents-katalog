---
name: annotated-video-production
description: Plan, produce, resume, or audit editorial annotations for recorded conversations, including source screenshots, demos, and pull quotes. Routes the surrounding production cycle from cut selection to release; owns overlay decisions and review. Use for an annotated episode or its cue/asset review, not standalone download, transcription, thumbnail, upload, or motion-graphics tasks.
---

# Annotated video production

Show what the conversation is about. This skill owns editorial annotation and its review cycle; neighboring skills own acquisition, transcription, rendering mechanics, packaging, and publication. Overlay guidance is developed here. Other stages are deliberately thin routes, to expand only when actual production work establishes new requirements.

## Enter or resume at any stage

Start with the user's requested outcome and existing artifacts. Do not force an episode through completed or irrelevant stages. Recover the current cut/timebase, selections, assets, approved treatment, latest output, and outstanding feedback. Ask only for missing information needed for the next action.

Keep a short stage record in the existing project notes or manifest, not a new workflow framework:

- Current stage and requested stopping point.
- Paths to source cut, transcript, cue board, asset manifest, preview/final render, and release record, where they exist.
- Decisions/approvals and unresolved items; next concrete action.

At a handoff, pass these artifacts and scope to the receiving skill, then record its result. If inputs change, revisit only affected work: a new cut invalidates cue timing; an asset replacement affects its layout/render/QA. Preserve original footage and review versions.

## Routing and ownership

Load only the skill needed for the current action. Resolve named skills from the installed catalog; inspect their current instructions rather than copying their mechanics here.

| Stage / entry request | Owner and handoff |
| --- | --- |
| Acquire or compare cuts | `download-video` or source-specific downloader acquires media. Here, compare duration, opening, audio, continuity, and representative footage; record chosen cut and timebase. |
| Transcript / editorial context | `transcribe-anything` for ASR; `podcast-publishing-assistant` for chapters and publishing copy. Use transcript to locate topics, then verify speaker and timing against footage. |
| Research / select / capture overlays | This skill; produce selected cues and verified assets. |
| Design / preview / full render | This skill owns treatment and acceptance. Retain the existing renderer; use `design-apps-with-imagegen` for requested exploration. Route custom HyperFrames composition work through `hyperframes`/`general-video` when that engine is appropriate. |
| Audit existing annotated output | Enter directly at encoded-result review below; return findings without assuming a rerender. |
| Titles / descriptions / thumbnails | `podcast-publishing-assistant` for copy; `latent-space-thumbnail-director` for LS artwork. Pass episode facts, series identity, chosen hooks, real-face references, and official brand assets. |
| Upload / metadata / release | Relevant YouTube upload/API skill owns execution and account/channel verification. Pass exact output, metadata, channel, and authorized visibility. Record returned video ID and verified state. |

`media-transform` owns platform-transfer and generic media pipelines. For an annotation-led episode, use this skill as the coordinator and call atomic skills directly; do not nest two orchestrators or repeat their checkpoints. Standalone adjacent requests go directly to their owner. Do not edit neighboring skills merely to route this one.

Stop at the requested deliverable. Planning does not start a render; preview approval does not imply publication. “Don't rerender” permits inspection but stops render work. Existing approval remains valid within its scope.

## Research and select

Build a broad chronological board across the whole episode, with reasonably even coverage of new points and substantial monologues. Avoid filler quotas. Search the speaker's own posts, demos, and articles first; then exact primary sources; then useful external explanations. Use intentional pull quotes where the argument itself merits emphasis.

For this user's research, use X `filter:follows`, selected high-signal lists, and [Latent Space AINews](https://www.latent.space/s/ainews). Later references are acceptable: retain dates without repetitive chronology warnings.

Each candidate needs time, speaker/topic, source link, exact proposed visual, why it helps, and approximate hold. Let the user cut the broad board; import selection exports and preserve their edits. A URL alone is not a resolved visual.

## Capture the selected thing

Read [capture-and-cues.md](references/capture-and-cues.md) when resolving assets or reconciling a cue manifest.

Prefer original attached images and playable source media. Inspect the saved asset. A successful download, plausible filename, or attribution does not establish that the requested image/chart/demo is present. A photo-only post failing a video downloader still has a photo to recover. Check existing local originals before repeating research.

Choose demo segments showing action/results, not intros, branding, or teasers. Scroll articles with pauses on useful passages. A still-image pan does not substitute for a functioning demo.

After reasonable recovery attempts, omit unavailable inserts and report them; continue the rest. Escalate only an explicitly indispensable visual or a gap that prevents the requested outcome. Never silently replace a requested visual with prose.

## Frame for watchability

Sample representative camera setups and use placement heuristics; avoid exhaustive tracking for mostly static footage.

- Protect the active speaker's eyes/mouth. Listener faces, hands, and table space may be covered. Reposition or end an insert when camera cuts invalidate placement.
- Make useful detail large enough to read, including square/tall assets. Use available side, lower, and upper space, or a cutaway/split view. Fit the card to the asset; crop irrelevant margins instead of white letterboxing or stretching.
- Focus on the reason the asset was chosen. Highlights encompass complete words/lines with padding and track scrolling. A focused crop or subtle emphasis often beats a heavy rectangle.
- Use concise source/author attribution and a readable URL/domain. Keep full links in the source record/description. Use LS branding without redundant oversized logos.
- Use selective, accurate, naturally attributed pull quotes. Do not turn available photos, charts, or interfaces into generic title/body cards.
- Keep research caveats internal. Avoid repeated “DISCUSSION SUMMARY,” “PRODUCT PAGE EXCERPT,” or “not a benchmark/private workspace” labels. If context matters, use a brief natural attribution/date or a better asset.
- Use perceptible, restrained entrances/exits and requested sound cues. Listen under dialogue at normal volume; lack of clipping alone does not prove the sound works.

## Preview quickly, then extend

Default: render the first ten minutes (or requested interval) and provide a lightweight board of the remaining exact assets/compositions. Use stills or short low-resolution previews for later treatments when useful or requested; do not require another comprehensive motion-preview round.

Inspect the preview at playback and small-screen size; play its motion and audio. Apply feedback about framing, margins, emphasis, and timing throughout. Full-render approval extends the approved quality and variety, not permission to fill later sections with text fallbacks. Reconcile selected visuals with actual renderer inputs before rendering.

## Review the encoded result

For audits or completed renders, read [render-review.md](references/render-review.md). Inspect every insertion in the final encoded file; play moving inserts, transitions, and their audio. Sample untouched conversation rather than requiring continuous whole-episode playback.

Compare selected visual → captured source → rendered output. Repair systematic defects across affected cues when fixes are authorized. An audit-only request ends with findings. A production request ends when its requested output is verified, with omitted inserts reported. Additional creative alternatives are optional, not completion gates.

Deliver versioned output, updated cue/stage record, and concise findings. Packaging preserves series identity first (for example `High Taste Testers: [hook]`); publication proceeds only within the user's authorized scope. A revised asset or local render is not a changed live upload.
