---
name: stripe-link-cli
description: Agent payments via Stripe Link — cards, SPT, approvals.
version: 0.1.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Payments, Stripe, Link, Checkout, MPP]
    related_skills: [mpp-agent, stripe-projects]
---

# Stripe Link CLI 技能

该技能基于 [@stripe/link-cli](https://github.com/stripe/link-cli) 开发，使 Hermes 能够使用一次性虚拟卡或共享支付令牌（SPT）代表用户完成购买。每次消费都需通过 Link 移动端/网页应用内的内置审批流程——Hermes 无法自行批准。

目前仅支持美国地区（需拥有 Link 账户）。上游 CLI 不支持 Windows 系统，因此该技能仅可在 `[linux, macos]` 环境中使用。

## 适用场景

触发语句包括：

- “购买 X”、“为 X 支付”、“完成购买”、“结束结账”
- “给我一张卡”、“我需要一种支付方式”
- “登录 Link”、“连接我的 Link 钱包”
- 商家 API 返回 HTTP 402 响应且包含 `www-authenticate: ... method="stripe"` 字段

如果用户需要进行需要付费的 API 调用（出现 HTTP 402 错误且无结账表单），说明使用的 `card` 路径有误——应通过此技能使用 SPT，或转交给 `mpp-agent` 技能处理。

## 先决条件

- `PATH` 环境变量中已安装 Node.js 20+ 版本（可通过 `node --version` 查验）
- 用户需位于美国地区（需拥有 Link 账户）

在 Hermes 尝试付款之前，无需预先设置 Link 账户、支付方式或消费审批应用——CLI 在首次运行时会引导用户完成相关设置：

- 一个 https://app.link.com 上的 Link 账户：在首次使用 `link-cli` 进行身份验证时创建或关联
- 至少一种支付方式：在首次访问 https://app.link.com/wallet 时添加
- Link 移动端/网页应用：用于在收到首次消费请求时进行审批

无需配置任何环境变量——认证状态由 CLI 存储在其自身的配置目录中。

## 安装

只需全局安装一次即可：

```
npm install -g @stripe/link-cli
```

或者通过 `npx @stripe/link-cli` 命令进行临时调用。下述技能即采用了已安装的 `link-cli` 工具。

## 运行方式

所有命令均通过 `terminal` 工具执行。CLI 会自动识别非 TTY 环境下的调用，并默认输出简洁的 `toon` 格式结果——该格式已能满足模型的需求。如果某一步需要结构化字段，则可传递 `--format json` 参数。

查看可用命令：`link-cli --llms-full`。
在调用前查看某命令的架构定义：`link-cli <command> --schema`。

## 操作步骤

### 1. 检查/建立身份认证

```
link-cli auth status
```

如果尚未完成身份验证，请使用明确的客户端名称登录（该名称会显示在用户的 Link 应用中）：

```
link-cli auth login --client-name "Hermes" --interval 5 --timeout 300
```

`--interval`/`--timeout` 参数采用轮询方式，因此代理无需手动管理 `_next` 步骤。只需将验证网址及短语显示给用户，然后等待 CLI 返回结果即可。

**在 `auth status` 显示登录成功之前，请勿继续执行后续步骤。**

### 2. 在创建消费请求前对商户进行评估

首先确定凭证类型：

| 商户界面形式 | `--credential-type` |
|---|---|
| 标准网页结算表单 / Stripe Elements | `card`（默认值） |
| 返回 HTTP 402 错误，且 `www-authenticate` 中包含 `method="stripe"` | `shared_payment_token` |
| 返回 HTTP 402 错误，但 `www-authenticate` 中不包含 `method="stripe"` | 不支持 —— 应立即停止 |

对于返回 402 错误的响应，切勿手动解码挑战信息。直接传递原始请求头即可：

```
link-cli mpp decode --challenge '<full WWW-Authenticate header>'
```

该步骤用于验证挑战请求，并提取网络标识符以及解码后的请求体。

### 3. 列出支付方式与配送选项

```
link-cli payment-methods list
link-cli shipping-address list
```

除非用户另有指定，否则请使用第一个选项。`payment-methods list` 中的 `id` 值即为下一步操作中所需的 `--payment-method-id` 参数。

### 4. 创建支出请求

在执行此命令之前，请先与用户确认最终金额。所有金额均以分为单位。

```
link-cli spend-request create \
  --payment-method-id <pm_id> \
  --merchant-name "<name>" \
  --merchant-url "<url>" \
  --context "<one sentence: what is being purchased and why>" \
  --amount <cents> \
  --line-item "name:<item>,unit_amount:<cents>,quantity:1" \
  --total "type:total,display_text:Total,amount:<cents>" \
  --request-approval
```

对于 MPP 商家，请添加参数 `--credential-type shared_payment_token`。

`--request-approval` 会向用户的 Link 应用发送请求，并持续轮询直至用户批准或拒绝。若遭遇拒绝或超时，CLI 的退出码将为非零值。

### 5. 安全地获取凭证

**切勿将卡片信息输出到标准输出流。**请使用 `--output-file` 参数，这样卡号就永远不会出现在代理的记录或日志中：

```
link-cli spend-request retrieve <lsrq_id> \
  --include card \
  --output-file /tmp/link-card.json \
  --format json
```

该文件的权限设置为`0600`；标准输出仅显示已脱敏的字段（品牌名、卡号后四位、有效期），以及`card_output_file`的路径。

### 6. 使用凭证

- 对于网页支付场景：可将文件路径直接交给用户，或将其传递给能够直接从磁盘填充表单的浏览器操作工具。切勿通过`read_file`或`cat`命令将卡文件内容读取到智能体的推理上下文中。
- 对于MPP商家：

  ```
  link-cli mpp pay <merchant-url> \
    --spend-request-id <lsrq_id> \
    --method POST \
    --data '<json body>'
  ```

### 7. 清理操作

交易完成后应立即删除卡片文件：

```
rm -f /tmp/link-card.json
```

## 可选：以 MCP 服务器模式运行

使用 `@stripe/link-cli --mcp` 可通过标准输入输出提供与 MCP 工具相同的命令功能。若要将其注册到 Hermes 的原生 MCP 系统中：

```
hermes mcp add stripe-link --command "npx" --args "@stripe/link-cli --mcp"
```

此时执行 `hermes mcp list` 应该能显示 `stripe-link`。其审批规则依然适用——MCP 并不会跳过 Link 应用的审批步骤。

## 常见问题

- **仅限美国地区。** 在美国以外，`auth login` 操作将会失败。请告知用户无需反复尝试。
- **卡号 PAN 绝对不能进入代理上下文。** 每次操作都必须使用 `--output-file` 参数。如果之前未使用该参数就已获取了卡号信息，仅执行 `link-cli auth logout` 是不够的——虽然该卡号仅能使用一次，但遵循安全规范进行更换仍是必要的。
- **`--request-approval` 会一直阻塞直到用户操作。** 如果用户正在休息，CLI 会达到超时时间。请提前向用户说明这一点。
- **多步骤的 `_next` 命令。** 某些命令会返回 `_next.command`，必须执行该命令才能继续后续操作。如有疑问，建议优先使用内联轮询参数（`--interval`/`--timeout`）。
- 在非 TTY 模式下，输出格式默认为 `toon`。这种格式适用于普通文本，但如果后续步骤需要解析特定字段，则应使用 `--format json` 参数。
- **不要默认选择 `card` 类型。** 设置商户评估步骤（第 2 节）的目的就在于避免因选择错误的凭证类型而导致购买失败或泄露过多数据。

## 验证方法

```
link-cli --version && link-cli auth status
```

退出码为0表示已成功安装并完成登录。
