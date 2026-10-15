---
name: cordis-v3-plugin-dev
description: Cordis v3 and Koishi plugin development guide for Context, Plugin, Service/inject, lifecycle events, Schema, revertible effects, hot reload safety, and audits.
---

# Cordis: Meta-Framework of Spatiotemporal Composability

Use this skill to develop, explain, debug, and audit Cordis plugins. It covers the core Cordis runtime model: `Context`, plugin forms, services and dependency injection, lifecycle events, the event system, configuration schemas, revertible effects, hot reload safety, and maintainability audits.

## Mental Model

Cordis is a meta-framework for spatiotemporal composability. A plugin receives a `Context`, registers effects through that context, declares required services with `inject`, and relies on Cordis to revert context-managed effects when the plugin is unloaded or reloaded.

Core concepts:

| Concept | Meaning |
|---|---|
| `Context` | The plugin runtime scope, service access point, effect collector, and scope derivation API. |
| `Plugin` | A composable runtime unit: function, class, or object with `apply()`. |
| `Service` | A named capability or resource shared through the context. |
| `inject` | A dependency declaration that controls when plugin logic may run. |
| Lifecycle | Plugin initialization, teardown, and reusable-instance behavior such as `dispose` and `fork`. |
| Revertible effect | A registered side effect that can be reverted when its owning scope is disposed. |
| `Schema` | Configuration declaration, validation, default values, and metadata via schemastery. |

## Plugin Forms

A Cordis plugin can be written as a function, a class, or an object with an `apply()` method.

### Function Plugin

```ts
export function apply(ctx: Context, config: Config) {
  // register effects here
}
```

### Class Plugin

```ts
export default class Example {
  constructor(ctx: Context, config: Example.Config) {
    // register effects here
  }
}
```

### Object Plugin

```ts
export default {
  name: 'example',
  apply(ctx: Context, config: Config) {
    // register effects here
  },
}
```

Guidelines:

- Keep the export shape stable unless changing it is the purpose of the task.
- Give function plugins an explicit exported `name` when the runtime-visible plugin name should differ from the function identifier; write that `name` in kebab-case.
- Give object plugins an explicit `name`, and write it in kebab-case.
- Class names can be used as plugin names.
- Register effects through the current `ctx` whenever possible.

## Recommended Skeleton

```ts
import { Context, Schema } from 'cordis'

export const name = 'example'

export interface Config {
  endpoint: string
  timeout: number
}

export const Config: Schema<Config> = Schema.object({
  endpoint: Schema.string().role('link').required().description('Service endpoint.'),
  timeout: Schema.number().default(60).description('Timeout in seconds.'),
})

export const inject = {
  optional: ['http'],
}

export async function apply(ctx: Context, config: Config) {
  // async initialization can happen directly in apply

  ctx.inject(['http'], (ctx) => {
    // service-dependent effects should use this callback ctx
  })

  ctx.on('dispose', () => {
    // cleanup resources not managed by Cordis APIs
  })
}
```

## Context

`Context` is the plugin's runtime environment. It is responsible for:

- Accessing services.
- Registering effects.
- Loading nested plugins.
- Creating derived scopes.
- Binding registered effects to the current plugin scope.

Common API patterns:

```ts
await initialize()
ctx.on('dispose', callback)
ctx.plugin(otherPlugin, config)
ctx.inject(['service'], callback)
```

Rules:

- In `ctx.inject()` callbacks, use the callback `ctx` for effects that depend on the injected service.
- In `fork` callbacks, use the callback `ctx` for per-instance effects.
- Do not store `ctx` in long-lived globals or singletons.
- Do not let external objects keep using `ctx` after the plugin scope is disposed.

## Services and inject

Services are the core of Cordis spatial composability. Plugins should coordinate through declared service dependencies rather than implicit load order.

### Required Dependencies

```ts
export const inject = ['server']
```

A plugin with required dependencies waits until those services are available. If a required service disappears or changes, dependent plugin scopes may be rolled back or reloaded.

### Optional Dependencies

```ts
export const inject = {
  optional: ['assets'],
}
```

Use optional dependencies for enhancements. Do not mark a service optional if the plugin cannot perform its intended role without it.

