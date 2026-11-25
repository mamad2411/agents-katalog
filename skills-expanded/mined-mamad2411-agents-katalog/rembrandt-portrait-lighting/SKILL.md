---
name: rembrandt-portrait-lighting
description: Turn an everyday people or pet photo into a format-adaptive Rembrandt-lit studio hero portrait with strong chiaroscuro and subject separation. Use for cinematic studio portraits, profile pictures, editorial crops, or studio swaps of people and pets; not for ordinary background replacement or light retouching.
---

# Format-Adaptive Rembrandt Portrait Lighting

Turn a supplied photo into a complete, credible Rembrandt-lit studio hero portrait at a proportion suited to the source and intended use. Rembrandt chiaroscuro is the defining style; the studio conversion, framing, subject separation, and final grade exist to make that light hit with premium editorial authority.

## Scope and subject fidelity

- Use the built-in image-generation editing workflow. If the source is a local file, inspect it with `view_image` first. Never overwrite the original.
- The subject can be one or more people, pets, or a mixed group. If no photo is supplied, ask the user to attach one; if they want only a prompt, provide it without generating an unrelated subject.
- Preserve the original subject, count, identity, expression, clothing, accessories, and visible anatomy. Preserve pose and viewpoint by default, but permit the controlled composition and posture refinements below when they make a static source feel like a credible new studio sitting. Do not mirror or radically re-pose merely to accommodate a lighting diagram.
- For people, preserve identity, apparent age, ethnicity, skin tone, facial proportions, hairstyle, hands, tattoos, jewelry, glasses, and wardrobe.
- For pets, preserve species, breed traits, coat color and markings, muzzle, eye color and shape, ear position, whiskers, collar, limbs, and tail. Do not humanize animal eyes, add makeup, alter paws, or invent a different animal.

## Default: full low-key studio conversion

Unless the user explicitly asks to retain the scene, treat the request as a **full Rembrandt studio conversion**: replace the casual environment with a clean deep-charcoal-to-ink studio field and relight the subject around one dominant high-side key. It must feel like one exposure made in one studio, never a cut-out pasted onto black. A background swap without new subject lighting is a failure.

Build clear **figure-ground separation**:

- Make the subject’s key-side planes the highest-value area. Render empty background as a smooth, noise-free deep charcoal that falls toward ink black across the frame. Use one extremely broad, low-contrast, asymmetric tonal transition aligned with the key so the set has depth without becoming visible scenery; never use a centered head halo, spotlight disc, gray haze, or uniformly clipped black canvas. The subject must read instantly even as a thumbnail.
- Treat the background as a **clean low-ISO commercial digital capture**: silky continuous-tone gradient, visually noise-free at 100% zoom, with no film emulation. Gradient is allowed and desirable; grain, texture, and random luminance variation are not.
- Use one dominant, image-coordinate key (`key from image-left` or `key from image-right`), 40–60° off camera and 30–45° above the primary face/eyes. Never use an unqualified “left” or “right”.
- Describe a large, close, feathered, gridded soft source: directional enough for visible highlight-to-shadow modeling, but broad enough for a natural penumbra, gentle highlight roll-off, and believable light wrap at hair, fur, ears, and shoulders.
- Default to a **4:1–6:1 key-to-fill ratio** (about two to two-and-a-half stops) with restrained black-flag **negative fill** on the shadow side. Reserve 8:1 for an explicitly severe theatrical result. Keep both eyes alive and preserve texture in the shadows; do not make the shadow side a dead black cutout.
- Add a restrained, physically plausible **kicker** only when the subject merges into the backdrop. It should define fur, hair, shoulders, or ears at lower intensity than the key—never a neon rim halo. Preserve irregular fine edge hairs and slight optical softness so the silhouette does not resemble a segmentation mask.
- Hold focus on the nearer eye(s) and facial/muzzle plane, then let sharpness fall naturally across ears, shoulders, and clothing as an 85 mm-equivalent studio portrait would. Preserve real skin, fur, whiskers, and fabric without amplifying pores, wrinkles, weave, or edge contrast. Ban clarity/texture boosting, crunchy microcontrast, plastic smoothing, and synthetic bokeh.

Use rich neutral blacks, neutral-to-gently-warm highlights, controlled specular roll-off, and restrained saturation. Preserve the source skin or coat albedo; do not lay an amber, copper, orange, or brown wash over the subject. Keep natural microtexture without exaggerating it. Avoid flat front light, beauty-light wash, HDR halos, orange-and-teal grading, painterly texture, and global film-grain overlays.

