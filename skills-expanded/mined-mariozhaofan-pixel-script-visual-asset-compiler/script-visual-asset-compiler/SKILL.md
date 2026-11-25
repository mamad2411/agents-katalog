---
name: script-visual-asset-compiler
description: Extract production-ready visual asset plans, prompt documents, cinematic image prompts, style-amplified prompts, and optional canvas blueprints from scripts, outlines, novels, director breakdowns, or storyboards. Use when Codex needs to turn 剧本, 导演拆解, 分镜, 角色, 服装, 场景, 怪兽/生物, 载具, 色卡/视觉DNA, 关键道具, 生图提示词, 工业化提示词文档, scene continuity, same-location multi-angle images, doorway/interior/exterior scene plates, cinematic LOOK cards, LOOK transfer, 真人电影, 影视风格, 玄幻低饱和, zodiac/MBTI visual systems, style not obvious enough, canvas workflows, concept art, reference-image planning, or AI image asset requests into structured assets, scene-view prompts, shot-frame prompts, cinematic casting plates, clean image-generation prompts, and optional canvas node payloads.
---

# 剧本资产提取器

## Operating Goal

Turn a script into a reusable visual asset package. The user-facing skill name is `剧本资产提取器`; keep the technical skill ID as `$script-visual-asset-compiler` for Codex invocation compatibility.

```text
Script -> Director intake / fact levels -> Director breakdown -> Continuity memory graph -> Key subjects -> Prompt documents -> Optional canvas blueprint / CLI node payload -> Optional image generation
```

The default final output is Chinese, production-oriented, and ready for image generation. Do not only summarize the plot. Extract a stable visual system that can generate consistent character, costume, scene, prop, creature, vehicle, color/material DNA, storyboard, video-segment, and optional cinematic frame images across later storyboard or video work.

If `$cinematic-video-prompt-compiler` is available and the user also wants full cinematic shot prompts, use it as the companion skill after this asset extraction. Do not depend on it for the core asset inventory.

## Reference Files

Read only the files needed for the current task:

| File | Read when |
|------|-----------|
| `references/cinematic/integration-rules.md` | When applying cinematic quality to extracted assets, deciding asset-safe vs full cinematic treatment, or resolving conflicts between clean reference assets and dramatic frames. |
| `references/cinematic/style-amplification.md` | When the user asks for stronger stylization, live-action film stills, 真人电影, 影视风格, 玄幻低饱和, style not obvious enough, character casting plates, or visualized systems such as zodiac / MBTI. |
| `references/cinematic/scene-shot-prompt-grammar.md` | When compiling stylized scene plates, derived scene views, storyboard frames, cinematic keyframes, or unifying scene / shot prompt format from a prompt-style reference. |
| `references/cinematic/look-card-and-transfer.md` | When the user asks for LOOK CARD, LOOK transfer, style variants, named looks, or cinematic still frames. |
| `references/cinematic/presets-reference.md` | When a known style, film, show, DP-style, preset name, or "像...风格" request is named. |
| `references/cinematic/params-reference.md` | When assembling any cinematic prompt layer. |
| `references/cinematic/recipes-reference.md` | When the style request is fuzzy and no exact preset is available. |
| `references/cinematic/anti-slop-system.md` | When adding realism, anti-slop, or model-aware negative/positive constraints. |
| `references/cinematic/model-adapters.md` | When the user names GPT Image, Midjourney, Flux, SDXL, or another still-image model. |
| `references/production/director-intake-and-creative-baseline.md` | When the user wants deep director analysis, project bible, fact-level separation, creative baseline, film reference, sound/music bible, or stronger preproduction logic before asset prompts. |
| `references/production/emotion-curve.md` | When the user asks for emotional curve, rhythm map, tension graph, act-level intensity, or a director overview image/prompt before asset production. |
| `references/production/character-costume-workflow.md` | When extracting characters, costume states, dependency batches, character/creature state gates, or the default costume design sheet prompts. |
| `references/production/prop-dossier-mode.md` | When filtering key prop candidates, compiling key prop dossiers, or choosing between default 45°/back prop views and a single product-dossier prompt. |
| `references/production/asset-taxonomy-and-profiles.md` | When extracting creatures, vehicles, color/material DNA, storyboards, video segments, priorities, project profiles, or broad asset maps. |
| `references/production/prompt-document-compiler.md` | When the user wants industrial prompt documents, node-ready prompt docs, QA notes, rerun fixes, or versioned prompt packages. |
| `references/production/codex-image-generation.md` | When running local Codex image generation from compiled prompts, especially with `image_gen.py`, `gpt-image-2`, 4K PNG output, or ID-mapped image files. |
| `references/production/output-templates.md` | When the user wants the full default output structure, prompt-only output, generation manifest, or a file-ready package. |
| `references/canvas/generic-canvas-blueprint.md` | When the user asks for canvas planning, CLI node creation, LibTV, 小云雀, updream, neowow, or any generic infinite-canvas CLI workflow. |

