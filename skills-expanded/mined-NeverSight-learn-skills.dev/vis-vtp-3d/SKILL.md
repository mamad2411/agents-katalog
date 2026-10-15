---
name: vis-vtp-3d
description: Visual Translation Protocol (VTP-3D-01) for compiling high-end 3D animation movie character portraits from real human photos. Use when translating real portraits into Pixar/Disney-grade 3D character art, preserving biometric facial identity, and compiling multi-layer image generation prompts.
---

# VTP-3D-01: 3D Animated Movie Portrait Visual Translation & Prompt Compiler

A deterministic visual translation protocol (VTP-3D-01) that translates real human portrait photographs into high-end, 3D animation feature-film characters (Pixar/DreamWorks/Disney quality) while strictly preserving individual biometric identity, spatial topology, and expression.

> **Highest Directive**: *Do not redesign the person. Translate the person.*  
> **Core Pipeline Order**: `Identity First` $\rightarrow$ `Topology Second` $\rightarrow$ `Composition Third` $\rightarrow$ `Style Fourth` $\rightarrow$ `Environment Fifth` $\rightarrow$ `Rendering Last`.

For exhaustive specifications and master protocols, consult [`references/vtp-3d-master-protocol.md`](references/vtp-3d-master-protocol.md).

---

## 6-Phase Visual Compiler Workflow

```
[Phase 1: Biometric Identity Extraction] ➔ [Phase 2: Topology & Pose Anchor] ➔ [Phase 3: 3D Material & Shader Translation] ➔ [Phase 4: Cinematic Lighting & Camera] ➔ [Phase 5: Prompt Compilation] ➔ [Phase 6: Verification Matrix]
```

### Phase 1: Biometric Identity Extraction
Extract inviolable subject biometric anchors:
- **Facial Geometry**: Cranial shape, eye corner tilt, epicanthic fold, nasal bridge height and apex curvature, philtrum depth, lip volume, jawline contour.
- **Demographics & Gaze**: Perceived age, gender presentation, gaze direction, and subtle micro-expressions.
- **Hair & Wardrobe**: Hairline shape, hair volume, color highlights, wardrobe silhouettes, and distinctive accessories (glasses, earrings, jewelry).

### Phase 2: Spatial Topology & Composition Anchor
- **Framing & Aspect Ratio**: Lock aspect ratio (e.g. 3:4, 16:9, 1:1) and head-to-shoulder proportions.
- **Multi-Subject Topology**: If multiple subjects are present, lock relative eye levels, shoulder overlaps, and scale differences. Never alter left-to-right positioning.

### Phase 3: 3D Animation Material Translation
Translate realistic textures into Pixar/Disney-grade 3D shader properties:
- **Skin**: Stylized subsurface scattering (SSS) with peach-fuzz sheen; remove blemishes while retaining characteristic freckles, dimples, or laugh lines.
- **Eyes**: Large, highly refractive cornea with cinematic catchlights and stylized iris patterns.
- **Hair**: Clump-based strand grooms with stylized subsurface anisotropic reflections.
- **Clothing**: Tactile fabric micro-details (e.g. chunky knit, matte cotton, glossy leather) rendered in 3D stylized form.

### Phase 4: Cinematic Lighting, Camera & Scene Environment
- **Lighting**: Three-point cinematic setup (warm key light, cool soft fill, crisp rim/hair light).
- **Camera & Lens**: 85mm portrait focal length equivalent, shallow depth of field (f/1.8 to f/2.8), subtle chromatic aberration and anamorphic bokeh.
- **Environment**: High-end studio lighting backdrop or narrative cinematic environment harmonized with subject rim lighting.

### Phase 5: Multi-Layer Prompt Compilation
Compile positive and negative generation directives for target diffusion/multimodal models (Midjourney v6/Niji 6, Flux 1.1 Pro, SDXL, GPT-Image 2).

---

## Compiler Output Schema

```markdown
# VTP-3D-01 Translation Package

## 1. Biometric & Identity Anchors
- **Subject**: [Age, gender, ethnic features]
- **Facial Geometry**: [Mapped eye, nose, lip, jaw contour]
- **Hair & Wardrobe**: [Hair style/color, wardrobe textures]
- **Expression & Gaze**: [Subtle smile, direct eye contact]

## 2. 3D Shader & Material Translation
- **Skin Shader**: High-end 3D subsurface scattering (SSS), warm peach skin tones, soft specular highlights.
- **Eye Shader**: Refractive glass cornea, deep dimensional iris, warm catchlights.
- **Hair Shader**: Volumetric stylized groom with soft rim glow.

## 3. Compiled Generation Prompt (Midjourney / Flux / SDXL)

### Core Positive Prompt
```text
3D animated movie character portrait of a [gender, approximate age], [exact biometric facial likeness: eye shape, nose shape, lip shape], [exact hair style and color], [exact wardrobe details], stylized 3D feature animation aesthetic, Pixar and DreamWorks character design style, rich subsurface scattering skin shader, expressive refractive eyes with dual catchlights, clumped strand hair groom, three-point cinematic studio lighting, warm key light, crisp rim lighting, shallow depth of field, 85mm lens, 8k render, Octane Render, masterpiece --ar 3:4 --v 6.1 --stylize 250
```

### Core Negative Prompt
```text
photorealistic, real human photo, 2d anime, flat vector art, plastic toy, wax figure, deformed face, asymmetry, extra eyes, bad anatomy, lowres, grainy, noisy render
```

## 4. Verification Matrix
- [x] Identity fidelity verified against reference photo
- [x] 3D shader parameters adhere to animation movie standards
- [x] Spatial composition and camera framing locked
```

---

## Checkable Completion Criteria

- [ ] All six phases executed in order: identity, topology, shader, lighting, prompt compilation, verification.
- [ ] Biometric anchors preserved: eye, nose, lip, jaw contours and expression match the source photo.
- [ ] Positive prompt encodes 3D feature-animation style with SSS skin, refractive eyes, and cinematic camera specs; negative prompt excludes photorealism.
- [ ] Verification matrix completed inside the delivered Translation Package.
