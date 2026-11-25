---
name: presentation-script-coach
description: Turn an existing PPT, slides file, or strategy brief into a tailored speaking strategy, natural page-by-page verbatim script, transitions, Q&A prep, rehearsal notes, and non-destructive PPT/slides revision suggestions. Reads charts, diagrams, and screenshots on the pages via multimodal page images, so image-heavy PPT/slides get real scripts, not placeholders. Use when the user provides or references a PPTX, PDF, HTML presentation, slides, speaker notes, or `presentation-report-preflight` brief and asks for a 汇报逐字稿, 讲稿, 口播稿, speaker script, 按页讲解, 看图讲解, 图表怎么讲, 演讲策略, 汇报策略, 答辩话术, 路演话术, 销售提案讲法, Q&A preparation, rehearsal plan, 说人话, 自然一点, 不要太像 AI, 提词器, teleprompter, speaker notes, 备注注入, T 键弹窗, 提词卡, cue cards, 汇报辅助, or advice on how to present existing PPT/slides to a specific audience, occasion, industry, duration, or decision-maker.
---

# Presentation Script Coach

## Objective

Create a `Presentation Speaking Brief` from existing PPT/slides or a presentation strategy brief. The deliverable answers: "How should these slides be spoken in this room, for this audience, to achieve this outcome?"

This skill is a companion to `presentation-report-preflight`, but it stands alone. It does not design, generate, or edit slides. It produces speaking strategy, page-level scripts grounded in what is actually visible on each page (including charts, diagrams, and screenshots read via multimodal page images), transitions, Q&A defense, rehearsal guidance, diagnostic revision suggestions, and, after script approval, optional presentation-assist derivatives for HTML/PPTX plus printable cue cards.

## Core Rules

1. Existing PPT/slides first: extract text AND read the page visuals of the provided PPTX, PDF, HTML, or preflight brief before asking questions.
2. Do not edit source files: output advice and scripts only unless the user explicitly invokes another skill to revise the PPT/slides.
3. Scene drives wording: tailor the script to audience, occasion, industry, duration, desired action, and speaker role.
4. Page-by-page means every usable page gets a speaking job, time budget, verbatim script, transition, compressed version, and likely Q&A.
5. Keep revision suggestions non-destructive: identify the page, issue, live-room risk, suggested fix, and priority.
6. Do not invent facts, numbers, customer names, ROI, legal claims, or industry context. Mark uncertain items as `to_verify` or `present_without_source`. Numbers that you can only see in an image (chart labels, screenshot text) get claim_status `read_from_image`; cross-check them against extracted text, and when the image is small or blurry, treat the value as `to_verify` and use conservative spoken wording ("大概在……量级").
7. You are a multimodal agent: for image-only, chart, diagram, or screenshot pages, obtain the page visual through the Visual Access Strategy and read it before writing the script. Only fall back to a placeholder script when no visual channel works, and then keep the page marked `image_only`/`needs_ocr` honestly — never pretend to understand a page you could not see.
8. In `interactive` mode, do not generate the full page-by-page script immediately. After extraction, visual reading, and speaking-context inference, stop at a `需求确认卡` and wait for the user to confirm or correct it. If the user says "直接给", "别问", "先出稿", "just make it", or similar, continue in `run_mode: autonomous` and record assumptions.
9. Create spoken language, not essay prose. Scripts should be natural to read aloud: short sentences, clear pauses, signposting, and audience-aware emphasis.
10. Always identify the weakest 1-2 live risks instead of reporting an all-green checklist.
11. Protect information before style: preserve numbers,口径, names, source caveats, commitments, responsibilities, and exact asks before making the script more colloquial.
12. Remove AI-ish performance: avoid formulaic openers, exaggerated empathy, slogan endings, fake authority, rigid three-part lists, and "not only... but also..." style set pieces unless the source slide truly requires them.
13. Do not build presentation-assist outputs until the user confirms the page-by-page script is acceptable.
14. Presentation-assist outputs are always derived files: HTML uses a T-key popup teleprompter (with in-page overlay fallback), PPTX writes managed speaker notes, cards writes printable presenter cue cards. Never overwrite source files by default.
15. In `interactive` mode with more than ~8 pages, confirm tone with 1-2 sample page scripts before writing the whole presentation; a 30-page script in the wrong voice is expensive to redo.
16. Before final delivery, run `scripts/check_timing.py` against the contract JSON and reconcile the estimate with `runtime_plan` — do not hand over a "15 分钟" script that reads out at 22 minutes.
17. After delivering the approved-script draft and contract, always ask the user to choose the next presentation-assist action: HTML teleprompter, PPTX speaker notes, cue cards, or no assist output for now. Do not stop right after producing JSON.

