---
name: x402-card
description: >
  Trigger this skill when the user expresses intent to create, manage, or query a virtual card.

  This includes intents such as:
  - "get a virtual card"
  - "create a card"
  - "card status"
  - "set up a card for an agent"

  Also, any request involving the creation of a one-time-use virtual Visa/Mastercard
  funded with cryptocurrency for agent use.
emoji: "💳"
homepage: https://github.com/AEON-Project/x402-card
metadata:
  version: "0.4.3"
  author: AEON-Project
  openclaw:
    requires:
      bins:
        - node
        - npx
    primaryEnv: X402_CARD_SERVICE_URL
    user-invocable: true
    disable-model-invocation: false
compatibility: 需要 Node.js >= 18 和 npm
---

# x402 虚拟卡技能

通过 x402 HTTP 支付协议，使用 BSC 链上的 USDT 为 Agent 创建一次性使用的虚拟借记卡（Visa/Mastercard）。

> ⚡ **Gas 模型**：
> BSC USDT 不支持 EIP-3009，建卡前客户端需做一次 `approve` 授权（链上交易），真正的 USDT 转账由服务端执行。
> - **建卡（x402）**：客户端需少量 BNB 完成 `approve` 授权 → 然后 EIP-712 签名（免 gas）→ 服务端提交转账（服务端付 gas）
> - **充值（topup）**：WalletConnect 一次连接，自动转 USDT + 0.001 BNB（用于 approve gas），用户需在钱包 App 内确认 **2 笔交易**
> - **赎回（withdraw）**：本地钱包直发 ERC20 transfer，需要 BNB 付 gas
> - **补 gas（gas）**：仅转 BNB（当 topup 时 BNB 转账失败或需要额外补充时用）

---

## 启动语（必读）

任何时候首次进入本技能，先输出一行启动语：

> Let me load the tool and check the existing environment first.

随后**立即**进入「步骤 1：预检查」。

---

## 命令一览

所有操作通过全局命令 `x402-card`。

> 📦 **前置安装**（仅一次）：
> ```bash
> npm install -g @aeon-ai-pay/x402-card@latest
> ```
> 用全局命令而非 `npx`，可避免每次 4-5 秒的冷启动延迟。
> 升级：`npm update -g @aeon-ai-pay/x402-card`。

```bash
x402-card setup --check                # 预检查 / 自动建钱包
x402-card setup --show                 # 查看配置
x402-card create --amount <usd> --poll # 创建虚拟卡
x402-card status --order-no <orderNo>  # 查询卡片状态
x402-card wallet                       # 查询本地钱包余额
x402-card topup --amount <usdt>        # 自动充值 USDT + BNB（WalletConnect, 2 笔确认）
x402-card gas [--amount <bnb>]         # 给本地钱包充 BNB（WalletConnect, 用于 withdraw）
x402-card withdraw [--to <addr>] [--amount <usdt>]  # 提取资金
```

配置存储在 `~/.x402-card/config.json`（权限 600）。
**绝不向用户索要私钥；本地钱包私钥由 CLI 自动生成。**

---

## 步骤 1：预检查（自动钱包初始化）

无论用户意图为何，**首先**运行：

```bash
x402-card setup --check
```

CLI 行为：
1. 读取 `~/.x402-card/config.json`
2. 若 `privateKey` 缺失 → 用 `viem.generatePrivateKey()` 在本地生成新私钥并保存
3. 返回 JSON：`{ ready, created, mode, address, mainWallet, serviceUrl, amountLimits }`

### 输出模板

固定先输出一行进度提示：

```
> Pre-check in progress...
```

#### 分支 A：钱包已存在（`ready: true`，`created: false`）

```
0x0...{last4} Ready. Proceed to create a card for your agent.
```

#### 分支 B：本次自动创建（`ready: true`，`created: true`）

```
Auto-creating your designated wallet...
0x0...{last4} Ready. Proceed to create a card for your agent.
```

