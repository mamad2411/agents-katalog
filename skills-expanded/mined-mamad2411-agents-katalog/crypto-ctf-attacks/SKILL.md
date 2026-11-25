---
name: crypto-ctf-attacks
description: CTF密码学攻击知识库 — RSA攻击（小指数/共模/Wiener/Coppersmith）、AES攻击（Padding Oracle/ECB字节翻转/GCM
  nonce重用）、ECC攻击、LFSR/LCG/PRNG攻击、古典密码、LWE格攻击。Use when performing authorized penetration
  testing, CTF, or security assessment tasks related to ctf-crypto.
version: 1.0.0
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes_origin: import
  upstream_source_path: /skills/specialized/ctf-crypto/SKILL.md
  upstream_original_name: ctf-crypto
tags:
- red-teaming
- penetration-testing
- security
- imported
related_skills:
- pentest-workflow
- pentest-quick-checklist
- pentest-tool-setup
- ctf-web-attacks
---

# CTF 密码学攻击知识库

针对 CTF Crypto 题目的实战攻击知识库，提供**具体攻击参数、数学公式、Python 代码片段**。

**与 `-crypto-toolkit` 的区别**：
- `-crypto-toolkit` → 编解码操作工具（base64 解码、MD5 哈希、AES 加解密）
- `crypto-ctf-attacks` → 密码学攻击知识（RSA 小指数攻击怎么做、Padding Oracle 怎么利用）

## 核心原则

1. **先识别加密体系** — 看密钥长度、加密模式、已知量，确定攻击方向
2. **工具验证** — 使用 `python_execute` 执行攻击代码，用 `crypto_decode` 做辅助编解码
3. **参数敏感** — 密码学攻击对参数极其敏感，必须精确计算

## 场景路由

| 场景 | 参考文档 | 核心攻击 |
|------|---------|---------|
| RSA 攻击 | `rsa-attacks-cheatsheet.md` | 小e/共模/Wiener/Pollard/Fermat/Coppersmith |
| AES/分组密码攻击 | `aes-and-block-cipher-attacks.md` | ECB翻转/Padding Oracle/GCM nonce重用 |
| ECC 攻击 | `ecc-attacks-cheatsheet.md` | 小子群/invalid curve/Smart/Pohlig-Hellman |
| PRNG/流密码攻击 | `prng-and-stream-cipher-attacks.md` | MT19937/LCG/LFSR/RC4 |
| 古典密码 | `classic-cipher-attacks.md` | Vigenere/XOR频率分析/OTP重用 |
| 格攻击 | `lattice-and-lwe-attacks.md` | LLL/BKZ/HNP/LWE embedding |

## 快速判题指南

| 题目特征 | 可能攻击 | 推荐参考 |
|---------|---------|---------|
| 给了 n, e, c | RSA | rsa-attacks-cheatsheet.md |
| e=3 或 e 很小 | RSA 小指数攻击 | rsa-attacks-cheatsheet.md |
| 多组 (n, e, c) 且 n 相同 | RSA 共模攻击 | rsa-attacks-cheatsheet.md |
| n 很大但 e 很大 | Wiener 攻击 | rsa-attacks-cheatsheet.md |
| AES-CBC + 解密 oracle | Padding Oracle | aes-and-block-cipher-attacks.md |
| AES-ECB + 可控明文 | ECB 字节翻转 | aes-and-block-cipher-attacks.md |
| 椭圆曲线参数 | ECC 攻击 | ecc-attacks-cheatsheet.md |
| 给了随机数序列 | PRNG 预测 | prng-and-stream-cipher-attacks.md |
| 给了密文和部分明文 | XOR/流密码 | classic-cipher-attacks.md |
| 矩阵/向量运算 | 格攻击 | lattice-and-lwe-attacks.md |

## Hermes 使用適配

- 來源為  專案技能，已匯入 Hermes 本地 skill。僅在**已授權**滲透測試、CTF、內部安全評估或防禦驗證範圍內使用。
- 原文若提到 `fetch`，在 Hermes 中優先使用 `web_extract`、`browser` 或 `terminal(curl/HTTPie)` 取得真實回應。
- 原文若提到 `python_execute`，在 Hermes 中使用 `execute_code` 或 `terminal(python3 ...)`；計算、編碼、hash、PoC 驗證必須用工具實測，不靠猜。
- 原文若提到 MCP/Burp/adb/frida/jadx/chrome_devtools 等外部工具：先確認本機是否安裝或可用；不可用時以 Hermes 現有 `web`、`browser`、`terminal`、`file`、`vision` 工具替代，並明確標註限制。
- 下一次滲透任務中，先載入 `-pentest-flow` 做總路由，再依場景載入本系列專項 skill（例如 `-web-security-advanced`、`-osint-recon`、`-rapid-checklist`）。

## 來源與維護

- 原始 skill 已保存於 `references/upstream-skill.md`；README/LICENSE 已保存於 `references/`。
