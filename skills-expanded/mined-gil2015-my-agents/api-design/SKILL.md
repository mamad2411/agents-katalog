---
name: api-design
description: 当需要从前端接口文档或独立需求出发，设计后端 API 契约（包含 DTO、VO、业务逻辑、权限和校验规则）时使用
---

# API 设计

## 概述

从前端产物（`apiDoc/api.md`、前端模块 `defs/service.ts`、`defs/type.ts`）或独立后端需求出发，设计并确认后端 API 契约，产出后端可直接消费的 `api-design.md`。

**核心原则：** 前端契约是起点，后端设计是补全。前端定义了"调什么"，后端补全"怎么做"。

## 适用场景

**必须使用：**

- 前端已完成接口定义，需要设计后端实现
- 后端需要独立设计 API（无前端契约输入）
- 需要补充前端看不到的后端视角：校验规则、权限控制、业务逻辑、数据库关联
- 接口契约已变化，需要重新对齐前后端

**例外情况（需征询开发者）：**

- 只是修改已有接口的内部实现，不涉及契约变化
- 纯后端内部接口，不对外暴露
- 接口文档缺少关键信息，无法确定方法、路径或响应结构

## 铁律

```text
FRONTEND CONTRACT IS THE STARTING POINT - BACKEND DESIGN COMPLETES IT
```

硬约束：

- 前端已定义的接口路径和响应结构，默认沿用，除非有明确的后端限制
- 如果后端需要调整前端已定义的契约，必须在 `api-design.md` 中标记 `NEEDS_ADJUST` 并说明原因
- 每个接口必须明确 DTO 类名、VO 类名和校验规则
- 不在 Controller 里临场发明参数校验和响应结构

## 违反后果

如果 `api-design.md` 不存在、DTO 校验规则缺失，或与前端契约有未标记的不一致，当前 API 设计视为未完成；`db-design` 和 `module-dev` 不应启动。

## 执行流程

### 第 1 步：LOAD - 读取接口来源与上下文

优先按以下顺序获取接口信息：

**从前端 mission 产物读取（推荐）：**

- `.ai/missions/{missionId}/apiDoc/api.md` — 前端视角的接口定义
- `"{projectRoot}/{moduleRoot}/{module.name}/defs/service.ts"` — 实际调用的路径和参数
- `"{projectRoot}/{moduleRoot}/{module.name}/defs/type.ts"` — 请求/响应类型定义

**从配置中读取：**

- `.ai/missions/{missionId}/config.json` 中的 `projectRoot`、`moduleRoot`、`module.name`
- `.ai/missions/{missionId}/config.json` 中的 `apiDesignSources`

**从独立来源读取：**

- 用户指定的接口文档目录或文件
- 前端模块路径不符合默认约定时，由 `apiDesignSources` 提供的精确文件路径
- 用户直接粘贴的接口说明

同时读取：

- `{projectRoot}/.ai/docs/backend-context.md` — 确认响应封装、异常处理、验证管道等项目约定
- `.ai/missions/{missionId}/reqDocs/req.md` — 业务需求和验收标准
- `.ai/missions/{missionId}/apiDesign/api-design.md` — 如存在，增量更新

必须先确认：

- 本轮是首次设计，还是在已有 `api-design.md` 上增量更新
- 前端是否已有接口定义，有则以其为基准
- 后端模块名是否已写入 `config.json.backend.moduleName`
- 如果要读取前端 `defs`，是否能根据 `projectRoot + moduleRoot + module.name` 定位到真实文件；若不能，必须改读 `apiDesignSources` 或用户明确给出的路径

定位规则：

- 默认先按 `projectRoot/moduleRoot/module.name/defs/` 定位前端 `defs`
- 默认路径不存在时，不全量扫描前端目录；改为读取 `apiDesignSources` 或向用户要精确路径
- `api.md` 与 `defs` 冲突时，在 `api-design.md` 中标记 `NEEDS_ADJUST`

**至少执行：**

- `test -f ".ai/missions/{missionId}/config.json"`
- `test -f ".ai/missions/{missionId}/apiDoc/api.md" || true`
- `test -f "{projectRoot}/{moduleRoot}/{module.name}/defs/service.ts" || true`
- `test -f "{projectRoot}/{moduleRoot}/{module.name}/defs/type.ts" || true`

