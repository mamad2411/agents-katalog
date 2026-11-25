---
name: kysely-schema
description: 当用户提供 MySQL DDL、CREATE TABLE 语句、表结构截图或要求补齐 Kysely 数据库类型、DB 接口、Insertable / Updateable 类型、批量插入、批量更新、upsert、query/modify 方法时使用这个 skill。重点是把 DDL 准确转换为本仓库的 Kysely 类型和对应 service 方法，避免 ToGenerated、null/default 判断和 camelCase/snake_case 映射出错。
---

# 数据库表结构到代码生成工作流

这个 skill 用于把 MySQL `CREATE TABLE` 语句转换成本仓库需要的 Kysely 表类型，并在用户需要时继续补齐对应的插入、更新或查询方法。

## 适用场景

当拿到一份 `CREATE TABLE` 语句，需要在本仓库里补齐表结构类型，或者继续补齐对应的插入/更新方法时使用。

如果用户只要求补表类型，完成 `src/types/database.d.ts` 里的 DB 接口、显式 `XxxDB`、`Selectable`、`Insertable`、`Updateable` 后就停，不要顺手新增 service 方法。

如果用户继续要求新增插入、更新、upsert 或查询方法，再进入对应 `*-modify.ts` 或 `*-query.ts`。

## 总流程

```text
读取 DDL
   │
   ▼
识别表名、字段名、类型、NULL、DEFAULT、自增、注释
   │
   ▼
转换成 camelCase 字段和 Kysely 字段类型
   │
   ▼
更新 src/types/database.d.ts 的 DB 接口和 XxxDB 类型
   │
   ├─ 用户只要表类型 ──► 停止
   │
   └─ 用户还要 service 方法
          │
          ▼
     选择对应领域的 *-modify.ts 或 *-query.ts
          │
          ▼
     导入 Insertable / Updateable / Selectable 类型
          │
          ▼
     生成插入、更新、upsert 或查询方法
          │
          ▼
     检查字段映射、JSDoc、import 合并和 SQL 名称
```

## 必守规则

| 规则                 | 正确做法                                         | 常见错误                     |
| -------------------- | ------------------------------------------------ | ---------------------------- | ------------------- |
| 新表 DB shape        | 直接写显式 `XxxDB`                               | 套 `ToGenerated` 偷懒        |
| 默认值字段           | 写 `Generated<type>`                             | 同时写成 `type               | null`               |
| 允许 NULL 且无默认值 | 写 `type                                         | null`                        | 忽略 NULL，写成必填 |
| 自增主键             | 写 `Generated<number>`                           | 写成普通 `number`            |
| 字段命名             | TS 字段用 camelCase，SQL 字段和表名用 snake_case | camelCase 和 snake_case 混用 |
| 类型位置             | 表类型只放 `src/types/database.d.ts`             | 在 service 里临时拼类型      |
| service 位置         | 增删改放 `*-modify.ts`，查询放 `*-query.ts`      | 把变更和查询混到一个入口里   |
| 注释                 | 导出类型、导出函数、class static 方法补 JSDoc    | 生成方法没有 JSDoc           |
| 导入                 | 同一路径的 `import` / `import type` 合并         | 从同一路径拆多条导入         |

## DDL 到 Kysely 类型映射

字段判断优先看 `AUTO_INCREMENT`、`DEFAULT`、`NULL`，不要只根据 MySQL 类型猜 TS 类型。

| DDL 特征                          | Kysely 字段类型                      | 说明                              |
| --------------------------------- | ------------------------------------ | --------------------------------- | --------------------- |
| `AUTO_INCREMENT` 主键             | `Generated<number>`                  | 自增字段由数据库生成              |
| 任意 `DEFAULT ...` 字段           | `Generated<type>`                    | 有默认值就不再标 `                | null`                 |
| `NOT NULL` 且无默认值             | `type`                               | 调用方插入时必须传                |
| `NULL` 且无默认值                 | `type                                | null`                             | 只有这种情况才标 null |
| `datetime` / `timestamp` 有默认值 | `Generated<Date>` 或项目既有时间类型 | 跟随 `database.d.ts` 里同类表写法 |
| `decimal` / `numeric`             | `string`                             | 保留小数精度，不直接写 number     |
| `tinyint` / `int` / `bigint`      | 跟随项目同类字段                     | 业务状态码不要顺手新建魔法数字    |
| `varchar` / `text`                | `string`                             | 注释可写字段业务含义              |
| `json`                            | 跟随项目既有 JSON 字段类型           | 不用 `any` 或 `unknown` 糊过去    |

