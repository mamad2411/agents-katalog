---
name: npx-skills-cli
description: 汇总、说明并帮助选择正确的 `npx skills` 命令，用于安装、列出、搜索、卸载、检查、更新、初始化或同步 agent skills。当用户询问如何使用 `skills` CLI、需要正确的命令或参数、需要别名对照，或需要在 project scope、global scope、特定 agent 或特定 skill 之间做选择时使用。
---

# Npx Skills CLI

按用户所需粒度说明 `npx skills` 命令。

需要命令目录、别名、选项或示例时，阅读 [references/commands.md](references/commands.md)。

优先给出可执行的准确命令，少用抽象描述；除非用户要求完整步骤说明，否则保持答复紧凑。

## 工作流程

1. 明确用户目标。
2. 映射到最接近的 `npx skills` 子命令。
3. 仅补充 scope、agent 或 skill 选择所需的最少参数。
4. 返回一条或多条可直接运行的命令。
5. 仅在有助于快速浏览或对比命令时提及别名。

## 决策指引

- 用户要从仓库、URL、git 源或本地路径安装 skills 时，用 `add`。
- 用户要查看已安装内容时，用 `list`。
- 用户要发现或按关键词搜索时，用 `find`。
- 用户要卸载 skills 时，用 `remove`。
- 用户要知道是否有更新时，用 `check`。
- 用户要升级已安装的 skills 时，用 `update`。
- 用户要脚手架新建 `SKILL.md` 时，用 `init`。
- 用户要从 lock file 恢复时，用 `experimental_install`。
- 用户要从 `node_modules` 同步 skills 时，用 `experimental_sync`。

## 回复规则

- 区分 project scope 与 global scope。
- 涉及全局安装或卸载时说明 `-g`。
- 用户关心特定 agent（如 `codex`、`claude-code`）时说明 `-a` 或 `--agent`。
- 用户只要部分 skill 而非整仓时说明 `-s` 或 `--skill`。
- 用户明确要求对所有 agent 安装全部 skill 时说明 `--all`。
- CLI 中存在且确实有用的别名可以写出。
- 用户要「全部命令」时，从参考文档给出完整命令列表。
- 用户要推荐方案时，先给出准确命令，再附一行理由。

## 示例问法

- 「如何只为 Codex 安装某个 skill 仓库？」
- 「列出所有 `npx skills` 命令。」
- 「如何全局卸载某一个 skill？」
- 「`check` 和 `update` 有什么区别？」
- 「如何新建 skill 模板？」

## 参考

需要以下内容时使用 [references/commands.md](references/commands.md)：

- 规范子命令名
- 别名
- 常用参数
- 调用示例
- experimental 命令说明
