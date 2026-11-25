---
name: seedance-2.5-prompts
description: Write and adapt Seedance 2.5 video prompts using the repository's original prompt catalog, timeline structure, reference workflows, and review rules. Use when a user asks for a Seedance 2.5 prompt, wants to improve one, or needs product-lock, motion-style, voice, music-sync, multi-shot, camera, lighting, or audio guidance.
---

# Create Seedance 2.5 prompts

1. Identify the subject, goal, format, aspect ratio, duration, resolution, and available image, video, or audio references.
2. Choose the closest workflow and catalog pattern below.
3. Preserve the pattern's chronological scene-beat structure while replacing subject, setting, action, camera, lighting, audio, and dialogue with request-specific facts.
4. Return a copy-ready prompt in a fenced text block plus a short technique note.
5. Never promise deterministic output; flag placeholders, permissions, claims, disclosures, reference rights, and review needs.

## Formula

```text
[0-Xs: shot, subject, and first observable action] -> [Xs-Ys: camera move and physical micro-action] -> [Ys-end: reveal, reaction, or final state] + [lighting and environment across the timeline] + [dialogue, ambience, and sound cues aligned to each beat].
```

## Operating rules

- Write beats in chronological order and keep every beat feasible within the requested duration.
- Name one environmental detail, one physical micro-action, and one sound cue; prefer concrete physical detail over vague adjectives.
- Put spoken words in quotation marks and describe ambience or music separately.
- When a reference already shows a face, product, room, or style, do not re-describe it; prompt only what the reference cannot show.
- State exactly what each reference must preserve, and do not ask one reference type to solve a different problem.
- For multi-shot clips, use explicit `Shot 1.` and `Cut to.` cues, maintain identity and geography, and give the final beat a clear end state.

## Choose a workflow

| Workflow | Best for | Prompting note |
|---|---|---|
| Text to video | Best default for the complete prompts below. | Write subject or shot, motion, camera, lighting, and audio in timeline order. |
| Image references — product lock | Exact products, labels, faces, characters, or multi-angle appearance. | Let the image define appearance; state what must remain exact and describe only motion, camera, and audio. |
| Video references — motion style | Reusing a proven camera move, shake amplitude, speed curve, action timing, or cut point. | Name the motion and pacing to transfer, then identify the new subject or image reference receiving it. |
| Audio references — voice & music sync | Locked scripts, approved reads, lip-sync, music transients, or beat-aligned reveals. | Preserve the reference audio's words, timing, and pauses; align visual beats to the actual voice or music and do not invent replacement audio. |

## Prompt catalog

<a id="product-ad"></a>
## Product Ad

### 1. Serum dropper macro

```text
Subject. A frosted glass dropper bottle of amber facial serum, label facing camera, resting on a wet black stone slab.
Motion. A single drop falls from the dropper tip and lands on the stone, spreading into a thin amber puddle; the bottle rocks once from the impact then settles still.
Camera. 100mm macro lens, slow dolly-in from eye level, shallow depth of field keeping the label sharp while the background blurs.
Lighting. Hard top-down key light throws a bright rim along the bottle's shoulder; a cool blue backlight separates the glass from the black surface.
Audio. A single wet droplet tap on stone, then low ambient studio hum fading to silence.
```

**Technique note:** The droplet, bottle rock, and settled end state form one readable impact chain. Macro focus and rim light keep the label and glass silhouette dominant.

### 2. Sneaker turntable reveal

```text
Subject. A matte black running shoe on a rotating concrete pedestal, laces slightly loose, one lace hanging over the edge.
Motion. The pedestal turns a quarter-rotation as a shaft of light sweeps across the shoe's side panel, catching the stitched seams; the hanging lace sways once from the air movement.
Camera. 50mm lens, slow arc move circling the shoe at knee height, camera fixed on the shoe.
Lighting. Single hard spotlight from camera-left crosses the shoe as it turns, deep shadow pooling on the concrete behind it.
Audio. A low mechanical whir from the pedestal turning, one soft lace flutter, then quiet.
```

**Technique note:** A quarter-turn, one light sweep, and one lace movement add layered motion without distracting from the product. Fixed attention on the shoe protects the hero framing.

### 3. Coffee bag pour

```text
Subject. A kraft-paper coffee bag standing upright next to a white ceramic mug on a wooden counter, steam curling from the mug.
Motion. Dark roasted coffee pours from off-frame into the mug, rising toward the rim; a few beans roll off the bag's folded top and settle against its base.
Camera. 35mm lens, static low-angle shot, camera fixed, steam and pour motion carrying all the movement.
Lighting. Warm low side light from a window at camera-left, steam catching the light as it rises.
Audio. A steady pour trickle, a ceramic clink as a bean rolls into the mug, room tone.
```

