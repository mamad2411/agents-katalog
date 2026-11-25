---
name: short-video-director
description: Generate Chinese prompt packages for image-to-video short-video models with strong character consistency, camera continuity, sensory detail, and shot-level controllability. Use when the user provides 1-2 reference images, describes a protagonist, environment, or short plot beat, or asks for a Doubao-ready short-video prompt, storyboard, scene breakdown, or image-guided video prompt.
---

# Short Video Director

Produce a Chinese short-video prompt package that is directly usable in an image-to-video model. Treat the task as directing a controllable sequence, not writing decorative copy.

The goal is not to write pretty copy. The goal is to output a prompt that the model can execute more stably.

## Core Principles

- Lock high-weight anchors before plot beats.
- Keep viewpoint, character identity, props, and spatial relations stable.
- Describe motion as a continuous process, not just a result.
- Reinforce fragile areas: face, eyes, hands, mouth shape, contact moments, fast motion, and camera transitions.
- Make every segment answer: what is seen, how it moves, why it moves, what happens on contact, and what is heard.

This prompt style should feel like `导演口述分镜 + 声音设计 + 负面约束`, not a string of decorative adjectives.

## When To Use

Use this skill when the user wants any of the following:

- A Chinese prompt for an image-to-video or short-video model
- A storyboard-like prompt with time segments
- A prompt package based on 1-2 reference images
- A prompt that emphasizes character consistency, action clarity, camera continuity, or audio layering
- A Doubao-ready short-video prompt

## Workflow

### 1. Route the input first

Classify the request into one of these modes before writing:

- `1 image + idea`: infer whether the image controls the character, the environment, or both. State the assumption only if it materially affects the result.
- `2 images`: default to `image 1 = character reference`, `image 2 = environment reference` unless the user states otherwise.
- `character image + environment image + short plot`: preserve the plot, and mainly expand camera, material feedback, and sound detail.
- `text-only plot`: infer only the missing controls that materially improve stability. Do not invent new lore or plot points.

If the request involves heavy movement, multi-character interaction, POV camera, or prop contact, also read [references/action-patterns.md](references/action-patterns.md), [references/camera-grammar.md](references/camera-grammar.md), and [references/failure-modes.md](references/failure-modes.md).

If the user asks for a specific visual look, mixed medium, or genre style, also read [references/style-presets.md](references/style-presets.md).

Always read [references/output-template.md](references/output-template.md) before producing the final answer.

### 2. Lock four anchor groups before story beats

Put the highest-weight anchors at the beginning of the master prompt.

#### Visual anchors

Define:

- resolution and frame rate
- character style
- environment style
- line and edge quality
- lighting direction and light quality
- color direction
- clarity requirements for subject, face, eyes, and key contact actions

If the user mixes styles, make the boundary explicit. Example: `Q版 2D 角色 + 电影级写实环境`, with one short note on how they coexist visually.

Do not use vague words like `电影感` or `高级感` without breaking them into light, lens feel, material depth, color temperature, and focus priority.

#### Camera anchors

Define:

- one main viewpoint only unless the user explicitly wants cuts
- camera stability rule
- composition priority
- whether the clip feels like a single shot, pseudo one-take, or a lightly segmented sequence

Prefer stable spatial relations and limited camera grammar. Avoid unnecessary camera complexity.

#### Character anchors

If images are supplied, bind them explicitly in the output.

Define:

- body proportion
- stable face and eye traits
- hair silhouette and hair color
- costume structure, accessories, shoes, and socks when relevant
- signature expression and movement traits
- speech pattern or catchphrase if relevant

#### Sensory anchors

Define:

- layered ambience
- action and material sounds
- tactile feedback from surfaces and props
- air feel, temperature, and weather cues
- overall emotional tone

### 3. Identify the control axis before writing shots

Determine the request's main control axes:

- viewpoint axis: first-person, third-person, or fixed observer
- emotion axis: healing, playful, tense, comedic, intimate, daily-life, and so on
- motion axis: static observation, light follow, chase, fast action, or prop interaction
- performance axis: micro-expression driven, action driven, prop driven, or dialogue driven

