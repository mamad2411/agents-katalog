---
name: project-context-build
description: 当需要从 NestJS 项目代码中提取架构上下文（ORM、管道、鉴权、响应封装、公共服务等），供后续后端开发 step 复用时使用
---

# 项目上下文构建

## 概述

从 NestJS 项目代码、开发者补充信息和配置文件中提炼 `backend-context.md`，供后续 `api-design`、`db-design`、`module-dev` 直接复用项目既有的技术选型和约定。

**核心原则：** 优先沉淀已验证的架构事实，不发明一套不存在的架构体系。

## 适用场景

**必须使用：**

- 后端开发经常猜不准项目的 ORM 用法、异常处理或响应封装方式
- 新项目刚开始，需要先把架构规范录入给 AI
- 需要确认项目的认证鉴权、配置管理、日志体系等技术选型
- 希望先沉淀一份全项目共用的架构基线，再让多个需求任务复用

**例外情况（需征询开发者）：**

- 一次性演示或 PoC，不会沉淀为正式项目资产
- 项目已经存在可用且最新的 `backend-context.md`，本轮也没有新增架构约束

## 铁律

```text
PREFER VERIFIED ARCHITECTURE SOURCES - NEVER INVENT A TECH STACK
```

没有证据支持的结论，只能标记为 `inferred` 或 `open_question`。

## 产物

- 项目级基线：`{projectRoot}/.ai/docs/backend-context.md`
- 所有需求任务共用同一份项目级架构基线
- 不在 mission 目录下重复维护架构文档
- 各 step 读取顺序固定为项目级基线

## 核心提取维度

| 维度     | 具体内容                                                      |
| -------- | ------------------------------------------------------------- |
| 技术栈   | NestJS 版本、TypeScript 版本、Node.js 版本约束                |
| ORM      | TypeORM / Prisma / Sequelize；版本、配置方式、Entity 基类     |
| 数据库   | 类型（PostgreSQL / MySQL / SQLite）、连接配置方式、多数据源   |
| 模块组织 | feature module vs shared module、全局模块注册方式             |
| 请求管道 | Guard → Interceptor → Pipe → Controller → Service 链路        |
| 认证鉴权 | JWT / Session / OAuth；守卫实现、装饰器使用方式               |
| 异常处理 | 全局异常过滤器、业务错误码体系、HttpException 子类            |
| 响应封装 | 统一响应格式、拦截器实现、是否自动包装                        |
| 配置管理 | ConfigModule、环境变量、配置文件约定                          |
| 日志体系 | Logger 选型、日志格式、日志级别                               |
| 公共服务 | 已封装的通用 services（分页、文件上传、缓存、Redis 等）       |
| 事务管理 | 事务封装方式（装饰器 / QueryRunner / DataSource.transaction） |
| 验证管道 | ValidationPipe 配置、class-validator 选项                     |

## 执行流程

### 第 1 步：LOAD - 读取项目上下文来源

优先读取以下信息：

- `projectRoot`：当前项目根目录
- 可选 `.ai/missions/{missionId}/config.json`：辅助获取 `projectRoot`、`backend.moduleRoot`
- 现有项目级 `backend-context.md`
- 开发者补充的架构说明
- 目标项目中的关键配置文件和入口代码

必须先确认：

- 本轮是否需要更新项目级架构基线
- 项目是否已经有稳定的架构约定，还是仍处于早期阶段
- 是否存在历史文档；如果存在，必须增量更新而不是整份重写
- 后端源码主目录是什么；若 mission 已配置 `backend.moduleRoot`，优先按 `projectRoot/backend.moduleRoot` 扫描，否则按 `projectRoot/src` 兜底

**至少执行：**

- `test -d "{projectRoot}"`
- `test -f "{projectRoot}/package.json"`
- `test -f "{projectRoot}/.ai/docs/backend-context.md" || true`

**关键文件扫描：**

- `cat "{projectRoot}/package.json"` — 依赖和版本
- `find "{projectRoot}/{backend.moduleRoot}" -name "*.module.ts" -maxdepth 4 | sort`
- `rg -n "TypeOrmModule|PrismaModule|SequelizeModule" "{projectRoot}/{backend.moduleRoot}"`
- `rg -n "APP_GUARD|APP_INTERCEPTOR|APP_FILTER|APP_PIPE" "{projectRoot}/{backend.moduleRoot}"`
- `rg -n "ConfigModule|ConfigService" "{projectRoot}/{backend.moduleRoot}"`
- `rg -n "JwtModule|PassportModule|AuthGuard" "{projectRoot}/{backend.moduleRoot}"`

