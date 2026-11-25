---
description: 自动生成"我这周做了什么"markdown 周报。读最近 N 天 session 的 summary + tags + files + commands + tokens, LLM 汇总(主要主题 / 关键决策 / 触及项目 / 产出物 / token 花费 / 工作模式观察 / 下周建议)。结果写 ~/.claude/mirror/reports/。Use when 用户 types /weekly-report 或问 "这周我干了啥 / 周报 / 总结这周 / 最近 N 天做了什么"。
when_to_use: Triggered by /weekly-report, "这周我干了啥", "周报", "总结这周", "最近 N 天做了什么". Skip if 已经知道.
disable-model-invocation: false
allowed-tools: Read Bash(python3:*)
arguments: days
---

# Weekly-Report — 自动周报

读最近 N 天 session 的元数据(默认 7 天), 1 次 LLM 调用汇总成 markdown。

## 触发后的动作

### 1. 解析参数

`$ARGUMENTS` 例:
- 空 → 默认最近 7 天
- `--days 14` → 最近 14 天
- `--days 1` → 今天

### 2. 跑主脚本

```bash
python3 ~/.claude/skills/weekly-report/report.py $ARGUMENTS
```

主脚本:
- 读 `~/.claude/mirror/search-index.json` + `~/.claude/mirror/summaries.json`
- 过滤最近 N 天 mtime 的 session
- 拼 prompt 调 DeepSeek
- 输出 markdown 到 `~/.claude/mirror/reports/YYYY-MM-DD-Nd-report.md`
- 自动 open 文件

### 3. 报告进度

显示报告路径 + token / 花费 / 处理 session 数。

## 成本

- ~¥0.012-0.02 单次(单次 DeepSeek 调用)

## Fallback

- summaries.json 不存在 → 提示先跑 `/summarize-sessions`
- DEEPSEEK_API_KEY 找不到 → 提示 export 或 `echo sk-xxx > ~/.deepseek`
