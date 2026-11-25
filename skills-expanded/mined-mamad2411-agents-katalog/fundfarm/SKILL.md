---
name: fundfarm
description: 如何将养基场 MCP Server 接入 AI 智能体（OpenClaw、Claude Desktop、Cursor 等）
---

# 养基场 MCP Server 接入指南

## 快速连接

### MCP Server 地址

```
https://api.myfundfarm.com/mcp
```

协议: SSE (Server-Sent Events)，标准 MCP 协议。

> ⚠️ **重要：如果你是 MCP 客户端（OpenClaw、Claude Desktop、Cursor、Gemini CLI 等），直接将上面的地址配置为 MCP Server 连接即可。OAuth 授权会自动弹出浏览器完成，不要手动拼授权 URL。**

---

## 连接方式

### 各客户端配置

**OpenClaw**

OpenClaw 通过插件系统支持 MCP。在 MCP 设置或 `~/.openclaw/openclaw.json` 中添加养基场 MCP Server：
```
https://api.myfundfarm.com/mcp
```
首次连接会自动弹出浏览器完成 OAuth 授权。

**Claude Desktop**

从 Claude 设置 → Connectors，添加自定义 MCP Server，URL 填：
```
https://api.myfundfarm.com/mcp
```

**Claude Code**

```bash
claude mcp add --transport http fundfarm https://api.myfundfarm.com/mcp
```
然后在会话中运行 `/mcp` 完成认证。

**Cursor**

在 Cursor 设置 → MCP → Add Server，Server URL 填：
```
https://api.myfundfarm.com/mcp
```

**VS Code / Windsurf**

在 MCP 配置文件中添加：
```json
{
  "mcpServers": {
    "fundfarm": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.myfundfarm.com/mcp"]
    }
  }
}
```

**Gemini CLI**

```bash
gemini mcp add fundfarm --url https://api.myfundfarm.com/mcp
```

**其他支持 MCP 的 Agent**

通用配置，只需填入 Server URL：
```
https://api.myfundfarm.com/mcp
```
协议: SSE，认证: OAuth 2.1（自动完成）。

> 所有客户端首次连接时会自动弹出浏览器，在养基场页面点击「授权」即可。Token 自动保存和续期，无需手动操作。
>
> **授权后取得授权码的方法：** 用户点击「授权」后，页面会直接展示授权码并提供「复制授权码」按钮。用户点击复制按钮，将授权码粘贴给你即可。不需要从 URL 中提取 code 参数。

### API Key（备选方式）

适用于：不支持 MCP 协议的 Agent、自建 Agent、或想跳过 OAuth 流程的场景。

