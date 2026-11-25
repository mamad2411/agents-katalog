---
name: configure-mcp
description: "配置 MCP 服务的标准流程：Hermes 原生 vs mcporter 两种路径，诊断连接问题，Header / 认证 / 传输方式配置，以及渐进式加载 vs 全量注入的取舍。"
version: 1.0.0
---

# 配置 MCP 服务

给 Hermes 接入外部 MCP 服务的标准流程。核心认知：**不是所有 MCP 服务都适合用 Hermes 原生客户端**。

## 两条路径

| | Hermes 原生 MCP | mcporter |
|---|---|---|
| 配置位置 | `config.yaml` → `mcp_servers` | `/opt/data/config/mcporter.json` |
| 工具加载 | **启动时全量注入**，所有会话可见 | **按需调用**，像 Skill 一样渐进式 |
| 上下文开销 | 工具 schema 占常驻 token | 零常驻开销 |
| 适合场景 | 少量轻量工具（如 time、filesystem） | 大量复杂工具、重型 schema |
| 客户端 | Python `mcp` 包 | Node.js mcporter CLI |

**核心判断**：工具多（5+）或 schema 重（嵌套复杂）→ 用 mcporter。工具少且简单 → 用原生。

## 路径 A：Hermes 原生 MCP

### 配置格式

```yaml
mcp_servers:
  service-name:
    url: "https://example.com/mcp"       # HTTP/SSE
    # 或
    command: "npx"                        # stdio
    args: ["-y", "package-name"]

    headers:                              # HTTP 专用
      Authorization: "Bearer <token>"
    timeout: 180
    connect_timeout: 60
```

### 添加方式

```bash
# CLI 方式（仅适用于命令型 / 无Header型）
hermes mcp add <name> --url <url>
hermes mcp add <name> --command npx --args -y pkg-name

# 需要自定义 Header 时，直接编辑 config.yaml
hermes config edit
```

### 验证

```bash
hermes mcp list          # 查看所有已配置
hermes mcp test <name>   # 测试连接
```

### 生效

修改 `config.yaml` 后需重启 gateway，或在会话中执行 `/reload-mcp`。

## 路径 B：mcporter（推荐用于重型 MCP）

### 安装

```bash
npm install -g mcporter
export PATH="$PATH:$(npm root -g)/../bin"
```

### 配置

```bash
mcporter config add <name> \
  --url "https://..." \
  --header "Authorization=Bearer <token>"
```

配置保存在 `/opt/data/config/mcporter.json`。

### 发现工具

```bash
mcporter list <name> --schema    # 列出所有工具及参数 schema
mcporter list <name> --json      # JSON 格式输出
```

### 调用工具

```bash
mcporter call <name>.<tool> key1=value1 key2=value2

# 示例
mcporter call myservice.findPosts limit=10 sort=-createdAt
mcporter call myservice.createPosts title="标题" slug="slug" ...
```

参数用 `key=value` 格式，空格分隔。值中的引号、花括号需要 shell 转义。

## 诊断连接问题

### 预热检查：curl 直连

```bash
# 1. 先测 MCP 握手
curl -s -X POST "https://HOST/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer <token>" \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"hermes","version":"1.0"}}}'

# 2. 检查是否返回 serverInfo（说明握手成功）
```

### 常见问题速查

| 现象 | 根因 | 解决 |
|------|------|------|
| Hermes 原生 `tools/list` 返回 -32601 | Python mcp 包与服务端不兼容（常见于 mcp-typescript + Vercel） | **换 mcporter** |
| curl 返回 406 | 缺少 `Accept: text/event-stream` 头 | 加上 Accept 头 |
| curl 返回 403 | Cloudflare 拦截（Python 默认 UA） | 加 `User-Agent: Mozilla/5.0` |
| mcporter 首次慢 5-10s | Vercel serverless 冷启动 | 正常，后续秒回 |
| `Method not found` 但握手成功 | 服务端未注册任何工具，或需要 session | 检查 Bearer token 是否有效；用 mcporter 重试 |
| mcporter: command not found | npm 全局 bin 不在 PATH | `export PATH="$PATH:$(npm root -g)/../bin"` |

### 诊断脚本模板

```python
import json, urllib.request, ssl

ctx = ssl.create_default_context()
base = "https://HOST/mcp"
token = "Bearer <token>"

def mcp(method, params=None, call_id=1):
    payload = {"jsonrpc":"2.0","id":call_id,"method":method,"params":params or {}}
    data = json.dumps(payload).encode()
    r = urllib.request.Request(base, data=data, method="POST")
    r.add_header("Content-Type", "application/json")
    r.add_header("Accept", "application/json, text/event-stream")
    r.add_header("User-Agent", "Mozilla/5.0")
    r.add_header("Authorization", token)
    with urllib.request.urlopen(r, timeout=15, context=ctx) as resp:
        body = resp.read().decode()
        for line in body.split('\n'):
            if line.startswith('data: '):
                return json.loads(line[6:])

# 1. 握手
init = mcp("initialize", {"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"hermes","version":"1.0"}})
print("Server:", init.get("result",{}).get("serverInfo",{}))

# 2. 已初始化通知
mcp("notifications/initialized", call_id=None)

# 3. 列出工具
tools = mcp("tools/list")
for t in tools.get("result",{}).get("tools",[]):
    print(f"  {t['name']}: {t.get('description','')[:80]}")
```

## Hermes 原生 vs mcporter：决策树

```
工具数 < 5 且 schema 简单？
  ├── 是 → Hermes 原生 MCP
  │        直接写入 config.yaml
  │        启动时自动注入
  │
  └── 否 → mcporter
            npm install -g mcporter
            mcporter config add ...
            Hermes 中通过 terminal 调用
```

## 避坑

- **不要混用**：同一个服务要么用原生要么用 mcporter，不要两边都配
- **PATH 持久化**：mcporter 装完后把 PATH 写进 `.bashrc`，否则每次新 terminal 找不到
- **Token 轮换**：`mcporter.json` 和 `config.yaml` 里的 token 不会自动轮换，需要手动更新
- **Hermes 原生重载**：`/reload-mcp` 在 gateway 中可用，CLI 需要重启进程
- **Vercel 不适合 MCP**：serverless 10s 超时与 MCP 长连接协议矛盾，优先用非 serverless 部署（Dokploy、VPS）

## Payload CMS 内容发布

当 MCP 后端是 Payload CMS 时，`createPosts` / `updatePosts` 的 `content` 字段使用 Lexical Rich Text 格式。详见 `references/payload-lexical-format.md`。

关键点：每个节点必须有 `version` 字段；代码块内容在单个 text child 中；shell 传参时用临时文件避免转义问题。