## Reference Routing

Load only what the task needs:

| Need | Read |
| --- | --- |
| Choose audience/occasion strategy | `references/delivery-playbooks.md` |
| Write page-level verbatim scripts, transitions, compressed versions, tone variants, or chart-walkthrough lines | `references/script-writing-guide.md` |
| Make scripts more natural, colloquial, and less AI-like while preserving facts | `references/natural-speech-guide.md` |
| Diagnose PPT/slides issues (incl. visual checks) and revision suggestions | `references/slides-diagnosis-guide.md` |
| Render pages to PNG for visual reading | `scripts/render_page_images.py` |
| Verify spoken duration vs. time budget | `scripts/check_timing.py` |
| Build an approved HTML teleprompter, PPTX speaker-notes derivative, or cue cards | `scripts/build_presentation_assist.py` |
| Validate the machine-readable contract | `references/speaking-brief.schema.json` |
| Need a complete model output | `references/example-speaking-brief.md` |

If a `presentation-report-preflight` brief is provided, use its scenario, audience, desired action, title chain, evidence plan, runtime plan, and open questions as high-priority context. Do not require preflight output.

Scripts declare inline dependencies (PEP 723): if the current Python lacks `python-pptx`/`pdfplumber`/`lxml`/`pymupdf`, run them with `uv run scripts/<name>.py ...` instead of `python`.

## Workflow

### Phase 0 - Detect Input And Run Mode

Classify the source:
- `pptx`: local PowerPoint / PPT slides file.
- `pdf`: exported slides or handout.
- `html`: HTML slides.
- `strategy_brief`: `presentation-report-preflight` brief or similar Markdown/YAML.
- `mixed`: multiple sources.

Detect `run_mode`:
- `interactive`: user can answer; after source extraction and inference, a confirmation gate is required before writing the full page-by-page script.
- `autonomous`: headless context, downstream invocation, or speed keywords ("直接给", "别问", "先出稿", "just make it"); state assumptions and continue.

Detect `output_language` from the user prompt and source material. Human-readable sections and scripts follow `output_language`; YAML keys remain English.

Choose `script_tier`:
- `lite`: quick internal sync, under ~8 slides, or under ~10 minutes.
- `standard`: default; full page-by-page scripts with concise diagnostics.
- `full`: high-stakes pitch, promotion defense, board/customer/investor presentation, or explicit rehearsal/coaching need.

### Phase 1 - Extract PPT / Slides Context

For PPTX, PDF, or HTML files, run:

```bash
python scripts/extract_slides_context.py /absolute/path/to/slides.ext \
  --out /absolute/path/to/slides-context.json \
  --assets-dir /absolute/path/to/slides-assets
```

(`--assets-dir` exports embedded images — PPTX pictures, HTML data-URIs — so you can read them directly. Use `uv run` if dependencies are missing; in Codex desktop, prefer the bundled Python returned by `load_workspace_dependencies` when available.)

Use the JSON as the page inventory. If extraction fails, inspect the file with the best available format-specific tools and record the extraction limitation in `slides_context.extraction_warnings`.

The extraction JSON is evidence about the PPT/slides, not a script. It should include page number, title, text blocks, tables, speaker notes, image hints, embedded image paths, status, warnings, `source_page_id`, `title_hash`, and `content_hash`. PPTX pages should also carry `slide_id`; HTML pages should also carry `html_locator`.

### Phase 1.5 - Visual Reading Pass

You are a multimodal agent; the text extraction above is deliberately blind to charts, diagrams, screenshots, and layout. Close that gap here, using the cheapest reliable visual channel per format — full-page rendering is the high-fidelity fallback, not a mandatory step:

| Source | First choice (cheap) | Fallback (high fidelity) |
| --- | --- | --- |
| `pdf` | Read the PDF file directly page by page if your harness renders PDF pages visually | `python scripts/render_page_images.py slides.pdf --out-dir .../page-images` then read the PNGs |
| `pptx` | `render_page_images.py` (LibreOffice → PDF → PNG). Required for pages with native charts/diagrams — they are invisible to both text extraction and embedded-image export | If LibreOffice is unavailable: read `embedded_images` from Phase 1, and mark chart pages `needs_visual_render` in warnings |
| `html` | Read the HTML source (markup, inline SVG, and styles are model-readable) plus the local image files listed in `embedded_images` | `render_page_images.py` (Playwright screenshots) when pages contain canvas/JS-drawn charts or when layout emphasis matters |

