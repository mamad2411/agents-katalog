---
name: kwc-ks-controller-development
description: 【KWC KS Controller 开发阶段 Skill】由 kwc-orchestrator 在 Controller 代码实现阶段调度，仅当 app/ks/controller/ 目录存在时激活。本 Skill 专注于 KingScript 脚本控制器的 XML 配置编写和 TypeScript/KingScript 代码实现，不负责工程创建、构建或部署（交由 kwc-project-scaffold），也不负责 UI/UX 设计（交由 kwc-design）。涉及 KingScript 语言规范和 SDK 使用时，引用 kingscript-code-generator 技能包。若任务涉及 kd CLI、构建、部署，必须通知 kwc-orchestrator 切换到 kwc-project-scaffold。
---

# KWC KS Controller 开发专家

当项目中需要开发 KingScript 脚本控制器（后端 REST API）时，本 Skill 负责控制器的 XML 配置编写和脚本代码实现。

## 重要：使用前置条件

**必须同时满足以下条件才能使用本 Skill：**
1. 当前目录已存在 `.kd/config.json` 文件
2. 工程中已存在 `app/ks/controller/` 目录
3. 工程已通过 `kwc-project-scaffold` 完成初始化

**以下场景禁止使用本 Skill，必须交由 `kwc-project-scaffold`：**
- 工程初始化（`kd project init`）
- 创建组件或页面（`kd project create --type kwc` / `kd project create --type page`）
- 生成或修改 `.js-meta.kwc` 组件元数据
- 生成或修改 `.page-meta.kwp` 页面元数据
- 环境配置（`kd env` 相关命令）
- 构建操作（`npm run build:controller` / `kd project build --type controller`）
- 部署操作（`kd project deploy`）
- 调试操作（`kd debug`）— 调试由 kwc-project-scaffold 负责，须以后台模式运行（`is_background: true`），详见其调试约定

若当前不满足上述前置条件，请立即停止并切换到 `kwc-project-scaffold` Skill。

## 核心职责

你负责指导用户进行 KingScript 脚本控制器的开发、修改和维护，包括：
- 编写和修改 Controller XML 配置文件
- 编写和修改 Controller KingScript/TypeScript 脚本代码
- 使用 KS SDK 进行数据查询和业务操作

**重要**：你必须严格遵守**本 Skill 目录下的** `rule.md` 文件中定义的硬性约束。在开始任何代码编写前，请务必阅读并理解这些规则。

## KingScript 技能引用映射

本 Skill 的 KingScript 语言和 SDK 知识来自 `kingscript-code-generator` 技能包。当需要查阅语言规范、SDK 类和方法时，应引用以下路径：

| 场景 | 引用路径 |
|------|---------|
| Controller XML 配置和请求/响应 API | `kingscript-code-generator/references/docs/custom-development/脚本控制器开发指南.md` |
| KingScript 语言基础（变量、类、方法、模块、异常处理） | `kingscript-code-generator/references/language/kingscript/README.md` |
| SDK 类型查询 | `kingscript-code-generator/references/sdk/indexes/class-index.md` |
| SDK 方法查询 | `kingscript-code-generator/references/sdk/indexes/method-index.md` |
| 按场景查找 SDK 用法 | `kingscript-code-generator/references/sdk/indexes/scenario-index.md` |
| 数据对象操作（DynamicObject） | `kingscript-code-generator/references/sdk/classes/DynamicObject.md` |
| 数据库查询（QueryServiceHelper） | `kingscript-code-generator/references/sdk/classes/QueryServiceHelper.md` |
| 业务数据操作（BusinessDataServiceHelper） | `kingscript-code-generator/references/sdk/classes/BusinessDataServiceHelper.md` |
| Java-KingScript 类型桥接 | `kingscript-code-generator/references/sdk/docs/java-kingscript-bridge.md` |
| SDK 完整策略和降级链路 | `kingscript-code-generator/references/sdk/strategy.md` |

## 标准工作流 (Workflow)

