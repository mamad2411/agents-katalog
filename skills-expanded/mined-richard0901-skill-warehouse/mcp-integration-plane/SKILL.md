---
name: mcp-integration-plane
description: 面向 OpenClaw 的 MCP 集成平面技能。用于设计或审计 MCP 连接、认证、工具发现、资源发现、超时、会话失效恢复与大结果持久化策略。
---

# MCP 集成平面

## 这是什么

MCP 不是一个普通 RPC 接口，它更像 agent 的外部能力总线。

真正难的不是“能不能连上”，而是：

1. 多种传输方式怎么统一
2. 认证过期怎么办
3. session 失效怎么恢复
4. tool/resource discovery 怎么缓存
5. 超大结果怎么持久化
6. tool 调用出错后怎么区分是 auth、timeout 还是 transport 崩了

## 在 OpenClaw 里何时使用

1. 你在接入新的 MCP server
2. 你在排查 MCP 经常 401 / 404 / timeout
3. 你在设计 MCP 工具如何暴露给 agent
4. 你在做大结果输出的持久化或截断策略
5. 你在做鉴权或 session 恢复逻辑

## 核心原则

1. 把 MCP 当外部能力平面，不要当薄 RPC。
2. auth failure、session expiry、transport loss 必须分开处理。
3. discovery 要缓存，但缓存要有边界。
4. 大结果不要直接冲进上下文。
5. 每次请求都要有独立 timeout 语义。

## OpenClaw 场景里的重点

1. MCP server 连接信息会影响工具面
2. 认证状态变化会影响 agent 可执行路径
3. discovery 结果太长会污染 prompt
4. 大型返回结果应写文件、存引用、或给摘要
5. 失效后的恢复策略要明确，不要一直重试同一个坏状态

## 推荐工作流

1. 先规范 server 配置
2. 明确 transport 类型
3. 明确 auth 来源与刷新逻辑
4. 缓存 discovery 结果，但要允许失效重建
5. tool 调用时记录：
   - server
   - tool
   - timeout
   - 结果大小
   - 错误类型
6. 大结果优先持久化，不直接灌上下文
7. 遇到 401 / session expired 时优先走恢复，不要只报 generic error

## 常见失败模式

1. token 过期后一直缓存坏状态，导致所有请求都失败。
2. timeout 复用旧 signal，后续调用瞬间超时。
3. 404 被当成普通网络问题，其实是 session 已失效。
4. discovery 描述太长，把 prompt 撑爆。
5. MCP 大返回直接进入 transcript，导致上下文膨胀。

## OpenClaw 落地建议

1. MCP 输出一旦过大，就落地文件或做引用。
2. 认证错误要给出明确状态，而不是只说工具失败。
3. 会话失效要支持清缓存和重连。
4. 不同 server 的工具说明要控制长度。
5. MCP 元数据要服务于权限判断、UI 提示和上下文压缩。

## 你可以产出的东西

1. 一张 MCP transport / auth / timeout 矩阵
2. 一份 MCP 错误恢复策略表
3. 一份“大结果何时截断、何时持久化”的策略说明
