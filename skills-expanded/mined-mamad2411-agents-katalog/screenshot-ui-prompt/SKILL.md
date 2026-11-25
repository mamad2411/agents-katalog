---
name: screenshot-ui-prompt
description: "此技能用于：用户上传 UI 截图并希望生成精准、可直接复制的 AI 提示词（用于 v0、Lovable、Cursor、CodeBuddy、图像生成器等）以复刻该界面。它先识别截图属于前端元素（组件 / 页面 / 区块）还是非前端元素（流程图、图表、照片、文档），再确认使用设计令牌还是从图片提取配色，最后输出包含显式风格词的完整 UI/UX 交互设计提示词。触发场景：把这张图写成提示词、根据截图生成组件提示词、describe this UI as a prompt、screenshot to prompt。"
---

# 根据截图生成UI提示词 / Screenshot-to-UI Prompt Generator

## Overview

Turn a screenshot into a precise, structured AI prompt that recreates the UI. The skill enforces a
four-phase flow: **classify → confirm functional requirements (FIRST) → gather design constraints →
emit prompt**. Functional behavior (incl. 异常 / 控制) leads; an explicit **风格词 (style words)**
section is always included so the prompt carries visual authority, not just structure.

## When to Use

- User uploads an image and asks to "write a prompt", "generate a component/page prompt", or "describe
  this UI for an AI builder".
- User pastes a screenshot and wants a spec they can feed to v0 / Lovable / Cursor / CodeBuddy / image
  generators.
- Do NOT use for pure code review, or when the user only wants a verbal description (use normal reply).

## Preconditions

- The executing model MUST support vision (image input). If the model reports it cannot read images,
  stop and tell the user to switch to a multimodal model before proceeding.
- The screenshot must be available as a local file path. If the user only pasted a remote URL, download
  or fetch it locally first (e.g., via WebFetch / curl) before running the color-extraction script.

## Workflow

### Phase 1 — Analyze & Classify

1. Read the image. Identify concrete design elements: controls (button, input, dropdown, select,
   switch, tab, table, card, modal, filter builder, etc.), layout regions, typography, spacing, borders,
   shadows, rounded corners, icons.
2. Classify the screenshot into one of:
   - **组件 (component)** — a single reusable control or small composite (e.g., the filter builder from
     the example).
   - **区块 (section)** — a meaningful part of a page (header bar, sidebar, settings panel).
   - **页面 (page)** — a full screen with navigation + content + (optional) footer.
   - **非前端元素 (non-front-end)** — flowchart, mind map, org chart, photo, scanned document,
     illustration, logo, pure data chart with no UI chrome.
3. If classified as **non-front-end**, STOP and ask the user with `AskUserQuestion`:
   - Explain what the image appears to be (e.g., "这看起来是一张流程图/照片/文档，不是前端 UI 元素").
   - Offer options: (a) 仍然按 UI 提示词输出（当作参考视觉）; (b) 改为描述/提取该内容本身;
     (c) 用户提供一张真正的前端截图。 Do NOT guess silently.
4. If front-end, summarize the classification briefly to the user (one line) and proceed to Phase 2.

### Phase 2 — Confirm Functional Requirements (FIRST)

Functional behavior is the skeleton — confirm it BEFORE any visual/style decision. Ask the user with
`AskUserQuestion` (one call, up to two questions):

**Q1 — Functional scope:**
- "由我从截图推断功能" — infer behavior, states, and ESPECIALLY 异常 (exceptions: empty / no-match /
  invalid input / network failure / out-of-range / permission denied) and 控制 (control: disabled,
  loading, controlled-vs-uncontrolled, debounce/throttle, permission gating, read-only, focus/keyboard,
  max limits) from the screenshot; ALSO default the four production-grade dimensions (a11y, full-state +
  ErrorBoundary, strict component API, test/perf/docs) as MUST-cover and state every assumption explicitly.
- "我来指定功能清单" — user supplies the functional spec; you then ensure 异常 + 控制 coverage is added.
- "两者结合" — infer + let the user correct/augment.
If the user already described functionality in their message, skip this question and use theirs.

**Q2 — Exception & control emphasis (bundle if the user picked infer/combine):**
- "异常态覆盖哪些" — e.g., 空数据 / 无匹配结果 / 输入非法 / 请求失败 / 越界 / 权限不足 / 并发冲突.
- "控制态覆盖哪些" — e.g., 禁用(disabled) / 加载中(loading) / 只读(read-only) / 受控-非受控 /
  节流防抖(debounce/throttle) / 权限门禁 / 防重复提交 / 最大条数限制.
If the user picked "由我推断", pre-fill sensible defaults for both and let them trim.

Record the functional scope; it becomes the LEAD section of the emitted prompt in Phase 4.

### Phase 3 — Gather Design Constraints (tokens + style)

Ask the user (bundle into ONE `AskUserQuestion` call with up to two questions):

**Q1 — Design tokens vs. color extraction:**
- "我提供设计令牌 (Design Tokens)" — user will paste CSS variables / JSON / theme; use them verbatim.
- "从图片提取配色" — run `scripts/extract_colors.py IMAGE_PATH` to get dominant colors + a palette
  with exact hex, then use those values.
- "两者结合" — user provides tokens AND you refine/verify with extracted colors.
- "使用参考风格" — skip exact tokens; use a named reference style (see Q2 / style library).

