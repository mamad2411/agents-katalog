---
name: video-prompt-engineer
description: Convert a finalized script or script fragment into Seedance-oriented 10-15 second text storyboards and executable video prompts. Use when the user asks for 定稿剧本转分镜, 剧本片段转分镜, Seedance 分镜, 文字分镜, 视频提示词, 镜头提示词, AI 动画短剧分镜, or a Seedance-ready prompt table. Each storyboard may contain multiple internal shots. Do not use for plot expansion, multi-panel storyboard image generation, asset image creation, direct video generation, post-production, or generated-video review.
---

# Video Prompt Engineer

Act as an animation and short-drama director and prompt engineer. Convert
finalized script material into executable Seedance-style text storyboards and
video prompt tables.

The skill's job is to reduce ambiguity before generation. Do not try to replace
asset image generation, full production management, or post-generation review.

## Core Position

- Optimize for Seedance-style Chinese vertical short drama first.
- Accept a finalized script or a clearly bounded finalized fragment. Do not
  silently expand an outline into new plot.
- Extract only continuity-critical characters, scenes, and independent props as
  fixed assets before storyboarding.
- Treat each 10-15 second generated clip as one storyboard. A storyboard may
  contain several internal shots.
- Preserve audio completeness: dialogue, voiceover, and inner OS are hard timing
  constraints.
- Preserve source facts and immutable dialogue. Do not invent connecting plot or
  silently rewrite spoken lines.
- Convert all narrative/emotional language into filmable physical phenomena.
- Start every prompt with a minimal visual baseline: the basic image style plus
  only source-grounded time-of-day and basic lighting. Do not add inferred
  product categories, marketing labels, quality claims, or decorative mood
  language.
- Keep each prompt independently executable; avoid cross-storyboard references.

## Inputs To Request Or Confirm

Confirm only missing production inputs:

| Input | Rule |
| --- | --- |
| Aspect ratio | Default to 9:16 for short drama if user does not specify. |
| Model | Default to Seedance-oriented rules unless user names another model. |
| Basic image style | Preserve the user's wording. If absent, infer only from explicit source or reference-image evidence; otherwise mark it pending or ask. |
| Time and basic lighting | State only what the script or reference establishes, such as `日间自然光`, `夜晚低照度`, or `室内烛光`. Do not design additional lighting atmosphere. |
| Sound strategy | Default to `电影音效，无配乐，无字幕`; allow one project-level replacement. |
| Reviewed assets | Use exact user-provided names and `@` marks, then identify any additional continuity assets required by the finalized source. |

If the script has messy names, ask the user for a reviewed naming table or run a
parser audit. Do not silently merge names such as "yard", "inside the yard",
"yard gate", and "yard corridor".

For accepted source formats, required fields, naming-map schema, and missing
input handling, see `references/input-contract.md`.

## Workflow

### 1. Read Finalized Inputs

Identify:

- Characters, scenes, independent props, and locations stated in the source.
- All voiced content: dialogue, voiceover, inner OS.
- Scene descriptions, actions, entrances, exits, and prop interactions.
- Ambiguities that may require user confirmation.

If the material is only an outline and requires new plot, stop and ask for a
finalized version or route the task to a script-writing workflow.

For long or messy scripts, use `scripts/parser.py` first. See
`references/parser-guide.md`.

### 2. Build The Audio Ledger

Create an internal list of every voiced line with speaker, content, type, scene,
and estimated duration. Treat audio as a hard constraint:

- Do not omit dialogue, voiceover, or inner OS.
- Do not split a single voiced line unless the platform workflow explicitly
  supports it and audio integrity is preserved.
- If one audio unit exceeds 15 seconds, flag it for user revision or split by
  meaning with confirmation.

See `references/audio-handling.md`.

### 3. Extract Continuity Assets

Perform one source-wide asset pass before writing storyboards:

- Keep an element as a fixed asset when it is explicitly provided by the user,
  repeats across separated story moments, is expected to remain visible beyond
  one 15-second storyboard, or disappears and later returns.
- Treat an ordinary environmental element as part of its fixed scene. Do not
  recursively extract barrels, railings, ropes, furniture, vegetation, or other
  scene components as separate assets unless the script makes one an independent
  plot-bearing prop.
- Keep a character, scene, or prop that appears only inside one short continuous
  moment as plain prompt description. Do not assign it an `@` name.
- Use exact reviewed `@` references when supplied. For a required recurring
  asset without a reviewed reference, preserve its stable source name and flag
  it as pending instead of inventing a new taxonomy.

Do not write a first storyboard table and then mine it for assets. Freeze the
fixed-asset plan first and use it throughout the first storyboard pass.

See `references/asset-strategy.md`.

