---
name: rest-graphql-debug
description: "Debug REST/GraphQL APIs: status codes, auth, schemas, repro."
version: 1.2.0
author: eren-karakus0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [api, rest, graphql, http, debugging, testing, curl, integration]
    category: software-development
    related_skills: [systematic-debugging, test-driven-development]
---

# API 测试与调试

借助 Hermes 工具对 REST 和 GraphQL 接口进行诊断——可使用 `terminal` 执行 `curl` 命令，用 `execute_code` 调用 Python 的 `requests` 库，或通过 `web_extract` 获取供应商提供的文档。在尝试修复问题之前，先定位出出现故障的具体环节。

## 适用场景

- API 返回意外的状态码或响应内容
- 认证失败（如令牌刷新、OAuth 或 API 密钥相关导致的 401/403 错误）
- 在 Postman 中能正常工作，但在代码中却无法运行
- 调试 Webhook 或回调集成问题
- 编写或审查 API 集成测试用例
- 遇到速率限制或分页问题

若涉及界面渲染、数据库查询优化或 DNS/防火墙基础设施相关问题，请跳过此步骤并上报处理。

## 核心原则

**先隔离问题环节，再逐一修复。** 即使返回 200 OK 状态码，数据仍可能存在错误；而 500 错误有时也可能只是由于一个字符的认证输入错误所致。需按顺序逐步排查，绝不能跳过任何步骤。

```
1. Connectivity   → can we reach the host at all?
1.5 Timeouts      → connect-slow vs read-slow?
2. TLS/SSL        → cert valid and trusted?
3. Auth           → credentials correct and unexpired?
4. Request format → payload shape match server expectations?
5. Response parse → does our code accept what came back?
6. Semantics      → does the data mean what we assume?
```

## 5分钟快速入门

### 通过终端使用REST接口

```python
# Verbose request/response exchange
terminal('curl -v https://api.example.com/users/1')

# POST with JSON
terminal("""curl -X POST https://api.example.com/users \\
  -H 'Content-Type: application/json' \\
  -H "Authorization: Bearer $TOKEN" \\
  -d '{"name":"test","email":"test@example.com"}'""")

# Headers only
terminal('curl -sI https://api.example.com/health')

# Pretty-print JSON
terminal('curl -s https://api.example.com/users | python -m json.tool')
```

### 通过终端使用 GraphQL

```python
terminal("""curl -X POST https://api.example.com/graphql \\
  -H 'Content-Type: application/json' \\
  -H "Authorization: Bearer $TOKEN" \\
  -d '{"query":"{ user(id: 1) { name email } }"}'""")
```

**GraphQL 的常见陷阱：** 即使查询失败，服务器也常常会返回 HTTP 200 状态码。无论状态码如何，都务必检查 `errors` 字段中的内容。

```python
execute_code('''
import os, requests
resp = requests.post(
    "https://api.example.com/graphql",
    json={"query": "{ user(id: 1) { name email } }"},
    headers={"Authorization": f"Bearer {os.environ['TOKEN']}"},
    timeout=10,
)
data = resp.json()
if data.get("errors"):
    for err in data["errors"]:
        print(f"GraphQL error: {err['message']} (path: {err.get('path')})")
print(data.get("data"))
''')
```

### 通过 execute_code 使用 Python（requests）

```python
execute_code('''
import requests
resp = requests.get(
    "https://api.example.com/users/1",
    headers={"Authorization": "Bearer <TOKEN>"},
    timeout=(3.05, 30),  # (connect, read)
)
print(resp.status_code, dict(resp.headers))
print(resp.text[:500])
''')
```

## 分层调试流程

### 第一步 — 连接性验证

```python
terminal('nslookup api.example.com')
terminal('curl -v --connect-timeout 5 https://api.example.com/health')
```

故障原因：DNS解析失败、防火墙阻隔、需要使用VPN、缺少代理服务器。

### 第1.5步 — 超时问题

区分“无法连接”与“可连接但速度缓慢”两种情况：

```python
terminal('''curl -w "dns:%{time_namelookup}s connect:%{time_connect}s tls:%{time_appconnect}s ttfb:%{time_starttransfer}s total:%{time_total}s\\n" \\
  -o /dev/null -s https://api.example.com/endpoint''')
```

在 Python 中，务必传入一个元组形式的超时参数——因为 `requests` 没有默认超时设置，否则会导致程序永久挂起。

