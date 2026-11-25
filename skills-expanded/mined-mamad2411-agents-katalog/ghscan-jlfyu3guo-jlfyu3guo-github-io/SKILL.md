---
title: book-to-skill：把技术书编译成 Agent 技能
date: 2026-07-29
category: AI Agent
tags: [book-to-skill, Hermes Agent, Agent Skills, 知识管理, 上下文优化]
source: 昕科技
source_url: "https://mp.weixin.qq.com/s/FvNZvM8ymi_g1UZsRfU0kw"
repo_url: "https://github.com/virgiliojr94/book-to-skill"
repo_name: "github.com/virgiliojr94/book-to-skill"
skills_note: "安装：pip install git+https://github.com/virgiliojr94/book-to-skill.git　|　生成的技能放入 ~/.hermes/skills/ 即可被 Hermes 加载"
summary: 开源工具 book-to-skill 把技术书预编译成 Agent 可直接加载的技能：按章节懒加载，单次查询仅约 5K token，比全文注入上下文省 24~51 倍；核心价值是从"检索相似段落"升级为"直接调用作者框架"。
---

## 一句话

**book-to-skill** 是一个"技能编译器"：把技术书（PDF/文本）预编译成 AI Agent 能直接加载的 Skill，而不是每次把全书塞进上下文让它慢慢翻页。

## 核心知识点

**1. 结构：懒加载是省 token 的关键**

输出是一个标准技能目录，章节按需加载：

```text
skills/<book-name>/
├── SKILL.md      # 核心心智模型 + 章节索引（~4K tokens）
├── chapters/     # 每章一个文件，按需加载（各 ~1K tokens）
├── glossary.md   # 术语表
├── patterns.md   # 技术/算法/设计模式
└── cheatsheet.md # 决策表 + 速查
```

不问某一章，那一章就不占 token 预算。

**2. 收益：不是省一点，是省几十倍**

| 方式 | Token/问题 | 倍数 |
|---|---|---|
| 全书注入上下文 | 119K–256K | 24×–51× |
| Agent 自行翻页搜索 | 12K–78K | 2.4×–15.6× |
| **book-to-skill** | **~5,000** | — |

关键差别：全文注入**每轮对话都要付**成本；skill 只付一次性提取成本（约 $1/本），之后每次查询只加载几千 token。

**3. 与 RAG 的本质区别（最重要的一条）**

- **RAG** → 切块 + 向量化 + 找相似段落，回答的是"**哪里提到了 X**"
- **book-to-skill** → 提取作者构建的**框架、原则、反模式、决策规则**，回答的是"**这里有 12 个框架，拿去用**"

Agent 加载 skill 后不是在翻书，而是在**用作者的框架思考**。省 token 只是副产品。

## 集成到 Hermes Agent（三步）

Hermes Agent 的 `~/.hermes/skills/` 兼容开放的 Agent Skills 标准，所以可直接复用。

```bash
# 1. 安装
pip install git+https://github.com/virgiliojr94/book-to-skill.git
book-to-skill --check

# 2. 把文档编译成技能
book-to-skill ~/books/技术书.pdf <技能名>
# 多文件合并成一个技能也支持
book-to-skill ~/papers/a.pdf ~/notes/b.txt unified-research

# 3. 让 Hermes 加载
cp -r ~/.agents/skills/<技能名>/ ~/.hermes/skills/<技能名>/
# 或软链（后续更新无需再复制）
ln -s ~/.agents/skills/<技能名> ~/.hermes/skills/<技能名>
```

调用方式：

```text
@skill:<技能名> 讲一下这个框架的核心原则
@skill:<技能名>/ch03 加载第三章内容
```

## 适用范围

名字叫"书转技能"，但输入不限于书——**架构决策记录、runbook、品牌指南、RFC、论文合集**等任何你频繁翻阅的文档都适用。

> 判断标准：如果一个文档频繁到你觉得"要是我背下来就好了"，它就是候选者。

## 现状

项目发布两个月即达 11.6k stars / 1.3k forks，说明"知识无法随时调用"是普遍痛点。

**本质转变**：不是"更好地记笔记"，而是**让 AI 以它能直接理解的方式替你记住**。

---
*测试环境：WSL2 + Python 3.13 · book-to-skill v1.2.0 · Hermes Agent（Nous Research）*