> - `{last4}` 取自返回的 `address` 末 4 位
> - 记录 `amountLimits.{min,max}` 供后续金额校验使用
> - 预检查 **不联网**、**不查链上余额**、**不调用服务端**

### 边界场景

| 用户问 | 回应 |
| --- | --- |
| 「我的钱包地址是？」 | 直接展示 `setup --check` 返回的 `address` |
| 「我想导入自己的私钥」 | 不支持。CLI 仅自动生成本地钱包；如需自定义请手动编辑 `~/.x402-card/config.json` |
| 「能恢复钱包吗？」 | 不可。私钥仅存本地；建议提取资金前先备份配置文件 |

---

## 步骤 2：创建虚拟卡（含余额不足时自动充值）

触发：用户想 **buy / create / get a virtual card**。

### 2.0 金额确认

- 金额必须落在 `amountLimits.min ~ amountLimits.max`（来自步骤 1 返回，禁止硬编码）
- 若用户未指定金额，向用户展示有效区间并请求确认

### 2.1 执行创建

```bash
x402-card create --amount <usd> --poll
```

CLI 内部依次执行：
1. 参数与限额校验
2. 链上余额检查（USDT + BNB）
3. `approve` 授权（链上交易，消耗少量 BNB）
4. EIP-712 签名（免 gas）→ 服务端提交实际转账
5. 若带 `--poll` → 最多轮询 10 次，每次间隔 5 秒

输出首行：

```
> Creating Agent Card...
```

### 2.2 情况分支

#### 情况 A：金额超出范围

CLI 返回：
```json
{"error":"Amount must be at least $0.6 ...","min":0.6,"max":800}
```
向用户展示有效区间，请求重新确认。

#### 情况 A.1：BNB 不足（approve 授权需要 gas）

CLI 返回：
```json
{"error":"No BNB for approve transaction...","hint":"Run 'x402-card gas' or 'x402-card topup'"}
```

提示用户：
```
Balance check: no BNB for approve gas
→ Run 'x402-card topup' (includes BNB automatically)
→ Or run 'x402-card gas' to add BNB only
```

`topup` 会自动附带 0.001 BNB，**用户在钱包内确认 2 笔交易**（1 笔 USDT + 1 笔 BNB）。

#### 情况 B：USDT 充足，创建成功

CLI 输出 JSON 包含 `success: true` 与 `orderNo`。展示：

```
Card created successfully.
Order No: {orderNo}
Card: ****{last4}
Status: {orderStatus}
```

务必**记录 orderNo** —— 这是后续状态查询的唯一凭证。

#### 情况 C：USDT 余额不足 → 启动 WalletConnect 自动充值

CLI 返回：
```json
{"error":"Insufficient USDT balance","required":"5 USDT (approx)","available":"0 USDT","shortfall":"5.000000 USDT","address":"0x..."}
```

向用户展示（**文案必须完全一致**，下方变量替换为实际值，其余文字逐字保留）：

```
Balance check: insufficient
Required amount: {required} USDT

→ Fund manually: 0x0...{session_last4}
→ Or auto-authorize transfer by link: WalletConnect (will open QR code)
```

征得用户同意后执行：

```bash
x402-card topup --amount <required>
```

⚠️ **WalletConnect 流程为交互式，必须前台同步运行**：
- 终端打印 QR 码 + `wc:` URI
- 用户用钱包 App（MetaMask、Trust Wallet、imToken 等）扫码连接
- 在钱包 App 中确认 1 笔 USDT 转账（金额 = `<required>`，目标 = 本地钱包）
- 全过程最长 120 秒