**Q2 — Style reference (风格词):** offer a few from `references/prompt_templates.md` §风格词库, e.g.:
- 金融终端极简 (Goldman Sachs / Bloomberg): 深蓝 #0A2540, 灰白底, 像素级对齐, 高密低噪.
- Apple HIG / 现代简洁.
- Ant Design / 企业后台.
- Linear / 暗色科技.
- 用户自定义 (让用户输入风格描述).
If the user already gave style words in their message, skip this question and use theirs.

Record the chosen constraints; if "从图片提取配色" was chosen, execute the extraction script now and
capture the hex palette into the prompt.

### Phase 4 — Emit the Prompt

1. Load `references/prompt_templates.md` and pick the matching template by Phase-1 classification
   (组件 / 区块 / 页面). Fill every placeholder with the classified elements, Phase-2 functional scope,
   and Phase-3 design constraints.
2. The emitted prompt MUST contain these sections, in THIS order (functional lead, style after):
   - **组件定位** — what it is, where it lives, controlled/uncontrolled stance.
   - **功能描述（含 异常 / 控制）** — behavior, dynamic operators by field type, AND explicit sub-sections:
     异常 (empty / no-match / invalid / network-fail / out-of-range / permission / race) and 控制
     (disabled / loading / read-only / controlled-vs-uncontrolled / debounce-throttle / gating / max-limit /
     focus-keyboard / a11y). REQUIRED — never omit.
   - **入参 Props** — controlled input (fields, value, onChange, options, disabled, maxRules…).
   - **输出 / 事件** — onChange next-state, atomic callbacks, explicit "不直连 API" boundary.
   - **数据交互** — state ownership, parent linkage, debounce + query contract, empty = no filter.
   - **生产级工程要求（高可用，必填）** — a11y (semantic tags, ARIA roles, keyboard nav, focus trap
     for popovers, screen-reader text, prefers-reduced-motion); full state machine + ErrorBoundary
     (idle/loading/success/empty/error/disabled, AbortController race handling, fallback UI, onError
     hook); strict TS types + compound-component API + controlled/uncontrolled dual mode + imperative
     ref; tests (Vitest + RTL + axe) + performance (virtualization/debounce/memo) + Storybook + i18n +
     SSR-safe (useId, no window/document at render). REQUIRED for production-grade output.
   - **风格词 (Style words)** — explicit visual authority (reference style + primary + background +
     quality + vibe + UX goal). REQUIRED — never omit.
   - **布局 / 结构** — regions, toolbar, panel, grid.
   - **组件 / 页面要素** — the identified controls, with their states.
   - **配色 / 设计令牌** — exact hex from tokens or extraction.
   - **字体 / 排版** — family, sizes, monospace for numbers if density matters.
   - **交互（视觉层）** — hover/focus/click, add/delete, AND/OR, empty states.
   - **技术栈** — React + TS + Tailwind (or named lib), component name, controlled props.
3. Output the prompt in **Chinese first**, then provide an **English version** (for v0 / Lovable / 国际
   工具). Wrap each in a fenced code block so the user can copy directly.
4. After emitting, offer next steps: "要我直接生成该组件/页面的代码预览吗？" or "要补一份纯设计稿提示词吗？"

## Output Quality Rules

- **Functional requirements are confirmed BEFORE visual style.** In the workflow, Phase 2 (functional)
  precedes Phase 3 (style/tokens); in the emitted prompt, the 功能描述 section leads all visual sections.
- Always include the **功能描述（含 异常 / 控制）** section for any component or page prompt. A shippable
  prompt specifies: behavior, **异常** (empty / no-match / invalid / network-fail / out-of-range /
  permission / race), **控制** (disabled / loading / read-only / controlled-vs-uncontrolled / debounce /
  gating / max-limit / focus-keyboard / a11y), controlled Props (input), emitted events/output, and the
  data-interaction boundary. Visual-only prompts are rejected as incomplete.
- Always include the **风格词** section — a prompt with only structure is weak; visual authority comes
  from explicit style words.
- Always include the **生产级工程要求（高可用）** section. A prompt intended for real frontend-page
  development MUST mandate: a11y, full-state machine + ErrorBoundary, strict component API
  (controlled/uncontrolled + compound pattern), and test/perf/docs (Vitest+RTL+axe, virtualization,
  debounce, Storybook, i18n, SSR-safe). Happy-path-only prompts are rejected as non-production-grade.
- Use exact hex values, never vague color names, when tokens/extraction are available.
- Keep prompts self-contained and copy-pasteable; no markdown outside the code fences for the prompt body.
- Preserve the source language of the user's request for the primary version.

## Resources

### scripts/extract_colors.py
Deterministic dominant-color + palette extractor. Run:
`python3 scripts/extract_colors.py IMAGE_PATH [--colors N]`
Outputs a ranked palette with hex, RGB, and an approximate role label (background / surface / primary /
text / accent). Use it in Phase 2 when the user chooses "从图片提取配色".

### references/prompt_templates.md
Ready-to-fill prompt templates for 组件 / 区块 / 页面, plus a 风格词库 (style-word library) with
concrete examples (financial-terminal, Apple HIG, Ant Design, Linear, etc.). Load this in Phase 3.
