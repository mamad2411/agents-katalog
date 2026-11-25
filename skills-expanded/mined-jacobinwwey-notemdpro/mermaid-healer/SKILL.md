---
name: mermaid-healer
description: Validate Mermaid and conservatively repair invalid flowcharts without damaging Markdown.
---

# Mermaid healer

## English

Use `mermaidProcessor.ts` from the complete repository after `npm ci`. Individual skill installation supplies instructions, not the shared helper dependencies.

1. Read the authorized source and preserve it until validation succeeds.
2. Run `checkMermaidErrors(content)`: it uses the real Mermaid parser and counts incomplete Mermaid fences as errors. Matching backtick/tilde fence lengths determine ownership; examples inside other fences are protected.
3. Run `refineMermaidBlocks(content)`. Valid blocks stay byte-identical. In invalid, closed flowcharts, automatic repair only changes a complete bare-ID edge `A --|> B` to `A --> B`, then requires parsing to succeed. Labels and unrelated punctuation remain unchanged. Unknown families, other syntax errors and unclosed blocks stay intact for explicit review.
4. Validate again before writing. Do not claim an unresolved parse error was fixed. A renderer/parser unavailable in the host is an unavailable capability, not success.

Never delete parentheses, braces, quotes, nodes or relationships to make a diagram pass. Public legacy fixer exports remain for compatibility; `applyDeepDebugToMermaidBlocks` is an explicit manual flowchart operation and its result requires validation. `cleanupLatexDelimiters` converts paired LaTeX inline delimiters only in prose, preserving escaped currency and code.

For headless Node parser tests, the repository supplies a JSDOM test document. This is parser support, not visual rendering evidence. Run `npm test` and `npm run typecheck`.

For CLI use, run `npm run check:mermaid -- note.md` or `npm run repair:mermaid -- note.md new-output.md`. The dedicated CLI supplies the parser's DOM; library callers must provide their own DOM. Repair refuses an existing output and writes nothing while parser errors remain.

## 中文

在完整仓库中运行 `npm ci` 后使用 `mermaidProcessor.ts`。单独安装技能只提供操作说明，不包含共享工具依赖。

1. 读取已获授权的源文件，在验证通过前保留原文。
2. 运行 `checkMermaidErrors(content)`，使用真实 Mermaid 解析器，并把未闭合的 Mermaid 围栏计为错误。依据反引号/波浪号及长度匹配围栏，保护其他围栏中的示例。
3. 运行 `refineMermaidBlocks(content)`。有效代码块逐字节不变。对无效且已闭合的流程图，自动修复仅把完整的纯 ID 边 `A --|> B` 改为 `A --> B`，并要求重新解析成功。标签和无关标点保持不变。未知类型、其他语法错误及未闭合代码块保留原文，供明确审阅。
4. 写入前再次验证，不把残留错误报告为修复成功。宿主缺少渲染器/解析器时，应报告能力不可用。

不得为了通过验证而删除括号、花括号、引号、节点或关系。保留已有遗留函数导出以兼容调用；`applyDeepDebugToMermaidBlocks` 是显式手动流程图操作，输出必须验证。`cleanupLatexDelimiters` 只转换正文中成对的 LaTeX 行内分隔符，保留转义金额和代码。

仓库使用 JSDOM 文档进行无界面的 Node 解析测试。这属于解析器支持，不代表视觉渲染验收。运行 `npm test` 和 `npm run typecheck`。

CLI 可运行 `npm run check:mermaid -- note.md` 或 `npm run repair:mermaid -- note.md new-output.md`。专用 CLI 提供解析器所需的 DOM，库调用方需提供自己的 DOM。修复命令拒绝覆盖已有输出，解析错误未解决时不写入。
