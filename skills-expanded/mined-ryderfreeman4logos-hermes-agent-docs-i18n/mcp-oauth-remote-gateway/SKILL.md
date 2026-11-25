---
name: mcp-oauth-remote-gateway
description: Manual OAuth for remote MCP servers on headless gateways.
version: 1.0.0
author: Ben Barclay (benbarclay), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [MCP, OAuth, PKCE, Remote-Deployment]
    related_skills: [hermes-agent, mcporter, fastmcp]
---

# 远程 Hermes 网关上的 MCP OAuth

## 概述

Hermes 内置的 MCP OAuth 客户端会在 Hermes 进程内的 `127.0.0.1:<port>` 地址上启动一个一次性 HTTP 监听器，并将该回环地址注册为 OAuth 的 `redirect_uri`。对于运行在用户本机上的本地 CLI，这种方式能够完美工作。但当 Hermes 作为远程网关（容器、VPS、消息机器人等）运行时，该方法就会完全失效——因为用户的浏览器会将 `127.0.0.1` 解析为用户自己的笔记本电脑地址，而非远程容器地址，从而导致授权码根本无法送达 Hermes。

本技能会手动完成 OAuth 授权流程，并将生成的令牌写入 Hermes 令牌存储所期望的特定文件中。这样一来，后续执行 `/reload-mcp` 命令时就能找到缓存的令牌，从而完全跳过浏览器授权流程。

## 适用场景

仅在满足以下**所有**条件时才可使用此技能：

1. 用户希望添加一个需要 OAuth 授权的远程 HTTP MCP 服务器（而非使用静态 Bearer 令牌）。
2. Hermes 正在作为**远程网关**运行（容器、VPS、Docker、托管服务等），而非用户笔记本电脑上的本地 CLI。
3. 该服务器支持带有 PKCE 功能的 OAuth 2.1 标准以及 RFC 7591 规定的动态客户端注册功能（大多数现代 MCP 服务器都支持，如 Better Stack、Linear、Cloudflare、Datadog 等）。如果该服务器不支持 DCR 功能（GitHub 是典型的例外），则此技能不适用——此时应使用预先注册的 OAuth 应用或个人访问令牌。

**请勿将此技能用于以下情况：**
- **本地 CLI Hermes** — 仅需在 `mcp_servers.<name>` 及 `/reload-mcp` 配置中设置 `auth: oauth` 即可。内置流程会自动打开浏览器，并在本地主机捕获回调请求，运行效果十分理想。  
- **支持静态Bearer令牌（API密钥）的服务器** — 若用户同意，建议始终使用 `headers.Authorization: "Bearer <token>"` 的方式，这样更简单，也无需处理令牌刷新的问题。  
- **GitHub Copilot MCP** (`api.githubcopilot.com/mcp/`) — GitHub并未提供DCR接口，因此需使用PAT或预先注册的OAuth应用（参见注意事项12）。

## 为何内置OAuth流程在远程网关上会失败

Hermes自带的MCP OAuth客户端（`tools/mcp_oauth.py`）的工作流程如下：

1. 选择一个空闲的本地端口 `P`。  
2. 向授权服务端注册一个动态OAuth客户端，同时指定 `redirect_uri = http://127.0.0.1:P/callback`。  
3. 在Hermes进程内部于 `127.0.0.1:P` 端口启动一个HTTP服务器。  
4. 输出授权URL，并在本地端点等待用户返回的授权码。

当Hermes在远程环境中运行时，`redirect_uri` 中的 `127.0.0.1` 实际指的是远程容器的回环地址，而非用户的本地地址。用户完成授权后，浏览器会被重定向至 `http://127.0.0.1:P/callback?code=...`，但由于该地址指向的是用户自己的笔记本，因此无法建立连接。回调请求永远无法送达Hermes进程，流程随之超时，此时执行 `/reload-mcp` 会返回“没有可用的MCP工具”这样的提示，且不会提供任何详细信息。

可识别的异常迹象包括：在hermes用户对应的系统中出现 `[xdg-open] <defunct>` 类型的进程，` $HERMES_HOME/mcp-tokens/` 目录为空或不存在，以及重新加载后虽有响应，但 `change_detail` 输出中却没有任何“已添加/重新连接：X”之类的记录。

