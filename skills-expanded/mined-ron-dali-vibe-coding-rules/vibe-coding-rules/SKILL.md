---
name: Vibe Coding Rules
id: vibe-coding-rules
version: 2.7.0
primary: true
description: >
  6个自我进化的AI编程纪律Skill。改代码前强制自查→安全执行→改后28条规则扫描→自动化测试→变更日志，一条龙闭环。
  🍞独家面包屑系统：文件自动记住耦合关系和历史坑位。信任分级规则自生长：重复Bug升级为硬规则。
  V2.7新增渐进式采纳L1/L2/L3 + 失败恢复模式 + 多技术栈检测。
  由代码小白用AI写14万行代码的踩坑经验沉淀。支持CodeBuddy/Cursor/Windsurf。Apache 2.0。
  6 self-evolving AI coding discipline Skills. Pre-check → Safe exec → 28-rule post-check → Auto-test → Changelog. Closed loop.
  🍞 Breadcrumb auto-seeding. Trust-tiered rule growth. V2.7: Progressive L1/L2/L3 + Failure recovery + Multi-stack detection.
tags:
  - vibe-coding
  - ai-coding
  - code-quality
  - coding-assistant
  - developer-tools
  - self-check
  - testing
  - pipeline
  - breadcrumb
  - self-growing
  - progressive-adoption
category: 开发工具
author: 躺不平联盟
website: https://tangbuping.com
license: Apache-2.0
---

# Vibe Coding Rules V2.7

> **AI 写代码最大的敌人，是它自己——它会忘记昨天修好的 Bug，会在同一个坑里反复跌倒。**
>
> 6 个会自我进化的 Skill，给 AI 装上"编程纪律"。从改前自查到变更记录，一条流水线闭环交付。
> V2.7 新增**渐进式采纳**：改3行不用跑全套，改功能才走全链路。按需激活，不浪费上下文。
>
> **AI's biggest enemy is itself — it forgets the bugs it fixed yesterday.**
> 6 self-evolving Skills. V2.7 adds **Progressive Adoption**: 3-line fix ≠ full pipeline. Activate only what's needed.

---

## ⚡ Before & After / 装前装后

| 场景 | 没装之前 | 装了之后 |
|:--|:--|:--|
| 数值 0 被当 false 吞掉 | 每次排查半小时 | coding-principles 改前就拦住了 |
| `<select>` 假选中 | 用户反馈才修 | safe-terminal-executor 脚本自验证 |
| 同一个 Bug 犯第 3 次 | AI 毫无记忆 | self-check 自动升级为硬规则，永不再犯 |
| 改完代码不知道影响谁 | 发布后炸了才知道 | 🍞面包屑标出耦合文件，改前就提醒 |

---

## 🎯 Progressive Adoption / 渐进式采纳 (V2.7 NEW)

> **不是每次改动都需要跑 6 个 Skill。按改动大小自动匹配合适的纪律层数，避免浪费上下文。**
> **Not every change needs all 6 Skills. Match discipline depth to change size. Save context.**

| Level | 触发条件 / Trigger | 激活的 Skill / Skills Activated | 适用场景 / Use Case |
|:--|:--|:--|:--|
| **L1 · 轻量** | 改动 ≤ 3 个文件，≤ 30 行净变更 | `coding-principles` 五原则自检 | 修小 Bug、改文案、调 CSS |
| **L2 · 标准** | 改动 3-10 个文件，或涉及路由/数据流 | L1 + `self-check` 28条规则 | 中等改动、修跨模块 Bug |
| **L3 · 完整** | 改动 > 10 个文件，或新功能/重构 | L1 + L2 + `web-testing` + `changelog` 全链路 | 新功能开发、架构调整 |

**自动降级规则 / Auto-downgrade rules**：
- 改动项目中检测到 5+ 个违规 → 不阻塞交付，但标记为 BASELINE（基线债务），下次同模块改动时升级为 L3
- 改动 `safe-terminal-executor` 始终可用，无论 L1/L2/L3（网络命令安全封装不需要上下文代价）
- 用户可手动指定层级：「用 L2 自检」或「走完整 L3」

---

## 📦 Install / 安装

```bash
# CodeBuddy / Cursor / Windsurf
openclaw skills install @ron-dali/vibe-coding-rules

# 或手动
git clone https://github.com/Ron-dali/vibe-coding-rules.git
```

安装后对 AI 说：**"初始化流水线"**，AI 自动检测项目并配置。

---