```python
execute_code('''
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout
try:
    requests.get(url, timeout=(3.05, 30))
except ConnectTimeout:
    print("Cannot reach host — DNS, firewall, VPN")
except ReadTimeout:
    print("Connected but server is slow")
''')
```

诊断结果：`time_connect` 值过高通常由网络或防火墙问题导致；而 `time_connect` 值正常但 `time_starttransfer` 值偏高，则说明服务器响应缓慢。

### 第 2 步 — TLS/SSL 设置

```python
terminal('curl -vI https://api.example.com 2>&1 | grep -E "SSL|subject|expire|issuer"')
```

错误原因包括：证书过期、自签名证书、主机名不匹配以及缺少CA证书包。请仅将 `-k` 选项用于临时调试，绝不可将其嵌入代码中。

### 第3步 — 认证

```python
# Token validity check
terminal('curl -s -o /dev/null -w "%{http_code}\\n" -H "Authorization: Bearer $TOKEN" https://api.example.com/me')

# Decode JWT exp claim — handles base64url padding correctly
execute_code('''
import json, base64, os
tok = os.environ["TOKEN"]
payload = tok.split(".")[1]
payload += "=" * (-len(payload) % 4)
print(json.dumps(json.loads(base64.urlsafe_b64decode(payload)), indent=2))
''')
```

检查清单：
- 令牌是否已过期？（JWT中的`exp`字段）
- 使用的协议是否正确？是Bearer、Basic、Token还是`X-Api-Key`？
- 环境设置是否无误？在生产环境中误使用测试密钥是常见错误
- API密钥是放在请求头中还是查询参数中（`?api_key=…`）？

### 第4步 — 请求格式

```python
terminal("""curl -v -X POST https://api.example.com/endpoint \\
  -H 'Content-Type: application/json' \\
  -d '{"key":"value"}' 2>&1""")
```

**内容类型与请求体不匹配——隐形的 415/400 错误：**

```python
# WRONG — data= sends form-encoded, header lies
requests.post(url, data='{"k":"v"}', headers={"Content-Type": "application/json"})

# RIGHT — json= auto-sets header AND serializes
requests.post(url, json={"k": "v"})

# WRONG — Accept says XML, code calls .json()
requests.get(url, headers={"Accept": "text/xml"})

# RIGHT — let requests build multipart with boundary
requests.post(url, files={"file": open("doc.pdf", "rb")})
```

常见问题：表单编码与JSON格式的区别、缺失必填字段、错误的HTTP方法以及未编码的查询参数。

### 第5步 — 响应解析

在调用`.json()`方法之前，务必先检查内容类型：

```python
execute_code('''
import requests
resp = requests.post(url, json=payload, timeout=10)
print(f"status={resp.status_code}")
print(f"headers={dict(resp.headers)}")
ct = resp.headers.get("Content-Type", "")
if "application/json" in ct:
    print(resp.json())
else:
    print(f"unexpected content-type {ct!r}, body={resp.text[:500]!r}")
''')
```

错误类型：本应返回 JSON 格式却出现 HTML 错误页面、响应体为空，或是字符集不正确。

### 第 6 步——语义验证

虽然数据已成功解析，但其内容是否*正确*？

- `"status": "active"` 的含义是否符合您的代码预期？
- 响应中的 ID 是否与请求时的一致？
- 时间戳是否处于正确的时区？
- 分页返回的是所有数据，还是仅第 1 页的内容？

## HTTP 状态码指南

### 401 未授权——凭证缺失或无效

1. 确实存在 `Authorization` 请求头？（可使用 `curl -v` 进行确认）
2. Token 是否正确且未过期？
3. 使用的认证机制是否正确？（`Bearer`、`Basic` 还是 `Token`）
4. 部分 API 会使用查询参数（如 `?api_key=…`）而非请求头进行认证。

### 403 禁止访问——已通过认证但无相应权限

1. Token 是否具备所需的权限范围/权限？
2. 该资源是否属于其他账户所有？
3. 是否被 IP 允许列表阻止访问？
4. 浏览器是否启用了 CORS？（请检查 `Access-Control-Allow-Origin` 设置）

### 404 未找到——资源不存在或 URL 错误

1. 路径是否正确？（是否存在尾随斜杠、拼写错误或版本前缀问题）
2. 资源 ID 是否存在？
3. 使用的 API 版本是否正确？（`/v1/` 还是 `/v2/`）？
4. 基础 URL 是否正确？（测试环境还是生产环境？）

### 409 冲突——状态不一致

1. 该资源已存在（出现重复创建情况）？
2. `ETag` / `If-Match` 值是否已过期？
3. 是否有其他进程正在同时修改该资源？