## 经济实惠的备用方案：内置流程自带的应急出口

在手动进行令牌操作之前，先确认内置流程的备用机制是否已能解决当前部署问题。当Hermes检测到远程会话时，它会在授权URL（`tools/mcp_oauth.py`）旁边显示两种选项：

1. **复制粘贴法**——在交互式终端中，标准输入读取器会与HTTP监听器同时工作。用户完成授权后，若浏览器无法连接到`127.0.0.1:<port>`，则可将地址栏中的完整URL（`?code=...&state=...`）直接粘贴到命令提示符中。此方法适用于通过SSH连接的CLI会话。
2. **SSH端口转发法**——使用命令`ssh -N -L <port>:127.0.0.1:<port> <user>@<host>`，即可让请求正常传递至远程监听器。

这两种方法都需要连接到Hermes主机的交互式终端。本指南的其余内容则针对没有交互式终端的情况——即Hermes仅作为消息网关或机器人运行，此时执行`/reload-mcp`指令会触发流程，但并无用户处于命令提示符前。

## 首选入口：Hermes控制面板（在手动操作令牌之前请先尝试此方法）

远程Hermes网关通常还会以独立进程的形式运行**控制面板**Web界面（例如`hermes dashboard --host 0.0.0.0 --port <port>`；可通过`ps aux | grep 'hermes dashboard'`查看其运行状态）。该控制面板提供了一个连接器/MCP控制台，包含诸如 `/api/mcp/servers`、`/api/mcp/status` 和 `/connectors` 等接口（所有接口均需登录才能访问；使用无cookie的curl请求若返回401/302错误，即说明这些接口确实存在）。

**为何仪表板能解决核心问题：** 当用户在**自己的浏览器**中通过仪表板发起 OAuth 请求时，重定向会进入仪表板可捕获的上下文，从而避免因 `127.0.0.1` 回调失败而导致的 CLI/手动操作流程中断。因此，“在远程网关上添加或重新认证 OAuth MCP 服务器”的正确处理顺序为：

1. **用户浏览器中的仪表板**——这是预定的主要操作入口。用户可直接在此添加服务器、执行 OAuth 认证并刷新页面，所有操作均在用户身份下完成。无需反复复制粘贴处理回调，也无需手动编写令牌文件。
2. **手动令牌处理（即本技能的其余部分）**——在无法通过浏览器访问仪表板时（纯聊天界面/无界面环境）的备用方案。

**查找仪表板的公网 URL。** 仪表板在内部绑定到 `0.0.0.0:<port>`，但用户需要的是可被外部访问的 URL。大多数部署平台会将该地址注入到运行环境中——建议通过搜索查找，而非让用户自行寻找。

```bash
env | grep -iE "HERMES_DASHBOARD_PUBLIC_URL|RAILWAY_PUBLIC_DOMAIN|RAILWAY_STATIC_URL|RAILWAY_SERVICE_.*_URL|PUBLIC_URL|BASE_URL|DOMAIN" \
  | sed -E 's/(TOKEN|SECRET|KEY|PASSWORD)=.*/\1=***REDACTED***/I'
```

当 `HERMES_DASHBOARD_PUBLIC_URL` 被设置时，其值具有权威性。在 Railway 环境中，还需检查 `RAILWAY_PUBLIC_DOMAIN`/`RAILWAY_STATIC_URL`（即 `*.up.railway.app` 这类主机地址）以及 `RAILWAY_SERVICE_*_URL` 这些环境变量，因为它们有时会使用更友好的自定义域名。请将完整的 `https://` 链接提供给用户，并引导他们前往 Connectors/MCP 部分。务必先通过上述的 `sed` 命令进行敏感信息遮蔽处理——因为这些环境变量往往与 `*_TOKEN`/`*_SECRET` 变量处于同一位置。

**仪表板无法解决的問題（仍属于主机端/Shell 层面）：** 需要 Shell 认证状态的 stdio 服务器（即那些凭据可能在重启后丢失的 CLI `login` 命令），以及任何从 `$HERMES_HOME/.env` 文件中读取凭据的程序。无论如何，这些都属于仪表板的功能范畴之外。