Coverage by `script_tier`:
- `lite`: read visuals only for pages whose status is `image_only`/`needs_ocr`/`partial` or whose hints mention charts/canvas.
- `standard`: those pages plus every page that has any image, chart, or table screenshot.
- `full`: every page, preferring full-page renders — layout tells you what the audience will look at first, which shapes the script.

Read images in batches (multiple images per read call) to control context cost.

For each visually read page, record into `slides_context.pages[]`:
- `visual_summary`: 2-4 sentences — what is actually shown, and the one-line takeaway the visual is arguing ("这张图要说的一句话");
- `visual_claims`: key numbers/facts readable only from the visual, each with `confidence` (`high`/`medium`/`low`) and `needs_verification` when small print or blur is involved;
- update `status` to `visually_read` when the visual was successfully understood;
- note visual emphasis when relevant (the biggest number, the highlighted bar, the reddest cell) — scripts should direct the audience's eyes there.

Provenance discipline: a `high`-confidence visual claim that matches extracted text may be spoken as fact. A number that exists only in an image keeps claim_status `read_from_image`; a `low`-confidence one is spoken conservatively and listed in `open_questions`/`to_verify`. Never let the visual pass silently overwrite a number that came from extracted text.

### Phase 2 - Infer Speaking Context

Infer first:
- scenario: sales proposal, investor pitch, promotion defense, quarterly review, technical talk, training, consulting delivery, retrospective, case study, etc.;
- audience: executives, customers, investors, judges, colleagues, learners, technical peers, public;
- industry or domain;
- desired action or decision;
- success criteria;
- total duration and Q&A reserve;
- speaker role and relationship to audience;
- tone: executive, consultative, confident, educational, defensive, inspiring, technical, candid.

If essential context is missing and `run_mode: interactive`, include it in the `需求确认卡` as `待确认问题`; do not write the full script in the same turn. If `run_mode: autonomous`, continue with explicit assumptions and record them in `open_questions`.

### Phase 3 - Demand Confirmation Card

Before the full script, output a compact `需求确认卡`. In `interactive` mode this is a hard stop: do not continue into diagnosis, sample scripts, or full page-by-page scripts until the user confirms, corrects, or explicitly says to skip confirmation.

The card must include:
- 汇报场景;
- 听众;
- 行业 / 领域;
- 汇报目标 / 希望对方做什么;
- 总时长 / Q&A 预留;
- speaker 身份;
- 推荐口吻;
- 关键假设;
- 待确认问题;
- 下一步提示: "确认后我再生成完整逐页稿；如果你想跳过确认，可以说'直接给'。"

In `autonomous` mode, skip the hard stop, continue, and record the confirmation gate as skipped by user instruction.

After the user confirms or corrects the card, continue from the confirmed context. Do not repeat the confirmation card unless the source file changes, pages are reordered, or the user changes audience, duration, goal, or tone.

### Phase 3.5 - Sample Script Confirmation (interactive, larger slide files)

When `run_mode: interactive` and the PPT/slides file has more than ~8 usable pages, write 1-2 sample page scripts first — pick one high-stakes page (the core claim or ask) and one ordinary page — and ask the user to confirm tone, density, and person ("这个口吻对吗?"). Apply the feedback, then write the rest. Skip this phase in `autonomous` mode or for small slide files.

### Phase 4 - PPT / Slides Diagnosis

Read `references/slides-diagnosis-guide.md` before producing revision suggestions. Diagnose at page level:
- topic title vs conclusion title;
- missing source, unit, baseline, or data口径;
- overloaded page;
- weak CTA or unclear decision request;
- unsupported claim;
- logic jump between pages;
- likely Q&A risk;
- visual issues you saw in the page images: chart contradicts the title's claim, unreadable font/legend at room distance, chart junk, sensitive information visible in screenshots.

Prioritize suggestions with `must_fix`, `should_fix`, or `nice_to_have`. Do not make the PPT/slides worse by suggesting rewrites that exceed the user's stated scope.

### Phase 5 - Page-by-page Script

Read `references/script-writing-guide.md` and `references/natural-speech-guide.md`. For every usable page, produce:
- page purpose;
- recommended talk time;
- verbatim script;
- transition into or out of the page;
- compressed version for a short run;
- must-keep points;
- likely question and answer direction.

For chart, diagram, or screenshot pages that were visually read, write a real chart-walkthrough script (see the 看图话术 pattern in `script-writing-guide.md`): orient the audience ("左边这张是过去四个季度的留存"), point ("重点看三月这个拐点"), then land the takeaway — the one-line conclusion from `visual_summary`. Do not narrate every data point.