## Input Handling

Accept scripts, outlines, dialogue, novels, shot lists, storyboards, reference images, existing prompts, or mixed materials.

When reference images are provided, assign explicit roles before extraction:

```text
@[image-1] as character identity / costume / scene / prop / palette / scene-angle reference
```

State what each reference controls and what it does not control. If a reference conflicts with the script on identity, costume, period, setting, geography, prop function, or doorway/interior/exterior relation, ask whether to preserve the reference or preserve the script.

Do not ask clarifying questions unless missing information would materially change the asset set or break spatial continuity. Make conservative assumptions and label them briefly.

## Source-of-Truth Model

Keep these layers separate:

1. `Base Truth`: script facts, confirmed references, user constraints, fact levels, and stable asset IDs.
2. `Continuity Context`: adjacent scenes, recurring locations, portals, screen direction, style lock, previous generated assets, and reference-image roles.
3. `Derived Prompts`: per-asset and per-view image prompts derived from Base Truth plus Continuity Context.
4. `Cinematic LOOK Layer`: optional camera, lens, light, color, texture, mood, realism, and anti-slop treatment. It can enrich prompts but never override Base Truth.
5. `Production Prompt Document`: optional versioned document containing prompt body, parameters, QA notes, and rerun fixes.
6. `Canvas Blueprint / CLI Payload`: optional vendor-neutral plan for creating canvas nodes through an already available CLI.
7. `Submission Payload`: the final concise prompt and selected reference images sent to an image generator.

Do not let generated images silently rewrite Base Truth. If a generated asset contradicts the script, mark it as a candidate that needs acceptance, revision, or rejection.

Use fact levels when the script is long, ambiguous, style-sensitive, or intended for serious production:

- `剧本事实`: explicitly stated in the source.
- `强推断`: supported by multiple source clues; state the basis.
- `导演提案`: necessary production specificity not written in the source; offer one best-fit option.
- `待定冲突`: a blocking choice that would materially change assets, continuity, or story meaning.

Never present a director proposal as script fact. Once the user confirms a proposal, it becomes project truth for downstream prompts.

## Workflow

1. Read the script for story function, not just nouns. Identify who changes, where action happens, and which objects move the plot.
2. If the task needs a deep production pass, read `references/production/director-intake-and-creative-baseline.md` and establish fact levels, project bible, creative baseline, and optional sound/music principles before writing final asset prompts.
3. Build a director breakdown:
   - premise and genre
   - time period and world rules
   - scene geography and recurring locations
   - character power relationships and visual contrast
   - recurring motifs, prop logic, and reveal moments
4. Build a compact storyboard map:
   - scene order and story beats
   - which characters, costumes, locations, props, and scene states appear in each beat
   - what must stay visually consistent across beats
5. Build a continuity memory graph:
   - characters, costumes, scenes, props, and their stable IDs
   - scene zones, entrances, exits, doors, windows, hallways, stairs, vehicles, counters, beds, tables, altars, screens, or other fixed landmarks
   - screen-left/screen-right axis, movement direction, doorway direction, and camera-parent relationships when a scene needs multiple views
6. Extract key subjects into stable IDs:
   - `CHR-01` characters
   - `CST-01` costumes or costume states when one character has multiple looks
   - `CRE-01` creatures, monsters, animals, mechanical beasts, mounts, mutated life, or non-human entities
   - `SCN-01` canonical scenes / locations / location states
   - `SCN-01_VIEW-01_PRIMARY` / `SCN-01_VIEW-02_REVERSE` derived scene views from the same canonical scene
   - `PRP-01` plot props, weapons, tokens, letters, devices, vehicles, artifacts, repeated objects, or visually iconic objects
   - `VEH-01` vehicles, ships, cars, aircraft, mecha, bikes, carts, or other transport systems
   - `DNA-01` color palette, material DNA, lighting DNA, and visual bible assets
   - `STB-01` storyboard grids or sequence boards
   - `VID-01` video segment plans only when video prompting is requested
   - `SHOT-01_FRAME-01` cinematic keyframes only when the user requests frames with characters, posters, or storyboard stills