## 替代解决方案

手动完成 OAuth 认证流程，然后将生成的令牌写入 Hermes 的 `HermesTokenStorage` 本应写入的文件中。这样一来，当执行 `/reload-mcp` 指令时，Hermes 就能找到已缓存的令牌，从而完全跳过浏览器端的认证流程。

在网关主机上通过 `terminal` 工具运行以下 Shell 命令，再通过 `execute_code` 或直接调用 `terminal python3` 来执行 Python 代码中的相关操作（如 PKCE 令牌生成、令牌交换及文件写入）。注意，文件写入操作必须与令牌交换操作放在同一个代码块中（参见问题 16）。

### 1. 确认当前为远程网关

```bash
env | grep -iE "HERMES|RAILWAY|CONTAINER"
echo "$DISPLAY $WAYLAND_DISPLAY $SSH_CLIENT"
```

无显示界面且带有远程指示灯的状态即代表为远程网关。`tools/mcp_oauth.py::_can_open_browser()`函数也会使用这些相同的环境变量，因此如果Hermes自身的自动检测功能判定为“无头模式”，则内置的流程将无法正常运行。

### 2. 查找HERMES_HOME及配置文件路径

```bash
HERMES_HOME=$(python3 -c 'from hermes_constants import get_hermes_home; print(get_hermes_home())')
echo "config: $HERMES_HOME/config.yaml"
echo "tokens: $HERMES_HOME/mcp-tokens/"
```

### 3. 从MCP服务器获取OAuth元数据

MCP服务器会通过RFC 9728标准（OAuth 2.0受保护资源元数据）来公开其OAuth配置信息。401响应中的`WWW-Authenticate`请求头会指示您应在何处查找这些信息：

```bash
curl -sI https://mcp.example.com | grep -i www-authenticate
# → Bearer realm="mcp", resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource"
```

**并非所有服务器都会返回 `WWW-Authenticate` 头信息。** 有些服务器会直接返回仅包含 `{"errors":["Unauthorized"]}` 的 401 响应，且不提供任何身份验证相关的提示。遇到这种情况时，应直接探测常见的路径：

```bash
for p in \
  /.well-known/oauth-protected-resource \
  /.well-known/oauth-authorization-server \
  /.well-known/openid-configuration ; do
  echo "=== $p ==="
  curl -s -A "python-httpx/0.27" "https://mcp.example.com$p" | head -c 400; echo
done
```

首先获取资源元数据以获得 `authorization_servers`，随后读取 AS 的 `/.well-known/oauth-authorization-server` 文件，从而获取 `authorization_endpoint`、`token_endpoint` 和 `registration_endpoint`。

注意事项：许多服务器位于 Cloudflare 后端，会导致使用纯 `urllib` 用户代理时出现 403 错误。在此流程中的请求中，务必设置 `User-Agent: python-httpx/0.27`（或类似值）。

### 4. 动态客户端注册（RFC 7591）

向 `registration_endpoint` 发送 POST 请求，内容如下：

```json
{
  "client_name": "Hermes Agent (manual OAuth)",
  "redirect_uris": ["http://127.0.0.1:8765/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "scope": "<scopes_from_resource_metadata>"
}
```

如果 AS 的 `scopes_supported` 为空，则完全无需包含 `scope` 参数——请参考第 5 步中的注意事项。可使用端口 `8765`（或任意端口，因为不会有其他程序监听该端口）。将 `token_endpoint_auth_method` 设置为 `none` 即可标识该客户端为公共 PKCE 客户端，请保存返回的 `client_id`。

### 5. 使用 PKCE 构建授权 URL

需要生成以下内容：
- `code_verifier`：`secrets.token_urlsafe(64)[:128]`
- `code_challenge`：`base64url(sha256(code_verifier))`（无需添加填充字符）
- `state`：`secrets.token_urlsafe(24)`