若未提供 `backend.moduleRoot`，以上命令中的 `{backend.moduleRoot}` 默认按 `src` 处理。

### 第 2 步：DETECT - 识别技术选型和架构模式

重点识别以下事实：

- ORM 类型和配置入口
- 数据库类型和连接方式
- 全局管道注册（Guard、Interceptor、Filter、Pipe）
- 认证鉴权方案和装饰器
- 响应封装拦截器的实现
- 异常过滤器和错误码体系
- 公共模块和共享服务

规则：

- 只记录真实运行链路上的架构实现，不把废弃代码当现行规范
- 如果项目同时存在多种方案，优先记录 `app.module.ts` 全局注册的那条链路
- 无法确认时，保留为 `open_question`

### 第 3 步：EXTRACT - 提炼 AI 可执行的架构约束

`backend-context.md` 至少需要覆盖：

- 技术栈版本和核心依赖
- ORM 使用方式：Entity 基类、Repository 注入模式、迁移工具
- 请求处理管道：全局注册的 Guard / Interceptor / Pipe / Filter 及其职责
- 认证鉴权：守卫实现、装饰器、token 验证链路
- 响应封装：统一响应格式、拦截器类名和转换逻辑
- 异常处理：业务异常类、错误码定义方式、全局异常过滤器
- 配置管理：环境变量加载方式、配置命名空间
- 公共服务：分页、文件上传、缓存、定时任务等已封装能力
- 命名约定：模块名、文件名、类名、表名、字段名
- 禁止事项：明确列出架构约束中"不允许做"的事

### 第 4 步：MERGE - 合并多来源信息并标注证据

每条架构结论都要标注证据等级：

- `code_verified`：来自当前项目已生效代码
- `doc_verified`：来自明确的架构文档或开发者填写文档
- `user_provided`：来自当前轮用户/开发者口述
- `inferred`：基于有限证据推断得出

冲突处理规则：

- 默认以 `code_verified` 优先
- 多个来源冲突且无法判断时，保留冲突说明与 `open_question`

### 第 5 步：PREVIEW - 先展示拟覆盖内容

若目标文档不存在，可直接进入 `OUTPUT`。

若目标文档已存在，不得直接覆盖。必须先展示：

- 即将写入的目标路径
- 主要新增 / 删除 / 替换点
- 关键内容预览

**硬约束：**

- 未获用户明确同意前，不写任何文件

### 第 6 步：OUTPUT - 写入架构上下文文档

生成或更新 `{projectRoot}/.ai/docs/backend-context.md`。

写入要求：

- 顶部必须写清技术栈版本、ORM 类型和文档状态
- 每条关键规则都要能追溯到代码或用户输入
- 已有条目优先增量更新
- 若架构信息仍不充分，输出"已确认事实 + 未确认问题"

## 速查表

| 阶段    | 关键动作                       | 完成标准                                 |
| ------- | ------------------------------ | ---------------------------------------- |
| LOAD    | 读取项目根目录和关键配置文件   | 明确本轮产物范围与可用来源               |
| DETECT  | 识别 ORM、管道、鉴权等技术选型 | 能说明每个关键能力从哪里定义、在哪里生效 |
| EXTRACT | 提炼架构约束                   | 各 step 可直接复用，不必二次猜测         |
| MERGE   | 按证据等级合并冲突信息         | 所有推断项都被显式标注                   |
| PREVIEW | 展示拟覆盖内容                 | 用户能在写入前审阅主要改动               |
| OUTPUT  | 增量更新 `backend-context.md`  | 产物可被后续 step 直接消费               |

## 常见借口

| 借口                               | 现实                                         |
| ---------------------------------- | -------------------------------------------- |
| "先写一套完整的架构规范"           | 一旦写成文档，后续 skill 会把它当真          |
| "全局管道太多了，随便挑一个"       | 先确认真实注册链路，不然会把废弃实现继续传播 |
| "旧文档我先直接改了再说"           | `.ai` 不在 git 里，覆盖前必须先征得同意      |

## 危险信号 - 立即停下来

- 你把 `node_modules` 里的框架默认行为当成项目自定义实现
- 你发现项目有多个 ORM 配置，却没核实哪个真的在运行
- 你在未获同意前就准备覆写 `.ai/docs/` 下的现有文档

## 参考文档

| 主题     | 文件                                     |
| -------- | ---------------------------------------- |
| 通用规则 | `../../references/rules/common-rules.md` |

## 集成关系

- **主消费方：** `step1-api-design`、`step2-db-design`、`step3-module-dev`
- **可选触发者：** 开发者手动调用
- **非阻塞说明：** 缺少 `backend-context.md` 不阻塞后续 step，但必须显式说明上下文缺口