7. Decide dependencies and confirmation gates. For complex projects, read `references/production/character-costume-workflow.md` and do not produce downstream costume/state prompts before required upstream identities or accepted references exist.
8. Decide the output mode:
   - prompt-only for Codex/GPT chat
   - production prompt documents
   - canvas blueprint only
   - CLI command plan
   - execute an already available canvas CLI only when explicitly requested
9. Decide the cinematic treatment:
   - clean asset reference only
   - cinematic costume design plate / 真人电影服装设计图 when the user wants styled character costume assets
   - scene plate with cinematic LOOK
   - full cinematic frame prompt
   - LOOK CARD first because the style request is fuzzy
   - LOOK transfer from a named preset/style
10. Write image-generation prompts or prompt documents for each subject. Each prompt must be usable without reading the whole script.
11. If the user asks to generate images or create canvas nodes, execute in dependency order: project profile / DNA, character identity text and costume design plates, creatures/vehicles/props, scene master plates, derived scene views, storyboard/keyframes, video segments.

## Extraction Rules

Characters:

- Extract named characters and unnamed characters with visual or plot importance.
- Include visible age range, body type, facial features, hair, expression baseline, posture, social class, and visual temperament only when supported by the script or required for generation.
- Include every costume state that matters to continuity: everyday outfit, uniform, disguise, damaged state, ceremonial outfit, wet/bloody/dusty state, etc.
- Keep identity separate from clothing so a character can be reused with multiple costumes.
- Default image deliverable is a `CST-*` costume design sheet, not character three-view output. Keep `CHR-*` as the identity and performance lock; bind each generated clothing asset to one `CST-*`.

Scenes:

- Extract every distinct location that appears on screen, including repeated locations with materially different states, such as day/night, destroyed/intact, crowded/empty, clean/rainy.
- Treat a scene as a spatial asset, not a mood label. Describe layout, scale, zones, entrances/exits, portal relationships, fixed landmarks, material surfaces, lighting source, atmosphere, color palette, and objects fixed in the set.
- Scene asset prompts must be location plates with no people.
- Do not describe characters, acting, or dialogue in scene asset prompts.

Props:

- Extract props that drive plot, reveal identity, repeat across scenes, create conflict, mark status, or need continuity.
- Include invitation letters, weapons, heirlooms, tokens, phones, contracts, medicine, jewelry, masks, devices, vehicles, ritual objects, special containers, and clue objects.
- Describe scale, material, color, wear, marks, inscriptions, damage, mechanism, and the prop's story function.
- Do not include generic furniture or background clutter unless it becomes important in action, blocking, recognition, or spatial continuity.

Broader production assets:

- Extract `CRE-*` when the script contains monsters, animals, mechanical beasts, mounts, unknown life forms, mutated organisms, or creature-like threats.
- Extract `VEH-*` when a vehicle or transport system has visual continuity, action importance, world-building value, or generation difficulty.
- Extract `DNA-*` when a project needs a shared color palette, material system, lighting rule, visual bible, or profile lock before generating multiple assets.
- Extract `STB-*` when the user needs a storyboard grid, beat board, contact sheet, or sequence-level visual plan.
- Extract `VID-*` only when the user asks for video prompt planning. Do not start final video generation unless explicitly requested.

## Cinematic Treatment Rules

Cinematic style is a derived prompt layer. It must improve image quality without corrupting asset extraction.

Use `references/cinematic/integration-rules.md` when deciding how much cinematic treatment to apply. In short:

- Character and costume reference assets stay on a clean solid-color background by default. Add realistic skin, hair, textile, material, and optical clarity, but do not add film sets, smoke, random foreground, dramatic action, or lens flare.
- If the user asks for 真人电影, 影视风格, 风格化, 定妆照, 正面全身图, 服装设计图, or says the character image is not stylized enough, read `references/cinematic/style-amplification.md` and `references/production/character-costume-workflow.md`; compile a cinematic costume design plate unless the user explicitly requests an actor/casting portrait.
- Prop reference assets stay on a clean solid-color background. Add material fidelity, wear, construction details, and scale logic, but do not add hands or scene environments.
- Scene assets can use full cinematic LOOK treatment because they are environment plates. They must still be empty, geographically readable, and consistent across derived views.
- Shot frames can use the full cinematic still-image layer only when the user requests character-containing frames, posters, keyframes, or storyboard images. Label them as `SHOT-*`, not `SCN-*`.

