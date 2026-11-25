---
name: yaliai-gpt-image-2-inspiration
description: >-
  Use for GPT-image2/Yali AI image and prompt workflows: generate/create/make/design/draw/render/produce/find/write/improve/edit images/prompts. Trigger for visual tasks even if Yali/templates are not mentioned: website/app UI, SaaS/dashboard screens, landing visuals, product shots, e-commerce images, covers, posters, banners, ads, infographics, diagrams, logos/brand visuals, storyboards, social media, WeChat/Xiaohongshu/video covers, PPT/slide visuals, batch variants, and image-to-image edits such as retouching, inpainting, masking, background/object removal or replacement, text localization, style transfer, compositing, or reference-image generation. Also use to search/browse/copy/compare prompts, inspiration cases, example/reference images, categories, templates, styles, or prompt libraries. Run before host-native image tools to classify tasks, search Yali examples/templates when useful, craft prompt/edit specs, preflight requirements, and choose Yali API, host-native generation/editing, or prompt-only.
---

# Yali AI GPT-Image2 Inspiration

Use this skill before image-generation or image-editing execution, even when the user only describes a concrete visual output such as "make a blue website UI" or "create a product poster." It turns the user's task into a concrete working path: search examples/templates when useful, choose categories, write a production-ready prompt/edit spec, and then route to Yali queued API, a host-native image tool, or a prompt-only fallback.

Do not include or invent private API keys. Yali API generation requires the user's own key from `https://www.yaliai.com/free-image/skill/`, preferably configured as `YALIAI_API_KEY`. Codex-native image generation may not need a Yali key, but that only applies inside hosts that already provide native image tools.

## References

- Read `references/api.md` when calling the Yali AI API or explaining setup.
- Read `references/prompt-workflow.md` when choosing categories, adapting inspiration cases, or writing final prompts.
- Read `references/image-generation-workflow.md` when deciding between prompt-only, Yali queued generation, Codex-native generation, edits, batches, sizes, or quality settings.
- Read `references/ppt-generation/README.md` when the user asks for PPT, slides, decks, presentations, keynote-style output, or multi-slide reports.

## Activation Rule

If the user's request will likely produce or modify a visual asset, use this skill first. The user does not need to say "Yali", "inspiration library", "template", "GPT-image2", or "prompt."

Common trigger wording includes:

- Chinese: 生成图片, 设计一张图, 做封面, 做海报, 做商品图, 做网页UI, 做App界面, 生成网站界面, 生成蓝色后台界面, 生成PPT, 做幻灯片, 改图, 修图, 换背景, 去掉某物, 替换文字, 用参考图生成.
- English: generate image, create visual, design UI, make a website mockup, product shot, poster, cover, banner, infographic, logo, storyboard, slide deck, edit image, remove object, replace background, use reference image.

Do not wait for the user to ask for "prompt inspiration." For broad creative generation, search Yali inspiration first unless the user says not to search, network/API access is unavailable, or the task is a purely mechanical edit.

Boundary: do not use this skill for ordinary frontend or application coding when the user only wants code changes. Use it for coding tasks only when the user asks for visual inspiration, generated mockup images, image assets, prompts, or slide visuals to support that coding work.

## Use Inspiration As References

Yali inspiration cases and templates help shape the result; they do not replace the user's request. Treat retrieved cases as visual references for structure, composition, platform conventions, style, and prompt patterns.

- Do not copy a case prompt unless the user explicitly asks to reuse that exact prompt.
- When cases match well, adapt their useful structure into a new prompt for the user's subject.
- When cases are weak, empty, or mismatched, do not force them into the result. Use category matching, live templates, and visual reasoning to write an original prompt.
- Preserve the user's explicit subject, visible text, platform, aspect ratio, edit invariants, and constraints over anything found in the inspiration library.
- Use template keys only for clearly matching output types. If no template clearly fits, omit `template_key` and express the needed layout, style, and constraints directly in the prompt.

## Operating Loop

Follow this loop for every triggered task. Do not skip steps unless the skip condition is explicit.

