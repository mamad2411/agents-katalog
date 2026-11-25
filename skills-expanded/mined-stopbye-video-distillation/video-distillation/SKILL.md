---
name: video-distillation
description: Distill uploaded videos, keyframes, screenshots, reference images, narration scripts, and short plot briefs into a Chinese analysis package plus a Doubao-ready short-video prompt. Use when Codex needs to watch a video, summarize story beats, identify characters, lock scene/style anchors, break motion down on a continuous time axis, extract audio cues, and separate visible dialogue, first-person POV speech, and non-diegetic narration or voiceover, or convert video and image references into a controllable image-to-video prompt.
---

# Video Distillation

Produce a Chinese distillation package first, then produce the final Doubao prompt package. Treat the work as `observe -> bind identity -> distill motion -> distill sound -> rewrite for generation`.

## Routing

Choose the route before writing anything:

1. Use the full video path when the user uploads a readable video attachment in the conversation.
2. Use the keyframe path when the user provides screenshots, extracted frames, or only a few important stills.
3. Use the audio-assisted path when the user provides a narration script, subtitle text, or explicit commentary together with the video.
4. Use the director path when the user provides only reference images plus a story idea and no video to observe.
5. Stop and ask for an upload or keyframes when the user gives only a local video path that cannot actually be read in the current context.

Never pretend to have watched a video that is not accessible.

## Core Workflow

1. Lock identity first.
- If the user provides character reference images, bind them explicitly before analyzing motion.
- If there is no reference image, derive a `角色卡` from the clearest readable appearance in the video.
- Reuse the same character card for every later section. Do not silently redesign the character from segment to segment.
- When identity is uncertain, mark it in `不确定项` instead of guessing.

2. Lock scene and style anchors.
- Extract location, materials, weather, time of day, light direction, depth layers, camera grammar, and emotional tone.
- Separate what is stable across the clip from what changes moment to moment.
- Preserve mixed styles explicitly, such as `Q版角色 + 写实环境`.

3. Distill on a continuous timeline.
- Use continuous time ranges with no gaps and no jumps.
- Default short clips to `2秒` chunks. For longer clips, first group by major scene, then split each scene into contiguous smaller ranges.
- Keep time ranges readable and approximate when exact timecode is unavailable, but stay sequential.
- Around any story-turning action, switch from coarse timeline reading to dense local reading before committing to a description.

4. Distill action as choreography.
- Give every segment at least `3-5` visible action nodes.
- Describe `起始状态 -> 触发动作 -> 身体部位先后 -> 动作过程 -> 接触反馈 -> 情绪变化 -> 镜头跟随 -> 段尾状态`.
- Write movement as process, not result.
- Strengthen fragile areas: faces, eyes, hands, mouth shapes, prop contact, ground contact, turns, running, cloth, hair, and multi-character eyelines.

5. Distill sound as space.
- Separate environment sound, action sound, material sound, visible dialogue or vocalization, first-person POV speech, and non-diegetic narration or voiceover.
- Default background music to off in the final prompt unless the user explicitly wants to preserve it.
- If speech is clearly audible, retain the exact line. If it is unclear, mark it as uncertain instead of fabricating.
- If the user provides a narration script or subtitle text, bind that text as a high-priority audio anchor and keep it separate from character dialogue.
- When a readable video is available and spoken audio matters, run [scripts/transcribe_audio.py](scripts/transcribe_audio.py) first to get a transcript candidate before writing `音频拆解` and `旁白 / 解说`.

 - If a short catchphrase, name call, pet phrase, or mascot-like vocalization matters and the first ASR pass misses it, run a second targeted pass on the local time range with VAD off when appropriate and an `--initial-prompt` seeded with known names or catchphrases.
 - Treat short, high-pitched, stylized, childlike, or mascot-like speech as a high-risk audio beat. Do not conclude that the character stayed silent just because a normal ASR pass missed it.

6. Rewrite for generation.
- Convert the distilled anchors into a Doubao-ready prompt package.
- Reuse the character card, scene card, motion chain, sound chain, and continuity constraints.
- Keep the final prompt pasteable and model-friendly.

## Identity Locking

When identity matters, also read [references/identity-binding.md](references/identity-binding.md).

Use this priority order:

1. User-provided reference image or explicit name
2. Clearest readable frame from the video
3. Repeated stable costume, accessory, hairstyle, silhouette, or voice cue
4. Uncertain identity note

For each major character, capture:

- `角色名/标签`
- `绑定来源`
- `首次清晰出场时段`
- `脸型`
- `眼睛`
- `发型与发色`
- `服装结构`
- `配饰`
- `体型或头身比`
- `声音/口头禅`
- `稳定动作习惯`
- `识别置信度`

Do not convert a low-confidence identity into a high-confidence prompt anchor.

## Timeline And Motion Rules