When a generated result feels like concept art, game CG, generic fantasy, or weakly styled output, treat it as a prompt defect. Strengthen the next prompt with `style_strength`, concrete visual DNA, live-action medium anchors, practical set/costume/material language, and explicit exclusions for illustration, anime, game render, and plastic CGI.

When the script contains abstract systems such as zodiac, MBTI, personality panels, reputation scores, divine rank lists, or social-media heat, convert them into visual grammar: geometry, costume construction, light behavior, spatial motifs, symbols without readable text, material patterns, and composition. Do not leave them as labels.

When the user names a style, preset, film, show, DP-style, or says "像...风格", read `references/cinematic/presets-reference.md` and transfer the LOOK layer only. Preserve script facts, asset IDs, clean-background requirements, no-people scene plates, and spatial continuity.

When the user gives a fuzzy style request, read `references/cinematic/recipes-reference.md` and `references/cinematic/look-card-and-transfer.md`. Output a LOOK CARD first unless the user explicitly asks to proceed automatically.

When assembling cinematic scene or shot prompts, read `references/cinematic/scene-shot-prompt-grammar.md` to keep prompt bodies in the unified order: shot/view type, subject/action or empty location state, environment, fixed composition, immutable style keywords, and concise limits. Then read `references/cinematic/params-reference.md`, `references/cinematic/anti-slop-system.md`, and `references/cinematic/model-adapters.md` as needed. Use anti-slop as a compact, subject-aware clause, not a long generic negative prompt.

## Prompt Document and Canvas Modes

Default to `prompt_only` unless the user asks for a canvas, nodes, CLI execution, or a project board.

Use `references/production/prompt-document-compiler.md` when the user wants structured prompt documents. Keep these layers separate:

- `Prompt Body`: only model-facing image/video prompt text.
- `Parameters`: aspect ratio, model, quality, reference images, canvas section, node metadata.
- `Production Notes`: QA checklist, rerun fixes, version suggestions, operator instructions.

Do not put production notes, CLI commands, node metadata, or rerun instructions inside the model prompt body.

Use `references/canvas/generic-canvas-blueprint.md` for canvas workflows. Support these modes:

- `prompt_only`: output asset prompts only.
- `blueprint_only`: output canvas plan and node content, do not run CLI.
- `cli_command_plan`: output safe commands or JSON payload plan, do not execute.
- `execute_cli`: run a detected/provided canvas CLI only when the user explicitly asks to create/update canvas nodes.

Canvas planning must be vendor-neutral. LibTV, 小云雀, updream, neowow, and custom canvas tools are all treated as CLI canvas targets when a usable executable and command syntax are available. Do not hard-code one vendor.

CLI safety:

- Never install a canvas CLI as part of this skill.
- Never read, print, modify, or write API keys or access tokens.
- Only check executable existence and help/version output when needed.
- If CLI syntax is unknown, stop at `cli_command_plan` or ask for the tool's node-creation syntax.
- If no CLI is available, still return the asset list, prompt documents, and optional canvas blueprint.

## Scene Continuity and Multi-View Rules

Create a scene master plate for every important location. Add derived views only when the script needs them.

Create derived scene views when any of these are true:

- the same location appears in multiple beats or episodes
- action crosses a door, gate, window, car door, elevator, stairwell, corridor, or threshold
- the story needs inside/outside, room/corridor, upstairs/downstairs, front/back, reverse shot, or over-the-shoulder geography
- a reveal depends on what is visible from one angle but hidden from another
- a chase, confrontation, search, entrance, exit, or eavesdropping beat depends on path continuity
- later image/video generation explicitly needs consistent scene references beyond the master plate

Use this view hierarchy:

```text
SCN-01_MASTER                  canonical wide view / spatial truth
SCN-01_VIEW-01_PRIMARY          primary story-facing angle
SCN-01_VIEW-02_REVERSE          reverse angle, if needed
SCN-01_VIEW-03_INSIDE_TO_OUT    inside looking outside through the threshold, if needed
SCN-01_VIEW-04_OUTSIDE_TO_IN    outside looking inside through the threshold, if needed
SCN-01_VIEW-05_APPROACH_PATH    path/entry/corridor/stair/vehicle approach view, if needed
SCN-01_DETAIL-01                key fixed landmark or prop zone, if needed
```