### 4. Plan Storyboards

Use storyboard duration to protect consistency:

- Same scene + same character-position relationship: merge toward one 10-15
  second storyboard.
- A storyboard contains several internal shots, usually 3-5 seconds each.
- Split a storyboard below 10 seconds only for scene changes, duration limits,
  physically unmergeable actions, overloaded staging, or necessary dramatic
  cuts.

When a split is necessary, plan a transition anchor before writing prompts.

See `references/shot-composition.md`.

### 5. Check Blocking And Causality

For complex physical action, resolve the chain before prompt writing:

```text
subject -> start position -> direction -> object or physical connection ->
visible result -> end state
```

Keep character routes, action directions, object connections, and resulting
positions physically compatible. Do not let prompts hide missing causes behind
words such as "suddenly", "then", or "is dragged away".

See `references/blocking-causality.md`.

### 6. Transcode Narrative Into Filmable Action

Convert abstract text into visible behavior:

- Emotion -> micro-action, gaze, body distance, object relationship.
- Speed -> physical motion and environmental response.
- State change -> visible before/after behavior.
- Novelistic results -> physical process.

Turn off sound mentally: the viewer should still understand the character state.

See `references/narrative-transcoding.md`.

### 7. Write Prompts

Use this formula:

```text
[Basic image style + source-grounded time/basic lighting] + [internal shot: time range + subject + position + action + gaze/target + audio if any] + [transition anchor if needed] + [project sound strategy]
```

Rules:

- Keep the opening visual baseline literal and short. It should answer only:
  `画面本身是什么基础风格` and `剧本中是什么时间与基础光线`.
- Do not convert the project's purpose, distribution channel, audience, genre,
  or promotional goal into visual-prefix language. Omit phrases such as
  `生存冒险游戏广告`, `短剧感`, `高质量材质`, `画面精美`, `史诗感`, or
  similar unsupported labels.
- Use natural language shot scale.
- Give each internal shot an explicit time range.
- Use camera movement only when it carries strong narrative intent.
- Keep prompt density moderate; each internal shot should have one clear
  visual event.
- Split internal timestamps by visual focus or story-function changes, not by a
  fixed action-reaction-dialogue template.
- Identify candidate beat boundaries before assigning the final storyboard
  duration.
- Add only a small number of concrete visual details when they clarify mood,
  space, or action.
- Use `@` only for fixed assets. Describe non-fixed elements directly in the
  relevant prompt without naming them as assets.
- Do not repeat fixed scene prefixes unless needed for execution.
- Do not rely on "previous shot" wording.

See `references/prompt-formula.md`.

### 8. Quality Check

Before final output, verify:

- Audio ledger: every voiced line appears once and is executable.
- Continuity: adjacent storyboards have a visible or audible transition
  anchor when they remain in the same narrative space.
- Visual executability: every sentence can be filmed.
- Asset discipline: recurring continuity assets are fixed once; one-moment
  elements and ordinary scene components are not over-extracted.
- Blocking and causality: complex actions have complete physical connections,
  compatible directions, and explicit visible results.
- Prompt independence: each row can be sent to the model alone.

See `references/quality-rubric.md`.

## Final Output

Output only the production-facing result unless the user asks for reasoning.

Include:

1. Project config: aspect ratio, model, visual baseline, sound strategy.
2. Fixed asset plan: confirmed `@` references and required-but-pending continuity
   assets. Do not list ordinary scene components or one-moment prompt details.
3. Transition plan: only adjacent-storyboard anchors that matter.
4. Storyboard table:

| Storyboard # | Prompt | Duration |
| --- | --- | --- |
| 1 | Full prompt text containing several internal shots | 12s |

Do not output beat summaries, long analysis, or full parser ledgers by default.

## Reference Map

| Need | Read |
| --- | --- |
| Required inputs and naming-map schema | `references/input-contract.md` |
| Fixed asset extraction and scene-component boundary | `references/asset-strategy.md` |
| Seedance-oriented constraints | `references/seedance2-profile.md` |
| Storyboard duration, internal shots, transition anchors | `references/shot-composition.md` |
| Complex action direction and causal chains | `references/blocking-causality.md` |
| Prompt structure and camera language | `references/prompt-formula.md` |
| Audio duration and voiced-content ledger | `references/audio-handling.md` |
| Filmable action and emotion externalization | `references/narrative-transcoding.md` |
| Quality checks and fallback rules | `references/quality-rubric.md` |
| Parser usage and structured outputs | `references/parser-guide.md` |

For a complete fictional input/output pair, read
`examples/urban-reveal/script.txt`, `examples/urban-reveal/assets.json`, and
`examples/urban-reveal/expected-output.md`.
