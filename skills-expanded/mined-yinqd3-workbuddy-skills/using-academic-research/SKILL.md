---
name: using-academic-research
description: Academic Research Skills 学术研究技能集入口。覆盖从选题、文献调研、论文写作到同行评审的完整学术研究管线。触发词：写论文、深度研究、文献综述、同行评审、审稿、学术管线、research、paper、review。
agent_created: true
---

# Academic Research Skills — WorkBuddy 版

基于 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)（6.4k+ Stars）适配的学术研究技能集。

## 核心理念

> **AI 是副驾驶，不是驾驶员。** 这套工具不会替你写论文。它处理苦力活——文献检索、引文格式化、数据验证、逻辑一致性检查——让你能专注于需要真正用脑的部分：定义问题、选择方法、解读数据、写出"我认为"之后那句话。

## 四技能管线

```
选题探索 → 深度文献调研 → 论文写作 → 同行评审 → 修回 → 发表
```

| # | 技能 | 子代理 | 模式 | 定位 |
|:--:|:---|:--:|:--:|:---|
| 1 | `deep-research` | 13 个 | 7 种 | 深度文献调研：选题→检索→分析→报告 |
| 2 | `academic-paper` | 12 个 | 10 种 | 论文写作：配置→写作→引文→格式化 |
| 3 | `academic-paper-reviewer` | 7 个 | 6 种 | 同行评审：多视角审查→编辑决策→修回路线图 |
| 4 | `academic-pipeline` | 4 个 | 10 阶段 | 全链路编排：调研→写作→审查→修改→定稿 |

## 四条原则

1. **人机协同** — AI 做苦力，你定方向
2. **每一步都可验证** — 完整性检查、反泄露协议、统计验证
3. **质量优先于速度** — 风格校准、写作质量检查、同行评审模拟
4. **引用真实性** — 100% 引文核验、Semantic Scholar API 验证

## 适配说明

原版为 Claude Code 设计，WorkBuddy 版适配：
- 子代理调度：Claude Code Task → WorkBuddy `Agent` 工具
- 文件操作：Claude Code → WorkBuddy `Read`/`Write`/`Edit`/`Bash`
- 语言：繁体→简体中文适配，保留中英双语触发
- 格式输出：LaTeX/DOCX → 依赖本地工具（Pandoc、tectonic 等）
