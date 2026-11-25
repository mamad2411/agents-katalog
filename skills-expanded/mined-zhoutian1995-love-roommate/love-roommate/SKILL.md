---
name: love-roommate
description: Use when a user wants to turn an authorized one-to-eight-person photo into a humorous photorealistic desktop pet on Windows x64 or Apple-silicon macOS.
---

# Love Roommate

Turn an authorized 1–8-person photo into a photorealistic desktop pet. Never place private photos, generated people, project output, or host paths inside this Skill.

## Conversation

Speak in the user's language; default to plain Chinese. Ask exactly one missing question per turn.

On the first reply after a photo, diagnose usability, number every separable person left-to-right as `1号`, `2号`… and mention occlusion, cropping, blur, or identity ambiguity. Then ask only the next missing required question. Reuse valid answers already supplied; authorization already supplied means do not ask it again. If authorization, self, and mode are already present, proceed from diagnosis directly to final confirmation.

Use this fixed sequence: `authorization -> self -> Chinese mode -> confirmation`.

1. Ask `照片里的人都知道并同意制作桌宠吗？` when missing. Say `我只能记录你的确认，不能替你证明其他人真的同意。` Stop if the answer is no or unclear.
2. Ask which numbered person is the user, or accept explicit `不在`. Never infer self. `没回答本人是谁，不等于本人不在。只有用户明确回复“不在”，才能进入无本人分支。`
3. Present exactly `1 普通桌宠`、`2 集体跪喊`、`3 屎追逐`、`4 全部都要`. Never expose `person-N`, mode keys, leader/follower controls, exclusions, or eating order.
4. Confirm authorization, self, Chinese mode, and derived behavior before generating.

Tell ordinary users:

- 对话流程：`上传照片 → 授权 → 本人 → 模式 → 最终确认`
- 制作流程：`身份确认 → 动作确认 → 逐模式搞笑评分 → 构建与真实运行验收`
- 用户可以一次说完：`照片里的人都同意，我是3号，全部都要。` 或 `照片里的人都同意，我不在照片里，全部都要。`

Explain the confirmed branch with these meanings:

- `普通桌宠`：所有人物在桌面自由活动，可拖拽、暂停和退出；指定本人保持直立，绝不爬行。
- `集体跪喊`：有本人时本人站立不跪，其余全员跪喊爸爸、爷爷；本人不在照片时不虚构站立接收者，全员跪喊。两种分支都优先居中单排，放不下时使用不重叠、不裁切的居中多排。
- `屎追逐`（有本人）：整队缓慢安全落位一次后固定，普通鼠标移动不影响任何人；本人持续拉，其他人全员轮流追吃；只有主动拖拽本人时整队与当前屎同步移动，松手后固定。
- `屎追逐`（本人不在）：鼠标控制一坨点击穿透的屎，全员连接成人形蜈蚣，以限速、加速度和死区平滑追随，禁止瞬移或断链。
- `全部都要`：四个可见场景为普通桌宠、爸爸喊、爷爷喊和当前屎追逐分支。`集体跪喊`是一个用户选项，爸爸喊和爷爷喊是两个独立场景，不增加用户问题。

With a one-person photo and self present, group shout and poop chase are both safely skipped; only normal desktop pet remains active. With a one-person photo and no self selected, group shout and cursor-poop chase remain available.

After confirmation, expose only the next checkpoint. Pause for identity approval, then action/transparent-edge approval. Do not dump the internal checklist.

## Workflow

Use Codex Desktop and load its Node, pnpm, and node_modules paths. Read only the reference required by the current phase:

- Environment or runtime download: [references/codex-runtime.md](references/codex-runtime.md)
- Image generation, stale cache recovery, or transparency: [references/visual-generation.md](references/visual-generation.md)
- Commands and balanced profiles: [references/workflow-commands.md](references/workflow-commands.md)
- Manual review or scoring: [references/self-check.md](references/self-check.md)
- Runtime configuration changes: [references/runtime-config.md](references/runtime-config.md)
- Packaging or platform acceptance: [references/platform-build.md](references/platform-build.md)
- Selected-self movement/formation code changes only: [docs/self-role-invariant.md](docs/self-role-invariant.md)

Create projects only with `--consent confirmed`; validate before writing and never overwrite an existing output. V1 manifests require the explicit migration command.

Use the balanced runner for validation and delivery:

```text
node scripts/run_workflow.mjs --profile iteration --root <output-root> --source <photo>
node scripts/run_workflow.mjs --profile delivery --root <output-root> --source <photo>
node scripts/run_workflow.mjs --profile skill-release
```

- `iteration` reuses unchanged identity, action, review, and scenario evidence. Inspect only `preview/workflow-summary.json` plus changed artifacts.
- `delivery` checks the complete actual project, packages it, runs packaged smoke and the short real-EXE performance smoke, then requires manual tray, drag, right-click, and click-through checks.
- `skill-release` runs the complete Skill suite and reuses a redacted 5+8 packaged performance certificate only when the shared candidate fingerprint and contract still match.

Existing individual scripts remain supported. Direct `release_check.mjs` without arguments is always the complete release check.

## Image And Transparency Gates

Read [references/visual-generation.md](references/visual-generation.md) before generation. Use Codex image generation under the declared GPT Image 2 workflow and save user imagery only under the user's `preview/`.

