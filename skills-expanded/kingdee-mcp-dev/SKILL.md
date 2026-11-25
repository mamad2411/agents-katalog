---
name: kingdee-mcp-dev
description: |
  Knowledge base for the Kingdee MCP Dev Squad. Covers how to integrate the Kingdee Cloud Star OpenAPI (ApiDoc) interfaces into the kingdee-mcp Python+FastMCP project: WebAPI login/metadata caching, field-discovery SOP, 二开 (customized) bill pitfalls, and the ApiDoc coverage tracking template.
metadata:
  version: "1.0.0"
---

# 金蝶 MCP 开发团 · 知识库

本 Skill 是 `kingdee-mcp-dev` 专家团的共享知识底座，供主理人（龚联达）与四位团员（范探源 / 寇豆码 / 严过关 / 温书成）在协作时查阅。目标是**把金蝶开放平台 ApiDoc 的全部接口集成进 `D:\AI\projects\kingdee-mcp`**。

## 项目事实（已实证，勿凭记忆）

- **源码位置**：`D:\AI\projects\kingdee-mcp`，Python + FastMCP。
- **工具规模**：`src/kingdee_mcp/server.py` 当前 **97 个 `@mcp.tool`**（2026-08-07 实测 97；本日新增 6 个标准动作通用工具 `kingdee_cancel_bills` / `kingdee_void_bills` / `kingdee_close_bill` / `kingdee_unclose_bill` / `kingdee_forbid_bills` / `kingdee_enable_bills`，覆盖 14/15 标准动作；报表由 `kingdee_query_report` 覆盖；覆盖 13 大业务域 + 4 个 SQL Server 探查）。
- **构建后端**：`hatchling`（`python -m build`），`dist/` 产物 `kingdee_mcp-0.2.0-py3-none-any.whl` / `.tar.gz`。
- **运行环境**：金蝶 K3Cloud `http://<K3Cloud-Server>/k3cloud/`，账套 `<ACCT_ID>`（<公司名>）。
- **登录方式**：仅账号密码（`ValidateUser`），无第三方应用授权；配置 `KINGDEE_SERVER_URL` / `KINGDEE_ACCT_ID` / `KINGDEE_USERNAME` / `KINGDEE_PASSWORD`。
- **WebAPI 权限拒绝**返回 `[[{'Result':{报错}}]]`（r[0][0] 是 dict），正常数据返回 `[[值,...]]`（r[0][0] 是标量）—— 写查询脚本务必用此区分，否则会把错误当数据。

## ApiDoc 结构（浏览器实测）

`https://openapi.open.kingdee.com/ApiDoc` 是 Element UI(el-tree) SPA，需真实浏览器爬取。结构为 **16 业务领域 → 77 模块 → 操作（标准金蝶 WebAPI 动作集）**：

- 16 业务领域：员工服务、财务会计、税务管理、成本管理、资产管理、管理会计、供应链、电商与分销、零售管理、生产制造、质量管理、星空云服务、基础管理、BOS、移动应用、PLM。
- 标准操作动作（每个单据模块通用）：保存 / 提交 / 审核 / 反审核 / 撤销 / 下推 / 作废 / 整单关闭 / 反关闭 / 批量保存 / 单据查询 / 查看 / 暂存 / 删除，外加部分领域专属动作（如费用类「申请单退款」）。
- 原始抓取树见 `references/api-inventory-raw.json`（领域→模块已全量；操作级仅在「员工服务」域完整抓取，其余域操作需逐模块切换抓取）。

## 集成工作流（团队 SOP 映射）

| 阶段 | 负责团员 | 关键动作 | 输入 → 输出 |
|------|----------|----------|-------------|
| 探字段 / WebAPI 映射 | 范探源 | `kingdee_get_fields` 探 FormId 与字段 Key；映射 ApiDoc 操作到 `Save/Submit/Audit/Push/ExecuteBillQuery` | 任务 → 字段/操作映射表 |
| 实现 `@mcp.tool` | 寇豆码 | 复用提速工具，落地工具代码 | 映射表 → 工具签名 |
| 测试回归 | 严过关 | `bin/kmcp test` + 用例；区分权限拒绝 vs 正常数据 | 工具签名 → 回归报告 |
| 文档 / 发布 | 温书成 | 更新 `docs/`、`mcp_optimization_notes.md`、CHANGELOG；`bin/kmcp build` → `twine upload` → Pages | 变更 → 发布清单 |

## 提速工具（已落地 server.py，优先复用）

- `kingdee_validate_bill`：保存前校验，返回 `auto_fixes / missing_required / entry_issues / suggestions`，**不真正保存**。
- `kingdee_get_bill_template`：取已验证 model 骨架，支持 `SAL_Quotation` / `SAL_SaleOrder` / `PUR_PurchaseOrder`。
- `kingdee_refresh_metadata`：强制刷新元数据。
- 元数据已落盘缓存到 `~/.workbuddy/kingdee_metadata_cache/`。

**推荐工作流**：`get_bill_template → 填数 → validate_bill → save_bill`。

## 必读参考

- `references/webapi-login-cache.md` — 金蝶 WebAPI 登录机制、元数据缓存读取与刷新。
- `references/field-discovery-sop.md` — `kingdee_get_fields` 探字段的标准操作流程与返回解析。
- `references/ercustom-pitfalls.md` — 本环境二开单据坑（SAL_SaleOrder 二开、TRNV_Receipt/PaymentSlip、FCUSTID 全大写、FBaseUnitId 等）。
- `references/apidoc-coverage-template.md` — ApiDoc 覆盖进度跟踪表模板，配合 `bin/kmcp coverage` 使用。
- `references/avoid-duplication.md` — **防止重复开发红线**：通用/专用工具清单 + 决策树 + `bin/kmcp tools` 查重用法。开工前必读。

## 助手命令（bin/kmcp）

团队配套 CLI `bin/kmcp`：

- `bin/kmcp test` — 跑 `evals/` + `tests/` 回归（连真实金蝶环境）。
- `bin/kmcp build` — `python -m build` 构建 wheel / sdist。
- `bin/kmcp list-tools` — 统计 `@mcp.tool` 数量。
- `bin/kmcp coverage` — 对照 `references/api-inventory-raw.json` 输出 ApiDoc 覆盖进度。