Do not generate all view types by default. For each scene, output only the views needed by the script and give a short reason for every included derived view. If a view type is unnecessary, omit it instead of listing it with empty content.

For every multi-view scene, output a `场景连续性卡`:

- `空间母版`: one-sentence canonical scene identity.
- `平面关系`: describe left/right/front/back, depth, routes, and zones in words.
- `固定锚点`: doors, windows, furniture, signage, lamps, cracks, stairs, counters, vehicles, trees, skyline, or other objects that must not move between views.
- `门槛/连接点`: for door scenes, define what is on both sides, door swing direction, handle side, wall material, floor transition, and what can be seen through the opening.
- `光线逻辑`: source, direction, time, weather, spill from adjacent space, and material reaction.
- `风格锁`: lens feel, color palette, texture, realism level, art direction.
- `视角树`: root/master view and child views, with a short reason for each derived view.

Scene view prompts must explicitly preserve the master scene:

```text
继承 SCN-01_MASTER 的空间结构、材质、门窗位置、固定锚点、光线方向和风格；只改变相机位置与可见区域。
```

Doorway / threshold prompts must lock both sides:

```text
门内与门外属于同一连续空间，门框、门把手方向、地面材质交界线、墙面颜色、光线溢出方向保持一致；从门外看见室内的同一锚点，从门内看见门外的同一走廊/街道锚点。
```

For same-scene multi-angle prompts:

- Generate the canonical master wide plate first.
- Use the master plate as the preferred scene reference for derived angles when an image tool supports references.
- If no tool reference is available, repeat the scene continuity card in concise form inside each derived prompt.
- Keep characters out of all scene asset images unless the user explicitly asks for shot frames instead of scene plates.
- Do not let a derived angle introduce new doors, windows, furniture, props, lighting sources, signage, or weather that contradict the master plate.

Keep scene plates separate from shot frames:

- `SCN-*` outputs are empty environment/location assets.
- If the user asks for a frame with characters, create a `SHOT-xx_FRAME-*` or storyboard/keyframe prompt that references `SCN-*`, `CHR-*`, `CST-*`, and `PRP-*`; do not relabel it as a scene asset.
- If a location is normally crowded, first create the empty scene plate. Treat crowd/extras as a separate background performer group or shot-frame layer only when needed.

## Output Structure

Use a compact structure by default: director breakdown, storyboard asset map, continuity graph, project profile/DNA, cinematic LOOK layer, assets by type, optional prompt documents, optional Canvas Blueprint, gaps/assumptions, and QA summary.

When the user wants only prompts, omit long analysis but keep asset IDs, scene continuity cards, and prompts. When the user wants the full template, prompt-only format, or manifest, read `references/production/output-templates.md`. When the user wants a file artifact, save the result as Markdown and include a manifest mapping IDs to generated image filenames.

## Image Prompt Requirements

All prompts must be self-contained. Each prompt must name:

- subject ID and subject name
- visual identity or set identity
- costume / material / color / texture
- view angle and framing
- lighting and background requirement
- continuity anchors
- negative constraints

Highest-priority real-light clause:

```text
最高优先级: 真实肌肤质感, 真实光影效果和阴影高光, 统一光线来源, 遵从真实光线; 不要展示全部细节, 暗部干净无噪点, 让部分信息自然沉入阴影。
```

Use this clause for all cinematic character, scene, prop, creature, vehicle, and shot-frame prompts. For people, emphasize real skin pores, subtle imperfections, natural hair, and skin translucency. For non-human assets, apply the same rule as material realism, real shadow/highlight behavior, and a single motivated light source. Do not brighten every surface just to reveal details.

Character asset prompts must include:

- clean solid-color or seamless studio background
- one `服装设计图 / Costume Design Sheet` prompt for each required `CST-*` costume state
- the linked `CHR-*` identity text lock: age range, body proportion, posture, social class, temperament, and hair/face constraints only as needed to preserve costume fit and continuity
- a default sheet layout that prioritizes clothing information: front outfit view, back outfit view, key fabric/trim/accessory details, silhouette notes, and material behavior in one image
- no mandatory character three-view set, no mandatory headshot, and no full acting pose unless the user explicitly asks for them
- same identity, same body proportions, same costume, and same left/right asymmetric anchors across all panels/views in the sheet
- costume-state ID such as `CST-01`; create one costume design prompt per required costume state
- no extra characters, no text, no watermark, no logo