### 422 错误实体——JSON 格式有效，但数据无效

错误响应体通常会指出有问题的字段。请检查以下内容：
- 字段类型（字符串与整数、日期格式等）
- 字段是必填还是可选
- 值是否属于允许的枚举集合中

### 429 请求过多——达到速率限制

请查看 `Retry-After` 和 `X-RateLimit-*` 头字段。采用指数退避策略：

```python
execute_code('''
import time, requests

def with_backoff(method, url, **kwargs):
    for attempt in range(5):
        resp = requests.request(method, url, **kwargs)
        if resp.status_code != 429:
            return resp
        wait = int(resp.headers.get("Retry-After", 2 ** attempt))
        time.sleep(wait)
    return resp
''')
```

### 5xx错误 —— 服务器端问题，通常非用户过错

- **500** —— 服务器故障。请记录关联ID，并将相关文件提交给服务提供商。
- **502** —— 上游服务不可用。请采用退避策略后重试。
- **503** —— 服务器过载或正在维护中。请查看状态页面。
- **504** —— 上游请求超时。建议减少请求数据量或延长超时时间。

对于所有5xx错误：均应采用带抖动机制的退避策略，若问题持续存在则需触发警报。

## 分页与幂等性

**分页处理。**请确保获取到*全部*结果。注意查看`next_cursor`、`next_page`及`total_count`等字段。分页方式有两种：
- 偏移量分页（`?limit=100&offset=200`）——实现简单，但若数据顺序发生变化可能导致遗漏部分数据。
- 游标分页（`?cursor=abc123`）——更适合实时数据或大规模数据集。

**幂等性。**对于非幂等操作（如POST请求），请在请求中添加`Idempotency-Key: <uuid>`字段，以避免重复处理导致的数据重复创建或费用双重收取。支付与订单相关操作必须遵循此原则。

## 合同验证

在问题影响生产环境之前，及时发现架构变动。

```python
execute_code('''
import requests

def validate_user(data: dict) -> list[str]:
    errors = []
    required = {"id": int, "email": str, "created_at": str}
    for field, expected in required.items():
        if field not in data:
            errors.append(f"missing field: {field}")
        elif not isinstance(data[field], expected):
            errors.append(f"{field}: want {expected.__name__}, got {type(data[field]).__name__}")
    return errors

resp = requests.get(f"{BASE}/users/1", headers=HEADERS, timeout=10)
issues = validate_user(resp.json())
if issues:
    print(f"contract violations: {issues}")
''')
```

在 API 升级后、集成新第三方时，或在进行 CI 烟雾测试时运行。

## 关联编号

务必记录提供方的请求编号——这是联系供应商获取支持的最快途径：

```python
execute_code('''
import requests
resp = requests.post(url, json=payload, headers=headers, timeout=10)
request_id = (
    resp.headers.get("X-Request-Id")
    or resp.headers.get("X-Trace-Id")
    or resp.headers.get("CF-Ray")  # Cloudflare
)
if resp.status_code >= 400:
    print(f"failed status={resp.status_code} req_id={request_id} ts={resp.headers.get('Date')}")
''')
```

**供应商缺陷报告模板：**

```
Endpoint:    POST /api/v1/orders
Request ID:  req_abc123xyz
Timestamp:   2026-03-17T14:30:00Z
Status:      500
Expected:    201 with order object
Actual:      500 {"error":"internal server error"}
Repro:       curl -X POST … (auth: <REDACTED>)
```

## 回归测试模板

将该模板放入 `tests/` 目录中，然后通过命令 `terminal('pytest tests/test_api_smoke.py -v')` 来运行：

```python
import os, requests, pytest

BASE_URL = os.environ.get("API_BASE_URL", "https://api.example.com")
TOKEN    = os.environ.get("API_TOKEN", "")
HEADERS  = {"Authorization": f"Bearer {TOKEN}"}

class TestAPISmoke:
    def test_health(self):
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        assert resp.status_code == 200

    def test_list_users_returns_array(self):
        resp = requests.get(f"{BASE_URL}/users", headers=HEADERS, timeout=10)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data.get("data", data), list)

    def test_get_user_required_fields(self):
        resp = requests.get(f"{BASE_URL}/users/1", headers=HEADERS, timeout=10)
        assert resp.status_code in (200, 404)
        if resp.status_code == 200:
            user = resp.json()
            assert "id" in user and "email" in user

    def test_invalid_auth_returns_401(self):
        resp = requests.get(
            f"{BASE_URL}/users",
            headers={"Authorization": "Bearer invalid-token"},
            timeout=10,
        )
        assert resp.status_code == 401
```

