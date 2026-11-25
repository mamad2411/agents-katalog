---
name: gdpa-cli
description: Use when installing or updating the gdpa-cli command-line tool.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# GDPA CLI 安装

> **何时使用**: 当需要安装或更新 gdpa-cli 命令行工具时使用。安装后 gdpa-cli 具备自动更新能力，无需再次手动更新。

## 安装方法

运行安装脚本：

```bash
bash {{SKILL_DIR}}/install.sh
```

安装完成后，`gdpa-cli` 将被安装到 `~/.local/bin/` 目录。

如果 `~/.local/bin` 不在 PATH 中，请将以下内容添加到 shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`）：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 安装后使用

```bash
# 查看版本
gdpa-cli --version

# 运行 skill
gdpa-cli run <skill_name> --input '<json_string>'

# 查看可用 skills
gdpa-cli skills
```

## 注意事项

- gdpa-cli 二进制具备**自动更新能力**，每次运行时会自动检测并更新到最新版本
- 如需禁用自动更新，使用 `--disable-update` 参数
- 保证 WorkDir 为项目的根目录
