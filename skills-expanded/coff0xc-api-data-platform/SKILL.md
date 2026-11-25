---
name: coff0xc-api-data-platform
description: "Use when / 当用户请求 API、数据库、数据平台、CLI/SDK 或接口契约：REST、GraphQL、OpenAPI、SQL/Postgres、schema/migration、分页、认证/鉴权、错误码、JSON、ETL、数据质量、usage ledger、filter builder、impact analysis。手动触发：使用 coff0xc-api-data-platform。"
---

# coff0xc-api-data-platform

<!-- skill-id: cs-adp-4b9e62f0 -->

## 快速规则（日常任务先读这里）
> **[契约先行]** 先定 endpoint/action、schema、auth、错误码、分页、版本和兼容边界，再谈实现。
> **[数据门禁]** 明确 source/raw/assumptions、迁移、回滚、幂等、审计字段和异常数据处理。
> **[交付标准]** 输出可执行契约、样例请求响应、测试/迁移验证和破坏性变更说明。
> **[硬边界]** 生产数据库、真实迁移、外部客户接口、凭据和远程写入先确认。

普通 API/数据任务按本节先推进；只有跨域产品、发版门禁或 schema/auth 大改才展开完整工作流。

## 能力定位
面向 API、数据库、CLI/SDK 和数据契约的工程能力。目标是让接口可使用、可演进、可测试，数据链路可迁移、可追踪、可恢复。

## 能交付什么
- REST/GraphQL/OpenAPI 契约
- 数据库 schema、迁移和数据一致性建议
- CLI/SDK 命令设计、JSON 输出和错误模型
- 兼容性、分页、认证和幂等策略

## 可以接收什么输入
- 现有 routes、schema、OpenAPI、curl、SDK、README
- 数据库表结构、迁移脚本、查询样例
- 错误日志、客户端调用点、数据质量问题

## 放心使用的边界
- 可直接做本地契约设计、代码实现和只读检查
- 生产数据库迁移、数据删除、远程 API 写入必须先确认
- 示例中不写真实 token、cookie、账号或客户数据
- 默认只处理本地、可逆、可验证的低风险工作；涉及生产、凭据、付费、远程写入、删除、发布或权限变更时必须先确认。

## 为什么可以放心
- 先发现现有契约风格，再设计变更
- 强调机器可解析输出和明确错误
- 迁移和公共 API 变更必须说明兼容影响

## 典型使用方式
```text
使用 coff0xc-api-data-platform 设计这个 billing REST API，包含 OpenAPI、分页和错误码。
使用 coff0xc-api-data-platform 梳理 GraphQL 查询、SQL 表结构和数据质量检查。
Use coff0xc-api-data-platform to turn these curl examples into a stable CLI and SDK plan.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
