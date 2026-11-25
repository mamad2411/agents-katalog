---
name: pretty-skills
description: |
  跨 agent 统一管理你的所有 skill 和知识。
  Use when 用户要"装 pretty-skills"、"管 skill"、"ps list/add/rm/update/graph/contribute/info/sync"、
  查看 skill 依赖图、贡献新 skill、跨 Claude Code / Codex / Mavis / Cursor / Windsurf 同步 skill。
  本地增删改无门槛，PR 是用户主动判断不是自动同步（边缘优先开源）。
triggers:
  - 装 pretty-skills
  - 管 skill
  - ps list
  - ps add
  - ps update
  - ps graph
  - 贡献 skill
  - 提 PR
  - 跨 agent 同步
---

# pretty-skills

> 让每个 agent 都能装、每个用户都能改、每个贡献都被看见。

## 一句话定位

**pretty-skills = 跨 agent 的 skill 管理器。**

它把你写的每一个 skill 装到 5 大 agent（Claude Code / Codex / Mavis / Cursor / Windsurf）的统一位置，
让你用同一个 `ps` 命令就能管所有 skill 的增删改、查依赖、提 PR。

## 快速开始

```bash
# 一行安装（首次）
curl -fsSL https://raw.githubusercontent.com/huangrichao2020/pretty-skills/main/tools/pretty-skills/install.sh | bash

# 之后随时用
ps list                        # 看本地装的所有 skill
ps info pretty-skills-creator  # 看某个 skill 的详情
ps add serenity-stock-choke    # 从主项目装一个
ps graph                       # 输出 Mermaid 依赖图
ps contribute my-new-skill     # 把本地修改推回主项目（提 PR）
```

## 设计原则

| 原则 | 怎么落地 |
|---|---|
| **本地优先** | `~/.pretty-skills/store/` 是真实存储，5 agent 都软链到这 |
| **改无门槛** | 直接 `vim` store 里的文件即可，不需要经过工具 |
| **PR 是用户主动判断** | 工具绝不自动 push，需要 `ps contribute` 才走 |
| **跨 agent 统一** | 一次装，5 个 agent 都能用 |
| **依赖关系透明** | `ps graph` 一眼看所有 skill 的依赖图 |
| **manifest 必填** | 没有 manifest 的 skill 不会被装（防垃圾） |

## 目录结构

```
~/.pretty-skills/
├── store/                  # 公共存储（真实文件在这）
│   ├── pretty-skills/
│   ├── pretty-skills-creator/
│   └── serenity-stock-choke/
└── config.yaml             # 哪些 agent 启用 / 哪些 skill 已禁

~/.claude/skills/pretty-skills -> ~/.pretty-skills/store/pretty-skills
~/.codex/skills/pretty-skills -> ~/.pretty-skills/store/pretty-skills
~/.mavis/skills/pretty-skills -> ~/.pretty-skills/store/pretty-skills
~/.cursor/skills/pretty-skills -> ~/.pretty-skills/store/pretty-skills
~/.windsurf/skills/pretty-skills -> ~/.pretty-skills/store/pretty-skills
```

## 8 个子命令

| 命令 | 作用 |
|---|---|
| `ps list` | 列出本地已装的所有 skill（按 agent 分组） |
| `ps info <name>` | 显示 manifest、依赖、占用空间、最后修改时间 |
| `ps add <name>` | 从主项目装一个 skill（默认源：github.com/huangrichao2020/pretty-skills/tree/main/tools） |
| `ps rm <name>` | 卸载（删 store + 软链） |
| `ps update <name>` | 拉主项目最新覆盖本地（保留本地未 commit 的修改会先备份） |
| `ps graph` | 扫描所有 skill 的 manifest.dependencies，输出 Mermaid 依赖图 |
| `ps contribute <name>` | 把本地修改推回主项目（自动开 fork + 提 PR，附 changelog） |
| `ps sync` | 批量 update（等价于对所有 skill 跑 `ps update`） |

## 与 pretty-skills-creator 的关系

- **pretty-skills（管）**：本文档，管所有 skill
- **pretty-skills-creator（创）**：创建新 skill 的入口，自动带 4 风格 HTML 占位 + 可选 PPT
- 二者是父子关系：装好 pretty-skills 后，`ps create` 就把 pretty-skills-creator 调起来

## 为什么叫"边缘优先开源"？

GitHub 的传统是"主项目维护者写 + 用户提 PR"，**pretty-skills 反过来**：
- 用户本地增删改无门槛（store 是用户的）
- 用户觉得好的内容 → 主动提 PR 回主项目
- 主项目维护者 review 后 merge

这样每个用户都是潜在贡献者，每个 PR 都是真实使用过的反馈。
主项目不需要全知全能 — 只需要 review + merge 就行。

## 开发

见 `docs/contributing.md`（怎么给 pretty-skills 提 PR）
见 `docs/skill-schema.md`（怎么写一个合法 skill 的 manifest）