If the user explicitly asks for actor views, casting plates, front view, back view, headshot, or three-view output, output only the requested views and keep the ID/view name stable. If the user asks for 真人电影 / 影视风格, use a cinematic costume design plate by default: one real actor or neutral fit model only when needed for clothing fit, full-scale practical costume construction, real skin/hair/fabric/metal/jade/leather texture, low-key clean studio background, visible project visual DNA in costume seams, embroidery, wear, accessories, or material contrast.

Scene asset prompts must include:

- wide panoramic establishing view for the master plate
- no people, no crowds, no character silhouettes
- clear readable geography: foreground, midground, background, entrances, exits, portals, key set pieces, fixed landmarks
- lighting source, time of day, weather, material reaction, and color palette
- for derived views, explicit inherited anchors from the master plate and what changes in camera position
- the unified scene prompt-body order from `scene-shot-prompt-grammar.md` when the user asks for stylized scene images, cinematic scene plates, or a prompt format reference has been merged
- the selected LOOK layer when the user asks for cinematic quality or a style has been inferred
- no text labels, no UI, no watermark

Prop asset prompts must include:

- clean solid-color background
- `45°侧视图` prompt showing front/side form and important details
- `背视图` prompt showing rear construction and continuity marks
- material, scale, wear, mechanism, unique marks, and story-use details
- no hands unless the user asks for scale reference; no text labels, no watermark

Creature asset prompts must include:

- species or construction logic
- side, front, top-down, and 3/4 view when a full design sheet is requested
- scale, anatomy/mechanical structure, surface material, signature visual memory point, functional story elements
- same creature across all views; no random species drift

Vehicle asset prompts must include:

- side, front, top, and 3/4 view when a full design sheet is requested
- silhouette, scale, movement system, cockpit/control interface, materials, decals/customization, damage/weathering
- same vehicle across all views; no toy-like or generic 3D render drift

Color/material DNA prompts or specs must include:

- color names, functions, and optional hex codes when useful
- material system
- lighting DNA
- inheritance notes for characters, scenes, props, creatures, vehicles, storyboards, and video segments
- forbidden drift

Shot-frame prompts must include:

- `SHOT-*` ID and the referenced `CHR-*`, `CST-*`, `SCN-*`, and `PRP-*` IDs
- one clear visual center when multiple characters or objects appear
- scene moment, framing, foreground depth if needed, camera/lens, lighting, color/texture, mood, realism, and anti-slop
- the unified shot prompt-body order from `scene-shot-prompt-grammar.md`: shot type, subject/action, environment, fixed composition, immutable style keywords, concise limits
- continuity inheritance from the scene master and character/prop assets
- no contradiction with clean reference assets; a dramatic frame does not replace CHR/SCN/PRP asset truth

Storyboard and video prompts must include:

- referenced asset IDs
- sequence or segment function
- continuity lock for character, costume, scene, props, and lighting
- panel list for storyboard grids or timecoded action timeline for video segments
- no final video generation unless explicitly requested

Canvas node payloads must include:

- node name, node type, asset reference, section, action, generate_now flag, and content source
- prompt body separated from parameters and QA notes
- node index table in final response when canvas output is created or planned

Use concise negative constraints at the end:

```text
限制: 纯色干净背景, 单一主体, 无文字, 无水印, 无logo, 无额外人物, 不改变角色身份/服装/比例
```

For scenes, replace the pure-background constraint with:

```text
限制: 无人物, 无人影, 无群众, 无文字, 无水印, 无logo, 不出现角色, 不出现与时代/剧情无关的物件, 不改变场景固定锚点/门窗位置/光线方向/材质关系
```

## Prompt Compression Priority

Final prompts should be complete but not bloated. Preserve guidance in this priority order:

1. asset ID, subject name, and required view name
2. character identity / scene master anchors / prop form anchors
3. view-specific camera position and what changed from the master view
4. doorway, route, screen direction, or continuity constraints that would visibly break if omitted
5. the highest-priority real-light clause: real skin/material texture, unified motivated light source, realistic shadows/highlights, clean noiseless shadow falloff, and partial detail hidden in darkness
6. style, lighting, color, material, and atmosphere
7. concise negative constraints

