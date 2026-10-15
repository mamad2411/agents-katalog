---
name: koishi-schema-builder
description: 为 Koishi 插件补充控制台配置体验、Computed 配置、动态配置和插件导出约定；通用 Schema/Config/schemastery 规则请使用 cordis-v3-plugin-dev。
---

# Koishi Schema Builder

这个 skill 用于处理 **Koishi 插件配置在控制台和会话上下文中的表现**。通用 `Config` / `Schema<Config>` 类型配对、基础类型、默认值、必填、`role()`、`union()`、`intersect()`、`transform()` 等规则，统一参考 `cordis-v3-plugin-dev`。

## 边界

使用 `cordis-v3-plugin-dev` 处理：

- `interface Config` 与 `Schema<Config>` 是否一致。
- `Schema.object()` / `Schema.string()` / `Schema.number()` / `Schema.boolean()` 等基础类型。
- `.description()` / `.default()` / `.required()` / `.role()` 等通用元信息。
- `union`、`intersect`、`transform` 的通用建模。
- Schema 与插件生命周期、审计的关系。

使用本 skill 处理：

- Koishi 控制台表单的用户体验。
- 默认导出类的 namespace 配置挂载。
- `Computed<T>` / `Schema.computed()` 与 `session.resolve()`。
- `Schema.dynamic()` 与 Koishi 运行时动态选项。
- `ctx.schema.set()` 提供动态配置类型。
- Koishi 插件市场用户能否看懂配置。

## Koishi 插件配置心智模型

Koishi 插件配置同时面向三类消费者：

1. **TypeScript 开发者**：通过 `interface Config` 获得类型。
2. **Koishi 运行时**：通过 `Schema<Config>` 校验、填充默认值。
3. **控制台用户**：通过 Schema 元信息看到表单、说明、密钥框、链接框、分组和模式选择。

最小示例：

```ts
import { Context, Schema } from 'koishi'

export interface Config {
  endpoint: string
  token: string
  enabled: boolean
}

export const Config: Schema<Config> = Schema.object({
  endpoint: Schema.string().role('link').required().description('API 地址。'),
  token: Schema.string().role('secret').required().description('访问令牌。'),
  enabled: Schema.boolean().default(true).description('是否启用。'),
})

export function apply(ctx: Context, config: Config) {}
```

## 默认导出类的 Config 挂载

如果插件使用默认导出类，推荐把配置挂到 namespace：

```ts
class Example {
  constructor(ctx: Context, config: Example.Config) {}
}

namespace Example {
  export interface Config {
    foo: string
  }

  export const Config: Schema<Config> = Schema.object({
    foo: Schema.string().required().description('示例字段。'),
  })
}

export default Example
```

这样可以保持类插件导出形态和配置元信息一致。

## 控制台表单体验

配置描述要写给控制台用户，而不是只写给开发者。

建议：

- 所有用户可见字段都写 `.description()`。
- 密钥用 `.role('secret')`。
- URL 用 `.role('link')`。
- 长文本用 `.role('textarea')`。
- 颜色用 `.role('color')`。
- 少量互斥选项用 `.role('radio')`。
- 多选项用 `.role('checkbox')`。
- 复杂数组对象用 `.role('table')`。
- 分组用 `Schema.intersect([...]).description(...)`。
- 多模式配置用 tagged union，并给每个分支写 description。

## Computed 配置

`Schema.computed()` 适合和过滤器或会话上下文相关的值。

```ts
import { Computed, Context, Schema } from 'koishi'

export interface Config {
  reply: Computed<string>
}

export const Config: Schema<Config> = Schema.object({
  reply: Schema.computed(String).description('回复内容。'),
})

export function apply(ctx: Context, config: Config) {
  ctx.command('reply').action(({ session }) => {
    return session.resolve(config.reply)
  })
}
```

规则：

- `Computed<T>` 不应当作普通 `T` 直接使用。
- 在有 `session` 的位置用 `session.resolve(config.xxx)`。
- 适合按平台、频道、用户、过滤器变化的配置。
- 如果配置不依赖上下文，不要过度使用 computed。

## Dynamic 配置

`Schema.dynamic()` 用于引用运行时注册的动态类型。

提供方：

```ts
ctx.schema.set('choices', Schema.union(['foo', 'bar']))
```

使用方：

```ts
Schema.dynamic('choices').description('请选择一个值。')
```

使用原则：

- 只有候选值必须依赖运行时服务或插件生态时才使用。
- 静态枚举优先用 `Schema.union([...])`。
- 动态 key 要稳定，避免插件重载后表单失效。
- 提供方和使用方之间应通过服务依赖或加载顺序保证可用性。

## Koishi 市场视角的配置质量

发布给普通用户前，检查：

- 用户是否知道每个字段该填什么。
- token / secret 是否用密钥输入框。
- endpoint / webhook / selfUrl 是否说明内网和公网差异。
- 默认值是否安全，不会导致误发消息、暴露服务或消耗大量资源。
- 实验配置是否标注 `.experimental()`。
- 废弃配置是否标注 `.deprecated()` 并提供迁移说明。
- 多模式配置是否能从表单中看出差异。