## 第一步 添加表类型到 DB 接口

在 `src/types/database.d.ts` 的 `DB` 类型接口中添加新表，并把它放到对应业务分组的末尾。

```typescript
export type DB = {
  // monitor
  m_monitor_evaluation: MonitorEvaluationDB;
  m_monitor_evaluation_list: MonitorEvaluationListDB;
  m_monitor_evaluation_dimension: MonitorEvaluationDimensionDB;
};
```

## 第二步 创建表结构类型

表结构类型直接写成显式 Kysely 风格，不要再包 `ToGenerated`。字段判断按上面的映射表处理。

一个完整示例如下。

```typescript
/**
 * m_monitor_evaluation_list 课堂评价明细
 */
export type MonitorEvaluationListDB = {
  id: Generated<number>;
  monitorId: number; // 三率主记录ID
  dimensionId: number; // 维度ID
  score: string; // 课堂评价分数
  avgScore: string | null; // 平均分数
  type: Generated<number>; // 0 接口获取 1自己算
};
export type MonitorEvaluationList = Selectable<MonitorEvaluationListDB>;
export type InsertMonitorEvaluationListDB = Insertable<MonitorEvaluationListDB>;
export type UpdateMonitorEvaluationListDB = Updateable<MonitorEvaluationListDB>;
```

如果当前任务只要求补类型，到这里就可以停，不需要硬补 `modify` 方法。

## 第三步 选择 service 落点

需要补 service 方法时，先按职责选择文件，不要把查询和变更混在一起。

| 需求                                 | 文件位置                       | 方法倾向                                                          |
| ------------------------------------ | ------------------------------ | ----------------------------------------------------------------- |
| 批量插入、插入更新、按 id 更新、删除 | 对应领域的 `*-modify.ts`       | `dbInsert<Table>`、`dbUpdate<Table>ByIds`、`dbDelete<Table>ByIds` |
| 列表、详情、聚合、统计、条件查询     | 对应领域的 `*-query.ts`        | `dbGet<Table>...`、`dbList<Table>...`                             |
| 多步骤复杂业务编排                   | 对应领域 `logic/`              | 只有流程足够复杂才拆 class                                        |
| 只是一层很薄的透传                   | 留在 controller 或现有 service | 不要为了形式新增薄 logic                                          |

## 第四步 在 modify 文件里导入新类型

在对应的 `src/service/**/modify.ts` 文件里，导入这个表对应的新增类型。同一路径的 type import 要合并成一条。

```typescript
import type { InsertMonitorEvaluationListDB, UpdateMonitorEvaluationListDB } from "#types/database.d.ts";
```

## 第五步 创建插入或更新方法

方法放在对应业务类里，写法跟现有项目保持一致。

字段映射要同时检查 `updateField`、`values`、MySQL `VALUES(...)` 和 PostgreSQL 兼容分支 `EXCLUDED...`。字段名在 TS 对象里用 camelCase，raw SQL 字符串里用真实 snake_case。

