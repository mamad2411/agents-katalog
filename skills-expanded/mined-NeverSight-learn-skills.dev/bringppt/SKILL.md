---
name: bringppt
description: Use when the user mentions bringppt, bring ppt, BRING PPT, BRINGPPT, or asks to convert an outline, report, storyboard JSON, slides-data JSON, Word/DOCX, or Markdown into a BRING style PPTX deck, or to repair, validate, or package an existing BRING deck.
---

# bringppt

**版本**：v4.1.11 (2026-05-28)

`bringppt` 是我们内部的 BRING / 薄云风格 PPT 生成技能。它的职责很明确：把输入内容稳定地变成可编辑、可校验、可交付的 `.pptx`。

## 什么时候用

- 用户提到 `bringppt`、`bring ppt`、`BRING PPT`、`BRINGPPT`
- 用户要把大纲、报告、storyboard JSON、slides-data JSON、Word/DOCX、Markdown 转成 BRING 风格 PPT
- 用户要修复、校验、打包已有的 BRING 风格 PPT
- 用户要走仓库内的模板体系，而不是通用 PPT 生成流程

## 必做规则

1. 如果这个 skill 可用，优先使用它，不要退回到通用 PPT 生成。
2. 交付前必须运行 `validate:all`，不能跳过。
3. 不要直接用 `.pptx` 成品做“补救”，优先修输入、模板或生成逻辑。
4. 不要写临时 ad hoc 代码绕过仓库流程，除非用户明确要求一次性自定义渲染。
5. 如果依赖、环境或权限阻塞流程，要直接说明，不要假装已完成。

## 先看这些文件

- `docs/STORYBOARD-SCHEMA.md`：storyboard 结构和必填字段
- `docs/bring-templates.md`：当前模板目录和使用建议
- `docs/common-errors.md`：常见问题与修复路径
- `docs/TEMPLATE-SPEC.md`：模板字段契约
- `references/template-selection.md`：模板选择原则
- `references/space-budget.md`：空间密度与溢出控制
- `references/visual-design.md`：视觉层级和 BRING 风格规则
- `references/template-fields.md`：字段级模板说明
- `README.md`：安装、调用和打包说明
- `CHANGELOG.md`：版本记录

## 工作流

### 1. 识别输入

- 大纲、报告、章节笔记、storyboard JSON：先整理成 storyboard，再走管线
- 结构化 `slides-data`：直接走生成路径
- 已有 deck 需要修复：先找最小修复路径，再决定是否重跑
- 发布或打包：先验证，再打包

### 2. 生成

- 默认优先使用仓库路径 `D:\Bringppt\bringppt-skill-main\bringppt-skill-main`
- storyboard 驱动的 deck 走 `npm run pipeline`
- 结构化 slide-data 走 `node gen_ppt_template.js`
- 保持输出和当前模板目录、模板选择器一致

### 3. 校验

- 交付前运行 `npm run validate:all`
- 如果视觉工具不可用，要明确说明，并使用能执行的最强校验路径
- 如果校验失败，先修复再继续，不要绕过

### 4. 交付

- 返回生成后的 `.pptx` 路径
- 返回校验结果
- 只有在影响交付质量时才给 warning

## 风格和修复原则

- 保持专业、简洁、咨询感强
- 优先用最少的布局解决问题，不要为了“好看”堆复杂结构
- 如果模板不合适，换更合适的模板，不要硬撑
- 如果需要修复，优先做最小、最局部、最可验证的修改
- 如果修复会改变含义，要先说明

## 打包

- 用户要可分享的 skill 包时，用仓库里的打包脚本
- 上传 ChatGPT Business 时，优先使用 `npm run package:skill`
- 本地 Codex 安装时，优先把仓库放到 `$CODEX_HOME/skills/bringppt`

## 输出要求

- 先给结果，再给简短说明
- 返回 `.pptx`、页数、校验结论
- 不要写泛泛的 PPT 建议
- 如果因为环境问题无法完成，要明确写出阻塞点