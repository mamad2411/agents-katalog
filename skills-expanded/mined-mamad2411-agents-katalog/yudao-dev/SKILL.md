---
name: yudao-dev
description: ruoyi-vue-pro（yudao/芋道）全栈开发规范与模块知识库。在 yudao 项目里新增/扩展/重构业务模块、设计数据库表与实体类(DO)、生成 CRUD、设计 REST API、或选择工厂/策略/模板方法等设计模式时使用。覆盖 14 个业务模块（system/infra/pay/member/mall/crm/erp/bpm/ai/iot/mp/report/mes/wms/im）的领域模型、数据表、代码规范与扩展指南。
---

# yudao-dev — ruoyi-vue-pro 开发知识库

本 skill 是从 ruoyi-vue-pro（yudao）项目代码中提取的结构化知识库。**不要一次性读取所有文件**——先读本入口，根据用户任务从下方路由表按需加载对应文件，再按其规范执行。

## 何时使用

出现以下任一情况时激活：

- 项目是 ruoyi-vue-pro / yudao / 芋道源码（包名 `cn.iocoder.yudao.*`，模块名 `yudao-module-*`）。
- 任务涉及：新增业务模块、扩展已有模块功能、重构模块、生成 CRUD 代码、设计数据库表 / 实体类(DO) / REST API、多租户(`TenantBaseDO`/`@TenantIgnore`)、RBAC 权限、设计模式选型（工厂/策略/模板方法）。
- 关键词：yudao、芋道、DO 实体、BaseMapperX、CommonResult、ErrorCode、`@PreAuthorize('@ss.hasPermission(...)')`、租户、套餐、字典。

## 知识库结构

| 目录 | 内容 |
|------|------|
| `modules/<module>/skill-<module>.yaml` | 各业务模块的领域模型、数据表设计、分层架构、代码规范、扩展指南（每个 600–960 行） |
| `design/*.yaml` | 跨模块通用设计规范：数据库表 / 实体类 / API / CRUD 代码生成 |
| `patterns/*.yaml` | 设计模式知识：工厂、策略、模板方法（含选择指南与组合） |
| `usage/*.md` | 完整开发流程样例（端到端场景的提示词模板，头部含 `references` 自动引用配置） |
| `templates/` | 知识提取模板与提取提示词 |
| `index.yaml` | 全部模块/设计规范的总索引（状态、优先级、行数） |

## 场景 → 文件路由表

> 路径均**相对于本 skill 目录**（即 SKILL.md 所在目录）。安装后路径不变。usage 文档头部 `references` 里带的 `skills/` 前缀是历史语义路径，加载时请用本表的真实相对路径。

### 1. 业务模块开发（按模块加载对应 skill）

用户指定模块名后，Read 对应文件：

| 模块码 | 文件 | 说明 |
|--------|------|------|
| system | `modules/system/skill-system.yaml` | 用户/角色/权限/部门/租户/字典/短信/邮件/站内信/OAuth2 |
| infra | `modules/infra/skill-infra.yaml` | 基础设施：代码生成、文件、定时任务、API 日志 |
| pay | `modules/pay/skill-pay.yaml` | 支付：渠道、订单、退款 |
| member | `modules/member/skill-member.yaml` | 会员 |
| mall | `modules/mall/skill-mall.yaml` | 商城 |
| crm | `modules/crm/skill-crm.yaml` | CRM |
| erp | `modules/erp/skill-erp.yaml` | ERP |
| bpm | `modules/bpm/skill-bpm.yaml` | 工作流 |
| ai | `modules/ai/skill-ai.yaml` | AI 模块 |
| iot | `modules/iot/skill-iot.yaml` | 物联网 |
| mp | `modules/mp/skill-mp.yaml` | 微信公众号 |
| report | `modules/report/skill-report.yaml` | 报表 |
| mes | `modules/mes/skill-mes.yaml` | 制造执行 |
| wms | `modules/wms/skill-wms.yaml` | 仓储 |
| im | `modules/im/skill-im.yaml` | 即时通讯 |

### 2. 设计规范（跨模块通用）

| 任务 | 文件 |
|------|------|
| 设计数据库表 / 建表 SQL / 字段命名 / 索引 | `design/db-designer.yaml` |
| 生成实体类(DO)：继承体系、注解、命名转换、类型映射 | `design/entity-designer.yaml` |
| 设计 REST API：Controller 注解、请求响应、权限标识 | `design/api-designer.yaml` |
| 根据表结构一键生成完整 CRUD 代码 | `design/crud-designer.yaml` |

### 3. 设计模式

| 任务 | 文件 |
|------|------|
| 选择/应用设计模式、模式组合 | `patterns/index.yaml`（先看选择指南） |
| 工厂模式（如支付/短信渠道客户端创建） | `patterns/factory-pattern.yaml` |
| 策略模式（如算法/支付方式切换） | `patterns/strategy-pattern.yaml` |
| 模板方法模式（如支付下单/短信发送流程骨架） | `patterns/template-method-pattern.yaml` |

### 4. 完整开发流程样例（端到端）

| 场景 | 文件 |
|------|------|
| 快速上手 / 日常定位代码 | `usage/quick-start.md` |
| 新增完整业务模块（从建表到 Controller） | `usage/new-module.md` |
| 实现实体类（含 Mapper/Service/Controller 全链路） | `usage/entity-implementation.md` |
| 扩展已有模块功能 | `usage/extend-module.md` |
| 重构模块 | `usage/refactor-module.md` |
| 设计模式应用实战 | `usage/pattern-usage.md` |
| 全部场景索引 | `usage/index.md` |

## 使用方式

1. **读取本 SKILL.md**，对照「场景 → 文件路由表」定位用户任务对应的文件。
2. 用 Read 加载该文件（通常一个 YAML 或一个 usage .md）。
3. usage 文档头部有 `references` 配置——它声明了该场景还应额外加载哪些 design/patterns 文件，按需一并 Read。
4. 若用户未指定模块，先问清目标模块，再加载 `modules/<module>/skill-<module>.yaml`。
5. 严格按加载到的规范生成/修改代码：命名转换、继承体系（`TenantBaseDO` vs `BaseDO`）、注解、错误码格式、权限标识、分层架构。
6. 多个规范同时适用时，design 规范为全局约束，module skill 为模块具体实现，两者冲突以模块实际代码为准。

## 质量底线（生成代码后自检）

- 实体类以 `DO` 结尾，`@TableName` 含 `autoResultMap = true`，`@EqualsAndHashCode(callSuper = true)`，不重复定义审计字段，不用 Swagger `@Schema`。
- 多租户表继承 `TenantBaseDO`；需忽略租户隔离的表用 `BaseDO` + `@TenantIgnore`。
- Mapper 继承 `BaseMapperX<DO>`；Service 接口与实现分离；Controller 用 `@PreAuthorize('@ss.hasPermission(...)')`。
- 跨模块调用走 API 层，不直接调 Service。
- 错误码遵循 `模块号-子模块号-序号` 格式（如 `1_002_000_000`）。
