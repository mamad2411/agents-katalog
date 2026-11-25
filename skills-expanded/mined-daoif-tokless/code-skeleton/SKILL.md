---
name: code-skeleton
description: 提取代码文件或目录的紧凑语法骨架（仅保留类名、函数签名、导出接口与精确 [L起-L止] 行号，剥离具体实现代码）。在探索代码库、排查 Bug 或读取中大型文件前使用此技能快速定位行号，可减少 85%~97% 的探索期 Token 消耗。
---

# 代码骨架极速提取指南 (code-skeleton)

为了避免调用 `read_file` 或 `Read` 盲目全量读取几百行代码导致后续每一轮对话背负高额的 Cache Read 滚雪球成本，请先提取带 `[L起-L止]` 行号的语法骨架。

## 使用方法

> 注：若已全局安装 `tokless` 包，可直接运行 `tokless skeleton <路径> [--depth 2]`（兼容 `repo-skeleton`）。Antigravity 仅向 Hook / MCP 进程注入 `PLUGIN_ROOT`，不会注入到常规 `run_command` 终端中，未全局安装 CLI 时请直接使用下方插件路径：

### macOS / Linux (bash / zsh)

```bash
# 1. 扫描源码目录（自动排除 node_modules/.git/dist/target 等，默认深度 2），一步拿到全局函数与行号地图
node "$HOME/.gemini/config/plugins/agy-tokless/tools/repo-skeleton/cli.js" <目录路径> --depth 2

# 2. 提取单个大文件的函数/类签名与起止行号
node "$HOME/.gemini/config/plugins/agy-tokless/tools/repo-skeleton/cli.js" <文件路径>
```

### Windows (PowerShell)

```powershell
# 1. 扫描源码目录（自动排除 node_modules/.git/dist/target 等，默认深度 2），一步拿到全局函数与行号地图
node "$env:USERPROFILE\.gemini\config\plugins\agy-tokless\tools\repo-skeleton\cli.js" <目录路径> --depth 2

# 2. 提取单个大文件的函数/类签名与起止行号
node "$env:USERPROFILE\.gemini\config\plugins\agy-tokless\tools\repo-skeleton\cli.js" <文件路径>
```

拿到目标函数的 `[L起-L止]` 行号后，直接调用 `read_file(Path, StartLine, EndLine)`（或 Claude Code `Read(file_path, offset, limit)`）按需完整读取对应代码段（无单次行数跨度限制，凡传入显式行号一律放行；若启用 `--with-guard` 护栏，仅对 `>800` 行无行号盲读返回全文骨架辅助导航）。
