---
name: formula-healer
description: Repair paired standalone math delimiters while preserving Markdown structure.
---

# Formula healer

## English

Use the bundled `formulaFixer.ts` from a complete repository checkout after `npm ci`. Installing this skill alone installs instructions; it does not install the repository's shared TypeScript runtime.

- `fixFormulaFormats(content)` returns a string. It promotes paired standalone `$` lines to `$$` outside frontmatter and fenced code. Existing display math, inline math, escaped currency and unmatched delimiters remain unchanged.
- `fixFormulaFormatsInFile(filePath, reporter?)` returns whether the file changed. It accepts a regular filesystem path, not an Obsidian App/TFile pair. File failures propagate; unchanged files are not written.
- `batchFixFormulaFormatsInFolder(folderPath, reporter?)` visits Markdown/text files recursively and returns `modifiedCount`, `processedCount`, `cancelled`, and per-file `errors`. It does not follow symbolic links. The optional reporter exposes `log`, `updateStatus`, and a readable `cancelled` property.

Confirm the authorized files, read them, apply the helper, review the diff and report every failure. Preserve BOM and line endings. Never interpret a cancelled batch as completed. Validate with `npm test` and `npm run typecheck`; tests use isolated temporary files.

## 中文

在完整仓库中运行 `npm ci` 后使用随附的 `formulaFixer.ts`。单独安装此技能只安装操作说明，不会安装仓库共享的 TypeScript 运行代码。

- `fixFormulaFormats(content)` 返回字符串。仅将 frontmatter 和围栏代码之外成对的独立 `$` 行改为 `$$`，保留既有显示公式、行内公式、转义金额及未配对分隔符。
- `fixFormulaFormatsInFile(filePath, reporter?)` 返回文件是否改变。参数为普通文件路径，不再使用 Obsidian App/TFile。文件错误继续抛出；内容不变时不写入。
- `batchFixFormulaFormatsInFolder(folderPath, reporter?)` 递归处理 Markdown/文本文件，返回 `modifiedCount`、`processedCount`、`cancelled` 和逐文件 `errors`，不跟随符号链接。可选 reporter 提供 `log`、`updateStatus` 和可读取的 `cancelled` 属性。

确认已获授权的文件，读取并应用工具，审阅差异，报告每项失败。保留 BOM 与换行格式，不把已取消批次报告为完成。运行 `npm test` 和 `npm run typecheck`；测试使用隔离的临时文件。
