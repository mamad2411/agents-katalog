---
name: skill-usage-audit
description: 扫描 Claude Code 与 Codex 会话日志，统计各 Skill 的真实使用情况（正式调用次数、会话数、项目分布、最近使用时间），把"skill 到底有没有被用上"从黑盒变成一张报表。触发词：skill 使用统计、skill 用量、哪些 skill 被用了、使用台账、skill-usage-audit。
---

# skill-usage-audit

回答一个问题：**我装的这些 Skills，在真实工作中到底有没有被用、被谁用、用了多少次。**

## 何时使用

- 用户想知道某个 Skill（或全部 Skills）的真实使用情况；
- 评估一套 Skill 体系（如 app-flow、web-flow）是否真的参与了项目开发；
- 决定归档某个 Skill 前，先确认它是不是真的无人使用。

不适用：分析单次会话的执行效率（用 `efficiency-audit`）；按日期回顾做了什么（用 `cc-history`）。

## 执行

直接运行脚本，无需大模型解析日志：

```bash
node scripts/skill-usage-audit.mjs                  # 全量统计
node scripts/skill-usage-audit.mjs --days 30        # 只看最近 30 天
node scripts/skill-usage-audit.mjs --skill app-flow # 只看某个 skill
node scripts/skill-usage-audit.mjs --json           # 机器可读输出
node scripts/skill-usage-audit.mjs --no-codex       # 跳过 Codex 日志
```

脚本路径按本 Skill 目录解析（`scripts/skill-usage-audit.mjs`）；日志目录默认 `~/.claude/projects` 与 `~/.codex/sessions`，可用 `--claude-dir` / `--codex-dir` 覆盖。

## 解读报表（必读）

报表分两段，**口径不同，不可相加**：

1. **Claude Code · 正式 Skill 调用**：精确口径。只统计日志中通过 Skill 工具的正式调用记录（含 subagent 转写文件），Bash 命令文本里碰巧出现 skill 名不会被误计。
2. **Codex · 启发式**：Codex 没有统一的 Skill 调用事件，脚本以「工具调用中从安装根（`.agents/skills/`、`.claude/skills/`、`.codex/skills/`）读取 `<name>/SKILL.md`」为信号；系统提示里的技能清单、在仓库里开发 skill 文件都不会被计入。结果偏保守。

**系统性低估的来源**：Skill 内容被"内联使用"（模型读过 SKILL.md/rubric 后，把知识直接写进 subagent 提示词或自行运用）不会留下任何正式记录，任何基于日志的统计都看不见这部分。若要某个 Skill 可被准确统计，需在其 SKILL.md 中要求"必须正式调用、禁止内联替代"（参考 app-flow 对 app-flow-reviewer 的强制调用规则）。

呈现结果时向用户明确这一口径差异，不要把报表数字当作使用量的完整真相。

## 测试

```bash
node --test skills/skill-usage-audit/tests/
```
