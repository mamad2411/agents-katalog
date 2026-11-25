---
name: ost-open-gsd-gsd-core-install
description: '帮助用户安装或更新 GSD Core runtime 配置。主路径：运行支持包内的一键脚本；脚本不可用或用户需要 native/manual 路径时回退到 repo_readme_summary.md 第 2 部分。范围：运行官方 npx 安装器并提示验证方式，不含安装 Node.js、Codex CLI 或运行 GSD 项目工作流。'
argument-hint: '至少一个 runtime flag，如 --claude 或 --codex；可选 scope：--local、--global、--location=local、--location=global'
---

# GSD Core 安装（skill_for_setup）

> **安装作用域**：模式 D；`--local` 为 CWD-sensitive。AI Agent 必须把用户的项目根目录作为最后一个 `TARGET_DIR` 参数传给脚本；只在 `--global` 时省略它。

> 参考：[`repo_readme_summary.md`](../../repo_readme_summary.md)  
> 脚本：[`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> 官方仓库：[open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)

## When to Use

当用户希望安装、更新或配置 GSD Core 到 Claude Code、Codex CLI 或其他官方支持 runtime 时使用本 Skill。典型触发包括：

- "安装 GSD Core"
- "给 Claude Code 配置 GSD Core"
- "给 Codex CLI 安装 open-gsd/gsd-core"
- "更新 GSD Core runtime 配置"

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) — 安装方式、平台限制、验证命令和官方替代路径
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) — 实际支持的参数、检查逻辑和脚本边界
3. [`../../.ost-refs/`](../../.ost-refs/) 目录（如存在）— 本地约定

## Pre-checks

从对话上下文中确认：

| 信息 | 默认值 | 说明 |
|------|--------|------|
| 操作系统 | 无 | 主路径只支持 macOS、Linux、WSL；Windows native shell 走兜底路径 |
| Runtime | 无 | 必须至少选择一个 runtime flag，例如 `--claude` 或 `--codex` |
| Scope | `--local` | 可改为 `--global`；`--all` 必须配合 `--global` |
| 自定义配置目录 | 无 | 如需使用 `CLAUDE_CONFIG_DIR`、`GEMINI_CONFIG_DIR` 等环境变量，运行脚本前由用户明确指定 |
| Codex CLI 版本 | 脚本检查 | 仅选择 `--codex` 时需要 Codex CLI >= 0.130.0 |

如果 runtime 或 scope 不明确，先向用户确认。不要在未确认 runtime 的情况下运行安装脚本。

## Procedure

### 主路径：运行一键脚本（macOS / Linux / WSL）

从支持包根目录（本 `SKILL.md` 向上两级）执行：

```sh
sh scripts_for_install/install.sh [runtime flags] [scope] [TARGET_DIR]
```

常用示例：

```sh
sh scripts_for_install/install.sh --claude --local /path/to/project
sh scripts_for_install/install.sh --codex --local /path/to/project
sh scripts_for_install/install.sh --claude --codex --global
sh scripts_for_install/install.sh --all --global
```

脚本会执行平台检查、Node.js/npm/npx 版本检查、Codex CLI 版本检查（仅 `--codex`），然后调用官方 `@opengsd/gsd-core` 安装器。脚本执行前会打印摘要，执行后会打印验证方式。

### 兜底路径：参考 repo_readme_summary.md

遇到以下情况时，转为按 `repo_readme_summary.md` **第 2 部分（安装与更新）** 逐步执行：

- 用户处于 Windows native shell，不能或不想使用 WSL / Git Bash 运行脚本
- 用户要求官方交互式安装、Claude native plugin、Gemini native extension、无 Node.js 机器复制输出目录或手动转换源文件
- 脚本报错且错误不属于可直接补充参数的情况
- 用户需要对官方安装命令逐条确认或手动控制

将第 2 部分中对应路径的安装命令发给用户确认后逐条运行，不要猜测未写明的转换规则。

### 验证

安装完成后，提示用户重启目标 runtime，然后运行对应命令：

```sh
/gsd-new-project
```

Codex CLI 使用：

```sh
$gsd-new-project
```

命令被识别并开始询问项目问题，即代表安装成功。

---

## 安装完成后告知用户

```text
GSD Core 安装器已执行完成。请重启目标 runtime 后运行对应验证命令：
Claude Code / Copilot / OpenCode / Kilo / Cline 等：/gsd-new-project
Gemini CLI：/gsd:new-project
Codex：$gsd-new-project
命令被识别并开始询问项目问题，即代表安装成功。
```

---

## Troubleshooting

| 现象 | 原因 | 处理 |
|------|------|------|
| 未指定 runtime 时脚本报错 | 脚本不运行交互式安装，必须显式选择 runtime | 追加 `--claude`、`--codex` 或其他 runtime flag 后重试 |
| `--all` 报 scope 错误 | 官方摘要只给出 `--all --global` | 改用 `--all --global`，或选择单个 runtime |
| Node.js / npm 版本不满足要求 | GSD Core 要求 Node.js >= 22.0.0、npm >= 10.0.0 | 先升级 Node.js / npm，再重新运行脚本 |
| `--codex` 时 Codex CLI 检查失败 | Codex runtime 需要 Codex CLI >= 0.130.0 | 先安装或升级 Codex CLI，再重新运行脚本 |
| Windows native shell 报不支持 | 脚本只支持 macOS、Linux、WSL | 改用 WSL / Git Bash，或按 `repo_readme_summary.md` 第 2 部分执行官方路径 |
| 安装后命令不识别 | 目标 runtime 尚未重启或配置未加载 | 重启目标 runtime；Codex 可重启或运行 `codex --reload` |