查询参数包括：`response_type=code`、`client_id`、`redirect_uri`、`code_challenge`、`code_challenge_method=S256`、`state`，以及 `resource=<mcp_server_url>`（符合 RFC 8707 标准——许多服务器要求此参数以便将令牌与特定的 MCP 资源关联）。仅当 AS 元数据的 `scopes_supported` 是非空数组，且/或资源元数据指定了特定作用域时，才需添加 `scope=<以空格分隔的作用域列表>` 参数。如果 `scopes_supported: []`，则应省略 `scope` 参数——服务器会自动授予其完整的默认作用域集。在 `scopes_supported` 为空的情况下随意构造作用域字符串，可能会导致某些 AS 返回 `invalid_scope` 错误。

请将 `code_verifier` 和 `state` 的值保存到磁盘上（例如路径为 `/tmp/.mcp-oauth-work/<server>.json`，权限设置为 0600）。第 7 步需要使用这些数据，且可能在多轮对话中都需要。

### 6. 将授权 URL 提供给用户

```
Open this URL in your browser:
<authorize_url>

After approving, your browser will try to load http://127.0.0.1:8765/callback
and fail to connect — THAT'S EXPECTED. Just copy the entire URL from the
address bar (it will contain ?code=...&state=...) and paste it back here.
```

### 7. 将代码转换为令牌

当用户粘贴回调 URL 后：

1. 从查询字符串中解析出 `code` 和 `state`。
2. **验证 `state` 是否与之前保存的值一致**（这是 CSRF 防护措施，切勿跳过）。
3. 使用 `application/x-www-form-urlencoded` 格式向 `token_endpoint` 发送 POST 请求，需包含以下参数：
   - `grant_type=authorization_code`
   - `code=<来自回调的代码>`
   - `redirect_uri=<与第4步相同的值>`
   - `client_id=<第4步中设置的值>`
   - `code_verifier=<之前保存的值>`
   - `resource=<mcp_server_url>`（如果认证服务在第5步中要求提供该参数，也需在此处包含）
4. 响应中会返回 `access_token`、`refresh_token`、`token_type`、`expires_in` 以及 `scope` 等信息。

### 8. 按 Hermes 的规范格式存储令牌

`tools/mcp_oauth.py::HermesTokenStorage` 要求在 `$HERMES_HOME/mcp-tokens/` 目录下创建两个文件（该目录权限需设置为 `0o700`，文件权限则需设置为 `0o600`）：

**`<server_name>.json`** — 用于存储 `OAuthToken` pydantic 模型的数据：
```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 7200,
  "refresh_token": "...",
  "scope": "read write"
}
```

**`<server_name>.client.json`** — 即 `OAuthClientInformationFull` 模型：
```json
{
  "client_id": "...",
  "redirect_uris": ["http://127.0.0.1:8765/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "scope": "read write",
  "client_name": "..."
}
```

请使用 `json.dumps(..., indent=2)` 的方式来编写每个文件。同时需通过 `re.sub(r'[^\w\-]', '_', server_name)[:128]` 对文件名进行净化处理——该操作方式与 Hermes 令牌存储机制中的 `_safe_filename()` 函数一致。

### 9. 将服务器信息添加到 config.yaml 文件中

```yaml
mcp_servers:
  <name>:
    url: "https://mcp.example.com"
    auth: oauth
    timeout: 180
    connect_timeout: 60
```

### 10. 在要求用户重新加载之前先对令牌进行测试

手动发送一个MCP `initialize`请求，以确认令牌在整个流程中都能正常工作——这样就能在用户因再次出现“暂无可用MCP工具”的提示而感到困惑之前，及时发现作用域配置错误、`resource`值不正确以及CF拦截器等问题。

```python
body = json.dumps({
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "hermes-debug", "version": "1.0"},
    },
}).encode()
# POST to the MCP URL with:
#   Authorization: Bearer <access_token>
#   Accept: application/json, text/event-stream
#   Content-Type: application/json
#   MCP-Protocol-Version: 2025-06-18
#   User-Agent: python-httpx/0.27
```

系统将返回状态码为 200 的 HTTP 响应，其 `Content-Type` 字段值为 `text/event-stream`，响应体中包含包含 `serverInfo` 和 `capabilities` 字段的 JSON-RPC 结果。**请勿使用默认 UA 的 `urllib` 库**——即便 Hermes（它使用的是 httpx 库）能够正常工作，Cloudflare 仍会拒绝请求并返回 403 错误。`scripts/diagnose-oauth-mcp.py` 脚本可用于自动执行此功能测试。