### 第 2 步：ALIGN - 对齐前端契约

如果存在前端 `api.md`：

- 逐个接口对齐：方法、路径、请求参数、响应结构
- 标记前端对齐状态：
  - `ALIGNED`：后端可直接按前端定义实现
  - `NEEDS_ADJUST`：后端需要调整，附说明
  - `BACKEND_ONLY`：后端独有接口，前端未定义

如果不存在前端契约：

- 从需求文档或用户输入出发，按标准 RESTful 约定设计接口
- 全部标记为 `BACKEND_ONLY`

### 第 3 步：DESIGN - 补充后端视角信息

针对每个接口，至少补充以下后端视角信息：

| 维度       | 内容                                       |
| ---------- | ------------------------------------------ |
| Controller | 类名、方法名、路由装饰器                   |
| DTO        | 类名、字段列表、class-validator 校验装饰器 |
| VO         | 类名、响应字段、Entity → VO 转换规则       |
| 业务逻辑   | 查询条件、排序规则、分页策略、数据过滤     |
| 权限控制   | 需要哪些 Guard、角色/权限要求              |
| 数据校验   | 字段格式、范围、长度、必填性、联合校验     |
| 错误码     | 后端业务错误码、前端处理策略               |
| 关联实体   | 用到哪些数据库表/实体、关系类型            |

### 第 4 步：VERIFY - 校验设计完整性

逐接口检查：

| 检查项     | 关注点                                       |
| ---------- | -------------------------------------------- |
| 路径一致性 | 是否与前端 `service.ts` 中的路径一致         |
| 参数覆盖   | 前端发送的所有参数是否都有对应 DTO 字段      |
| 响应覆盖   | 前端消费的所有字段是否都在 VO 中定义         |
| 校验完整   | 每个 DTO 字段是否都有 class-validator 装饰器 |
| 错误码覆盖 | 前端 `api.md` 中提到的错误码是否都有后端定义 |
| 权限明确   | 每个接口是否都明确了鉴权要求                 |

### 第 5 步：OUTPUT - 写入 API 设计文档

将结果写入 `.ai/missions/{missionId}/apiDesign/api-design.md`，格式以 `../../references/doc-templates/api-design-doc-template.md` 为准。

同时维护 `config.json`：

- 只增量更新 `backend.moduleName`
- 不覆盖其他配置字段

## 速查表

| 阶段   | 关键活动                  | 完成标准                     |
| ------ | ------------------------- | ---------------------------- |
| LOAD   | 读取前端契约和项目上下文  | 接口来源明确，上下文足够     |
| ALIGN  | 对齐前端接口定义          | 每个接口都有前端对齐状态     |
| DESIGN | 补充 DTO/VO/业务逻辑/权限 | 后端视角信息完整             |
| VERIFY | 校验设计完整性            | 前后端契约一致，校验规则完整 |
| OUTPUT | 写入 `api-design.md`      | 下游 step 可直接消费         |

## 常见借口

| 借口                             | 现实                                             |
| -------------------------------- | ------------------------------------------------ |
| "前端的 api.md 直接用就行"       | 前端只定义了调用契约，校验、权限、业务逻辑还要补 |
| "DTO 校验后面写代码时再加"       | 没有预先设计的校验规则，代码时一定会漏           |
| "先把接口路径定了，字段后面再补" | 字段不明确的设计文档对 step3 没有价值            |

## 危险信号 - 立即停下来

- 你没有读前端 `api.md` 就开始设计接口
- 你修改了前端已定义的路径但没标记 `NEEDS_ADJUST`
- 你的 DTO 字段没有 class-validator 校验装饰器说明
- 你把前端 `type.ts` 中的展示字段（如 `statusLabel`）写进了后端 VO

## 参考文档

| 主题             | 文件                                                        |
| ---------------- | ----------------------------------------------------------- |
| 通用规则         | `../../references/rules/common-rules.md`                    |
| API 设计文档模板 | `../../references/doc-templates/api-design-doc-template.md` |
| NestJS 代码规则  | `../../references/rules/nestjs-code-rules.md`               |

## 集成关系

- **可选上游：** 前端 `api-integrate` 的 `apiDoc/api.md`
- **可选上游：** `project-context-build` 的 `backend-context.md`
- **直接下游：** `db-design`、`module-dev`
