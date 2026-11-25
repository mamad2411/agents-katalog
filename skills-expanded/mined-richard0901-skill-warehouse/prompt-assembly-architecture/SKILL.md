---
name: prompt-assembly-architecture
description: 面向 OpenClaw 的 Prompt 拼装架构技能。用于设计或审计 system prompt、workspace rules、skills、memory、环境信息和动态注入内容的分层与边界。
---

# Prompt 拼装架构

## 这是什么

prompt 不应该是临时拼出来的一大段字符串，而应该是一个有边界、有稳定前缀、有动态尾部的装配系统。

这个 skill 关注的是：

1. 哪些内容是稳定的
2. 哪些内容是动态的
3. 如何划出边界
4. 如何减少改一处就导致整个前缀失稳
5. 如何让缓存、调试、diff 都更容易做

## 在 OpenClaw 里何时使用

1. 你在整理 system prompt
2. 你在混合 workspace rules、skills、memory
3. 你发现 prompt 越堆越乱
4. 你想优化 prompt cache 命中
5. 你想搞清楚哪些信息应该晚注入

## 核心原则

1. 稳定内容尽量放前面。
2. 动态内容尽量后置。
3. 用 section 而不是大字符串思维。
4. 先分层，最后再 join。
5. 不要让运行时状态污染静态前缀。

## 在 OpenClaw 里的典型分层

### 静态层

1. 基础身份
2. 长期行为规则
3. 通用格式要求
4. 工具使用总原则
5. 安全规则

### 动态层

1. 当前 channel / session 元信息
2. 当前时间
3. 当前 workspace context
4. memory 检索结果
5. 这轮命中的 skill 说明
6. 当前工具面或临时能力变化

## 推荐做法

1. 先列出所有 prompt 组成部分。
2. 给每一部分标记：
   - 稳定
   - 半稳定
   - 每轮动态
3. 把每部分独立成 section。
4. 为动态部分建立清晰注入点。
5. 让 builder 最终返回 section 数组，再统一拼接。

## 常见失败模式

1. 一开始就拼成大字符串，后面谁也拆不动。
2. 静态前缀里读了运行时状态，导致缓存不断失效。
3. 风格规则和执行规则反复在多个 helper 中重复。
4. 技能说明每轮全量注入。
5. 为了省事把所有东西都塞在 system prompt 顶部。

## OpenClaw 落地建议

1. 把固定规则和当前会话态区分开。
2. memory 与 skills 都应晚注入。
3. 当前时间、会话元信息、临时工具变化不要污染静态区。
4. 每个 section 最好有稳定名字，方便审计和 diff。
5. 设计时就考虑缓存，而不是事后补救。

## 你可以产出的东西

1. 一张 prompt section 地图
2. 一份“静态 / 动态边界”清单
3. 一个最小化 prompt builder 设计草图
