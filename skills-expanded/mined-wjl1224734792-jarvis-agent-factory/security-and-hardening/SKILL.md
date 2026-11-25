---
name: security-and-hardening
description: "安全加固——OWASP 前十防护模式、鉴权模式、密钥管理、依赖审计、三层边界体系。用于处理用户输入、鉴权、数据存储或外部集成。"
version: "4.3.8"
updated: "2026-05-14"
---

# 安全加固

## 概述

安全不是可选项，也不是最后一步。从第一行代码开始，安全意识就应贯穿始终。一次疏忽足以让整个系统沦陷。

**核心原则：** 永远不信任用户输入，永远不硬编码密钥，永远假设攻击者比你聪明。

<HARD-GATE>
在引入任何用户输入处理、鉴权逻辑、数据存储或外部集成之前，必须先完成本文的安全检查。
</HARD-GATE>

## 铁律

```
不信任任何外部输入。不硬编码任何密钥。不留任何已知漏洞。
```

如果你在代码中看到了 `password = "admin123"`、`sql += userInput` 或 `innerHTML = data`，请立即停下来。

## 何时使用

**必须使用：**
- 处理任何用户输入（表单、URL 参数、HTTP header、文件上传）
- 实现鉴权或会话管理
- 涉及数据库查询
- 集成第三方服务或外部 API
- 存储或传输敏感数据
- 配置 CORS、CSP 或其他安全 header
- 添加新的依赖或更新现有依赖
- 处理文件上传
- 设计 API 端点

**以下情况也不要跳过：**
- 项目是"内部工具"（内部工具也是攻击入口）
- 这是原型阶段（原型会变成产品）
- 框架已经自带安全功能（框架提供工具，不提供保证）

## 安全审查流程

你必须按顺序完成每一步。

### 第一步：输入验证

**目标：** 确保所有外部输入在进入系统前被验证和净化。

1. **识别所有输入点**
   - 用户表单、URL 参数、HTTP header、Cookie
   - 文件上传、API 请求体、WebSocket 消息
   - 第三方回调参数

2. **客户端和服务端双重验证**
   - 客户端验证提升体验，但绝不能作为唯一防线
   - 服务端验证是最后一道闸门，必须存在
   - 规则：先验证格式（白名单），再验证语义（业务规则）

3. **SQL 注入防护**
   - 永远使用参数化查询（Parameterized Query），绝不拼接 SQL 字符串
   - 使用 ORM 时仍要检查是否有原生 SQL 拼接点

   ```python
   # 错误：字符串拼接
   cursor.execute(f"SELECT * FROM users WHERE name = '{username}'")

   # 正确：参数化查询
   cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
   ```

4. **XSS 防护**
   - 输出到 HTML 时对用户内容做上下文感知的编码
   - 使用 `textContent` 而非 `innerHTML`
   - 使用框架的模板引擎自动转义（如 React 的 JSX、Vue 的 `{{ }}`）
   - 避免 `dangerouslySetInnerHTML`、`v-html`，除非你完全信任内容

   ```javascript
   // 错误
   element.innerHTML = userInput;

   // 正确
   element.textContent = userInput;
   ```

5. **命令注入防护**
   - 绝不将用户输入拼接到 shell 命令
   - 使用参数化 API 而非 `exec()`、`system()`

### 第二步：鉴权与授权

**目标：** 确认用户身份（鉴权）并只允许必要的操作（授权）。

1. **鉴权检查**
   - 验证 Token 签名和过期时间
   - Session ID 使用安全随机数，设置 `HttpOnly`、`Secure`、`SameSite` 标记
   - 密码使用 bcrypt / argon2 哈希，绝不存明文
   - 实现 CSRF Token 保护所有状态变更操作

2. **授权检查**
   - 遵循最小权限原则（Least Privilege）：只给完成任务所需的最小权限
   - 每个 API 端点都做授权检查，不只靠前端隐藏按钮
   - 检查对象归属：用户 A 不能访问用户 B 的资源

   ```python
   # 错误：只检查了登录状态
   if request.user.is_authenticated:
       return get_order(order_id)

   # 正确：同时检查归属
   order = get_order(order_id)
   if order.user_id != request.user.id:
       raise PermissionDenied
   ```

3. **JWT 最佳实践**
   - 设置合理的过期时间（Access Token 15 分钟，Refresh Token 7 天）
   - 不在 Payload 中存放敏感信息（JWT 只签名不加密）
   - 验证 `iss`、`aud`、`exp` 所有关键字段

### 第三步：密钥管理

**目标：** 密钥绝不进入代码仓库或日志。

1. **禁止硬编码**
   - API Key、数据库密码、加密密钥——一律不得出现在代码中
   - 使用 `.env` 文件存放开发环境密钥，确保 `.env` 已加入 `.gitignore`
   - 生产环境使用 Vault（HashiCorp Vault）、云平台密钥管理服务或 Kubernetes Secrets

2. **环境变量规范**
   ```bash
   # 错误
   DATABASE_URL=postgres://admin:MyPassword123@localhost/db

   # 正确：密钥单独管理
   DATABASE_URL=postgres://localhost/db
   DB_USERNAME=admin
   DB_PASSWORD=  # 从密钥管理器注入，不写在 .env 中（生产环境）
   ```