Only pages that remained `image_only`/`needs_ocr` after the Visual Reading Pass get a safe placeholder script based on surrounding context, with an explicit statement of what must be verified.

After drafting page scripts, run a naturalness pass:
- protect facts,口径, responsibilities, and exact asks;
- remove formulaic AI phrasing and over-polished transitions;
- remove repeated page-level openings such as "这一页讲...", "本页主要...", and "这页展示..."; if the full script uses `这一页` / `本页` / `这页` more than 3 times in spoken lines, rewrite until the repetition is gone unless the phrase is needed for visual pointing or a compressed summary;
- make the wording sound like a specific presenter speaking in this room;
- reread for factual drift before final delivery.

### Phase 6 - Q&A And Rehearsal Plan

Prepare Q&A for high-risk pages:
- market size, financial forecast, ROI, benchmark, competitor comparison, customer case, legal/security/compliance claim, personal contribution, resource request, implementation risk, or limitation.

Build rehearsal guidance:
- 3 pages to practice most;
- likely overrun points;
- numbers or claims needing source confirmation;
- 5-minute compression path;
- opening hook and closing ask.

### Phase 7 - Contract, Timing Check, And Validation

Always write the machine contract as `presentation-speaking-brief.contract.json`, containing all required top-level fields plus `slides_context.pages[]` (with `visual_summary`/`visual_claims` where produced) and page identity fields in `page_scripts[]`. Validate required fields and enum values against `references/speaking-brief.schema.json` before final delivery.

Then run the deterministic timing check:

```bash
python scripts/check_timing.py --contract /absolute/path/to/presentation-speaking-brief.contract.json
```

If it reports `OVERRUN`/`UNDERRUN` (or flags individual pages), rebalance the scripts or the time budgets before delivering — trimming the verbatim script beats silently shipping an unspeakable plan. Record the result in the contract's `timing_check` field. If the user explicitly accepts the mismatch, record that in `open_questions`.

In the human-readable Markdown, include only a compact `Speaking Handoff Contract` summary (tier, mode, source, language, durations, page count) plus a pointer to the JSON file — do not paste the full pages/page_scripts arrays into the Markdown.

After the contract summary, always include `下一步汇报辅助` with source-aware choices:
- `html`: ask whether to generate `*.teleprompter.html`; mention the presenter presses `T` to open an independent popup teleprompter.
- `pptx`: ask whether to generate `*.with-notes.pptx`; mention scripts are written to matching speaker notes while preserving existing notes.
- `pdf` or `strategy_brief`: ask whether to generate printable `cue-cards.md`.
- `mixed`: list the applicable HTML/PPTX/card choices for the detected files; if no injectable file is available, offer cue cards only.
- Always include "暂不生成辅助文件" as an option. State that assist outputs require the user's script approval and never overwrite the source by default.

Required top-level fields:
- `script_tier`
- `run_mode`
- `source_type`
- `output_language`
- `slides_context`
- `speaking_context`
- `runtime_plan`
- `page_scripts`
- `revision_suggestions`
- `qa_plan`
- `rehearsal_plan`
- `naturalness_pass`
- `weakest_links`
- `references_consulted`
- `open_questions`

### Phase 8 - Optional Presentation Assist Output

Run this phase only after the user confirms the page-by-page script is correct.

If `source_type: html`, build a derived HTML file with a T-key teleprompter popup:

```bash
python scripts/build_presentation_assist.py html \
  --source /absolute/path/to/input.html \
  --contract /absolute/path/to/presentation-speaking-brief.contract.json \
  --out /absolute/path/to/input.teleprompter.html
```

The generated HTML must not show the script on the main screen. The presenter presses `T` to open an independent popup window, can drag that window to another display, and the popup syncs to the current page as the HTML slides advance. The popup shows the page's time budget with a live elapsed timer (turns red on overrun), the must-keep list, and has font-size controls. If the popup is blocked, pressing `T` toggles a hidden side overlay in the main window instead (`Esc` closes it). Reveal.js pages use the Reveal API/events; other HTML slide pages use best-effort page detection.

If `source_type: pptx`, build a derived PPTX with speaker notes:

```bash
python scripts/build_presentation_assist.py pptx \
  --source /absolute/path/to/input.pptx \
  --contract /absolute/path/to/presentation-speaking-brief.contract.json \
  --out /absolute/path/to/input.with-notes.pptx
```

