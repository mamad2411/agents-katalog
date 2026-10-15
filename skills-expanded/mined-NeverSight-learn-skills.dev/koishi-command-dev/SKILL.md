---
name: koishi-command-dev
description: 为 Koishi 编写、解释和排查指令插件：ctx.command()、参数/选项、别名、子指令、帮助、权限、Session、before/action、文本参数、引号和命令不触发排查。
---

# Koishi 指令开发

这个 skill 用于编写和排查 Koishi 指令系统代码。处理命令问题时，先判断：指令声明是否正确、参数/选项是否匹配、别名/子指令/帮助是否完整、权限是否拦截、`Session` 是否在合适位置使用、文本参数和引号是否导致解析偏差。

## 快速规则

- 用 `ctx.command()` 定义指令。
- `<name>` 表示必选参数，`[name]` 表示可选参数。
- `...` 表示变长参数。
- `:text` 表示贪婪文本参数。
- `.option()` 定义选项。
- `.alias()` 添加别名。
- `.subcommand()` 或 `foo/bar`、`foo.bar` 注册子指令。
- `.usage()` 与 `.example()` 丰富帮助。
- `authority` 控制指令或选项权限。
- `argv.session` 读取当前会话。
- `before()` 做前置检查，`action()` 做实际执行。
- 文本参数会吞掉后续内容，选项尽量写在文本参数前。

## 基本写法

```ts
ctx.command('echo <message:text>', '发送消息')
  .action((argv, message) => message)
```

指令定义通常由三部分组成：

1. 指令名和参数声明。
2. 描述文本。
3. 配置对象，例如 `{ authority: 2, hidden: true }`。

## 参数

### 必选与可选

```ts
ctx.command('test <arg1> [arg2]')
  .action((_, arg1, arg2) => {})
```

必选参数应在可选参数之前。参数不足会触发提示或错误。

### 变长参数

```ts
ctx.command('test <first> [...rest]')
  .action((_, first, ...rest) => {})
```

适合接收不定数量尾部参数。

### 文本参数

```ts
ctx.command('say <message:text>')
  .action((_, message) => message)
```

`text` 是贪婪匹配，会尽量吞掉后续内容。如果后面还有选项，建议把选项放在前面：

```sh
echo -t 300 Hello World
echo "Hello World"
```

### 参数类型

```ts
ctx.command('roll [count:number]')
ctx.command('ban <user:user>')
ctx.command('pick <date:date>')
```

常见类型：`string`、`number`、`integer`、`posint`、`natural`、`bigint`、`text`、`user`、`channel`、`date`、`image`。

## 选项

```ts
ctx.command('test')
  .option('alpha', '-a')
  .option('beta', '-b [value]')
  .option('gamma', '-g <value:number>')
  .action(({ options }) => JSON.stringify(options))
```

选项支持短选项、长选项、布尔开关、参数、默认值、权限和隐藏。

### 默认值

```ts
ctx.command('test')
  .option('timeout', '-t <seconds:number>', { fallback: 60 })
```

### 权限与隐藏

```ts
ctx.command('echo')
  .option('unescape', '-E', { authority: 3 })
  .option('debug', '-d', { hidden: true })
```

### 重载值

```ts
ctx.command('post')
  .option('writer', '-w <id>')
  .option('writer', '--anonymous', { value: 0 })
```

## 别名

```ts
ctx.command('echo <message:text>').alias('say')
```

别名可以预置参数：

```ts
ctx.command('market <area> <item>')
  .alias('市场', { args: ['China'] })
```

注意别名冲突。多个插件注册相同别名可能导致后加载失败或触发对象与预期不一致。

## 子指令

层级式：

```ts
ctx.command('foo/bar')
// 或
ctx.command('foo').subcommand('bar')
```

调用通常是：

```sh
foo bar
```

派生式：

```ts
ctx.command('foo.bar')
// 或
ctx.command('foo').subcommand('.bar')
```

调用通常是：

```sh
foo.bar
```

子指令不会出现在全局帮助中，但会出现在父指令帮助中。适合做管理命令树。

## 帮助信息

帮助通常依赖 `help` 插件。建议给用户命令写描述、usage 和 example：

```ts
ctx.command('echo <message:text>', '输出收到的信息')
  .option('timeout', '-t <seconds:number> 设定延迟发送时间')
  .usage('参数请写在前面，避免被 message 吸收。')
  .example('echo -t 300 Hello World  五分钟后发送 Hello World')
```

隐藏只影响帮助展示，不等于禁用：

```ts
ctx.command('secret', '隐藏指令', { hidden: true })
```

## 权限

指令权限：

```ts
ctx.command('admin', '管理命令', { authority: 3 })
```

选项权限：

```ts
ctx.command('echo')
  .option('unescape', '-E', { authority: 3 })
```

排查权限时检查：指令权限、选项权限、当前用户权限、是否在正确会话类型中调用、是否被控制台/数据库权限体系覆盖。

## Session 与 Argv

`action()` 的第一个参数是 `Argv`，通常包含：

- `args`
- `options`
- `session`
- `next`

```ts
ctx.command('echo <message:text>')
  .action(({ session, options }, message) => {
    return `${session.username}: ${message}`
  })
```

经验：纯参数从形参取；上下文信息从 `argv.session` 取。

## before 与 action

```ts
ctx.command('test')
  .before(({ session }) => {
    // 前置检查
  })
  .action(({ session }) => {
    return 'ok'
  })
```

推荐：`before()` 做校验和准备，`action()` 做业务和返回。

## 命令不触发排查

1. 消息是否满足触发条件：前缀、机器人昵称、at 机器人、私聊直触发。
2. 指令名、别名、子指令路径是否写对。
3. 必选参数是否缺失。
4. 文本参数是否吞掉了选项。
5. 是否需要引号包裹带空格参数。
6. 指令或选项权限是否不足。
7. 帮助里隐藏不代表不能执行。
8. 是否存在别名冲突。
9. 子指令是否挂错父级。
10. 是否被更早的中间件拦截。

## 常用模板

### 简单回显

```ts
ctx.command('echo <message:text>', '发送消息')
  .action((_, message) => message)
```

### 带选项和权限

```ts
ctx.command('echo <message:text>', '发送收到的信息', { authority: 1 })
  .option('timeout', '-t <seconds:number> 设定延迟时间')
  .option('unescape', '-E', { authority: 3 })
  .usage('选项请写在文本参数前。')
  .example('echo -t 300 Hello World')
  .action(({ session, options }, message) => {
    return message
  })
```

### 子指令树

```ts
const user = ctx.command('user', '用户管理')
user.subcommand('authorize <user:user> <level:number>', '设置权限')
user.subcommand('.locale <lang>', '设置语言')
```
