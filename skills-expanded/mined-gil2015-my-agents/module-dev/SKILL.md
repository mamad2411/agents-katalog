---
name: module-dev
description: 当需要按标准 NestJS 模块结构开发业务模块（Controller、Service、DTO、Entity、VO）时使用
---

# 模块开发

## 概述

根据 API 设计和数据库设计文档，在 NestJS 项目中按标准模块模板开发业务模块，输出必须可运行并通过基础测试。

**核心原则：** 先对齐模板和职责边界，再写具体实现。结构错了，后面的测试和 Bug 修复都会变慢。

## 适用场景

**必须使用：**

- 新建 NestJS 业务模块
- 在现有模块上新增一组完整功能
- 根据 `api-design.md` 和 `db-schema.md` 实现后端接口
- 独立后端需求但仍需落到标准模块结构

**例外情况（需征询开发者）：**

- 一次性 PoC 或演示，不会进入正式模块体系
- 明确要求保留旧模块结构，本次不做模板迁移
- 仅修改已有接口的内部逻辑，不涉及结构变更

## 铁律

```text
EVERY MODULE STARTS FROM THE SHARED TEMPLATE - LAYERING FIRST, LOGIC SECOND
```

Controller 里混入数据库操作、Service 里直接操作 Request，就不是"先把接口写出来"，而是在制造后续测试和维护成本。

硬约束：

- Controller 只做路由转发和参数接收，不写业务逻辑
- Service 是业务逻辑的唯一入口
- Service 返回 VO 而不是 Entity
- DTO 必须使用 class-validator 装饰器
- Entity 不包含业务逻辑
- 优先沿用 `../../references/module-template/` 的分层方式

## 违反后果

如果模块分层、DTO 校验或 Entity 映射不符合模板，当前实现视为未完成；继续缺陷修复或最终测试前必须先补齐结构。

## 第 1 步：读取上下文

读取以下信息：

- `.ai/missions/{missionId}/config.json`，确认 `projectRoot`、`backend.moduleName`、`backend.orm`、`backend.moduleRoot`
- `.ai/missions/{missionId}/apiDesign/api-design.md`
- `.ai/missions/{missionId}/dbDesign/db-schema.md`
- `{projectRoot}/.ai/docs/backend-context.md`（如存在）
- 已有的模块代码（如是扩展现有模块）

必须先搞清楚：

- 本次是新建模块，还是在现有模块内扩展
- 真实目标模块目录名是什么
- 项目使用的 ORM 和数据库类型
- 项目是否有统一的响应封装、异常处理、分页工具
- 是否有 Entity 基类可以继承
- 如果 `backend.moduleRoot` 未填写，本轮是否按默认值 `src/modules` 处理

**至少执行：**

- `test -f ".ai/missions/{missionId}/config.json"`
- `test -f ".ai/missions/{missionId}/apiDesign/api-design.md" || true`
- `test -f ".ai/missions/{missionId}/dbDesign/db-schema.md" || true`

## 第 2 步：搭建骨架（仅新建模块时）

以以下基线为准：

- `../../references/module-template/`
- `../../references/rules/nestjs-code-rules.md`

目标结构至少包含：

```text
{projectRoot}/{backend.moduleRoot}/{module-name}/
├── {module-name}.module.ts
├── {module-name}.controller.ts
├── {module-name}.service.ts
├── dto/
│   ├── create-{module-name}.dto.ts
│   ├── update-{module-name}.dto.ts
│   └── query-{module-name}.dto.ts
├── entities/
│   └── {module-name}.entity.ts
├── vo/
│   └── {module-name}.vo.ts
├── constants/
│   └── index.ts
└── __test__/
    ├── {module-name}.controller.spec.ts
    └── {module-name}.service.spec.ts
```

说明：

- 已有模块扩展时，不重建目录；在现有结构上补缺文件
- 模板里的占位代码可以作为起点，但交付前必须替换或删除

**至少执行：**

- `find "{projectRoot}/{backend.moduleRoot}/{module-name}" -maxdepth 3 -type f | sort`

## 第 3 步：先定义契约（Entity → DTO → VO → Constants）

先写数据层和契约层，再写实现。顺序固定：

1. **Entity**：按 `db-schema.md` 定义实体，使用 ORM 装饰器
2. **DTO**：按 `api-design.md` 定义请求参数，添加 class-validator 装饰器
3. **VO**：按 `api-design.md` 定义响应结构，实现 `fromEntity()` 静态方法
4. **Constants**：定义模块常量、枚举和错误码