### 11. 告知用户运行 `/reload-mcp` 命令

在重新加载后，Hermes 会识别到 `auth: oauth` 的配置，随即调用 `HermesTokenStorage.get_tokens()` 方法获取已缓存的令牌，从而跳过浏览器验证流程，并注册 `mcp_<name>_*` 类型的工具。在令牌有效期结束之前，系统会自动触发刷新操作。

## 常见问题与经验总结

1. **切勿认为“无头模式”就意味着无法使用 OAuth**。对于本地 CLI 环境，内置的认证流程完全可以正常工作；问题主要出现在远程部署场景中，即用户的浏览器与 Hermes 进程运行在不同的机器上。在断言 OAuth 不可用之前，请先确认具体的执行环境。

2. **应查阅源代码而不仅仅是技能文档**。`tools/mcp_oauth.py` 文件以及 `website/docs/` 目录中的 MCP 配置参考资料才是最权威的依据。在告知用户某项功能“不存在”之前，建议先通过搜索工具查看相关代码实现。

3. **Cloudflare 的 UA 过滤机制**。许多 MCP/OAuth 服务提供商会使用 Cloudflare 作为其基础设施的前端代理，而该代理即便面对公开接口，也会对带有 `python-urllib/*` UA 字符串的请求返回 403 错误。因此，在此类请求中，需在每个请求中设置 `User-Agent: python-httpx/0.27`（或任何类似浏览器的字符串）。由于 Hermes 本身使用的是 httpx 库，所以在实际的连接流程中不会遇到此问题。

4. **在授权请求和令牌请求中均需包含 `resource` 参数。** 对于大多数现代 MCP 服务器而言，RFC 8707 规定的资源标识符并非可选项——它们用于将生成的令牌与特定的 MCP 资源 URL 关联起来。虽然有时省略该参数也能正常工作，但这样生成的令牌日后在 MCP 服务器端可能会因范围/授权主体错误而失效。

5. **末尾的斜杠非常重要。** 某些服务器会将资源地址标识为带有末尾斜杠的 `https://mcp.example.com/` 格式，并拒绝使用无斜杠版本生成的令牌。请直接从 `.well-known/oauth-protected-resource` 的响应中复制 `resource` 值。

6. **`/reload-mcp` 命令在失败时不会输出任何提示信息。** 如果重新加载后仅显示“没有可用的 MCP 工具”，且没有 `change_detail` 字段，说明服务器配置虽已正确，但未能建立连接，且未出现任何错误提示。此时应查看错误日志，通过手动发送 `initialize` POST 请求对令牌进行直接测试；如果一切正常，再请求彻底重启整个进程。

7. **熔断机制可抵御 `/reload-mcp` 操作。** `tools/mcp_tool.py` 会维护一个模块级的错误计数字典，并设置较低的阈值。一旦触发熔断（例如令牌过期导致连续多次失败），工具处理程序会在调用服务器之前直接中断流程，因此成功的调用不会重置该计数器。出现的症状是：虽然重新连接后显示“已重新连接：X”，但在同一对话中后续调用仍会因“无法访问服务器”而失败。恢复步骤为：首先尝试执行 `/reload-mcp`（成本较低，且不会影响聊天流程）——在当前版本中该操作即可清除计数器；只有在对系统进行重新加载后，实时调用依然中断时，才需要进一步重启整个网关进程。切勿直接告知用户“必须重启”。

8. **令牌过期且熔断已触发时的刷新操作会导致死锁。** 自动刷新逻辑运行在MCP调用路径中，而一旦熔断机制被触发，该路径就会立即中断。仅手动刷新磁盘中的令牌并不能解决问题——应结合完整重启操作来处理令牌刷新，而非使用 `/reload-mcp`。

