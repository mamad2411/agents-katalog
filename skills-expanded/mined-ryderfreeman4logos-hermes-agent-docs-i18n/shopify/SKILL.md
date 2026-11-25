---
name: shopify
description: Query Shopify Admin/Storefront GraphQL APIs via curl.
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [SHOPIFY_ACCESS_TOKEN, SHOPIFY_STORE_DOMAIN]
  commands: [curl, jq]
required_environment_variables:
  - name: SHOPIFY_ACCESS_TOKEN
    prompt: Shopify Admin API access token (starts with shpat_)
    help: "Shopify admin → Settings → Apps and sales channels → Develop apps → Create an app → API credentials. Token shown ONCE on install."
  - name: SHOPIFY_STORE_DOMAIN
    prompt: Your shop subdomain without protocol (e.g. my-store.myshopify.com)
    help: "The permanent myshopify.com domain, not your custom domain."
  - name: SHOPIFY_API_VERSION
    prompt: Shopify API version (default 2026-01)
    help: "Stable quarterly version. Override if you need an older one."
metadata:
  hermes:
    tags: [Shopify, E-commerce, Commerce, API, GraphQL]
    related_skills: [airtable, xurl]
    homepage: https://shopify.dev/docs/api/admin-graphql
---

# Shopify — 管理后台与店铺前端 GraphQL API

您可以直接通过 `curl` 命令与 Shopify 店铺进行交互：列出商品、管理库存、获取订单信息、更新客户资料以及读取元数据。无需 SDK 也不用任何应用框架，只需使用 GraphQL 接口端点以及自定义应用的访问令牌即可。

自 2024 年 4 月起，REST 管理后台 API 已被标记为旧版本，仅会接收安全补丁。**所有管理操作请使用 GraphQL 管理 API**；而针对仅用于读取的、面向客户端的查询（如商品、系列、购物车信息），则请使用**店铺前端 GraphQL API**。

## 前提条件

1. 进入 Shopify 管理后台：**设置 → 应用与销售渠道 → 开发应用 → 创建应用**。
2. 点击**配置管理后台 API 权限范围**，选择所需功能（下方有示例），然后保存。
3. **安装应用**——此时管理后台 API 的访问令牌将仅显示一次，请立即复制，因为 Shopify 不会再次展示该令牌。令牌的起始字符为 `shpat_`。
4. 将该令牌保存到 `${HERMES_HOME:-~/.hermes}/.env` 文件中：
   ```
   SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxx
   SHOPIFY_STORE_DOMAIN=my-store.myshopify.com
   SHOPIFY_API_VERSION=2026-01
   ```

> **重要提示：** 自 2026 年 1 月 1 日起，通过 Shopify 管理后台创建的旧版“自定义应用”将不再存在。新项目应使用 **开发控制台**（`shopify.dev/docs/apps/build/dev-dashboard`）进行搭建。现有通过管理后台创建的应用仍可正常使用。如果用户的店铺在 2026-01-01 之后且没有自定义应用，建议引导其直接使用开发控制台，而非传统的管理后台流程。

不同任务对应的常用权限范围：
- 产品/系列：`read_products`、`write_products`
- 库存：`read_inventory`、`write_inventory`、`read_locations`
- 订单：`read_orders`、`write_orders`（可读取最近 30 笔订单，不可使用 `read_all_orders`）
- 客户：`read_customers`、`write_customers`
- 草稿订单：`read_draft_orders`、`write_draft_orders`
- 配送信息：`read_fulfillments`、`write_fulfillments`
- 元字段/元对象：由对应的资源权限范围覆盖

## API 基础知识

- **端点地址：** `https:// $SHOPIFY_STORE_DOMAIN/admin/api/$SHOPIFY_API_VERSION/graphql.json`  
- **认证头信息：** `X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN`（而非 `Authorization: Bearer`）  
- **请求方法：** 始终使用 `POST`，内容类型固定为 `application/json`，请求体格式为 `{"query": "...", "variables": {...}}`  
- **HTTP 200 状态码并不代表操作成功。** GraphQL 会将错误信息分别放在顶层 `errors` 数组以及各字段对应的 `userErrors` 中，务必同时检查这两部分内容。  
- **ID 为 GID 格式的字符串：** `gid://shopify/Product/10079467700516`、`gid://shopify/Variant/...`、`gid://shopify/Order/...`。请原样传递这些字符串，切勿删除前缀部分。  
- **速率限制机制：** 根据查询成本通过“漏桶算法”进行计算。每个响应都会包含 `extensions.cost` 字段，其中列有 `requestedQueryCost`、`actualQueryCost` 以及 `throttleStatus.{currentlyAvailable, maximumAvailable, restoreRate}` 等信息。当 `currentlyAvailable` 的值低于下一次查询所需的成本时，应暂停请求以等待恢复。普通店铺的速率限制为 100 点/次，恢复速率为 50 次/分钟；Plus 计划的速率限制为 1000 点/次，恢复速率为 100 次/分钟。  