Then identify fragile points and reinforce them in the prompt:

- multi-character interaction
- turning, running, chasing, or sudden directional changes
- handing, eating, touching, carrying, or passing props
- lip-sync and short vocalizations
- POV handheld motion
- contact with sand, grass, water, cloth, fur, or other reactive materials

### 4. Convert the request into a causal shot chain

Write each time segment as a process, not a result summary.

Each segment should contain this chain:

`start state -> trigger action -> motion process -> contact or feedback -> emotional reaction -> camera follow -> held landing state`

Every segment should clearly describe:

- character position
- what moves first
- how the motion transfers through the body
- what gets touched and how it reacts
- facial change and eyeline
- prop state
- camera movement
- composition focus

Keep one composition priority per segment.

Do not write:

- `她跑过去踢倒城堡`

Prefer:

- `她先转身、迈步加速、镜头跟着她的身影转过去、跑到城堡前抬脚、脚尖碰到沙堡后沙体塌落四散、对方看到结果后情绪爆发`

### 5. Write segment language like a storyboard, not a caption

For each time segment:

- use concrete camera terms such as `特写`, `中近景`, `平视`, `俯视`, `跟拍`, `轻微摇移`, or `镜头定住`
- if it is POV, state what the lens sees first, how it turns, and whether the handheld motion is subtle
- show how the action starts, not just the finished state
- show how the expression changes in layers, not with a single adjective
- show contact feedback clearly: collapse, wobble, drag, compression, cloth friction, hair movement, ground response
- keep one dominant composition focus per segment

### 6. Layer audio into every segment

Background music is off by default unless the user explicitly requests it.

For each segment, include:

- ambience
- action sound
- material feedback
- dialogue or vocalization if relevant

Keep dialogue short, sync-friendly, and easy to stage visually.

If the user supplies a catchphrase, repeat it at the key action beat instead of mentioning it only once in the role description.

Do not write flat audio like `有海浪声`. Prefer layered phrasing like `轻柔海浪声、微风拂沙声、远处脚步由近到远`.

### 7. Apply model-friendly defaults

Unless the user specifies otherwise, default to:

- `4K`
- `24fps` or `30fps`
- one main viewpoint
- stable camera
- one-take or pseudo one-take feel
- a total duration of `6 seconds`
- three segments: `0-2秒`, `2-4秒`, `4-6秒`
- clear subject, clear face, clear eyes, clear key contact action
- no subtitles, no watermark, no UI, no extra characters

### 8. Apply negative constraints on purpose

Avoid all of the following unless the user explicitly wants a stylized break:

- drifting face shape, eye design, hairstyle, accessories, or costume structure
- body proportion drift
- POV suddenly changing to third-person
- axis confusion or unexplained direction flips
- random shake, random defocus, or unnecessary cuts
- teleporting actions or results with no initiating motion
- broken hand shapes, bad finger counts, or twisted limbs
- prop floating or clipping
- unsynced lip motion
- expression popping without transition
- wrong eyelines in multi-character scenes
- extra people, extra limbs, extra props, subtitles, watermark, UI, or garbled text
- character style and environment style feeling incompatible
- vague aesthetic words without supporting camera, light, and material detail

### 9. Self-check before responding

Check all of the following:

- the opening already contains the highest-weight anchors
- the main viewpoint is explicit
- image binding is explicit when images are present
- each segment contains a visible action process, not just a result
- each segment includes audio
- adjacent segments preserve pose, eyeline, prop state, and camera orientation
- material and contact feedback are concrete enough
- the ending has a visible aftertaste instead of stopping abruptly

## Output Rules

- Write in Chinese.
- Do not output analysis or chain-of-thought.
- Keep the result directly pasteable into the user's video model.
- Follow the exact section headers in [references/output-template.md](references/output-template.md).
- Keep `帮我生成一个视频：` as one continuous paragraph.
- Put negative constraints at the end of the master prompt paragraph unless the user explicitly requests a separate negative section.
- Add `补充说明：` only when you made a material assumption about image binding, duration, viewpoint, or mixed style handling.
