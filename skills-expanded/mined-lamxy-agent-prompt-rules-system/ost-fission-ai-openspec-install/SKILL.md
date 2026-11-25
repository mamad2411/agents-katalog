---
name: ost-fission-ai-openspec-install
description: '帮助用户安装并配置 OpenSpec。主路径：运行支持包内的一键脚本；脚本不可用时回退到 repo_readme_summary.md 第 2 部分。范围：安装/更新 CLI、验证版本、可选初始化或更新项目；不含卸载、删除生成文件或详细使用教程。'
argument-hint: '[--package-manager=npm|pnpm|yarn|bun] [--init-project --tools=claude,codex --project-dir=/path/to/project] [--update-project --project-dir=/path/to/project] [--profile=core]'
---

# OpenSpec 安装（skill_for_setup）

> **安装作用域**：模式 A。CLI 始终全局安装；`--init-project` 与 `--update-project` 是独立 CWD-sensitive 项目操作，AI Agent 必须把 `TARGET_DIR` 作为最后一个参数传入。

> 参考：[`repo_readme_summary.md`](../../repo_readme_summary.md)
> 脚本：[`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)
> 官方仓库：[Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)

## When to Use

当用户要求安装、更新或初始化 OpenSpec 时使用本 Skill。OpenSpec 是 `@fission-ai/openspec` CLI，安装后可在目标项目运行 `openspec init` 生成 OpenSpec specs/changes 与 AI tool command files。

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) — 官方安装方式、更新方式、平台说明和注意事项
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) — 一键脚本支持的平台、flags 和写入行为
3. [`../../.ost-refs/`](../../.ost-refs/) 目录（如存在）— 本地约定

## Pre-checks

从对话上下文中确认：

| 信息 | 默认值 | 说明 |
|------|--------|------|
| 操作系统 | 当前 shell | 脚本支持 macOS、Linux、WSL；Windows native shell 使用兜底路径 |
| Package manager | `npm` | 可选 `npm`、`pnpm`、`yarn`、`bun` |
| Node.js | 必须已安装 | OpenSpec 要求 Node.js `>= 20.19.0` |
| 是否初始化项目 | 不初始化 | `--init-project` 会在目标项目写入 OpenSpec 和 AI tool 配置文件 |
| 是否更新项目文件 | 不更新 | `--update-project` 会在目标项目运行 `openspec update` |
| 目标项目目录 | 当前目录 | 只在初始化或更新项目时需要 |
| AI tools | `none` | 非交互初始化时传给 `openspec init --tools`，例如 `claude,codex`、`all`、`none` |
| Profile | 官方默认 | 需要覆盖时传 `--profile=<profile>` |

在执行会安装全局 package 或写入项目文件的命令前，先向用户确认。

## Procedure

### 主路径：运行一键脚本（macOS、Linux、WSL）

从支持包根目录（本 `SKILL.md` 向上两级）执行：

```sh
sh scripts_for_install/install.sh [flags]
```

常用示例：

```sh
sh scripts_for_install/install.sh
sh scripts_for_install/install.sh --package-manager=pnpm
sh scripts_for_install/install.sh --init-project --tools=claude,codex --project-dir=/path/to/project
sh scripts_for_install/install.sh --update-project --project-dir=/path/to/project
sh scripts_for_install/install.sh --init-project --tools=all --profile=core --project-dir=/path/to/project
```

脚本会检查平台、Node.js `>= 20.19.0`、所选 package manager，安装或更新 `@fission-ai/openspec@latest`，再验证 `openspec --version`。只有显式传入 `--init-project` 或 `--update-project` 时才写入目标项目。

### 兜底路径：参考 repo_readme_summary.md

遇到以下情况时，转为按 `repo_readme_summary.md` **第 2 部分（安装与更新）** 逐步执行：

- 用户使用 Windows native shell，或当前平台不是 macOS、Linux、WSL。
- 用户要求使用 Nix 安装或直接运行。
- 一键脚本失败，但官方 package-manager 命令仍适用。
- 用户要求手动控制每一步安装、初始化或更新。

将安装命令发给用户确认后逐条运行。不要用兜底路径猜测未记录的 flags；若摘要中没有覆盖用户要求，先询问。

### 验证

```sh
openspec --version
```

如已初始化或更新项目，可在目标项目内做轻量检查：

```sh
openspec list
```

---

## 安装完成后告知用户

```text
OpenSpec CLI 已安装或更新。终端命令使用 `openspec ...`；AI chat 中使用 `/opsx:*` slash commands。
常用下一步：在目标项目运行 `openspec init --tools claude,codex`，然后在 AI chat 中使用 `/opsx:explore`、`/opsx:propose`、`/opsx:apply`、`/opsx:archive`。
```

---

## Troubleshooting

| 现象 | 原因 | 处理 |
|------|------|------|
| `Node.js version does not meet OpenSpec requirements` | OpenSpec 要求 Node.js `>= 20.19.0` | 升级 Node.js 后重新运行脚本 |
| `missing required command: npm/pnpm/yarn/bun` | 选择的 package manager 不在 `PATH` 中 | 安装对应 package manager，或改用 `--package-manager=npm` |
| Windows native shell 被脚本拒绝 | 脚本只支持 macOS、Linux、WSL | 按 `repo_readme_summary.md` 第 2 部分在 Node.js terminal 中执行官方 package-manager 安装命令，或使用 WSL |
| `openspec` 安装后不在 `PATH` | 全局 package manager bin 目录未被当前 shell 识别 | 打开新终端，或检查 npm/pnpm/yarn/bun 的 global bin 路径 |
| 初始化时工具配置不符合预期 | `openspec init --tools`、profile 或 delivery mode 影响生成文件 | 使用明确的 `--tools` 和 `--profile` 重新初始化，或在项目内运行 `openspec update` |
| 需要卸载 OpenSpec | 卸载涉及全局 package、项目目录和各 AI tool 生成文件 | 不默认执行卸载；参考 `repo_readme_summary.md` 第 5 部分的官方卸载入口 |