> 🚫 **绝对禁止**：
> - 不要用 `run_in_background: true` 调用 `topup` / `gas` / `connect` 等 WalletConnect 命令
> - 不要在用户扫码完成前 kill 进程
> - 一旦命令进入后台或被中断，**即使用户在钱包内已签名**，CLI 也无法记录 `mainWallet` 与确认链上回执 → 会出现"已支付但未被检测"的假象
>
> 🔧 **如果误把 `topup` 放到后台并已 kill**：
> 用户的链上交易**很可能已经发出**（USDT 实际已到本地钱包）。
> 此时**不要重新 topup**，直接：
> 1. 跑 `x402-card wallet` 确认 USDT 已到账
> 2. 若到账，直接重跑原 `create --amount <usd> --poll`
> 3. 若未到账（用户也没真扫码），再前台 `topup`

输出阶段提示：

```
> Funding flow triggered...
Initializing WalletConnect session...
Waiting for wallet confirmation...
USDT transfer confirmed.
```

#### 情况 C.1：用户在钱包内拒绝交易

CLI 返回 `"error": "Transaction rejected in wallet."`。
告知用户本次充值已取消，询问是否重试。**不要自动重试**。

#### 情况 C.2：WalletConnect 超时（120s 未扫码或未确认）

CLI 返回连接/超时错误。告知用户超时，建议重新执行 `topup`。

#### 情况 C.3：主钱包 USDT 不足（链上 revert）

CLI 返回 `"error": "USDT transfer failed: ..."`。展示：

```
> Funding flow triggered...

Source balance insufficient
Funding aborted
- 需要: {required}
- 可用: {available}
Add funds to continue
```

提示用户向其主钱包补 USDT，**不要循环重试**。

#### 情况 C.4：充值成功 → 自动重试创建

`topup` 返回 `success: true` 后，CLI 已自动把 `mainWallet` 字段写回 config（提取资金时会用到）。

**自动重试一次** `create`：
```bash
x402-card create --amount <usd> --poll
```
若再次失败，按对应分支处理；不要进入第三次重试。

#### 情况 D：服务端网络/调用失败

CLI 返回 `success: false` 及 HTTP 错误。展示原始错误，建议用户稍后重试或检查 `serviceUrl`。

#### 情况 E：轮询超时（`--poll` 用满 10 次）

CLI 输出：
```
Polling timeout after 10 attempts. Check manually with: x402-card status --order-no {orderNo}
```
告知用户卡片仍在处理中，记下 `orderNo`，稍后用步骤 3 查询。**禁止继续轮询。**

详细字段见 [create-card](references/create-card.md)。

---

## 步骤 3：查询卡片状态

触发：用户想 **check / query card status**。

### 3.1 命令

```bash
x402-card status --order-no <orderNo>
x402-card status --order-no <orderNo> --poll  # 轮询直至终态
```

### 3.2 输出模板

```
> Fetching card status...

Card: ****{last4}
State: {Active | Used | Expired | Pending | Failed}
Remaining balance: {balance} USD
Usage: {used} / {total} (single-use)
```

### 3.3 边界场景

| 情况 | 处理 |
| --- | --- |
| 用户没有 orderNo | 询问最近一次 `create` 输出中的 `orderNo`；无则告知无法查询 |
| orderNo 无效 / 服务端返回空 | 展示原始错误，建议用户核对 orderNo |
| 状态为 Pending | 提示卡片仍在处理；可选轮询，但仍不超过 10 次 |
| 状态为 Failed | 告知失败原因；订单已无效，需重新 `create` |

详细字段见 [check-status](references/check-status.md)。

---

## 步骤 4：钱包管理

触发：用户想 **查询余额 / 追加充值 / 提取资金**。

### 4.1 查询本地钱包余额

```bash
x402-card wallet
```

输出本地钱包 USDT 余额及地址。若曾通过 `topup` 充值，会附带主钱包余额。

### 4.2 追加充值（同 2.C 流程）

```bash
x402-card topup --amount <usdt>               # USDT + 0.001 BNB（默认）
x402-card topup --amount <usdt> --skip-gas     # 仅 USDT，不附带 BNB
```