## Camera, pose, and living presence

When the source is stiff, passport-like, or memorial-looking, make the smallest safe adjustment that creates editorial life while retaining identity:

- Prefer a subtle three-quarter relationship: turn the virtual camera or the head/torso only a few degrees, keep both eyes plausible, and preserve facial geometry. Never reveal a substantially unseen side of the face or body.
- For people, allow a slight head turn or tilt, relaxed shoulder drop, asymmetric shoulder line, mild torso rotation, or natural weight shift. Keep the original expression unless the user requests another; do not manufacture a grin, change hand gestures, or invent hidden limbs.
- For pets, allow a small head/gaze turn, more attentive but anatomically natural ear posture, or a slight seated/standing weight adjustment. Preserve breed structure, ear shape, paws, tail, coat markings, and the original emotional character.
- Use an eye-level or subtly elevated portrait camera by default. A small camera-height or yaw refinement is acceptable; dramatic low angles, overhead views, wide-angle distortion, or major perspective changes require an explicit request.
- Build asymmetry with gaze room, shoulder direction, light direction, and negative space—not dutch angles or theatrical action. The result should feel alert, present, and recently photographed, not frozen or ceremonial.

## Format and framing

Default to the **source image's aspect ratio and orientation**. Do not force a square, portrait, or landscape conversion when the user has not requested one.

- If the user specifies an aspect ratio or exact dimensions, obey them. If they specify only a use, choose a conventional ratio: `1:1` for avatars, `4:5` for social portrait posts, `3:4` for classic portrait/editorial, `2:3` for full-length portrait/print, `3:2` for photographic landscape/editorial, `4:3` for general landscape, or `16:9` for banners and cinematic covers.
- Preserve orientation unless the requested use clearly requires another orientation. Treat aspect ratio and pixel dimensions separately; never promise dimensions the generator cannot actually deliver.
- Reframe with the least destructive method. First remove expendable background. If cropping would clip hair, ears, chin, whiskers, hands, paws, tail, meaningful clothing, or the spatial relationship between multiple subjects, extend the studio field instead of cutting the subject.
- When extending, synthesize only plausible continuation of the dark studio set, existing clothing/body edges, and necessary contact shadows. Do not invent new anatomy, accessories, furniture, scenery, or a substantially wider camera viewpoint. Extension must match the key direction, lens perspective, depth of field, tonal falloff, and background cleanliness.
- Keep the face or pet head dominant without imposing a fixed head size on every source. Tight portraits may use head-and-shoulders framing; wider source photographs may retain upper body, full body, or group context when that better preserves the original photograph.
- Place the eye line and negative space according to the selected orientation and gaze direction. Do not center mechanically; leave breathing room toward the subject's gaze while keeping the subject visually dominant.
- Keep the eye(s) and face/muzzle as the first visual fixation through focus, local contrast, and controlled dodge-and-burn—not artificial glow or changed eye color.
- Use simple negative space and a clean silhouette. Do not add typography, badges, ornamental frames, fake lens flares, or props.
- Use the highest available native image quality. Do not claim “8K” unless the actual delivered dimensions are 8K; fake resolution language and oversharpening are not quality.

For `1:1` avatar output, use a tight head-and-shoulders crop, keep complete hair/ears/chin/whiskers inside the central 80% circular safe area, and verify readability at 64×64 px. For multiple subjects, preserve the group rather than deleting or merging anyone; use extension or a wider standard ratio when a square would damage the composition.

## Subject-specific light pattern

For people with a three-quarter face and both eyes visible, make the strong default **short-light Rembrandt**: the nasal shadow joins the cheek shadow as a closed loop and leaves a small natural **Rembrandt patch** below the far eye. It is a lighting diagnostic, not a painted-on triangle.

For frontal or profile people, use **Rembrandt-inspired low-key facial-plane modeling** instead; do not distort a nose shadow just to force a patch.

For pets, translate Rembrandt chiaroscuro into an elevated three-quarter side key with sculptural low-key modeling. Prioritize species-appropriate catchlights, muzzle form, eyes, ears, and coat/fur texture. Do not force human cheek-triangle geometry onto animals.

Read [subject diagnostics](references/subject-diagnostics.md) before choosing the light pattern.

## Background and set continuity

