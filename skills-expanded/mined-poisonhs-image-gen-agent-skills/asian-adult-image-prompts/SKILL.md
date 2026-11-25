---
name: asian-adult-image-prompts
description: Use when creating or refining adult-only, Asian-inspired editorial or boudoir image prompts from the bundled nsfw-prompt-templates-asian reference collection, especially when the request needs consistent scene, composition, wardrobe, lighting, pose, and visual-style choices.
license: MIT
compatibility: Markdown references only, no runtime dependencies. Adult content for fictional, consenting adult subjects only.
metadata:
  version: 2.0.0
  source: nsfw-prompt-templates-asian
  adult_only: true
---

# Asian Adult Image Prompts

Create coherent, adult-only image prompts from the bundled modular Asian visual-prompt collection. Extract only the details needed for the user's request; do not paste source passages into the response.


## Load References

Read `references/upstream/README.md` first, then load only the modules relevant to the request. See [source-map.md](references/source-map.md) for the pinned source revision and attribution details.

Do not load the whole collection for a simple request. Start with these files under `references/upstream/`:

| Need | Read |
| --- | --- |
| Scenario and narrative | `01-场景主题.md` |
| Shot, lens, device, composition | `02-景别构图.md` |
| Wardrobe and coverage | `03-裸露液体.md`, `04-服装专项.md` |
| Lighting and mood | `05-光影氛围.md` |
| Pose and expression | `06-姿势动作.md`, `07-表情眼神.md` |
| Film, makeup, hair, texture, props, persona | `08` through `14` as needed |
| Pose/costume/hair taxonomy + CN→EN mapping (1,439 poses / 3,224 outfits / 1,499 portraits) | `references/pose-atlas-anhao.md` |

## Compose

1. Extract only choices that fit the user brief. Resolve contradictions before writing, such as a phone-camera look paired with high-end cinema wording, or incompatible clothing and coverage states.
2. Use one primary visual idea. Add at most three to five supporting details; do not turn every module into a tag dump.
3. Assemble the English prompt in this order: subject and adult status, scene, composition/camera, wardrobe and coverage, pose/action, expression, lighting, then optional style/details.
4. Keep the image prompt between 80 and 150 English words unless the user specifies another limit. Prefer concrete visual language over abstract mood labels.
5. Include a short negative prompt only when the target model supports it. Focus it on image defects and composition problems, not on a second scene.

## Output Format

Return exactly the requested format. When the user does not specify one, use:

```text
Brief: <one Chinese sentence>

Prompt:
<English image prompt>

Negative prompt:
<optional, model-agnostic exclusions>
```

Mention any material assumption in `Brief`. Do not expose a long chain of reasoning or copy large passages from the reference collection.

## Common Errors

| Error | Correction |
| --- | --- |
| Mixing incompatible camera quality signals | Match image quality language to the stated device or remove the device. |
| Contradictory wardrobe and coverage | Select one coherent state and describe it once. |
| Generic words such as `cinematic` or `sexy` doing all the work | Add a specific lens, light direction, material, posture, or expression. |
| Unclear age or consent | Stop and request confirmation of a fictional, consenting adult subject. |
| Copying the source repository into the response | Extract only the needed choices; do not reproduce source passages. |

## Batch Conventions (standing user preferences)

- Default batch: ~8 prompt sets; each set = `Brief` (one Chinese sentence) + English `Prompt` + `Negative prompt` in a code block; close with a 差异一览 comparison table and a short 使用提示 note.
- Subjects are always explicitly adult (20s). Add `loli, child, minor` to negatives, especially for anime/2D styles. Student/school theme + nudity → reframe with adult versions (solo adult teacher, 20+ university student); 「JK」 is a skirt style worn by adult women.
- 不脸红: user wants calm composed expressions — `no blush, calm composed gaze` in the prompt; `blushing, flushed cheeks, rosy cheeks, shy expression` in negatives.
- Vary style, pose, occupation, scene, and film stock across sets and across batches — the user notices repetition and dislikes it.
- Exposure and interaction level follow user requests (step-ups like 再暴露一点, step-downs like 若隐若现; kissing → touching when asked); keep every subject a fictional adult and every scene consensual.
- Pairings: solo, F/F (`2girls, yuri`) and M/M (`2boys, yaoi`) are all requested. For two-person sets add `fused bodies` to negatives; for M/M also add `shota` and `female breasts, cleavage` so the male chest stays male.
- Axis rotation: when the user says 换场景/姿势/职业/镜头/丝袜/画风, regenerate the whole batch with that one axis changed and everything else fresh; the user rejects repeated compositions.
- Named-character series: for 「阿离」 use the anchor `Ali (阿离), an adult Chinese woman with almond eyes, long straight black hair, a small beauty mark under her left eye`; keep it verbatim across sets for face consistency.
- These prompts target local NSFW-capable models; mainstream online platforms refuse them — say so in 使用提示.
- No black-and-white or monochrome output: never use B&W film stocks or styling (Ilford HP5, Tri-X, Delta, `black and white`, `monochrome`, `grayscale`, 黑白) — every prompt stays in color.
- Pose/outfit sourcing: when the user names a pose family (M字开腿, 回眸, 跪立…) or asks to vary poses, pull exact entries from `references/pose-atlas-anhao.md` and cite the pose ID in the Brief (e.g. `参考 P018 M字开腿（坐位・双手后撑）`); each pose has five angle variants (正面/俯视/仰视/侧面/斜侧), so swap angles across sets instead of inventing new poses.

## Maintenance

- This directory is a git working copy of `github.com/poisonhs/asian-adult-image-prompts` (branch `main`, remote `origin`). The user expects every skill update to land in that repo: `git add -A && git commit -m "..." && git push origin main`, then confirm the push with `git ls-remote origin refs/heads/main` and compare it to `git rev-parse HEAD` — a local commit alone is not proof the remote updated.
