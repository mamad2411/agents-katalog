---
name: java-modular-monolith
description: >-
  Guides scaffolding and daily coding of a Java Spring Boot modular monolith:
  Maven BOM, framework starters, server shell, api/biz modules, three API channels,
  Controller/Service/Mapper layering, specific ErrorCode per failure, logging, and
  config governance. Use when creating a new backend, adding a module or API,
  reviewing architecture, copying conventions to another project, or when the user
  mentions 单体架构、模块化单体、搭建框架、工程规范、代码规范.
---

# Java 模块化单体规范（通用）

规定 **怎么搭框架、怎么写代码**，不绑定具体业务域。占位符见下表，先读仓库绑定再替换。

| 任务 | 先读 |
|------|------|
| 从零搭工程 / 迁框架 | [scaffolding.md](scaffolding.md) |
| 新模块 / 新 CRUD / 日常编码 | [coding.md](coding.md) |
| 日志、配置、开放对接、框架类型 | [reference.md](reference.md) |
| 自检 / Review | [checklist.md](checklist.md) |
| 复制到其它仓库 | [adapt.md](adapt.md) |

当前仓库若有「项目绑定」Skill（如 `*-architecture-standards`），**先读其占位表**，再套用本文。

---

## 1. 何时启用

- 新建 Spring Boot 后端、拆模块、加 Starter、加开放通道
- 新管理端 / C 端 / 外部接口，或 Code Review 分层与错误码
- 把本规范迁到另一个工程
- 用户提到：单体架构、模块化单体、搭建框架、工程规范、api/biz

不用于：纯业务字段含义、前端 Vue、具体表设计讨论（除非同时改后端分层）。

---

## 2. 占位符

| 占位 | 含义 | 示例 |
|------|------|------|
| `{app}` | 工程前缀（Maven artifact / YAML 根） | `acme` |
| `{base}` | Java 根包 | `co.example.acme` |
| `{domain}` | 业务域 | `order` |
| `{resource}` | 资源（URL 与类名） | `store-order` / `StoreOrder` |
| `{admin-prefix}` | 管理端 URL 前缀 | `/admin-api` |
| `{app-prefix}` | C 端 URL 前缀 | `/app-api` |

复制到新工程时只改这些值，目录形态不变。

---

## 3. 架构决策（必须遵守）

**形态**：一个 JVM、一个可执行 JAR。`{app}-server` 聚合各 `*-biz`；横切能力进 `{app}-framework`。

```text
{app}-server          启动壳：依赖 *-biz + application*.yaml
     │
     ├─ {app}-module-{domain}-biz     实现
     │        └── 依赖 → {app}-module-{domain}-api   契约
     ├─ {app}-framework               Starter 平台
     └─ {app}-dependencies            BOM
```

| 决策 | 意图 | 禁止 |
|------|------|------|
| 模块化单体 | 运维简单、本地事务 | 把模块当微服务乱加 RPC |
| api / biz 分离 | 跨模块只依赖契约 | biz 依赖另一模块的 biz |
| Starter 平台化 | 横切可复制 | 业务代码进 framework |
| 包路径驱动 URL | 约定优于配置 | Controller 手写 `{admin-prefix}` |
| 配置跟域走 | 启动类保持空 | 启动类堆 `@EnableConfigurationProperties` |

**一句话**：Server 是容器，Framework 是平台，Module 是插件。

---

## 4. 设计原则

| 原则 | 说明 |
|------|------|
| 契约与实现分离 | 跨模块只暴露 `*-api`（ErrorCode、enum、DTO） |
| 单向依赖 | Controller → Service → Mapper |
| 框架与业务解耦 | 通用进 framework，业务进 `module-*` |
| 接口分通道 | 管理端 / C 端 / 外部对接，鉴权隔离 |
| 统一契约 | `CommonResult`、ErrorCode、VO 命名一致 |
| 具体错误具体消息 | 每种失败独立 ErrorCode；禁止运行时拼 msg |

---

## 5. 按任务执行

**从零搭框架 / 裁剪复制框架** → [scaffolding.md](scaffolding.md)

1. 定占位符与技术栈  
2. 建 BOM → framework 最小集 → server 空壳  
3. 第一个 `module-{domain}`（api + biz）跑通一条管理端 CRUD  
4. 需要再加 security / redis / job；开放通道按 7 步加  

**新业务模块** → [scaffolding.md](scaffolding.md)「新模块」+ [coding.md](coding.md)

1. 父 POM 声明 `{app}-module-{domain}`（其下 api + biz）  
2. api：ErrorCode 段 + enum  
3. biz：dal → convert → service → controller  
4. **只改 server 的 pom 引入 `*-biz`**，不改启动类业务逻辑  

**新管理端 / C 端接口** → [coding.md](coding.md) → [checklist.md](checklist.md)

**新开放接口** → [reference.md](reference.md)「外部对接 7 步」

**Review / PR** → [checklist.md](checklist.md)

**迁到其它工程** → [adapt.md](adapt.md)

---

## 6. 工程与模块（摘要）

```text
{root}/
├── {app}-dependencies/
├── {app}-framework/
│   ├── {app}-common/
│   └── {app}-spring-boot-starter-{web|security|mybatis|...}/
├── {app}-server/
└── {app}-module-{domain}/
    ├── {app}-module-{domain}-api/
    └── {app}-module-{domain}-biz/
```

