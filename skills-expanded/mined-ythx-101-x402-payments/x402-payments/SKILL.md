---
name: x402-payments
description: x402 protocol payment client for AI agents — auto-pay HTTP 402 responses with USDC on Base, check balance, transfer USDC, with an encrypted wallet and per-payment spending cap. Use when an agent needs to pay for an x402-protected API or send USDC on Base.
---

# x402-payments

x402 协议支付客户端 — 让 AI Agent 自主完成链上微支付。

## 概述
基于 [Coinbase x402](https://x402.org) 协议，通过 HTTP 402 响应实现 Agent 自主支付。支持 Base 链上 USDC 稳定币交易。

## 用法

### 生成钱包
```bash
python3 scripts/generate_wallet.py
```
生成新钱包，私钥 AES-256-GCM 加密存储到 `.wallet.json`。

### 查询余额
```bash
python3 scripts/balance.py [--address 0x...]
```

### x402 支付请求
```bash
python3 scripts/pay.py --url <402-endpoint> [--max-amount 1.0]
```
自动处理 HTTP 402 响应，解析支付要求，签名并发送交易。

### 转账
```bash
python3 scripts/transfer.py --to <address> --amount <usdc_amount>
```

## 环境变量
| 变量 | 说明 | 必需 |
|------|------|------|
| `X402_WALLET_PATH` | 钱包文件路径 | 否（默认 `.wallet.json`）|
| `X402_WALLET_PASSWORD` | 钱包解密密码 | 是 |
| `X402_RPC_URL` | Base 链 RPC | 否（默认公共 RPC）|
| `X402_MAX_AMOUNT` | 单次最大支付 USDC | 否（默认 1.0）|
| `X402_HTTP_TIMEOUT` | HTTP 请求超时（秒）| 否（默认 30）|

## 安全
- 私钥 AES-256-GCM + PBKDF2-SHA256 加密存储（旧版 CBC 钱包仅兼容读取）
- 仅支持 Base 主网，操作的是真实资金
- 支付前检查金额上限
- 不存储明文密钥
- 所有敏感信息通过环境变量传入

## 依赖
需要 Python 3.10+。
```bash
pip install -r requirements.txt
```
```
web3>=7.0,<8
pycryptodome>=3.19
requests>=2.31
```

## 限制
本技能使用简化版 x402 流程（直接链上 USDC 转账，并在 `X-PAYMENT` 头带交易哈希），可能与标准 x402 服务器不兼容，详见 [README 的 Limitations](README.md#limitations)。
