---
name: bole-skill
description: 伯乐 — 全流程求职助手。一句话启动，多平台自动扫盘 → 跨源去重 → 政府资质交叉对比 → 透明评分排序
---

说一句话就开始：

```
帮我在北京看看 AI 产品经理的岗位
```

## Pipeline Overview

```
sources → collect → dedup → score → format → report
                             ↓
enterprise → clean → score → enrich → final_filter → kb_output
```

## Quick Start

```bash
pip install -r requirements.txt
bash install.sh
```

安装完成后，展示以下重启提示（只展示这个框，不加 `/bole` 快捷命令等额外说明）：

```
⚠️ 最后一步：重启 Claude Code
MCP 配置需要重启才能加载。请：

1. 完全退出当前 Claude Code 会话（退出进程）
2. 重新打开 Claude Code
3. 然后告诉我：「已重启，帮我在 XX 城市看看 XX 岗位」
```

用户重启并告知「已重启」后，清除 `data/.restart_required` 标记，继续走管线。

> **⚠️ 运行环境要求**
>
> 浏览器自动采集依赖 Playwright MCP（`browser_navigate` / `browser_snapshot` 等工具），**Claude Code CLI / VS Code 扩展均可运行**。安装后执行 `browser_snapshot`，正常返回截图即环境就绪。
>
> 验证方法：在 Claude Code 中执行 `browser_snapshot`，正常返回截图即环境就绪。

## Full Documentation

See `BOLE.md` for pipeline details and `CLAUDE.md` for Claude Code project instructions.
