---
title: "给博客猫教一个新技能：论文精读"
date: 2026-03-06
tags:
  - AI Agent
  - OpenClaw
  - 自动化
  - 论文精读
lang: zh
english: ai-agent/openclaw/openclaw-paper-reading-skill.en
---

> 🌐 [Read in English](./openclaw-paper-reading-skill.en.md)

之前搭好了 [[openclaw-blog-workflow|24 小时知识管家]]，minicat 已经能帮我写笔记、翻译、提交 git。但每次读论文还是纯手动——fetch 论文、提取插图、写中英双语笔记、更新 index、commit——流程固定但步骤多。于是决定把这套流程沉淀成一个可复用的 skill。

## 动机

读论文写笔记的流程其实非常模式化：

```
拿到论文链接
  ↓ 获取全文（arxiv HTML > PDF）
  ↓ 提取关键插图
  ↓ 写中文精读笔记（公式、实验数据、反思）
  ↓ 翻译英文版
  ↓ 更新 index.md
  ↓ git commit
```

每一步的逻辑都是固定的，变化的只是论文内容本身。这正是适合封装成 skill 的场景。

## 设计思路

### 插图提取：arxiv HTML 优于 PDF

一开始想用 PyMuPDF 从 PDF 提取图片。实际测试发现一个大问题：PDF 里存的是**原始嵌入图片**，不是渲染后的完整 figure。比如一个包含 4 张主播照片的 grid figure，PDF 提取出来是 4 张独立的人脸照片，而不是带标注的完整图表。

后来发现 arxiv 的 HTML 版本（`arxiv.org/html/ID`）里有完整渲染好的图片，命名为 `x1.png`、`x2.png` 等，直接下载就是论文里看到的样子。

所以最终策略是：**arxiv HTML 优先，PDF 作为回退**。写了一个 Python 脚本封装这两种模式：

```bash
# 优先：从 arxiv HTML 下载完整渲染图
python .skills/paper-reading/scripts/extract_figures.py \
  --arxiv 2602.09401 --output /tmp/figures/

# 回退：从 PDF 提取嵌入图片
python .skills/paper-reading/scripts/extract_figures.py \
  --pdf paper.pdf --output /tmp/figures/
```

脚本输出一个 `manifest.json`，记录每张图的文件名、来源 URL 和大小，方便后续挑选。

### 目录自动分配

论文笔记统一放在 `<领域>/papers-reading/` 目录下，按论文领域自动分配：

| 论文领域 | 目录 |
|---|---|
| 推荐系统、排序、CTR | `recommender-systems/papers-reading/` |
| Transformer、LLM 架构 | `machine-learning/papers-reading/` |
| AI Agent、多智能体 | `ai-agent/papers-reading/` |

这样论文笔记和手写的学习笔记（放在 `models/`、`training/` 等目录）自然分开，结构更清晰。

### 精读模板

默认写**精读**风格——读者不需要看原文就能学到核心内容。文章结构固定为：核心思路 → 系统架构（含公式）→ 训练目标 → 实验结果（含完整数据表）→ 值得思考的点 → 参考。

"值得思考的点"是最重要的部分，要求有真正的反思而不是复述摘要。比如指出论文没讨论的局限性、跟其他工作的联系、可能的改进方向。

也支持轻量模式——说"简单总结一下"就只写 1 页摘要。

## 融入 minicat

先说清楚 OpenClaw 的 skill 系统是怎么工作的。OpenClaw 有一套内置 skill 机制：它会扫描自己的全局 skills 目录（`/opt/homebrew/lib/node_modules/openclaw/skills/`），把每个 skill 的 `name` 和 `description` 注入到 agent 的系统提示里。当用户消息匹配到某个 skill 的 description 时，agent 就去读完整的 SKILL.md 并按流程执行。这是**系统级**的 skill，随 OpenClaw 安装走，比如内置的 `weather`、`healthcheck`、`coding-agent` 都在这里。

博客仓库里的 `.skills/paper-reading/` 是另一回事——这是我自定义的**项目级** skill，minicat 不会自动扫描它。minicat 的行为规范完全来自 workspace 里的 markdown 文件，每次启动 session 会主动读取 `SOUL.md`（身份）、`BLOG_INSTRUCTIONS.md`（博客操作指南）等。

所以我在 `BLOG_INSTRUCTIONS.md` 里加了"论文精读"章节，告诉 minicat：触发词是什么、流程是什么、脚本在哪。`.skills/` 目录是**工具箱**，`BLOG_INSTRUCTIONS.md` 是**使用说明**——minicat 读了说明，知道工具在哪、怎么用。

加入的触发词：

| Rose 说的话 | 行为 |
|---|---|
| arxiv 链接 / 论文 PDF / "读一下这篇" | 进入论文精读流程 |
| 技术博客链接 + "写个笔记" | 同上，按博客模式处理 |

## 测试

用 [SARM 论文](https://arxiv.org/abs/2602.09401)（快手直播推荐排序）跑了一次完整流程：

1. **内容获取** ✅ — WebFetch 抓 arxiv abstract + HTML 全文
2. **插图提取** ✅ — `extract_figures.py --arxiv` 提取 9 张图，选了 5 张（方法对比、系统架构、门控融合、部署流水线、案例分析）
3. **中文精读** ✅ — 完整公式、4 张实验数据表、5 条反思
4. **英文翻译** ✅ — 同结构自然翻译
5. **index.md** ✅ — 新建 `papers-reading/index.md`
6. **git commit** ✅

生成的笔记在 [[sarm-llm-livestream-ranking|这里]]，带插图、完整实验数据和 ablation 分析。

## Skill 文件结构

```
.skills/paper-reading/
├── SKILL.md              # Pipeline 完整定义（流程文档）
└── scripts/
    └── extract_figures.py # 插图提取（arxiv HTML + PDF 双模式）
```

加上 `BLOG_INSTRUCTIONS.md` 里的论文精读章节（minicat 的调用入口），两个地方配合，一个存工具，一个写规则。

## 小结

把重复性工作封装成 skill 的核心收益不是"省时间"——一篇论文精读笔记本身就需要大量思考。真正的价值是**流程标准化**：每次都走相同的 pipeline，不会漏掉插图、忘了更新 index、或者中英文版结构不一致。

下次想读论文的时候，只需要发一个 arxiv 链接就好了。