Treat `$CODEX_HOME/generated_images` as a stale generated-images cache unless it is bound to the current native generation event. Recover the exact current `image_generation_call.id` result from the task session JSONL when needed; validate PNG signature, dimensions, SHA-256, and unique hashes. Never fabricate generation provenance or switch models because a cache file did not refresh.

Approve one identity master per person, then generate required actions individually or as left/right pairs. Record master fingerprint, prompt version, action, version, replacement reason, and workflow attestation. The attestation is not an OpenAI-signed receipt.

Final sprites must be transparent PNGs with complete bodies and no purple, green, gray, cream, or white halo. Clear hidden RGB in fully transparent pixels. Do not use strong global despill on photorealistic skin or clothing.

Transparency recovery is bounded: at most three distinct high-contrast key attempts. After three failures, use local mask repair on `127.0.0.1` with a random port and token. The browser sends strokes only and must not upload corrected images or canvas pixels. Re-run visual and self-check gates; fail closed on contamination or person erosion.

Only after those paths fail and the user gives `显式授权` may the optional 真透明 fallback use CLI `gpt-image-1.5` with local `OPENAI_API_KEY`. 不得静默切换模型；never print or persist the key.

## Runtime Invariants

- The explicitly selected self never renders `crawl_*` or `centipede_*`, for every 1–8-person count and every self position. Normal movement uses upright idle frames; self-poop uses only poop-role artwork.
- With self present, ordinary cursor movement changes no character position during poop chase. Perform one slow safe placement, keep self visibly in front as the only poop source, keep one readable dropping, and cycle every other person through chase/eat/return in photo order. Only dragging self translates the complete queue and dropping by the same bounded offset.
- With no self, use only cursor-controlled click-through poop plus capped speed, capped acceleration, dead zone, and mouth-to-rear anchors for the connected centipede.
- Dad/grandpa use self as the standing recipient when present and all others as kneeling participants. Without self, use no recipient and make everyone kneel. A single selected self is a safe no-participants no-op.
- Keep effect windows truly transparent and permanently click-through. The poop SVG is one flat brown fill with `filter: none`; forbid gradients, highlights, outlines, drop shadows, glow, pale edge decoration, and opaque window/page backgrounds.
- For every release-eligible poop capture, freeze the same full composition, capture the visible effect, hide only the effect, then capture `effect-underlay.png`. Require transparent interior, outer edge band, and all four corners to match the underlay. Independently reject neutral white/gray pixels and pale halos. Evidence must contain controlled light and dark background regions; white-only evidence is invalid.
- Use one shared 30 fps ticker, suppress unchanged bounds/IPC, create effects lazily, and stop high-frequency work while paused.

## Review And Delivery Gates

Build the identity board and action contact sheet, validate Manifest V2, run privacy audit, and run self-check. Open visual artifacts with `view_image`; JSON alone cannot approve them. Repair only failed or changed characters.

Require `self-check-report.json` status `pass` and score at least 90. Score each selected special prank independently: `dad-shout`, `grandpa-shout`, and `poop-chase` or `cursor-centipede`. Every prank below 90 must fail；特殊恶搞低于 90 必须失败。普通桌宠模式不要求 humor review.

Use the six-field 100-point contract: 角色关系 25、荒诞程度 20、动作与节奏 20、队形表现 15、屎的可读性 10、回看欲 10. Record evidence refs, meaningful deductions, concrete optimization, a new capture, and reevaluation. Never average separate pranks.

Hard visual failures override scores: self and kneeling group separated by more than one character height; dad/grandpa differing only by text/color; eater mouth missing the poop edge; poop covering a face; or a broken cursor-centipede chain.

Inspect complete desktop-compositor captures, not per-window screenshots. Preserve exact configured count; a five-person project is an example, not a fixed product shape. Support every one-to-eight-person photo and centered multi-row overflow.

Before delivery require privacy pass, final packaged smoke, and manual operation of the copied package: tray Pause/Quit, drag, right-click, and transparent-pixel click-through. Build only for the current host.

## Privacy And Skill Release

Persist only relative project paths. Never persist the source photo hash, metadata, username, or host path. Use `--source` only for an in-memory exact-copy scan. Audit the whole output before and after packaging; allow only manifest-listed project raster files.

Keep the performance cache outside the Skill and project at `$CODEX_HOME/cache/love-roommate/performance-v1/`. Cache only fictional 5/8-person reports, hashes, thresholds, platform, architecture, Electron version, contract version, and shared candidate fingerprint. Never cache names, photos, sprites, or absolute paths. Invalidate on code, Electron, threshold, contract, fixture changes, corruption, failure, or age over 30 days.

For Skill release, run the unified release check and official validator. On a Windows cache miss, use `run_performance_audit.mjs` for real packaged 5+8 audits with the unchanged contract: target 30 fps, active p95 ≤ 50 ms, non-transition pause ≤ 150 ms, average total CPU ≤ 10%, all windows visible within 5 seconds and throughout each phase, private bytes ≤ 500 MB, 10-minute growth ≤ 50 MB, Pause CPU ≤ half active CPU, and Pause ticker ≤ 25% of active. Working set is diagnostic only. Never pass by deleting people/actions or lowering clarity.

Transfer final packages through `scripts/lib/release-transfer.mjs`; preserve macOS symlinks and clean partial destinations on failure.