1. **Classify**: decide one intent: prompt/case search, prompt writing, template-shaped generation, new image generation, image editing, batch generation, or PPT visuals.
2. **Retrieve**: for prompt writing or broad generation, search Yali inspiration first. Use 2-4 concise queries. Skip only if the user says not to search, no network/API access exists, the edit is purely mechanical, or the user gives a complete prompt and explicitly asks to generate directly.
3. **Match**: map to Yali categories and check live templates when the output type is explicit. Do not force a template for ambiguous creative work.
4. **Craft**: write an original prompt or edit spec. Preserve exact user text, visible layout requirements, aspect/size, constraints, and edit invariants.
5. **Preflight**: before any generation/edit call, decide provider and verify required inputs: key, reference images, template size, quality, and polling/result behavior.
6. **Execute or fallback**: run Yali queued API, host-native generation/editing, PPT branch, or prompt-only fallback. Never pretend a generation occurred.
7. **Report**: state provider, search queries/cases if used, template if used, final prompt/edit spec, and task/result fields for the chosen provider.

## Capability Router

Use this routing before calling any image-generation or image-editing tool:

| User intent | What this skill contributes | Required reference | Execution path |
| --- | --- | --- | --- |
| Find examples or prompts: "找提示词", "找灵感", "参考图", "example cases", "prompt library" | Query public Yali inspiration APIs and summarize matching cases | `references/api.md`, `references/prompt-workflow.md` | Public Yali API, no key |
| Write or improve prompts: "帮我写提示词", "优化这个 prompt", "改成 GPT-image2 可用" | Map to Yali categories, use cases as structural inspiration, write an original prompt | `references/prompt-workflow.md` | Prompt-only unless user asks to generate |
| Use a template: "公众号封面模板", "商品主图", "UI mockup", "信息图", "视频封面" | Fetch live templates and select a matching `template_key` only when the request clearly fits | `references/api.md`, `references/prompt-workflow.md` | Template metadata is public; Yali generation still needs a key |
| Generate a new image: "生成/创建/设计/做一张图", cover, poster, banner, product visual, UI, infographic, logo, storyboard, social image | Shape the prompt with Yali categories, templates, dimensions, text placement, and inspiration cases | `references/prompt-workflow.md`, `references/image-generation-workflow.md` | Yali API with key, host-native generation, or prompt-only |
| Edit an image: "编辑/修改/重绘/换背景/去掉/替换/局部改/文字替换/风格迁移/用参考图" | Define edit intent, invariants, reference-image payloads, prompt spec, and provider boundary | `references/image-generation-workflow.md`, `references/api.md` | Yali queued API with `action:"edit"` and 1-2 `reference_images`, host-native edit, or prompt-only |
| Generate PPT, slides, deck, presentation, or multi-slide report | Route to the PPT branch and support slide visual prompts/images | `references/ppt-generation/README.md` | Dedicated PPT workflow plus Codex-native/Yali API/prompt-only image path |

For image generation or editing requests, do not skip directly to a host-native image tool. First use this skill to decide category, template fit, provider path, size/aspect, exact text, and constraints.

## Provider Modes

Choose exactly one mode before execution:

| Mode | Use when | Key requirement | Output |
| --- | --- | --- | --- |
| Public retrieval | searching examples, prompts, categories, case details, or templates | none | case/template data and adapted prompt guidance |
| Yali queued API | user wants Yali website behavior, templates, credits, queue, task IDs, result URLs, or provides `YALIAI_API_KEY` | `YALIAI_API_KEY` | `task_id`, queue/status/result metadata, image URL when complete |
| Host-native generation/editing | current host explicitly provides native image tools and user does not require Yali queue/account behavior | no Yali key | host-native image result; no Yali task ID |
| Prompt-only | no generation backend/key is available, or user asks only for prompts | none | final prompt/edit spec plus setup guidance |
| PPT branch | user asks for PPT/slides/deck/presentation | depends on image provider | dedicated PPT workflow artifacts and slide visual prompts |

Never mix provider semantics. A host-native image result is not a Yali task. A Yali template key is sent only to the Yali API; for host-native generation, translate the template's visible constraints into the prompt.

