---
name: prompt-cache-economics
description: 面向 OpenClaw 的 Prompt 缓存经济学技能。用于优化稳定前缀、减少 cache miss、控制技能说明预算、降低动态注入抖动与 token 成本。
---

# Prompt 缓存经济学

## 这是什么

prompt cache 不是小优化，而是一个真实的性能和成本系统。

会影响缓存命中的，不只是 prompt 文本，还包括：

1. 工具面变化
2. 模型变化
3. thinking 配置变化
4. 动态注入内容变化
5. MCP 状态变化

这个 skill 的目标是：让你在设计时就考虑缓存，而不是每轮都重新烧 token。

## 在 OpenClaw 里何时使用

1. 你发现相似请求成本很高
2. 你在设计长期会话或多 agent fork
3. 你在优化 skills / memory / MCP 注入长度
4. 你想减少 cache bust 的来源

## 核心原则

1. 稳定前缀越长越好。
2. 动态尾部越窄越好。
3. 动态状态不要污染静态前缀。
4. 发现类文本要有预算。
5. cache miss 要能解释原因。

## OpenClaw 场景里的高频 cache breaker

1. 每轮变化的时间信息
2. 当前 skill 列表或顺序变化
3. MCP 连接状态变化
4. 临时实验开关
5. thinking 或模型配置变化
6. 同一任务 fork 了不同工具面

## 推荐做法

1. 把长期稳定规则固定在前缀。
2. 把 memory、skills、MCP 状态、当前时间放到动态区。
3. skill listing 要短，不要写成长广告。
4. summary / compact 类任务尽量工具最小化。
5. fork 子 agent 时，若想共享 cache，就尽量保持模型、工具、thinking 一致。

## 常见失败模式

1. 静态区里读取了本轮环境状态。
2. 技能说明无限变长。
3. 每轮重新生成一大段几乎不变的工具说明。
4. 子 agent 想复用父 cache，却换了模型和工具集。
5. 明明 cache 命中差，却不知道是哪个变量导致的。

## OpenClaw 落地建议

1. skill 列表只保留高信号描述。
2. MCP 说明尽量增量化，而不是整块重写。
3. 多 agent 协作时，只有在收益明确时才强求形状一致。
4. 对 compact / summary agent，尽量关闭不必要工具。
5. 定期审视哪些动态段落其实可以延后注入。

## 你可以产出的东西

1. 一张 cache miss 来源图
2. 一份稳定前缀契约
3. 一份 skills / MCP / summary 文本预算表
