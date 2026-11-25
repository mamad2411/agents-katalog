---
name: dreamy-motion-editorial
description: Extract the semantic hero from any casual photo and rebuild it as a premium hazy dreamlike motion-editorial image with large negative space, simplified context, selective preservation, and restrained poster hierarchy. Use when the user provides or references a photo and asks for 高级感、朦胧感、梦幻感、电影感、慢门拖影、柔焦、胶片感、诗意海报、Pinterest 同类氛围、图生图提示词、AI 生图提示词、照片风格改造、帖子视觉、封面图、艺术摄影、青春残影、玻璃倒影、花卉虚焦、逆光晕染, or wants a reusable photo-to-poster art-direction workflow. Produces an adaptive diagnosis, mechanism selection, Chinese and English image-to-image prompts, negative prompt, preservation constraints, strength and ratio guidance, and optional restrained poster copy.
---

# Dreamy Motion Editorial

Turn the supplied photograph into an art-directed photographic event, not a faithful full-scene reconstruction or generic blur filter. Preserve the semantic hero and essential action, then simplify, fade, remove, crop, or reposition nonessential content to create editorial hierarchy.

## Default Composition Policy

Default to `semantic-core`, not full-scene fidelity.

- Use **Keep / Fade / Remove** before writing prompts.
- Keep one hero, one essential gesture or object, and no more than two contextual cues.
- Use **kinetic negative space**, not blank empty space: allocate **35–55%** of the frame to broad directional motion veils, **15–30%** to quiet tonal fields, and the remainder to the sharp hero.
- Let the hero occupy roughly 25–40% of the frame unless the source requires a close portrait.
- Permit reframing, asymmetric placement, subject repositioning, and background reconstruction.
- Fade by transformation, not erasure: stretch 2–4 secondary people, flowers, fabric, vehicles, paper, foliage, or architectural edges into large directional blur masses, translucent streaks, and light-color trails.
- Remove only tiny clutter and competing details. Keep enough secondary forms to build foreground, midground, and background motion depth.
- Preserve the entire scene only when the user explicitly requests `identity-lock` or documentary fidelity.

The output should feel extracted, kinetic, and composed, not merely color-graded. A successful result has fewer readable objects than the source but more large-scale motion energy: a sharp anchor surrounded by moving translucent forms.

## Workflow

1. **Inspect the photo visually.** Identify the hero, identity-sensitive details, pose, relationships, clothing, environment, existing light direction, depth layers, reflective surfaces, plausible motion, native colors, and structural risks.
2. **Extract the semantic core.** Write three short lists: **Keep**, **Fade**, and **Remove**. Keep only the hero identity, essential gesture or object, one native accent color, and no more than two context cues.
3. **Design kinetic negative space.** Specify three depth layers: near-lens directional motion veil, midground secondary-form drag, and background light/color trails. Empty quiet fields are supporting space only, never the main effect.
4. **Select the route.** Read `references/style-system.md`. Choose exactly one primary mechanism and at most one support mechanism:
   - `crowd-drift`
   - `floral-diffusion`
   - `glass-memory`
   - `backlit-halation`
   - `low-angle-color-field`
   - `passing-gesture`
5. **Use the helper when useful.** Convert observed traits into a route recommendation with:

   ```powershell
   python scripts/analyze_photo.py --subject portrait --light backlit --motion walking --depth layered --background street --risks face --strength dream-haze --json
   ```

   Treat the result as a consistency aid, not a replacement for visual judgment. The script analyzes supplied observations; it does not inspect pixels.
6. **Choose strength.** Default to `dream-haze`. Use `restrained-premium` for brands, products, identity-sensitive portraits, or subtle requests. Use `experimental-memory` only when the user clearly wants stronger abstraction.
7. **Build the prompt package.** Read `references/prompt-recipes.md`. Follow the required order:

   `source preservation → composition → action/motion → lighting → color → optical behavior → analog texture → emotional tone → rendering constraints`
8. **Add negative controls.** Include anatomy, identity, blur, optical, color, and cheap-aesthetic exclusions relevant to the actual photo. Do not dump irrelevant negative keywords.
9. **Add poster direction only when requested.** Keep typography under 12% of the frame, use existing negative space, and suggest adding exact long text in a design tool rather than relying on image-generation spelling.
10. **Verify before delivery.** Apply `references/quality-rubric.md`. Rewrite if preservation, sharpness hierarchy, or physical motivation scores zero.
11. **Generate only when explicitly requested.** Default to prompt output. When the user asks to create or edit the actual raster image, invoke the available image-generation/image-editing tool and use the finished prompt package as the generation brief.

