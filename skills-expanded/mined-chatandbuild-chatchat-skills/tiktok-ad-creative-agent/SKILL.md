---
id: tiktok-ad-creative-agent
name: tiktok-ad-creative-agent
description: "Use when a TikTok advertiser, media buyer, creative strategist, brand operator, or growth team wants an AI agent to turn a product, Amazon page, ecommerce URL, landing page, offer, or ad brief into TikTok-ready ad concepts, hooks, storyboards, voiceover copy, AI image/video prompts, editing briefs, compliance review, delivery checklists, or a confirmed finished ad production workflow."
category: TikTok
---

# TikTok Ad Creative Agent

This skill helps an agent produce performance-oriented TikTok ad creative packages for advertisers. It is tool-neutral: it can be used with text-only planning, image models, video models, editors, or human production teams.

## Use This Skill For

- New TikTok ad concepts for a product, offer, store, app, service, or brand.
- Turning a product page, landing page, PDF, raw brief, or product image into ad angles.
- Producing hooks, storyboards, voiceover copy, AI visual prompts, editing notes, and QC.
- Preparing a package for media buyers, editors, UGC creators, or creative strategists.
- Producing a finished ad when the user confirms the creative draft and provides usable model/tool access.

## Do Not Assume

- Do not assume the product facts are true unless they come from provided materials or verified sources.
- Do not invent prices, discounts, guarantees, awards, clinical claims, endorsements, or performance numbers.
- Do not put readable brand text, legal lines, pricing, or logos inside AI image/video generation prompts unless the user explicitly wants a rough mockup. Add exact text in post.
- Do not present legal, medical, financial, or platform policy review as final professional clearance.

## Core Workflow

1. Intake
   Gather or ask for the creative brief, aspect ratio, duration, language, audio preference, and whether the user wants final assembly. Ask only for user-facing choices; verify model/tool capabilities yourself during execution.

2. Product Source Extraction
   If the input is a URL, PDF, document, image, or product page, extract product facts, product reference images, proof points, offer state, reviews/social proof, and missing or blocked fields. Keep a source ledger.

3. Product And Offer Understanding
   Extract the product promise, proof points, objections, buying triggers, and conversion event.

4. Audience And Pain Point
   Define the buyer, current behavior, emotional stakes, objections, urgency, and reason to believe.

5. Creative Strategy
   Select 3-6 ad angles from `references/creative-angles.md`. Prioritize angles that match the offer, evidence, and platform behavior.

6. Hook Set
   Generate multiple 1-3 second openings. Each hook should map to one angle and one audience tension.

7. Storyboard
   Build 15s, 30s, 45s, or 60s beat sheets using `references/storyboard-formats.md`. Include timing, visual action, on-screen copy, voiceover copy, product exposure, and CTA.

8. Creative Draft Confirmation
   If the user asks to make, generate, produce, render, or create a video/ad from a brief, treat it as a production request. First show the proposed concept, selected hook, beat sheet, visual direction, voiceover/caption draft, CTA, and audio direction, then ask the user to confirm or revise it before spending credits or generating final media. The confirmation question must explicitly say that approval will move into finished video production; do not frame the next step as only a "production package" unless the user asked for files/prompts only.

9. Production Tool Selection
   After creative draft confirmation, ask which image, video, voiceover, BGM/SFX, and assembly tools or models the user wants to use if they have not already specified them. A brief approval such as "yes", "ok", "confirm", "approved", "好呀", "可以", or "确认" approves only the creative draft; it is not permission to choose default tools. If production tools are missing, ask the tool-selection question and stop before any production-stage action. Do not ask whether those tools support specific parameters; inspect access and capabilities yourself only after the user selects tools or explicitly says the agent may choose.

10. Product Reference Gate
   Before any image or video generation that depicts a specific product, collect at least one usable product reference image from the source page, PDF, provided files, brand assets, or user upload. Pass the product image into the generation tool when the chosen tool supports image references. If the chosen tool cannot use image references, use it only for backgrounds/non-product shots and composite the exact product image in post, or ask the user to choose/approve a different production path. Do not invent the product appearance from text alone.

11. AI Prompt Pack
   If AI visuals or audio assets are needed, create prompts using `references/prompt-templates.md` and the generation rules in `references/asset-generation.md`. Keep the workflow tool-neutral; do not bake a provider-specific model or parameter into the skill unless the user explicitly names it for the current job.

12. Editing Brief
   Give an editor or editing agent precise instructions for pacing, subtitles, product lockup, sound, CTA, safe area, aspect ratio, and end card.

