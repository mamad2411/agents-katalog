---
name: crypto
description: "Crypto triage：从密文、RSA 参数、AES 模式、哈希、PRNG 和协议证据选择具体密码分析流程。"
metadata:
  category: "crypto"
  keywords: "[\"crypto\",\"密码\",\"加密\",\"RSA\",\"AES\",\"hash\",\"PRNG\",\"nonce\",\"signature\",\"密文\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/crypto.md\",\"section\":\"# Crypto Skill\",\"start_line\":1,\"end_line\":175,\"sha256\":\"5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777\"}"
  resources: "[\"references/checklist.md\"]"
---

# 密码题分类与检查

## 适用前提
主要阻碍是加密、签名、哈希、PRNG、数学结构或类似密码分析的编码题。

## 工作流
1. 从源文件解析 n/e/c、iv、nonce、salt、seed、a/b/m、公钥和签名，识别 PEM/DER/JSON/Python/Sage/hex/base64，记录位长、块长度和重复块。
2. 优先验证编码、XOR、古典密码、ECB 重复块和 many-time pad 等有证据支持的简单路线；已提取的常量保存到脚本，不重复手抄大整数。
3. 按当前瓶颈加载专项 Skill：RSA 用 `rsa-factorization`，PRNG 用 `prng-analysis`，特定四轮 AES 用 `reduced-aes-integral`，复杂有状态协议用 `protocol-transcript`。
4. 其他分支按需读参考：CBC/CTR/GCM 的 oracle 或 nonce 复用、Hash/MAC、ECC 签名与群参数、格/整数环检查。
5. 写一个有界 `solve.py`，从文件解析参数，输出字节 hex/repr 与必要验证结果。

## 验证与失败处理
区分“看起来可读”和“符合原算法/原服务校验”；解密候选应执行重加密、方程检查或题目规定的验证。工具或数学前提不满足时记录限制，不盲目穷举。主要工作变为理解程序时转 Rev，密文仍需从媒体中提取时先 Forensics。

## 按需参考
`references/checklist.md` 保存非专项分支的原检查表；专项内容分别归属于上述四个 Skill，避免每次加载整份密码手册。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/crypto.md` 的 1–175 行（# Crypto Skill）。完整原文件 SHA-256：`5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