约束：

- Entity 字段名和类型必须与 `db-schema.md` 一致
- DTO 字段必须与 `api-design.md` 的请求参数一致
- VO 字段必须与 `api-design.md` 的响应结构一致
- 不用 `any` 占位

## 第 4 步：实现 Service 层

Service 是业务逻辑的唯一入口。至少完成：

1. 注入 Repository
2. 按 `api-design.md` 的业务逻辑规则实现每个方法
3. 实现 Entity → VO 转换
4. 处理业务异常和错误码
5. 实现事务管理（如跨表操作）

约束：

- Service 方法签名与 `api-design.md` 的接口一一对应
- 返回 VO 而非 Entity
- 使用项目统一的业务异常类
- 分页查询使用项目统一的分页工具（如有）

## 第 5 步：实现 Controller 层

Controller 只做路由转发。至少完成：

1. 使用装饰器声明路由、方法和 Swagger 注解
2. 使用 `@Body()`、`@Param()`、`@Query()` 接收参数
3. 调用 Service 方法并返回结果
4. 添加权限守卫（如 API 设计中要求）

约束：

- 不在 Controller 中写业务逻辑
- 不手动包装响应格式
- 路由路径和方法必须与 `api-design.md` 一致

## 第 6 步：注册 Module

1. 在模块文件中注册 Controller、Service、Entity
2. 在 `app.module.ts` 或对应的父模块中导入新模块
3. 确认依赖注入链路完整

## 第 7 步：收尾校验

逐项检查：

- [ ] 模块结构与 `../../references/module-template/` 对齐
- [ ] Controller 只做路由转发和参数接收
- [ ] Service 是业务逻辑的唯一入口
- [ ] DTO 都使用了 class-validator 装饰器
- [ ] Service 返回 VO 而非 Entity
- [ ] Entity 字段与 `db-schema.md` 一致
- [ ] 路由路径和方法与 `api-design.md` 一致
- [ ] 模块已在上级模块中注册
- [ ] 无 `any` 类型残留
- [ ] 无模板占位符残留
- [ ] 已使用项目统一的响应封装和异常处理

**至少执行：**

- `rg -n "__MODULE_NAME__|__TABLE_NAME__|__MODULE_CODE__" "{projectRoot}/{backend.moduleRoot}/{module-name}"`
- `rg -n "Injectable|Controller|Entity|IsString|IsInt" "{projectRoot}/{backend.moduleRoot}/{module-name}"`
- `find "{projectRoot}/{backend.moduleRoot}/{module-name}" -maxdepth 3 -type f | sort`

## 速查表

| 阶段            | 关键动作                      | 完成标准                      |
| --------------- | ----------------------------- | ----------------------------- |
| 读取上下文      | 确认 ORM、数据库和模块边界    | 输入信息足够落地              |
| 搭建骨架        | 对齐共享模板结构              | 文件树和命名符合模板基线      |
| 定义契约        | Entity → DTO → VO → Constants | 数据层和契约层完整            |
| 实现 Service    | 业务逻辑编排                  | 每个接口对应一个 Service 方法 |
| 实现 Controller | 路由转发                      | Controller 不含业务逻辑       |
| 注册 Module     | 模块依赖注入                  | 模块能被正确加载              |
| 收尾校验        | 结构和分层检查                | 无模板残留和分层违规          |

## 常见借口

| 借口                              | 现实                                         |
| --------------------------------- | -------------------------------------------- |
| "Controller 里加一个小逻辑没关系" | 放到 Service，Controller 不要偷带逻辑        |
| "先返回 Entity，后面再转 VO"      | 后面通常不会转，而且 Entity 暴露了数据库结构 |
| "DTO 校验太烦了，先跳过"          | 没有校验的接口等于对任意输入敞开大门         |

## 危险信号 - 立即停下来

- 你在 Controller 中直接调用 Repository
- 你的 Service 方法直接返回 Entity
- 你的 DTO 没有 class-validator 装饰器
- 你保留了模板占位符

## 参考文档

| 主题            | 文件                                          |
| --------------- | --------------------------------------------- |
| 通用规则        | `../../references/rules/common-rules.md`      |
| 共享模块模板    | `../../references/module-template/`           |
| NestJS 代码规则 | `../../references/rules/nestjs-code-rules.md` |

## 集成关系

- **直接上游：** `api-design`、`db-design`
- **可选上游：** `project-context-build`
- **主测试阶段：** `module-test`
- **失败回流：** `bug-fix`