## Pipeline Architecture / 流水线架构

```          ┌── L1 轻量（≤3文件，≤30行变更）
          │   └→ coding-principles（五大原则 + 面包屑预扫描）
          │
          ├── L2 标准（3-10文件，或涉及路由/数据流）
          │   └→ L1 + self-check（28条规则 + 阻断点 + 面包屑播种）
          │
          └── L3 完整（>10文件，或新功能/重构）
              └→ L2 + web-testing + changelog → ✅ 闭环交付
```

```
coding-principles (5 Principles + 🍞 Breadcrumb Pre-scan / 改前五大原则 + 面包屑预扫描)
  → safe-terminal-executor (Safe Terminal Exec / 安全终端执行，始终可用)
    → Write/Modify Code / 编写修改代码
      → self-check (28 Rules + Integrity Gate 🛑 + Breadcrumb Seeding / 28条规则自检 + 完整性阻断点 + 面包屑播种)
        → web-testing (Auto Regression Test / 自动化回归测试，阻断点通过后强制)
          → changelog (Changelog + Growth Detection / 变更日志 + 生长检测)
            → ✅ Closed Loop / 闭环交付
```

## Included 6 Skills / 包含的 6 个 Skill

| Skill | Function / 功能 |
|-------|------|
| 🥇 `coding-principles` | Pre-code 6-principle self-check + 🍞 pre-scan + 3 trap auto-intercept / 改代码前强制自检六大原则 + 3个常见陷阱自动拦截 |
| 🛡️ `safe-terminal-executor` | Safe terminal wrapper, timeout protection + forced exit / 终端命令安全封装，超时保护+强制退出 |
| 🔍 `self-check` | Post-code 28-rule scan + 🛑 integrity gate (V2.6) + trust-tiered growth + 🍞 breadcrumb auto-seeding / 改后28条规则逐项检查+完整性阻断点+信任分级+🍞面包屑播种 |
| 🧪 `web-testing` | DOM assertion + screenshot + OCR automated regression test / DOM断言+截图+OCR自动化回归测试 |
| 📝 `changelog` | Auto changelog generation + rule growth detection / 变更日志自动生成+规则生长检测 |
| 🚀 `pipeline-init` | One-click project pipeline bootstrap / 新项目一键初始化流水线 |

## Core Features / 核心特性

- 🎚️ **Progressive Adoption L1/L2/L3 / 渐进式采纳** — 改3行用L1轻量自检，改功能走L3全链路，按需激活不浪费上下文 / Match discipline depth to change size. No overkill.
- 🔄 **Self-Growing Rules / 规则自生长** — Today's pitfall becomes tomorrow's hard rule the AI can't break / 今天踩的坑，明天变成AI不能再犯的硬规则
- 🍞 **Breadcrumb System V2.7 / 面包屑系统** — Auto-plant coupled files + historical gotchas in file headers, AI never forgets / 文件头部自动播种耦合关系+历史坑位，AI不再失忆
- 🎯 **Trust-Tiered Growth / 信任分级** — Tier0 Observation Pool → Tier1 [SOFT] → Tier2 [HARD], auto promote/demote / 观察池→软规则→硬规则，自动晋升退役
- 🛡️ **Failure Recovery Mode / 失败恢复模式** — 5+ violations → HARD/SOFT/BASELINE 分组，不阻塞交付 / Multi-violation grouped recovery, delivery unblocked
- 🌍 **Cross-Platform / 跨界兼容** — Works with CodeBuddy, Cursor, Windsurf / 三种AI Agent通用

## Who Needs This? / 谁需要这个？

- 🐣 AI coder who doesn't know programming → Discipline exoskeleton / 用AI写代码但不懂编程 → 编程纪律外骨骼
- 💻 Solo dev / one-person company → Your own QA team / 独立开发者一人公司 → 自己的QA团队
- 🏢 Small team using AI assistance → Unified quality standards / 小型团队用AI辅助 → 统一质量标准
- 🤖 Heavy AI Agent user → Agent gets smarter over time / 重度AI Agent用户 → Agent越用越聪明

## Author / 作者

躺不平联盟 (TangBuPing) — A coding beginner who wrote 140,000 lines of code across a 3-platform system with AI, distilling every painful lesson into these 6 Skills.
代码小白用AI写140000行三端平台，把踩坑经验沉淀为这6个Skill。

[GitHub](https://github.com/Ron-dali/vibe-coding-rules) · [tangbuping.com](https://tangbuping.com)