If a final prompt becomes too long, remove decorative adjectives and low-impact mood language before removing spatial anchors, ID locks, or reference roles.

## Optional Image Generation

If the user asks to generate images:

1. Confirm the requested scope only when the count is unclear or excessive.
2. Generate separate images for each required view.
3. In Codex/local execution contexts, read `references/production/codex-image-generation.md` when the user asks for actual files, 4K output, `gpt-image-2`, or `image_gen.py`.
4. For Codex 4K portrait PNG generation with an available `image_gen.py`, default to model `gpt-image-2`, size `2160x3840`, quality `high`, output format `png`, and ID-based output paths under `output/imagegen/`.
5. Do not add Codex image-generation commands to GPT Builder behavior. GPT versions should output asset prompts, prompt documents, and optional canvas blueprints, not local execution commands.
6. Use dependency order:
   - character identity text locks and `CST-*` costume design plates
   - `SCN-xx_MASTER` scene master plate
   - derived scene views using the master as reference when possible
   - prop views
7. Keep each generated image mapped to its ID and view name, for example `CST-01_design`, `SCN-01_MASTER`, `SCN-01_VIEW-03_INSIDE_TO_OUT`, `SCN-01_VIEW-04_OUTSIDE_TO_IN`, `PRP-01_45deg`, `PRP-01_back`. Use `CHR-01_front`, `CHR-01_back`, or `CHR-01_head` only when the user explicitly asks for those actor views.
8. If an image-generation tool supports reference images, use character references for identity only, costume references for clothing only, scene references for environment/geometry only, and prop references for object form only.
9. After generation, report the output paths or visible images with the ID map.

## Quality Gate

Before finalizing, verify:

- Every named or visually important character has identity and costume coverage.
- Every scene appearing in the script is represented, including changed states of the same place.
- Important repeated or threshold-based scenes have a master scene plate and only the derived views the script actually needs.
- Doorway/interior/exterior prompts preserve both sides of the same connection.
- Scene plates and character-containing shot frames are not mixed under the same `SCN-*` asset.
- Every plot-driving or repeated prop is included.
- Characters, costumes, scenes, scene views, and props have stable IDs and cross-reference the storyboard map.
- Creatures, vehicles, color/material DNA, storyboard grids, and video segments are included when story-relevant or requested.
- Cinematic LOOK choices are treated as derived prompt layers, not script facts.
- Character/costume prompts include `CST-*` costume design sheets by default; actor front/back/headshot views appear only when explicitly requested.
- Scene prompts are no-people location plates; master and derived views do not contradict each other.
- Style requests are not left as abstract labels: prompts include `style_strength`, live-action or medium anchors, recurring visual motifs, and model-safe exclusions for concept art / game CG when relevant.
- Prop prompts include 45° side view and back view.
- Shot-frame prompts, when requested, are labeled as `SHOT-*` and reference existing CHR/CST/SCN/PRP IDs.
- Stylized scene and shot prompts follow the unified prompt-body grammar without mixing QA notes, canvas metadata, or CLI plans into the model prompt.
- Clean character and prop reference prompts are not polluted by cinematic background action, random foreground objects, or dramatic scene lighting.
- Fuzzy cinematic style requests produce a LOOK CARD first unless the user explicitly asks to proceed automatically.
- Named-look transfer preserves the user's script facts and only transfers camera, lens, light, color, texture, mood, and anti-slop behavior.
- Industrial prompt documents keep prompt body, parameters, QA notes, and rerun fixes separate.
- Canvas Blueprint is generated before any CLI node creation.
- CLI execution is skipped unless the user explicitly requests canvas node creation/update and a safe executable plus command syntax are available.
- No API keys, access tokens, or credential values are read, printed, modified, or written.
- Prompts are clean, literal, and image-generation ready, not vague mood labels.
- Prompts preserve the highest-priority real-light clause: real skin/material texture, one motivated light source, realistic shadow/highlight behavior, clean noiseless dark areas, and selective detail with natural shadow loss.
- Reference-image roles and conflicts are explicit when references exist.
- Guidance is prioritized, not bloated: preserve at most the highest-impact continuity constraints inside each final prompt.
- No invented prop, costume, scene, or spatial relation is presented as script fact; assumptions are labeled.
