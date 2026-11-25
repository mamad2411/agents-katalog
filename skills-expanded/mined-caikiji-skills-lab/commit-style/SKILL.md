---
name: commit-style
description: 执行任何 git 提交（commit/amend/rebase/squash）前必须读取并遵守本 skill。按 Conventional Commits 规范生成并校验提交信息；会话开始时确认提交汇报模式：每次提交展示确认，或自检通过后自动提交。
---

# Commit Style Skill

为仓库按 Conventional Commits 规范生成并校验提交信息。

## 规则

格式：`<type>(<scope>): <subject>`

- type 用白名单：`feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`
- `(scope)` 可选；`type`、`scope` 与 `:` 之间不写空格
- subject ≤50 字符，结尾不写标点；语言跟随仓库（中文仓库写中文）
- body 需要时写"为什么"，不罗列改动
- breaking change：`<type>!: <subject>` 或 footer 写 `BREAKING CHANGE: <说明>`
- `revert`：`revert: <被回滚提交的 subject>`

## 工作流

1. 会话开始时确认提交汇报模式（一次提问）：
   - **每次展示**：每条提交信息展示给用户确认后再提交。
   - **自动提交**：自检通过直接提交；未通过则修正后展示确认。
2. 读仓库惯例：`git log --oneline -20` 看现有风格，读 `AGENTS.md`/`CLAUDE.md` 的提交规则（语言、scope 习惯、中文语义）。
3. 按规则草拟提交信息。
4. 自检：逐条核对规则，不符重写。
5. 文档同步检查：对照下表扫描本次 diff，命中则先按对应 skill 更新文档并一并纳入本提交。

   | 本次改动 | 需检视 |
   |---------|--------|
   | 命令/脚本入口增删改名 | readme-style（快速开始）+ agents-style（常用命令） |
   | 安装、构建方式变化 | readme-style（快速开始） |
   | 新增用户可见能力 | readme-style（特性章） |
   | 团队约定、禁区变化 | agents-style（约定/边界章） |
   | 新增深文档 | 两者索引章 |

   纯内部重构、测试、格式化直接跳过；查过但无需更新也在回复中说一句"文档已检视"。
6. 提交前检查：
   - 核对文件清单：`git status --short` + `git diff --cached --stat`，只包含本次改动才能提交。
   - 只 add 精确路径，不用 `git add -A` / `git add .`。
   - 暂存区混入无关文件：`git restore --staged <路径>` 撤出暂存，确认后再提交。
6. 按用户选择的模式执行；修正过的信息始终展示确认。

## 诊断

校验给定的提交信息（提交前、amend、rebase 场景）：

1. 逐条核对规则，列出违规点。
2. 给出修正版。