**基线栈**：Java 17 · Spring Boot 3.x · Maven · MyBatis-Plus · MapStruct · Redis · Spring Security

**api 只放**：ErrorCode、enums、跨模块 DTO（无 Controller / 无 Spring Web）  
**biz 只放**：Controller、ServiceImpl、DO、Mapper、Convert、域内 Filter / Configuration

跨 **2+ 模块** 才抽 `XxxApi` + `XxxApiImpl`；同 JVM 不必 RPC 化。

---

## 7. 三通道（安全架构）

| 通道 | 包 | URL | 鉴权 |
|------|-----|-----|------|
| 管理端 | `controller.admin.*` | `/{domain}/{resource}` | Token + `@PreAuthorize` |
| C 端 | `controller.app.*` | 模块约定 | 用户 Token |
| 外部 | `controller.{开放名}` | `/external/{系统}` | **独立 Filter**，不走管理端 Bearer |

- 管理端由框架按包名加 `{admin-prefix}`；Controller **只写资源路径**
- 管理端 REST：`POST /create` · `PUT /update` · `DELETE /delete` · `GET /get` · `GET /page` · `GET /export-excel`
- 外部鉴权算法可不同（JWT / HMAC），**目录结构必须统一**

---

## 8. 分层（摘要）

| 层 | 做 | 禁止 |
|----|----|------|
| Controller | `@Valid`、权限、调 Service、`return success(data)` | 事务、Mapper、吞异常、手写 `{admin-prefix}` |
| VO | Create / Update / Page / Resp / Excel + BaseVO | 业务字段乱塞 BaseVO |
| Service | 规则、事务、编排、返回 RespVO | 返回 DO、`return CommonResult.error` |
| Convert | MapStruct 字段映射 | 业务 if |
| DAL | `BaseDO` + `BaseMapperX` + `xxxIfPresent` | 手写 null 拼条件 |

注入用 `@Resource`。Service：`@Slf4j` `@Service` `@Validated`。

---

## 9. 统一响应与错误码（强制）

```json
{ "code": 0, "data": {}, "msg": "" }
```

- 成功：`code === 0`；HTTP 多为 200，以 body 为准
- ErrorCode 定义在 `*-api`；Service **只** `throw exception(ERROR_CODE)` 或 `invalidParamException`
- 禁止 `RuntimeException` 表达业务错误；禁止 `exception0` / 私有 `authFailed(String)` 运行时拼 msg
- **一场景一常量**：缺参、格式错、不存在、时间窗……各自 msg；仅签名/token 不匹配允许笼统「签名验证失败」
- Filter / 全局异常透传 `ServiceException` 的 code + message，不得改回笼统文案

完整条文与模板见 [coding.md](coding.md) § 错误码、[reference.md](reference.md) § 错误码。

---

## 10. 配置与日志（摘要）

| 层级 | 职责 |
|------|------|
| 启动类 | 只 `@SpringBootApplication` + 扫描 `{base}.server` / `{base}.module` |
| 域内 `*Configuration` | `@EnableConfigurationProperties` + 本域 Bean |
| `*Properties` | 绑定 YAML，无业务逻辑 |

日志五层（应用 / 访问 DB / 错误 DB / 操作 DB / 集成审计）见 [reference.md](reference.md)。要点：

- Service 禁止空 catch；禁止 log 明文 password / secret / sign / token
- 访问日志 DB **默认只覆盖管理端前缀**；`/external/**` 必须有域内审计表
- 前缀：`[{domain}] {动作} key={}`

---

## 11. 推荐默认

| 项 | 默认 |
|----|------|
| 新表删除 | `@TableLogic`；历史业务删除字段触达再统一 |
| 跨模块调用 | 2+ 模块才抽 Api 接口 |
| 开放接口 | 每个 `/external/{系统}` 必有 Filter + 审计表 |
| 生产访问日志 | 管理端 enable |
| HTTP 失败 | 对内 200 + body.code；网关可映射 4xx |
| 旧代码 | 触达再改，不一次性重构 |

---

## 12. 反例

| ❌ | ✅ |
|----|-----|
| Controller → Mapper | Controller → Service → Mapper |
| 启动类堆 EnableConfigurationProperties | 域内 Configuration |
| external 复用 admin Token | 独立 Filter |
| 以为 external 会进访问日志 DB | 仅管理端前缀；外部走审计表 |
| 空 catch / log 打 secret | warn + 脱敏 |
| Controller 写 `{admin-prefix}/...` | 只写 `/{domain}/{resource}` |
| `exception0` / 私有 helper 拼 msg | api 定义 ErrorCode + `throw exception(...)` |
| 多种失败共用一句笼统 msg | 每场景独立 ErrorCode（安全敏感除外） |
| 业务类放进 framework | 业务进 `module-*` |

---

## 13. 交付前

走 [checklist.md](checklist.md) 对应清单（新工程 / 新模块 / 新接口 / 开放接口 / PR）。

规则文件模板（复制到目标仓库 `.cursor/rules/`）：[templates/java-backend-standards.mdc](templates/java-backend-standards.mdc)