9. **手动刷新时出现 `invalid_grant` 错误，意味着刷新令牌已失效——此时唯一的解决办法是重新进行身份验证，切勿陷入循环尝试。** 当访问令牌过期时间过长时，服务器端也可能会撤销或使刷新令牌失效。此时使用 `grant_type=refresh_token` 发送的请求将会返回 HTTP 400 错误响应，内容为 `{"error":"invalid_grant",...}`（具体表述可能有所不同，如“未找到授权信息”、“令牌已过期”或“刷新令牌无效”）。网关端无法对此进行任何修复操作。应将问题反馈给用户，并提供两种解决方案：(a) 重新执行完整的 OAuth 手动认证流程（步骤 3–10）；(b) 如果服务提供商提供了静态个人 API 密钥，可切换使用该密钥——由于无需经历刷新或过期机制，因此更适用于无人值守的远程网关。建议尽早进行检测：在对 OAuth MCP 执行任何创建/更新操作之前，先检查 `expires_at` 的时间值与当前时间 `time.time()` 的关系；若令牌已过期，应首先尝试刷新令牌，并立即显示 `invalid_grant` 错误，而非在操作中途直接失败。

10. **即使刷新成功，但获取的令牌仍被拒绝，这说明是服务器端会话已被撤销；唯有通过全新的授权码流程才能解决此问题。** 这与问题9不同。虽然存储的令牌文件看似正常（`expires_at`时间远未到期且包含`refresh_token`），但在执行实时`initialize` POST请求时仍会返回`401 invalid_token`错误，其JSON-RPC响应内容类似`{"error":{"code":-32002,"message":"Session expired. Please re-authenticate."}}`。使用`grant_type=refresh_token`的POST请求虽可能**成功**（返回HTTP 200状态码并生成新的`access_token`），但这个新令牌也会出现同样的`-32002`错误。实际上，服务提供商已在服务器端撤销了底层的MCP *会话*；OAuth刷新机制虽然可以重新生成凭证，却无法恢复已被撤销的会话。当OAuth MCP报告“未连接”时，可遵循以下处理规则：(1) 通过手动执行`initialize` POST请求来测试存储的`access_token`是否有效；(2) 若返回`401 invalid_token`错误，则尝试刷新并测试新生成的令牌；(3a) 新令牌可用 → 将其保存下来并重启服务以解除故障状态；(3b) 新令牌仍出现`-32002`错误或“会话已过期”提示 → 应立即停止操作，因为这是会话被撤销的情况，需将授权URL提供给用户以便其重新进行认证。脚本`scripts/diagnose-oauth-mcp.py`可自动执行步骤1–2，并显示当前所处的处理分支。对于那些会话不断被撤销且无人值守的网关，建议使用静态个人API密钥。有关服务提供商每周主动撤销会话的实际示例，请参阅`references/stripe-mcp-oauth-revocation.md`。

11. **客户端信息文件并非可选项。** Hermes 需要 `<server>.client.json` 文件才能获取用于刷新授权的 `client_id`。若省略该文件，首次刷新将会失败，用户必须重新进行身份验证——而编写这两个文件的初衷正是为了解决这一问题。

12. **切勿让用户手动输入需要打开的重定向地址。** 应通过 `urllib.parse.urlencode()` 以编程方式生成授权 URL。作用域中的空格以及 `state` 参数中的特殊字符都可能导致通过字符串拼接生成的 URL 出现错误。

13. **安全性考虑：临时存储文件中包含 `code_verifier`。** 在成功完成令牌交换后，应立即删除 `/tmp/.mcp-oauth-work/<server>.json` 文件。一旦该身份验证凭证已被使用，便无需再保留它。

14. **需记录令牌接口实际返回的内容。** 认证服务提供商可能会授予比请求更窄（或更宽）的作用域。应将从令牌交换响应中获取的 `scope` 值写入 `<server>.json` 文件，而非第 5 步中所指定的内容。当 `scopes_supported: []` 时，您所提交的明确作用域列表在双方均具有权威性：有些服务器会严格遵循您列出的范围（通过限制作用域来实现最小权限原则，或在用户需要全部功能时列出完整范围）；而有些服务器在注册阶段不会反馈已授予的作用域——唯有令牌交换响应才是具有权威性的依据。

