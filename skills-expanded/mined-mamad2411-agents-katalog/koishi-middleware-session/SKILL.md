---
name: koishi-middleware-session
description: 设计和排查 Koishi 消息中间件、Session、消息流、优先级、临时中间件以及机器人不响应问题；通用事件和生命周期请使用 cordis-v3-plugin-dev。
---

# Koishi 中间件与 Session

这个 skill 用于 Koishi 消息处理与机器人响应排查。它聚焦 **Koishi 的 message pipeline、middleware、Session、指令与中间件关系、机器人不响应**。

> 边界：`ctx.on()` / `ctx.once()` / `ctx.emit()` / `ctx.parallel()` / 服务就绪阶段 / `dispose` / `fork` 等通用 Cordis 事件和生命周期机制，请使用 `cordis-v3-plugin-dev`。本 skill 只保留 Koishi 消息流语境中的事件排查入口。

## 一句话心智模型

- **中间件**是专门面向 `message` 的处理流水线，适合过滤、鉴权、拦截、短路、兜底回复。
- **Session** 是一次消息或平台事件的上下文对象，承载 `content`、`elements`、`send()`、`prompt()`、用户、频道和 bot 信息。
- **指令**运行在 Koishi 消息处理流程中；多数“命令没反应”问题要同时看指令、中间件、权限和会话状态。
- **事件**是更底层的发布 / 订阅机制；通用事件 API 归入 `cordis-v3-plugin-dev`。

## 中间件和事件的区别

| 维度 | 中间件 | 事件 |
|---|---|---|
| 适用范围 | 消息流 | 任意事件 |
| 注册方式 | `ctx.middleware()` | `ctx.on()` / `ctx.once()` / `ctx.before()` |
| 控制流 | 通过 `next()` 决定是否继续 | 监听发生了什么 |
| 回复方式 | 可以直接返回回复内容 | 通常手动 `session.send()` |
| 常见用途 | 过滤、鉴权、复读、兜底 | 生命周期、自定义事件、平台通知 |

如果需要“继续 / 停止”这种链式控制，用中间件。如果只是观察某件事发生，用事件。

## 消息流

一条消息大致会经历：

1. 平台适配器产生 message 事件。
2. Koishi 把消息封装成 `Session`。
3. 内置逻辑处理前缀、昵称、at、用户 / 频道数据、指令解析等。
4. 前置中间件和普通中间件按顺序执行。
5. 指令和后续处理在消息流中运行。

关键理解：指令不是绕开中间件，而是消息处理流程中的一部分。前面中间件误拦截，会导致命令不触发。

## 普通中间件

```ts
ctx.middleware((session, next) => {
  if (session.content === '天王盖地虎') {
    return '宝塔镇河妖'
  }
  return next()
})
```

规则：

- 返回字符串会作为回复。
- 调用 `next()` 才会交给后续中间件和指令。
- 忘记 `next()` 会截断后续处理。
- 未命中分支应该明确 `return next()`。

## 异步中间件

```ts
ctx.middleware(async (session, next) => {
  await session.observeUser(['authority'])
  if (session.user.authority === 0) return '权限不足。'
  return next()
})
```

异步中间件里调用 `next()` 必须 `return next()` 或 `await next()`。

## 前置中间件

```ts
ctx.middleware((session, next) => {
  if (session.content === '高优先级命中') return '先处理我'
  return next()
}, true)
```

前置中间件比普通中间件更早执行，适合：

- 全局统计。
- 高优先级拦截。
- 早期过滤。
- 安全检查。

风险：前置中间件很容易抢走消息，导致指令和普通中间件不执行。除非明确需要，否则不要把大量业务逻辑放到前置中间件。

## 临时中间件

临时中间件用于当前链路中的兜底处理：

```ts
ctx.middleware((session, next) => {
  if (session.content === 'hlep') {
    return next('你想说的是 help 吗？')
  }
  return next()
})
```

适合：

- “如果后面没人处理，就回复这个”的低优先级建议。
- 拼写纠错。
- 兜底帮助。

## Session 常用能力

常用属性：

- `session.content`：消息文本。
- `session.elements`：消息元素数组。
- `session.bot`：当前机器人。
- `session.event`：原始事件。
- `session.platform`：平台。
- `session.guildId` / `session.channelId` / `session.userId`：会话定位信息。
- `session.user` / `session.channel`：数据库观察对象，通常只能在中间件或指令中可靠使用。

常用方法：

- `session.send(message)`

## 用户和频道数据

访问 `session.user` / `session.channel` 前，通常需要观察字段：

```ts
ctx.middleware(async (session, next) => {
  await session.observeUser(['authority'])
  if (session.user.authority < 2) return '权限不足。'
  return next()
})
```

检查：

- 是否在中间件或指令中访问。
- 是否 observe 了需要字段。
- 是否需要数据库服务支持。
- 群聊和私聊是否都有对应 channel 数据。

## 指令与中间件关系

命令不触发时，除 `koishi-command-dev` 中的指令声明问题外，还要检查消息流：

- 是否有更早中间件没有 `next()`。
- 是否有前置中间件抢走消息。
- 是否有 `session.prompt()` 接管输入。
- 是否有权限中间件提前返回。
- 是否被平台、频道、用户过滤器排除。
- 是否 bot 没收到消息。

## 机器人不响应排查

按顺序查：

1. `ctx.on('message')` 是否能看到消息。看不到说明问题在适配器、平台连接或机器人状态。
2. 是否有中间件分支忘记 `return next()`。
3. 异步中间件是否忘记 `await/return next()`。
4. 是否被前置中间件或更早注册的中间件拦截。
5. 是否有 `session.prompt()` 接管了下一条输入。
6. 指令前缀、昵称、at、权限是否满足。
7. `session.user` / `session.channel` 是否在正确位置访问。
8. 机器人登录状态是否正常。
9. 平台权限、intents、群聊 / 私聊限制是否满足。
