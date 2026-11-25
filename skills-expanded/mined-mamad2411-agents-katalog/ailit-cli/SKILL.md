---
name: ailit-cli
description: Use when an agent needs to perform 智慧记AI进销存 business operations via the local `ailit` CLI — including customer/product/account search, sale order management, stock queries, purchase records, sales reports, and debt analysis, especially in non-TTY environments where multi-result selection or resumable login may be needed.
---

# Ailit CLI

Use the local `ailit` command as the primary interface for 智慧记AI进销存 operations.

## Core rules

### Auth & health

- Default to the browser authorization flow. When the CLI is not logged in, guide the user to run `ailit auth login` instead of manually writing `token` into config.
- Run `ailit doctor` before business commands when config health is unknown.
- Do not default to `ailit config set token ...` as the repair path.

### Output & format

- Prefer the default table or pretty output for user-facing calls.
- Use `--format json` only when the agent needs machine-readable output for parsing or troubleshooting.
- If the CLI returns a friendly Chinese error, reuse it instead of rewriting the meaning.
- Do not expose token values, `pay_records`, raw stack traces, or internal IDs unless they are needed for troubleshooting.

### Search & selection

- For customer, product, and account lookup, never guess when multiple results are returned.
- In machine-readable mode, search commands may return `selection_required` with `resultSetId`, `items[].selectToken`, and structured candidate display data.
- When `selection_required` is returned, show the user the numeric `selectToken`, `displayName`, and `items[].fields` first. Use `summary` only as a compatibility fallback, then continue with `--result-set <id> --select <selectToken>`.
- When `selection_validated` is returned, confirm the choice with `displayName` and `fields`. Do not tell end users "商品 ID 已确认" unless they explicitly asked for IDs.
- Never execute follow-up business actions by visual row order alone. Map the user choice back to `selectToken` or stable ID first.
- For product search, after `selection_validated`, extract from the response directly — do NOT call `ailit product get` again if all needed fields are present:
  - `validatedItems[0].meta.productId` → use as `lines[].productId`
  - `validatedItems[0].meta.productSkuId` → use as `lines[].productSkuId`
  - `validatedItems[0].meta.retailPrice` → reference price
  - `validatedItems[0].displayName` → use as `lines[].productName`

Current candidate field conventions:

- Product: `displayName` is the product name; `fields` include spec, barcode, retail price, and wholesale price.
- Customer: `displayName` is the customer name; `fields` include phone and current debt.
- Account: `displayName` is the account name; `fields` include current balance.

### Mutation safety

- For sale creation, always run `ailit sale create --json <file> --dry-run` first. The default output is now a user-facing draft summary. Add `--format json` only when the raw request payload is needed.
- Do not run a real sale creation command until the user explicitly confirms.
- For create, update, delete, invalidate, restore, and similar business operations, prefer user-facing success fields such as bill code, customer name, and product name. Do not default to raw numeric IDs in end-user confirmations.
- When a mutating command succeeds and no human-friendly identifier is available, fall back to a generic success message instead of exposing the numeric ID.
- If creation fails, report the CLI error and stop. Do not auto-retry create operations.
- For sale invalidation or deletion, always run `ailit sale get <id>` first to confirm the bill code and amount with the user before executing.
- In non-TTY login flows, `ailit auth login --non-interactive --format json` may return a resumable workflow response with `workflowId`, `step`, `resultSetId`, and candidate `items`.
- When login returns a resumable workflow, continue with `ailit auth login --resume <workflowId> --result-set <resultSetId> --select <selectToken> --format json`.

## Recommended workflow

### 1. Health check

Run:

```powershell
ailit doctor
```

If config or auth is missing:

- tell the user to run `ailit auth login`
- if the environment is non-TTY, prefer `ailit auth login --non-interactive --format json`
- if login returns `selection_required`, show the candidate list and continue with `--resume --result-set --select <selectToken>`
- after login, re-run `ailit doctor`

#### Login Methods And Procedure

##### Method 1: User-assisted login 

When the agent's browser is unavailable or the user prefers to use their own browser:


**Step 1: Start login server and immediately share the URL**

Use direct output redirection to capture URL immediately:

```powershell

ailit auth login --timeout 3m 

```
This outputs the auth URL immediately. Share this URL with the user:
- Example: `https://<domain_name>/#/?client_name=ailit-cli&mode=auth_code&redirect_uri=http%3A%2F%2F127.0.0.1%3A34203%2Fcallback&state=...`


**Step 2: User completes login in their browser**

User opens the URL, scans WeChat QR code, and logs in.

**Step 3: User provides the callback URL**

