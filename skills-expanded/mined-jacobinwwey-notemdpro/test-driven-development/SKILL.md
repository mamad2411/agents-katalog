---
name: test-driven-development
description: Verify portable helpers with production-module regression tests before changing behavior.
---

# Test-driven development

## English

From a complete checkout, install locked dependencies with `npm ci`. Run `npm test` (Node test runner through tsx) and `npm run typecheck`. The tests import actual helpers; they do not use Obsidian mocks.

Before a behavior fix, add a fixture demonstrating lost structure or incorrect output and confirm the failure. Implement the smallest change, rerun focused tests, then the full local suite. Use isolated temporary directories for file tests; never delete a fixed user vault.

Cover unchanged valid content, nested/long/tilde fences, BOM and line endings, unknown Mermaid families, errors and cancellation. Parser success is not proof of semantic fidelity or visual quality. Review node/edge preservation and output diffs separately. Documentation-only changes need link and command consistency checks.

## 中文

在完整仓库中运行 `npm ci` 安装锁定依赖，再运行 `npm test`（通过 tsx 使用 Node 测试运行器）与 `npm run typecheck`。测试导入真实工具函数，不使用 Obsidian mock。

修复行为前，先增加能重现结构丢失或输出错误的样例并确认失败。实施最小修改，先跑专项测试，再跑完整本地套件。文件测试使用隔离临时目录，绝不删除固定的用户笔记库。

覆盖有效内容不变、嵌套/长/波浪号围栏、BOM 与换行、未知 Mermaid 类型、错误与取消。解析成功不能证明语义保真或视觉质量，需要另行检查节点/关系与输出差异。仅文档修改需检查链接与命令一致性。