## Route Selection Rules

- Prefer a feature already present in the source over an invented decorative element.
- Assign motion and diffusion mainly to secondary layers, and make the selected motion mechanism visibly occupy 35–55% of the default dream-haze frame.
- Keep one face plane, eye line, gesture, product edge, label, silhouette, or flower center readable.
- Use flowers or petals only when present, semantically plausible, or explicitly requested.
- Use glass or reflection only when it improves depth and can be physically explained.
- Do not choose `crowd-drift` for isolated products or quiet selfies without plausible surrounding movement.
- Retain 2–4 large secondary motion forms when the source supports people, flowers, traffic, fabric, paper, foliage, or nearby objects.
- Do not combine more than two mechanisms.
- Do not imitate a named living artist or a single Pinterest creator. Translate transferable visual principles instead.

## Strength Defaults

### Restrained Premium

- Preserve the hero while allowing subtle movement across 25–40% of the frame.
- Use one subtle optical cue.
- Keep bloom, grain, and color separation restrained.
- Default for products, brand work, and recognition-sensitive portraits.

### Dream Haze

- Preserve the hero while using 35–55% of the frame for visible directional motion veils and trails.
- Make the chosen motion, reflection, or diffusion clearly visible.
- Allow one compatible support mechanism.
- Default for social posts and editorial portraits.

### Experimental Memory

- Use stronger motion drag, doubling, refraction, or color contamination.
- Preserve one unmistakable visual anchor.
- Do not allow semantic collapse, face replacement, or arbitrary scene invention.

## Output Format

Deliver in this structure:

```markdown
## 照片诊断
- 主体：
- 必须保留：
- 可利用的光线/动态/前景：
- 风险：

## 构图提炼
- Keep：
- Fade：
- Remove：
- 动态覆盖：
- 安静留白：
- 前景掠影：
- 中景拖影：
- 背景光色流：
- 主体占比与位置：

## 视觉方案
- 主机制：
- 辅助机制：无 / ...
- 强度：克制高级 / 梦幻朦胧 / 强烈实验
- 选择理由：

## 中文图生图提示词
...

## English Image-to-Image Prompt
...

## 负面提示词
...

## 保真约束
- ...

## 建议参数
- 比例：
- 重绘强度：
- 主体保真优先级：

## 备选方向（可选）
...

## 海报文案与排版（仅在需要时）
...
```

## Parameter Guidance

Use model-neutral language unless the user names a generator.

- Portrait post: `4:5`
- Editorial poster: `3:4`
- Story or vertical cover: `9:16`
- Environmental scene: preserve the source ratio or use `4:5`
- Recognition-sensitive image-to-image: low-to-medium denoise or transformation strength
- Dream Haze: medium transformation strength
- Experimental Memory: medium-high transformation strength while locking identity or reference strength when supported

Never invent unsupported parameter names. If the user names a model, adapt terminology to that model's current interface.

## Failure Modes

Reject and rewrite prompts that:

- preserve every background object with equal clarity
- produce a literal full-scene reconstruction with no hierarchy
- produce a static empty background with no directional motion atmosphere
- erase every secondary person or object instead of transforming some into motion masses
- keep more than two contextual cues by default
- blur the whole frame uniformly
- replace physical optical causes with abstract “dream magic”
- add random flowers, sparkles, jewelry, costumes, or people
- beautify the subject into a generic face
- request white fog over the entire image
- stack every mechanism into one scene
- combine sterile 8K HDR sharpness with analog softness
- use extreme teal-orange grading
- turn the result into wedding-studio, cosplay, cyberpunk, or stock-photo imagery
- place dense text over faces, gestures, or product labels

## Resource Map

- Read `references/style-system.md` for diagnosis, route grammar, color, texture, and strength logic.
- Read `references/prompt-recipes.md` for bilingual templates, mechanism modules, preservation add-ons, negative prompts, and examples.
- Read `references/quality-rubric.md` for scoring and repairs.
- Run `scripts/analyze_photo.py` when a structured route recommendation improves consistency.