`topup` 默认在一次 WalletConnect 会话内**同时转 USDT 和 0.001 BNB**，用户需在钱包 App 内依次确认 **2 笔交易**：
1. 第 1 笔：USDT（指定金额）
2. 第 2 笔：0.001 BNB（用于 BSC USDT approve 授权的 gas）

若第 2 笔 BNB 失败（如拒绝或余额不足），**不阻断**——USDT 已到账，BNB 可后续用 `x402-card gas` 单独补充。

### 4.3 提取资金到主钱包

```bash
x402-card withdraw                                  # 提全部 USDT 到记录的 mainWallet
x402-card withdraw --amount <usdt>                  # 指定金额
x402-card withdraw --to 0xMainWallet                # 指定目标地址
x402-card withdraw --to 0xMainWallet --amount <usdt>
```

> ⚠️ **withdraw 需要 BNB 作为 gas**：
> 与 x402 建卡（gasless）不同，`withdraw` 是本地钱包**直发的链上 ERC20 transfer**，
> 必须由本地钱包自己支付 BNB gas（建议 ≥ 0.0005 BNB）。
> 用户需要从交易所或自己钱包向本地钱包地址手动转入少量 BNB 才能赎回。

#### 目标地址解析优先级

1. CLI 参数 `--to <address>`
2. `~/.x402-card/config.json` 中的 `mainWallet`（**仅在用户曾用过 `topup` 后才会有**）

#### 输出模板（**文案必须完全一致**，仅变量替换）

```
> Reclaiming funds...

From: 0x0...{session_last4}
To: main wallet (0x0...{main_last4})

Amount: {amount} USDT
Status: completed
```

> 字面 "main wallet" 标签是规格要求，**不要省略**；括号内地址用于让用户确认转账目标。

#### 边界场景

| 错误 | 含义 | 处理 |
| --- | --- | --- |
| `No main wallet address found. Use --to <address>` | 配置无 mainWallet 且未传 `--to` | 询问用户提供目标地址 |
| `No USDT to withdraw.` | 本地钱包 USDT 余额为 0 | 告知无可提取，建议先 `topup` |
| `No BNB for gas. ...` | 本地钱包无 BNB，无法支付 gas | 提示用户运行 `x402-card gas` 通过 WalletConnect 充入少量 BNB；详见 4.4 |
| `Requested X USDT but only Y available` | `--amount` 大于实际余额 | 展示实际余额，请求重新确认 |
| `Withdraw failed: ...` | 链上交易失败 | 展示原始错误，建议稍后重试 |

### 4.4 为本地钱包补 gas（BNB）

当 `withdraw` 报 `No BNB for gas` 时，使用专用 `gas` 子命令通过 WalletConnect 从主钱包转少量 BNB 进来。

```bash
x402-card gas                    # 默认 0.001 BNB
x402-card gas --amount 0.002     # 自定义金额
```

⚠️ **此命令为交互式 WalletConnect 流程**（与 `topup` 同机制）：
- 终端打印 QR 码 + `wc:` URI
- 用户用钱包 App 扫码连接主钱包
- 在钱包内确认 1 笔 BNB 转账（金额 = `<amount>`，目标 = 本地钱包）
- 最长等待 120 秒，**不可后台运行**

成功后会自动把 `mainWallet` 写回 config（后续 withdraw 可省略 `--to`）。

#### 输出模板

```
> Topping up gas...
Initializing WalletConnect session...
Waiting for wallet confirmation...
BNB transfer confirmed.

Local wallet: 0x0...{last4}
Balance: {bnb} BNB
```

#### 边界场景

| 错误 | 处理 |
| --- | --- |
| `Transaction rejected in wallet.` | 告知用户已取消，询问是否重试，**不自动重试** |
| `BNB transfer failed: ...` | 主钱包 BNB 不足或链上 revert，提示用户先在主钱包准备 BNB |
| WalletConnect 120s 超时 | 告知超时，建议重新执行 `gas` |

---

## 决策路由总览

