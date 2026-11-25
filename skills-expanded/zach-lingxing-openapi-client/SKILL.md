---
name: zach-lingxing-openapi-client
description: |
  搭建并复用领星 ERP OpenAPI 接入底座，处理 token、sign、店铺/站点映射、文档缓存与基础烟测。
  使用时机：准备接入领星接口、编写依赖领星数据的新 skill、或排查领星 OpenAPI 鉴权与请求问题。
  触发词：/zach-lingxing-openapi-client
benefits-from: []
user-invocable: true
allowed-tools: Read, Glob, Bash, Write, Edit, Grep
risk-level: low
---

> **本机直连停用 / 固定出口模式可用**：领星 OpenAPI 因 IP 白名单限制，本地环境无法直接访问。
> 如已部署固定出口网关并将 `EIP` 加入白名单，可继续使用本 Skill。
> 未部署前，需要亚马逊经营数据时请优先改用 Amazon SP-API（MCP: `amazon-api`）。

> 本公开版 Skill 是自包含的，不依赖任何私有工作区文件、内部协议或团队手册。

# 领星 OpenAPI 客户端底座

## 核心功能

1. 统一管理 `access_token` 获取与续约
2. 按官方规则生成 `sign`
3. 封装 GET/POST 业务请求
4. 缓存关键官方文档到本地
5. 运行最小烟测，确认 `SellerLists -> StoreSales -> Orderlists -> promotionListingList` 链路可用
6. 给领星 MCP 和其他 skill 提供共享服务层

## 环境变量

| 变量名 | 必需 | 说明 |
|---|---|---|
| `LINGXING_APP_ID` | 是 | 领星开放接口 App ID |
| `LINGXING_APP_SECRET` | 是 | 领星开放接口 App Secret |
| `LINGXING_TOKEN_CACHE_FILE` | 否 | token 缓存文件路径，默认 `runtime/lingxing/token_cache.json` |
| `LINGXING_DOC_ACCESS_KEY` | 否 | 文档同步时使用的文档密钥 |

## Script Directory

脚本位于 `skills/zach-lingxing-openapi-client/scripts/`：

- `lingxing_client.py`：兼容入口，实际复用 `lib/lingxing_openapi/client.py`
- `timezone_map.py`：兼容入口，实际复用 `lib/lingxing_openapi/timezones.py`
- `sync_docs.py`：从官方 `_sidebar.md` 自动发现并同步 Amazon 相关只读文档到 `references/openapi_docs/`
- `smoke_check.py`：最小链路烟测

共享代码位于 `lib/lingxing_openapi/`：

- `client.py`：鉴权、续约、签名、统一请求封装
- `services.py`：店铺、销量、订单、促销等业务型封装
- `promotions.py`：促销标签与窗口归一化
- `errors.py`：统一错误与提示
- `mcp.py`：MCP 工具注册、stdio/HTTP 传输层

## 本地文档缓存

同步命令：

```bash
python3 skills/zach-lingxing-openapi-client/scripts/sync_docs.py
```

同步结果会写入：

```text
skills/zach-lingxing-openapi-client/references/openapi_docs/
```

会保留现有 12 页兼容文件名，并自动扩展更多 Amazon 相关只读页面。兼容页包括：

- GetToken
- RefreshToken
- SellerLists
- AllMarketplace
- StoreSales
- AsinDailyLists
- Orderlists
- promotionListingList
- promotionalActivitiesSecKillList
- promotionalActivitiesManageList
- promotionalActivitiesVipDiscountList
- promotionalActivitiesCouponList

## 使用方法

### 场景 1：给其他 skill 复用

直接在 Python 脚本中导入：

```python
from lib.lingxing_openapi import LingxingOpenAPIClient, LingxingOpenAPIService
```

### 场景 2：同步本地文档

```bash
export LINGXING_DOC_ACCESS_KEY="你的文档密钥"
python3 skills/zach-lingxing-openapi-client/scripts/sync_docs.py
```

### 场景 3：烟测

```bash
export LINGXING_APP_ID="ak_xxx"
export LINGXING_APP_SECRET="xxx"
python3 skills/zach-lingxing-openapi-client/scripts/smoke_check.py
```

## 公共规则

1. 所有业务接口使用 `https://openapi.lingxing.com`
2. 所有业务接口都要带 `access_token / app_key / timestamp / sign`
3. `sign` 生成规则严格按官方说明：
   - 所有业务参数 + 3 个公共参数一起参与签名
   - ASCII 排序
   - 空字符串不参与，`null` 参与
   - 拼接后先做 `MD5(32位大写)`
   - 再用 `appId` 做 `AES/ECB/PKCS5PADDING`
   - 最终作为 Query 参数传输时 URL encode

## 输出

- 本地 references 文档缓存
- token 缓存文件
- 烟测 JSON 输出

## 依赖环境

- Python 3.11+
- 系统自带 `openssl`

## 风险与边界
- **risk-level: low** — 只做接口接入和鉴权配置，不写入业务数据

## 上游 / 下游
- **上游**：无（基础底座 Skill，需要配置环境变量）
- **下游**：`zach-lingxing-mcp`（MCP 服务层）以及其他依赖领星数据的脚本或 Skill

## 完成后
报告完成状态：DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT
