---
name: api-doc-output
pack: universal
description: 改动 HTTP/RPC 接口时强制同步更新接口文档——落点见项目 AGENTS.md「目录结构」节，记录路径、方法、入参/出参、错误码、鉴权要求。
when_to_use: 新增/修改/删除任何对外接口、请求或响应结构、错误码时。
when_NOT_to_use: 仅内部函数重构、不影响对外契约。
---

# Skill: 接口文档产出

改接口必须同步更新对应服务的接口文档（落点见项目 AGENTS.md「目录结构」节），否则 CI 拦截。

## 每个接口需记录

1. 路径 + 方法 + 简述
2. 鉴权要求（是否需登录、需要的权限）
3. 入参（字段、类型、必填、约束）
4. 出参（成功结构，金额字段注明为 `string` 类型）
5. 错误码与含义

## 文档路径规则

接口文档的落点**由各项目自定义**，写在项目 `AGENTS.md` 的「目录结构」节 / 文档同步表里；按该表把改动的服务映射到对应文档。两种常见组织：

```
# 扁平（默认模板）
docs/api/<service>.md                  services/matching-engine/ → docs/api/matching-engine.md
docs/api/web.md                        前端对后端的接口依赖（可选）

# 按服务分目录（服务名可读、可含空格）
docs/services/<服务名>/api.md   cmd/matching-engine/ → docs/services/Matching Engine/api.md
```

> 找不到项目约定时，用扁平默认 `docs/api/<service>.md`。

## 格式模板

```markdown
## POST /v1/orders

**鉴权:** Bearer token（需 `orders:write` 权限）

**入参:**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| market_id | string (ULID) | ✓ | 交易市场 ID |
| side | enum: buy\|sell | ✓ | 方向 |
| price | string (Decimal18) | ✓ | 限价，单位与 market 精度一致 |
| quantity | string (Decimal18) | ✓ | 数量 |

**出参（200）:**
```json
{ "order_id": "01HXZ...", "status": "pending" }
```

**错误码:**
- `400 INVALID_PRICE` — 价格精度超限
- `403 FORBIDDEN` — 权限不足
```

## 反模式
- ❌ 改了响应字段不更新文档（前端按旧契约对接 → 线上故障）
- ❌ 金额字段写 `number` 类型（应为 `string`，禁止前端浮点）
- ❌ 新增接口没有错误码说明
