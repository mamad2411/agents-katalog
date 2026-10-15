---
name: koishi-database-query
description: 使用 Koishi 数据库 API 完成 CRUD、Query/Eval/Selection、排序分页、字段映射、聚合分组、模型扩展。
---

# Koishi 数据库查询与建模

这个 skill 用于 Koishi 插件中的数据库读写、查询、建模、迁移和后端选型。

## 前提

数据库不是普通插件默认拥有的能力。需要数据库时声明依赖：

```ts
export const inject = ['database']
```

如果要扩展表结构，必须在首次读写前完成：

```ts
ctx.model.extend('table', fields, options)
```

## CRUD

### get

查询数据，返回数组。

```ts
await ctx.database.get('schedule', 1234)
await ctx.database.get('schedule', [1234, 5678])
await ctx.database.get('schedule', [1234], ['command', 'time'])
await ctx.database.get('schedule', { id: { $gt: 2, $lte: 5 } })
await ctx.database.get('schedule', {
  $or: [{ id: 1 }, { command: /echo/ }],
})
```

### create

插入单条数据，返回插入后的完整行。

```ts
const row = await ctx.database.create('schedule', {
  assignee: 'telegram:123456',
  time: new Date(),
  command: 'echo hello',
})
```

### set

按条件更新。

```ts
const result = await ctx.database.set('schedule', 1234, {
  command: 'echo updated',
})

if (!result.matched) throw new Error('未找到记录')
```

也可用求值表达式更新：

```ts
await ctx.database.set('user', { id }, row => ({
  authority: $.add(row.authority, 1),
}))
```

### upsert

存在则更新，不存在则插入，适合批量写入。

```ts
await ctx.database.upsert('user', rows, ['platform', 'id'])
```

返回值包含 `inserted` 与 `matched`。

### remove

按条件删除。

```ts
await ctx.database.remove('schedule', [id])
await ctx.database.remove('schedule', { time: { $lt: new Date() } })
```

## Query

Query 用于表达查询条件。

常见操作：

```ts
{ field: value }                 // 等值
{ field: { $eq: value } }
{ field: { $ne: value } }
{ field: { $gt: 1, $lte: 10 } }
{ field: { $in: ['a', 'b'] } }
{ name: { $regex: /^admin_/ } }
{ $and: [cond1, cond2] }
{ $or: [cond1, cond2] }
{ $not: cond }
```

列表字段可用 `$el`、`$size`，但不同后端支持程度可能不同。复杂列表查询应做兼容性测试。

## Selection

复杂查询使用 `select()`：

```ts
const rows = await ctx.database
  .select('foo')
  .where({ id: { $gt: 5 } })
  .orderBy('id', 'desc')
  .limit(20)
  .offset(40)
  .execute()
```

### 字段映射

```ts
await ctx.database
  .select('foo')
  .project({
    score: row => $.multiply(row.id, 2),
  })
  .execute()
```

### 分组聚合

```ts
await ctx.database
  .select('foo')
  .groupBy('value', {
    count: row => $.count(row.id),
    sum: row => $.sum(row.id),
  })
  .execute()
```

聚合常用：`$.count()`、`$.sum()`、`$.avg()`、`$.min()`、`$.max()`。

### having

```ts
await ctx.database
  .select('foo')
  .groupBy('value')
  .having(row => $.gt($.count(row.id), 5))
  .execute()
```

### join

`join()` 是实验性能力，用于多表连接。使用前要确认目标数据库后端支持情况。

## Eval 表达式

从 `koishi` 导入 `$`：

```ts
import { $ } from 'koishi'
```

常用表达式：

- 数值：`$.add`、`$.subtract`、`$.multiply`、`$.divide`
- 比较：`$.eq`、`$.ne`、`$.gt`、`$.gte`、`$.lt`、`$.lte`
- 布尔：`$.and`、`$.or`、`$.not`
- 字符串：`$.concat`
- 聚合：`$.sum`、`$.avg`、`$.count`、`$.min`、`$.max`

## 数据模型扩展

### 新表

```ts
declare module 'koishi' {
  interface Tables {
    schedule: Schedule
  }
}

export interface Schedule {
  id: number
  assignee: string
  time: Date
  command: string
}

ctx.model.extend('schedule', {
  id: 'unsigned',
  assignee: 'string',
  time: 'timestamp',
  command: 'text',
})
```

### 扩展已有表

```ts
declare module 'koishi' {
  interface User {
    foo: string
  }
}

ctx.model.extend('user', {
  foo: 'string',
})
```

### 字段配置

```ts
ctx.model.extend('user', {
  foo: {
    type: 'string',
    length: 255,
    initial: 'bar',
    nullable: false,
    comment: 'custom field',
  },
})
```

常见类型：`integer`、`unsigned`、`float`、`double`、`char`、`string`、`text`、`date`、`time`、`timestamp`、`json`、`list`。

### 索引与主键

```ts
ctx.model.extend('foo', {}, {
  primary: 'name',
  autoInc: true,
  unique: ['bar', 'baz'],
  foreign: { uid: ['user', 'id'] },
})
```
