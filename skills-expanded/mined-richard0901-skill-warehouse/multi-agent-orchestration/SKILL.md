---
name: multi-agent-orchestration
description: 面向 OpenClaw 的多 agent 编排技能。用于设计或审计多个 session / subagent / ACP agent 之间的任务拆分、上下文裁剪、权限隔离、并行策略与结果回收。
---

# 多 Agent 编排

## 这是什么

多 agent 不是“多开几个助手一起跑”。真正重要的是：

1. 哪些任务该留在主 agent
2. 哪些任务值得委派
3. 每个 agent 的职责边界是什么
4. 上下文和权限如何隔离
5. 并行后怎么回收结果，不把主会话炸掉

## 在 OpenClaw 里何时使用

1. 你要用 `sessions_spawn` 拆分任务
2. 你要同时做代码实现、资料检索、验证
3. 你在设计 thread-bound ACP 工作流
4. 你在审计子 agent 之间是否权限串线
5. 你在思考哪些任务适合并行

## 核心原则

1. 委派不等于转移责任。
2. 主 agent 仍然负责最终整合与对用户负责。
3. 多 agent 的收益来自“分工清晰”，不是数量多。
4. 子 agent 默认最小权限。
5. 并行只是手段，不是默认答案。

## OpenClaw 实战分工建议

典型可拆成：

1. 主 agent
   - 理解用户目标
   - 定义拆分策略
   - 审核结果
   - 对用户汇报
2. 实现 agent
   - 写代码
   - 生成文件
   - 局部测试
3. 检索 agent
   - 查文档
   - 提取资料
   - 汇总来源
4. 验证 agent
   - 独立测试
   - 边界检查
   - 给 PASS / FAIL

## 什么时候别用多 agent

1. 单文件小改动
2. 上下文特别依赖连续细节
3. 任务本身很短
4. 你还没想清楚分工，就只是想“高级一点”

## 推荐工作流

1. 先决定哪些工作在主路径完成。
2. 再决定哪些子任务可并行。
3. 为每个 agent 写清楚 contract：
   - 目标
   - 工具
   - 权限
   - 输出格式
   - 停止条件
4. 为每个 agent 只给必要上下文。
5. 子 agent 回来后，由主 agent 做合并、去重、冲突处理。
6. 最终结果必须由主 agent 统一验收与交付。

## 常见失败模式

1. 什么都委派，主 agent 自己反而不工作。
2. 子 agent 拿到和主 agent 一样宽的权限。
3. 子 agent 回传原始大段 transcript，污染主上下文。
4. 没有 stop condition，线程越开越多。
5. 没有 verifier，最后只是多个 agent 互相吹捧。

## OpenClaw 落地建议

1. 大任务才开 agent，小任务直接做。
2. ACP harness 请求直接用 `sessions_spawn(runtime="acp")`，不要绕远路。
3. 多 agent 结果回传尽量摘要化。
4. 验证 agent 尽量独立，别让实现 agent 兼任验证。
5. 给长期 session 起明确 label，避免后期难以辨认。

## 你可以产出的东西

1. 一张 agent 角色矩阵
2. 一份“何时本地做、何时委派、何时并行”的决策表
3. 一份多 agent 收口与 cleanup 清单
