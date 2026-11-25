---
name: koishi-plugin-dev
description: 开发和维护 Koishi 机器人插件的总入口：按问题分流到指令、中间件/Session、消息元素、数据库、控制台扩展、部署和发布审计等专门 skill，并提供工作区流程与领域能力概览。Cordis 底座使用 cordis-v3-plugin-dev。
---

# Koishi Plugin Dev

这个 skill 用于开发和维护 **Koishi 机器人插件**。它关注 Koishi 在 Cordis 底座之上提供的能力：指令、消息中间件、`Session`、消息元素、数据库服务、控制台扩展、工作区流程和插件市场元信息。

> 边界：`Context`、插件形态、`Service/inject`、生命周期、事件、`Schema`、可逆副作用、热重载、通用测试与审计，统一使用 `cordis-v3-plugin-dev`。数据库 ORM / Query / Selection 使用 `koishi-database-query`。

## 先判断问题属于哪层

| 问题 | 优先 skill |
|---|---|
| 插件形态、`apply(ctx, config)`、`inject`、`dispose`、`fork`、Schema | `cordis-v3-plugin-dev` |
| 指令、参数、选项、权限、帮助 | `koishi-command-dev` |
| 消息流、中间件、`Session`、机器人不响应 | `koishi-middleware-session` |
| 消息元素、JSX、图片、at、平台降级 | `koishi-message-element` |
| 数据库 CRUD、Query、Selection、模型扩展 | `koishi-database-query` |
| 公网部署、server/selfUrl/反代/auth | `koishi-deploy-public` |
| 市场发布、package 元信息 | `koishi-plugin-publish-audit` |

## Koishi 插件常见组成

一个 Koishi 插件通常由 Cordis 底座能力和 Koishi 领域能力组合而成：

```ts
import { Context, Schema } from 'koishi'

export const name = 'example'
export const inject = ['database']

export interface Config {
  prefix: string
}

export const Config: Schema<Config> = Schema.object({
  prefix: Schema.string().default('#').description('触发前缀。'),
})

export function apply(ctx: Context, config: Config) {
  ctx.command('example <text:text>', '示例指令')
    .action(({ session }, text) => {
      return <>
        <at id={session.userId}/>
        {' '}{config.prefix}{text}
      </>
    })

  ctx.middleware((session, next) => {
    if (session.content === 'ping') return 'pong'
    return next()
  })
}
```

这里：

- `Context`、`inject`、`Config`、`Schema`、生命周期属于 Cordis 底座。
- `ctx.command()`、`ctx.middleware()`、`Session`、消息元素、`ctx.database` 属于 Koishi 领域能力或 Koishi 服务。

## 工作区流程

Koishi 插件常在 workspace 中开发。

创建插件：

```sh
npm run setup [name] -- [-c] [-m] [-G]
yarn setup [name] [-c] [-m] [-G]
```

常见布局：

```text
root
├── external
│   └── example
│       ├── src/index.ts
│       ├── client/index.ts
│       ├── tests/index.spec.ts
│       └── package.json
├── koishi.yml
└── package.json
```

添加依赖：

```sh
npm install [...deps] -w koishi-plugin-[name]
yarn workspace koishi-plugin-[name] add [...deps]
```

构建插件：

```sh
npm run build [...name]
yarn build [...name]
```

## 指令能力入口

Koishi 指令用于聊天交互：

```ts
ctx.command('echo <message:text>', '发送消息')
  .option('timeout', '-t <seconds:number> 设置延迟')
  .action(({ session, options }, message) => message)
```

注意：

- 参数、选项、别名、子指令、权限、帮助请使用 `koishi-command-dev`。
- 指令注册是插件副作用，底层可由 Cordis 生命周期回收。
- 指令不触发时同时检查前缀、权限、中间件拦截和 session 状态。

## 中间件与 Session 入口

消息流处理使用中间件：

```ts
ctx.middleware(async (session, next) => {
  if (session.content === 'ping') return 'pong'
  return next()
})
```

注意：

- 异步中间件必须 `return next()` 或 `await next()`。
- 忘记 `next()` 会截断后续指令和中间件。
- `Session` 承载 `content`、`elements`、`send()`、`prompt()`、用户和频道信息。
- 详细排查使用 `koishi-middleware-session`。

## 消息元素入口

跨平台消息优先用标准元素：

```tsx
return <>
  <at id={session.userId}/>
  {' '}你好！
  <img src="https://example.com/a.png"/>
</>
```

详细规则使用 `koishi-message-element`。

## 数据库服务入口

数据库是 Koishi 服务，不是插件默认能力。需要数据库时声明依赖：

```ts
export const inject = ['database']
```

读写和建模使用：

```ts
await ctx.database.get('user', { id })
ctx.model.extend('table', fields, options)
```

详细 CRUD、Query、Selection、Eval、模型扩展和后端兼容性使用 `koishi-database-query`。

## 控制台扩展入口

服务端注册控制台入口：

```ts
export const inject = ['console']

export function apply(ctx: Context) {
  ctx.console.addEntry({ dev, prod })
}
```

或局部依赖：

```ts
ctx.inject(['console'], (ctx) => {
  ctx.console.addEntry({ dev, prod })
})
```

## Koishi 插件 package 元信息

发布到 Koishi 生态时，插件包通常应满足：

- 包名符合：
  - `koishi-plugin-*`
  - `@scope/koishi-plugin-*`
- `version` 使用 semver。
- 不应误设 `private: true`。
- 声明 `peerDependencies.koishi`。
- 提供 `description`、`keywords`、`license`、`repository`、`homepage`。
- `koishi.description` 适合市场展示。
- `koishi.service.required / optional / implements` 与代码一致。

示例：

```json
{
  "name": "koishi-plugin-example",
  "version": "1.0.0",
  "peerDependencies": { "koishi": "^4.15.6" },
  "koishi": {
    "description": { "en": "Example plugin", "zh": "示例插件" },
    "service": {
      "required": ["database"],
      "optional": ["assets"],
      "implements": ["myService"]
    },
    "locales": ["en", "zh"],
    "preview": true,
    "hidden": false
  }
}
```

完整发布审计使用 `koishi-plugin-publish-audit`。

## Koishi 插件开发检查清单

- [ ] Cordis 底座问题已按 `cordis-v3-plugin-dev` 处理。
- [ ] 指令、消息、中间件、数据库、控制台、适配器职责清晰。
- [ ] 数据库、console、assets、server 等服务已通过 `inject` 声明。
- [ ] 指令权限、帮助和参数行为符合预期。
- [ ] 中间件不会误拦截后续处理。
- [ ] 消息元素有平台降级意识。
- [ ] 控制台入口和 DataService 前后端 key 一致。
- [ ] package 元信息适合 Koishi 市场。
- [ ] 插件在 sandbox 或真实平台验证过核心流程。
