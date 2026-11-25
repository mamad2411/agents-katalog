---
name: mpp-agent
description: Pay HTTP 402 APIs via Machine Payments Protocol (MPP).
version: 0.1.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Payments, MPP, HTTP-402, Tempo, Stripe]
    related_skills: [stripe-link-cli, stripe-projects]
---

# MPP Agent 技能

该技能用于封装 Machine Payments Protocol（MPP，https://mpp.dev）客户端，使得 Hermes 能够针对返回 `HTTP 402 Payment Required` 响应的服务器，按请求次数进行 API 支付。

共有三种客户端选项，均通过 npm 分发。请选择最轻量级且能满足用户需求的方案。目前该功能仅在 `[linux, macos]` 系统上可用，待 Windows 平台的支付工具成熟后将进一步开放。

## 适用场景

- 商家 API 返回带有 `www-authenticate` 标头的 `HTTP 402` 响应——且用户希望实际完成支付，而不仅仅是记录响应信息。
- 用户要求“按请求付费”、“创建代理钱包”、“使用 Tempo / Privy / AgentCash”，或希望查找按 MPP 定价的服务。
- 使用 Stripe Link 进行消费后产生了共享支付令牌（SPT），且代理需要将其附加到 402 挑战请求中——在这种情况下，建议使用 `link-cli mpp pay`（参见 `stripe-link-cli` 技能）。

## 客户端选择

| 工具 | 适用场景 | 设置方式 |
|---|---|---|
| `link-cli` | 用户已配置 Stripe Link，或 402 挑战请求中指定了 `method="stripe"` | 参见 `stripe-link-cli` 技能 |
| Tempo Wallet | 需要消费控制及服务发现功能的 MPP 服务 | 执行 `tempo wallet login` |
| Privy Agent CLI | 多链钱包、基于浏览器的充值功能 | 执行 `privy-agent-wallets login` |
| AgentCash | 通过一个 USDC.e 账户访问 300 多种预定价 API | 执行 `npx agentcash onboard` |
| `mppx` | 开发与调试场景，依赖项最少 | 先执行 `npm install -g mppx`，再执行 `mppx account create` |

默认情况下：如果用户已配置 Stripe Link，或 402 挑战请求指定了 `method="stripe"`，则使用 `link-cli mpp pay`（即 `stripe-link-cli` 技能）；否则，一次性付费调用及调试时选用 `mppx`，而用户需要持久性消费控制功能时则选用 Tempo Wallet。

## 先决条件

- `PATH` 环境变量中已安装 Node.js 20+ 版本
- 已充值的钱包（Tempo / Privy / AgentCash）或 `mppx` 账户
- 对于 Tempo / Privy / AgentCash，需按照其对应的入门指南进行操作：
  - `https://tempo.xyz/SKILL.md`
  - `https://agents.privy.io/skill.md`
  - `https://agentcash.dev/skill.md`

如果用户选择了某款工具，可使用 `web_extract` 工具获取相应的 SKILL.md 文件。

## 操作步骤（mppx，最快路径）

所有命令均在 `terminal` 工具中执行。

### 1. 安装并创建账户

```
npm install -g mppx
mppx account create
```

请将生成的账户凭证存储在 CLI 指定的位置（CLI 会将其保存在自己的配置文件中——切勿将其粘贴到代理的记录中）。

### 2. 检查商家的 402 挑战请求

如果用户提供了某个 URL，请先对其进行探测，以确认该 URL 确实使用的是 MPP 协议：

```
curl -i <url>
```

真正的 MPP 402 看起来如下：

```
HTTP/1.1 402 Payment Required
www-authenticate: tempo amount=0.1 currency=...
```

### 3. 提交请求以进行支付

```
mppx <url>
```

对于非 GET 方法或请求体：

```
mppx <url> --method POST --data '<json>'
```

`mppx` 会自动处理 402 挑战与凭证验证流程，成功时还会输出商家的实际响应内容。

### 4. 验证收据

`mppx` 会自动添加收据头部信息。如需查看该信息：

```
mppx <url> -v
```

## 操作步骤（Tempo 钱包）

官方参考文档为 https://tempo.xyz/SKILL.md 中的 Tempo 钱包技能说明；请使用 `web_extract` 工具获取该文档并据此操作。标题：

```
tempo wallet login
tempo wallet pay <url>
```

支出控制功能与服务发现功能均集成在 https://wallet.tempo.xyz 的钱包用户界面中。

## 常见问题

- **若请求未设置 `method="stripe"` 且返回 `HTTP 402`，则 Stripe Link 无法完成支付。** 如果验证页面仅支持 Tempo 其他支付方式，请使用 `mppx`（或对应其他钱包的客户端）——否则 Stripe Link 会拒绝该请求。反之，若验证页面明确标注了 `method="stripe"`，建议通过 `stripe-link-cli` 技能使用 Stripe Link，以便通过用户已授权的信用卡完成支付。
- **一个请求头中包含多种支付方式。** `www-authenticate` 请求可能列出多种支付方式（例如 `tempo, stripe`）。Stripe Link CLI 的 `mpp decode` 功能会优先选择 Stripe 方式，而 `mppx` 则会选择 Tempo 方式。并不存在唯一的“正确”客户端——需根据用户已充值的使用钱包来选择。
- **零金额验证请求。** 某些 MPP 接口会收取 `$0.00` 的费用，仅需要用户的认证凭证即可。此类请求无需使用已充值的钱包即可处理，不应将其视为“故障”而予以拒绝。
- **钱包密钥绝不会进入智能体上下文。** 四种客户端都会将密钥存储在各自的配置目录中（Privy 客户端则会为每次会话生成临时密钥对），切勿使用 `cat`/`read_file` 命令读取这些密钥。
- **服务器端 MPP 是独立的技能模块。** 如果用户希望在自己的 API 中集成 402 功能，此技能模块并不适用——请引导他们前往 https://mpp.dev/quickstart/server，以及 `mppx/nextjs` / `mppx/hono` / `mppx/express` / `mppx/elysia` 等中间件文档。未来可能会推出专门的 `mpp-server` 技能模块。

## 验证方式

```
mppx --version && mppx account list
```

退出码为 0 表示该组件已成功安装且存在对应账户。
