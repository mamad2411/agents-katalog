---
name: token-audit
description: 审计与对比 Antigravity 会话的真实 Token 账单（Input / Output / Cache Read）、检测 Prefix Cache 断层与自动压缩节点（CHECKPOINT）、揪出单次会话最烧额度的 Top 5 步骤，或诊断项目的 AGENTS.md / SKILL.md 肥胖度与 MCP 空载底座税。
---

# Antigravity 账单透视、缓存断层与底座税审计指南 (token-audit)

无需消耗任何模型 Token，直接通过本地脚本解析 Antigravity 底层会话日志（`transcript_full.jsonl` / `transcript.jsonl`）与项目/全局 MCP 配置，并自动区分不同代际模型的上下文自动压缩水位（三代模型常见约 256K，四代模型推测约 512K）。

## 常用命令

> 注：若已全局安装 `tokless` 包，可直接运行 `tokless audit <session|compare|project> ...`（兼容 `agy-audit`）。Antigravity 仅向 Hook / MCP 进程注入 `PLUGIN_ROOT`，不会注入到常规 `run_command` 终端中，未全局安装 CLI 时请直接使用下方插件路径：

### macOS / Linux (bash / zsh)

```bash
# 1. 解剖单个会话（支持短 ID 前缀或日志路径），查看缓存断层、最慢步骤 Top 3、MCP 空载继承与 Top 5 烧钱步骤
node "$HOME/.gemini/config/plugins/agy-tokless/tools/agy-audit/cli.js" session <会话ID或前缀>

# 2. 优化前后双会话 A/B 对比（对比总 Token、Cache Read 滚雪球、缓存命中率、盲读次数与节省比例）
node "$HOME/.gemini/config/plugins/agy-tokless/tools/agy-audit/cli.js" compare <优化前会话ID> <优化后会话ID>

# 3. 诊断指定项目的常驻规则/Skill 肥胖度，以及全局/工作区 MCP 与工具底座空载税
node "$HOME/.gemini/config/plugins/agy-tokless/tools/agy-audit/cli.js" project <项目目录路径>
```

### Windows (PowerShell)

```powershell
# 1. 解剖单个会话（支持短 ID 前缀或日志路径），查看缓存断层、最慢步骤 Top 3、MCP 空载继承与 Top 5 烧钱步骤
node "$env:USERPROFILE\.gemini\config\plugins\agy-tokless\tools\agy-audit\cli.js" session <会话ID或前缀>

# 2. 优化前后双会话 A/B 对比（对比总 Token、Cache Read 滚雪球、缓存命中率、盲读次数与节省比例）
node "$env:USERPROFILE\.gemini\config\plugins\agy-tokless\tools\agy-audit\cli.js" compare <优化前会话ID> <优化后会话ID>

# 3. 诊断指定项目的常驻规则/Skill 肥胖度，以及全局/工作区 MCP 与工具底座空载税
node "$env:USERPROFILE\.gemini\config\plugins\agy-tokless\tools\agy-audit\cli.js" project <项目目录路径>
```
