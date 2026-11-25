---
name: ost-colbymchenry-codegraph-install
description: '帮助用户安装并配置 CodeGraph。主路径：运行支持包内的一键脚本（macOS / Linux / WSL）；脚本不可用或平台不支持时，回退到 repo_readme_summary.md 的安装说明。范围：CLI 安装 + Agent 接入，不含 codegraph init。'
argument-hint: '目标 Agent 和配置范围，如 "--target=claude" 或 "--location=global"'
---

# CodeGraph 安装（skill_for_setup）

> **安装作用域**：模式 D；`--location=local` 为 CWD-sensitive。AI Agent 必须传入最后一个 `TARGET_DIR`，脚本会在子 Shell 中运行 `codegraph install`；`--global` 不带目录。

> 参考：[`repo_readme_summary.md`](../../repo_readme_summary.md)  
> 脚本：[`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> 官方仓库：[colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)

## When to Use

- "帮我安装 CodeGraph"
- "把 CodeGraph 接入我的 Claude Code / Codex / Cursor"
- "升级 CodeGraph 到最新版"

## Pre-read

执行任何操作前先读取：

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) — 安装方式和注意事项
2. [`../../.ost-refs/`](../../.ost-refs/) 目录（如存在）— 本地路径约定或特殊配置

## Pre-checks

从对话上下文中确认：

| 信息 | 默认值 | 说明 |
|------|--------|------|
| 操作系统 | — | 影响走主路径还是兜底路径 |
| 目标 Agent | `auto` | 从用户请求推断，不明确时保持 auto |
| 配置范围 | `local` | 项目级；用户明确要求全局时改为 `global` |

## Procedure

### 主路径：运行一键脚本（macOS / Linux / WSL）

从支持包根目录（本 SKILL.md 向上两级）执行：

```sh
sh scripts_for_install/install.sh [--target=<agents>] [--location=local|global] [TARGET_DIR]
```

常用示例：

```sh
sh scripts_for_install/install.sh /path/to/project       # auto 检测，项目级
sh scripts_for_install/install.sh --target=claude /path/to/project # 仅 Claude Code，项目级
sh scripts_for_install/install.sh --location=global      # 全局配置，auto 检测
```

### 兜底路径：参考 repo_readme_summary.md

遇到以下情况时，转为按 `repo_readme_summary.md` **第 2 部分（安装与更新）** 逐步执行：

- 用户平台为 Windows（sh 脚本不适用）
- 脚本执行报错
- 用户希望手动控制每一步

将安装命令发给用户确认后逐条运行。

### 验证

```sh
codegraph version
```

输出版本号即成功。

---

## 安装完成后告知用户

```
安装完成。请在每个需要使用 CodeGraph 的项目目录下执行：
  cd /path/to/your/project && codegraph init
```

---

## Troubleshooting

| 现象 | 原因 | 处理 |
|------|------|------|
| `codegraph: command not found` | 安装后未重开终端 | 新开终端后重试 |
| Agent 未调用 CodeGraph 工具 | 未执行 `codegraph install` 或未重启 Agent | 重新运行脚本或手动执行 `codegraph install` |
| 图谱未自动更新 | 沙箱环境禁止文件监听 | 手动执行 `codegraph sync` |
| 索引卡住 / 锁文件残留 | 上次异常退出 | `codegraph unlock` |