After login, the browser redirects to:
```
http://127.0.0.1:<port>/callback?auth_code=<code>&state=<state>
```

User copies this full callback URL and sends it to the agent.

**Step 4: Agent executes the callback**

```powershell
curl "http://127.0.0.1:<port>/callback?auth_code=<code>&state=<state>"
```

**Step 5: Verify login**

```powershell
ailit doctor
```

### 2. Search

Use the default output first:

```powershell
ailit customer search <keyword>
ailit product search <keyword>
ailit account search <keyword>
```

Only switch to JSON when the agent must parse fields programmatically:

```powershell
ailit customer search <keyword> --format json
ailit product search <keyword> --format json
ailit account search <keyword> --format json
```

Rules:

- If zero results are returned, ask the user for another keyword.
- If multiple results are returned in table/pretty mode, ask the user to select one.
- If multiple results are returned in JSON/NDJSON mode and the CLI responds with `selection_required`, do not guess. Present the returned numeric `selectToken`, `displayName`, and `fields` when available, falling back to `summary` only if `fields` is empty.
- Continue a chosen result with the same command plus `--result-set <resultSetId> --select <selectToken> --format json`, where `selectToken` is the numeric token the user chose from the displayed list.
- Only continue when customer, products, and account are unambiguous.

Example continuation:

```powershell
ailit product search 面巾纸 --format json
ailit product search --result-set <resultSetId> --select <selectToken> --format json
```

### 3. Dry run

Prepare a JSON draft file using the templates in `templates/`.

Run:

```powershell
ailit sale create --json <file> --dry-run
```

The default dry-run output already serves as the user-facing confirmation view. It should cover:

- shop
- warehouse
- customer
- line items
- bill date
- settlement mode
- settlement account when applicable
- total amount

Only use `--format json` when you need to inspect or parse the raw backend request payload. Do not dump the raw payload to the end user unless they ask for it.

### 4. Real create

Only after the user says the equivalent of `确认创建`, run:

```powershell
ailit sale create --json <file>
```

When the create succeeds, confirm the result with the returned bill code or document number first. Do not relay the raw sale ID to the end user unless they explicitly asked for IDs.

### 5. Query existing records

Query sales orders:

```powershell
ailit sale list --today
ailit sale list --week
ailit sale list --start 2024-01-01 --end 2024-01-31
ailit sale get <id>
```

Query stock:

```powershell
ailit stock list
ailit stock low               # 低库存预警（系统阈值）
ailit stock low --threshold 5 # 自定义阈值
ailit stock out               # 缺货商品
```

Query reports:

```powershell
ailit report all              # 综合报表（今日/本周/本月+热销，推荐优先使用）
ailit report today
ailit report week
ailit report month
ailit report hot-sale         # 今日热销排行
ailit report hot-sale --start 2024-01-01 --end 2024-01-31
```

Query debt and purchase:

```powershell
ailit customer debt           # 查询欠款客户列表
ailit purchase list --today
ailit purchase list --week
ailit purchase supplier
```

Rules:

- Prefer `ailit report all` for daily business overviews — it fetches today/week/month summaries and hot-sale in one call.
- For invalidation or deletion, always run `ailit sale get <id>` first to confirm with the user before executing.
- `ailit report` and `ailit sale list` do not support `--format csv`; do not attempt it.

## Draft file rules

Fields **auto-filled by CLI** (leave empty or omit in draft):

- `shopId` — filled from config `DefaultShopID`
- `warehouseId` — filled from config `DefaultWarehouseID`
- `operatorId` — filled from default operator API
- `billDate` — filled as today's date

Fields **you must provide**:

- `customer.id` and `customer.name`
- `lines[].productId`, `lines[].productSkuId`, `lines[].productName`
- `lines[].quantity` and `lines[].unitPrice`
- `settlement.mode` (`FULL` or `ON_ACCOUNT`)
- `accountId` when mode is `FULL`; do not set `accountId` when mode is `ON_ACCOUNT`

## Templates and examples

- Full payment template: `templates/sale-create-full.json`
- On-account template: `templates/sale-create-on-account.json`
- Sale return template: `templates/sale-return.json`
- Example command sequences: `examples.md`

## Login repair path

Preferred recovery when the CLI is not ready:

```powershell
ailit auth login
ailit doctor
```

Non-TTY recovery:

```powershell
ailit auth login --non-interactive --format json
ailit auth login --resume <workflowId> --result-set <resultSetId> --select <selectToken> --format json
ailit doctor
```

Only discuss manual config edits when the user is explicitly debugging a broken environment.
