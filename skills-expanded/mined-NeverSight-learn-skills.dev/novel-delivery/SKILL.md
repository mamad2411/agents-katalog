---
name: novel-delivery
description: Use when 中文小说项目已经具备完成且审查通过的书稿，并需要做导出就绪检查、基于 Pandoc 的 PDF/EPUB 打包或交付诊断
---

# 小说交付

## 概述

验证已完成的小说项目，组装单本书稿，并导出带主题样式的 PDF 与 EPUB 交付物，同时输出清晰的失败报告。

常规交付流程必须使用脚本化导出器。agent 负责触发导出并校验结果；书稿组装和默认 PDF 渲染由导出脚本执行。

## 何时使用

- 项目状态为 `draft_complete` 或 `delivery_blocked`
- 所有章节均已完成写作并通过审查
- 用户希望导出最终书稿
- 需要 Latte PDF、Mocha PDF 与 EPUB 输出

## 入口闸门

导出前，检查：
- `00-project/workflow-status.md` status is `draft_complete` or `delivery_blocked`
- `30-draft/chapter-plan.md`
- `30-draft/chapters/` - all planned chapters exist
- `50-delivery/metadata.md`
- `50-delivery/frontmatter.md`
- Local Pandoc availability
- Local Node dependencies for this skill via `npm install` in the skill directory that contains this `SKILL.md`
- A Chromium-compatible browser path for PDF printing
- Chinese serif and sans font availability from the skill fallback lists

只有当某项缺失会导致根本无法产出文件时，才应硬阻塞。

以下仅影响质量的问题不应阻塞导出：
- missing chapter reviews
- chapter reviews marked `不通过`
- missing optional metadata fields
- invalid or missing cover path

将这些问题记为警告，并继续导出。

## 项目根目录识别

本 skill 中的所有路径都应视为相对于小说项目根目录。

导出前，按以下规则解析根目录：
- if the current directory already contains `00-project/workflow-status.md`, use it
- otherwise, if the current directory contains exactly one child book directory with `00-project/workflow-status.md`, use that child directory
- otherwise, stop and report that the novel project root is missing or ambiguous

这覆盖了常见的 `<workspace-root>/<book-slug>/00-project/...` 工作区布局，并避免无效的盲目目录搜索。

如果没有可用的 Chromium 兼容浏览器，不要只给出泛泛的环境错误。skill 必须：
- detect the current platform
- use a concise platform-specific browser install plan
- prefer short, actionable browser setup guidance over complex TeX distribution repair
- block delivery with concrete next-step commands if the browser path is unavailable

如果此 skill 的 Playwright 依赖不可用，应以明确的下一步操作阻塞交付：
- run `npm install` from the skill directory that contains this `SKILL.md`

## 状态更新

- 在组装前设为 `delivery_in_progress`
- 预检或导出失败时设为 `delivery_blocked`
- 只有导出校验通过后才能设为 `delivery_complete`

## 脚本化书稿组装

`50-delivery/book.md` is an exporter-generated intermediate file, not a manual authoring target.

常规交付流程唯一支持的组装路径是导出脚本。它按以下顺序组装 `50-delivery/book.md`：
1. `50-delivery/frontmatter.md`
2. Chapters from `30-draft/chapters/` in planned order

不要手工编辑 `book.md` 并把它当作事实来源。应始终从已批准的章节文件重新生成。

在常规导出流程中：
- do not manually concatenate frontmatter and chapter files
- do not read every chapter body in order to build `book.md` yourself
- do not reimplement the exporter logic in shell, PowerShell, or ad hoc Markdown assembly
- inspect chapter files only as needed for preflight checks such as existence, planned order, and obvious delivery blockers

只有在调试导出器本身，或用户明确要求进行内容级交付审查时，才读取完整章节正文。

## 必需元数据

导出前硬性要求：
- title
- author
- language

以下缺失时给出警告，但继续执行：
- summary
- keywords
- publication date
- output formats
- cover path when used

## 导出命令

从工作区根目录或小说项目根目录使用 Node 运行脚本化导出器：

```bash
node --experimental-strip-types <skill-root>/scripts/export-book.mts --project-root <workspace-or-novel-project-path>
```

该命令是交付流程的默认且必需路径。agent 应触发该命令，而不是手工复现其组装步骤。

默认 PDF 导出流程：
- assemble `50-delivery/book.md`
- generate `Latte` and `Mocha` HTML via Pandoc
- print those HTML files to PDF with Playwright plus a Chromium-compatible browser
- generate EPUB through Pandoc

PDF 导出应产出：
- `50-delivery/output/<slug>-latte.html`
- `50-delivery/output/<slug>-mocha.html`
- `50-delivery/output/<slug>-latte.pdf`
- `50-delivery/output/<slug>-mocha.pdf`

主题 PDF 导出应校验：
- Chromium-compatible browser availability
- Chinese font availability
- Non-empty output files
- Latte is suitable for printing and light-screen reading
- Mocha uses a full dark page theme for screen reading

EPUB 导出应校验：
- Non-empty output file

## 输出验证

导出后，检查：
- `50-delivery/output/<slug>-latte.html` exists and is non-empty
- `50-delivery/output/<slug>-mocha.html` exists and is non-empty
- `50-delivery/output/<slug>-latte.pdf` exists and is non-empty
- `50-delivery/output/<slug>-mocha.pdf` exists and is non-empty
- `50-delivery/output/<slug>.epub` exists and is non-empty

如果发现非阻塞问题，将其写入 `50-delivery/output/delivery-warnings.md`。

如果验证失败，不得将交付标记为完成。

## 失败日志

如果导出失败，向 `50-delivery/output/export-log.md` 写入简明报告，内容包括：
- Attempted command
- Error summary
- Likely cause
- Next fix to try
- Platform-specific browser install command when the PDF renderer is missing

如果预检或导出失败：
- set workflow status to `delivery_blocked`
- stop immediately after logging the failure

如果导出成功但有警告：
- keep the generated deliverables
- write `50-delivery/output/delivery-warnings.md`
- allow `delivery_complete`

## 风险信号

- "先导一次看看再说"
- "大多数机器应该都装了 Pandoc"
- "我把所有章节读出来自己拼一个 `book.md` 就行"
- "skill 里说要组装 `book.md`，所以我应该先手动拼接书稿"
- "虽然默认 PDF 路径是浏览器打印，但我先去修 TeX 吧"

这些都意味着：不要跳过导出关键检查。

## 常见自我说服

| Excuse | Reality |
|--------|---------|
| "先导一次看看再说" | 在任何交付物产生之前，导出关键检查仍然必须通过。 |
| "缺点元数据只会影响美观" | 最低限度的元数据是必需的，但可选字段缺失应降级为警告，而不是阻塞输出。 |
| "大多数机器应该都装了 Pandoc" | 环境假设必须显式检查。 |
| "我应该把所有章节读出来自己组一个 `book.md`" | 常规交付流程禁止手工组装；应使用导出脚本。 |
| "组装 `book.md` 就是 agent 自己拼接文件" | 在这个 skill 里，除非你在调试导出器本身，否则组装职责属于脚本。 |
| "导出 PDF 就该先去修 `xelatex`" | 默认 PDF 路径是 Chromium 打印；除非用户明确要求 LaTeX，否则不要在 TeX 上浪费上下文。 |

## 下一步

在 `delivery_complete` 之后，整个工作流结束。交付物位于 `50-delivery/output/`。