## Preflight Rules

- Before Yali generation/editing, check for `YALIAI_API_KEY`. If missing or invalid, direct the user to `https://www.yaliai.com/free-image/skill/`; do not write keys to files.
- Before Yali editing, require 1-2 `reference_images`; use `action:"edit"`. If no reference image exists, ask for it or return an edit spec.
- Before reference-image generation, allow up to 2 reference images; use `action:"generate"` or omit `action` on the Yali path.
- Before template-shaped Yali generation, fetch live templates and use `fixedSize` or the best `sizeOptions` value.
- Before host-native generation/editing, still complete retrieval, category/template reasoning, and prompt/edit spec. Do not send Yali-only fields such as `template_key`.
- For ambiguous, expensive, or high-polish tasks, present 1-3 directions or ask one concise question. For precise "generate now" requests, proceed after the required preflight.
- Do not reinstall skills, modify `.env`, overwrite user files, or save private keys unless the user explicitly asks for setup.

## Endpoint Map

Use these public endpoints for retrieval before generation when useful:

- Search examples: `GET https://www.yaliai.com/wp-json/yali/v1/inspiration/search?q=<query>&limit=5`
- Browse categories: `GET https://www.yaliai.com/wp-json/yali/v1/inspiration/categories`
- Case detail: `GET https://www.yaliai.com/wp-json/yali/v1/inspiration/cases/{case_id}`
- Live templates: `GET https://www.yaliai.com/wp-json/yali/v1/free-image/api/templates`

Use this authenticated endpoint only when executing through Yali:

- Generate or edit: `POST https://www.yaliai.com/wp-json/yali/v1/free-image/api/generate`

## Core Workflow

1. Detect the user's language and respond in that language.
2. Identify the concrete task from user wording:
   - find/search/copy/compare prompts, cases, example images, templates, or reference images
   - write/rewrite/improve/translate/classify an image prompt
   - generate/create/make/design a new image, cover, poster, banner, product shot, UI mockup, infographic, logo, storyboard, or social media visual
   - edit/retouch/inpaint/mask/replace/remove/localize/restyle/composite an image, usually with 1-2 reference images
   - create PPT, slides, decks, presentations, or multi-slide reports
3. For inspiration search, use the public API. No API key is needed.
4. For PPT-like requests, read `references/ppt-generation/README.md` and route to the dedicated PPT workflow. Use this skill only for visual inspiration, slide image prompts, and image generation support.
5. For prompt work or broad image generation, search matching cases first, then write an original prompt adapted to the user's subject. Use multiple queries if needed: subject, output type, style, platform, and category. If the user provides a complete production prompt and says to generate directly, skip search and proceed to provider preflight.
6. For clear output types, fetch live templates before generation. Use a template only when it clearly fits; otherwise keep template as `none`.
   - If the selected template fits the output type, send only the clean user-facing prompt plus `template_key`; do not paste or invent hidden template internals.
   - If no template fits, omit `template_key` and express the needed layout, aspect, text, and style directly in the prompt.
   - If search results do not match the user's intent, say they were weak or mismatched, use the closest structural lessons only if useful, and write an original prompt from the user's request.
7. For image editing, only search inspiration if it helps the style or target result. Always define `Edit target`, `Must preserve`, `Allowed changes`, and reference-image payload rules.
8. For image generation or editing, read `references/image-generation-workflow.md` before calling a tool. Preserve exact visible text, platform size, edit invariants, and user constraints.
9. For actual image generation, choose the execution path before writing commands:
   - Use Yali queued API when the user asks for Yali generation/editing, account/credit tracking, website-consistent templates, reference-image support, public API behavior, or provides `YALIAI_API_KEY`.
   - Use Codex-native generation/editing only when running in Codex or another host that explicitly provides native image generation/editing and the user does not require the Yali queued API.
   - If neither path is available, return the final prompt and key/setup instructions.