- Use time ranges as the primary structure, not shot cuts.
- Keep every time range contiguous with the previous one.
- Give each segment one composition priority, but do not reduce the action chain to one sentence.
- Name which body part moves first when that order affects generation quality.
- Describe how the movement starts, carries through the body, and settles.
- Include weight, hesitation, rhythm, and stop states when characters walk, turn, reach, react, or speak.
- Include contact feedback for floor, mud, grass, sand, cloth, fur, props, doors, water, food, smoke, fog, or similar materials.
- For speaking beats, include pre-line pause or inhale, mouth preparation, line delivery, and post-line hold.
- Prioritize decisive story actions over decorative ambience when the two compete for attention.
- Distinguish `接触一下`, `拦住`, `抓住`, `牵着走`, `拖着走`, `带着跑`, `抱着移动`, and `松手后停止` as different motion types. Do not collapse sustained displacement into a one-frame contact description.

When motion detail matters, also read [references/action-patterns.md](references/action-patterns.md).
When contact continues across movement, also read [references/motion-continuity.md](references/motion-continuity.md).

## Audio And Narration Rules

When audio matters, also read [references/audio-reading.md](references/audio-reading.md).

- Treat visible character dialogue, first-person POV speech, narration, voiceover, off-screen commentary, and subtitles provided by the user as separate sources.
- If the camera-holder is also the speaker and the wording reflects what the POV character is saying in-scene, label it as `POV 说话`, not `旁白`.
- If a voice is not clearly tied to a visible speaking mouth, do not automatically label it as character dialogue.
- If a voice is off-screen but clearly belongs to the camera-holder reacting to the scene in real time, treat it as diegetic first-person speech rather than non-diegetic commentary.
- If narration is present, summarize its narrative role even when exact wording is unavailable.
- If the user provides exact narration text, preserve it verbatim in the analysis package and keep later prompt writing consistent with it.
- If the video has audible speech but exact transcript is not reliable, describe the type of voice and its likely function, then move exact wording into `不确定项`.
- Treat auto-transcription as evidence, not truth. Use it to recover candidate wording, then check whether it matches visible mouth sync, on-screen speaker presence, and narration timing.
- If the user explicitly tells you that a named line exists, such as a catchphrase or repeated verbal tic, treat that line as a high-priority speech anchor and verify it against timing, visible mouth movement, and partial ASR evidence before dropping it.
- When ASR recovers only a partial form of a known catchphrase, such as a repeated name without the trailing syllables, report the ASR limitation and preserve the full line only when user confirmation or source context makes the missing portion reliable.

## Critical Beat Verification

When a beat can change the story interpretation, also read [references/critical-reading.md](references/critical-reading.md).

Treat these as high-risk beats:

- an accessory being removed, handed over, or dropped
- a prop entering from the foreground near the camera
- a handhold, pull, drag, lead, or carry moment
- a destroy / hit / kick / grab / bite / eat / touch moment
- a character changing emotional direction because of a visible event
- a line delivery that anchors the whole scene

For every high-risk beat:

- Check at least three moments: just before the action, the contact or handoff moment, and the immediate result.
- Prefer dense local reading over a single representative frame.
- Verify where the object comes from before naming it. If it appears attached to the body in one moment and detached in the next, first test whether it is a wearable such as a hat, ribbon, bag, or accessory rather than a new prop.
- Verify the consequence, not just the motion attempt. Do not describe `踢塌`, `吃掉`, `递给对方`, or `接住` unless the result is actually visible.
- For pull / lead / drag beats, verify whether the contact produces continued displacement across multiple frames. Do not reduce `被牵着走了一段距离` to `被抓住一下`.
- If the object identity or action outcome still cannot be proven, move it into `不确定项` instead of overcommitting.

## Output Contract

Write the successful result in Chinese and follow [references/output-template.md](references/output-template.md).

The standard successful output order is fixed:

1. `视频内容概述`
2. `角色绑定 / 角色卡`
3. `场景设定 / 风格锚点`
4. `时间轴动作拆解`
5. `音频拆解`
6. `POV 说话`
7. `旁白 / 解说`
8. `豆包提示词`
9. `不确定项` only when needed

Keep the final Doubao prompt package structured and directly pasteable.
If a decisive beat was uncertain during reading, preserve the uncertainty in the analysis package and avoid hard-coding the wrong version into the final prompt.

## Doubao Prompt Rules

- Keep the master prompt as one paragraph.
- Put the highest-weight anchors first: resolution, frame rate, style, viewpoint, identity anchors, clarity requirements, tone, and negative constraints.
- Preserve the strongest usable details from the source instead of rewriting everything into generic aesthetic words.
- Default clarity rule: `主体清晰，面部清晰，眼睛清晰，关键接触动作清晰`.
- Default exclusions: `不要字幕，不要水印，不要UI，不要额外人物，不要无关道具`.
- Default audio rule: `背景音乐关闭，以环境声和动作声为主`.
- If narration is a core part of the source, either preserve it as `旁白` in the analysis package or explicitly state that the final prompt omits it by design. Do not silently lose it.

## Fallback Rules

- If the user provides only a non-readable local video path, ask for a video upload or keyframes and stop.
- If the source is too dark, too blurry, too occluded, or too fast to identify reliably, keep the main structure but move uncertain claims into `不确定项`.
- If the user provides only images and text, keep the same section order but use `视频内容概述` to state that the package is inferred from still references rather than direct video observation.