3. **密钥不落地**
   - 密钥不写入日志（配置日志脱敏）
   - 密钥不通过 URL 传递
   - 前端代码中绝不能出现服务端密钥
   - CI/CD 中使用平台提供的 Secret 变量

### 第四步：依赖审计

**目标：** 已知漏洞必须在第一时间处理。

1. **运行审计命令**
   ```bash
   npm audit        # Node.js
   pip-audit        # Python
   cargo audit      # Rust
   bundle audit     # Ruby
   ```

2. **分级处置决策树**

   | 严重程度 | 行动 | 时间要求 |
   |---------|------|---------|
   | Critical | 立即修复，必要时回滚部署 | 当天 |
   | High | 本迭代内修复，评估是否可绕过 | 本 Sprint |
   | Moderate | 制定修复计划，安排在后续迭代 | 2 周内 |
   | Low | 记录跟踪，下次大版本更新时处理 | 按计划 |

3. **持续审计**
   - 将 `npm audit` / `pip-audit` 加入 CI 流程
   - 使用 Dependabot / Renovate 自动创建更新 PR
   - 关注的不只是直接依赖，还有间接依赖

### 第五步：安全头与边界防护

**目标：** 建立纵深防御的第三层——即使前两层失守，仍有防护。

1. **Content-Security-Policy (CSP)**
   - 限制脚本来源，禁止 `unsafe-inline` 和 `unsafe-eval`
   - 限制样式、图片、字体、连接的来源
   - 使用 `report-uri` 或 `report-to` 收集违规报告

   ```
   Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
   ```

2. **CORS 配置**
   - 不要用 `Access-Control-Allow-Origin: *`，除非是公开 API
   - 明确列出允许的 Origin 白名单
   - 避免 `Access-Control-Allow-Credentials: true` 与 `*` 同时使用
   - 限制 `Access-Control-Allow-Methods` 为实际需要的方法

3. **其他关键安全头**
   ```
   Strict-Transport-Security: max-age=31536000; includeSubDomains
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   Referrer-Policy: strict-origin-when-cross-origin
   Permissions-Policy: camera=(), microphone=(), geolocation=()
   ```

### 第六步：文件上传安全

**目标：** 文件上传是最高危的入口之一，必须层层设防。

1. **白名单扩展名验证**
   - 只允许业务必需的扩展名（如 `.jpg`、`.png`、`.pdf`）
   - 区分大小写，检查双扩展名（如 `file.jpg.php`）

2. **MIME 类型验证**
   - 检查文件头魔数（Magic Bytes），不信任客户端提供的 Content-Type
   - 使用服务端库检测真实文件类型

3. **存储与访问控制**
   - 上传文件存储在 Web 根目录之外
   - 使用随机文件名，不保留原始文件名
   - 通过鉴权接口提供文件下载，不直接暴露文件路径
   - 限制上传文件大小

4. **恶意文件扫描**
   - 生产环境集成 ClamAV 或其他反病毒引擎
   - 图片文件做重新编码（strip EXIF）以消除潜在 payload

### 第七步：速率限制

**目标：** 防止暴力破解、资源滥用和 DoS 攻击。

1. **必须限制的端点**
   - 登录接口：5 次/分钟/账户
   - 密码重置：3 次/小时/账户
   - 注册接口：3 次/小时/IP
   - 短信/邮件发送：1 次/分钟/手机号
   - API 端点：根据业务设定合理上限

2. **实现方式**
   - 使用 Redis 等内存数据库做计数器
   - 按 IP + 账户双维度限制
   - 返回 `429 Too Many Requests` 并附带 `Retry-After` header
   - 不要在客户端实现——服务端是唯一可信的施行点

### 第八步：安全响应

**目标：** 发现漏洞时不慌乱，按流程处理。

1. **评估**
   - 确认漏洞是否可复现
   - 评估影响范围：哪些数据、多少用户
   - 评估利用难度：是否已有公开 POC

2. **修复**
   - Critical 漏洞立即修复，必要时热修复上线
   - 修复后同步更新测试用例，防止回归
   - 审查同类代码，防止同一模式在其他地方存在

3. **通知**
   - 涉及用户数据泄露：按法规要求在时限内通知用户和监管机构
   - 内部记录：更新安全日志，记录根因和修复措施
   - 团队复盘：如何防止同类问题再次出现

## OWASP 前十速查