10. For clear template-shaped use cases, select the matching `template_key` and use that template's fixed size or size options when appropriate. If the request does not clearly match a template, generate without `template_key`.
11. For Yali API generation, require `YALIAI_API_KEY` or an explicit user-provided key. Never store the key in generated project files unless the user explicitly asks for local environment setup.
12. Start Yali generation through the queued API and return the `task_id`. Poll status every 2-3 seconds if the user asks you to wait for completion.
13. If generation is complete, return the image URL and relevant metadata.

## Common Task Paths

- Website, app, SaaS, dashboard, or Web UI: read `prompt-workflow.md`; map to `产品界面/交互设计` and `ui-mockup`; search terms such as `网站 UI`, `网页界面`, `dashboard UI`, `SaaS UI`, plus color/style words; check the `ui-mockup` template; then generate through the chosen provider.
- Covers, posters, banners, ads, and social visuals: map to `海报/封面/广告` plus platform categories; search platform/output terms; check `wechat-cover`, `xiaohongshu-cover`, `video-cover`, or `website-banner` when explicit.
- Product, e-commerce, packaging, and mockups: map to `产品/电商/包装`; search product type plus `商品主图`, `product hero`, or `packaging`; check `product-hero`.
- Infographics, diagrams, explainers, and technical flows: map to `信息图/结构图`; search topic plus `信息图`, `diagram`, or `technical diagram`; check `infographic` or `technical-diagram`.
- Logo, typography, and brand visuals: map to `品牌/视觉规范` and/or `字体/字效设计`; search brand/style terms; check `logo-concept` when exploring marks.
- Reference-image generation and image editing: map to `图像编辑/参考图控制`; decide edit vs generation with references; use up to 2 reference images; for Yali editing send `action:"edit"`.
- PPT, slides, and decks: route to `references/ppt-generation/README.md`; use this skill for visual style, inspiration search, slide image prompts, and provider selection.

## Output Defaults

- Put the useful result first: prompt, case list, or task result.
- Use this report shape when generation/editing was requested: `Provider`, `Search`, `Reference cases`, `Template`, `Prompt/edit spec`, `Result`.
- For Codex-native image generation/editing, image outputs are normally saved as PNG/JPEG/WEBP files under `$CODEX_HOME/generated_images/<run-id>/`. After the image tool finishes, locate the generated local absolute path and show it in the final response with Markdown image syntax: `![short specific image description](/absolute/path.png)`.
- For Yali API image generation/editing, read the result image URL from `response.url`, falling back to `response.assets[0].url`. When filesystem access exists, download the image to a stable local path, show the local file with Markdown image syntax: `![short specific image description](/absolute/path.png)`, and also report the original remote URL.
- For other host-native or third-party generation paths, get the accessible output location returned by that provider. Prefer a local absolute path with Markdown image syntax: `![short specific image description](/absolute/path.png)`; use a remote URL only when no local file is available.
- Markdown image descriptions must be short and specific, naming the subject, purpose, or visible content, such as `red security tools web UI`, `WeChat article cover`, or `product hero image`.
- Include case IDs and links when using references.
- Keep prompts concrete: subject, composition, style, materials, lighting, text requirements, size/aspect ratio, constraints, and negatives.
- If the user's request is vague, present 2-3 direction options before generating.
- If the user's request clearly matches a template, state the selected template key and use the template's constraints in the generation request. Do not force a template for broad or ambiguous creative requests.
- If search was skipped, briefly say why: user requested no search, no network/API access, or purely mechanical edit.
- If no Yali API key is configured, use host-native image generation only when the host provides it and the user accepts that path. Otherwise provide the final prompt and tell the user to get/configure `YALIAI_API_KEY` from `https://www.yaliai.com/free-image/skill/`.

## API Key Rules

- Never embed a real API key in `SKILL.md`, references, GitHub examples, NPM package files, or generated code samples.
- Use `$YALIAI_API_KEY` in examples.
- Tell users to get their own key from `https://www.yaliai.com/free-image/skill/` after login.
- Prefer environment variables over hardcoded key strings.
- Do not imply that an NPM install creates a universal image-generation backend. The package installs the agent skill; generation still depends on either the Yali API key or the host's native image capability.