### Local Dependencies

When only part of a plugin needs a service, isolate that part with `ctx.inject()`:

```ts
ctx.inject(['console'], (ctx) => {
  ctx.console.addEntry({ dev, prod })
})
```

Rules:

- Service-dependent effects belong inside the `ctx.inject()` callback.
- Use the callback `ctx`, not the outer `ctx`, for those effects.
- Avoid top-level service probing as the main dependency mechanism.

### Custom Services

Define a service when a plugin provides an API to other plugins.

```ts
import { Context, Service } from 'cordis'

class MyService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'myService', true)
  }

  start() {}
  stop() {}
  fork() {}
}

declare module 'cordis' {
  interface Context {
    myService: MyService
  }
}

export function apply(ctx: Context) {
  new MyService(ctx)
}
```

Service design checklist:

- The service name is stable and semantic.
- The public API does not leak unnecessary implementation details.
- Resources owned by the service are released with the owning plugin scope.
- Consumers declare the service dependency with `inject`.
- Type augmentation matches runtime registration.

## Lifecycle

### Initialization

For asynchronous initialization in a normal plugin, make `apply` async and await the setup work directly.

```ts
export async function apply(ctx: Context) {
  await loadCache()
}
```

Use service lifecycle methods for resources owned by a service class, with a matching teardown path.

### `dispose`

Use `dispose` to release resources that are not automatically managed by Cordis.

```ts
const watcher = createWatcher()

ctx.on('dispose', () => {
  watcher.close()
})
```

Manually clean up:

- External HTTP servers.
- Timers created outside context-managed timer APIs.
- File watchers.
- External event emitter listeners.
- Network connections.
- Child processes.
- Global listeners.

### `fork` and Reusable Plugins

Reusable plugins need a clear boundary between one-time registration and per-instance state.

```ts
export const reusable = true

export function apply(ctx: Context) {
  let count = 0

  ctx.on('fork', (ctx) => {
    count += 1
    ctx.on('dispose', () => count -= 1)
  })
}
```

Rules:

- Put shared one-time registration outside `fork`.
- Put per-instance state and effects inside `fork`.
- Use the callback `ctx` for per-instance effects.
- Do not mark a plugin as reusable without designing instance isolation.

## Event System

Cordis events provide a general publish / subscribe mechanism.

```ts
const dispose = ctx.on('event', callback)
dispose()

ctx.once('custom-event', callback)
ctx.before('some-event', callback)
```

Triggering APIs:

| API | Semantics |
|---|---|
| `ctx.emit()` | Synchronously notify listeners. |
| `ctx.parallel()` | Run async listeners concurrently. |
| `ctx.bail()` | Run listeners in order and stop at the first meaningful return value. |
| `ctx.serial()` | Async serial variant of bail-style dispatch. |

Selection guide:

- Use `emit` for simple notifications.
- Use `parallel` when all async side effects should run.
- Use `bail` when the first meaningful result wins.
- Use `serial` when order and async completion both matter.

## Configuration Schema

Cordis uses schemastery to describe plugin configuration. A reliable configuration keeps TypeScript types, runtime validation, defaults, and metadata aligned.

```ts
export interface Config {
  endpoint: string
  token: string
  cache: boolean
}

export const Config: Schema<Config> = Schema.object({
  endpoint: Schema.string().role('link').required().description('API endpoint.'),
  token: Schema.string().role('secret').required().description('Access token.'),
  cache: Schema.boolean().default(true).description('Enable cache.'),
})
```

### Basic Types

- `Schema.any()`
- `Schema.never()`
- `Schema.const(value)`
- `Schema.string()`
- `Schema.number()`
- `Schema.boolean()`
- `Schema.is(Date)` / `Schema.is(RegExp)`
- `Schema.array(inner)`
- `Schema.dict(inner)`
- `Schema.tuple([...])`
- `Schema.object({...})`
- `Schema.union([...])`
- `Schema.intersect([...])`
- `Schema.transform(inner, fn)`

### Metadata