**Technique note:** The locked camera lets the pour, steam, and rolling beans carry the scene. Warm side light makes both the liquid motion and lifestyle setting legible.

<a id="ugc-testimonial"></a>
## UGC Testimonial

### 4. Skincare testimonial

```text
Subject. A woman in her late 20s, damp hair pushed back, sitting in a sunlit bathroom, holding a serum bottle at chest height, speaking to camera.
Motion. She turns the bottle to show the label, presses her lips together thinking, then taps the dropper cap twice against her palm before setting it down.
Camera. Handheld selfie framing, 24mm, slight natural sway, front-facing medium close-up.
Lighting. Soft window light from camera-right, faint mirror reflection visible behind her left shoulder.
Audio. Her voice: "Okay, three weeks in, and my skin has genuinely calmed down." Bathroom fan hum low underneath.
```

**Technique note:** Specific hand and facial beats make the testimonial feel observed rather than staged. Natural sway and bathroom ambience support a native UGC finish.

### 5. Fitness app testimonial

```text
Subject. A man in workout clothes, sweat on his hairline, sitting on a gym bench with his phone in hand, catching his breath between sets.
Motion. He wipes his forearm across his brow, glances down at the app on his phone screen, then looks up and half-laughs before speaking.
Camera. Handheld, 35mm, static medium shot at bench height.
Lighting. Overhead gym fluorescents, hard practical light with visible equipment shadows on the floor behind him.
Audio. His voice: "I stopped guessing my sets — the app just tells me when to push." Distant clang of weights racking, gym ambience.
```

**Technique note:** The wipe, app glance, and half-laugh establish context before the line. Practical light and weight noise keep the testimonial grounded on the gym floor.

<a id="action-sequence"></a>
## Action Sequence

### 6. Rooftop parkour

```text
Shot 1. Low-angle medium shot, a runner in a gray hoodie sprints along a rooftop ledge, gravel crunching under each footfall, city skyline behind him.
Cut to. Tracking shot from behind, he plants one foot on the ledge and launches across the gap between buildings, wind snapping his hoodie sleeves.
Cut to. Handheld low shot from the landing rooftop, he hits the surface in a roll, dust kicking up around his shoulder, and comes up running without breaking stride.
Lighting. Late-afternoon sun low on the horizon, long hard shadows stretching across the rooftops, warm rim light on his silhouette mid-jump.
Audio. Footfalls on gravel, one sharp gust of wind during the jump, a hard exhale on landing.
```

**Technique note:** Each cut advances one causal action—run, jump, land—while the consistent hoodie, light, and sound preserve continuity across the three-shot sequence.

### 7. Motorsport drift

```text
Shot 1. Wide shot, a matte-orange coupe drifts sideways through a rain-slicked intersection, tire smoke peeling off the rear wheels.
Cut to. Low ground-level shot as the car passes camera, water spraying off the tires in a fan, streetlights streaking across the wet hood.
Cut to. Interior shot over the driver's shoulder, his knuckles tighten on the wheel as he counter-steers, headlight glare sweeping across his face through the windshield.
Lighting. Wet asphalt reflecting orange sodium streetlights, headlights cutting hard beams through drifting tire smoke.
Audio. Engine snarl rising through the drift, tire squeal, a hard exhale from the driver.
```

**Technique note:** The exterior-to-interior progression moves from spectacle to driver reaction. Wet reflections, engine rise, and counter-steer connect the cuts into one timed drift beat.

<a id="unboxing"></a>
## Unboxing

### 8. Tech gadget unboxing

```text
Subject. A pair of hands on a light wood desk lifting the lid off a matte white product box, a wireless earbuds case nested in foam inside.
Motion. Thumbs peel back a foam insert flap, the case slides slightly as the box tilts, one hand lifts it free and thumbs the lid open with a soft click.
Camera. Overhead top-down shot, 35mm, camera fixed, hands entering and exiting frame.
Lighting. Soft diffused desk lamp from camera-left, faint warm reflection on the glossy case lid.
Audio. Cardboard lid lifting, foam compression, a single magnetic click as the case opens.
```

**Technique note:** The overhead locked view preserves hand and package geography. Material-specific sounds mark the lid, foam, and magnetic reveal in order.

### 9. Fashion unboxing

```text
Subject. Hands untying a ribbon on a matte black apparel box on a marble countertop, tissue paper folded neatly inside.
Motion. The ribbon falls away, fingers part the tissue paper, revealing a folded knit sweater in deep green; a hand lifts one sleeve to show the texture.
Camera. 50mm lens, slow dolly-in from a three-quarter angle, shallow depth of field.
Lighting. Cool north-facing window light, soft shadow under the box edge on the marble.
Audio. Ribbon slide, tissue paper crinkle, a faint fabric rustle as the sleeve lifts.
```

