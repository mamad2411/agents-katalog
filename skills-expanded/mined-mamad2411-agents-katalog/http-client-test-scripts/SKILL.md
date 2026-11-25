---
name: http-client-test-scripts
description: 编写 IntelliJ HTTP Client 的 *.http 自动化测试脚本。当用户需要创建、编辑或调试 .http 文件时使用此技能，包括：编写 HTTP/GraphQL/WebSocket 请求、添加响应断言测试、使用变量和环境配置、编写 pre-request 和 response handler 脚本、配置循环请求和导入、从 cURL/OpenAPI/Postman 转换请求。即使用户只提到 "http 请求"、"接口测试"、"API 测试"、"REST 测试"、".http 文件" 或 "HTTP Client"，也应触发此技能。
metadata.source: https://github.com/justinwongcn/jetbrains-http-client-skills/tree/main/skills/http-client-test-scripts
---

# HTTP Client 自动化测试脚本编写技能

本技能指导你编写 IntelliJ IDEA HTTP Client 的 `.http` 文件，用于 API 接口测试和自动化验证。

## 核心概念

`.http` 文件可以包含多个请求，用 `###` 分隔。每个请求由请求行、头部、请求体和可选的脚本组成。

### 请求行格式

```
Method Request-URI HTTP-Version
```

- Method: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, WEBSOCKET, GRAPHQL 等
- GET 请求可省略方法，直接写 URI
- HTTP-Version 可选：`HTTP/1.1`、`HTTP/2`、`HTTP/2 (Prior Knowledge)`

### 请求命名与注释

- 在 `###` 后写描述性名称，或用 `# @name` 命名
- `//` 或 `#` 开头的行为注释

### 变量使用

所有变量用 `{{variable}}` 引用。变量优先级从高到低：

1. **环境变量** — `http-client.env.json` / `http-client.private.env.json`
2. **全局变量** — `client.global.set()` 在脚本中设置
3. **文件内变量** — 文件顶部 `@host = value` 定义
4. **请求级变量** — pre-request 脚本中 `request.variables.set()` 设置
5. **动态变量** — `{{$uuid}}`、`{{$timestamp}}`、`{{$random.email}}` 等

### 脚本系统

- **Pre-request 脚本** `< {% ... %}` — 请求前执行，设置变量、计算签名
- **Response Handler 脚本** `> {% ... %}` — 响应后执行，断言测试、提取数据
- **公共导入块** `={% ... %}` — 文件顶部，导入共享模块

### 断言测试

```javascript
client.test("测试名称", function() {
    client.assert(response.status === 200, "状态码不是 200");
    client.assert(response.body.id !== undefined, "缺少 id 字段");
});
```

### 认证模式

- `Authorization: Basic username password` — Basic 认证
- `Authorization: Digest username password` — Digest 认证
- `Authorization: Bearer {{auth_token}}` — Token 认证（先登录获取，`client.global.set` 保存）

### 循环请求（数据驱动测试）

在 pre-request 脚本中用 `request.variables.set("items", [...])` 定义数组，请求体中用 JSONPath `{{$.items..field}}` 循环，response handler 中用 `request.iteration()` 获取当前迭代索引。

### 请求标签

| 标签 | 说明 |
|------|------|
| `@no-redirect` | 禁用重定向跟随 |
| `@no-cookie-jar` | 禁用 Cookie 存储 |
| `@no-log` | 禁用请求日志 |
| `@no-auto-encoding` | 禁用自动编码 |
| `@timeout` | 设置超时（秒） |
| `@connection-timeout` | 设置连接超时 |

## 编写测试的最佳实践

1. **每个请求都应有描述性名称** — 方便在 Services 工具窗口中识别
2. **断言要有清晰的错误消息** — 便于定位问题
3. **使用环境变量管理不同环境** — 不要硬编码 host 和凭证
4. **敏感信息放在 private 环境文件** — 确保不提交到版本控制
5. **利用全局变量传递 Token** — 先登录获取，后续请求复用
6. **使用循环进行数据驱动测试** — 避免重复编写相似请求
7. **将公共脚本抽取为模块** — 通过 import 复用
8. **使用 `@no-log` 保护敏感请求** — 避免日志泄露
9. **合理使用 `@timeout`** — 为慢速接口设置超时
10. **先验证状态码再验证内容** — 确保请求本身成功

## 参考资源索引

当需要查看具体的语法示例或 API 细节时，请按需阅读以下参考文件：

### 语法与示例（references/syntax-and-examples.md）

请求类型详解（GET/POST/GraphQL/WebSocket）、变量系统完整说明、脚本系统用法、认证请求、循环请求、文件导入与运行、响应重定向、加密签名、WebSocket/事件流/XML 处理、CLI 运行、完整测试示例。当你需要查看某个功能的完整代码示例时查阅。

### API 参考（references/api-reference.md）

`client`/`response`/`request` 对象的完整方法列表、动态变量完整列表、加密 API、请求标签、CLI 命令参考。当你需要查看某个具体 API 的参数或用法时查阅。

### 官方示例文件（references/examples/）

JetBrains 官方 .http 示例，覆盖所有请求类型。当你不确定某个功能的精确语法时，优先查阅对应示例。

| 文件 | 覆盖内容 | 何时查阅 |
|------|----------|----------|
| `get-requests.http` | GET 请求、查询参数、请求头、Cookie、动态变量、请求标签、响应重定向、HTTP/2 | 写 GET 请求或需要请求标签时 |
| `post-requests.http` | POST 请求、JSON body、x-www-form-urlencoded、multipart/form-data 文件上传 | 写 POST 请求或上传文件时 |
| `graphql-requests.http` | GRAPHQL 关键字（HTTP & WebSocket）、query/mutation/subscription、变量传递、AWS AppSync | 写 GraphQL 请求时 |
| `ws-requests.http` | WEBSOCKET 关键字、`===` 消息分隔、`=== wait-for-server`、`onEachMessage` 脚本、`output()` | 写 WebSocket 请求时 |
| `requests-with-authorization.http` | Basic/Digest 认证、Bearer Token 流程、`client.global.set` 传递 token | 写认证相关请求时 |
| `requsts-with-test.http` | `client.test`/`client.assert` 断言、response 属性验证、crypto 签名、`import` 模块 | 写断言测试或加密签名时 |
| `requests-with-loop.http` | `request.variables.set` 数组、JSONPath 循环、`request.iteration()`、`jsonPath()` | 写数据驱动循环测试时 |
| `requests-with-include.http` | `import` 导入文件、`run` 运行外部请求、`run #请求名`、覆盖变量 | 需要跨文件引用或运行时 |
| `whats-new.http` | `={% %}` 公共导入块、`setTimeout`/`sleep()` 延时、`$random.locale` 本地化、Cookie 提取 | 使用延时、Cookie、公共导入时 |
| `different-responses.http` | 图片/PDF/HTML 等非 JSON 响应类型 | 处理非 JSON 响应时 |