```typescript
/**
 * 插入或更新课堂评价明细
 */
static async dbInsertMonitorEvaluationLists<T extends InsertMonitorEvaluationListDB>(
  params: DBInsertParams<T>,
) {
  const { dataList, tx = db } = params;
  if (isFalsy(dataList)) return [];

  const first = dataList[0];
  const updateField = {
    id: isValidValue(first.id),
    monitorId: isValidValue(first.monitorId),
    dimensionId: isValidValue(first.dimensionId),
    score: isValidValue(first.score),
    avgScore: isValidValue(first.avgScore),
    type: isValidValue(first.type),
  };

  const values = dataList.map((item) => ({
    id: item.id,
    monitorId: item.monitorId,
    dimensionId: item.dimensionId,
    score: item.score,
    avgScore: item.avgScore,
    type: item.type,
  }));

  const result = await DBUtil.upsert(
    tx.insertInto("m_monitor_evaluation_list").values(values),
    {
      id: updateField.id ? sql<number>`VALUES(id)` : undefined,
      monitorId: updateField.monitorId ? sql<number>`VALUES(monitor_id)` : undefined,
      dimensionId: updateField.dimensionId ? sql<number>`VALUES(dimension_id)` : undefined,
      score: updateField.score ? sql<string>`VALUES(score)` : undefined,
      avgScore: updateField.avgScore ? sql<string | null>`VALUES(avg_score)` : undefined,
      type: updateField.type ? sql<number>`VALUES(type)` : undefined,
    },
    {
      id: updateField.id ? sql.ref<number>("EXCLUDED.id") : undefined,
      monitorId: updateField.monitorId ? sql.ref<number>("EXCLUDED.monitor_id") : undefined,
      dimensionId: updateField.dimensionId ? sql.ref<number>("EXCLUDED.dimension_id") : undefined,
      score: updateField.score ? sql.ref<string>("EXCLUDED.score") : undefined,
      avgScore: updateField.avgScore ? sql.ref<string | null>("EXCLUDED.avg_score") : undefined,
      type: updateField.type ? sql.ref<number>("EXCLUDED.type") : undefined,
    },
  )
    .$call(debugSQL(false))
    .executeTakeFirst();

  return DBUtil.setInsertId(dataList, Number(result.insertId));
}
```

## 字段映射检查表

| 检查点                                     | 要看什么                                           |
| ------------------------------------------ | -------------------------------------------------- | -------------------------------------- |
| DB 接口                                    | 新表名是否放到合适分组，表名是否保持 snake_case    |
| `XxxDB`                                    | 每个 DDL 字段是否都存在，camelCase 是否正确        |
| `Generated<>`                              | 自增字段和 default 字段是否都被覆盖                |
| `                                          | null`                                              | 是否只出现在允许 NULL 且无默认值的字段 |
| `Selectable` / `Insertable` / `Updateable` | 三个导出类型是否齐全                               |
| `updateField`                              | 是否覆盖所有允许 upsert 更新的字段                 |
| `values`                                   | 是否没有漏字段，没有把 snake_case 写进 TS 对象 key |
| `VALUES(...)`                              | raw SQL 字段是否使用真实 snake_case                |
| `EXCLUDED...`                              | 字段名是否和真实 SQL 字段一致                      |
| JSDoc                                      | 导出函数或 static 方法是否解释业务用途             |

## 常见错误

| 错误                                         | 修正                                             |
| -------------------------------------------- | ------------------------------------------------ | ---------------------- |
| 新表直接套 `ToGenerated`                     | 改成显式 `XxxDB`                                 |
| DDL 有 `default`，字段类型还写成 `           | null`                                            | 改成 `Generated<type>` |
| `updateField`、`values`、`upsert` 参数漏字段 | 对照 DDL 和字段映射检查表补齐                    |
| camelCase 和 snake_case 混着写               | TS 字段用 camelCase，SQL 字符串用 snake_case     |
| 导出函数和 `static` 方法没写 JSDoc           | 在定义上方补简短 JSDoc                           |
| 为了状态码顺手新增 enum                      | 先判断是否跨文件复用；单点简单语义不要过度枚举化 |
| 用 `any`、`unknown` 或断言绕类型             | 补准确类型或跟随既有 JSON 字段写法               |

## 验证清单

| 项目             | 通过标准                                        |
| ---------------- | ----------------------------------------------- | ----- |
| DB 接口          | 已经加了新表类型                                |
| 表结构类型       | 使用显式 `XxxDB` 写法                           |
| 导出类型         | 已导出 `Selectable`、`Insertable`、`Updateable` |
| 默认值           | 有默认值的字段已经用了 `Generated<>`            |
| null             | `default` 字段没有误标 `                        | null` |
| service 类型导入 | 对应文件已导入新类型，且 import 已合并          |
| 插入或更新方法   | 字段映射完整，raw SQL 字段名正确                |
| 命名             | TS camelCase / SQL snake_case 约定一致          |
| 注释             | JSDoc 已补齐                                    |
