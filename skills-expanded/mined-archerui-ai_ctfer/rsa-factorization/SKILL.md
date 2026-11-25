---
name: rsa-factorization
description: "已获取 RSA n/e/c 时解析并核对参数，优先检查 FactorDB 和结构弱点，用方程验证解密结果。"
metadata:
  category: "crypto"
  keywords: "[\"RSA\",\"n e c\",\"FactorDB\",\"factorization\",\"分解\",\"共模\",\"共享素数\",\"low exponent\",\"Wiener\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/crypto.md\",\"section\":\"RSA checklist:\",\"start_line\":25,\"end_line\":71,\"sha256\":\"5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777\"}"
  resources: "[\"references/checklist.md\"]"
---

# RSA 参数与分解路线

## 适用前提
输入包含 RSA 公钥/密文或相关泄漏。先确认 n、e、c 的来源、位长、消息编码和题目使用方式。

## 工作流
1. 从文件解析参数并在单一脚本中保存，避免反复手抄长整数。公钥可用 `openssl rsa -pubin -in key.pub -text -noout` 查看。
2. 原来源建议优先使用已有 `rsa_factordb --file chall.py` 查询公开分解数据；多文件参数在脚本中统一解析。helper 不适用时再考虑参考中的 API 调用。
3. 核对得到的因子与原模数，只有满足实际 RSA 结构和可逆性条件才计算私钥与明文。检查 `decrypt_status` 以及明文字节输出。
4. 没有已知分解时按证据检查低指数、共模、广播、近素数、小私钥、跨模数 GCD、CRT 参数或部分泄漏。
5. 本地分解只针对规模和结构合适的输入；检查可用工具并设置超时。随机均衡大半素数缺少适用工具时明确说明限制。

## 验证与失败处理
先验证因子乘积与模数、私钥方程及重加密，再按题目编码解释明文。返回已知因子不保证消息可直接恢复；FactorDB 无结果也不证明模数不存在弱点。对同一不适用的 Pollard rho/Fermat 路线不循环重试。

## 按需参考
`references/checklist.md` 保留原 RSA 检查表、helper 和有界命令模板。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/crypto.md` 的 25–71 行（RSA checklist:）。完整原文件 SHA-256：`5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