- `.description(text)`: explain the field to the configuration user.
- `.default(value)`: declare a default value.
- `.required()`: require the field to be present.
- `.role()`: control form appearance.
- `.hidden()`: hide from the form while still validating.
- `.disabled()`: show as disabled while still validating.
- `.deprecated()`: mark deprecated configuration.
- `.experimental()`: mark experimental configuration.

Common roles:

```ts
Schema.string().role('secret')
Schema.string().role('link')
Schema.string().role('textarea')
Schema.string().role('color')
Schema.number().role('slider')
Schema.union(['a', 'b']).role('radio')
Schema.array(Schema.union(['a', 'b'])).role('checkbox')
```

### Grouping and Modes

Use `intersect` for grouped configuration:

```ts
export const Config = Schema.intersect([
  Schema.object({ enabled: Schema.boolean().default(true) }).description('Basic'),
  Schema.object({ timeout: Schema.number().default(60) }).description('Advanced'),
])
```

Use tagged unions for mutually exclusive modes:

```ts
Schema.union([
  Schema.object({
    type: Schema.const('http').required(),
    endpoint: Schema.string().role('link').required(),
  }).description('HTTP mode'),
  Schema.object({
    type: Schema.const('local').required(),
    path: Schema.string().required(),
  }).description('Local mode'),
])
```

Schema checklist:

- `interface Config` and `Schema<Config>` match.
- Defaults are centralized in the schema.
- Do not combine `.default()` and `.required()` for the same field.
- `.required()` does not mean a string is non-empty; add an explicit constraint if needed.
- `.role()` is not validation logic.
- Hidden or disabled fields still need valid values.
- Union branches have clear descriptions.
- Tagged union defaults match branch constants.
- `transform()` is used for compatibility or normalization, not for hiding obvious errors.

## Revertible Effects

Cordis plugins should follow the rule: every effect added by a plugin must have a way to be removed with that plugin's scope.

A revertible API usually:

- Registers a side effect.
- Returns a disposer or records the disposer on the current context.
- Runs the disposer when the owning scope is disposed.

Example:

```ts
const dispose = ctx.on('event', callback)
dispose()
```

External resources need explicit disposal:

```ts
const timer = setInterval(tick, 1000)
ctx.on('dispose', () => clearInterval(timer))
```

## Hot Reload Debugging

Symptoms and likely causes:

| Symptom | Check first |
|---|---|
| Duplicate handling after reload | Duplicate listeners, commands, middleware, or external subscriptions. |
| Background work continues after unload | Timers, watchers, sockets, servers, or child processes missing `dispose`. |
| Dependent scopes repeatedly restart | Incorrect `inject`, unstable service provider, or wrong service name. |
| Local service feature runs too early | Effects registered outside the `ctx.inject()` callback. |
| Reusable instances affect each other | Missing isolation in `fork` state. |

Debugging order:

1. Confirm that the plugin scope actually unloads and reloads.
2. Identify all external resource creation sites.
3. Match each creation site with a `dispose` path.
4. Check `ctx.inject()` and `fork` callbacks for outer-context leaks.
5. Start and stop the plugin repeatedly and observe whether effects grow.

## Audit Checklist

### Plugin Structure

- Export shape is intentional and stable.
- `name` is clear.
- Configuration type and schema are aligned.
- The plugin body primarily registers effects instead of doing uncontrolled work.

### Service Dependencies

- Required services are declared with `inject`.
- Optional services are declared as optional.
- Local dependencies use `ctx.inject()`.
- Consumers do not replace dependency lifecycle with ad-hoc probing.
- Custom service type augmentation matches runtime registration.

### Lifecycle and Reversibility

- External resources have a `dispose` path.
- Dynamic registration has a disposer.
- Reloads do not duplicate effects.
- `fork` and `inject` callbacks use their own `ctx`.
- External objects do not keep using disposed contexts.

### Schema

- TypeScript types and schema output match.
- Defaults are centralized in the schema.
- User-visible fields have useful descriptions.
- Roles match field semantics.
- Hidden and disabled fields still validate.
- Complex unions and intersections are readable.

### Resources

- Persistent data is not written into package directories.
- Absolute paths are not hardcoded unnecessarily.
- Temporary files have cleanup behavior.
- External processes, sockets, and watchers have lifecycle management.
