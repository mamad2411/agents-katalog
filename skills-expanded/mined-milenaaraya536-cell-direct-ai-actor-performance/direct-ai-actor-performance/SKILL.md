---
name: direct-ai-actor-performance
description: Turn a short plot, emotional situation, or character moment into a production-ready prompt for realistic live-action AI video performance. Use when the user wants director-style acting instructions, cinematic human acting, subtle micro-expressions, emotional beats, subtext, eye-line and breathing direction, image-to-video or text-to-video actor prompts, or help making an AI-generated person perform like a believable real actor. Trigger on requests such as "导演式表演提示词", "真人演技", "微表情", "让AI会演戏", "表演指令", "演员调度", "acting prompt", or "direct this scene".
---

# Direct AI Actor Performance

Convert the user's simple plot into a self-contained, model-agnostic video prompt that directs a believable screen performance. Prefer behavioral specificity over emotional adjectives.

## Required references

Read [references/acting-direction.md](references/acting-direction.md) for every request. Read [references/examples.md](references/examples.md) only when the input is unusually sparse, involves multiple actors, or needs calibration. Apply [references/evaluation-rubric.md](references/evaluation-rubric.md) silently before returning the final answer.

## Default behavior

- Accept one sentence of plot as sufficient input.
- Do not ask follow-up questions when sensible cinematic assumptions can complete the scene.
- Infer missing character, relationship, location, preceding event, subtext, duration, shot size, lighting, and emotional arc.
- Default to one continuous 8-second shot, vertical 9:16, chest-up close shot, restrained film acting, naturalistic lighting, and no spoken dialogue.
- Match the user's language. Provide an English version only when requested or when the named generator works materially better with English prompts.
- Keep the final prompt tool-neutral unless the user names a generator. When a generator is named, adapt terminology without inventing unsupported controls.
- Use only original, fictional, public-domain, or authorized likenesses and voices. If the request uses a real person's identity without clear authorization, replace it with a fictional character and state that adjustment briefly.

## Workflow

### 1. Find the dramatic engine

Infer all of the following from the plot:

- **Given circumstances:** what happened immediately before the shot.
- **Objective:** what the character wants from the other person or situation.
- **Obstacle:** why the character cannot simply act or speak.
- **Stakes:** what may be lost.
- **Subtext:** the thought the character refuses or fails to say.
- **Turn:** the instant the internal strategy changes.

Never expose this as an essay. Use it to design visible behavior.

### 2. Choose a playable performance arc

Build 3-5 chronological beats. Each beat must contain:

1. an external focus or trigger;
2. an internal decision;
3. a visible but restrained physical response;
4. a transition into the next beat.

Express emotion through eye focus, blink timing, breath, swallow, jaw tension, lips, facial asymmetry, posture, hand pressure, weight shift, and reaction delay. Avoid stacking every signal at once.

### 3. Direct for screen realism

- Let thought precede movement.
- Insert small pauses and incomplete impulses.
- Use asymmetry and imperfect timing.
- Keep blinks, breathing, balance, and muscle tension continuous.
- Reserve the strongest visible change for the turn.
- Prefer containment, substitution, or concealment over overt emotional display.
- Give the actor a playable action such as reassure, conceal, test, resist, persuade, or protect; do not merely command "be sad" or "look angry".

### 4. Coordinate camera and performance

Choose one camera concept that supports the acting instead of competing with it. Specify framing, lens character, movement, depth of field, lighting motivation, background activity, and continuity. Keep the camera still or nearly imperceptibly moving for subtle acting unless the plot requires instability.

### 5. Add failure prevention

Write concise negative constraints targeting:

- exaggerated theatrical acting;
- instant tears or emotion appearing without buildup;
- synchronized eyebrow-mouth movement;
- face, identity, wardrobe, age, or lighting drift;
- eye wandering, lip twitching, frozen breathing, plastic skin, or morphing;
- random gestures, extra people, camera shake, cuts, or background changes;
- dialogue or lip-sync when none was requested.

### 6. Run the silent quality check

Use the evaluation rubric. Revise before answering if the performance lacks subtext, escalation, a turn, physiological continuity, or shootable timing.

## Output format

Return the following sections and nothing else unless the user asks for explanation:

### 导演判断

Write one compact line containing the inferred subtext and performance strategy.

### 完整生成提示词

Write one copy-ready prompt containing:

1. format and visual realism;
2. character and setting continuity;
3. preceding event, objective, obstacle, stakes, and subtext;
4. time-coded performance beats;
5. camera, lens, light, depth, and motion;
6. physiological and identity continuity;
7. ending pose that can hold naturally.

For an 8-second shot, target 250-450 Chinese characters or 180-320 English words. Use enough detail to control performance, not decorative prose.

### 负面约束

Provide one compact comma-separated block that can be pasted into a negative prompt field or appended to the main prompt.

### 建议参数

State duration, aspect ratio, shot type, camera motion, and recommended generation mode. Prefer image-to-video when identity consistency matters.

### 挑片标准

Give exactly three observable checks for selecting the best generation.

## Special cases

- **Multiple actors:** assign each actor a separate objective, beat sequence, eye-line, reaction timing, and physical territory. Make reactions overlap naturally without simultaneous robotic movement.
- **Dialogue:** direct the intention beneath each line, pauses, breath placement, listening, and post-line reaction. Keep spoken text short enough for the duration.
- **Comedy:** preserve human reaction timing; avoid explaining the joke in the prompt.
- **Horror:** build anticipation through attention, listening, and incomplete perception before overt fear.
- **Romance:** use proximity, interrupted eye contact, breath, and restraint; avoid generic smiling and beauty-shot behavior.
- **Action:** preserve weight, balance, fatigue, anticipation, impact, and recovery; do not sacrifice physical causality for speed.
- **Reference image:** preserve facial geometry, age, skin texture, hair, wardrobe, body proportions, and scene lighting. Direct expression changes without redesigning the subject.