The PPTX writer preserves existing notes and adds/replaces only the managed block between `PRESENTATION SCRIPT COACH START` and `PRESENTATION SCRIPT COACH END`.

If `source_type` is `pdf` or `strategy_brief`, build printable presenter cue cards instead (also useful as a print companion for any source type):

```bash
python scripts/build_presentation_assist.py cards \
  --contract /absolute/path/to/presentation-speaking-brief.contract.json \
  --out /absolute/path/to/cue-cards.md \
  --source /absolute/path/to/slides.pdf
```

(`--source` is optional for cards but re-checks page identity when given.) Offer conversion to HTML or PPTX only when the user wants the live teleprompter or injected speaker notes.

Before writing any assist file, `build_presentation_assist.py` re-extracts the source and validates page count, page IDs, title hashes, and content hashes. If the PPT/slides changed after script approval, stop and ask the user to regenerate or confirm the mapping.

## Output Format

Prefer writing or returning a Markdown file named `presentation-speaking-brief.md`.

Use this order:

````markdown
# Presentation Speaking Brief

## 汇报策略摘要
- 一句话目标：
- 听众最关心：
- 现场打法：
- 推荐语气：
- 总时长：
- 最大风险：

## Direction Snapshot
- 这场汇报应该怎么赢：
- 哪些页要慢讲：
- 哪些页要快讲 / 可跳过：
- 最可能被追问：
- 关键假设：

## PPT / Slides 诊断与改稿建议
| 页码 | 问题 | 现场风险 | 建议改法 | 优先级 |
| --- | --- | --- | --- | --- |

## Timing Brief
| 部分 | 页码 | 建议时长 | 讲法 |
| --- | --- | --- | --- |

## Page-by-page Verbatim Script
### 第 1 页：<标题>
- 本页目的：
- 页面画面：<这页实际展示什么(来自视觉阅读);纯文字页可省略>
- 建议时长：
- 逐字稿：
- 转场句：
- 压缩版：
- 必须保留：
- 可能追问：
- 回答方向：

## Q&A / 追问攻防
| 问题 | 风险 | 建议回答 | 需要补充 |
| --- | --- | --- | --- |

## 彩排自检
- 最需要练熟的 3 页：
- 最容易超时的地方：
- 最需要补来源的数字：
- 5 分钟压缩版讲法：
- 时长核算：<check_timing.py 结果:全稿估算 vs 计划>

## 自然度回读
- 已保护的信息：
- 已压掉的 AI 味：
- 仍需人工确认的口吻：

## 交付前自检（最弱环）
- 最可能翻车处 1：
- 最可能翻车处 2：

## Speaking Handoff Contract
- 完整机器契约见 `presentation-speaking-brief.contract.json`（含 slides_context.pages、page_scripts、visual_summary 等）。

```yaml
script_tier: standard
run_mode: interactive
source_type: pptx
output_language: zh
page_count: TBD
visually_read_pages: TBD
runtime_plan:
  total_duration: TBD
  talk_time: TBD
  qa_time: TBD
timing_check:
  status: TBD  # ok / overrun / underrun
  estimated_talk_time: TBD
contract_file: presentation-speaking-brief.contract.json
```

## 下一步汇报辅助
- 这版逐字稿如果你确认没问题，我可以继续生成：
- HTML 源文件：`*.teleprompter.html`，按 `T` 打开独立提词器弹窗。
- PPTX 源文件：`*.with-notes.pptx`，把逐字稿写入对应页备注并保留原备注。
- PDF / strategy brief：`cue-cards.md`，生成可打印提词卡。
- 也可以选择暂不生成辅助文件。
````

## Quality Bar

A good output:
- contains concrete page-by-page scripts, not generic presentation advice;
- is grounded in what each page actually shows — chart pages get real chart-walkthrough lines ("先看左边的趋势,重点是三月这个拐点"), not "这页展示了我们的数据";
- adapts wording and defense posture to the audience and room;
- sounds like a person speaking, not a polished AI essay or generic consultant memo;
- does not repeat mechanical page openers across the script; avoid recurring "这一页讲...", "本页主要...", and "这页展示..." phrasing in spoken lines;
- gives each page one speaking job and a realistic time budget that survives `check_timing.py`;
- includes transitions so the talk does not sound like isolated slide narration;
- marks weak evidence and uncertain claims honestly, including numbers read from images;
- gives non-destructive PPT/slides revision suggestions with priority;
- includes compressed versions for time cuts;
- prepares Q&A for high-risk claims;
- names the 1-2 weakest live risks.