可复用的基础 curl 请求模板：

```bash
shop_gql() {
  local query="$1"
  local variables="${2:-{}}"
  curl -sS -X POST \
    "https://${SHOPIFY_STORE_DOMAIN}/admin/api/${SHOPIFY_API_VERSION:-2026-01}/graphql.json" \
    -H "Content-Type: application/json" \
    -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
    --data "$(jq -nc --arg q "$query" --argjson v "$variables" '{query: $q, variables: $v}')"
}
```

通过 `jq` 处理输出以便更易于阅读。选项 `-sS` 可让错误信息保持显示，同时隐藏进度条。

## 发现功能

### 商店信息与当前 API 版本
```bash
shop_gql '{ shop { name myshopifyDomain primaryDomain { url } currencyCode plan { displayName } } }' | jq
```

### 列出所有受支持的 API 版本
```bash
shop_gql '{ publicApiVersions { handle supported } }' | jq '.data.publicApiVersions[] | select(.supported)'
```

## 产品

### 搜索产品（显示前20个匹配结果）
```bash
shop_gql '
query($q: String!) {
  products(first: 20, query: $q) {
    edges { node { id title handle status totalInventory variants(first: 5) { edges { node { id sku price inventoryQuantity } } } } }
    pageInfo { hasNextPage endCursor }
  }
}' '{"q":"hoodie status:active"}' | jq
```

查询语法支持使用 `title:`、`sku:`、`vendor:`、`product_type:`、`status:active`、`tag:` 以及 `created_at:>2025-01-01` 等条件。完整的语法规范请参见：https://shopify.dev/docs/api/usage/search-syntax

### 按页加载商品（游标方式）
```bash
shop_gql '
query($cursor: String) {
  products(first: 100, after: $cursor) {
    edges { cursor node { id handle } }
    pageInfo { hasNextPage endCursor }
  }
}' '{"cursor":null}'
# subsequent calls: pass the previous endCursor
```

### 获取包含变体及元字段的产品
```bash
shop_gql '
query($id: ID!) {
  product(id: $id) {
    id title handle descriptionHtml tags status
    variants(first: 20) { edges { node { id sku price compareAtPrice inventoryQuantity selectedOptions { name value } } } }
    metafields(first: 20) { edges { node { namespace key type value } } }
  }
}' '{"id":"gid://shopify/Product/10079467700516"}' | jq
```

### 创建仅包含一个变体的产品
```bash
shop_gql '
mutation($input: ProductCreateInput!) {
  productCreate(product: $input) {
    product { id handle }
    userErrors { field message }
  }
}' '{"input":{"title":"Test Hoodie","status":"DRAFT","vendor":"Hermes","productType":"Apparel","tags":["test"]}}'
```

在最新版本中，变体现已拥有独立的突变功能。

```bash
# Add variants after creating the product
shop_gql '
mutation($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkCreate(productId: $productId, variants: $variants) {
    productVariants { id sku price }
    userErrors { field message }
  }
}' '{"productId":"gid://shopify/Product/...","variants":[{"optionValues":[{"optionName":"Size","name":"M"}],"price":"49.00","inventoryItem":{"sku":"HD-M","tracked":true}}]}'
```

### 更新价格/SKU信息
```bash
shop_gql '
mutation($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id sku price }
    userErrors { field message }
  }
}' '{"productId":"gid://shopify/Product/...","variants":[{"id":"gid://shopify/ProductVariant/...","price":"55.00"}]}'
```

## 订单

### 查看近期订单（默认显示最近30笔订单，如使用`read_all_orders`参数则可查看全部）
```bash
shop_gql '
{
  orders(first: 20, reverse: true, query: "financial_status:paid") {
    edges { node {
      id name createdAt displayFinancialStatus displayFulfillmentStatus
      totalPriceSet { shopMoney { amount currencyCode } }
      customer { id displayName email }
      lineItems(first: 10) { edges { node { title quantity sku } } }
    } }
  }
}' | jq
```

实用的订单查询筛选条件包括：`financial_status:paid|pending|refunded`、`fulfillment_status:unfulfilled|fulfilled`、`created_at:>2025-01-01`、`tag:gift` 以及 `email:foo@example.com`。

### 获取包含配送地址的单个订单信息
```bash
shop_gql '
query($id: ID!) {
  order(id: $id) {
    id name email
    shippingAddress { name address1 address2 city province country zip phone }
    lineItems(first: 50) { edges { node { title quantity variant { sku } originalUnitPriceSet { shopMoney { amount currencyCode } } } } }
    transactions { id kind status amountSet { shopMoney { amount currencyCode } } }
  }
}' '{"id":"gid://shopify/Order/...."}' | jq
```

## 客户端

```bash
# Search
shop_gql '
{
  customers(first: 10, query: "email:*@example.com") {
    edges { node { id email displayName numberOfOrders amountSpent { amount currencyCode } } }
  }
}'

# Create
shop_gql '
mutation($input: CustomerInput!) {
  customerCreate(input: $input) {
    customer { id email }
    userErrors { field message }
  }
}' '{"input":{"email":"test@example.com","firstName":"Test","lastName":"User","tags":["api-created"]}}'
```

## 库存管理

库存以与具体规格版本关联的**库存条目**形式存在，同时还会按**存储位置**记录相应的数量。

```bash
# Get inventory for a variant across all locations
shop_gql '
query($id: ID!) {
  productVariant(id: $id) {
    id sku
    inventoryItem {
      id tracked
      inventoryLevels(first: 10) {
        edges { node { location { id name } quantities(names: ["available","on_hand","committed"]) { name quantity } } }
      }
    }
  }
}' '{"id":"gid://shopify/ProductVariant/..."}'
```

调整库存（增量）——使用 `inventoryAdjustQuantities` 功能：

```bash
shop_gql '
mutation($input: InventoryAdjustQuantitiesInput!) {
  inventoryAdjustQuantities(input: $input) {
    inventoryAdjustmentGroup { reason changes { name delta } }
    userErrors { field message }
  }
}' '{
  "input": {
    "reason": "correction",
    "name": "available",
    "changes": [{"delta": 5, "inventoryItemId": "gid://shopify/InventoryItem/...", "locationId": "gid://shopify/Location/..."}]
  }
}'
```

设置绝对库存量（而非变动量）——`inventorySetQuantities`：

```bash
shop_gql '
mutation($input: InventorySetQuantitiesInput!) {
  inventorySetQuantities(input: $input) {
    inventoryAdjustmentGroup { id }
    userErrors { field message }
  }
}' '{"input":{"reason":"correction","name":"available","ignoreCompareQuantity":true,"quantities":[{"inventoryItemId":"gid://shopify/InventoryItem/...","locationId":"gid://shopify/Location/...","quantity":100}]}}'
```

## 元字段与元对象

元字段用于为资源（产品、客户、订单、店铺）添加自定义数据。

```bash
# Read
shop_gql '
query($id: ID!) {
  product(id: $id) {
    metafields(first: 10, namespace: "custom") {
      edges { node { key type value } }
    }
  }
}' '{"id":"gid://shopify/Product/..."}'

# Write (works for any owner type)
shop_gql '
mutation($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { id key namespace }
    userErrors { field message code }
  }
}' '{"metafields":[{"ownerId":"gid://shopify/Product/...","namespace":"custom","key":"care_instructions","type":"multi_line_text_field","value":"Wash cold. Tumble dry low."}]}'
```

## Storefront API（公共只读版）

该版本使用独立的接口端与令牌，专为面向客户的应用程序及 Hydrogen 风格的无头架构设计。其请求头也有所不同：

- **接口地址：** `https:// $SHOPIFY_STORE_DOMAIN/api/$SHOPIFY_API_VERSION/graphql.json`
- **公共认证请求头：** `X-Shopify-Storefront-Access-Token: <公共令牌>` —— 可嵌入浏览器中使用
- **私有认证请求头：** `Shopify-Storefront-Private-Token: <私有令牌>` —— 仅服务器端可使用

```bash
curl -sS -X POST \
  "https://${SHOPIFY_STORE_DOMAIN}/api/${SHOPIFY_API_VERSION:-2026-01}/graphql.json" \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Storefront-Access-Token: ${SHOPIFY_STOREFRONT_TOKEN}" \
  -d '{"query":"{ shop { name } products(first: 5) { edges { node { id title handle } } } }"}' | jq
```