## 安全性

### 令牌处理
- 绝不对完整的令牌进行日志记录。应将其遮蔽为：`Bearer <REDACTED>`。
- 切勿在脚本中硬编码令牌。应从环境变量（如 `os.environ["API_TOKEN"]`）或 `${HERMES_HOME:-~/.hermes}/.env` 中读取令牌。
- 若在日志、错误信息或 Git 历史记录中发现令牌，应立即更换。

### 安全的日志记录方式

```python
def redact_auth(headers: dict) -> dict:
    sensitive = {"authorization", "x-api-key", "cookie", "set-cookie"}
    return {k: ("<REDACTED>" if k.lower() in sensitive else v) for k, v in headers.items()}
```

### 漏洞检查清单

- [ ] **URL 中的凭证信息。** 查询字符串中的 API 密钥可能会出现在服务器日志、浏览器历史记录以及引用头中——应使用专用头部字段来传递。
- [ ] **错误响应中的敏感个人信息。** 如 `/users/123` 返回 `404` 错误时，不应暴露该用户是否存在的信息（即避免信息枚举）。
- [ ] **生产环境中的堆栈跟踪信息。** 500 类错误不应泄露文件路径或框架版本等信息。
- [ ] **内部主机名/IP 地址。** 错误响应内容中不应出现 `10.x.x.x`、`internal-api.corp.local` 等内部地址。
- [ ] **被原样返回的令牌。** 部分 API 会在错误详情中包含认证令牌，需确认此类情况不存在。
- [ ] **过量的 `Server` / `X-Powered-By` 头部信息。** 这些信息可能泄露系统架构细节，需在安全审查时重点注意。

## Hermes 工具模式

### terminal — 适用于 curl、dig、openssl 等工具

```python
terminal('curl -sI https://api.example.com')
terminal('openssl s_client -connect api.example.com:443 -servername api.example.com </dev/null 2>/dev/null | openssl x509 -noout -dates')
```

### execute_code — 用于多步骤 Python 流程

在调试包含认证 → 获取数据 → 分页处理 → 验证等环节的流程时，可使用 `execute_code`。该函数可使变量在脚本中保持有效，结果会输出到标准输出，并且不会在当前上下文中引发令牌滥用风险：

```python
execute_code('''
import os, requests

token = os.environ["API_TOKEN"]
base  = "https://api.example.com"
H     = {"Authorization": f"Bearer {token}"}

# 1. auth
me = requests.get(f"{base}/me", headers=H, timeout=10)
print(f"auth {me.status_code}")

# 2. paginate
all_users, cursor = [], None
while True:
    params = {"cursor": cursor} if cursor else {}
    r = requests.get(f"{base}/users", headers=H, params=params, timeout=10)
    body = r.json()
    all_users.extend(body["data"])
    cursor = body.get("next_cursor")
    if not cursor:
        break
print(f"users={len(all_users)}")
''')
```

### web_extract — 用于获取供应商 API 文档

直接获取您正在调试的接口的详细规范，而无需自行猜测：

```python
web_extract(urls=["https://docs.example.com/api/v1/users"])
```

### delegate_task — 用于执行完整的 CRUD 测试流程

```python
delegate_task(
    goal="Test all CRUD endpoints for /api/v1/users",
    context="""
Follow the rest-graphql-debug skill (optional-skills/software-development/rest-graphql-debug).
Base URL: https://api.example.com
Auth: Bearer token from API_TOKEN env var.

For each verb (POST, GET, PATCH, DELETE):
  - happy path: assert status + response schema
  - error cases: 400, 404, 422
  - log a repro curl for any failure (redact tokens)

Output: pass/fail per endpoint + correlation IDs for failures.
""",
    toolsets=["terminal", "file"],
)
```

## 输出格式

在报告检测结果时：

```
## Finding
Endpoint: POST /api/v1/users
Status:   422 Unprocessable Entity
Req ID:   req_abc123xyz

## Repro
curl -X POST https://api.example.com/api/v1/users \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <REDACTED>' \
  -d '{"name":"test"}'

## Root Cause
Missing required field `email`. Server validation rejects before processing.

## Fix
-d '{"name":"test","email":"test@example.com"}'
```

## 相关内容

- `systematic-debugging` — 在定位出出问题的 API 层之后，深入探究代码的根本原因  
- `test-driven-development` — 在发布修复方案之前，先编写回归测试
