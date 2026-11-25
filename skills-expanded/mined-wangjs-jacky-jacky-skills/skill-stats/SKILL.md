---
name: skill-stats
description: "查看本机 skill 使用频率统计：哪些 skill 高频、哪些近期常用、哪些长期没碰过（可考虑清理）。数据由本插件的采集 hook 持续记录，区分 AI 自动调用 与 用户手输 /命令 两种来源。触发：用户说『/skill-stats、skill 使用频率、哪些 skill 常用、哪些 skill 没用过、skill 使用统计、skill 排行、我的 skill 用得多吗、清理不用的 skill』。"
---

# skill-stats —— Skill 使用频率统计

## 这个 skill 做什么

读取使用日志 `~/.claude/skill-usage.jsonl`，输出一张排行榜：每个 skill 用了多少次、其中多少是 AI 自动调用 / 多少是用户手输 `/命令`、近 7 天热度、最近一次使用时间，以及超过 30 天没再碰过的「僵尸 skill」。

数据由本插件的**采集 hook 自动记录**（Claude Code 通过 `hooks/hooks.json` 注册；Codex 通过 `~/.codex/hooks.json` 注册），挂在两个事件上：
- **PostToolUse(Skill)** —— AI 每次主动调用 skill，记 `source=ai`
- **UserPromptSubmit** —— 用户每次手输 `/xxx` 命令（已过滤 `/help`、`/clear` 等内置命令），记 `source=user`

Codex 也会把这两个事件转发到同一个采集脚本，因此 Codex 中的 Skill 调用会写入同一份 `~/.claude/skill-usage.jsonl`。

## ⚠️ 强制规则

> 当用户问「skill 使用频率 / 哪些 skill 常用 / 哪些没用过 / 清理不用的 skill」时，**必须运行本 skill 的统计脚本**，禁止手动去扒日志文件或猜测。

## 执行步骤

统计脚本是本 skill 目录下的 `scripts/skill-stats.py`（路径用绝对路径，支持在任意目录执行）。运行它，把完整输出原样展示给用户，并用一两句点出关键结论（最常用的是谁、有没有值得清理的僵尸 skill）：

```bash
python3 <本 skill 目录>/scripts/skill-stats.py
```

根据用户诉求附加参数：

| 用户想看 | 参数 |
|----------|------|
| 默认全部时间排行 | （无） |
| 近 7 天热度 | `--days 7` |
| 只看前 10 名 | `--top 10` |
| 只看用户手动触发的 | `--source user` |
| 只看 AI 自动调用的 | `--source ai` |
| 哪个项目爱用哪些 skill | `--by-project` |

## 解读要点

- **总数 = AI + 用户**：同一次 `/tt` 可能既被 UserPromptSubmit 记一次（user），后续 AI 真正执行时再被 PostToolUse 记一次（ai）。所以「总数」是「被触发的总热度」，想看「我主动用了多少」就看 `--source user`。
- **近7天** 列反映当前活跃度，比总数更能说明「现在还在用」。
- **🧊 超过 30 天未再使用**：低价值候选，可考虑清理，给上下文瘦身。

## 注意

- 若提示「还没有任何记录」，说明采集 hook 刚装好、还没产生数据；新开一个 Claude Code 会话让 hook 生效，正常用一段时间后再看。
- 数据文件可由环境变量 `SKILL_USAGE_LOG` 覆盖（仅测试用）。