| 排名 | 漏洞类型 | 核心对策 |
|------|---------|---------|
| A01 | 访问控制失效 (Broken Access Control) | 每个端点都做授权检查，最小权限原则 |
| A02 | 加密失效 (Cryptographic Failures) | 用 bcrypt/argon2，HTTPS 全站强制，密钥不进代码 |
| A03 | 注入 (Injection) | 参数化查询，输入验证，命令参数化 API |
| A04 | 不安全设计 (Insecure Design) | 威胁建模，安全需求写入设计文档 |
| A05 | 安全配置错误 (Security Misconfiguration) | 关闭调试模式，加固默认配置，定期审计 |
| A06 | 自带漏洞组件 (Vulnerable Components) | 持续依赖审计，及时更新 |
| A07 | 鉴权失效 (Identification Failures) | 强密码策略，会话管理，防暴力破解 |
| A08 | 软件与数据完整性失效 (Software Integrity Failures) | 验证依赖完整性，CI/CD 管道安全 |
| A09 | 日志与监控失效 (Logging Failures) | 记录安全事件，配置告警，日志不泄露敏感信息 |
| A10 | SSRF (Server-Side Request Forgery) | 白名单验证出站请求目标，禁用不必要的 URL scheme |

## 常见合理化借口

| 合理化借口 | 现实 |
|-----------|------|
| "这是内部工具，不需要安全" | 内部工具也会被攻破。攻击者瞄准最弱环节。一个内部后台的弱密码足以让内网沦陷。 |
| "安全以后再加" | 事后加安全比从一开始构建难 10 倍。架构层面的安全问题几乎无法后期弥补。现在就加。 |
| "没人会攻击这个" | 自动化扫描器 24/7 在扫描互联网。安全靠隐蔽不是安全（Security by obscurity is not security）。 |
| "框架自带了安全" | 框架提供工具，不提供保证。React 防 XSS 的前提是你不用 `dangerouslySetInnerHTML`。你仍需正确使用它们。 |
| "这只是原型" | 原型会变成产品。安全习惯从第一天养成。一旦原型被"临时"部署到内网，它就是攻击面。 |
| "我不处理敏感数据" | 任何用户数据都可能被用于横向移动。一个看似无害的文件上传接口可能成为 RCE 入口。假设最坏情况。 |
| "开发环境无所谓" | 开发环境泄露的密钥可能关联生产。开发者本地的数据库可能包含真实用户数据。 |
| "等渗透测试再说" | 渗透测试一年一次，攻击者每天都在尝试。安全是持续的过程，不是年度检查点。 |

## 红线——停下来，做安全检查

如果你发现自己在想或写：
- `password = "xxx"` / `secret = "xxx"`（硬编码密钥）
- `sql += userInput` / `"SELECT * FROM " + tableName`（SQL 拼接）
- `innerHTML = data` / `dangerouslySetInnerHTML`（XSS 风险）
- `os.system(userInput)` / `exec(cmd + userArg)`（命令注入）
- `.env` 文件没有被 `.gitignore` 忽略
- `Access-Control-Allow-Origin: *` 配合 `Credentials: true`
- 文件上传没有校验文件类型
- 密码用 MD5 / SHA1 哈希
- 登录接口没有速率限制
- Token 没有设置过期时间

**以上任何一条出现，立即修复，不要继续写新功能。**

## 验证检查清单

在提交代码或发起 PR 前，逐项确认：

### 输入与注入
- [ ] 所有 SQL 查询使用参数化查询，无字符串拼接
- [ ] 用户输入内容在输出到 HTML 时做了上下文编码
- [ ] 没有将用户输入拼接到 shell 命令或 `eval` 中
- [ ] 客户端和服务端都有输入验证

### 鉴权与会话
- [ ] 每个需要保护的 API 端点都有鉴权中间件
- [ ] 资源访问有归属校验（用户不能访问他人数据）
- [ ] Session Cookie 设置了 `HttpOnly`、`Secure`、`SameSite`
- [ ] 实现了 CSRF 保护（状态变更操作）
- [ ] 密码使用 bcrypt / argon2 哈希存储

### 密钥与环境
- [ ] `.env` 已加入 `.gitignore`，不在仓库中
- [ ] 代码中无硬编码的密钥、密码、Token
- [ ] CI/CD 使用平台 Secret 变量，不在配置文件中暴露
- [ ] 日志输出已配置密钥脱敏

### 依赖
- [ ] `npm audit` / `pip-audit` 无 Critical 或 High 漏洞
- [ ] `.gitignore` 包含 `node_modules`、`venv` 等
- [ ] 依赖版本有理有据（不是随机 pin 到某个版本）

### HTTP 安全头
- [ ] 设置了 Content-Security-Policy（或至少有计划）
- [ ] CORS 配置为白名单模式，不使用 `*`
- [ ] 设置了 `Strict-Transport-Security`
- [ ] 设置了 `X-Content-Type-Options: nosniff`
- [ ] 设置了 `X-Frame-Options: DENY`

### 文件上传
- [ ] 文件类型使用扩展名白名单 + 魔数双重验证
- [ ] 上传文件存储在 Web 根目录之外
- [ ] 文件名使用随机字符串，不保留原始名
- [ ] 限制上传文件大小
- [ ] 生产环境有反病毒扫描

### 速率限制
- [ ] 登录接口有失败次数限制
- [ ] 密码重置接口有频率限制
- [ ] 短信/邮件发送接口有频率限制
- [ ] 关键 API 有合理的速率限制

### 日志与监控
- [ ] 关键操作有审计日志（登录、权限变更、数据删除）
- [ ] 日志不包含密码、Token 等敏感信息
- [ ] 异常情况有告警机制