- Preserve the source aspect ratio by default. Choose or change to a standard ratio only from an explicit dimension, aspect ratio, or use-case request, following the format rules above.
- Default to a clean, smooth, textureless deep-neutral-charcoal-to-ink studio field—not a uniformly clipped digital `#000000` canvas, charcoal cloth, painted wall, paper, visible cyclorama texture, or fog. Maintain a subtle broad asymmetric tonal falloff aligned with the key; it should create spatial depth with visually continuous, band-free tone. Background cleanliness is non-negotiable: no luminance noise, chroma noise, film grain, sensor grain, dither pattern, mottling, speckle, paper/fabric texture, smoke, dust, banding, JPEG blocks, or AI texture synthesis. Use absolute pure black only when explicitly requested.
- Background separation must come primarily from the directional key, natural light wrap, tonal depth, and only if essential a restrained edge kicker. Never place a gray glow, radial hotspot, obvious vignette, halo, or light pool behind the head to fake separation.
- The background’s direction, falloff, contact shadow, and color temperature must agree with the key. A bright source from the wrong side behind the subject is a defect.
- Respect difficult contours: hair, fur, whiskers, ears, transparent eyeglass frames, translucent fabric, and paws. Preserve natural contact and floor shadows when visible.
- Do not add speed trails, motion blur, wind, action effects, extra subjects, or duplicate limbs unless explicitly asked.

## Avoid memorial-portrait cues

The default result must read as contemporary editorial portraiture, not a memorial, funeral, obituary, or posthumous portrait. Avoid the combined pattern of dead-center frontal symmetry, rigid square shoulders, blank forward stare, uniformly pure-black background, sepia/monochrome skin, heavy vignette, oval framing, faded edges, floating bust crop, solemn ceremonial styling, flowers, candles, wreaths, religious symbols, or inscription space. Dark clothing must retain separation from the set. A calm older subject may remain calm and dignified; create living presence through directional gaze, asymmetric posture, dimensional color, catchlights, and breathable composition rather than forcing a smile.

## Prompt construction and iteration

Before editing, read [the studio production prompt](references/production-prompt.md). Inspect the source, fill the template with only observed facts and user directions, then make one focused edit request. Re-state every source invariant on each retry.

Classify the normal edit as `identity-preserve` plus `lighting-weather`; treat the studio backdrop as part of the integrated relight, not an unrelated replacement. Do not introduce props, text, logos, watermarks, costume changes, glamour makeup, or an oil-painting style.

Make one targeted retry only for an observable defect: noisy background, memorial/funeral resemblance, stiff frontal symmetry, cut-out/segmented appearance, visible background halo, insufficient subject separation, weak or frontal key, incorrect key direction, flat shadows, bronze/orange skin, exaggerated wrinkles or fabric, lost identity/coat markings, unsafe pose change, broken anatomy, artificial animal eyes, haloed fur/hair, or contradictory background light. If the image is otherwise successful but the backdrop contains noise, do **not** regenerate the portrait: request a **background-only cleanup**, locking the subject, crop, lighting, identity, skin/fur, clothing, silhouette edges, and existing broad gradient exactly. Remove only grain, speckle, noise, mottling, banding, and compression artifacts; return a silky continuous deep-charcoal-to-ink gradient with subtle optical integration at the silhouette.

## Final check

Before delivery, inspect every empty background quadrant at 100% zoom: the gradient must be smooth, continuous, neutral, and visually noise-free, with no grain, random texture, color speckle, banding, or compression blocks. Tonal depth must be broad and never form a head halo. Any visible background noise is a failed deliverable even when the subject is otherwise excellent; run the locked background-only cleanup once. Confirm there is no segmentation edge, crunchy microcontrast, copper skin cast, or crushed shadow anatomy. Also confirm that this is visibly one coherent new studio exposure—not the original subject pasted onto a different background; the subject is recognizably identical; one side is clearly key-lit while the other falls into deep legible shadow; and all silhouettes, whiskers, hands, paws, and catchlights remain plausible. Verify that cropping, extension, camera refinement, and posture refinement preserved anatomy, identity, lens plausibility, key direction, and meaningful context. Reject any result whose centered symmetry, black field, expression, or styling gives it an unintended memorial/funeral reading. For avatar output only, also inspect a 64×64 circular-crop preview. Report the actual dimensions, aspect ratio, and whether framing used preservation, cropping, extension, or controlled pose/viewpoint refinement.