15. **OAuth令牌通常也可用作访问提供商公开REST API的Bearer令牌。** `<server>.json` 文件中的 `access_token` 往往并非仅限于MCP使用——只要获得了相应的资源权限，使用 `Authorization: Bearer <token>` 访问提供商官方文档中规定的REST API即能成功。这是OAuth 2.0规范的要求，并非特定提供商的特殊设定。如果MCP服务器为只读模式而你需要执行写入操作，建议先确认该OAuth令牌是否可以直接调用提供商的REST API，再考虑使用独立的API密钥。

16. **敏感信息掩码功能可能会在工具输出中隐藏令牌。** 若启用了敏感信息掩码功能，令牌及过长的加密字符串会在工具输出结果中显示为 `***`，因此你无法通过 `print(response)` 的方式让 `access_token` 在多轮对话中保持可见。再加上基于授权码流程获得的单次有效 `code` 值：如果你打印了令牌交换的响应，不仅可能会丢失令牌，还会同时消耗掉该 `code`，迫使你必须使用新的授权URL重新开始流程。**务必在执行令牌交换的同一代码块中，将 `access_token` 直接写入目标文件。** 如果确实需要打印内容用于调试，也仅应输出 `len(access_token)`、`token_type`、`scope`、`expires_in` 等信息，绝不能包含任何敏感内容。

17. **GitHub MCP（`api.githubcopilot.com/mcp/`）使用的是预先注册的机密 OAuth 应用，而非 DCR + PKCE-public 方式。** 其客户端配置中会包含真实的 `client_secret`，且 `token_endpoint_auth_method` 的值为 `client_secret_post`。向 `https://github.com/login/oauth/access_token` 发送获取令牌的 POST 请求时，除了 `client_id`、`code`、`code_verifier` 和 `redirect_uri` 外，还必须将 `client_secret` 作为表单字段一并提交（PKCE 机制仍会在该机密信息的基础上继续生效）。OAuth 应用配置中的 `redirect_uri` 是**固定不可修改**的，因此无法使用手动调整监听端口的技巧；用户只需让浏览器尝试连接该端口失败后，再将地址栏中的网址重新粘贴即可。

## 不应采取的做法

- **切勿将 `mcp-remote` 作为备用方案。** 它会启动一个通过 npx 调用的子进程，而该子进程的 OAuth 回调服务器同样位于远程容器的本地主机上，问题依然存在。只有当 MCP 客户端完全不支持远程 HTTP 接口时（而 Hermes 本身已原生支持），`mcp-remote` 才能发挥作用。
- **如果用户明确要求使用 OAuth，就不要提议“粘贴您的 API 令牌，我会帮您添加请求头”**。只有在解释了为何在远程环境中原生 OAuth 流程无法正常工作时，才可提供静态令牌的快捷方式。应尊重用户为获得无需定期更换且权限范围受限的访问权限而愿意多花些功夫的选择。
- **在未查看源代码之前，切勿断言 Hermes 不支持某项功能**。在宣称某功能不可用之前，务必先对源代码树进行搜索确认。

## 快速参考文件

- `scripts/diagnose-oauth-mcp.py` — 该脚本可重复运行，默认为只读模式。输入服务器名称后，它会先对已存储的访问令牌进行功能测试，尝试刷新令牌并再次进行测试，最后明确指出当前所处的恢复流程分支（`TOKEN_OK` = 继续运行/重启，`REFRESH_FIXED` = 保留令牌后重启，`SESSION_REVOKED` = 需要完全重新认证，`REFRESH_DEAD` = 需要完全重新认证或更换API密钥）。若需以原子方式保存有效的刷新后令牌，可添加`--write`参数。该脚本绝不会输出任何敏感信息。**当OAuth MCP服务器报告“未连接”时，请首先运行此脚本**——它涵盖了问题7、9和10对应的决策流程。
- `references/stripe-mcp-oauth-revocation.md` — 一个基于Stripe的实际案例，展示了如何让服务提供商定期撤销其OAuth会话，以及相应的持久解决方案：改用静态的受限API密钥。

## 相关内容

- `native-mcp` — Hermes中MCP配置的通用指南，权威的配置参考资料也位于此处。
- `mcporter` — 用于在Hermes配置之外进行临时MCP调用的外部CLI桥接工具。