1. **确认目录存在**：Controller 目录已由 scaffold 创建（`app/ks/controller/<Name>/`）
2. **编写 XML 配置**：编写/修改 Controller XML 配置文件，定义 URL 路由、HTTP 方法和权限
3. **编写脚本代码**：编写/修改 Controller TypeScript/KingScript 脚本代码，实现业务逻辑
4. **查阅 SDK**：涉及 SDK 使用时，查阅 kingscript-code-generator 技能包的 SDK 索引和知识卡
5. **交付构建**：完成后通知用户回到 scaffold 进行构建和部署

## 关键约束摘要（详见 rule.md）

- **类名规范**：使用 PascalCase + Controller 后缀（如 `UserController`）
- **导出实例**：必须导出 `kwcController` 实例：`let kwcController = new MyController(); export { kwcController };`
- **方法签名**：统一为 `methodName(request: any, response: any)`
- **URL 规则**：至少 3 级路径（`/{isv}/{app}/{resource}`）
- **权限配置**：每个 method 必须有 permission 配置
- **SDK 调用**：不编造不存在的 KS API，调用前先确认存在

## 常用资源

- **Controller 在 KWC 工程中的集成工作流**：`reference/controller-scaffold-workflow.md`
- **Controller 常见模式和代码示例**：`reference/controller-patterns.md`
- **脚本控制器开发完整指南**（位于 kingscript-code-generator 技能包）：`kingscript-code-generator/references/docs/custom-development/脚本控制器开发指南.md`

## 输出检查清单

提交代码前，请自查：
- [ ] XML 必填字段完整（name/isv/app/version/url/scriptFile/methods）
- [ ] URL 路径符合 `/{isv}/{app}/...` 规则（至少 3 级）
- [ ] 每个 method 配置了 permission
- [ ] 脚本文件正确导出了 `kwcController` 实例
- [ ] 请求参数获取使用了正确的类型方法（如 `getLongPathVariable` 而非 `getPathVariable`）
- [ ] 错误场景有 `response.throwException` 处理
- [ ] SDK 调用在 kingscript-code-generator 索引中已确认存在
- [ ] **未运行**任何构建或部署命令（那是 scaffold 的职责）

## 快速参考

### A. 请求/响应 API 速查表

**Request API：**

| 方法 | 说明 | 示例 |
|------|------|------|
| `request.getLongPathVariable(name)` | 获取路径参数 (Long) | `/user/{id}` → `request.getLongPathVariable('id')` |
| `request.getPathVariable(name)` | 获取路径参数 (String) | `/user/{id}` → `request.getPathVariable('id')` |
| `request.getStringQueryParam(name)` | 获取查询参数 (String) | `?lang=zh` |
| `request.getIntQueryParam(name)` | 获取查询参数 (Int) | `?page=1` |
| `request.getBooleanQueryParam(name)` | 获取查询参数 (Boolean) | `?active=true` |
| `request.getMapBody()` | 获取 JSON 请求体 | POST body |
| `request.getHeader(name)` | 获取请求头 | `request.getHeader('Authorization')` |

**Response API：**

| 方法 | 说明 | 示例 |
|------|------|------|
| `response.ok(data)` | 成功响应 (200) | `response.ok({ id: 1 })` |
| `response.of(statusCode, data)` | 自定义状态码 | `response.of(201, { message: '创建成功' })` |
| `response.throwException(msg, httpCode, bizCode)` | 抛出异常 | `response.throwException('参数无效', 400, 'INVALID_PARAM')` |

### B. 权限配置速查

| 模式 | 配置关键字段 | 适用场景 |
|------|------------|--------|
| 标准权限验证 | `needall=false` + `entityNumber` + `permItemId` | 需要权限控制的接口 |
| 跳过权限检查 | `permitAll` 留空 | 内部调用、不需要权限检查 |
| 匿名访问 | `permitAll` + `anonymousUser` 留空 | 公开接口、无需登录 |

### C. 常用状态码

| 状态码 | 含义 | 使用方式 |
|--------|------|--------|
| 200 | 成功 | `response.ok(data)` |
| 201 | 创建成功 | `response.of(201, data)` |
| 400 | 请求参数错误 | `response.throwException(msg, 400, code)` |
| 401 | 未授权 | `response.throwException(msg, 401, code)` |
| 403 | 禁止访问 | `response.throwException(msg, 403, code)` |
| 404 | 资源不存在 | `response.throwException(msg, 404, code)` |
| 500 | 服务器内部错误 | `response.throwException(msg, 500, code)` |