**用户操作：** 登录 [养基场](https://myfundfarm.com) → 设置 → AI 智能体 → 点击「生成 API Key」→ 复制 Key → 粘贴给 Agent

**Agent 使用方式：** 在所有请求 Header 中携带：
```
Authorization: Bearer <用户提供的 API Key>
```

> API Key 有效期 90 天，过期后用户重新生成即可。每次生成新 Key 旧的自动失效。

### 方式三: 手动 OAuth2（自行开发 MCP 客户端时参考）

仅在自己用 MCP SDK 开发客户端时需要了解。普通接入无需阅读本节。

**关键端点：**

| 端点 | 地址 |
|------|------|
| 服务发现 | `https://api.myfundfarm.com/.well-known/oauth-authorization-server` |
| 授权页面 | `https://myfundfarm.com/#/oauth/authorize` |
| Token 端点 | `https://api.myfundfarm.com/api/v1/oauth/token` |
| 撤销端点 | `https://api.myfundfarm.com/api/v1/oauth/revoke` |

**可用的 client_id：**

| client_id | 适用 Agent |
|---|---|
| `claude-desktop` | Claude Desktop |
| `claude-code` | Claude Code (CLI) |
| `chatgpt-desktop` | ChatGPT Desktop |
| `cursor-ide` | Cursor |
| `windsurf-ide` | Windsurf |
| `gemini-cli` | Gemini CLI |
| `openclaw` | OpenClaw |
| `generic-mcp` | 其他未列出的 Agent |

> 所有 client_id 均为公开标识符（无 client_secret）。Access Token 有效期 1 小时，Refresh Token 30 天有效。

---

## 可用工具（26个）

连接后通过 MCP 协议自动发现，以下是完整列表供参考：

### 📊 基金查询
| 工具 | 说明 | 关键参数 |
|------|------|---------|
| `search_funds` | 搜索基金 | `keyword`, `limit` |
| `get_fund_detail` | 基金详情 | `fund_code` |
| `get_fund_nav_history` | 历史净值 | `fund_code`, `days` |
| `get_fund_top_holdings` | 重仓股 | `fund_code` |
| `get_fund_sector_allocation` | 行业配置 | `fund_code` |
| `get_fund_estimate` | 盘中估值 | `fund_code` |
| `get_fund_ranking` | 排行榜 | `sort_by`, `order`, `limit` |

### 📈 市场数据
| 工具 | 说明 |
|------|------|
| `get_market_indices` | 大盘指数行情 |
| `get_sector_ranking` | 板块涨跌排名 |
| `get_market_status` | 交易状态 |

### 👤 用户持仓
| 工具 | 说明 |
|------|------|
| `get_my_holdings` | 持仓及收益 |
| `get_my_watchlist` | 自选基金 |
| `get_portfolio_summary` | 组合概览 |
| `get_my_sectors` | 板块分布 |
| `get_my_nests` | 鸡窝列表 |
| `get_transactions` | 交易流水（可按基金代码/鸡窝筛选） |

### 🤖 AI 分析
| 工具 | 说明 |
|------|------|
| `get_latest_ai_report` | 最新分析报告 |
| `run_ai_analysis` | 运行 AI 分析（消耗额度） |

### ✏️ 写操作
| 工具 | 限制 |
|------|------|
| `add_to_watchlist` | |
| `remove_from_watchlist` | |
| `add_holding` | 单笔买入 |
| `batch_add_holdings` | 单次最多50笔，仅算1次写操作 |
| `import_holding` | 导入单个持仓（市值+收益），不需要构造买入交易 |
| `batch_import_holdings` | 批量导入持仓（最多50条） |
| `sell_holding` | 单次≤50%持仓 |
| `delete_transaction` | 只能删除 Agent 创建的记录，并自动回滚持仓 |

写操作限制：每日≤30次，每分钟≤10次。

---

## 可用 Scopes

| Scope | 说明 |
|-------|------|
| `fund:read` | 基金信息和市场数据（10个工具） |
| `portfolio:read` | 持仓、自选、交易流水（6个工具） |
| `portfolio:write` | 管理持仓/自选、撤销交易（6个工具） |
| `ai:read` | AI 分析报告（1个工具） |
| `ai:execute` | 运行 AI 分析（1个工具） |

---

## 典型对话

```
用户: 今天大盘怎么样 → get_market_indices
用户: 查一下 161725 → get_fund_detail("161725")
用户: 看看我的基金 → get_my_holdings
用户: 分析一下我的持仓 → run_ai_analysis 或 get_my_holdings + 自行分析
用户: 把 161725 加到自选 → add_to_watchlist("161725")
```

## 安全

- Token 绑定用户，只能访问自己的数据
- 写操作有白名单 + 量控
- 所有调用有审计日志

## Token 生命周期与持续连接

OAuth2 授权只需一次，之后 Token 自动续期，无需用户反复操作。

### Token 有效期

| Token | 有效期 | 说明 |
|-------|--------|------|
| Access Token | **1 小时** | 每次 MCP 调用携带的令牌 |
| Refresh Token | **30 天** | 用来自动换取新的 Access Token |
| API Key | **90 天** | 长期有效，无需续期逻辑 |

### 使用官方 MCP SDK（推荐，自动续期）

如果使用官方 MCP SDK（Python `mcp` 包 / TypeScript `@modelcontextprotocol/sdk`），Token 续期是**全自动**的，无需编写任何刷新逻辑：

**Python:**
```python
from mcp.client import ClientSession
from mcp.client.sse import sse_client

async with sse_client("https://api.myfundfarm.com/mcp") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # SDK 自动完成：OAuth2 授权 → 存储 Token → Access Token 过期时自动用 Refresh Token 续期
        tools = await session.list_tools()
        result = await session.call_tool("get_market_indices", {})
```

**TypeScript:**
```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const transport = new SSEClientTransport(
  new URL("https://api.myfundfarm.com/mcp")
);
const client = new Client({ name: "my-agent", version: "1.0" });
await client.connect(transport);
// SDK 自动处理 OAuth2 授权和 Token 刷新
```

SDK 在首次连接时会：
1. 自动读取 `.well-known/oauth-authorization-server` 发现端点
2. 弹出浏览器让用户点击「授权」（仅首次）
3. 存储 Access Token + Refresh Token
4. Access Token 过期后自动用 Refresh Token 换新的（用户无感）
5. 30 天内持续有效，无需重新授权

### 自行实现 HTTP 调用（手动处理续期）

如果不使用 MCP SDK，而是直接发 HTTP 请求调用 `/mcp/*` 接口，需要自行处理 Token 刷新：

**1. 首次授权后，保存两个 Token：**
```json
{
  "access_token": "xxx...",
  "refresh_token": "yyy...",
  "expires_in": 3600
}
```

**2. 调用 MCP 工具时，如果收到 401，用 Refresh Token 换新的 Access Token：**
```
POST https://api.myfundfarm.com/api/v1/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token=yyy...&client_id=你的client_id
```

**3. 用返回的新 Access Token 替换旧的，重试原请求。**

> 只要 Refresh Token 不过期（30天），就不需要用户重新授权。如果不想处理续期逻辑，建议改用 API Key 方式。

---

## 已知的客户端兼容性说明

### Authorization 头的标准行为

按照 HTTP 标准，**每一个独立的 HTTP 请求都应该携带 Authorization 头**。MCP SSE 协议的请求分为两类：

| 请求 | 说明 | 应该带 Authorization？ |
|------|------|----------------------|
| `GET /mcp` | 建立 SSE 长连接 | ✅ 是 |
| `POST /mcp/messages/` | 每次工具调用 | ✅ 是（标准要求） |

### OpenClaw / 部分客户端的已知 Bug

**现象：** 部分 MCP 客户端（包括早期版本的 OpenClaw）只在建立 SSE 连接时带了 Authorization 头，后续每次调用工具时（POST /mcp/messages/）不带该头，导致服务端返回 `401 未认证`，工具调用失败。

**官方标准：** MCP 规范要求客户端在 GET 和 POST 上都带 Authorization，OpenClaw 当前行为不符合规范，属于客户端 bug。

**服务端兼容方案（已实现）：** 养基场后端部署了 `MCPSessionAuthMiddleware` 中间件：
1. 捕获 `GET /mcp` 时的 Authorization 头，与客户端 IP 临时绑定缓存
2. 当 `POST /mcp/messages/` 没有带 Authorization 时，自动从缓存中补上对应的 Token

因此，即使客户端行为不规范，**工具调用也能正常鉴权**（服务端自动兜底）。

### 排查 MCP 认证失败

如果工具调用返回 401，按以下顺序排查：

1. **直接 curl 测试 API Key 是否有效：**
   ```bash
   curl -H "Authorization: Bearer <你的API Key>" https://api.myfundfarm.com/api/v1/mcp/market/status
   ```
   返回 `{"code": 0, ...}` 说明 API Key 本身没问题，是客户端没带头。

2. **查看后端日志：**
   ```bash
   journalctl -u fund-backend --since "10 min ago" | grep -E "MCP session|Error calling|401"
   ```
   如果看到 `✅ MCP session xxx... 已绑定 Authorization` → 中间件补丁生效  
   如果看到 `Error calling xxx. Status code: 401` → 中间件没补到（可能 IP 不匹配）

3. **多 worker 说明（可以放心）：** 虽然后端运行 2 个 uvicorn worker，但 MCP session 的 `GET /mcp`（建立 SSE 连接）和 `POST /mcp/messages/`（工具调用）由于 SSE 协议特性，`POST` 必须携带正确的 `session_id`，若该 `session_id` 不在目标 worker 的内存中，uvicorn 会直接返回 `404`。因此能成功处理 POST 的 worker 一定和处理 GET 是同一个，内存缓存中间件不存在竞争问题，是安全的。

---

## 数据新鲜度

基金净值和估值的时间线：

| 时段 | `nav_date` | `latest_nav` | `estimate_change_pct` |
|------|-----------|-------------|----------------------|
| 盘中（9:30-15:00） | 昨天 | 昨天的确认净值 | 实时估值涨跌幅 |
| 盘后等待（15:00-19:00） | 昨天 | 昨天的确认净值 | 收盘估值涨跌幅 |
| 净值公布后（~19:00+） | 今天 | 今天的确认净值 | 自动退化为实际值 |

**判断方法：** 用 `nav_date` 与今天日期比较。如果 `nav_date < 今天`，说明今日净值尚未公布，`estimate_change_pct` 是盘中预估值。

`get_my_holdings` 每只持仓返回 `estimate_change_pct`（估值涨跌幅）、`estimate_time`（估值更新时间）、`today_profit_estimate`（预估今日盈亏元），汇总层也有 `today_profit_estimate`（全部持仓预估总盈亏）。