## 批量操作

针对超过速率限制规模的导出数据（如完整产品目录、全年的所有订单）：

```bash
# 1. Start bulk query
shop_gql '
mutation {
  bulkOperationRunQuery(query: """
    { products { edges { node { id title handle variants { edges { node { sku price } } } } } } }
  """) {
    bulkOperation { id status }
    userErrors { field message }
  }
}'

# 2. Poll status
shop_gql '{ currentBulkOperation { id status errorCode objectCount fileSize url partialDataUrl } }'

# 3. When status=COMPLETED, download the JSONL file
curl -sS "$URL" > products.jsonl
```

每行 JSONL 数据代表一个节点，而嵌套关系则会通过添加 `__parentId` 字段以独立行形式呈现。如有需要，可在客户端进行重新组合。

## Webhooks

订阅事件即可，无需手动轮询：

```bash
shop_gql '
mutation($topic: WebhookSubscriptionTopic!, $sub: WebhookSubscriptionInput!) {
  webhookSubscriptionCreate(topic: $topic, webhookSubscription: $sub) {
    webhookSubscription { id topic endpoint { __typename ... on WebhookHttpEndpoint { callbackUrl } } }
    userErrors { field message }
  }
}' '{"topic":"ORDERS_CREATE","sub":{"callbackUrl":"https://example.com/webhook","format":"JSON"}}'
```

请使用应用程序的客户端密钥（而非访问令牌）来验证传入的 Webhook HMAC。

```bash
echo -n "$REQUEST_BODY" | openssl dgst -sha256 -hmac "$APP_SECRET" -binary | base64
# Compare to X-Shopify-Hmac-Sha256 header
```

## 常见问题与陷阱

- **REST 接口虽存在但已停止使用。** 请勿再为 `/admin/api/.../products.json` 开发新的集成，应改用 GraphQL。
- **令牌格式检查。** 管理员令牌以 `shpat_` 开头，而店铺公开令牌则以 `shpua_` 开头。如果使用了错误前缀的令牌，所有请求都会返回 401 错误，且不会附带有用的错误信息。
- **使用有效令牌仍出现 403 错误 = 缺少权限范围。** Shopify 会返回 `{"errors":[{"message":"Access denied for ..."}]}`。此时需在应用中重新配置管理 API 的权限范围，然后重新安装应用以生成新的令牌。
- **`userErrors` 为空并不代表操作成功。** 还需检查 `data.<mutation>.<resource>` 是否非空。某些错误情况下这两项都会为空，因此需要仔细查看整个响应内容。
- **GID 与数字 ID 的区别。** 旧版 REST 接口返回的是数字 ID，而 GraphQL 要求使用完整的 GID 字符串。转换方法为：`gid://shopify/Product/<numeric>`。
- **速率限制的意外影响。** 单次调用 `products(first: 250)` 且嵌套层级较深时，可能会消耗 1000 多个积分，导致标准套餐的店铺立即被限流。建议先缩小查询范围，查看 `extensions.cost` 的数值后再进行调整。
- **分页顺序问题。** `products(first: N, reverse: true)` 是按 `id` 从大到小排序，而非按创建时间排序。如需按“最新优先”排序，应使用 `sortKey: CREATED_AT, reverse: true`。
- **获取历史数据时需使用 `read_all_orders`。** 若不添加此权限范围，`orders(...)` 查询将默认仅返回最近 60 天内的订单数据。虽然不会报错，但返回的结果数量会少于预期。对于拥有大量订单的 Shopify Plus 商家，可通过应用的保护数据设置来申请该权限范围。
- **货币类型为字符串格式**。金额将以 `"49.00"` 的形式返回，而非 `49.0`。如果需要确保数值始终带有足够位数，请勿盲目使用 `jq tonumber` 函数进行处理。
- **多货币金额字段**同时包含 `shopMoney`（店铺使用的货币）和 `presentmentMoney`（客户看到的货币）。请统一选择其中一种格式进行使用。

## 安全性

在 Shopify 中执行的操作都是真实有效的——它们会创建产品、处理退款、取消订单以及安排发货。在运行 `productDelete`、`orderCancel`、`refundCreate` 或任何批量操作之前，务必明确说明要进行的更改内容、涉及的店铺，并获得用户确认。除非用户拥有独立的开发商店，否则系统中不存在与生产环境数据分离的测试环境副本。
