---
name: zach-lingxing-mcp
description: |
  负责配置、排查和使用领星 ERP OpenAPI 的 MCP 服务，支持本地 stdio 与团队 HTTP 两种形态。
  使用时机：需要把领星接口接成 MCP、检查工具是否可用、或排查 Bearer/鉴权/配置问题。
  触发词：/zach-lingxing-mcp
benefits-from: []
user-invocable: true
allowed-tools: Read, Glob, Bash, Write, Edit, Grep
risk-level: low
---

> **本机直连停用 / 固定出口模式可用**：领星 OpenAPI 因 IP 白名单限制，本地环境无法直接访问。
> 如已部署固定出口网关并将 `EIP` 加入白名单，可继续使用本 Skill。
> 未部署前，需要亚马逊经营数据时请优先改用 Amazon SP-API（MCP: `amazon-api`）。

> 本公开版 Skill 是自包含的，不依赖任何私有工作区文件或内部协议。

# 领星 MCP 运维 Skill

## 核心用途

- 配置固定出口网关上的领星 MCP
- 配置带 Bearer 的团队 `HTTP` 版领星 MCP
- 配置 Tailscale + SSH Tunnel 访问
- 了解有哪些 `lingxing_*` 工具可调用
- 排查环境变量、Bearer、权限、授权有效期和 IP 白名单问题

## 关键位置

- `mcp-servers/lingxing-openapi/server.py`
- `mcp-servers/lingxing-openapi/http_server.py`
- `mcp-servers/lingxing-openapi/README.md`
- `mcp-servers/lingxing-openapi/deploy/`
- `lib/lingxing_openapi/mcp.py`

## 环境变量

- `LINGXING_APP_ID`
- `LINGXING_APP_SECRET`
- `LINGXING_TOKEN_CACHE_FILE`
- `LINGXING_MCP_BEARER_TOKEN`
- `LINGXING_MCP_HOST`
- `LINGXING_MCP_PORT`

## 常用命令

```bash
python3 mcp-servers/lingxing-openapi/server.py
python3 mcp-servers/lingxing-openapi/http_server.py --host 127.0.0.1 --port 8099
python3 skills/zach-lingxing-openapi-client/scripts/smoke_check.py
bash mcp-servers/lingxing-openapi/deploy/deploy_gateway_via_ssh.sh --help
bash mcp-servers/lingxing-openapi/deploy/install_tailscale_via_ssh.sh --help
bash mcp-servers/lingxing-openapi/deploy/install_tailscale_on_ubuntu.sh --help
bash mcp-servers/lingxing-openapi/deploy/open_ssh_tunnel.sh --help
bash mcp-servers/lingxing-openapi/deploy/install_gateway_on_ubuntu.sh --help
```

## 工具清单

- `lingxing_health_check`
- `lingxing_seller_lists`
- `lingxing_marketplaces`
- `lingxing_store_sales`
- `lingxing_asin_daily_lists`
- `lingxing_product_performance`
- `lingxing_orders`
- `lingxing_promotion_listing`
- `lingxing_promotion_sec_kill`
- `lingxing_promotion_manage`
- `lingxing_promotion_vip_discount`
- `lingxing_promotion_coupon`
- `lingxing_resolve_daily_promotions`
- `lingxing_ad_accounts`
- `lingxing_ads_sp_*`
- `lingxing_ads_sd_*`
- `lingxing_ads_sb_*`
- `lingxing_profit_seller`
- `lingxing_profit_asin`
- `lingxing_profit_parent_asin`
- `lingxing_source_*`
- `lingxing_fba_*`
- `lingxing_replenishment_*`
- `lingxing_report_export_*`
- `lingxing_asin_ads_daily_rollup`
- `lingxing_asin_weekly_rollup`
- `lingxing_exp_*`
- `lingxing_smoke_check`

## 排错原则

1. 先跑 `lingxing_health_check` 看环境变量和 token
2. 再跑 `lingxing_smoke_check` 看 `SellerLists -> StoreSales -> Orderlists -> promotionListingList`
3. 如果是 `403`，优先回到领星后台检查授权有效期、接口权限和 IP 白名单
4. 如果是 HTTP 模式报 `missing_or_invalid_bearer`，只看 Bearer Token，不要先怀疑领星接口

## 风险与边界
- **risk-level: low** — 只做 MCP 服务配置和排查，不写入业务数据

## 上游 / 下游
- **上游**：`zach-lingxing-openapi-client`（API 鉴权底座）
- **下游**：所有依赖领星 MCP 工具的 Skill（`zach-lingxing-sales-anomaly-monitor` 等）

## 完成后
报告完成状态：DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT
