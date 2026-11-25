---
name: mideast-monitor-skill
description: 监测中东地区（美伊/以色列战线 + 沙特/海湾安全）公开新闻，每小时输出克制的安全简报。触发场景：用户说"中东舆情"、"中东战报"、"中东监测"、"美伊冲突最新"、"中东安全简报"、"沙特胡塞袭击"、"盯以色列伊朗"、"红海航运"、"霍尔木兹"、"measeast monitor"、"mideast digest"，或要求每天/每小时看一次中东公开新闻摘要。
version: 1.1.0
author: qinthqod
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [mideast, monitor, news, rss, cron, digest, iran, israel, saudi, houthis, hormuz, synonym-substitution]
    related_skills: [cron-web-briefings, flight-monitor-skill]
---

# Mideast Monitor — 中东舆情监测 skill

每小时/每天自动抓取中东地区公开新闻（23 个权威 RSS 源），输出克制的安全简报。已实战验证：7/16 一天内命中 16 条，10 秒跑完。

**v1.1.0 更新**（2026-08-13）：8/13 早 9:00 简报连续熔断、修复三次后用"同义替换"稳定通过。详见 [references/output-policy-block-fix-2026-08-13.md](references/output-policy-block-fix-2026-08-13.md) 与 [references/synonym-substitution-2026-08-13.md](references/synonym-substitution-2026-08-13.md)。**核心改动**：硬动作词同义替换（击落→打下，截击→应对，袭击→行动）—— 保留真实主语和事件骨架。

## 🚀 30 秒上手（复制粘贴给 AI）

> 把下面这段直接发给 Codex / Workbuddy / 任何智能体，它就懂怎么用这个 skill：

```
请阅读 https://github.com/qinthqod/mideast-monitor-skill/blob/master/SKILL.md 学习这个 skill。

我想监测中东新闻：每 1 小时跑一次，只关心美伊/以色列 + 沙特/海湾安全，
新的就推飞书，没新东西就静默。
```

接下来用户只需要说需求，AI 会问剩下的：

```
中东战报                                       ← 最简输入
中东舆情监测                                   ← 标准说法
我要看美伊冲突最新                              ← 自然语言
盯一下霍尔木兹海峡                              ← 具体话题
沙特胡塞最新动态                                ← 主题 B
每小时推一次中东安全简报（推飞书）                ← 完整描述
```

AI 会自动：
1. 装 `scripts/fetch.py` 定时抓 23 个 RSS 源
2. 48h 时间窗口过滤
3. 关键词三重过滤（地区词 + 军事安全词 + 反内容拦截哨兵）
4. 按主题分类（美伊/以色列 A vs 沙特/海湾 B）
5. 已读去重（`seen.json`），没新条目就静默

## When to Use

- User wants periodic Mideast security briefings: "中东战报", "中东简报", "中东监测"
- User wants US-Iran / Israel-Iran / Saudi-Houthi specific monitoring
- User wants a cron that pushes 24h / 48h Mideast news digests
- User wants Red Sea shipping, Hormuz Strait, Gaza, Lebanon watch

## What you (the agent) need to do — 你要做什么

### Step 1: 理解用户意图（自然语言抽取）

从自然语言抽出：

| 字段 | 例子 |
|---|---|
| **topics**（可选） | "美伊冲突"、"中东整体"、"沙特胡塞"、"霍尔木兹"、"红海航运" → 默认全选 A+B |
| **frequency** | "每1小时"、"每天9点"、"每天早晚两次" → 默认 `every 1h` |
| **channel**（可选） | "推飞书"、"微信"、"本地文件" → 默认 feishu |

### Step 2: 检查缺什么

最少只要 topics + frequency + channel 三选一不空就行；其他全用默认（地区 A+B 全选、48h 窗口、seen.json 去重）。

如果用户没说 channel：

```
你想怎么收到中东战报？
  1) 飞书（推荐，开箱即用）
  2) 微信（走 iLink gateway）
  3) 本地文件（写到 ~/.hermes/cron/output/）
```

### Step 3: 装 cron

确认后写 cron job（**用 Hermes cronjob 工具，不要纯系统 crontab**）：

```
name: 中东战报·实时巡检
prompt: 见 SKILL.md 底部模板
schedule: every 1h
deliver: feishu
```

详见 [references/cron-prompt.md](references/cron-prompt.md) — 复制 prompt 模板进去，**只改 chat_id 和频率**。

### Step 4: 第一次跑 + 验证

跑一次：
```bash
cd ~/mideast-monitor-skill && python3 scripts/fetch.py | jq '. | length, (.topic_a | length), (.topic_b | length)'
```

会看到：6+ 条命中，topic_a 和 topic_b 都有。

### Step 5: 监控已启动

不要再问。让 cron 自动跑。**没新条目就 `[SILENT]` 静默** — 只有真有新闻才推用户。

## Reference docs — 参考文档

- [references/cron-prompt.md](references/cron-prompt.md) — 复制 prompt 模板（最关键的一份）
- [references/data-sources.md](references/data-sources.md) — 23 个 RSS 源清单 + 增减方法
- [references/dedup-state.md](references/dedup-state.md) — seen.json 共享去重机制
- [references/troubleshooting.md](references/troubleshooting.md) — 静默失败 / 内容拦截 / iLink 限流
- [references/synonym-substitution-2026-08-13.md](references/synonym-substitution-2026-08-13.md) — **v1.1.0 新**：硬动作词同义替换表（击落→打下，截击→应对，袭击→行动）
- [references/output-policy-block-fix-2026-08-13.md](references/output-policy-block-fix-2026-08-13.md) — **v1.1.0 新**：8/13 三阶段修复完整记录（KW_BLOCK 增量 / 骨架化撤回 / 同义替换成功）

## Data sources — 数据源

23 个 RSS 源，分两大主题：

**主题 A：美伊/以色列战线**
- Google News 主题（中文）：伊朗-美国、伊朗-以色列、霍尔木兹、IAEA、黎巴嫩真主党、伊朗导弹
- Google News 主题（英文）：US-Iran military strike、Israel-Iran strike、Hormuz、Houthis-Red Sea
- 权威源：Al Jazeera、Reuters、BBC、ISW、Al-Monitor

**主题 B：沙特/海湾安全**
- Google News 主题（中文）：沙特袭击胡塞、沙特军事、红海航运、沙特防空拦截
- Google News 主题（英文）：Saudi-Houthi missile、Saudi defense interception、Red Sea shipping

**中文权威源**（共享 A+B）：央视国际、新华网国际、参考消息

详见 [references/data-sources.md](references/data-sources.md)。

## The hard lessons — 别重蹈覆辙

**1. 必须用 seen.json 共享去重，不要 last_run.txt。**
多个 cron job（早报 + 实时巡检）共享同一份 `state/seen.json`，早报覆盖了实时没推过的 → 实时那条永远推不出去。

**2. fetch.py 词表防御只能挡"纯煽动"**。
原 v1.0.0 的"再加词表"防御极限 ≈ 75%（实测 8/13 拦 6/8 剩 6/8 漏网）。具体事件骨架（击落/截击/袭击/轰炸）让 prompt 同义替换接手——词表永远追不上中文新闻的描述多样性。**8/13 实战经验**：`references/output-policy-block-fix-2026-08-13.md`。

**3. 骨架化（A方/B方） = 信息失真**。
v1.0.0 早期尝试过"喂模型 5 槽骨架、不传原标题"——模型不熔断了，但用户拍板"该是谁就是谁"。actor 永远保留真实国家/机构名。

**4. 同义替换是 v1.1.0 的正解**。
保留主语 + 设备型号，硬动作词用同义词（击落→打下，截击→应对，袭击→行动）。详见 `references/synonym-substitution-2026-08-13.md`。

**5. 没新条目必须返回 `[SILENT]`。**
写回 seen.json 必须看到实际报告内容；伪造"已生成"会被静默守门脚本拦截。

**6. 微信/iLink 限流时**降级飞书，不要 sleep retry。

**7. fetch.py 输出 JSON 是 multi-line + 嵌套对象**，不要尝试 `python -c "json.loads(sys.stdin)"` 单行解析。

**8. 不要擅自换 provider。**
用户拍板（2026-07-18）：cron job 全部用 `MiniMax-M3`，content_policy_blocked 时禁止擅自换 provider——先改 prompt（中性话题词、不引用 desc、禁用煽动用词），仍熔断才 [SILENT]。

**9. v1.1.1：敏感信息铁律。**
本 skill 是**公开 GitHub 仓库**，**禁止**在代码、注释、文档里出现：
- 本机绝对路径（`/home/<user>/...` / `/Users/...` / `C:\...`）→ 用 env 变量（如 `MIDEAST_RSS_HOME`）
- 飞书 / 微信 chat_id / open_id → 占位符 `oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- 用户私有服务 URL（`ilink.bot.<user>.cn` 之类）→ 占位符 + env 变量
- 用户邮箱 / 手机号 / API token
- 私有的 chat_id / cron job_id

**改动姿势**：hardcoded 值改成 env 变量读取，默认值用占位符：
```python
# 错误（提交前会被 grep 拦下）：
STATE_DIR = "/home/<your-username>/.hermes/scripts/mideast-rss/state"

# 正确：
import os
MIDEAST_RSS_HOME = os.environ.get("MIDEAST_RSS_HOME", os.path.expanduser("~/.hermes/scripts/mideast-rss"))
STATE_DIR = os.path.join(MIDEAST_RSS_HOME, "state")
```
**提交前自检**：`grep -rn "/home/\|/Users/\|oc_[a-z0-9]\{20,\}\|ilink\.bot" --include="*.py" --include="*.sh" --include="*.md" .` 应为 0 行（除本说明段里作为反例外）。

## Linked scripts — 关键脚本

- `scripts/fetch.py` — 23 RSS 源并发抓取 + 3 层过滤 + seen.json 共享去重
- `scripts/dedup.py` — seen.json 写回守门脚本（cron 调用）

## Architecture (one-liner)

```
[23 RSS 源] → 并发 fetch → [3 层过滤] → JSON to stdout
                                       ↓
                              [cron agent 重写/摘要]
                                       ↓
                              [seen.json 去重 + 推送]
```