13. Audio And Caption Post
   Plan voiceover, BGM, sound effects, ambience, captions, CTA cards, product overlays, and replacement paths for production-quality audio tools. Default BGM is on unless the user opts out; sound design should still include realistic action sounds and ambience.

14. Compliance QC
   Review claims, unsupported promises, regulated categories, before/after risk, testimonial risk, misleading scarcity, and platform sensitivity using `references/compliance-qc.md`.

15. Iteration
   Run at least one self-review pass using `references/iteration-loop.md` when producing a full ad package or generated media.

16. Production Or Delivery
   For a production request, continue into video generation, audio generation, assembly/rendering, QC, and final video delivery after confirmation and tool selection. For a planning request, return a package with brief, angle matrix, hooks, storyboard, visual prompts, editing brief, QC scorecard, and testing notes.

## Tool Selection Gate

Tool selection is a hard gate between creative approval and production.

- Do not infer tools from the local environment, installed CLIs, available APIs, or previous examples.
- Do not start asset downloading for production, image/video generation, voiceover generation, BGM/SFX generation, render/assembly project creation, assembly, or final export before this gate is answered.
- If the user already named tools earlier, restate the choices and ask for confirmation before production.
- If the user says "you choose", "use defaults", "你来选", or "用默认", then choose sensible available tools, state the choices, and continue.
- If tool choices are missing, ask a concise selection question and stop.

Required question shape:

`Creative direction confirmed. Before I start making the video, which tools/models should I use for image/video generation, voiceover, BGM/SFX, and final assembly? If you want me to choose, say "use defaults".`

Chinese shape:

`创意方向已确认。进入成片制作前，请先告诉我：生图/生视频、旁白、BGM/SFX、最终合成分别用哪些工具或模型？如果你想让我决定，请明确说“你来选”或“用默认”。`

## Default Output Package

When the user asks for a full package, produce:

- Creative brief.
- Audience and offer summary.
- 5-10 hooks.
- 3-6 creative angles.
- 1-3 storyboard variants.
- Creative draft confirmation question when moving into production.
- AI image/video prompt pack when relevant.
- Model selection and access notes when asset generation is requested.
- Editing brief.
- Compliance QC scorecard.
- Testing plan for first launch.

## Required Production CTA

When the user asked for a video/ad, end the creative draft with a direct production CTA in the user's language:

- Ask whether the user confirms the creative direction or wants revisions.
- State that confirmation will move into finished video production, not only prompt or document generation.
- Tell the user the next step is choosing or confirming image/video, voiceover, BGM/SFX, and assembly tools.
- Avoid saying only "I can make a production package" unless the user asked for prompts, files, or an editor handoff instead of a rendered video.

Example shape:

`If you confirm this direction, I can continue into finished video production. Next I will ask which image/video, voiceover, BGM/SFX, and assembly tools you want to use, then generate assets, assemble the cut, run QC, and deliver the video.`

## Reference Loading Guide

- Read `references/intake.md` when the input is incomplete or messy.
- Read `references/product-page-extraction.md` when the input is a URL, marketplace page, Amazon listing, app store page, or landing page.
- Read `references/offer-and-audience.md` when the product, buyer, or offer is unclear.
- Read `references/creative-angles.md` before generating ad angles.
- Read `references/storyboard-formats.md` before building beat sheets.
- Read `references/prompt-templates.md` when AI image or video prompts are requested.
- Read `references/asset-generation.md` when the user asks for image/video assets or names a generation tool.
- Read `references/editing-brief.md` before writing production handoff notes.
- Read `references/audio-post-production.md` when the user wants VO, BGM, sound effects, or a finished ad cut.
- Read `references/remotion-captioning.md` when the user mentions Remotion or wants motion captions / timed typography.
- Read `references/compliance-qc.md` for sensitive categories or final review.
- Read `references/human-approval-gates.md` when moving from draft to production.
- Read `references/iteration-loop.md` before revising a full package or generated asset set.
- Read `references/delivery-checklist.md` before final packaging.

## Template Assets

Use these Markdown templates when the user wants files or a structured package:

- `assets/creative-brief-template.md`
- `assets/source-ledger-template.md`
- `assets/storyboard-template.md`
- `assets/voiceover-template.md`
- `assets/audio-post-template.md`
- `assets/qc-scorecard-template.md`
- `assets/launch-test-plan-template.md`

## Human Review Default

Draft mode can run without stopping for approval. Production mode should pause once for creative draft confirmation before generating final media, then ask for tool/model choices and continue into production when access is available. Use clear review gates for product facts, claim boundaries, angle selection, asset generation spend, and final launch readiness.
