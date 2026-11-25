---
name: ost-usage-examples
description: 'Write optional usage_examples.md for an open_supports support package when a library has meaningful post-install workflows. Use after repo summary, install script, and setup Skill are complete.'
argument-hint: 'GitHub owner/repo of the target library, e.g. colbymchenry/codegraph'
---

# 编写 open_supports 使用示例（usage_examples.md）

## When to Use

- workflow 在 `skill_for_setup` 完成后检测到该库有足够复杂的安装后用法，并且用户同意生成详细用例
- 用户明确要求为某个支持包补充安装后的常见使用说明
- 官方 README 或 `.ost-refs/` 提供了多个实际用法场景，需要整理为本地快速入口

本 Skill 是可选阶段。没有 `usage_examples.md` 不影响支持包核心完成。

## Pre-read

执行前读取以下内容，按优先级顺序：

1. 目标支持包的 `repo_readme_summary.md`
2. 目标支持包的 `skill_for_setup/README.md`
3. 目标支持包的 `skill_for_setup/ost_*_install/SKILL.md`
4. 目标支持包的 `scripts_for_install/install.*`
5. 目标支持包的 `.ost-refs/` 目录（如存在且有内容）
6. `repo_readme_summary.md` 中引用的官方 README / 官方文档链接（仅在需要确认用法时读取）

## GitHub Source Policy

读取 GitHub 仓库事实、README、目录、release、issue、PR 或文件内容时，优先使用 GitHub connector / GitHub app 的结构化工具；若工具不可见，先通过 `tool_search` 搜索 GitHub 工具。仍不可用时，再考虑 `gh` CLI、GitHub 官方 API 或官方文档网站。

`curl` / raw GitHub URL 只用于官方安装命令本身，或作为明确记录的 fallback。生成使用示例时，不要用 raw README 抓取替代 GitHub connector / 官方文档入口；如必须降级，记录原因。

作为 workflow 阶段子代理返回结果时，必须包含：

- `sources_used`: 来源类别和关键路径摘要
- `fallbacks`: 降级原因摘要；没有降级时返回空数组

## Clarification / Blocking

如果执行本阶段所需信息无法从 `repo_readme_summary.md`、安装脚本、setup Skill、`.ost-refs/` 或官方文档中可靠判断：

1. 不要猜测命令、配置、客户端接入或预期结果
2. 向 workflow 返回一个澄清问题
3. 标明 blocked 字段：
   - `stage`: `optional_usage_examples`
   - `reason`
   - `question`
   - `suggested_default`（如有）
4. 等用户回答后再继续本阶段

典型阻塞点：

- 官方文档没有给出某个常见场景的命令或配置
- setup Skill 与官方文档对客户端接入方式描述不一致
- 无法判断示例应覆盖项目级配置还是全局配置
- 无法确认示例命令的预期成功输出

## 输出文件

写入目标支持包根目录：

```text
usage_examples.md
```

文件头格式：

```markdown
# {LibraryName} — 使用示例

> 来源：官方 README / 文档；本文件只保留 open_supports 使用者最常见的入口。
```

## 文档结构

按以下顺序编写：

| # | 部分标题 | 内容定位 |
|---|---------|---------|
| 1 | **快速开始** | 安装完成后的第一条可执行路径，不重复安装步骤 |
| 2 | **常见场景** | 2~5 个高频任务，每个任务可独立阅读 |
| 3 | **与 Agent 客户端配合** | Claude Code、Codex、MCP、IDE 等接入或日常使用方式；无相关内容则删除本节 |
| 4 | **验证与排错** | 最小验证命令、常见失败现象、可执行处理方式 |
| 5 | **延伸阅读** | 官方文档中更完整的教程或高级配置链接 |

若库具有项目级、CWD 敏感或双模式安装，在快速开始之前增加 `## 安装范围`：复用 `repo_readme_summary.md` Part 2 的 A/B/C/D 分类、官方默认和证据链接。此节只说明该安装写入哪里、何时需要目标目录；不重复完整安装流程。

## 示例条目格式

每个示例尽量使用以下结构：

````markdown
### {场景名称}

适用场景：{什么时候使用}

```sh
{命令或最小配置}
```

预期结果：{成功后应看到什么}

注意事项：{只写会影响执行的限制；没有则删除本行}
````

## 编写原则

- 面向“已经安装完成，现在要开始使用”的用户
- 示例必须能从官方文档、现有支持包文件或 `.ost-refs/` 追溯来源
- 优先保留最常见、最短路径的操作
- 注释用于解释命令目的和成功判断，不展开背景教程
- 安装步骤仍以 `repo_readme_summary.md` 第 2 部分和 `scripts_for_install/install.*` 为准
- 涉及项目目录的命令必须使用明确、已确认的目录（如 `/work/app`）；不得假设支持包目录或 Agent 当时的 CWD 就是用户项目
- `B` 类命令必须说明 CWD 会决定写入位置；`C` 类命令必须保留官方路径参数；`D` 类示例必须标明 global/project 分支和官方默认
- 有副作用的命令必须明确说明影响范围，不能伪装成无风险示例

## 禁止事项

- 不复制大段官方文档
- 不发明官方没有的命令、flag、配置键或客户端接入方式
- 不重写完整安装流程
- 不把卸载流程写成可执行指导；如官方有卸载文档，只能在延伸阅读或排错中给链接
- 不加入与 open_supports 使用者无关的高级场景
- 不把会修改用户项目、配置、云资源或本地状态的命令写成无副作用示例

## Quality Checklist

- [ ] 文件写入目标支持包根目录 `usage_examples.md`
- [ ] 快速开始不重复安装步骤
- [ ] 每个示例都有适用场景、命令或最小配置、预期结果
- [ ] 每个示例都能标明来源或链接，便于 review 追溯
- [ ] 命令、配置和客户端接入方式均可追溯到官方文档、支持包文件或 `.ost-refs/`
- [ ] 如果示例命令会修改用户项目、配置、云资源或本地状态，必须写清影响范围
- [ ] 项目级、CWD 敏感或双模式库已包含“安装范围”，且与摘要、脚本和 setup Skill 的 A/B/C/D 契约一致
- [ ] 项目相关示例使用明确目标目录，不依赖执行时 CWD
- [ ] 没有大段复制官方文档
- [ ] 没有发明未确认的命令、flag 或配置键
- [ ] 没有把卸载流程写成默认可执行操作
- [ ] 延伸阅读给出具体链接，不写“详见官方文档”这类无效表述