| 用户意图 | 入口命令 |
| --- | --- |
| 任何首次进入 / 不确定状态 | `setup --check` |
| 查看当前配置 / 钱包地址 | `setup --show` |
| 创建虚拟卡 | `create --amount <n> --poll` |
| Session Key USDT 不足时充值 | `topup --amount <n>` |
| 查询卡片状态 | `status --order-no <n>` |
| 查询本地钱包余额 | `wallet` |
| 提取资金到主钱包 | `withdraw [--to <addr>] [--amount <n>]` |
| 为本地钱包补 BNB（withdraw 前置） | `gas [--amount <bnb>]` |
| 了解 x402 协议本身 | 阅读 [x402-protocol](references/x402-protocol.md) |

---

## 文案一致性约束（必读）

以下 **关键短语** 与 **行级输出模板** 必须**逐字一致**，不得改写、翻译、增减字符（包括标点、空格、`>` 前缀和大小写）：

### 行级模板（必须完全一致）

| 步骤 | 模板首行 |
| --- | --- |
| 预检查 | `> Pre-check in progress...` |
| 自动建钱包 | `Auto-creating your designated wallet...` |
| 钱包就绪 | `0x0...{last4} Ready. Proceed to create a card for your agent.` |
| 创建卡片 | `> Creating Agent Card...` |
| 余额不足首行 | `Balance check: insufficient` |
| 充值流程 | `> Funding flow triggered...` |
| 主钱包不足 | `Source balance insufficient` / `Funding aborted` / `Add funds to continue` |
| 查询状态 | `> Fetching card status...` |
| 提取资金 | `> Reclaiming funds...` |
| 提取目标行 | `To: main wallet (0x0...{last4})` |
| 提取状态行 | `Status: completed` |

### 关键短语（必须保留原词）

- `Balance check`、`insufficient`、`Required amount`
- `Fund manually`、`auto-authorize transfer by link`
- `Source balance insufficient`、`Funding aborted`、`Add funds to continue`
- `Card`、`State`、`Remaining balance`、`Usage`、`single-use`
- `From`、`To`、`Amount`、`Status`、`completed`
- `main wallet`（withdraw 目标行的字面文字）

### 变量映射

| 占位符 | 来源 |
| --- | --- |
| `{last4}` | `setup --check` / `wallet` / `withdraw` 输出中 `address` 的末 4 位 |
| `{required}` | `create` 错误返回的 `required` 字段 |
| `{available}` | `create` 错误返回的 `available` 字段；或 `topup` 错误中显式数值 |
| `{amount}` | `withdraw` 输出 `withdrawn` 字段 |
| `{orderNo}` | `create` 输出 `orderNo` 字段 |

### 禁止的偏离

- ❌ 翻译为中文（如 "余额检查：不足"）
- ❌ 改大小写（如 "Balance Check"）
- ❌ 简写（如 "BNB insuff."）
- ❌ 加额外修饰（如 emoji、加粗、`✅`）
- ❌ 拆行或合并行
- ❌ 用同义词替换（如把 `insufficient` 换成 `not enough`）

---

## 全局禁止行为

- **绝不**向用户索要私钥；本地钱包由 CLI 自动生成
- **绝不**在未经用户确认金额的情况下执行 `create` 或 `topup`
- **绝不**记录或显示完整私钥；地址展示为 `0x0...last4` 格式
- **绝不**跳过 `setup --check` 直接执行其他命令
- **绝不**让 `topup` / `gas` / 任何 WalletConnect 命令在后台运行（必须前台同步等待）。误后台导致的"已支付未检测"问题，按步骤 2 情况 C 的「如果误把 topup 放到后台」恢复
- **不要**在 `topup` 失败后无限重试，按对应模板提示后停止
- **不要**轮询 `status` 超过 10 次；超时即停，提示用户记下 `orderNo` 自行查询
- **不要**自行编造 `amountLimits`；始终使用 `setup --check` 返回的 `min/max`