**Technique note:** The reveal escalates from ribbon to tissue to fabric texture. A restrained dolly-in and cool window light create a premium finish without adding extra actions.

<a id="talking-avatar"></a>
## Talking Avatar

### 10. Real estate agent

```text
Subject. A man in a navy blazer standing in a bright, empty living room with floor-to-ceiling windows behind him, speaking to camera.
Motion. He gestures once toward the window with an open palm, then clasps his hands back together at waist height as he finishes his sentence.
Camera. Static medium shot, 35mm, eye level, camera fixed.
Lighting. Bright natural daylight flooding through the windows behind him, soft fill on his face from a bounce card.
Audio. His voice: "Three bedrooms, south-facing, and it's on the market for the first time in nine years." Faint room echo from the empty space.
```

**Technique note:** One gesture supports the listing line without competing with lip-sync. The fixed eye-level shot and room echo make the empty property part of the pitch.

### 11. SaaS founder pitch

```text
Subject. A woman in a plain cream sweater sitting at a wooden desk in front of a softly blurred bookshelf, speaking directly to camera.
Motion. She leans forward slightly on the word "actually," tapping one finger once on the desk for emphasis, then settles back.
Camera. Static medium close-up, 50mm, eye level.
Lighting. Soft key light from camera-left, warm practical lamp glow visible on the desk edge.
Audio. Her voice: "We didn't set out to build another dashboard — we set out to kill the dashboard." Quiet room tone.
```

**Technique note:** The lean and single tap tie performance to a precise verbal emphasis. Static framing and quiet room tone prioritize the founder's line.

<a id="food"></a>
## Food

### 12. Burger bite

```text
Subject. A stacked cheeseburger on a wooden board, melted cheese still glossy, a hand gripping it from the side.
Motion. The hand lifts the burger and takes one bite from the corner, cheese pulling into a stretching strand before it snaps.
Camera. 100mm macro, slow push-in, camera fixed on the bite point.
Lighting. Warm overhead spotlight, steam rising visibly off the patty catching the light.
Audio. A soft crunch of the bun crust, a low sizzle from the board, one satisfied exhale.
```

**Technique note:** The lift, bite, stretch, and snap give the shot a complete food-action payoff. Macro framing and steam-lit highlights concentrate attention on texture.

### 13. Latte art pour

```text
Subject. A ceramic cup of espresso on a marble counter, milk being poured from a steel pitcher into the center.
Motion. Milk streams in, folding into a rosette pattern across the crema as the pitcher tilts and lifts away.
Camera. Overhead top-down shot, 35mm, camera fixed, pour motion carrying the frame.
Lighting. Bright diffused daylight from a skylight above, a soft reflection of the pitcher visible on the marble.
Audio. A steady milk pour, the pitcher tapping once against the cup rim at the end, cafe ambience low underneath.
```

**Technique note:** A fixed top-down view makes the rosette transformation easy to follow. The final pitcher tap supplies an audible endpoint to the pour.

<a id="cinematic-b-roll"></a>
## Cinematic B-Roll

### 14. Rain-wet city street

```text
Subject. A rain-wet city street at night, neon signs reflected in puddles, a lone figure walking away from camera under an umbrella.
Motion. The figure's silhouette moves through the frame as a taxi passes in the foreground, headlights briefly overexposing the puddle reflections.
Camera. 24mm wide lens, slow tracking move parallel to the street, low camera height near the puddles.
Lighting. Mixed neon color temperature, pink and cyan signage reflected in wet asphalt, hard headlight flare from the passing taxi.
Audio. Rain hitting the umbrella, tires hissing on wet road, distant traffic hum.
```

**Technique note:** Foreground taxi motion creates a brief light event while the umbrella figure anchors the composition. Low tracking height maximizes wet-street reflections and parallax.

### 15. Mountain sunrise

```text
Subject. A mist-covered mountain ridge at sunrise, pine trees silhouetted along the ridgeline, fog moving low through the valley.
Motion. The fog drifts slowly across the valley floor as the first direct sunlight breaks over the ridge, catching the top edge of the mist in gold.
Camera. 24mm wide lens, slow crane-up revealing more of the valley as the shot rises.
Lighting. Cold blue pre-dawn light shifting to warm gold as the sun crests the ridge, strong side-light on the pine silhouettes.
Audio. Wind moving through pine needles, a distant bird call, low ambient valley hum.
```

**Technique note:** The slow crane and blue-to-gold light shift create a natural reveal at landscape scale. Fog movement supplies subtle depth while the ridge remains stable.

## Final review

Review identity, anatomy, physics, geometry, continuity, exact text and labels, timeline feasibility, audio sync, reference fidelity, permissions, claims, disclosures, and safety as relevant. More production workflows: [Reviral](https://reviral.ai).
